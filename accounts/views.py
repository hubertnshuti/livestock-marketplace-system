from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import UserProfile, Farmer, Buyer
from django.contrib.auth.decorators import login_required


# ------------------------
# CUSTOM REGISTER FORM
# ------------------------
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    USER_TYPE_CHOICES = [
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
    ]

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned


# ------------------------
# REGISTER VIEW
# ------------------------
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create User
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Create UserProfile (THIS WAS YOUR BUG — MUST BE CREATED)
            user_type = form.cleaned_data["user_type"]
            profile = UserProfile.objects.create(
                user=user,
                user_type=user_type
            )

            # Create Farmer or Buyer linked tables
            if user_type == "farmer":
                Farmer.objects.create(
                    user=user,
                    farm_name=f"{user.username}'s Farm"
                )
            else:
                Buyer.objects.create(
                    user=user,
                    buyer_type="individual"
                )

            login(request, user)
            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


# ------------------------
# LOGIN VIEW
# ------------------------
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")

    return render(request, "login.html", {"form": form})


# ------------------------
# DASHBOARD VIEW
# ------------------------
@login_required
def dashboard(request):
    profile = request.user.profile

    if profile.user_type == "farmer":
        # Get the farmer profile
        farmer = request.user.farmer_profile
        # Get counts
        total_livestock = farmer.livestock_items.count()
        # Get actual items
        recent_listings = farmer.livestock_items.all().order_by('-listing_date')[:5]

        context = {
            "profile": profile,
            "total_livestock": total_livestock,
            "recent_listings": recent_listings
        }
        return render(request, "farmer_dashboard.html", context)

    elif profile.user_type == "buyer":
        return render(request, "buyer_dashboard.html", {"profile": profile})

    return render(request, "dashboard.html", {"profile": profile})