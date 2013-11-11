from django.conf.urls import patterns, url


urlpatterns = patterns("freeplay.views",
    url(r"^$", "dashboard", {}, name="freeplay_dashboard"),
    url(r"^(?P<region_pk>\d+?)/item/add/$",
        "create_item",
        name="freeplay_item_add"),
    url(r"^(?P<region_pk>\d+?)/item/(?P<item_pk>\d+?)/$",
        "change_item",
        name="freeplay_item_change"),
    url(r"^(?P<region_pk>\d+?)/item/(?P<item_pk>\d+?)/delete/$",
        "delete_item",
        name="freeplay_item_delete"),
)
