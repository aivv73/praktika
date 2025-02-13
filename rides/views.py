from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import RideForm, BookingForm
from .models import Ride, Booking
from django.contrib.auth.decorators import login_required 

@login_required 
def create_ride(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.driver = request.user  
            ride.save()
            return redirect('ride_list') 
    else:
        form = RideForm()
    return render(request, 'rides/create_ride.html', {'form': form})

@login_required(login_url='/rides/login') 
def ride_list(request):
    rides = Ride.objects.all()
    return render(request, 'rides/list.html', {'rides': rides})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('ride_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def create_booking(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.ride = ride
            booking.passenger = request.user
            
            if booking.seats_requested > ride.seats_available:
                form.add_error('seats_requested', 'Недостаточно свободных мест')
            else:
                booking.save()
                return redirect('ride_list')
    else:
        form = BookingForm()
    
    return render(request, 'rides/create_booking.html', {'form': form, 'ride': ride})

@login_required
def manage_booking(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.user != booking.ride.driver:
        return redirect('ride_list')
    
    if action == 'accept':
        booking.status = 'accepted'
        booking.ride.seats_available -= booking.seats_requested
        booking.ride.save()
    elif action == 'reject':
        booking.status = 'rejected'
    
    booking.save()
    return redirect('booking_requests')

@login_required
def booking_requests(request):
    bookings = Booking.objects.filter(ride__driver=request.user)
    return render(request, 'rides/booking_requests.html', {'bookings': bookings})