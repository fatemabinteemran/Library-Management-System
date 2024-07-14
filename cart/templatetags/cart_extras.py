from django import template
#from cart import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))
