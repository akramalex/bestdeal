from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>', views.product_detail, name='product_detail'),
    path('<int:product_id>/submit_review/', views.submit_review, name='submit_review'),  # Add/Edit Review
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),  # Delete Review
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
]