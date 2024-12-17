from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('products/add/', views.AddProductApi.as_view(), name='add_product'),
    # path('products/<str:product_id>/update/', views.UpdateProductApi.as_view(), name='add_product'),
    # path('products/<str:product_id>/detail/', views.ProductDetailApi.as_view(), name='add_product'),
    # path('products/list/', views.ProductListApi.as_view(), name='add_product'),

    
]
