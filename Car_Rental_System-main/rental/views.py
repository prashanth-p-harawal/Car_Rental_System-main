from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Car, Booking, Contact
from .forms import CarForm, BookingForm, RegisterForm


# =====================================
# HOME
# =====================================

def home(request):
    return render(request, "home.html")


# =====================================
# CARS
# =====================================

def cars(request):

    cars = Car.objects.filter(available=True)

    search = request.GET.get("search")
    brand = request.GET.get("brand")
    fuel = request.GET.get("fuel")
    transmission = request.GET.get("transmission")

    if search:
        cars = cars.filter(name__icontains=search)

    if brand:
        cars = cars.filter(brand__icontains=brand)

    if fuel:
        cars = cars.filter(fuel=fuel)

    if transmission:
        cars = cars.filter(transmission=transmission)

    paginator = Paginator(cars, 6)
    page_number = request.GET.get("page")
    cars = paginator.get_page(page_number)

    return render(request, "cars.html", {
        "cars": cars
    })


# =====================================
# ABOUT
# =====================================

def about(request):
    return render(request, "about.html")


# =====================================
# CONTACT
# =====================================

def contact(request):

    if request.method == "POST":

        Contact.objects.create(
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )

        messages.success(
            request,
            "Your message has been sent successfully."
        )

        return redirect("contact")

    return render(request, "contact.html")



# =====================================
# BOOK CAR
# =====================================

@login_required(login_url="user_login")
def book_car(request, id):

    car = get_object_or_404(Car, id=id)

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            existing_booking = Booking.objects.filter(
                car=car,
                status__in=["Pending", "Confirmed"],
                pickup_date__lte=booking.return_date,
                return_date__gte=booking.pickup_date
            ).exists()

            if existing_booking:

                messages.error(
                    request,
                    "This car is already booked for the selected dates."
                )

                return render(
                    request,
                    "book_car.html",
                    {
                        "car": car,
                        "form": form
                    }
                )

            booking.car = car
            booking.user = request.user

            days = (booking.return_date - booking.pickup_date).days

            if days <= 0:
                days = 1

            booking.total_days = days
            booking.total_amount = days * car.price

            booking.save()

            messages.success(
                request,
                "Booking Confirmed Successfully!"
            )

            return redirect("booking_success", id=booking.id)

    else:

        form = BookingForm()

    return render(
        request,
        "book_car.html",
        {
            "car": car,
            "form": form
        }
    )


# =====================================
# BOOKING SUCCESS
# =====================================

def booking_success(request, id):

    booking = get_object_or_404(Booking, id=id)

    return render(
        request,
        "booking_success.html",
        {
            "booking": booking
        }
    )


# =====================================
# CUSTOMER REGISTER
# =====================================
# =====================================
# CUSTOMER REGISTER
# =====================================

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Registration successful! Please login."
        )

        return redirect("user_login")

    return render(request, "register.html")

# =====================================
# CUSTOMER LOGIN
# =====================================

def user_login(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            login(request, form.get_user())

            messages.success(
                request,
                "Welcome back!"
            )

            return redirect("home")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "user_login.html",
        {
            "form": form
        }
    )


# =====================================
# CUSTOMER LOGOUT
# =====================================
@login_required
def user_logout(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("home")

# =====================================
# ADMIN LOGIN
# =====================================

def login_view(request):

    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.is_staff:

                login(request, user)

                messages.success(
                    request,
                    "Welcome Admin!"
                )

                return redirect("dashboard")

            else:

                messages.error(
                    request,
                    "You are not authorized to access the admin dashboard."
                )

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "login.html")


# =====================================
# ADMIN LOGOUT
# =====================================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("home")


# =====================================
# ADMIN DASHBOARD
# =====================================

