from django.urls import path
from . import views

urlpatterns = [

    # Home
    path('', views.home, name='home'),

    # Pages
    path('cars/', views.cars, name='cars'),
    path('car/<int:id>/', views.car_detail, name='car_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Booking
    path('book/<int:id>/', views.book_car, name='book_car'),
    path('booking-success/<int:id>/', views.booking_success, name='booking_success'),

    # -------------------------
    # Customer Authentication
    # -------------------------
    path('register/', views.register, name='register'),
    path('user-login/', views.user_login, name='user_login'),
    path('user-logout/', views.user_logout, name='user_logout'),

    # Customer Dashboard
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('cancel-booking/<int:id>/', views.cancel_booking, name='cancel_booking'),

    # -------------------------
    # Admin Authentication
    # -------------------------
    path('admin-login/', views.login_view, name='login'),
    path('admin-logout/', views.logout_view, name='logout'),

    # Admin Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Car Management
    path('dashboard/cars/', views.car_list, name='car_list'),
    path('dashboard/add-car/', views.add_car, name='add_car'),
    path('dashboard/edit-car/<int:id>/', views.edit_car, name='edit_car'),
    path('dashboard/delete-car/<int:id>/', views.delete_car, name='delete_car'),

    # Booking Management
    path('dashboard/bookings/', views.booking_list, name='booking_list'),
    path('dashboard/booking/update/<int:id>/', views.update_booking, name='update_booking'),
    path('dashboard/booking/delete/<int:id>/', views.delete_booking, name='delete_booking'),

]