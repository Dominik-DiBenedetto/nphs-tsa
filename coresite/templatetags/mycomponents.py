from django import template

register = template.Library()

@register.inclusion_tag('components/navbar.html', takes_context=True)
def navbar(context, active_navbar_link, active_sidebar_link):
    user = context['request'].user
    return {
        'user': user,
        'is_authenticated': user.is_authenticated,
        'active_navbar_link': active_navbar_link,
        'active_sidebar_link': active_sidebar_link
    }

    