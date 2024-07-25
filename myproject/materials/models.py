# materials/models.py
from django.db import models
from django.utils.text import slugify
import os


def upload_path(instance, filename):
    return f"materials/{instance.material.slug}/{instance.category}/{filename}"


class Material(models.Model):
    title = models.CharField(max_length=200)
    lectures = models.TextField(default='WYKŁAD')
    classes = models.TextField(default='ĆWICZENIA')
    labs = models.TextField(default='LABORATORIUM')
    projects = models.TextField(default='PROJEKT')
    slug = models.SlugField(unique=True, blank=True)
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


class File(models.Model):
    CATEGORY_CHOICES = [
        ('lectures', 'Lectures'),
        ('classes', 'Classes'),
        ('labs', 'Labs'),
        ('projects', 'Projects'),
    ]
    material = models.ForeignKey(Material, related_name='files', on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    file = models.FileField(upload_to=upload_path)

    def __str__(self):
        return f"{self.material.title} - {self.category} - {self.file.name}"

    def get_thumbnail_url(self):
        extension = os.path.splitext(self.file.name)[1].lower()
        if extension in ['.jpg', '.jpeg', '.png', '.gif']:
            return self.file.url
        elif extension == '.pdf':
            return '/media/icons/pdf-ico.png'
        elif extension in ['.doc', '.docx']:
            return '/media/icons/doc-ico.png'
        elif extension == '.txt':
            return '/media/icons/doc-ico.png'
        elif extension in ['.c', '.cpp', '.h', '.hpp', '.py', '.java', '.js', '.html', '.css', '.php', '.sql', '.sh', '.bat', '.ps1', '.psm1']:
            return '/media/icons/code-ico.png'
        elif extension in ['.mp3', '.wav', '.flac', '.ogg', '.wma', '.aac']:
            return '/media/icons/audio-ico.png'
        elif extension in ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.3gp', '.webm', '.mpg', '.mpeg', '.m4v']:
            return '/media/icons/video-ico.png'
        else:
            return '/media/icons/default-icon.png'

    def get_filename(self):
        return os.path.basename(self.file.name)
