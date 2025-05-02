from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def sneat_assets(url: str = "") -> str:
    templateUrl = 'assets/vendors/sneat/assets/'
    return f'{settings.STATIC_URL}{templateUrl}{url}'

@register.simple_tag
def leaflet_assets(url: str = "") -> str:
    templateUrl = 'assets/vendors/leaflet/'
    return f'{settings.STATIC_URL}{templateUrl}{url}'
