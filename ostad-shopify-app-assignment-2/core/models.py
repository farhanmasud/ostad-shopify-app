from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Language(models.Model):
    name = models.CharField(max_length=31)
    code = models.CharField(max_length=15)

    def __str__(self):
        return " - ".join([self.name, self.code])
    

class LanguageChoice(models.Model):
    shop = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    site_language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)
    translate_to = models.ManyToManyField(Language)
