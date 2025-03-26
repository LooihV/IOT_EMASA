from django.urls import path,include
from rest_framework import routers
from api import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
#router.register (r'Sensores',views.ProgrammerViewSet)
router.register (r'Maquinas',views.MachineViewSet)
router.register (r'Users',views.UserViewSet)
router.register (r'Registro',views.RegistroViewSet, basename = 'registro')



urlpatterns = [
    path('',include(router.urls)),
] 