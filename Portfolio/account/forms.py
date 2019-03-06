from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']: # for users to set their password and confirm it
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    #Django also provides a UserCreationForm form that you can use, which
    #resides in django.contrib.auth.forms and is very similar to the one we
    #have created.
    
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
#This will allow users to edit their first name, last
#name, and email, which are attributes of the built-in Django
#user model.
        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
 #This will allow users to edit the profile data we
#save in the custom Profile model. Users will be able to edit
#their date of birth and upload a picture for their profile       
        
        
        
        