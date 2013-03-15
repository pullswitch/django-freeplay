from django.contrib import admin

from relatedwidget import RelatedWidgetWrapperBase

from tidbits.models import Area, Bit, ContentBit
from tidbits.models import Item, Template


class AreaOptions(RelatedWidgetWrapperBase, admin.ModelAdmin):

    list_display = ("name", "slug", "min_items", "max_items")


class BitOptions(admin.ModelAdmin):

    list_display = ("template", "kind", "name", "context_name")


class BitInline(admin.StackedInline):
    model = Bit


class TemplateOptions(admin.ModelAdmin):

    inlines = [
        BitInline,
    ]


class ItemOptions(RelatedWidgetWrapperBase, admin.ModelAdmin):

    list_display = ("label", "area", "order")
    list_filter = ("area", )


admin.site.register(Area, AreaOptions)
admin.site.register(Template, TemplateOptions)
admin.site.register(Bit, BitOptions)
admin.site.register(Item, ItemOptions)
admin.site.register(ContentBit)
