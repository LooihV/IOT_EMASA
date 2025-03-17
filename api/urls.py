from django.urls import path,include
from rest_framework import routers
from api import views


router = routers.DefaultRouter()
#router.register (r'Sensores',views.ProgrammerViewSet)
router.register (r'maquinas',views.MachineViewSet)
router.register (r'users',views.UserViewSet)


urlpatterns = [
    path('',include(router.urls))
   
] 
