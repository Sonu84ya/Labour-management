from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_initials(user):
    """Return 2-letter initials for a user."""
    if not user:
        return '?'
    name = user.get_full_name() if hasattr(user, 'get_full_name') else str(user)
    if name.strip():
        parts = name.strip().split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        return name[:2].upper()
    return (user.username[:2].upper() if hasattr(user, 'username') else str(user)[:2].upper())

@register.filter
def mul(value, arg):
    """Multiply value by arg."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def sub(value, arg):
    """Subtract arg from value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value, total):
    """Return percentage of value out of total."""
    try:
        t = float(total)
        if t == 0:
            return 0
        return int((float(value) / t) * 100)
    except (ValueError, TypeError):
        return 0

@register.filter
def stars(value):
    """Return HTML star string for a rating value."""
    try:
        v = round(float(value))
    except (ValueError, TypeError):
        v = 0
    filled = '★' * v
    empty  = '☆' * (5 - v)
    return mark_safe(f'<span style="color:#E8A020;">{filled}</span><span style="color:#EDD9BC;">{empty}</span>')

@register.simple_tag
def avatar_color(user_id):
    """Return a deterministic gradient based on user id."""
    colors = [
        ('135deg, #C1440E, #E8A020'),
        ('135deg, #4A7C59, #4A90B8'),
        ('135deg, #4A90B8, #8A7060'),
        ('135deg, #5C3D28, #C1440E'),
        ('135deg, #E8A020, #C1440E'),
        ('135deg, #3D2B1F, #4A7C59'),
    ]
    return f'linear-gradient({colors[int(user_id) % len(colors)]})'
