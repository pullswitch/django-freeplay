from django import template

from tidbits.models import Area, Item

register = template.Library()


@register.assignment_tag
def content_bits(area_slug):
    try:
        area = Area.objects.get(slug=area_slug)
        return area.items.all()
    except:
        return None


@register.assignment_tag
def get_bit(area_slug, item_slug):
    try:
        return Item.objects.get(
            area__slug=area_slug,
            slug=item_slug
        )
    except:
        return None
