# views.py
import phonenumbers
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout, get_user_model
from urllib.parse import quote
from django.contrib.auth.models import User
from .models import User,Voyage,Commande,Favoris
import phonenumbers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from .models import Promotion
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.http import require_POST
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Promotion, Voyage
@user_passes_test(lambda u: u.statut != 'Client', login_url='/voyage/')
def Modifierpromo(request, id):
    promotion = get_object_or_404(Promotion, id=id)
    voyages = Voyage.objects.all()

    if request.method == 'POST':
        titre_voyage = request.POST.get('idVoyagePromotion', promotion.id_Voyage)
        
        # Récupérez l'instance de Voyage correspondant au titre
        voyage_instance = get_object_or_404(Voyage, titre=titre_voyage)

        promotion.titre = request.POST.get('titrePromotion', promotion.titre)
        promotion.id_Voyage = voyage_instance
        promotion.pourcentage = request.POST.get('pourcentagePromotion', promotion.pourcentage)

        # Gérer d'autres champs si nécessaire

        promotion.save()
        return redirect('dashProm')  # Rediriger vers la page souhaitée après la modification de la promotion

    return render(request, 'vacance/ModifierPromo.html', {'promotion': promotion, 'voyages': voyages})
@user_passes_test(lambda u: u.statut != 'Client', login_url='/voyage/')
def ModifierVoyage(request, id):
    voyage = get_object_or_404(Voyage, id=id)

    if request.method == 'POST':
        voyage.titre = request.POST.get('titre', voyage.titre)
        voyage.pays = request.POST.get('pays', voyage.pays)
        voyage.ville = request.POST.get('ville', voyage.ville)
        voyage.categorie = request.POST.get('categorie', voyage.categorie)
        voyage.date_debut = request.POST.get('dateDebut', voyage.date_debut)
        voyage.date_fin = request.POST.get('dateFin', voyage.date_fin)
        voyage.prix = request.POST.get('prix', voyage.prix)
        voyage.description = request.POST.get('description', voyage.description)

        # Gérer le champ d'image si nécessaire
        if 'image' in request.FILES:
            voyage.image_de_voyage = request.FILES['image']

        voyage.save()
        return redirect('dashVoy')

    return render(request, 'vacance/ModifierVoyage.html', {'voyage': voyage})
@user_passes_test(lambda u: u.statut != 'Client', login_url='/voyage/')
def modifier_statut_commande(request, commande_id):
    if request.method == 'POST':
        nouveau_statut = request.POST.get('nouveau_statut')
        commande = Commande.objects.get(pk=commande_id)
        commande.statut = nouveau_statut
        commande.save()
        return redirect('dashCom')
    else:
        # Gérer le cas où la requête n'est pas de type POST
        return redirect('dashCom')  
@user_passes_test(lambda u: u.statut != 'Client', login_url='/voyage/')
def dashCom(request):
    commande_trouvee = None
    dernieres_commandes = Commande.objects.all().order_by('-date_de_commande')[:]

    if 'q1' in request.GET:
        search_query = request.GET['q1']
        if search_query:
            commandes_trouvees = Commande.objects.filter(
                Q(id=search_query)
            )
            if commandes_trouvees.exists():
                commande_trouvee = commandes_trouvees[0]
            else:
                commande_trouvee = None

    context = {'commandes': dernieres_commandes, 'commande_trouvee': commande_trouvee}
    return render(request, 'vacance/dashcom.html', context)
def deconnexion(request):
    logout(request)
    return redirect('home') 
def modifier_statut_utilisateur(request, utilisateur_id):
    print(utilisateur_id)
    if request.method == 'POST':
        nouvel_statut = request.POST.get('nouveau_statut')
        print(f"Nouveau statut : {nouvel_statut}")
        if nouvel_statut == 'admin':
            # Modifier le statut de l'utilisateur directement dans le modèle
            utilisateur = get_object_or_404(User, pk=utilisateur_id)
            utilisateur.statut = 'Admin'
            utilisateur.save()
            print("Statut modifié avec succès !")
    return redirect('dashuti')
