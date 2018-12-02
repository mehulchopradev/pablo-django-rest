from django.db import models

# Create your models here.

class PublicationHouse(models.Model):
    name = models.CharField(max_length=50, null=False)
    ratings = models.IntegerField(null=False)

    # books

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=50, null=False)
    price = models.FloatField(null=False)
    pages = models.IntegerField(null=True)

    publication = models.ForeignKey(PublicationHouse, on_delete=models.CASCADE, related_name='books', default=None)

    def __str__(self):
        return self.title
