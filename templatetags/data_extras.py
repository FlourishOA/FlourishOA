from django import template

register = template.Library()


@register.filter
def to_three_sigfigs(value):
    return str.format('{0:.3f}', value)