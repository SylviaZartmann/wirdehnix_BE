from django.apps import AppConfig


class FilmographyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filmography'
    
    def ready(self):
        import filmography.signals
