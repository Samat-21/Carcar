from django import template
from main.models import *

register = template.Library()

@register.simple_tag()
def get_trips():
    return Trip.objects.all()

#@register.inclusion_tag('main/list_trips.html')
#def show_all_trips():
#    all_trips = Trip.objects.all()
#    return {'all_trips': all_trips}