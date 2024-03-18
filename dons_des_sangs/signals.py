# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Donateur
# from datetime import datetime, timedelta
# from django.utils import timezone

# @receiver(post_save, sender=Donateur)
# def update_pre_don(sender, instance, **kwargs):
#     # Si le donateur a fait un don, mettre à jour pre_don à True et les dates de donation
#     if instance.a_fait_don:
#         instance.pre_don = True
#         instance.date_don = datetime.now().date()
#         instance.date_don_active = datetime.now().date() + timedelta(days=1)
#         instance.save()
#     # Si le donateur n'a pas fait de don, vérifier si la date_don_active est passée
#     elif instance.date_don_active and instance.date_don_active <= timezone.now().date():
#         instance.pre_don = True
#         instance.save()
#     else:
#         instance.pre_don = False
#         instance.save()
