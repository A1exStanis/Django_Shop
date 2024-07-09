from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=500)
    slug = models.SlugField(default='', null=False, blank=True)
    image = models.ImageField(blank=True, upload_to='image')

    def create_slug(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)

    def slug_name(self):
        return self.slug

    def get_url(self):
        return reverse('game-detail', args=[self.slug])

    def __str__(self):
        return self.name
