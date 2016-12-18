from django import forms
from django.contrib.auth.models import User
from ControlMode.models import ComRoom, Cabinet, Cabinet_inner_IP, Cabinet_outer_IP, Equipments, Customers


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'groups']


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label=u'username', error_messages={'required': 'username is required'},
                               widget=forms.TextInput(attrs={'placeholder': u'username'}))
    password = forms.CharField(required=True, label=u'password', error_messages={'required': 'password is required'},
                               widget=forms.PasswordInput(attrs={'placeholder': u'password'}))

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"username and password are required")
        else:
            cleaned_data = super(LoginForm, self).clean()


class ComRoomForm(forms.ModelForm):
    class Meta:
        model = ComRoom
        fields = '__all__'


class CabinetForm(forms.ModelForm):
    class Meta:
        model = Cabinet
        fields = '__all__'


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipments
        fields = '__all__'


class InnerIPForm(forms.ModelForm):
    class Meta:
        model = Cabinet_inner_IP
        fields = '__all__'


class OuterIPForm(forms.ModelForm):
    class Meta:
        model = Cabinet_outer_IP
        fields = '__all__'
