from django.db import models

# Create your models here.
class Tour(models.Model):
    name=models.CharField(max_length=200)
    weather=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    district=models.CharField(max_length=200)
    link=models.CharField(max_length=200)
    description=models.CharField(max_length=10000)
    image1=models.FileField(upload_to='media')
    image2=models.FileField(upload_to='media')

    def __str__(self):
        return "{}".format(self.name)