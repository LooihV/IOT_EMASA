from django.urls import path,include
from rest_framework import routers
from api import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import  PasswordResetRequestViewSet, ChangePasswordViewSet, CustomObtainAuthToken, ChirpstackGatewayViewSet, ChirpstackDeviceProfileViewSet, ChirpstackDeviceViewSet, ChirpstackDeviceActivationViewSet, ChirpstackApplicationViewSet, ChirpstackMQTTCertificateViewSet, ChirpstackGatewayDeleteView, ChirpstackApplicationDeleteView, ChirpstackDeviceDelGetView


router = routers.DefaultRouter()
router.register (r'Maquinas',views.MachineViewSet)
router.register (r'Users',views.UserViewSet)
router.register (r'Registro',views.RegistroViewSet, basename = 'registro')
router.register (r'Tenants',views.TenantViewSet)



urlpatterns = [
    path('',include(router.urls)),
    path("pass/reset/", PasswordResetRequestViewSet.as_view(), name="Password_reset"),
    path("pass/change/", ChangePasswordViewSet.as_view(), name="Password_change"),
    path('token/', CustomObtainAuthToken.as_view(), name='Custom-token'),
    
    # ------------------------- URLS DE LA COMUNICACIÒN DE CHIRPSTACK -------------------------
    
    path("chirpstack/gateways/",ChirpstackGatewayViewSet.as_view(), name="Gateways"),
    path("chirpstack/gateways/<str:gateway_id>/",ChirpstackGatewayDeleteView.as_view(), name="Gateway-Delete"),
    path("chirpstack/device-profiles/",ChirpstackDeviceProfileViewSet.as_view(),name="Device-Profile"),
    path("chirpstack/devices/",ChirpstackDeviceViewSet.as_view(), name="Devices"),
    path("chirpstack/devices/<str:dev_eui>/", ChirpstackDeviceDelGetView.as_view(), name="Devices2"),
    path("chirpstack/devices/<str:dev_eui>/activation/", ChirpstackDeviceActivationViewSet.as_view(), name="Device-Activation"),
    path("chirpstack/applications/",ChirpstackApplicationViewSet.as_view(), name=("Applications")),
    path("chirpstack/applications/<str:application_id>/",ChirpstackApplicationDeleteView.as_view(), name=("Applications")),
    path("chirpstack/applications/<str:application_id>/mqtt-certificate/", ChirpstackMQTTCertificateViewSet.as_view()),    
    
]