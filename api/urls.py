from django.urls import path,include
from rest_framework import routers
from api import views


router = routers.DefaultRouter()
#router.register (r'Sensores',views.ProgrammerViewSet)
router.register (r'Maquinas',views.MachineViewSet)
router.register (r'Users',views.UserViewSet)
router.register (r'Registro',views.RegistroViewSet, basename = 'registro')



urlpatterns = [
    path('',include(router.urls)),
] 