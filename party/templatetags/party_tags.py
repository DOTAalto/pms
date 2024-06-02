from django import template
from party.models import Party

register = template.Library()

@register.simple_tag()
def get_active_party_title():
    return Party.objects.get(is_active=True).title 