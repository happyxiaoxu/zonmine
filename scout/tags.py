from django import template

register = template.Library()

@register.filter
def mysplit(value, key):
    return value.split(key)