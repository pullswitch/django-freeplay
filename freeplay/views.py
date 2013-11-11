from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from .forms import ItemForm
from .models import Region
from .settings import FREEPLAY


class FreeplayResponse(TemplateResponse):

    def __init__(self, request, template, context, **kwargs):

        context.update(FREEPLAY)

        super(FreeplayResponse, self).__init__(
            request, template, context=context, **kwargs)


@permission_required("freeplay.add_contentbit", raise_exception=True)
def dashboard(request):

    regions = Region.objects.all()

    return FreeplayResponse(request,
        "admin/freeplay/dashboard.html",
        {
        "regions": regions
        }
    )


@permission_required("freeplay.add_contentbit", raise_exception=True)
def create_item(request, region_pk):
    region = get_object_or_404(Region, pk=region_pk)

    form = ItemForm(region=region)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, region=region)
        if form.is_valid():
            form.save()
            messages.success(request, "The item was added successfully")
            return redirect("freeplay_dashboard")

    return FreeplayResponse(request,
        "admin/freeplay/{0}item_form.html".format(
            "_" if request.is_ajax() else ""),
        {
            "region": region,
            "form": form,
            "add": True,
            "opts": {
                "verbose_name": "Item for %s" % region.name
            }
        }
    )


@permission_required("freeplay.change_contentbit", raise_exception=True)
def change_item(request, region_pk, item_pk):
    region = get_object_or_404(Region, pk=region_pk)
    item = get_object_or_404(region.items, pk=item_pk)

    form = ItemForm(region=region, instance=item)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, region=region, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "The item was updated successfully")
            return redirect("freeplay_dashboard")

    return FreeplayResponse(request,
        "admin/freeplay/{0}item_form.html".format(
            "_" if request.is_ajax() else ""),
        {
            "region": region,
            "form": form,
            "add": False,
            "instance": item,
            "opts": {
                "verbose_name": "Item for %s" % region.name
            }
        }
    )


@permission_required("freeplay.delete_contentbit", raise_exception=True)
def delete_item(request, region_pk, item_pk):
    region = get_object_or_404(Region, pk=region_pk)
    item = get_object_or_404(region.items, pk=item_pk)

    form = ItemForm(region=region, instance=item)

    if request.method == "POST":
        item.delete()
        messages.success(request, "The item was deleted successfully")
        return redirect("freeplay_dashboard")

    return FreeplayResponse(request,
        "admin/freeplay/{0}item_delete.html".format(
            "_" if request.is_ajax() else ""),
        {
            "region": region,
            "instance": item,
            "opts": {
                "verbose_name": "Item for %s" % region.name
            }
        }
    )
