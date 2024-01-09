from django import forms


class LoginForm(forms.ModelForm):
    username = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control p-3',
                'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        label='Password',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control p-3',
                'placeholder': 'Password'
            }
        ))
    
    class Meta:
        model = None
        fields = ['username', 'password']