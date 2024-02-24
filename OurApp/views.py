from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Produit,Categorie,Commande,Produitscommande,InfoLivrason
from django.http import Http404
from .forms import SinscrireForm,InfoLivrasonForm,ProfilForm,Modifier_mdpForm
import json
from django.http import JsonResponse
from datetime import date


	
def home(request):
	if request.user.is_authenticated:
		client = request.user
		command, created = Commande.objects.get_or_create(client=client, complete=False)
		return render(request,"home.html",{"commande":command})
	else:
		return render(request,"home.html")

    # template = loader.get_template('home.html')
    # return HttpResponse(template.render())


def products(request):
	produits = Produit.objects.all()
	if request.user.is_authenticated:
		client = request.user
		command, created = Commande.objects.get_or_create(client=client, complete=False)
		return render(request, 'products.html', {'produits':produits,"commande":command})
	else:
		return render(request, 'products.html', {'produits':produits})

def sinscrire(request):

    return render(request,"sinscrire.html",{})


def detail_product(request,id):
	produit = Produit.objects.get(id=id)
	if request.user.is_authenticated:
		client = request.user
		command, created = Commande.objects.get_or_create(client=client, complete=False)
		return render(request,"detail_product.html" ,{'produit':produit,"commande":command})
	else:
		return render(request,"detail_product.html" ,{'produit':produit})



def seconnecter(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("Vous êtes connecté !"))
			return redirect('home')
		else:
			messages.error(request, ("Une erreur s'est produite, veuillez réessayer..."))
			return redirect('seconnecter')

	else:
		return render(request, 'seconnecter.html', {})

def sedeconnecter(request):
	logout(request)
	messages.success(request, ("Vous avez été déconnecté... Merci..."))
	return redirect('home')

def categorie(request,cat):
	category_instance = get_object_or_404(Categorie, nom=cat)
	produits = Produit.objects.filter(categorie=category_instance)
	if request.user.is_authenticated:
		client = request.user
		command, created = Commande.objects.get_or_create(client=client, complete=False)
		return render(request, 'categorie.html', {'produits':produits,'categorie':cat,"commande":command} )
	else:
		return render(request, 'categorie.html', {'produits':produits,'categorie':cat} )



def sinscrire(request):
	form = SinscrireForm()
	if request.method == "POST":
		form = SinscrireForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("You Have Registered Successfully!! Welcome!"))
			return redirect('home')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('sinscrire')
	else:
		return render(request, 'sinscrire.html', {'form':form})


def panier(request):
	if request.user.is_authenticated:
		client = request.user
		command, created = Commande.objects.get_or_create(client=client, complete=False)
		produits_c= command.produitscommande_set.all()
		return render(request,"panier.html",{"produits_c":produits_c,"commande":command})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')





def modifier_panier(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	q = data['quantite']
	print('Action:', action)
	print('Product:', productId)

	client = request.user
	produit = Produit.objects.get(id=productId)
	command, created = Commande.objects.get_or_create(client=client, complete=False)

	produits_c, created = Produitscommande.objects.get_or_create(commande=command, produits=produit)

	if action == 'add':
		produits_c.quantite = (produits_c.quantite + int(q))
		produits_c.save()
	elif action == 'remove':
		produits_c.delete()
	elif action == 'add-one':
		produits_c.quantite = (produits_c.quantite + 1)
		produits_c.save()
	elif action == 'remove-one':
		produits_c.quantite = (produits_c.quantite - 1)
		produits_c.save()
	if produits_c.quantite <= 0:
		produits_c.delete()
	
	return JsonResponse('Item was added', safe=False)



def info_livraison(request):
	if request.user.is_authenticated:
		client = request.user
		command, created = Commande.objects.get_or_create(client=client, complete=False)

		info_livrason_instances = InfoLivrason.objects.filter(client=client, order=command)
		if info_livrason_instances.exists():
			info_livrason = info_livrason_instances.first()
		else:
			info_livrason = InfoLivrason()

		if request.method == "POST":
			form = InfoLivrasonForm(request.POST, instance=info_livrason)  # Pass the instance for updating
			if form.is_valid():
				form.save()
				# messages.success(request, "Delivery information updated successfully!")
				return redirect('paiment')
			else:
				messages.error(request, "Error updating delivery information. Please check the form.")
				return redirect('info_livraison')
		else:
			form = InfoLivrasonForm(instance=info_livrason)

		return render(request, "info_livraison.html", {"form": form, "commande": command})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')



	
def profil(request):
	if request.user.is_authenticated:
		client = request.user
		command, created = Commande.objects.get_or_create(client=client, complete=False)
		form = ProfilForm(request.POST or None, instance=request.user)

		if form.is_valid():
			form.save()
			login(request, request.user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('home')
		return render(request, "profil.html", {'form':form,"commande":command})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')

def modifier_mdp(request):
	if request.user.is_authenticated:
		client = request.user
		command, created = Commande.objects.get_or_create(client=client, complete=False)
		
     
		current_user = request.user
		if request.method  == 'POST':
			form = Modifier_mdpForm(current_user, request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('profil')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('modifier_mdp')
		else:
			form = Modifier_mdpForm(current_user)
			return render(request, "modifier_mdp.html", {'form':form,"commande":command})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
# views.py




def paiment(request):
    if request.user.is_authenticated:
        client = request.user
        command, created = Commande.objects.get_or_create(client=client, complete=False)

        if request.method == 'POST':
            data = json.loads(request.body)
            command_id = data['command_id']
            total = data['total']
            command = Commande.objects.get(id=command_id)
            print(command_id, total)
            if total != command.get_total_panier:
                command.complete = True
                command.date_commander= date.today() 
                command.save()
                return JsonResponse({'message': 'Payment submitted.'})
            else:
                return JsonResponse({'message': 'Invalid total value.'}, status=500)
        else:
            return render(request, "paiment.html", {"commande": command})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')

def commandes(request):
	if request.user.is_authenticated:
		client = request.user
		commandes= Commande.objects.filter(client=client, complete=True)
		command, created = Commande.objects.get_or_create(client=client, complete=False)
		return render(request,"commande.html",{"commandes":commandes,"commande":command})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
  
        
	




