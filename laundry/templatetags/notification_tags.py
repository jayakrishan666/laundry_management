from django import template
from django.db.models import Q

register = template.Library()

@register.filter
def unread_notifications(user):
    if not user.is_authenticated:
        return 0
    return user.notification_set.filter(is_read=False).count() 