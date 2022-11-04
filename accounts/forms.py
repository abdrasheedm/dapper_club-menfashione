from .models import Account
from django import forms


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder' : 'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder' : 'confirm Password'}))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email address'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match! "
            )





# class CustomUserForm(UserCreationForm):
#     first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder' : 'Enter first name'}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder' : 'Enter last name'}))
#     username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder' : 'Enter username'}))
#     email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder' : 'Enter email'}))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2', 'placeholder' : 'Enter Password'}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2', 'placeholder' : 'confirm password'}))

#     class Meta:
#         model = User
#         fields = ['first_name','last_name','username', 'email','password1','password2']

