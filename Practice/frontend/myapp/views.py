from django.shortcuts import render

# Create your views here.
from myapp.models import *
from .serializers import *
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
import numpy as np
import requests

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

context={'a':'b'}
class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
   
class CurrentImagesViewSet(viewsets.ModelViewSet):
    queryset = CurrentImages.objects.all()
    serializer_class = CurrentImagesSerializer





def get_images():
      img_arr=np.random.randint(low = 1, high = 4, size = 4)    
      img0=Image.objects.get(sn=1)
      img1=Image.objects.get(sn=2)
      img2=Image.objects.get(sn=3)
      img3=Image.objects.get(sn=4)
      global context
      context = {'img0': img0,'img1': img1,'img2': img2,'img3': img3}
def my_view(request):
      get_images() 
      return render(request,'index.html',context)


class getCurrentImage(APIView):
     
    permission_classes = ()
    authentication_classes = () 

    def get(self, request, pk, format=None):
        currentimage = CurrentImages.objects.get(pk=pk)
        serializer = CurrentImagesSerializer(currentimage)
        return Response(serializer.data)    
    
    def put(self, request, pk, format=None):
        currentimage = CurrentImages.objects.get(pk=pk)
        
        if currentimage is not None:
            serializer = CurrentImagesSerializer(currentimage, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data)
        else:  
            serializer = CurrentImagesSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)    



# class getImage(APIView):
#     def get_object(self, pk):
#         try:
#             return Image.objects.get(pk=pk)
#         except Image.DoepkotExist:
#             return None    
        

#     def get(self, request, pk, format=None):
#         Image = self.get_object(pk)
#         serializer = ImageSerializer(Image)
#         return Response(serializer.data)   


# @register.filter(name='update_filter')
# def update_variable(variable):
#    get_images()
#    if(variable=='img0'):
#          print('0')
#    elif(variable=='img1'):
#          print('1') 
#    elif(variable=='img2'):
#          print('2')    
#    elif(variable=='img3'):
#          print('3')             
#    return 'hello'
