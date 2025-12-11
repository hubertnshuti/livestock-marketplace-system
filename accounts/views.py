<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import UserProfile
# IMPORT LIVESTOCK MODELS to fetch data
from livestock.models import LivestockItem, Order, OrderItem 
from django.db.models import Sum

=======
# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# CORRECT: Import only ACCOUNTS-RELATED forms and models
from .models import UserProfile, Farmer, Buyer
from .forms import (
    RegisterForm, 
    UserUpdateForm, 
    ProfileUpdateForm, 
    FarmerUpdateForm, 
    BuyerUpdateForm
)


# ------------------------
# REGISTER VIEW
# ------------------------
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
<<<<<<< HEAD
=======
            user_type = form.cleaned_data["user_type"]
            
            # Create UserProfile 
            UserProfile.objects.create(
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

            messages.success(request, f"Registration successful. Welcome!")
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

@login_required
def dashboard(request):
<<<<<<< HEAD
    profile = request.user.profile

    # --- LOGIC FOR FARMERS ---
    if profile.user_type == "farmer":
        farmer = request.user.farmer_profile
        
        # 1. My Livestock Stats
        total_livestock = farmer.livestock_items.count()
        recent_listings = farmer.livestock_items.all().order_by('-listing_date')[:5]
        
        # 2. Incoming Orders (Sales)
        # Get items owned by this farmer
        my_items = farmer.livestock_items.all()
        # Find OrderItems that reference these items
        incoming_sales = OrderItem.objects.filter(livestock__in=my_items).select_related('order')
        
        # Count pending sales
        active_alerts = incoming_sales.filter(order__order_status='pending_inquiry').count()
        
        # Calculate Sold count (items marked as sold)
        sold_count = my_items.filter(status='sold').count()
=======
    user_profile = request.user.userprofile 
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff

    if user_profile.user_type == "farmer":
        farmer = getattr(request.user, 'farmer_profile', None) 
        
        context = {
<<<<<<< HEAD
            "profile": profile,
            "total_livestock": total_livestock,
            "recent_listings": recent_listings,
            "active_alerts": active_alerts, # Pending Orders count
            "sold_count": sold_count,
            "incoming_sales": incoming_sales[:5] # Show last 5 inquiries
        }
        return render(request, "farmer_dashboard.html", context)

    # --- LOGIC FOR BUYERS ---
    elif profile.user_type == "buyer":
        buyer = request.user.buyer_profile
        
        # 1. Fetch Orders placed by this buyer
        my_orders = Order.objects.filter(buyer=buyer).order_by('-order_date')
        
        # 2. Stats
        active_orders_count = my_orders.exclude(order_status='completed').count()
        
        # Calculate Total Spent (Sum of total_amount)
        total_spent = my_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        context = {
            "profile": profile,
            "orders": my_orders[:5], # Recent 5 orders
            "active_orders_count": active_orders_count,
            "total_spent": total_spent,
            "saved_items_count": 0 # Placeholder for wishlist
=======
            "profile": user_profile,
            # Placeholder for future dashboard data
        }
        return render(request, "farmer_dashboard.html", context)

    elif user_profile.user_type == "buyer":
        buyer = getattr(request.user, 'buyer_profile', None) 
        
        context = {
            "profile": user_profile,
            # Placeholder for future dashboard data
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff
        }
        return render(request, "buyer_dashboard.html", context)

    return render(request, "dashboard.html", {"profile": user_profile})


# ------------------------
# PROFILE VIEW
# ------------------------
@login_required
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    farmer_form = None
    buyer_form = None

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        
        # Handle Role Specifics
        if hasattr(request.user, 'farmer_profile'):
            farmer_form = FarmerUpdateForm(request.POST, instance=request.user.farmer_profile)
        elif hasattr(request.user, 'buyer_profile'):
            buyer_form = BuyerUpdateForm(request.POST, instance=request.user.buyer_profile)

        # Validation Check
        if u_form.is_valid() and p_form.is_valid():
            role_valid = True
            if farmer_form and not farmer_form.is_valid(): role_valid = False
            if buyer_form and not buyer_form.is_valid(): role_valid = False
            
            if role_valid:
                u_form.save()
                p_form.save()
                if farmer_form: farmer_form.save()
                if buyer_form: buyer_form.save()
                
                messages.success(request, f'Your account has been updated!')
                return redirect('profile')
        else:
            messages.error(request, 'Error updating profile. Please check the fields.')

    else:
        # GET Request - Pre-fill forms with current data
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=user_profile)
        
        if hasattr(request.user, 'farmer_profile'):
            farmer_form = FarmerUpdateForm(instance=request.user.farmer_profile)
        elif hasattr(request.user, 'buyer_profile'):
            buyer_form = BuyerUpdateForm(instance=request.user.buyer_profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'farmer_form': farmer_form,
        'buyer_form': buyer_form,
        'is_farmer': user_profile.user_type == 'farmer'
    }

    return render(request, 'profile.html', context)