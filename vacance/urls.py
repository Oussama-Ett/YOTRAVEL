from django.urls import path
from . import views
urlpatterns = [
    path('acceuil/', views.acceuil, name='acceuil'),
    path('adm/', views.adm, name='adm'),
    path('inscription/', views.inscription, name='inscription'),
    path('Sec/', views.Sec, name='Sec'),
    path('login/', views.check_user, name='login'),
    path('notexist/', views.notexist, name='notexist'),
    path('admine/', views.admine, name='admine'),
    path('dashuti/', views.dashuti, name='dashuti'),
    path('dashCom/', views.dashCom, name='dashCom'),
    path('supprimer_utilisateur/<int:utilisateur_id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('dashVoy/', views.dashVoy, name='dashVoy'),
    path('supprimer_voyage/<int:voyage_id>/', views.supprimer_voyage, name='supprimer_voyage'),
    path('ajouter/', views.ajouter_voyage, name='ajouter_voyage'),
    path('dashProm/', views.dashProm, name='dashProm'),
    path('ajouter_promotion/', views.ajouter_promotion, name='ajouter_promotion'),
    path('supprimer_promotion/<int:promotion_id>/', views.supprimer_promotion, name='supprimer_promotion'),
    path('modifier_statut_utilisateur/<int:utilisateur_id>/', views.modifier_statut_utilisateur, name='modifier_statut_utilisateur'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('modifier_statut_commande/<int:commande_id>/', views.modifier_statut_commande, name='modifier_statut_commande'),
    # Utilisez le nom de la vue pour la modification de la promotion
    path('ModifierVoyage/<int:id>/', views.ModifierVoyage, name='ModifierVoyage'),
    path('Modifierpromo/<int:id>/', views.Modifierpromo, name='Modifierpromo'),
    #visitor paths
    path('', views.home, name='home'),
    path('details/<int:voyage_id>/', views.details, name='details'),
    path('detailsp/<int:voyage_id>/', views.detailsp, name='detailsp'),
    path('categories/<str:categorie_t>/', views.categories, name='categories'),
    #user paths
    path('voyage/', views.voyage, name='voyage'),
    path('reservations/', views.reservations, name='reservations'),
    path('detail/<int:voyage_id>/', views.detail, name='detail'),
    path('detailp/<int:voyage_id>/', views.detailp, name='detailp'),
    path('categ/<str:categorie_t>/', views.categ, name='categ'),
    path('favo/<int:voy_id>/', views.favo, name='favo'),
    path('favoris/', views.favoris, name='favoris'),
    path('reserver/', views.reserver, name='reserver'),
    path('profile/', views.profile, name='profile'),
    path('modifier_profile/', views.modifier_profile, name='modifier_profile'),


]
