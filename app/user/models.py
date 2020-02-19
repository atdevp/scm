from django.db import models
import django.utils.timezone as tz
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("the given email must be set")

        email = self.normalize_email(email)
        u = self.model(username=username, email=email, is_active=True, is_staff=False, role=3, **extra_fields)

        u.set_password(password)
        u.save(using=self._db)
        return u

    def create_superuser(self, username, email, password, **extra_fields):
        su = self.create_user(username, email, password, **extra_fields)
        su.is_staff = True
        su.is_active = True
        su.role = 1
        su.save(using=self._db)
        return su


class UserModel(AbstractBaseUser, PermissionsMixin):

    ACTIVE_CHOICES = ((1, "active"), (2, "die"), )
    ROLE_CHOICES = ((1, "admin"), (2, "team_leader"), (3, "user"), )
    GROUP_CHOICES = ((1, "ops"), (2, "dev"), (3, "recom"),)

    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=30, default='')
    mobile = models.IntegerField(blank=True, null=False, default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.IntegerField(choices=ROLE_CHOICES, default=3, blank=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_username(self):
        return self.email

    def natural_key(self):
        return (self.get_username(), )

    @property
    def is_authenticated(self):
        return True

    @property
    def is_superuser(self):

        return self.role == 1

    class Meta:
        db_table = 'tb_user'
        managed = True


class GroupModel(models.Model):
    groupname = models.CharField(unique=True, max_length=100)
    creater = models.EmailField(null=False, blank=False)
    ctime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tb_group"
        managed = True


class UserGroupModel(models.Model):
    id = models.IntegerField(primary_key=True)
    uid = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    gid = models.ForeignKey('GroupModel', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_user_group'
        managed = True
