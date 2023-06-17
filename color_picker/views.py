from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.http import HttpResponse


def index(request):
    return HttpResponse("Color Picker")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}! You can now log in"
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "color_picker/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        color = request.POST.get("color")
        request.user.profile.color = color
        request.user.profile.save()
        messages.success(request, f"Your profile has been updated!")
        return redirect("profile")
    return render(
        request, "color_picker/profile.html", {"profile": request.user.profile}
    )


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "color_picker/user_profile.html", {"profile": user.profile})
