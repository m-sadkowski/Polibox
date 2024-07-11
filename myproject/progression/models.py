from django.db import models
from django.contrib.auth.models import User

class Direction(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subject(models.Model):
    direction = models.ForeignKey(Direction, related_name='subjects', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    semester = models.IntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.elements.count() == 0:
            elements = ['Wykład', 'Ćwiczenia', 'Projekt', 'Laboratorium']
            for element_name in elements:
                SubjectElement.objects.create(subject=self, name=element_name)

class SubjectElement(models.Model):
    subject = models.ForeignKey(Subject, related_name='elements', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    element = models.ForeignKey(SubjectElement, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'element')
