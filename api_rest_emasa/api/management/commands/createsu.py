from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from api.models import CentralSystem

class Command(BaseCommand):
    help = 'Configuración inicial automática: superusuario, central y sitio'

    def handle(self, *args, **options):
        # Configuración
        CONFIG = {
            'superuser': {
                'username': 'EMASADOCK',
                'password': 'emasa123',
                'email': 'admin@emasa.com'
            },
            'central': {
                'name': 'EMASA'
            },
            'site': {
                'id': 1,
                'domain': 'localhost:8000',
                'name': 'localhost'
            }
        }

        # 1. Crear/actualizar Site
        site, created = Site.objects.update_or_create(
            id=CONFIG['site']['id'],
            defaults={
                'domain': CONFIG['site']['domain'],
                'name': CONFIG['site']['name']
            }
        )
        status = 'Creado' if created else 'Actualizado'
        self.stdout.write(self.style.SUCCESS(
            f'Site {status}: {site.domain} (ID: {site.id})'
        ))

        # 2. Crear superusuario
        User = get_user_model()
        if not User.objects.filter(username=CONFIG['superuser']['username']).exists():
            User.objects.create_superuser(**CONFIG['superuser'])
            self.stdout.write(self.style.SUCCESS(
                f'Superusuario {CONFIG["superuser"]["username"]} creado'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                'El superusuario ya existe'
            ))

        # 3. Crear central
        if not CentralSystem.objects.exists():
            CentralSystem.objects.create(name=CONFIG['central']['name'])
            self.stdout.write(self.style.SUCCESS(
                f'Central {CONFIG["central"]["name"]} creada'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                'La central ya existe'
            ))