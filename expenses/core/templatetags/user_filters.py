from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def fieldtype(field):
    return field.field.widget.__class__.__name__


@register.filter
def emptyvalue(field):
    if not field:
        return '---'
    return field


register.filter('addclass', addclass)
register.filter('fieldtype', fieldtype)
register.filter('emptyvalue', emptyvalue)
