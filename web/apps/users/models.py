from datetime import datetime
from django.utils.timezone import utc
import shortuuid

import hashlib
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# from .serializer import JWTUserProfileSerializer


class UserProfile(AbstractUser):
    """
    user
    """

    # first_name = None
    # last_name = None
    # user_name = models.CharField(max_length=64, verbose_name="name")
    # user_email = models.EmailField(max_length=256, verbose_name="email")
    # add_time = models.DateTimeField(default=datetime.now, verbose_name="user added time")

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "user"

    def __str__(self):
        return self.user_name

class Alias(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="alias name")
    is_used = models.BooleanField(default=False,verbose_name="is_used")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="add time", help_text="category added time")

    def __str__(self):
        return self.name
class UserMachine(models.Model):
    """
    user machine
    """
    machine_sn = models.CharField(max_length=16, blank=True, default='',verbose_name="machine sn")
    machine_secret = models.CharField(max_length=32, blank=True, default='', verbose_name="machine secret")
    machine_owner = models.ForeignKey(UserProfile)
    alias = models.OneToOneField(Alias,blank=True, null=True, verbose_name="alias", help_text="alias")
    os_name = models.CharField(max_length=32, verbose_name="operation system name")
    os_version = models.CharField(max_length=32, verbose_name="operation system version")
    comp_name = models.CharField(max_length=32, verbose_name="compiler name")
    comp_version = models.CharField(max_length=32, verbose_name="compiler version")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="machine added time")

    STATE_CHOICE = (
        (-1, 'prohibited'),
        (0, 'pending'),
        (1, 'active'),

    )
    state = models.IntegerField(choices=STATE_CHOICE, default=0,verbose_name="state", help_text="machine state")

    class Meta:
        verbose_name = "user machines"
        verbose_name_plural = "user machines"

    def __str__(self):
        return self.alias.__str__() + ' (' + self.os_name + ' ' + self.os_version + '' + self.comp_name + ' ' + self.comp_version + ')'

    def approve_machine(self):
        "Approve Machine(Modify the state to active, generate machine_sn, machine_secret, and assign an alias)"
        alias = Alias.objects.filter(is_used=False).order_by('?').first()
        if not alias:
            return {"is_success": False, "alias": '', "secret": '', "email":''}
        from django.db import transaction
        with transaction.atomic():
            alias.is_used=True
            alias.save()

            self.alias = alias
            self.state = 1
            if not self.machine_sn:
                self.machine_sn = shortuuid.ShortUUID().random(length=16)

            if not self.machine_secret:
                machine_str = self.alias.name + self.os_name + self.os_version + self.comp_name + self.comp_version + self.machine_sn

                m = hashlib.md5()
                m.update(make_password(str(machine_str), 'pg_perf_farm'))
                self.machine_secret = m.hexdigest()

            self.save()


        # serializer = JWTUserProfileSerializer(user)
        print(self.machine_owner.email)
        user_email = self.machine_owner.email
        system = self.os_name + ' ' + self.os_version
        compiler = self.comp_name + ' ' + self.comp_version
        return  {"is_success": True, "alias": self.alias.name, "secret": self.machine_secret, "system": system,  "compiler":compiler,"email":user_email}