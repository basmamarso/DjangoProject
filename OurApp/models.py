from django.db import models
from django.contrib.auth.models import User


image = models.ImageField(upload_to='uploads/product/')
# Create your models here.
class Categorie(models.Model):
	nom = models.CharField(max_length=50)

	def __str__(self):
		return self.nom

		

class Produit(models.Model):
	libelle = models.CharField(max_length=100)
	prix = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	poids = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	quantite_stock = models.IntegerField(default=0)
	categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, default=1)
	description = models.CharField(max_length=250, default='', blank=True, null=True)
	solde = models.BooleanField(default=False)
	prix_sold = models.DecimalField(default=0, decimal_places=2, max_digits=6)

	def __str__(self):
		return self.libelle

class Image(models.Model):
	produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
	image = models.ImageField(null=True, blank=True)

	
	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
	

class Commande(models.Model):
	etatsLivraison=[  
		('Expédiée', 'Expédiée'),
		('En Transit', 'En Transit'),
        ('Arrivée Locale', 'Arrivée Locale'),
        ('En Livraison', 'En Livraison'),
        ('Livrée', 'Livrée'),]
	client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	date_commander = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	etatLivraison=models.CharField(max_length=200,default='Expédiée',choices=etatsLivraison)#En Transit Arrivée Locale En Livraison Livré

	def __str__(self):
		return str(self.id)
	@property
	def get_total_panier(self):
		orderitems = self.produitscommande_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_nb_produits(self):
		orderitems = self.produitscommande_set.all()
		total = sum([item.quantite for item in orderitems])
		return total 

		

class Produitscommande(models.Model):
	produits = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True)
	commande = models.ForeignKey(Commande, on_delete=models.SET_NULL, null=True)
	quantite = models.IntegerField(default=0, null=True, blank=True)
	date_ajouter = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		if self.produits.solde:
			total = self.produits.prix_sold * self.quantite
		else:
			total = self.produits.prix * self.quantite
		return total


class InfoLivrason(models.Model):
	client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Commande, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	ville = models.CharField(max_length=200, null=False)
	pays = models.CharField(max_length=200, null=False)
	codePostal = models.CharField(max_length=200, null=False)
	numTele = models.CharField(max_length=200, null=False)

	def __str__(self):
		return self.address