from django.shortcuts import render, redirect, Http404, HttpResponse
from ControlMode.forms import RegisterForm
from ControlMode.forms import LoginForm, ComRoomForm, CabinetForm, EquipmentForm, InnerIPForm, OuterIPForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from ControlMode.models import ComRoom, Cabinet, Cabinet_inner_IP, Cabinet_outer_IP, Equipments, Customers
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
import json


# Create your views here.
@login_required(login_url='/login/')
@permission_required('User.can_add_user', login_url='/login/', raise_exception='permission_denied')
def RegistUser(request):
    log_status = request.user.is_authenticated()
    if request.method == 'GET':
        Regist = RegisterForm()
        return render(request, 'Regist.html', {'RegistForm': Regist, 'log_status': log_status})
    else:
        Regist = RegisterForm(request.POST)
        if Regist.is_valid():
            _username = request.POST.get('username')
            _password = request.POST.get('password')
            _group = request.POST.get('groups')
            User.objects.create_user(username=_username, password=_password)
            newUser = User.objects.get(username=_username)
            newUser.groups.add(_group)
            return redirect('/')
    return render(request, 'Regist.html', {'RegistForm': Regist, 'log_status': log_status})


def LoginPage(request):
    log_status = request.user.is_authenticated()
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'LoginPage.html', {'form': form, 'log_status': log_status})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('/')
            else:
                return render(request, 'LoginPage.html',
                              {'form': form, 'password_is_wrong': True, 'log_status': log_status})
        else:
            return render(request, 'LoginPage.html', {'form': form, 'log_status': log_status})


@login_required(login_url="/login/")
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def Management(request):
    log_status = request.user.is_authenticated()
    ComRooms = ComRoom.objects.all()
    _ComRoom = ComRoomForm()
    return render(request, 'Management.html', {'log_status': log_status, 'ComRooms': ComRooms, 'ComRoomForm': _ComRoom})


def HomePage(request):
    log_status = request.user.is_authenticated()
    ComRooms = ComRoom.objects.all()
    return render(request, 'home.html', {'log_status': log_status, 'ComRooms': ComRooms})


@login_required(login_url='/login/')
def CabinetDetail(request, Room_name):
    log_status = request.user.is_authenticated()
    _CabinetForm = CabinetForm()
    Invalid_Input = request.GET.get('Invalid_Input')
    try:
        Room = ComRoom.objects.get(Room_name=str(Room_name))
        _Cabinet = Cabinet.objects.filter(Room_address=Room.Room_name)
    except ComRoom.DoesNotExist:
        raise Http404
    return render(request, 'cabinetdetail.html',
                  {'Room': Room, 'log_status': log_status, 'Cabinets': _Cabinet, 'CabinetForm': _CabinetForm,
                   'Invalid_Input': Invalid_Input})


@login_required(login_url='/login/')
@permission_required('ControlMode.add_comroom', login_url='/login/', raise_exception='permission_denied')
def addComRoom(request):
    log_status = request.user.is_authenticated()
    if request.method == 'GET':
        _ComRoom = ComRoomForm()
        return render(request, 'Management.html', {'ComRoomForm': _ComRoom, 'log_status': log_status})
    else:
        _ComRoom = ComRoomForm(request.POST)
        if _ComRoom.is_valid():
            _Room_name = request.POST.get('Room_name')
            _Room_address = request.POST.get('Room_address')
            _IPS = request.POST.get('IPS')
            ComRoom.objects.create(Room_name=_Room_name, Room_address=_Room_address, IPS=_IPS)
            return redirect('/management/')
        else:
            ComRooms = ComRoom.objects.all()
            return render(request, 'Management.html',
                          {'ComRoomForm': _ComRoom, 'log_status': log_status, 'ComRooms': ComRooms,
                           'Invalid_Input': True})


