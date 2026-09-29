from django.contrib import admin
from .models import Car, Booking, Contact


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "model",
        "price",
        "available",
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "car",
        "pickup_date",
        "return_date",
        "status",
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone",
        "created_at",
    )