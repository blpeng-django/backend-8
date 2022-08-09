from django.db import models

# Create your models here.


class Book(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    author = models.CharField(max_length=100, null=False, default="알수없음")
    publisher = models.CharField(max_length=100, null=False, default="알수없음")
    price = models.IntegerField(null=False, default=0)

    def __str__(self) -> str:
        return self.name
