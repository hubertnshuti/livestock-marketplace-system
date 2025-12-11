<<<<<<< HEAD
import requests
import uuid
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LivestockItemForm, LivestockImageForm, SimpleOrderForm
from .models import LivestockItem, LivestockImage, Order, OrderItem

# 1. CREATE BASIC INFO
=======
# livestock/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q # Needed later for filtering

# FIX: Import the forms from the local livestock/forms.py file
from .forms import LivestockItemForm, LivestockImageForm, SimpleOrderForm 
from .models import LivestockItem, LivestockImage, Order, OrderItem
# Note: Species/Breed models are loaded via forms now


# --- 1. CREATE BASIC INFO (Step 1) ---
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff
@login_required
def livestock_create(request):
    if request.method == 'POST':
        form = LivestockItemForm(request.POST)
        if form.is_valid():
            livestock_item = form.save(commit=False)
<<<<<<< HEAD
            if hasattr(request.user, 'farmer_profile'):
                livestock_item.farmer = request.user.farmer_profile
                livestock_item.save()
=======
            
            if hasattr(request.user, 'farmer_profile'):
                livestock_item.farmer = request.user.farmer_profile
                livestock_item.save()
                messages.success(request, "Basic information saved. Now add photos.")
                # Redirect to the photo upload page (Step 2)
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff
                return redirect('livestock:add_photos', pk=livestock_item.pk)
            else:
                messages.error(request, "You must be a registered farmer to list livestock.")
                return redirect('dashboard')
    else:
        form = LivestockItemForm()
        
    return render(request, 'add_livestock.html', {'form': form})

<<<<<<< HEAD
# 2. ADD PHOTOS VIEW
@login_required
def add_photos(request, pk):
=======
# --- 2. ADD PHOTOS VIEW (Step 2) ---
@login_required
def add_photos(request, pk):
    # This view requires a template named add_photos.html
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff
    livestock = get_object_or_404(LivestockItem, pk=pk, farmer=request.user.farmer_profile)
    
    if request.method == 'POST':
        form = LivestockImageForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.livestock = livestock
            photo.save()
            messages.success(request, "Photo uploaded successfully!")
            return redirect('livestock:add_photos', pk=pk) 
    else:
        form = LivestockImageForm()

    photos = livestock.images.all()

    return render(request, 'add_photos.html', {
        'form': form, 
        'livestock': livestock, 
        'photos': photos
    })

<<<<<<< HEAD
# 3. SUCCESS VIEW
=======
# --- 3. SUCCESS VIEW (Step 3) ---
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff
@login_required
def upload_success(request):
    return render(request, 'upload_success.html')

<<<<<<< HEAD
# 4. MARKETPLACE VIEW
=======
# --- 4. MARKETPLACE VIEW (For Buyers) ---
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff
def marketplace(request):
    listings = LivestockItem.objects.filter(is_for_sale=True, status='available').order_by('-listing_date')
    context = {
        'listings': listings,
        'page_title': 'Marketplace'
    }
    return render(request, 'marketplace.html', context)
<<<<<<< HEAD

# 5. DETAIL VIEW
def livestock_detail(request, pk):
    livestock = get_object_or_404(LivestockItem, pk=pk)
    photos = livestock.images.all()
=======
    
# --- 5. DETAIL PAGE VIEW ---
def livestock_detail(request, pk):
    livestock = get_object_or_404(LivestockItem, pk=pk)
    order_form = SimpleOrderForm()
    
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff
    context = {
        'livestock': livestock,
        'order_form': order_form,
        'photos': livestock.images.all()
    }
    return render(request, 'livestock_detail.html', context)

<<<<<<< HEAD
# 6. PLACE ORDER VIEW (With Duplicate Check)
=======
# --- 6. ORDER PLACEMENT VIEW (Buy Now Logic) ---
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff
@login_required
def place_order(request, pk):
    if not hasattr(request.user, 'buyer_profile'):
        messages.error(request, "Only registered buyers can place orders.")
        return redirect('dashboard')
        
    livestock_item = get_object_or_404(LivestockItem, pk=pk)
    buyer = request.user.buyer_profile

