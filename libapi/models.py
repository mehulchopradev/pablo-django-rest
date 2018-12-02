from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=50, null=False)
    price = models.FloatField(null=False)
    pages = models.IntegerField(null=True)

    def __str__(self):
        return self.title
