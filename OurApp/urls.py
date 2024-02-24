from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views import products


urlpatterns = [
    path('', views.home, name='home'),
     path('products',views.products, name='products'),
      path('sinscrire', views.sinscrire, name='sinscrire'),
     path('seconnecter', views.seconnecter, name='seconnecter'),
  path('detail_product/<int:id>', views.detail_product, name='detail_product'),
    path('categorie/<str:cat>', views.categorie, name='categorie'),
  path('sedeconnecter', views.sedeconnecter, name='sedeconnecter'),
  path('panier', views.panier, name='panier'),
  path('modifier_panier', views.modifier_panier, name='modifier_panier'),
   path('info_livraison', views.info_livraison, name='info_livraison'),
      path('profil', views.profil, name='profil'),
            path('modifier_mdp', views.modifier_mdp, name='modifier_mdp'),
        path('paiment', views.paiment, name='paiment'),
        path('commandes', views.commandes, name='commandes'),
        

  
]
   
