from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name','phone', 'email','address_line_1','address_line_2','country','state','city','order_note']

    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)


        for field in self.fields:
            self.fields['first_name'].widget.attrs['placeholder'] = 'Enter the first Name'
            self.fields['last_name'].widget.attrs['placeholder'] = 'Enter the last Name'
            self.fields['email'].widget.attrs['placeholder'] = 'Enter the email address'
            self.fields['phone'].widget.attrs['placeholder'] = 'Enter the phone number'
            self.fields['address_line_1'].widget.attrs['placeholder'] = 'Enter the address'
            self.fields['address_line_2'].widget.attrs['placeholder'] = 'Enter the address '
            self.fields['city'].widget.attrs['placeholder'] = 'Enter your city '
            self.fields['state'].widget.attrs['placeholder'] = 'Enter your state'
            self.fields['country'].widget.attrs['placeholder'] = 'Enter your country'
            self.fields['order_note'].widget.attrs['placeholder'] = 'Enter the notes'
            
            self.fields[field].widget.attrs['class'] = 'form-control'