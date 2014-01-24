from django.conf import settings


FREEPLAY = {
    "CHOSEN_PATH": 'chosen_v1.0.0/chosen.jquery.min.js',
    "SLUGIFY_PATH": 'jquery-slugify/dist/slugify.min.js',
    "MASONRY_PATH": 'masonry/jquery.masonry.min.js'
}

if hasattr(settings, "FREEPLAY"):
    FREEPLAY.update(settings.FREEPLAY)
