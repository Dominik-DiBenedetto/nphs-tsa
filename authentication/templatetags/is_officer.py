# group_tags.py
from django import template

register = template.Library()

@register.filter(name='is_officer')
def is_officer(user):
    return user.groups.filter(name="Officer").exists()
