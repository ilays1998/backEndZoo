from django.db import models

# Create your models here.


class Metadata(models.Model):
    domain = models.CharField(max_length=30)
    kingdom = models.CharField(max_length=30)
    pyhlum = models.CharField(max_length=30)
    _class = models.CharField(max_length=30)
    superfamily = models.CharField(max_length=30)
    family = models.CharField(max_length=30)

    def __str__(self):
        return str(self.family)


class Animal(models.Model):
    name = models.CharField("animal name", max_length=30)
    image = models.URLField("animal image")
    age = models.IntegerField("animal age", default=0)
    metadata = models.ForeignKey(Metadata, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + ", age:" + str(self.age) + ", family: " + str(self.metadata)