@login_required(login_url='/login/')
@permission_required('ControlMode.add_cabinet', login_url='/login/', raise_exception='permission_denied')
def addCabinet(request):
    log_status = request.user.is_authenticated()
    if request.method == 'GET':
        return redirect('/management/')
    else:
        _Cabinet = CabinetForm(request.POST)
        if _Cabinet.is_valid():
            _Cabinet_id = request.POST.get('Cabinet_id')
            _Room_address = request.POST.get('Room_address')
            _Cabinet_floor = request.POST.get('Cabinet_floor')
            _Cabinet_position = request.POST.get('Cabinet_position')
            _Bandwidth = request.POST.get('Bandwidth')
            _ComRoom = ComRoom.objects.get(Room_name=_Room_address)
            Cabinet.objects.create(Cabinet_id=_Cabinet_id, Room_address=_ComRoom, Cabinet_floor=_Cabinet_floor,
                                   Cabinet_position=_Cabinet_position, Bandwidth=_Bandwidth)
            return redirect('/cabinet' + str(_Room_address) + '/')
        else:
            _Room_address = request.POST.get('Room_address')
            return redirect('/cabinet' + str(_Room_address) + '/?Invalid_Input=True')


@login_required(login_url='/login/')
@permission_required('ControlMode.delete_cabinet', login_url='/login/', raise_exception='permission_denied')
def deleteCabinet(request, Cabinet_id):
    _Cabinet = Cabinet.objects.get(Cabinet_id=str(Cabinet_id))
    _Cabinet_Room_address = str(_Cabinet.Room_address)
    _Cabinet.delete()
    return redirect('/cabinet' + _Cabinet_Room_address + '/')


@login_required(login_url='/login/')
@permission_required('ControlMode.change_cabinet', login_url='/login/', raise_exception='permission_denied')
def changeCabinet(request, Cabinet_id):
    log_status = request.user.is_authenticated()
    _Cabinet = Cabinet.objects.get(Cabinet_id=str(Cabinet_id))
    _Cabinet_form = CabinetForm()
    return render(request, 'cabinetModify.html',
                  {'CabinetForm': _Cabinet_form, 'Cabinet': _Cabinet, 'log_status': log_status})


@login_required(login_url='/login/')
@permission_required('ControlMode.change_cabinet', login_url='/login/', raise_exception='permission_denied')
def updateCabinet(request):
    log_status = request.user.is_authenticated()
    if request.method == 'GET':
        return redirect('/management/')
    else:
        _Cabinet_id = request.POST.get('Cabinet_id')
        _Cabinet_Room_address = request.POST.get('Room_address')
        _Cabinet_update = Cabinet.objects.get(Cabinet_id=_Cabinet_id)
        _Cabinet_update.Cabinet_floor = request.POST.get('Cabinet_floor')
        _Cabinet_update.Cabinet_position = request.POST.get('Cabinet_position')
        _Cabinet_update.Bandwidth = request.POST.get('Bandwidth')
        _Cabinet_update.save()
        return redirect('/cabinet' + _Cabinet_Room_address + '/')


@login_required(login_url='/login/')
def Equipmentsdetail(request, Cabinet_id):
    log_status = request.user.is_authenticated()
    _EquipmentForm = EquipmentForm()
    Invalid_Input = request.GET.get('Invalid_Input')
    try:
        _Equipment = Equipments.objects.filter(Cabinet_id=str(Cabinet_id))
    except ComRoom.DoesNotExist:
        raise Http404
    return render(request, 'equipManagemnet.html',
                  {'log_status': log_status, 'Equipments': _Equipment, 'EquipmentForm': _EquipmentForm,
                   'Invalid_Input': Invalid_Input})


