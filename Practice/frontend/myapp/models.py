from django.db import models

# Create your models here.
class Image(models.Model):
      picture=models.ImageField()
      sn=models.IntegerField(default=1)
      def __str__(self):
            return str(self.sn)
class CurrentImages(models.Model):
      img0=models.IntegerField(default=1)
      img1=models.IntegerField(default=1)
      img2=models.IntegerField(default=1)
      img3=models.IntegerField(default=1)
      programStarted = models.BooleanField(default=False)
                  
class TrafficLight(models.Model):
      
      color=models.CharField(default='white',max_length=20)
      sn=models.IntegerField(default=0)
      greenTime=models.FloatField(default=0)
      yellowTime=models.FloatField(default=0)
      def __str__(self):
            return str(self.sn)