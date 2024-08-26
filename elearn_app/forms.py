from django import forms

class SignUpForm(forms.Form):
    choices = [
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ]


    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    user_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(max_length=15)
    role = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
    user_image = forms.ImageField(required=False)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class AddCourseForm(forms.Form):
    name = forms.CharField(max_length=100)
    category = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False)

