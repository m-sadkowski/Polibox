from django.shortcuts import render, redirect
from .models import Direction, Subject, SubjectElement, UserProgress
from .forms import UserProgressForm
from django.contrib.auth.decorators import login_required

def direction_list(request):
    directions = Direction.objects.all()
    return render(request, 'progression/direction_list.html', {'directions': directions})

def subject_list(request, direction_id):
    subjects_by_semester = {}
    for semester in range(1, 8):
        subjects_by_semester[semester] = Subject.objects.filter(direction_id=direction_id, semester=semester)
    return render(request, 'progression/subject_list.html', {
        'subjects_by_semester': subjects_by_semester,
        'direction_id': direction_id,
    })

def subject_detail(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    elements = subject.elements.all()
    user_progress = UserProgress.objects.filter(user=request.user, element__in=elements)

    return render(request, 'progression/subject_detail.html', {
        'subject': subject,
        'elements': elements,
        'user_progress': user_progress
    })

@login_required
def update_progress(request, element_id):
    element = SubjectElement.objects.get(id=element_id)
    user_progress, created = UserProgress.objects.get_or_create(user=request.user, element=element)

    if request.method == 'POST':
        form = UserProgressForm(request.POST, instance=user_progress)
        if form.is_valid():
            form.save()
            return redirect('subject_detail', subject_id=element.subject.id)
    else:
        form = UserProgressForm(instance=user_progress)

    return render(request, 'progression/update_progress.html', {'form': form, 'element': element})
