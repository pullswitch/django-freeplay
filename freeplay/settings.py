import os

from django.conf import settings


FREEPLAY = {
    "CHOSEN_URL": os.path.join(
                                settings.STATIC_URL,
                                'chosen/chosen.jquery.min.js'
                                ),
    "SLUGIFY_URL": os.path.join(
                                settings.STATIC_URL,
                                'lib/jquery-slugify/dist/slugify.min.js'
                                ),
    "ISOTOPE_URL": os.path.join(
                                settings.STATIC_URL,
                                'lib/isotope/jquery.isotope.min.js'
                                )
}

if hasattr(settings, "FREEPLAY"):
    FREEPLAY.update(settings.FREEPLAY)
