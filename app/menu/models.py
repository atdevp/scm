from django.db import models

# Create your models here.

class MenuModel(models.Model):
    name =  models.CharField(max_length=60, unique=True, db_index=True)
    show_name = models.CharField(max_length=60)
    is_has_son = models.SmallIntegerField()
    parent_id = models.IntegerField()
    url = models.CharField(max_length=255)
    is_new_blank = models.SmallIntegerField()
    icon = models.CharField(max_length=32)
    
    class Meta:
        db_table = "tb_menu"
        managed = True

    def __str__(self):
        return self.name
