from django.db import models
from app.user.models import UserModel, GroupModel

# Create your models here.

class HostModel(models.Model):

    HOST_CHOICES = ((1, 'physical'), (2, 'virtual'))
    STATE_CHOICES = ((1, 'online'), (2, 'offline'))

    p_ip = models.CharField(max_length=15, db_index=True, unique=True)
    o_ip = models.CharField(max_length=15)
    h_type = models.IntegerField(choices=HOST_CHOICES, default=1)
    cores = models.IntegerField(default=1, blank=True)
    mem = models.IntegerField(null=False, blank=True)
    storage = models.IntegerField(null=False, blank=True)
    passwd = models.CharField(null=False, blank=True, max_length=50)
    state = models.IntegerField(choices=STATE_CHOICES, default=1)

    class Meta:
        db_table = 'tb_host'
        managed = True


class UserHostModel(models.Model):
    user = models.ForeignKey('user.UserModel', on_delete=models.CASCADE)
    host = models.ForeignKey('HostModel', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_user_host'
        managed = True


class GroupHostModel(models.Model):
    group = models.ForeignKey('user.GroupModel', on_delete=models.CASCADE)
    host = models.ForeignKey('HostModel', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_group_host'
        managed = True