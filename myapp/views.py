from django.shortcuts import render

# Create your views here.
from myapp.models import *
from .serializers import *
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import render,redirect
from rest_framework.views import APIView
import numpy as np
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from sys import path as pt
from sys import exit
from os import getcwd
pt.append(getcwd()+'/Traffic Program')

context={'a':'b'}
class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
   
class CurrentImagesViewSet(viewsets.ModelViewSet):
    queryset = CurrentImages.objects.all()
    serializer_class = CurrentImagesSerializer

class TrafficLightViewSet(viewsets.ModelViewSet):
    queryset = TrafficLight.objects.all()
    serializer_class = TrafficLightSerializer

def startedProgram(request):
    
    
        currentimage=CurrentImages.objects.get(pk=1)
        if(currentimage.programStarted):
            
            import main
            return '1'
    
        
        return redirect('http://127.0.0.1:8000/home')

def endProgram(request):
    
     currentimage=CurrentImages.objects.get(pk=1)
     requests.put('http://127.0.0.1:8000/current/1',data={'programStarted': False})
     
     return redirect('http://127.0.0.1:8000/home')

def get_images():
          
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

class getTrafficLight(APIView):
     
    permission_classes = ()
    authentication_classes = () 

    def get(self, request, sn, format=None):
        trafficlight = TrafficLight.objects.get(sn=sn)
        serializer = TrafficLightSerializer(trafficlight)
        return Response(serializer.data)    
    
    def put(self, request, sn, format=None):
        trafficlight = TrafficLight.objects.get(sn=sn)
        
        if trafficlight is not None:
            serializer = TrafficLightSerializer(trafficlight, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data)
        else:  
            serializer = TrafficLightSerializer(data=request.data)
            
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
