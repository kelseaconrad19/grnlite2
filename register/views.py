from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from .forms import RegisterForm
from my_app.models import Profile
from django.contrib.auth.forms import AuthenticationForm
from my_app.models import Profile

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from my_app.models import Manuscript  # Replace with the correct model for permissions

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        print(f"Form data: {request.POST}")  # Debug form data
        if form.is_valid():
            print("Form is valid.")  # Debug valid form
            user = form.save(commit=False)  # Save user instance without committing
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.email = form.cleaned_data.get("email")
            user.save()  # Save user instance

            # Save role in the Profile model
            role = form.cleaned_data.get("role")
            profile, created = Profile.objects.get_or_create(user=user, defaults={"role": role})
            print(f"Profile created: {created}; role is {role}")  # Debug profile creation

            if not created:
                print(f"Profile already exists for user {user.username}")  # Debug profile existence

            # Assign permissions based on the role
            content_type = ContentType.objects.get_for_model(Manuscript)
            if role == "author":
                permission = Permission.objects.get(codename="can_view_author_dashboard", content_type=content_type)
            elif role == "beta_reader":
                permission = Permission.objects.get(codename="can_view_reader_dashboard", content_type=content_type)
            else:
                permission = None

            if permission:
                user.user_permissions.add(permission)

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)  # Authenticate user
            if user is not None:
                print("User authenticated.")  # Debug authentication
                auth_login(request, user)  # Log in user
                
                # Redirect based on the user's role
                if role == "author":
                    return redirect("my_app:author-dashboard-html")  # Author dashboard URL name
                elif role == "beta_reader":
                    return redirect("my_app:reader-dashboard-html")  # Beta reader dashboard URL name
                else:
                    return redirect("my_app:home")  # Default fallback for other roles
        else:
            print(f"Form errors: {form.errors}")  # Debug form errors
            return render(request, "register/register.html", {"form": form})
    else:
        form = RegisterForm()
    return render(request, "register/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Get the authenticated user
            auth_login(request, user)  # Log the user in

            # Check the user's role and redirect to the appropriate dashboard
            profile = Profile.objects.filter(user=user).first()
            if profile and profile.role == "author":
                return redirect("my_app:author-dashboard-html")  # Replace with your URL name for the author dashboard
            elif profile and profile.role == "beta_reader":
                return redirect("my_app:reader-dashboard-html")  # Replace with your URL name for the beta reader dashboard
            else:
                return redirect("my_app:home")  # Default fallback if no role is found
        else:
            return render(request, "register/login.html", {"form": form})
    else:
        form = AuthenticationForm()
    return render(request, "register/login.html", {"form": form})