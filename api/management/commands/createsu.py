from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import CentralSystem

class Command(BaseCommand):
    help = 'Crea superusuario y central automáticamente'

    def handle(self, *args, **options):
        # Configuración
        SUPERUSER = {
            'username': 'EMASADOCK',
            'password': 'emasa123',
            'email': 'admin@emasa.com'
        }
        CENTRAL_NAME = 'EMASA'

        # Crear superusuario
        User = get_user_model()
        if not User.objects.filter(username=SUPERUSER['username']).exists():
            User.objects.create_superuser(**SUPERUSER)
            self.stdout.write(self.style.SUCCESS(f'Superusuario {SUPERUSER["username"]} creado'))
        
        # Crear central
        if not CentralSystem.objects.exists():
            CentralSystem.objects.create(name=CENTRAL_NAME)
            self.stdout.write(self.style.SUCCESS(f'Central {CENTRAL_NAME} creada'))