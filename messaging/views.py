from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Conversation, Message
from accounts.models import User
from jobs.models import Job


@login_required
def inbox_view(request):
    conversations = request.user.conversations.prefetch_related(
        'participants', 'messages', 'job'
    ).order_by('-updated_at')

    total_unread = sum(
        c.messages.filter(is_read=False).exclude(sender=request.user).count()
        for c in conversations
    )

    return render(request, 'messaging/inbox.html', {
        'conversations': conversations,
        'total_unread': total_unread,
        'active_conversation': None,
        'other_user': None,
        'messages_list': [],
    })


@login_required
def conversation_view(request, conv_id):
    conversation = get_object_or_404(
        Conversation, id=conv_id, participants=request.user
    )

    # Mark all incoming messages as read
    conversation.messages.filter(
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)

    all_conversations = request.user.conversations.prefetch_related(
        'participants', 'messages', 'job'
    ).order_by('-updated_at')

    other_user  = conversation.participants.exclude(id=request.user.id).first()
    messages_list = conversation.messages.select_related('sender').order_by('created_at')

    total_unread = sum(
        c.messages.filter(is_read=False).exclude(sender=request.user).count()
        for c in all_conversations
    )

    return render(request, 'messaging/inbox.html', {
        'conversations':      all_conversations,
        'active_conversation': conversation,
        'messages_list':      messages_list,
        'other_user':         other_user,
        'total_unread':       total_unread,
    })


@login_required
def start_conversation_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if other_user == request.user:
        return redirect('inbox')

    job_id = request.GET.get('job_id')

    # Look for an existing conversation between these two
    qs = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    )
    if job_id:
        qs = qs.filter(job_id=job_id)

    conv = qs.first()

    if not conv:
        job = None
        if job_id:
            try:
                job = Job.objects.get(id=job_id)
            except Job.DoesNotExist:
                pass
        conv = Conversation.objects.create(job=job)
        conv.participants.add(request.user, other_user)

    return redirect('conversation', conv_id=conv.id)


@login_required
@require_POST
def send_message_view(request, conv_id):
    conversation = get_object_or_404(
        Conversation, id=conv_id, participants=request.user
    )

    content   = request.POST.get('content', '').strip()
    msg_type  = request.POST.get('msg_type', 'text')
    voice_f   = request.FILES.get('voice_file')

    if not content and not voice_f:
        return redirect('conversation', conv_id=conv_id)

    msg = Message(
        conversation  = conversation,
        sender        = request.user,
        content       = content,
        message_type  = 'voice' if voice_f else 'text',
    )
    if voice_f:
        msg.voice_file = voice_f
    msg.save()

    # Bump conversation updated_at so it rises to the top
    Conversation.objects.filter(id=conv_id).update(updated_at=timezone.now())

    # AJAX / fetch response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'id':               msg.id,
            'content':          msg.content,
            'sender_name':      msg.sender.get_full_name() or msg.sender.username,
            'sender_initials':  msg.sender.get_initials(),
            'time':             msg.created_at.strftime('%I:%M %p'),
            'is_voice':         msg.message_type == 'voice',
        })

    return redirect('conversation', conv_id=conv_id)
