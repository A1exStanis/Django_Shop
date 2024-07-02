from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Game(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=200)
    slug = models.SlugField(default='', null=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('game-detail', args=[self.slug])

    def __str__(self):
        return self.name
