"""ComRoom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import ControlMode.views as Control_Views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^regist/$', Control_Views.RegistUser, name='regist'),
    url(r'^login/$', Control_Views.LoginPage, name='login'),
    url(r'^logout/$', Control_Views.logout, name='logout'),
    url(r'^management/$', Control_Views.Management, name='management'),
    url(r'^$', Control_Views.HomePage, name='homepage'),
    url(r'^cabinet(?P<Room_name>\w+)/$', Control_Views.CabinetDetail, name='cabinet'),
    url(r'^addRoom/$', Control_Views.addComRoom, name='addroom'),
    url(r'^addCabinet/$', Control_Views.addCabinet, name='addcabinet'),
    url(r'^deleteCabinet(?P<Cabinet_id>\w+)/$', Control_Views.deleteCabinet, name='deletecabinet'),
    url(r'^changeCabinet(?P<Cabinet_id>\w+)/$', Control_Views.changeCabinet, name='changecabinet'),
    url(r'^updateCabinet/$', Control_Views.updateCabinet, name='updateCabinet'),
    url(r'^equipment(?P<Cabinet_id>\w+)/$', Control_Views.Equipmentsdetail, name='equipmentdetail'),
    url(r'^addEquipment/$', Control_Views.addEquipment, name='addequipment'),
    url(r'^changeEquipment(?P<PIN_code>\w+)/$', Control_Views.changeEquipment, name='changeequipment'),
    url(r'^updateEquipment', Control_Views.updateEquipment, name='updateequipment'),
    url(r'^deleteEquipment(?P<PIN_code>\w+)/$', Control_Views.deleteEquipment, name='deleteequipment'),
    url(r'^InnerIPManagement(?P<Cabinet_id>\w+)/$', Control_Views.InnerIPDetail, name='inneripmanagement'),
    url(r'^addInnerIP', Control_Views.addInnerIP, name='addinnerip'),
    url(r'^changeInnerIP(?P<Cabinet_id>\S+)/(?P<InnerIP>\S+)$', Control_Views.changeInnerIP, name='changeinnerip'),
    url(r'^updateInnerIP/$', Control_Views.updateInnerIP, name='updateinnerip'),
    url(r'^deleteInnerIP(?P<InnerIP>\S+)/$', Control_Views.deleteInnerIP, name='deleteinnerip'),
    url(r'^OuterIPManagement(?P<Cabinet_id>\w+)/$', Control_Views.OuterIPDetail, name='outeripmanagement'),
    url(r'^addOuterIP', Control_Views.addOuterIP, name='addouterip'),
    url(r'^changeOuterIP(?P<OuterIP>\S+)/$', Control_Views.changeOuterIP, name='changeouterip'),
    url(r'^updateOuterIP/$', Control_Views.updateOuterIP, name='updateouterip'),
    url(r'^deleteOuterIP(?P<OuterIP>\S+)/$', Control_Views.deleteOuterIP, name='deleteouterip'),
]
