from django.urls import path

from . import views

urlpatterns = [
    path('', views.render_home_page, name='home_path'),
    path('products/', views.render_products_list_page, name='products_list_path'),
    path('products/<int:product_id>/', views.render_product_detail_page, name='product_path'),
    path('authorization/', views.render_authorization_page, name='authorization_path'),
    path('registration/', views.render_registration_page, name='registration_path'),
    path('logout/', views.render_logout_page, name='logout_path'),
    path('wishlist/', views.render_wishlist_page, name='wishlist_path'),
    path('wishlist/<int:product_id>/', views.activate_favourite, name='activate_favorite'),
    path('cart/', views.render_cart_page, name='cart_path'),
    path('cart/update/<int:product_id>/<str:action>/<int:quantity>/', views.update_cart, name='update_cart_path'),
    path('products/search/', views.search_products, name='search')
]