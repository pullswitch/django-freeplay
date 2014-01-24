from django.contrib import admin

from relatedwidget import RelatedWidgetWrapperBase

from freeplay.models import Region, Bit, ContentBit
from freeplay.models import Item, Template


class RegionOptions(RelatedWidgetWrapperBase, admin.ModelAdmin):

    list_display = ("name", "slug", "min_items", "max_items")


class BitOptions(admin.ModelAdmin):

    list_display = ("template", "kind", "name", "context_name")


class BitInline(admin.StackedInline):
    model = Bit


class TemplateOptions(admin.ModelAdmin):
    list_display = ("name", "active_item_count", "bit_names")

    inlines = [
        BitInline,
    ]

    def active_item_count(self, obj):
        return sum([r.items.count() for r in obj.region_set.all()])

    def bit_names(self, obj):
        return ", ".join([b.name for b in obj.bits.all()])


class ItemOptions(RelatedWidgetWrapperBase, admin.ModelAdmin):

    list_display = ("label", "region", "order")
    list_filter = ("region", )


admin.site.register(Region, RegionOptions)
admin.site.register(Template, TemplateOptions)
admin.site.register(Bit, BitOptions)
admin.site.register(Item, ItemOptions)
admin.site.register(ContentBit)