@login_required(login_url='/login/')
@permission_required('ControlMode.add_equipments', login_url='/login/', raise_exception='permission_denied')
def addEquipment(request):
    log_status = request.user.is_authenticated()
    if request.method == 'GET':
        _Equipment = EquipmentForm()
        return render(request, 'equipManagemnet.html', {'EquipmentForm': _Equipment, 'log_status': log_status})
    else:
        _Equipment = EquipmentForm(request.POST)
        if _Equipment.is_valid():
            _PIN_code = request.POST.get('PIN_code')
            _Model = request.POST.get('Model')
            _Inner_IP_address = request.POST.get('Inner_IP_address')
            _Outer_IP_address = request.POST.get('Outer_IP_address')
            _Intface_to_switch = request.POST.get('Intface_to_switch')
            _U_NUM = request.POST.get('U_NUM')
            _Cabinet_id = request.POST.get('Cabinet_id')
            _Bandwidth = request.POST.get('Bandwidth')
            _Company_name = request.POST.get('Company_name')
            _Machine_password = request.POST.get('Machine_password')
            _Using_date = request.POST.get('Using_date')
            _Cabinet = Cabinet.objects.get(Cabinet_id=_Cabinet_id)
            _Company = Customers.objects.get(Company_name=_Company_name)
            _Cabinet_Inner_IP = Cabinet_inner_IP.objects.get(Inner_IP_address=_Inner_IP_address)
            _Cabinet_Outer_IP = Cabinet_outer_IP.objects.get(Outer_IP_address=_Outer_IP_address)
            Equipments.objects.create(PIN_code=_PIN_code, Model=_Model, Inner_IP_address=_Cabinet_Inner_IP,
                                      Outer_IP_address=_Cabinet_Outer_IP, Intface_to_switch=_Intface_to_switch,
                                      U_NUM=_U_NUM, Cabinet_id=_Cabinet, Bandwidth=_Bandwidth,
                                      Company_name=_Company, Machine_password=_Machine_password,
                                      Using_date=_Using_date)
            return redirect('/equipment' + str(_Cabinet_id) + '/')
        else:
            _Cabinet_id = request.POST.get('Cabinet_id')
            return redirect('/equipment' + str(_Cabinet_id) + '/?Invalid_Input=True')


@login_required(login_url='/login/')
@permission_required('ControlMode.change_equipments', login_url='/login/', raise_exception='permission_denied')
def changeEquipment(request, PIN_code):
    log_status = request.user.is_authenticated()
    _Equipment = Equipments.objects.get(PIN_code=str(PIN_code))
    _EquipmentForm = EquipmentForm()
    return render(request, 'equipmentModify.html',
                  {'EquipmentForm': _EquipmentForm, 'Equipment': _Equipment, 'log_status': log_status})


@login_required(login_url='/login/')
@permission_required('ControlMode.change_equipments', login_url='/login/', raise_exception='permission_denied')
def updateEquipment(request):
    log_status = request.user.is_authenticated()
    if request.method == 'GET':
        return redirect('/management/')
    else:
        _PIN_code = request.POST.get('PIN_code')
        _Equipment_update = Equipments.objects.get(PIN_code=_PIN_code)
        _Equipment_update.Model = request.POST.get('Model')
        _Equipment_update.Inner_IP_address = Cabinet_inner_IP.objects.get(
            Inner_IP_address=request.POST.get('Inner_IP_address'))
        _Equipment_update.Outer_IP_address = Cabinet_outer_IP.objects.get(
            Outer_IP_address=request.POST.get('Outer_IP_address'))
        _Equipment_update.Intface_to_switch = request.POST.get('Intface_to_switch')
        _Equipment_update.U_NUM = request.POST.get('U_NUM')
        _Equipment_update.Cabinet_id = Cabinet.objects.get(Cabinet_id=request.POST.get('Cabinet_id'))
        _Equipment_update.Bandwidth = request.POST.get('Bandwidth')
        _Equipment_update.Company_name = Customers.objects.get(Company_name=request.POST.get('Company_name'))
        _Equipment_update.Machine_password = request.POST.get('Machine_password')
        _Equipment_update.Using_date = request.POST.get('Using_date')
        _Equipment_update.save()
        return redirect('/equipment' + request.POST.get('Cabinet_id') + '/')


@login_required(login_url='/login/')
@permission_required('ControlMode.delete_equipments', login_url='/login/', raise_exception='permission_denied')
def deleteEquipment(request, PIN_code):
    _Equipment = Equipments.objects.get(PIN_code=str(PIN_code))
    _Cabinet = str(_Equipment.Cabinet_id)
    _Equipment.delete()
    return redirect('/equipment' + _Cabinet + '/')


