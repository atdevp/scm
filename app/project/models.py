from django.db import models
from django.db.models import Max

# Create your models here.


class ProjectModel(models.Model):

    PROJECT_TYPE_CHOICES = ((1, "jar"), (2, "war"), (3, "zip"))

    name = models.CharField(unique=True, max_length=50, db_index=True, default='')
    func = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=200, null=False, blank=False)
    p_type = models.CharField(max_length=5, null=False, blank=False)
    creator = models.EmailField()
    br = models.CharField(null=False, blank=False, default='master', max_length=20)
    tag = models.CharField(max_length=15, blank=False, null=False, default='')
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tb_project'
        managed = True


class PackageLogModel(models.Model):

    project = models.ForeignKey('ProjectModel', on_delete=models.CASCADE)
    br = models.CharField(null=False, blank=False, max_length=20)
    module = models.CharField(null=True, blank=True, max_length=20, default='')
    env = models.CharField(max_length=12, blank=False, null=False)
    tag = models.IntegerField(null=True, blank=True, default=1)
    msg = models.CharField(max_length=200, blank=True, null=True, default='')
    ptime = models.DateTimeField(auto_now_add=True)
    puser = models.EmailField()

    class Meta:
        db_table = 'tb_ci_log'
        ordering = ['-ptime']
        managed = True
        unique_together = ['project', 'module', 'tag', 'ptime']


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


# Get lastest tag number then return tag + 1
def get_new_tag(id):

    new_tag = "v1"

    if PackageLogModel.objects.filter(project_id=id).exists():
        m = PackageLogModel.objects.filter(env='online').all().aggregate(Max('tag'))
        if m['tag__max'] is None:
            return new_tag 
        if isinstance(m['tag__max'], int):
            new_tag = 'v{0}'.format(m['tag__max']+1)

    return new_tag
