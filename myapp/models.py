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
      # @property
      # def started(self):
      #       if(self.programStarted):
      #             pass
      #             return 1
      #       else:
      #             return 0      
      def __str__(self):
            return str(self.img0)+' - '+str(self.img1)+' - '+str(self.img2)+' - '+str(self.img3)
class TrafficLight(models.Model):
      
      color=models.CharField(default='white',max_length=20)
      sn=models.IntegerField(default=0)
      greenTime=models.FloatField(default=0)
      yellowTime=models.FloatField(default=0)
      emergency = models.BooleanField(default=False)
      def __str__(self):
            return str(self.sn)+' - '+self.color+' - '+str(self.emergency)