@login_required(login_url='/login/')
def InnerIPDetail(request, Cabinet_id):
    log_status = request.user.is_authenticated()
    _Cabinet_Inner_IP = InnerIPForm()
    Invalid_Input = request.GET.get('Invalid_Input')
    try:
        _Inner_IP = Cabinet_inner_IP.objects.filter(Cabinet_id=str(Cabinet_id))
        print(_Inner_IP)
    except ComRoom.DoesNotExist:
        raise Http404
    return render(request, 'InnerIPManagement.html',
                  {'log_status': log_status, 'Cabinet_Inner_IP': _Inner_IP, 'InnerIPForm': _Cabinet_Inner_IP,
                   'Invalid_Input': Invalid_Input})


@login_required(login_url='/login/')
@permission_required('ControlMode.add_cabinet_inner_ip', login_url='/login/',
                     raise_exception='permission_denied')
def addInnerIP(request):
    log_status = request.user.is_authenticated()
    if request.method == 'GET':
        return redirect('/management/')
    else:
        _Cabinet_Inner_IP = InnerIPForm(request.POST)
        if _Cabinet_Inner_IP.is_valid():
            _Cabinet_id = request.POST.get('Cabinet_id')
            _Inner_IP_address = request.POST.get('Inner_IP_address')
            _Using_condition = request.POST.get('Using_condition')
            _Cabinet = Cabinet.objects.get(Cabinet_id=_Cabinet_id)
            Cabinet_inner_IP.objects.create(Cabinet_id=_Cabinet, Inner_IP_address=_Inner_IP_address,
                                            Using_condition=_Using_condition)
            return redirect('/InnerIPManagement' + str(_Cabinet_id) + '/')
        else:
            _Cabinet_id = request.POST.get('Cabinet_id')
            return redirect('/InnerIPManagement' + str(_Cabinet_id) + '/?Invalid_Input=True')


@login_required(login_url='/login/')
@permission_required('ControlMode.change_cabinet_inner_ip',login_url='/login/',raise_exception='permission_denied')
def changeInnerIP(request, Cabinet_id, InnerIP):
    log_status = request.user.is_authenticated()
    _InnerIP = Cabinet_inner_IP.objects.get(Inner_IP_address=str(InnerIP),Cabinet_id=str(Cabinet_id))
    _InnerIPForm = InnerIPForm()
    return render(request, 'IPModify.html',
                  {'InnerIPForm': _InnerIPForm, 'InnerIP': _InnerIP, 'log_status': log_status, 'From': 'Inner'})


@login_required(login_url='/login/')
@permission_required('ControlMode.change_cabinet_inner_ip',login_url='/login/',raise_exception='permission_denied')
def updateInnerIP(request):
    log_status = request.user.is_authenticated()
    if request.method == 'GET':
        return redirect('/management/')
    else:
        _Cabinet_id = request.POST.get('Cabinet_id')
        _Inner_IP_address = request.POST.get('Inner_IP_address')
        _Using_condition = request.POST.get('Using_condition')
        _InnerIP = Cabinet_inner_IP.objects.get(Inner_IP_address=_Inner_IP_address,Cabinet_id=_Cabinet_id)
        _Cabinet = Cabinet.objects.get(Cabinet_id=_Cabinet_id)
        _InnerIP.Cabinet_id = _Cabinet
        _InnerIP.Inner_IP_address = _Inner_IP_address
        _InnerIP.Using_condition = _Using_condition
        _InnerIP.save()
        return redirect('/InnerIPManagement' + _Cabinet_id + '/')


@login_required(login_url='/login/')
@permission_required('ControlMode.delete_cabinet_inner_ip',login_url='/login/',raise_exception='permission_denied')
def deleteInnerIP(request, InnerIP):
    _Cabinet_Inner_IP = Cabinet_inner_IP.objects.get(Inner_IP_address=InnerIP)
    _Cabinet = str(_Cabinet_Inner_IP.Cabinet_id)
    _Cabinet_Inner_IP.delete()
    return redirect('/InnerIPManagement' + _Cabinet + '/')