@user_passes_test(lambda u: u.statut != 'Client', login_url='/voyage/')
def dashProm(request):
    promotion_trouve = None
    derniers_promotions = Promotion.objects.all().order_by('-id')[:]

    if 'q1' in request.GET:
        titre_recherche = request.GET['q1']
        if titre_recherche:
            promotions_trouvees = Promotion.objects.filter(titre__icontains=titre_recherche)
            if promotions_trouvees.exists():
                promotion_trouve = promotions_trouvees[0]
            else:
                promotion_trouve = None
    promotion_id=0
    context = {'promotions': derniers_promotions, 'promotion_trouve': promotion_trouve,'promotion_id':promotion_id}
    voyages = Voyage.objects.all()
    context['voyages'] = voyages
    return render(request, 'vacance/dashProm.html', context)
def ajouter_promotion(request):
    if request.method == 'POST':
        titre_promotion = request.POST.get('titrePromotion', '')
        id_voyage_promotion = request.POST.get('idVoyagePromotion', '')
        pourcentage_promotion = request.POST.get('pourcentagePromotion', '')

        # Vérifier si l'ID du voyage est un entier valide
        try:
            id_voyage_promotion = int(id_voyage_promotion)
        except ValueError:
            return HttpResponse("L'ID du voyage doit être un entier.")

        # Récupérer l'instance du Voyage ou renvoyer une réponse 404 si elle n'existe pas
        voyage_instance = get_object_or_404(Voyage, id=id_voyage_promotion)

        # Créer un nouvel objet Promotion avec l'instance du Voyage
        nouvelle_promotion = Promotion(
            titre=titre_promotion,
            id_Voyage=voyage_instance,
            pourcentage=pourcentage_promotion
        )

        try:
            # Sauvegarder dans la base de données
            nouvelle_promotion.save()
            message = "Promotion ajoutée avec succès!"
            return redirect('dashProm')
        except Exception as e:
            message = f"Erreur lors de l'ajout de la promotion : {str(e)}"
            return HttpResponse(f"Erreur lors de l'ajout de la promotion : {str(e)}")

    return redirect('dashProm')

def supprimer_promotion(request, promotion_id):
    promotion = get_object_or_404(Promotion, id=promotion_id)
    promotion.delete()
    return redirect('dashProm')
def ajouter_voyage(request):
    if request.method == 'POST' or request.method == 'GET':
        titre = request.GET.get('titre', '') or request.POST.get('titre', '')
        pays = request.GET.get('pays', '') or request.POST.get('pays', '')
        ville = request.GET.get('ville', '') or request.POST.get('ville', '')
        categorie = request.GET.get('categorie', '') or request.POST.get('categorie', '')
        date_debut = request.GET.get('dateDebut', '') or request.POST.get('dateDebut', '')
        date_fin = request.GET.get('dateFin', '') or request.POST.get('dateFin', '')
        prix = request.GET.get('prix', '') or request.POST.get('prix', '')
        description = request.GET.get('description', '') or request.POST.get('description', '')
        image_de_voyage = request.GET.get('image', '') or request.FILES.get('image', '')

        # Convertir les champs appropriés si nécessaire (par exemple, date)
        # ...

        # Créer un nouvel objet Voyage
        nouveau_voyage = Voyage(
            titre=titre,
            pays=pays,
            ville=ville,
            categorie=categorie,
            date_debut=date_debut,
            date_fin=date_fin,
            prix=prix,
            description=description,
            image_de_voyage=image_de_voyage
        )

        try:
            # Sauvegarder dans la base de données
            nouveau_voyage.save()
            message = "Voyage ajouté avec succès!"
            return redirect('dashVoy')
        except Exception as e:
            message = f"Erreur lors de l'ajout du voyage : {str(e)}"
            return HttpResponse(f"Erreur lors de l'ajout du voyage : {str(e)}")

    return render(request, 'vacance/dashVoy.html')
def supprimer_utilisateur(request, utilisateur_id):
    utilisateur = get_object_or_404(User, id=utilisateur_id)
    utilisateur.delete()  # Utilisation de la méthode delete directement
    return redirect('dashuti')
def supprimer_voyage(request, voyage_id):
    voyage = get_object_or_404(Voyage, id=voyage_id)
    voyage.delete()
    return redirect('dashVoy')
