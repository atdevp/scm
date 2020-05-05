from django.db import models
from app.user.models import UserModel

# Create your models here.

class BUModel(models.Model):
    id = models.IntegerField(primary_key=True)
    bu_name = models.CharField(max_length=100, db_index=True)
    leader = models.ForeignKey(to='UserModel')
    parent_id = models.IntegerField()

    class Meta:
        db_table = 'tb_bu'
        managed = True
    
    def __str__(self):
        return self.bu_name

