from django import template
from django.utils.timezone import now

register = template.Library()


@register.simple_tag(name='deltadate')
def deltadate(created):
    delta = now() - created
    minutes = int(delta.total_seconds() / 60)
    if minutes <= 60:
        return "a few minutes ago"
    elif 1440 >= minutes > 60:
        return str(minutes // 60) + " hours ago"
    elif 44640 >= minutes > 1440:
        return str(minutes // 1440) + " days ago"
    elif 16293600 >= minutes > 44640:
        return str(minutes // 44640) + " month ago"
