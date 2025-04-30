from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomToken  # Asegúrate que este import apunta a tu modelo correcto

class CustomTokenAuthentication(BaseAuthentication):
    keyword = 'Token'
    model = CustomToken  # Esto es CRUCIAL - le decimos qué modelo usar

    def authenticate(self, request):
        auth = request.headers.get('Authorization', '').split()
        
        if not auth or auth[0].lower() != self.keyword.lower():
            return None
            
        if len(auth) == 1:
            raise AuthenticationFailed('Prefijo de token inválido')
        elif len(auth) > 2:
            raise AuthenticationFailed('Header de autorización inválido')
            
        try:
            token = self.model.objects.select_related('user').get(key=auth[1])
            if not token.user.is_active:
                raise AuthenticationFailed('Usuario inactivo')
            return (token.user, token)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Token inválido')