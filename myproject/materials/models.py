# materials/models.py
from django.db import models
from django.utils.text import slugify


class Material(models.Model):
    objects = None
    title = models.CharField(max_length=200)
    lectures = models.TextField(default='')
    classes = models.TextField(default='')
    labs = models.TextField(default='')
    projects = models.TextField(default='')
    slug = models.SlugField(unique=True, blank=True)  # Allow blank slugs
    date = models.DateTimeField(auto_now_add=True)  # Set the date automatically

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)  # Slugify the title
            unique_slug = base_slug  # Start with the base slug
            counter = 1  # Start at 1
            while Material.objects.filter(slug=unique_slug).exists():  # Avoid duplicates
                unique_slug = f"{base_slug}-{counter}"  # Add a counter to the slug
                counter += 1  # Increment the counter
            self.slug = unique_slug  # Set the unique slug
        super().save(*args, **kwargs)
