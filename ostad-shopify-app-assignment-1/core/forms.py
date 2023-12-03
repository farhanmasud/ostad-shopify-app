from django.forms import Form, CharField, Textarea


class CollectionCreateForm(Form):
    title = CharField(max_length=255)
    description = CharField(widget=Textarea)


class ProductCreateForm(Form):
    title = CharField(max_length=255)
    description = CharField(widget=Textarea)
