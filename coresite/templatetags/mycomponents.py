from django import template

register = template.Library()

@register.inclusion_tag('components/navbar.html', takes_context=True)
def navbar(context):
    user = context['request'].user
    return {
        'user': user,
        'is_authenticated': user.is_authenticated
    }

    