from django.contrib.auth.decorators import user_passes_test
@user_passes_test(lambda u: u.statut != 'Client', login_url='/voyage/')
def admine(request):
    # Votre logique de vue ici
    user_count = User.objects.count()
    voy_count = Voyage.objects.count()
    comd_count = Commande.objects.count()
    cmd=Commande.objects.all()
    revenu=0
    for i in cmd :
        revenu+=i.prix_total
    revenu=int(revenu)
    current_user_first_name = request.user.username
    dernieres_commandes = Commande.objects.all().order_by('-date_de_commande')[:]
    #current_user_last_name = request.user.last_name
    context = { 'user_count':user_count,
                'voy_count': voy_count,
                'current_user_first_name': current_user_first_name,
                'comd_count': comd_count,
                'dernieres_commandes': dernieres_commandes,
                'revenu':revenu,}
                #'current_user_last_name': current_user_last_name,}
    return render(request, 'vacance/admine.html',context)
@user_passes_test(lambda u: u.statut != 'Client', login_url='/voyage/')
def dashuti(request):
    utilisateur_trouve = None
    derniers_utilisateurs = User.objects.filter(statut='Client').order_by('-date_joined')[:]

    if 'q1' in request.GET:
        search_query = request.GET['q1']
        if search_query:
            utilisateurs_trouves = User.objects.filter(
                Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query),
                statut='Client'
            )
            if utilisateurs_trouves.exists():
                utilisateur_trouve = utilisateurs_trouves[0]
            else:
                utilisateur_trouve = None

    context = {'utilisateurs': derniers_utilisateurs, 'utilisateur_trouve': utilisateur_trouve}
    return render(request, 'vacance/dashuti.html', context)
@user_passes_test(lambda u: u.statut != 'Client', login_url='/voyage/')
def dashVoy(request):
    voyage_trouve = None
    derniers_voyages = Voyage.objects.all().order_by('-id')[:]

    if 'q1' in request.GET:
        titre_recherche = request.GET['q1']
        if titre_recherche:
            voyages_trouves = Voyage.objects.filter(titre__icontains=titre_recherche)
            if voyages_trouves.exists():
                voyage_trouve = voyages_trouves[0]
            else:
                voyage_trouve = None

    context = {'voyages': derniers_voyages, 'voyage_trouve': voyage_trouve}
    return render(request, 'vacance/dashVoy.html', context)

def Sec(request):
    # Votre logique de vue ici
    return render(request, 'vacance/seCon.html')


def GenrerListe():
    days = range(1, 32)
    months = [
    "Janvier", "Février", "Mars",
    "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre",
    "Octobre", "Novembre", "Décembre"
    ] 
    years = range(2024, 1980, -1)

    context = {
        'days': days,
        'months': months,
        'years': years,
    } 
    return context
def acceuil(request):
    context=GenrerListe()
    return render(request, 'vacance/acceuil.html', context)


#@login_required(login_url='Sec')
def adm(request):
	context={'utilisateurs':User.objects.all()}
	return render(request,'vacance/adm.html', context)
def notexist(request):
    return render(request,'vacance/notexist.html')
