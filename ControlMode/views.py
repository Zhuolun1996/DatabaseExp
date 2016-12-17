from django.shortcuts import render
from ControlMode.forms import RegisterForm


# Create your views here.
def RegistUser(request):
    if request.method == 'GET':
        Regist = RegisterForm()
        return render(request, 'Regist.html', {'RegistForm': Regist})
    else:
        Regist = RegisterForm(request.POST)
    render(request, 'Regist.html', {'RegistForm': Regist})
