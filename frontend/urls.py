"""frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include


from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register(r'images', views.ImageViewSet)
router.register(r'currentimages', views.CurrentImagesViewSet)
router.register(r'trafficlights', views.TrafficLightViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('home',views.my_view),
    # path('picture/<int:pk>',views.getImage.as_view()),
    path("current/<int:pk>",csrf_exempt(views.getCurrentImage.as_view())),
    path("tl/<int:sn>",csrf_exempt(views.getTrafficLight.as_view())),
    path('start',views.startedProgram),
    path('end',views.endProgram)
]

if settings.DEBUG == True: 
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
