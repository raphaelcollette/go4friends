from django.db import models

class ClassInfo(models.Model):
    descr = models.TextField()
    full_name = models.TextField()
    hr_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'class_info'