from django import forms
from FoodApp.models import Order
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name','email','mobile','address']

    def clean(self):
        super(OrderForm, self).clean()
        name = self.cleaned_data.get('name')
        mobile = self.cleaned_data.get('mobile')
        email = self.cleaned_data.get('email')
        address = self.cleaned_data.get('address')
        if not name:
            self._errors['username'] = self.error_class([
                'Please provide your name'])
        mb_bool_val = mobile.isnumeric()
        if mb_bool_val == False:
            self._errors['mobile'] = self.error_class([
                'Please proide your 10 digit mobile number'])
        elif len(mobile) != 10:
           self._errors['mobile'] = self.error_class([
               'Please proide your 10 digit mobile number'])
        if not address:
            self._errors['address'] = self.error_class([
                'Please provide your address'])
        if not email:
            self._errors['email'] = self.error_class([
                'Please provide your valid email'])
        # return any errors if found
        return self.cleaned_data

        # total_data = super().clean()
        # if len(total_data['mobile']) != 10:
        #     raise ValidationError("Please provide valid mobile number")
        # if not total_data['name']:
        #     raise ValidationError("Please enter your name")
        # if not total_data['email']:
        #     raise ValidationError("Please enter your email")
        # if not total_data['address']:
        #     raise ValidationError("Please enter your address for delievery")


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'input-text with-border'}))
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name']
