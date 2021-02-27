from django import forms

from apps.account.models import User


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'repeat_password']


class LogInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)  # thisIsMyEmail == thisismyemail
        if not qs.exists():
            raise forms.ValidationError("This is an invalid user.")
        elif qs.count() != 1:
            raise forms.ValidationError("This is an invalid user.")
        return email