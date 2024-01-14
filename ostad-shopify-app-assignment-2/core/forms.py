from django.forms import Form, ModelForm, CharField, Textarea, HiddenInput, ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple, SelectMultiple
from django.db import models
from .models import LanguageChoice, Language


class CollectionCreateForm(Form):
    title = CharField(max_length=255)
    description = CharField(widget=Textarea)


class ProductCreateForm(Form):
    title = CharField(max_length=255)
    description = CharField(widget=Textarea)


class LanguageChoiceForm(ModelForm):
    # translate_to = ModelMultipleChoiceField(queryset=Language.objects.all())
    class Meta:
        model = LanguageChoice
        fields = [
            "shop",
            "site_language",
            "translate_to",
        ]

        # widgets = {
        #     "translate_to": SelectMultiple()
        # }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["shop"].widget = HiddenInput()
        self.fields["translate_to"].widget = CheckboxSelectMultiple()
        self.fields["translate_to"].queryset = Language.objects.all()
