from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import NewUserForm
from .models import Profile
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main-page')
    form = NewUserForm()
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context=context)

def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('main-page')
    else:
        return redirect('main-page')


@login_required
def users_profile(request):
    if request.method == "POST":
        contact_number = request.POST.get("number")
        image = request.FILES["upload"]
        user = request.user
        profile = Profile(user=user, contact_number=contact_number, image=image)
        profile.save()
    return render(request, "users/profile.html")
