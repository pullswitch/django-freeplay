from django.conf.urls import patterns, include, url


urlpatterns = patterns("tidbits.views",
    url(r"^$", "dashboard", {}, name="tidbits_dashboard"),
    url(r"^(?P<area_pk>\d+?)/item/add/$", "create_item", name="tidbits_item_add"),
    url(r"^(?P<area_pk>\d+?)/item/(?P<item_pk>\d+?)/$", "change_item", name="tidbits_item_change"),
)
