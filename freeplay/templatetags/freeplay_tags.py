from django import template

from freeplay.models import Region, Item

register = template.Library()


@register.assignment_tag
def content_bits(region_slug):
    try:
        region = Region.objects.get(slug=region_slug)
        return region.items.all()
    except:
        return None


@register.assignment_tag
def get_bit(region_slug, item_slug=None):
    if item_slug:
        try:
            return Item.objects.get(
                region__slug=region_slug,
                slug=item_slug
            )
        except Item.DoesNotExist:
            return None
    else:
        try:
            return Item.objects.filter(
                region__slug=region_slug
            )[0]
        except IndexError:
            return None