<<<<<<< HEAD
    # Availability Check
    if not livestock_item.is_for_sale or livestock_item.status != 'available':
        messages.error(request, "This item has already been sold.")
        return redirect('livestock:marketplace')

    # Duplicate Check
    existing_order = Order.objects.filter(
        buyer=buyer, 
        payment_status='pending',
        order_items__livestock=livestock_item
    ).first()

    if existing_order:
        messages.info(request, "You already have a pending order for this item. Resuming payment...")
        return redirect('livestock:retry_payment', pk=existing_order.pk)
=======
    if livestock_item.is_for_sale == False or livestock_item.status != 'available':
        messages.error(request, "This item is not currently available for purchase.")
        return redirect('livestock:livestock_detail', pk=pk)
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff

    if request.method == 'POST':
        form = SimpleOrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
<<<<<<< HEAD
            amount = livestock_item.price * quantity
            tx_ref = str(uuid.uuid4())
            
            new_order = Order.objects.create(
                buyer=buyer,
                total_amount=amount,
                order_status='pending_payment',
                payment_status='pending',
            )
            
=======
            
            # 1. CREATE the Order header
            new_order = Order.objects.create(
                buyer=buyer,
                total_amount=livestock_item.price * quantity,
                order_status='pending_inquiry',
                payment_status='pending'
            )
            
            # 2. CREATE the OrderItem line
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff
            OrderItem.objects.create(
                order=new_order,
                livestock=livestock_item,
                quantity=quantity,
                unit_price_at_time=livestock_item.price,
            )

<<<<<<< HEAD
            context = {
                'order': new_order,
                'item': livestock_item,
                'tx_ref': tx_ref
            }
            return render(request, 'payment_simulation.html', context)
            
    return redirect('livestock:livestock_detail', pk=pk)

# 7. PAYMENT CALLBACK
@login_required
def payment_callback(request):
    tx_ref = request.GET.get('tx_ref')
    fake_status = request.GET.get('status') 

    if fake_status == 'success':
        order = Order.objects.filter(buyer=request.user.buyer_profile, payment_status='pending').last()
        
        if order:
            order.payment_status = 'paid'
            order.order_status = 'confirmed'
            order.save()
            
            # Use direct lookup to fix naming error
            items = OrderItem.objects.filter(order=order)
            for item in items:
                item.livestock.status = 'sold'
                item.livestock.is_for_sale = False
                item.livestock.save()
                
            messages.success(request, f"Payment Successful! Order #{order.order_id} confirmed.")
            return redirect('livestock:order_history')
            
    messages.error(request, "Payment failed or cancelled.")
    return redirect('dashboard')

# 8. BUYER ORDER HISTORY
=======
            messages.success(request, f"Your inquiry for {livestock_item.species.species_name} has been sent. Order #{new_order.pk} logged.")
            return redirect('dashboard') 
            
    return redirect('livestock:livestock_detail', pk=pk)

# --- 7. BUYER ORDER HISTORY ---
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff
@login_required
def order_history(request):
    if not hasattr(request.user, 'buyer_profile'):
        messages.error(request, "You are not registered as a buyer.")
        return redirect('dashboard')
        
    buyer_orders = Order.objects.filter(buyer=request.user.buyer_profile).order_by('-order_date')
    
    context = {
        'orders': buyer_orders,
        'page_title': 'My Order History'
    }
    return render(request, 'buyer_order_history.html', context)
<<<<<<< HEAD

# 9. FARMER SALES INQUIRIES
@login_required
def sales_inquiries(request):
    if not hasattr(request.user, 'farmer_profile'):
        messages.error(request, "You are not registered as a farmer.")
        return redirect('dashboard')
    
    farmer_items = LivestockItem.objects.filter(farmer=request.user.farmer_profile)
    sales_inquiries = OrderItem.objects.filter(livestock__in=farmer_items).select_related('order', 'livestock')
    
    context = {
        'inquiries': sales_inquiries,
        'page_title': 'Incoming Sales Inquiries'
    }
    return render(request, 'farmer_sales_inquiries.html', context)

# 10. APPROVE INQUIRY
@login_required
def approve_inquiry(request, pk):
    inquiry_item = get_object_or_404(OrderItem, pk=pk)
    
    if inquiry_item.livestock.farmer != request.user.farmer_profile:
        messages.error(request, "You do not have permission to manage this order.")
        return redirect('livestock:sales_inquiries')
=======

