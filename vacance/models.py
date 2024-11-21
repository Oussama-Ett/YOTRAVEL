from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, User

class User(AbstractUser):
    #nom = models.CharField(max_length=100)
    #prenom = models.CharField(max_length=100)
    #email = models.EmailField(unique=True)
    numero_de_telephone = models.CharField(max_length=15, null=True, blank=True)
    pays = models.CharField(max_length=100, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    #mot_de_passe = models.CharField(max_length=100)
    image_de_profil = models.ImageField(upload_to='images/profiles/', null=True, blank=True)
    statut = models.CharField(max_length=50)
    date_Nai = models.DateField(null=True, blank=True) 
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class Voyage(models.Model):
	categories=[
		("H","HAJJ"),
		("O","OMRA"),
		("A","ASIE"),
		("T","TURQUIE"),
		("M","MAROC"),
	]
	categorie = models.CharField(max_length=1, choices=categories)
	titre = models.CharField(max_length=30)
	pays = models.CharField(max_length=30)
	ville = models.CharField(max_length=30)
	date_debut=models.DateField(null=True, blank=True)
	date_fin=models.DateField(null=True, blank=True)
	prix=models.FloatField()
	description=models.TextField()
	image_de_voyage = models.ImageField(upload_to='static/images/voyages/', null=True, blank=True)
	def __str__(self):
		return self.titre
class Promotion(models.Model):
	titre = models.CharField(max_length=30)
	id_Voyage = models.ForeignKey(Voyage,on_delete=models.CASCADE)
	pourcentage=models.FloatField()	
	def __str__(self):
		return self.titre
class Favoris(models.Model):
	id_Voyage = models.ForeignKey(Voyage,on_delete=models.CASCADE)
	id_User = models.ForeignKey(User,on_delete=models.CASCADE)
	#def __str__(self):
		#return self.title
class Commande(models.Model):
	id_Voyage = models.ForeignKey(Voyage,on_delete=models.CASCADE)
	id_User = models.ForeignKey(User,on_delete=models.CASCADE)
	status=[
		("W","WAITING"),
		("A","APPROVED"),
		("C","CANCELED"),
		("R","REJECTED"),
    ]
	nbr_de_personnes=models.IntegerField()
	prix_total=models.FloatField()
	statut = models.CharField(max_length=1, choices=status)
	date_de_commande=models.DateField(null=True, blank=True)
	recu = models.ImageField(upload_to='static/images/recus/', null=True, blank=True)

	#def __str__(self):
		#return self.title