from django.db import models

# Create your models here.

class ProjectModel(models.Model):

    PROJECT_TYPE_CHOICES = ((1, "jar"), (2, "war"))

    name = models.CharField(unique=True, max_length=50, db_index=True, default='')
    url = models.CharField(max_length=200, null=False, blank=False)
    p_type = models.IntegerField(choices=PROJECT_TYPE_CHOICES, default=1)
    creator = models.EmailField()
    br = models.CharField(null=False, blank=False, default='master', max_length=20)
    tag = models.CharField(max_length=15, blank=False, null=False, default='v0')
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tb_project'
        managed = True


class PackageLogModel(models.Model):

    ENV_CHOICES = ((1, 'online'), (2, 'test'), (3, 'dev'))
    
    project = models.ForeignKey('ProjectModel', on_delete=models.CASCADE)
    br = models.CharField(null=False, blank=False, max_length=20)
    module = models.CharField(null=False, blank=False, max_length=20)
    env = models.IntegerField(choices=ENV_CHOICES, default=3)
    tag = models.CharField(max_length=15, blank=False, null=False)
    ptime = models.DateTimeField(auto_now_add=True)
    puser = models.EmailField()
    
    class Meta:
        db_table = 'tb_ci_log'
        managed = True


class UserProjectModel(models.Model):
    user = models.ForeignKey('user.UserModel', on_delete=models.CASCADE)
    project = models.ForeignKey('ProjectModel', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_user_project'
        managed = True


class GroupProjectModel(models.Model):
    group = models.ForeignKey('user.GroupModel', on_delete=models.CASCADE)
    project = models.ForeignKey('ProjectModel', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_group_project'
        managed = True