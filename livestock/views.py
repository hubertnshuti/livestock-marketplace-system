from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LivestockItemForm, LivestockImageForm, SimpleOrderForm
from .models import LivestockItem, LivestockImage, Order, OrderItem

# 1. CREATE BASIC INFO (Step 1)
@login_required
def livestock_create(request):
    if request.method == 'POST':
        form = LivestockItemForm(request.POST)
        if form.is_valid():
            livestock_item = form.save(commit=False)
            # Ensure the user acts as a farmer
            if hasattr(request.user, 'farmer_profile'):
                livestock_item.farmer = request.user.farmer_profile
                livestock_item.save()
                # Redirect to Step 2 (Add Photos)
                return redirect('livestock:add_photos', pk=livestock_item.pk)
            else:
                messages.error(request, "You must be a registered farmer to list livestock.")
                return redirect('dashboard')
    else:
        form = LivestockItemForm()
        
    return render(request, 'add_livestock.html', {'form': form})

# 2. ADD PHOTOS VIEW (Step 2)
@login_required
def add_photos(request, pk):
    # Ensure the user owns this livestock item before allowing photo uploads
    livestock = get_object_or_404(LivestockItem, pk=pk, farmer=request.user.farmer_profile)
    
    if request.method == 'POST':
        form = LivestockImageForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.livestock = livestock
            photo.save()
            messages.success(request, "Photo uploaded successfully!")
            return redirect('livestock:add_photos', pk=pk) # Reload to allow adding more
    else:
        form = LivestockImageForm()

    # Get existing photos to display
    photos = livestock.images.all()

    return render(request, 'add_photos.html', {
        'form': form, 
        'livestock': livestock, 
        'photos': photos
    })

# 3. SUCCESS VIEW (Step 3)
@login_required
def upload_success(request):
    return render(request, 'upload_success.html')

# 4. MARKETPLACE VIEW (For Buyers) - THIS WAS MISSING
def marketplace(request):
    # Get all livestock that are marked 'for_sale' and 'available'
    listings = LivestockItem.objects.filter(is_for_sale=True, status='available').order_by('-listing_date')
    
    context = {
        'listings': listings,
        'page_title': 'Marketplace'
    }
    return render(request, 'marketplace.html', context)

# 5. DETAIL VIEW (Single Item)
def livestock_detail(request, pk):
    # Get the specific item or return 404 error if not found
    livestock = get_object_or_404(LivestockItem, pk=pk)
    
    # Get related photos
    photos = livestock.images.all()
    
    context = {
        'livestock': livestock,
        'photos': photos,
        'page_title': f"{livestock.species.species_name} Details"
    }
    return render(request, 'livestock_detail.html', context)


@login_required
def place_order(request, pk):
    # 1. Security Check: Must be a Buyer
    if not hasattr(request.user, 'buyer_profile'):
        messages.error(request, "Only registered buyers can place orders.")
        return redirect('dashboard')
        
    # 2. Get the animal
    livestock_item = get_object_or_404(LivestockItem, pk=pk)
    buyer = request.user.buyer_profile

    # 3. Availability Check
    if livestock_item.is_for_sale == False or livestock_item.status != 'available':
        messages.error(request, "This item is not currently available for purchase.")
        return redirect('livestock:livestock_detail', pk=pk)

    # 4. Process the Order
    if request.method == 'POST':
        form = SimpleOrderForm(request.POST)
        if form.is_valid():
            
            # Create the main Order
            new_order = Order.objects.create(
                buyer=buyer,
                total_amount=livestock_item.price * form.cleaned_data['quantity'],
                order_status='pending_inquiry', # Initial status
                payment_status='pending'
            )
            
            # Create the Order Item (Snapshot of the deal)
            OrderItem.objects.create(
                order=new_order,
                livestock=livestock_item,
                quantity=form.cleaned_data['quantity'],
                unit_price_at_time=livestock_item.price,
            )

            messages.success(request, f"Order sent! The farmer has been notified about your interest in {livestock_item.species.species_name}.")
            return redirect('dashboard') 
            
    return redirect('livestock:livestock_detail', pk=pk)

































# from django.urls import reverse_lazy
# from django.views import generic # Generic Views are here
# from .models import LivestockSpecies, Breed


# # ADDED IMPORTS (The culprit for the circular load):
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from accounts.models import Farmer 
# from .forms import LivestockItemForm, LivestockImageForm
# from .models import LivestockItem, LivestockImage


# # --- LivestockItem CRUD Views ---

# # 1. CREATE BASIC INFO (Updated)
# @login_required
# def livestock_create(request):
#     if request.method == 'POST':
#         form = LivestockItemForm(request.POST)
#         if form.is_valid():
#             livestock_item = form.save(commit=False)
#             livestock_item.farmer = request.user.farmer_profile
#             livestock_item.save()
            
#             # REDIRECT TO STEP 2 (Add Photos) passing the new item's ID
#             return redirect('livestock:add_photos', pk=livestock_item.pk)
#     else:
#         form = LivestockItemForm()
        
#     return render(request, 'add_livestock.html', {'form': form})

# # 2. ADD PHOTOS VIEW (New)
# @login_required
# def add_photos(request, pk):
#     livestock = get_object_or_404(LivestockItem, pk=pk, farmer=request.user.farmer_profile)
    
#     if request.method == 'POST':
#         form = LivestockImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             photo = form.save(commit=False)
#             photo.livestock = livestock
#             photo.save()
#             messages.success(request, "Photo uploaded successfully!")
#             return redirect('livestock:add_photos', pk=pk) # Reload to allow adding more
#     else:
#         form = LivestockImageForm()

#     # Get existing photos to display
#     photos = livestock.images.all()

#     return render(request, 'add_photos.html', {
#         'form': form, 
#         'livestock': livestock, 
#         'photos': photos
#     })

# # 3. SUCCESS VIEW (New)
# @login_required
# def upload_success(request):
#     return render(request, 'upload_success.html')

















