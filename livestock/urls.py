from django.urls import path
from . import views

app_name = 'livestock'

urlpatterns = [
    # Farmer Create Flow
    path('add/', views.livestock_create, name='livestock_add'),
    path('add/<int:pk>/photos/', views.add_photos, name='add_photos'),
    path('add/success/', views.upload_success, name='upload_success'),

    # Buyer Marketplace
    path('marketplace/', views.marketplace, name='marketplace'),
    
    # NEW: Detail Page
    path('<int:pk>/', views.livestock_detail, name='livestock_detail'),

    # Order Placement URL
    path('<int:pk>/place-order/', views.place_order, name='place_order'),
]