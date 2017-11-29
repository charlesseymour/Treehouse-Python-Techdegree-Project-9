from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateField(default=timezone.localdate)
    expiration_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.season

    def get_absolute_url(self):
        return reverse('menu:menu_detail', kwargs={'pk': self.id})


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')
    created_date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
