from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.http import HttpResponse
from django.utils import timezone
from .forms import UserRegisterForm
from django.contrib.auth import login
from .models import Profile


def index(request):
    return HttpResponse("Color Picker")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            user.last_login = timezone.now()  # set last_login to current time
            user.save()
            profile = Profile(user=user, color="")
            profile.save()

            login(request, user)
            return redirect("profile")
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