@login_required(login_url='/login/')
def OuterIPDetail(request, Cabinet_id):
    log_status = request.user.is_authenticated()
    _Cabinet_Outer_IP = OuterIPForm()
    Invalid_Input = request.GET.get('Invalid_Input')
    try:
        _OuterIP = Cabinet_outer_IP.objects.filter(Cabinet_id=str(Cabinet_id))
        print(_OuterIP)
    except ComRoom.DoesNotExist:
        raise Http404
    return render(request, 'OuterIPManagement.html',
                  {'log_status': log_status, 'Cabinet_Outer_IP': _OuterIP, 'OuterIPForm': _Cabinet_Outer_IP,
                   'Invalid_Input': Invalid_Input})


@login_required(login_url='/login/')
@permission_required('ControlMode.add_cabinet_outer_ip', login_url='/login/',
                     raise_exception='permission_denied')
def addOuterIP(request):
    log_status = request.user.is_authenticated()
    if request.method == 'GET':
        return redirect('/management/')
    else:
        _Cabinet_Outer_IP = OuterIPForm(request.POST)
        if _Cabinet_Outer_IP.is_valid():
            _Cabinet_id = request.POST.get('Cabinet_id')
            _Outer_IP_address = request.POST.get('Outer_IP_address')
            _Using_condition = request.POST.get('Using_condition')
            _Cabinet = Cabinet.objects.get(Cabinet_id=_Cabinet_id)
            Cabinet_outer_IP.objects.create(Cabinet_id=_Cabinet, Outer_IP_address=_Outer_IP_address,
                                            Using_condition=_Using_condition)
            return redirect('/OuterIPManagement' + str(_Cabinet_id) + '/')
        else:
            _Cabinet_id = request.POST.get('Cabinet_id')
            return redirect('/OuterIPManagement' + str(_Cabinet_id) + '/?Invalid_Input=True')


@login_required(login_url='/login/')
@permission_required('ControlMode.change_cabinet_outer_ip', login_url='/login/',
                     raise_exception='permission_denied')
def changeOuterIP(request, OuterIP):
    log_status = request.user.is_authenticated()
    _OuterIP = Cabinet_outer_IP.objects.get(Outer_IP_address=str(OuterIP))
    _OuterIPForm = OuterIPForm()
    return render(request, 'IPModify.html',
                  {'OuterIPForm': _OuterIPForm, 'OuterIP': _OuterIP, 'log_status': log_status, 'From': 'Outer'})

@login_required(login_url='/login/')
@permission_required('ControlMode.change_cabinet_outer_ip', login_url='/login/',
                     raise_exception='permission_denied')
def updateOuterIP(request):
    log_status = request.user.is_authenticated()
    if request.method == 'GET':
        return redirect('/management/')
    else:
        _Cabinet_id = request.POST.get('Cabinet_id')
        _Outer_IP_address = request.POST.get('Outer_IP_address')
        _Using_condition = request.POST.get('Using_condition')
        _OuterIP = Cabinet_outer_IP.objects.get(Outer_IP_address=_Outer_IP_address)
        _Cabinet = Cabinet.objects.get(Cabinet_id=_Cabinet_id)
        _OuterIP.Cabinet_id = _Cabinet
        _OuterIP.Outer_IP_address = _Outer_IP_address
        _OuterIP.Using_condition = _Using_condition
        _OuterIP.save()
        return redirect('/OuterIPManagement' + _Cabinet_id + '/')


@login_required(login_url='/login/')
@permission_required('ControlMode.delete_cabinet_outer_ip', login_url='/login/',
                     raise_exception='permission_denied')
def deleteOuterIP(request, OuterIP):
    _Cabinet_Outer_IP = Cabinet_outer_IP.objects.get(Outer_IP_address=OuterIP)
    _Cabinet = str(_Cabinet_Outer_IP.Cabinet_id)
    _Cabinet_Outer_IP.delete()
    return redirect('/OuterIPManagement' + _Cabinet + '/')
