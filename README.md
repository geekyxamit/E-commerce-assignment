# E-commerce-assignment
Overview:
This repo shows an e-commerce platform with user, product and shipping cart tables.
Urls included:
- to register user
  path('register/', views.RegisterUser.as_view(), name='register')
- to login into user account
  path('login/', views.LoginUser.as_view(), name='login'),
- to add a product
  path('products/add/', views.AddProductApi.as_view(), name='add_product'),
- to update a product detai
  path('products/<str:product_id>/update/', views.UpdateProductApi.as_view(), name='add_product'),
- to view a certain product details
  path('products/<str:product_id>/detail/', views.ProductDetailApi.as_view(), name='add_product'),
- to view list of all avaliable products
  path('products/list/', views.ProductListApi.as_view(), name='add_product'),

Steps to run:
- Kindly create a virtual environment on your system
- Install the required dependencies


