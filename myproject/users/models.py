from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

@receiver(pre_save, sender=User)
def check_unique_email(sender, instance, **kwargs):
    if User.objects.filter(email=instance.email).exclude(username=instance.username).exists():
        raise ValidationError("Istnieje zarejestrowany użytkownik z takim adresem email.")