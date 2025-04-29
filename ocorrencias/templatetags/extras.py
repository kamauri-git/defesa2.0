from django import template

register = template.Library()

@register.filter
def pluck(queryset, campo):
    return [obj[campo] for obj in queryset]
