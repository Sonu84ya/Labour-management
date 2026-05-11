from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.inbox_view,               name='inbox'),
    path('<int:conv_id>/',          views.conversation_view,        name='conversation'),
    path('start/<int:user_id>/',    views.start_conversation_view,  name='start_conversation'),
    path('<int:conv_id>/send/',     views.send_message_view,        name='send_message'),
]
