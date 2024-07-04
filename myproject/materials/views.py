from django.shortcuts import render, redirect
from .models import Material
from .forms import MaterialForm
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
	return user.is_superuser


@user_passes_test(is_admin, login_url="/users/login/")
def material_new(request):
	if request.method == 'POST':
		form = MaterialForm(request.POST)
		if form.is_valid():
			material = form.save(commit=False)
			material.save()
			return redirect('materials:list')  # Przekierowanie po dodaniu materiału
	else:
		form = MaterialForm()

	return render(request, 'materials/material_new.html', {'form': form})


@login_required(login_url="/users/login/")
def materials_list(request):
	materials = Material.objects.all().order_by('-date')
	return render(request, 'materials/materials_list.html', {'materials': materials})


@login_required(login_url="/users/login/")
def material_page(request, slug):
	material = Material.objects.get(slug=slug)
	return render(request, 'materials/material_page.html', {'material': material})
