from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Categorie)
admin.site.register(Produit)
admin.site.register(Image)
admin.site.register(Commande)
admin.site.register(Produitscommande)
admin.site.register(InfoLivrason)

