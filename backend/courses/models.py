from django.db import models

class ClassInfo(models.Model):
    descr = models.TextField()
    full_name = models.TextField()
    internet_id = models.TextField()

    class Meta:
        managed = False
        db_table = 'class_info'
        unique_together = (('descr', 'full_name'),)