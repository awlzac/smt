# Forms for smt
#
from django import forms
from addrmap.models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'            