@csrf_protect
def inscription(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Vérifier si l'email existe déjà
        if User.objects.filter(email=email).exists():
            print("Email already exists. Choose a different email.")
            context = GenrerListe()
            context['erreur_email'] = 'Email already exists. Choose a different email.'
            # Ajouter d'autres champs nécessaires dans le contexte
            return render(request, 'vacance/acceuil.html', context)

        # Vérifier si la date est valide
        jour = request.POST.get('day')
        mois = request.POST.get('month')
        annee = request.POST.get('year')
        if not (jour and mois and annee):
            print("Invalid date. Please provide a valid date.")
            context = GenrerListe()
            context['erreur_date'] = 'Invalid date. Please provide a valid date.'
            # Ajouter d'autres champs nécessaires dans le contexte
            return render(request, 'vacance/acceuil.html', context)

        # Vérifier si le mot de passe correspond à la confirmation du mot de passe
        mot_de_passe = request.POST.get('psw')
        mot_de_passe_confirmation = request.POST.get('psw_repeat')
        if mot_de_passe != mot_de_passe_confirmation:
            print("Passwords do not match. Please enter matching passwords.")
            context = GenrerListe()
            context['erreur_password'] = 'Passwords do not match. Please enter matching passwords.'
            # Ajouter d'autres champs nécessaires dans le contexte
            return render(request, 'vacance/acceuil.html', context)

        # Vérifier si une image a été fournie
        image = request.FILES.get('image')
        if not image:
            print("Image is required. Please upload an image.")
            context = GenrerListe()
            context['erreur_image'] = 'Image is required. Please upload an image.'
            # Ajouter d'autres champs nécessaires dans le contexte
            return render(request, 'vacance/acceuil.html', context)

        # Vérifier si le numéro de téléphone est valide
        phone = "+212" + request.POST.get('phone')
        try:
            parsed_phone = phonenumbers.parse(phone)
            if not phonenumbers.is_valid_number(parsed_phone):
                print("Invalid phone number.")
                context = GenrerListe()
                context['erreur_phone'] = 'Invalid phone number.'
                # Ajouter d'autres champs nécessaires dans le contexte
                return render(request, 'vacance/acceuil.html', context)
        except phonenumbers.NumberFormatException:
            print("Invalid phone number format.")
            context = GenrerListe()
            context['erreur_phone'] = 'Invalid phone number format.'
            # Ajouter d'autres champs nécessaires dans le contexte
            return render(request, 'vacance/acceuil.html', context)

        # Enregistrer l'utilisateur avec id égal au maximum de id + 1
        try:
            #max_id = User.objects.aggregate(Max('id'))['id__max'] or 0
            utilisateur = User(
                username=email,
                password=make_password(mot_de_passe),
                first_name=request.POST.get('prenom'),
                last_name=request.POST.get('nom'),
                date_Nai=f"{annee}-{mois}-{jour}",
                numero_de_telephone=phone,
                image_de_profil=image,
                statut="Client"
            )
            utilisateur.save()
            #return HttpResponseRedirect(reverse('voyage'))
            user = authenticate(request, username=email, password=mot_de_passe)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('voyage'),user)

        except IntegrityError as e:
            print(f"IntegrityError: {e}")

    return render(request, 'vacance/acceuil.html')
@csrf_protect
def check_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"{email}   {password}")

        # Vérifier si les champs ne sont pas vides
        if not email or not password:
            print("Champs d'email ou de mot de passe vides.")
            return render(request, 'vacance/seCon.html', {'error_message': 'Veuillez remplir tous les champs.'})

        # Utiliser authenticate pour vérifier les informations d'identification
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # L'utilisateur est authentifié
            login(request, user)
            #user1=User.objects.create(username=email)
            if user.statut == "Admin":
                # Rediriger vers la page adm pour les administrateurs
                return HttpResponseRedirect(reverse('admine'))
            else:
                # Rediriger vers la page home pour les autres utilisateurs
                return HttpResponseRedirect(reverse('voyage'),user)
        else:
            # Les informations d'identification sont incorrectes
            print("Mot de passe incorrect ou utilisateur inexistant.")
            return render(request, 'vacance/seCon.html', {'email': email, 'error_message': 'Mot de passe incorrect ou utilisateur inexistant. Veuillez réessayer.'})

    return render(request, 'vacance/seCon.html')


####clients viewer
def details(request, voyage_id):
    promos=Promotion.objects.all()
    categories=Voyage.categories
    cats = [nom[:] for code, nom in categories]
    voyage = get_object_or_404(Voyage, id=voyage_id)
    context = {'voyage': voyage,'promos':promos,'cats':cats}
    return render(request, 'vacance/client/details.html', context)
def detailsp(request, voyage_id):
    promos=Promotion.objects.all()
    categories=Voyage.categories
    cats = [nom[:] for code, nom in categories]
    voyage = get_object_or_404(Voyage, id=voyage_id)
    prm = get_object_or_404(Promotion, id_Voyage=voyage)
    voyage.prix=(voyage.prix)-((voyage.prix)*(prm.pourcentage/100))
    context = {'voyage': voyage,'promos':promos,'cats':cats}
    return render(request, 'vacance/client/details.html', context)

