from django.contrib import admin
from .models import Voyage, Promotion, Commande, Favoris, User
# Register your models here.
admin.site.register(Voyage),
admin.site.register(Promotion),
admin.site.register(Commande),
admin.site.register(Favoris),
admin.site.register(User),