@login_required
def dashboard(request):

    if not request.user.is_staff:
        return redirect("home")

    total_cars = Car.objects.count()
    available = Car.objects.filter(available=True).count()
    unavailable = Car.objects.filter(available=False).count()
    total_bookings = Booking.objects.count()

    total_revenue = sum(
        booking.total_amount
        for booking in Booking.objects.all()
    )

    recent_bookings = Booking.objects.order_by("-id")[:5]

    context = {
        "total_cars": total_cars,
        "available": available,
        "unavailable": unavailable,
        "total_bookings": total_bookings,
        "total_revenue": total_revenue,
        "recent_bookings": recent_bookings,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


# =====================================
# CAR LIST
# =====================================

@login_required
def car_list(request):

    if not request.user.is_staff:
        return redirect("home")

    cars = Car.objects.all()

    return render(
        request,
        "cars/car_list.html",
        {
            "cars": cars
        }
    )


# =====================================
# ADD CAR
# =====================================

@login_required
def add_car(request):

    if not request.user.is_staff:
        return redirect("home")

    if request.method == "POST":

        form = CarForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Car added successfully."
            )

            return redirect("car_list")

    else:

        form = CarForm()

    return render(
        request,
        "dashboard/car_form.html",
        {
            "form": form,
            "title": "Add Car"
        }
    )


# =====================================
# EDIT CAR
# =====================================

@login_required
def edit_car(request, id):

    if not request.user.is_staff:
        return redirect("home")

    car = get_object_or_404(Car, id=id)

    if request.method == "POST":

        form = CarForm(
            request.POST,
            request.FILES,
            instance=car
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Car updated successfully."
            )

            return redirect("car_list")

    else:

        form = CarForm(instance=car)

    return render(
        request,
        "dashboard/car_form.html",
        {
            "form": form,
            "title": "Edit Car"
        }
    )


# =====================================
# DELETE CAR
# =====================================

@login_required
def delete_car(request, id):

    if not request.user.is_staff:
        return redirect("home")

    car = get_object_or_404(Car, id=id)

    if request.method == "POST":

        car.delete()

        messages.success(
            request,
            "Car deleted successfully."
        )

        return redirect("car_list")

    return render(
        request,
        "dashboard/delete_car.html",
        {
            "car": car
        }
    )


# =====================================
# CAR DETAIL
# =====================================

def car_detail(request, id):

    car = get_object_or_404(Car, id=id)

    return render(
        request,
        "car_detail.html",
        {
            "car": car
        }
    )
    
# =====================================
# BOOKING LIST (ADMIN)
# =====================================

@login_required
def booking_list(request):

    if not request.user.is_staff:
        return redirect("home")

    bookings = Booking.objects.all().order_by("-id")

    return render(
        request,
        "dashboard/booking_list.html",
        {
            "bookings": bookings
        }
    )


# =====================================
# UPDATE BOOKING (ADMIN)
# =====================================

@login_required
def update_booking(request, id):

    if not request.user.is_staff:
        return redirect("home")

    booking = get_object_or_404(Booking, id=id)

    if request.method == "POST":

        booking.status = request.POST.get("status")
        booking.save()

        messages.success(
            request,
            "Booking updated successfully."
        )

        return redirect("booking_list")

    return render(
        request,
        "dashboard/update_booking.html",
        {
            "booking": booking
        }
    )


# =====================================
# DELETE BOOKING (ADMIN)
# =====================================

@login_required
def delete_booking(request, id):

    if not request.user.is_staff:
        return redirect("home")

    booking = get_object_or_404(Booking, id=id)

    if request.method == "POST":

        booking.delete()

        messages.success(
            request,
            "Booking deleted successfully."
        )

        return redirect("booking_list")

    return render(
        request,
        "dashboard/delete_booking.html",
        {
            "booking": booking
        }
    )


# =====================================
# CUSTOMER DASHBOARD
# =====================================

@login_required(login_url="user_login")
def customer_dashboard(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by("-id")

    return render(
        request,
        "customer/dashboard.html",
        {
            "bookings": bookings
        }
    )


# =====================================
# CANCEL BOOKING
# =====================================

@login_required(login_url="user_login")
def cancel_booking(request, id):

    booking = get_object_or_404(
        Booking,
        id=id,
        user=request.user
    )

    if booking.status == "Pending":

        booking.status = "Cancelled"
        booking.save()

        messages.success(
            request,
            "Booking cancelled successfully."
        )

    else:

        messages.error(
            request,
            "Only pending bookings can be cancelled."
        )

    return redirect("customer_dashboard")