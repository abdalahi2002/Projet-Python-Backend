from django.contrib import admin
from .models import Wilaya,Type_Sang,Donateur,User,Administrateur


# Register your models here.
admin.site.register(Wilaya)
admin.site.register(Type_Sang)
admin.site.register(Donateur)
admin.site.register(User)
admin.site.register(Administrateur)