# --- 8. FARMER SALES INQUIRIES ---
@login_required
def sales_inquiries(request):
    if not hasattr(request.user, 'farmer_profile'):
        messages.error(request, "You are not registered as a farmer.")
        return redirect('dashboard')
    
    farmer_items = LivestockItem.objects.filter(farmer=request.user.farmer_profile)
    sales_inquiries = OrderItem.objects.filter(livestock__in=farmer_items).select_related('order', 'livestock').order_by('-order__order_date')
    
    context = {
        'inquiries': sales_inquiries,
        'page_title': 'Incoming Sales Inquiries'
    }
    return render(request, 'farmer_sales_inquiries.html', context)
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff

    order = inquiry_item.order
    order.order_status = 'confirmed'
    order.save()

<<<<<<< HEAD
    animal = inquiry_item.livestock
    animal.status = 'sold'
    animal.is_for_sale = False
    animal.save()
=======
# --- 9. FARMER ORDER ACTIONS (Accept/Reject) ---
@login_required
def accept_order(request, order_item_pk):
    if request.method != 'POST':
        return redirect('livestock:sales_inquiries')

    if not hasattr(request.user, 'farmer_profile'):
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    order_item = get_object_or_404(OrderItem, pk=order_item_pk)
    
    if order_item.livestock.farmer != request.user.farmer_profile:
        messages.error(request, "Error: You do not own this livestock item.")
        return redirect('livestock:sales_inquiries')

    if order_item.order.order_status != 'pending_inquiry':
        messages.warning(request, "This order has already been processed.")
        return redirect('livestock:sales_inquiries')

    order_item.order.order_status = 'confirmed'
    order_item.order.payment_status = 'confirmed' 
    order_item.order.save()

    livestock = order_item.livestock
    livestock.status = 'sold'
    livestock.is_for_sale = False
    livestock.save()

    messages.success(request, f"Sale approved! Livestock ID {livestock.tag_id} marked as confirmed sale.")
    return redirect('livestock:sales_inquiries')
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff

    messages.success(request, f"Sale confirmed! {animal.species.species_name} marked as SOLD.")
    return redirect('livestock:sales_inquiries')

<<<<<<< HEAD
# 11. REJECT INQUIRY
@login_required
def reject_inquiry(request, pk):
    inquiry_item = get_object_or_404(OrderItem, pk=pk)
    
    if inquiry_item.livestock.farmer != request.user.farmer_profile:
        messages.error(request, "Permission denied.")
        return redirect('livestock:sales_inquiries')

    order = inquiry_item.order
    order.order_status = 'cancelled'
    order.save()
    
    messages.info(request, "Inquiry rejected. The animal remains available.")
    return redirect('livestock:sales_inquiries')

# 12. RETRY PAYMENT (Smart Version)
@login_required
def retry_payment(request, pk):
    order = get_object_or_404(Order, pk=pk, buyer=request.user.buyer_profile)
    
    if order.payment_status == 'paid':
        messages.info(request, "This order is already paid.")
        return redirect('livestock:order_history')
        
    order_item = OrderItem.objects.filter(order=order).first()
    if not order_item:
        messages.error(request, "Order has no items.")
        return redirect('livestock:order_history')
        
    livestock_item = order_item.livestock
    
    # Check if sold to someone else
    if livestock_item.status == 'sold':
        # If sold, BUT this order is the one that is 'Confirmed' (Farmer Accepted), allow pay.
        if order.order_status == 'confirmed':
            pass 
        else:
            order.order_status = 'cancelled'
            order.save()
            messages.error(request, "Sorry, this item was sold to another buyer.")
            return redirect('livestock:order_history')
    
    tx_ref = str(uuid.uuid4())
    context = {
        'order': order,
        'item': livestock_item, 
        'tx_ref': tx_ref
    }
    return render(request, 'payment_simulation.html', context)
=======
@login_required
def reject_order(request, order_item_pk):
    if request.method != 'POST':
        return redirect('livestock:sales_inquiries')
    
    if not hasattr(request.user, 'farmer_profile'):
        messages.error(request, "Access denied.")
        return redirect('dashboard')
        
    order_item = get_object_or_404(OrderItem, pk=order_item_pk)

    if order_item.order.order_status != 'pending_inquiry':
        messages.warning(request, "This order has already been processed.")
        return redirect('livestock:sales_inquiries')
        
    order_item.order.order_status = 'rejected'
    order_item.order.save()

    messages.info(request, f"Inquiry #{order_item.order.order_id} has been rejected.")
    return redirect('livestock:sales_inquiries')
>>>>>>> 7e69cb7777706784fd40ea566681d39beed376ff
