from django.urls import path

from . import views

urlpatterns = [
    # store main page
    path('', views.Store, name='store'),
    
    # Individual products
    path('product/<slug:slug>', views.product_info, name='product-info'),
    
    # Individual category
    path('search/<slug:category_slug>', views.list_category, name="list-category"),

]

