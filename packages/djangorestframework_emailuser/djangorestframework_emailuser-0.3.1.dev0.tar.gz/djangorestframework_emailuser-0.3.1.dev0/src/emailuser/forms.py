from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class EmailUserCreationForm(UserCreationForm):
    class Meta():
        model = get_user_model()
        fields = ('email', 'name')


class EmailUserChangeForm(UserChangeForm):
    class Meta():
        model = get_user_model()
        fields = ('email', 'name')