def categories(request, categorie_t):
    cate=categorie_t[0]
    promos = Promotion.objects.all()
    categories = Voyage.categories
    cats = [nom[1] for  nom in categories]
    voyages = Voyage.objects.filter(categorie=cate)
    context = {'voyages': voyages, 'promos': promos, 'cats': cats}
    return render(request, 'vacance/client/categories.html', context)

from datetime import datetime

def home(request):
    dernieres_voyages = Voyage.objects.all().order_by('prix')
    voyage_trouve = None
    promos = Promotion.objects.all()
    categories=Voyage.categories
    
    cats = [nom[1] for  nom in categories]

    titre_recherche = request.GET.get('q1', '')
    prix_recherche = request.GET.get('q2', '')
    date_debut_recherche = request.GET.get('q3', '')
    date_fin_recherche = request.GET.get('q4', '')

    voyages_trouves = Voyage.objects.all()

    if titre_recherche:
        voyages_trouves = voyages_trouves.filter(titre__icontains=titre_recherche)

    if prix_recherche:
        try:
            prix_recherche = float(prix_recherche)
            voyages_trouves = voyages_trouves.filter(prix__lte=prix_recherche)
        except ValueError:
            pass

    if date_debut_recherche:
        try:
            date_debut_recherche = datetime.strptime(date_debut_recherche, '%Y-%m-%d')
            voyages_trouves = voyages_trouves.filter(date_debut__gte=date_debut_recherche)
        except ValueError:
            pass

    if date_fin_recherche:
        try:
            date_fin_recherche = datetime.strptime(date_fin_recherche, '%Y-%m-%d')
            voyages_trouves = voyages_trouves.filter(date_fin__lte=date_fin_recherche)
        except ValueError:
            pass

    if voyages_trouves.exists():
        voyage_trouve = voyages_trouves
    else:
        voyage_trouve = None

    context = {
        'voyages': dernieres_voyages,
        'voyage_trouve': voyage_trouve,
        'promos': promos,
        'cats': cats,
    }

    return render(request, 'vacance/client/home.html', context)

######################## user
def detail(request, voyage_id):
    promos=Promotion.objects.all()
    categories=Voyage.categories
    cats = [nom[:] for code, nom in categories]
    voyage = get_object_or_404(Voyage, id=voyage_id)
    context = {'voyage': voyage,'promos':promos,'cats':cats}
    return render(request, 'vacance/user/details.html', context)

def detailp(request, voyage_id):
    promos=Promotion.objects.all()
    categories=Voyage.categories
    cats = [nom[:] for code, nom in categories]
    voyage = get_object_or_404(Voyage, id=voyage_id)
    prm = get_object_or_404(Promotion, id_Voyage=voyage)
    
    voyage.prix=(voyage.prix)-((voyage.prix)*(prm.pourcentage/100))
    context = {'voyage': voyage,'promos':promos,'cats':cats}
    return render(request, 'vacance/user/details.html', context)

#ajouter au favoris
def favo(request,voy_id):
    
    voyage = get_object_or_404(Voyage, id=voy_id)
    use = get_object_or_404(User, id=request.user.id)
    #### retirer le favoris
    
    ####

    fa=Favoris(
    id_User = use,
    id_Voyage = voyage
    )
    fa.save()

    promos=Promotion.objects.all()
    categories=Voyage.categories
    cats = [nom[:] for code, nom in categories]
    voyage = get_object_or_404(Voyage, id=voy_id)
    context = {'voyage': voyage,'promos':promos,'cats':cats}
    return render(request, 'vacance/user/details.html', context)
#page des favoris

def favoris(request):
    promos = Promotion.objects.all()
    categories = Voyage.categories
    favoriss = Favoris.objects.filter(id_User=request.user.id)
    voyages=[]
    for f in favoriss:
        voyage = get_object_or_404(Voyage, id=f.id_Voyage.id)
        voyages.append(voyage)
        print('tettt')
    cats = [nom[1] for  nom in categories]
    context = {'voyages': voyages, 'promos': promos, 'cats': cats}
    return render(request, 'vacance/user/favoris.html', context)
    
    
def categ(request, categorie_t):
    cate=categorie_t[0]
    promos = Promotion.objects.all()
    categories = Voyage.categories
    cats = [nom[1] for  nom in categories]
    voyages = Voyage.objects.filter(categorie=cate)
    context = {'voyages': voyages, 'promos': promos, 'cats': cats}
    return render(request, 'vacance/user/categories.html', context)
