from django import template

register = template.Library()

@register.filter
def replace_string(value, arg):
    value = str(value)
    old_substring, new_substring = arg.split(',')
    return value.replace(old_substring, new_substring)