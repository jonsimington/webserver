from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, HTML, Field
from crispy_forms.bootstrap import FormActions

from models import UserProfile


# Create the form class.
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()


    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            HTML('<hr>'),
            Field('about_me', placeholder="Tell us about yourself!",
                  css_class="input-block-level"),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel')
                ),
            )


    def save(self, *args, **kwargs):
        profile = super(UserProfileForm, self).save(*args, **kwargs)
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        profile.user.email = self.cleaned_data['email']
        profile.user.save(*args, **kwargs)
        print "Saved"
        return profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, request=None, **kwargs):
        self.request = request

        super(LoginForm, self).__init__(**kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Login',
                'username',
                'password',
            ),
            FormActions(
                Submit('login', 'Login'),
            ),
        )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data['username']
        password = cleaned_data['password']

        error_message = "Username/password combination does not match"

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(error_message)

        # Check the password
        if not user.check_password(password):
            raise forms.ValidationError(error_message)

        return cleaned_data

    def get_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        return authenticate(username=username, password=password)
