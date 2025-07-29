from django.db import models

class ClassInfo(models.Model):
    id = models.AutoField(primary_key=True)
    descr = models.TextField()
    full_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'class_info'