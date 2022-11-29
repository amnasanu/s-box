from django.urls import path
from .import views

urlpatterns = [
    path('',views.adminpanel,name="adminpanel"),
    path('admin_logout/',views.admin_logout,name="admin_logout"),
    path('user_accounts_table/<int:id>',views.user_accounts_table,name="user_accounts_table"),
    path('cart_table/<int:id>',views.cart_table,name="cart_table"),
    path('category_table/<int:id>/',views.category_table,name="category_table"),
    path('order_table/<int:id>/',views.order_table,name='order_table'),
    path('store_table/<int:id>/',views.store_table,name="store_table"),
    path('todayOffer/',views.todayoffer, name = "today_offer"),
    path('changeoffer/',views.changetodayoffer, name="changeoffer"),

    path('ban_user/<int:id>/',views.ban_user,name="ban_user"),
    path('unban_user/<int:id>/',views.unban_user,name='unban_user'),
    path('add_category/',views.add_category,name="add_category"),
    path('edit_category/<int:id>/',views.edit_category,name="edit_category"),
    path('delete_category/<int:id>/',views.delete_category,name='delete_category'),


    path('add_product/',views.add_product,name="add_product"),
    path('edit_product/<int:id>/',views.edit_product,name='edit_product'),
    path('delete_product/<int:id>/',views.delete_product,name="delete_product"),

    path('add_variations/',views.add_variations,name="add_variations"),
    path('edit_variations/<int:id>/',views.edit_variations,name='edit_variations'),
    path('delete_variatons/<int:id>/',views.delete_variatons,name="delete_variatons"),

    path('order_accepted/<int:order_id>',views.order_accepted,name="order_accepted"),
    path('order_completed/<int:order_id>',views.order_completed,name="order_completed"),
    path('order_cancelled/<int:order_id>',views.order_cancelled,name="order_cancelled"),




    
]
