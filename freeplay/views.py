from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from .forms import ItemForm
from .models import Region


@permission_required("freeplay.author_contentbits", raise_exception=True)
def dashboard(request):

    regions = Region.objects.all()

    return TemplateResponse(request,
        "admin/freeplay/dashboard.html",
        {
        "regions": regions
        }
    )


@permission_required("freeplay.author_contentbits", raise_exception=True)
def create_item(request, region_pk):
    region = get_object_or_404(Region, pk=region_pk)

    form = ItemForm(region=region)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, region=region)
        if form.is_valid():
            form.save()
            messages.success(request, "The item was added successfully")
            return redirect("freeplay_dashboard")

    return TemplateResponse(request,
        "admin/freeplay/item_form.html",
        {
            "region": region,
            "form": form,
            "add": True,
            "opts": {
                "verbose_name": "Item for %s" % region.name
            }
        }
    )


@permission_required("freeplay.author_contentbits", raise_exception=True)
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

    return TemplateResponse(request,
        "admin/freeplay/item_form.html",
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
