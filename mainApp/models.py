from django.db import models

# Create your models here.
class UserCountTable(models.Model):
    count = models.IntegerField()

    def __str__(self):
        return str(self.count)
