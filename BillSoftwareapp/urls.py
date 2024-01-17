from . import views
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('service', views.service, name='service'),
    path('register', views.register, name='register'),
    path('registercompany', views.registercompany, name='registercompany'),
    path('registerstaff', views.registerstaff, name='registerstaff'),
    path('login', views.login, name='login'),
    path('registeruser', views.registeruser, name='registeruser'),
    path('add_company', views.add_company, name='add_company'),
    path('staff_registraction', views.staff_registraction, name='staff_registraction'),
    path('homepage', views.homepage, name='homepage'),
    path('staffhome', views.staffhome, name='staffhome'),
    path('loginurl', views.loginurl, name='loginurl'),
    path('logout', views.logout, name='logout'),
    path('base', views.base, name='base'),
    path('profile', views.profile, name='profile'),
    path('editprofile/<int:pk>/', views.editprofile, name='editprofile'),
    path('edit_profilesave/<int:pk>/', views.edit_profilesave, name='edit_profilesave'),
    path('editstaffprofile', views.editstaffprofile, name='editstaffprofile'),
    path('edit_staffprofilesave/', views.edit_staffprofilesave, name='edit_staffprofilesave'),
    path('staffprofile', views.staffprofile, name='staffprofile'),
    path('add_item', views.add_item, name='add_item'),
    path('item_create_new', views.item_create_new, name='item_create_new'),
    path('view_item', views.view_item, name='view_item'),
    path('view_items/<int:pk>/', views.view_items, name='view_items'),
    path('edit_item/<int:pk>/', views.edit_item, name='edit_item'),
    path('update_item/<int:pk>/', views.update_item, name='update_item'),
    path('item_delete/<int:pk>/', views.item_delete, name='item_delete'),
    path('itemhistory/<int:pk>/', views.itemhistory, name='itemhistory'),
    path('item_unit_create', views.item_unit_create, name='item_unit_create'),
    path('ajust_quantity/<int:pk>/', views.ajust_quantity, name='ajust_quantity'),
    path('itemmodaladjust/<int:pk>/', views.itemmodaladjust, name='itemmodaladjust'),
    path('edititemmodaladjust/<int:pk>/<int:trans>', views.edititemmodaladjust, name='edititemmodaladjust'),
    path('update_adjusted_transaction/<int:pk>/<int:trans>', views.update_adjusted_transaction, name='update_adjusted_transaction'),
    path('transaction_delete/<int:pk>', views.transaction_delete, name='transaction_delete'),
    path('item_delete_openstock/<int:pk>',views.item_delete_openstock,name='item_delete_openstock'),









]