def voyage(request):
    dernieres_voyages = Voyage.objects.all().order_by('prix')
    voyage_trouve = None
    promos = Promotion.objects.all()
    categories=Voyage.categories
    
    cats = [nom[1] for  nom in categories]

    titre_recherche = request.GET.get('q1', '')
    prix_recherche = request.GET.get('q2', '')
    date_debut_recherche = request.GET.get('q3', '')
    date_fin_recherche = request.GET.get('q4', '')

    voyages_trouves = Voyage.objects.all()

    if titre_recherche:
        voyages_trouves = voyages_trouves.filter(titre__icontains=titre_recherche)

    if prix_recherche:
        try:
            prix_recherche = float(prix_recherche)
            voyages_trouves = voyages_trouves.filter(prix__lte=prix_recherche)
        except ValueError:
            pass

    if date_debut_recherche:
        try:
            date_debut_recherche = datetime.strptime(date_debut_recherche, '%Y-%m-%d')
            voyages_trouves = voyages_trouves.filter(date_debut__gte=date_debut_recherche)
        except ValueError:
            pass

    if date_fin_recherche:
        try:
            date_fin_recherche = datetime.strptime(date_fin_recherche, '%Y-%m-%d')
            voyages_trouves = voyages_trouves.filter(date_fin__lte=date_fin_recherche)
        except ValueError:
            pass

    if voyages_trouves.exists():
        voyage_trouve = voyages_trouves
    else:
        voyage_trouve = None

    context = {
        'voyages': dernieres_voyages,
        'voyage_trouve': voyage_trouve,
        'promos': promos,
        'cats': cats,
    }

    return render(request, 'vacance/user/voyage.html', context)
#page des commande
def reservations(request):
    promos = Promotion.objects.all()
    categories = Voyage.categories

    commands = Commande.objects.filter(id_User=request.user.id).order_by('-id')[:]
    voyages=[]
    for f in commands:
        voyage = get_object_or_404(Voyage, id=f.id_Voyage.id)
        voyages.append(voyage)


    cats = [nom[1] for  nom in categories]
    context = {'voyages': voyages, 'promos': promos, 'cats': cats ,'commands':commands}
    return render(request, 'vacance/user/reservations.html', context)
    ###reserver
from datetime import date

def reserver(request):

    if request.method == 'POST' :
        use = get_object_or_404(User, id=request.user.id)
        v = request.POST.get('idv', '')
        voy = get_object_or_404(Voyage, id=v)
        dat = datetime.now()

        rec = request.FILES.get('imag','')

        if rec:
            dat = datetime.now()
            cm = Commande(
                id_User=use,
                id_Voyage=voy,
                statut='W',
                nbr_de_personnes=1,
                date_de_commande=dat,
                recu=rec,
                prix_total=voy.prix
            )
            cm.save()
                    
            promos=Promotion.objects.all()
            categories=Voyage.categories
            commands = Commande.objects.filter(id_User=request.user.id).order_by('-id')[:]
            voyages=[]
            for f in commands:
                voyage = get_object_or_404(Voyage, id=f.id_Voyage.id)
                voyages.append(voyage)


            cats = [nom[1] for  nom in categories]
            context = {'voyages': voyages, 'promos': promos, 'cats': cats ,'commands':commands}
            return render(request, 'vacance/user/reservations.html', context)
        else:
            return redirect('Sec')
#####profile user
def profile(request):
    user = request.user
    return render(request, 'vacance/user/profile.html', {'user': user})
def modifier_profile(request):
    user = request.user

    if request.method == 'POST':
        user.numero_de_telephone = request.POST.get('numero_de_telephone', user.numero_de_telephone)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.date_Nai = request.POST.get('date_Nai', user.date_Nai)

        # Handle profile image upload
        if 'image_de_profil' in request.FILES:
            user.image_de_profil = request.FILES['image_de_profil']

        user.save()
        return redirect('profile')  # Change 'dashboard' to your actual dashboard URL name

    return render(request, 'vacance/user/profile.html', {'user': user})
