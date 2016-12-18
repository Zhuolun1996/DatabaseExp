from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.
class ComRoom(models.Model):
    Room_name = models.CharField(max_length=100, primary_key=True)
    Room_address = models.CharField(max_length=100)
    IPS = models.CharField(max_length=50)

    def __str__(self):
        return self.Room_name


class Cabinet(models.Model):
    Cabinet_id = models.CharField(max_length=20, primary_key=True)
    Room_address = models.ForeignKey('ComRoom', on_delete=models.CASCADE)
    Cabinet_floor = models.CharField(max_length=50)
    Cabinet_position = models.CharField(max_length=50)
    Cabinet_machine_total = models.IntegerField()
    Bandwidth = models.CharField(max_length=50)
    Rest_IP = models.IntegerField()

    def __str__(self):
        return self.Cabinet_id


class Cabinet_inner_IP(models.Model):
    USING_CONDITION_CHOICES = (('inUsing', 'the IP is being using'), ('notUsing', 'the IP is not being using'))
    Cabinet_id = models.ForeignKey('Cabinet', on_delete=models.CASCADE)
    Inner_IP_address = models.CharField(max_length=20)
    Using_condition = models.CharField(max_length=10, choices=USING_CONDITION_CHOICES)

    class Meta:
        db_table = 'Global_IP_address'
        unique_together = (("Cabinet_id", "Inner_IP_address"))

    def __str__(self):
        return str(self.Cabinet_id) + '/' + self.Inner_IP_address


class Cabinet_outer_IP(models.Model):
    USING_CONDITION_CHOICES = (('inUsing', 'the IP is being using'), ('notUsing', 'the IP is not being using'))
    Cabinet_id = models.ForeignKey('Cabinet', on_delete=models.CASCADE)
    Outer_IP_address = models.CharField(max_length=20, primary_key=True)
    Using_condition = models.CharField(max_length=10, choices=USING_CONDITION_CHOICES)

    class Meta:
        db_table = 'Local_IP_address'

    def __str__(self):
        return str(self.Cabinet_id) + '/' + self.Outer_IP_address


class Customers(models.Model):
    Company_name = models.CharField(max_length=100, primary_key=True)
    Contacts = models.CharField(max_length=20)
    PhoneNumber = models.CharField(max_length=20)

    def __str__(self):
        return self.Company_name


class Equipments(models.Model):
    INTERFACE_TO_SWITCH_CHOICE = (
        ('F 0/0', 'FastEthernet 0/0'), ('F 0/1', 'FastEthernet 0/1'), ('F 0/2', 'FastEthernet 0/2'),
        ('F 0/3', 'FastEthernet 0/3'), ('F 0/4', 'FastEthernet 0/4'), ('F 0/5', 'FastEthernet 0/5'),
        ('F 0/6', 'FastEthernet 0/6'), ('F 0/7', 'FastEthernet 0/7'), ('F 0/8', 'FastEthernet 0/8'),
        ('F 0/9', 'FastEthernet 0/9'), ('F 0/10', 'FastEthernet 0/10'), ('F 0/11', 'FastEthernet 0/11'))
    PIN_code = models.CharField(max_length=50, primary_key=True)
    Model = models.CharField(max_length=50)
    Inner_IP_address = models.OneToOneField('Cabinet_inner_IP', on_delete=models.CASCADE, unique=True)
    Outer_IP_address = models.OneToOneField('Cabinet_outer_IP', on_delete=models.CASCADE, unique=True)
    Intface_to_switch = models.CharField(max_length=20, choices=INTERFACE_TO_SWITCH_CHOICE, unique=True)
    U_NUM = models.IntegerField()
    Cabinet_id = models.ForeignKey('Cabinet', on_delete=models.CASCADE)
    Bandwidth = models.CharField(max_length=50)
    Company_name = models.ForeignKey('Customers', on_delete=models.CASCADE)
    Machine_password = models.CharField(max_length=50)
    Using_date = models.DateField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not Cabinet.objects.get(Cabinet_id=self.Cabinet_id).Cabinet_machine_total >= 15:
            super(Equipments, self).save()

    def __str__(self):
        return self.PIN_code


@receiver(pre_save, sender=Cabinet)
def Cabinet_set_total_machine(sender, instance, **kwargs):
    instance.Cabinet_machine_total = Equipments.objects.filter(Cabinet_id=instance.Cabinet_id).count()
    instance.Rest_IP = Cabinet_outer_IP.objects.filter(Using_condition='notUsing').count()


@receiver(post_save, sender=Equipments)
def Equiments_Trigger_Cabinet_Created(sender, created, instance, **kwargs):
    new_Inner_IP_address = (str(instance.Inner_IP_address).split('/'))[1]
    new_Outer_IP_address = (str(instance.Outer_IP_address).split('/'))[1]
    OneToOne_Inner_IP = Cabinet_inner_IP.objects.get(Inner_IP_address=new_Inner_IP_address)
    OneToOne_Outer_IP = Cabinet_outer_IP.objects.get(Outer_IP_address=new_Outer_IP_address)
    OneToOne_Inner_IP.Using_condition = 'inUsing'
    OneToOne_Outer_IP.Using_condition = 'inUsing'
    OneToOne_Inner_IP.save()
    OneToOne_Outer_IP.save()
    if created == True:
        OneToOne_Cabinet = Cabinet.objects.get(Cabinet_id=instance.Cabinet_id)
        OneToOne_Cabinet.Cabinet_machine_total += 1
        OneToOne_Cabinet.Rest_IP -= 1
        OneToOne_Cabinet.save()


@receiver(post_delete, sender=Equipments)
def Equiments_trigger_Cabinet_Deleted(sender, instance, **kwargs):
    new_Inner_IP_address = (str(instance.Inner_IP_address).split('/'))[1]
    new_Outer_IP_address = (str(instance.Outer_IP_address).split('/'))[1]
    OneToOne_Inner_IP = Cabinet_inner_IP.objects.get(Inner_IP_address=new_Inner_IP_address)
    OneToOne_Outer_IP = Cabinet_outer_IP.objects.get(Outer_IP_address=new_Outer_IP_address)
    OneToOne_Inner_IP.Using_condition = 'notUsing'
    OneToOne_Outer_IP.Using_condition = 'notUsing'
    OneToOne_Inner_IP.save()
    OneToOne_Outer_IP.save()
    OneToOne_Cabinet = Cabinet.objects.get(Cabinet_id=instance.Cabinet_id)
    OneToOne_Cabinet.Cabinet_machine_total -= 1
    OneToOne_Cabinet.Rest_IP += 1
    OneToOne_Cabinet.save()
