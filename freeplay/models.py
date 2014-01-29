from django.db import models
from django.template import Context, Template as DjTemplate
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from model_utils import Choices


class Region(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    min_items = models.IntegerField(default=0)
    max_items = models.IntegerField(default=0)

    template = models.ForeignKey("Template")

    def __unicode__(self):
        return u"{0}".format(self.name)


class Template(models.Model):
    name = models.CharField(max_length=100)
    code = models.TextField(help_text=_(
        "Be sure to use the 'safe' filter when the input might include \
         HTML tags"
    ))

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        super(Template, self).save(*args, **kwargs)

        # Re-save any items using this template
        for region in self.region_set.all():
            for item in region.items.all():
                item.save()


class Bit(models.Model):
    KINDS = Choices(
        ("image", _("Image")),
        ("text", _("Plain text")),
        ("html", _("HTML")),
        ("markdown", _("Markdown")),
        ("code", _("Code"))
    )
    template = models.ForeignKey(Template, related_name="bits")
    kind = models.CharField(choices=KINDS, default=KINDS.text, max_length=20)
    name = models.CharField(_('Name'), max_length=100)
    context_name = models.CharField(
        max_length=40,
        help_text=_("This will be the name in the template context."),
    )
    order = models.IntegerField(default=0)

    TEXT_WIDGET_CHOICES = (
        ("charfield", _('Text Input Field')),
        ("textarea", _('Textarea Input Field')),
    )

    text_widget = models.CharField(
        max_length=10,
        choices=TEXT_WIDGET_CHOICES,
        default='charfield',
        help_text=_("Which type of input widget to use in admin form \
                    for Plain Text fields."),
    )
    image_constraints = models.CharField(max_length=20, blank=True, null=True)
    image_quality = models.IntegerField(blank=True, null=True)

    required = models.BooleanField(
        _('Required'),
        default=False,
        help_text=_('Is this field required?')
    )

    help_text = models.TextField(_('Optional admin help text'), blank=True)

    @property
    def image_x(self):
        if self.kind == "image" and self.image_constraints:
            return self.image_constraints.split("x")[0]
        return None

    @property
    def image_y(self):
        if self.kind == "image" and self.image_constraints:
            return self.image_constraints.split("x")[1]
        return None

    class Meta:
        unique_together = ("template", "order")


class ContentBit(models.Model):
    bit = models.ForeignKey(Bit)
    item = models.ForeignKey("Item", related_name="content_bits")
    data = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/content/",
                              blank=True, null=True)

    @property
    def image_formatted(self):
        f = ImageSpecField(
            source="image",
            format="PNG",
            options={"quality": self.bit.image_quality},
            processors=[ResizeToFill(self.bit.image_x, self.bit.image_y)],
        )
        f.contribute_to_class(ContentBit, "image_formatted")
        return self.image_formatted

    @property
    def markup(self):
        if self.image:
            return mark_safe("<img src=\"{0}\" alt=\"{1}\">".format(
                self.image_url,
                self.item.label
            ))
        return mark_safe(self.data)

    @property
    def image_url(self):
        if self.image:
            return self.image_formatted.url if self.bit.image_x \
                else self.image.url


class BitClass:
    def __init__(self, contentbit):
        self.url = contentbit.image_url
        self.type = contentbit.bit.kind
        self.contentbit = contentbit

    def __repr__(self):
        return self.contentbit.markup


class Item(models.Model):
    region = models.ForeignKey(Region, related_name="items")
    order = models.IntegerField(default=0)
    label = models.CharField(max_length=100)
    slug = models.SlugField()

    data = models.TextField(blank=True, null=True, editable=False)

    def __unicode__(self):
        return u"{0}".format(self.label)

    def save(self, *args, **kwargs):
        code = self.region.template.code
        ctx = {
            "label": self.label,
            "order": self.order,
            "slug": self.slug
        }
        for cb in self.content_bits.all():
            bc = BitClass(cb)
            if bc.contentbit.image:
                ctx.update({
                    cb.bit.context_name: bc,
                    "{0}_url".format(
                        cb.bit.context_name): bc.contentbit.image_url
                })
            else:
                ctx.update({
                    cb.bit.context_name: smart_text(bc.contentbit.markup)
                })
        t = DjTemplate(code)
        self.data = t.render(Context(ctx))
        super(Item, self).save(*args, **kwargs)

    def save_content(self, data):
        updated = []
        for bit in self.region.template.bits.all():
            cb, created = ContentBit.objects.get_or_create(
                bit=bit,
                item=self
            )
            if bit.kind == "image":
                cb.image = data.get("bit{0}".format(bit.pk))
            else:
                cb.data = data.get("bit{0}".format(bit.pk))
            if cb.bit.kind == "markdown":
                import markdown
                cb.data = markdown.markdown(cb.data)
            cb.save()
            updated.append(cb.pk)
        self.content_bits.exclude(pk__in=updated).delete()

    class Meta:
        ordering = ("region", "order", )
        unique_together = ("region", "slug")
