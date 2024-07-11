from django.contrib import admin
from .models import Direction, Subject, SubjectElement, UserProgress

admin.site.register(Direction)
admin.site.register(Subject)
admin.site.register(SubjectElement)
admin.site.register(UserProgress)
