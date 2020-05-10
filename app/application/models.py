from django.db import models
from app.project.models import ProjectModel

# Create your models here.
class ApplicationModel(models.Model):
    app = models.CharField(unique=True, max_length=100, db_index=True)
    pro_id = models.ForeignKey(to=ProjectModel, on_delete=models.SET_NULL, null=True)
    module = models.CharField(max_length=50, blank=True, null=True)
    scheme = models.CharField(max_length=10, blank=False, default='test')
    main_class = models.CharField(max_length=800, blank=True, null=True)
    main_args = models.CharField(max_length=800, blank=True, null=True)
    jvm_args = models.CharField(max_length=1000, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    script = models.TextField(blank=True, null=True, default=None)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tb_app"
        managed = True
        unique_together = ['app', 'module', 'scheme', 'pro_id']
        

    def __str__(self):
        return self.app












