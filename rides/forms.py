from django import forms
from .models import Ride, Booking
from django.core.exceptions import ValidationError
from django.utils import timezone

class RideForm(forms.ModelForm):
    seats_available = forms.TypedChoiceField(
        choices=[(i, i) for i in range(1, 5)],  
        coerce=int,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    departure_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'YYYY-MM-DD HH:MM'
        }),
        input_formats=['%Y-%m-%d %H:%M'],
    )

    def clean_departure_time(self):
        departure_time = self.cleaned_data['departure_time']
        if departure_time < timezone.now():
            raise ValidationError("Дата не может быть в прошлом!")
        return departure_time

    class Meta:
        model = Ride
        fields = ['from_location', 'to_location', 'departure_time', 'seats_available', 'price']
        widgets = {
            'from_location': forms.TextInput(attrs={'class': 'form-control'}),
            'to_location': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seats_requested']
        labels = {'seats_requested': 'Количество мест'}