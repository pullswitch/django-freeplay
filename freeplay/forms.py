from django import forms

from .models import Item


class EmptyContentBit:
    def __init__(self, bit):
        self.bit = bit
        self.data = None
        self.image = None


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item

    def __init__(self, *args, **kwargs):
        self.region = kwargs.pop("region")
        super(ItemForm, self).__init__(*args, **kwargs)
        if not len(args):
            args = [{}, {}]
        if kwargs.get("instance"):
            bits = kwargs.get("instance").content_bits.all()
        else:
            bits = [
                EmptyContentBit(bit) for bit in self.region.template.bits.all()
            ]
        for cb in bits:
            if cb.bit.kind == "image":
                field = forms.ImageField()
                if cb.image:
                    field.initial = cb.image
            else:
                field = forms.CharField()
                if cb.bit.text_widget == "textarea":
                    field.widget = forms.widgets.Textarea()
                if cb.data:
                    field.initial = cb.data
            field.label = cb.bit.name
            if cb.bit.help_text:
                field.help_text = cb.bit.help_text
            if not cb.bit.required:
                field.required = False
            self.fields.insert(cb.bit.order + len(self.fields) - 1, "bit{0}".format(cb.bit.pk), field)

        self.fields["region"].widget = forms.widgets.HiddenInput()
        self.fields["region"].initial = self.region

    def save(self):
        item = super(ItemForm, self).save()
        item.save_content(data=self.cleaned_data)
        item.save()
