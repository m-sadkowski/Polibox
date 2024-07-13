# progression/models.py
from django.db import models
from django.contrib.auth.models import User


class Direction(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def calculate_completion(self, user):
        subjects = self.subjects.all()
        total_percentage = 0
        total_elements = 0

        for subject in subjects:
            for element in subject.elements.all():
                user_progress = UserProgress.objects.filter(user=user, element=element).first()
                if user_progress:
                    total_percentage += user_progress.completion_percentage()
                total_elements += 1

        if total_elements == 0:
            return 0
        return total_percentage / total_elements


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

    def calculate_completion(self, user):
        total_percentage = 0
        total_elements = self.elements.count()
        for element in self.elements.all():
            user_progress = UserProgress.objects.filter(user=user, element=element).first()
            if user_progress:
                total_percentage += user_progress.completion_percentage()

        if total_elements == 0:
            return 0
        return total_percentage / total_elements


class SubjectElement(models.Model):
    subject = models.ForeignKey(Subject, related_name='elements', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    element = models.ForeignKey(SubjectElement, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_fragments = models.IntegerField(default=0)
    total_fragments = models.IntegerField(default=1)

    class Meta:
        unique_together = ('user', 'element')

    def completion_percentage(self):
        if self.total_fragments == 0:
            return 0
        return (self.completed_fragments / self.total_fragments) * 100
