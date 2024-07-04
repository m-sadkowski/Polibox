from django.db import models
from django.utils.text import slugify
import uuid

class Material(models.Model):
    title = models.CharField(max_length=200)
    lectures = models.TextField(default='')
    classes = models.TextField(default='')
    labs = models.TextField(default='')
    projects = models.TextField(default='')
    slug = models.SlugField(unique=True, blank=True)  # Allow blank slugs
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Material.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)