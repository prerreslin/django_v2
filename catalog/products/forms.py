from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices={"liqpay":"With LiqPay", "monopay":"With MonoPay", "googlepay":"With Google Pay", "cash":"With Cash"})
    class Meta:
        model = Order
        fields = ['contact_name', 'contact_email', 'contact_phone', 'address', 'payment_method']
        labels = {'contact_name': 'Your Name:', 
                'contact_email': 'Your email address:', 
                'contact_phone': 'Your phone number:', 
                'address': 'Your address:',
                'payment_method': 'Payment Method:',
                }

