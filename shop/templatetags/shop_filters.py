
from django import template

register = template.Library()

def decrease(value, arg):
    return int(value) - arg

register.filter("decrease", decrease)