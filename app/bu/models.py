from django.db import models
from app.user.models import UserModel
from app.application.models import ApplicationModel

# Create your models here.

class BUModel(models.Model):
    id = models.IntegerField(primary_key=True)
    bu_name = models.CharField(max_length=100, db_index=True)
    leader = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
    parent_id = models.IntegerField()

    class Meta:
        db_table = 'tb_bu'
        managed = True
    
    def __str__(self):
        return self.bu_name


class BuApplicationModel(models.Model):
    id = models.IntegerField(primary_key=True)
    bid = models.ForeignKey(to=BUModel, null=True, on_delete=models.SET_NULL)
    aid = models.ForeignKey(to=ApplicationModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_bu_app'
        managed = True

    def __str__(self):
        pass