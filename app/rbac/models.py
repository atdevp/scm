from django.db import models


# Create your models here.
class PermissionsModel(models.Model):
    uid = models.ForeignKey(to='user.UserModel', on_delete=models.CASCADE)
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=32)
    is_menu = models.BooleanField(default=False)


    class Meta:
        db_table = "tb_permissions"
        managed = True

    def __str__(self):
        return self.title
