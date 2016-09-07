from django import template

register = template.Library()


@register.filter
def add_comma(value):
    return str.format("{0:,.2f}", value)


@register.filter
def to_three_sigfigs(value):
    return str.format('{0:.3f}', value)


@register.simple_tag
def url_replace(request, field, value):
    params = request.GET.copy()
    params[field] = value
    return params.urlencode()
