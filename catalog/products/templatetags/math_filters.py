from django import template


register = template.Library()

@register.filter
def calculate_discount(value, arg):
    return value * arg / 100

