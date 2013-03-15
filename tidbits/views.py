from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from .forms import ItemForm
from .models import Area


@permission_required("tidbits.author_contentbits", raise_exception=True)
def dashboard(request):

    areas = Area.objects.all()

    return TemplateResponse(request,
        "admin/tidbits/dashboard.html",
        {
        "areas": areas
        }
    )


@permission_required("tidbits.author_contentbits", raise_exception=True)
def create_item(request, area_pk):
    area = get_object_or_404(Area, pk=area_pk)

    form = ItemForm(area=area)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, area=area)
        if form.is_valid():
            form.save()
            messages.success(request, "The item was added successfully")
            return redirect("tidbits_dashboard")

    return TemplateResponse(request,
        "admin/tidbits/item_form.html",
        {
            "area": area,
            "form": form,
            "add": True,
            "opts": {
                "verbose_name": "Item for %s" % area.name
            }
        }
    )


@permission_required("tidbits.author_contentbits", raise_exception=True)
def change_item(request, area_pk, item_pk):
    area = get_object_or_404(Area, pk=area_pk)
    item = get_object_or_404(area.items, pk=item_pk)

    form = ItemForm(area=area, instance=item)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, area=area, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "The item was updated successfully")
            return redirect("tidbits_dashboard")

    return TemplateResponse(request,
        "admin/tidbits/item_form.html",
        {
            "area": area,
            "form": form,
            "add": False,
            "instance": item,
            "opts": {
                "verbose_name": "Item for %s" % area.name
            }
        }
    )
