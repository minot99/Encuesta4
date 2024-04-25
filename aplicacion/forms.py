from django import forms
from django.contrib.auth.models import User

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']  # Campos que se pueden editar

class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []  # No se necesitan campos ya que solo se va a eliminar el usuario