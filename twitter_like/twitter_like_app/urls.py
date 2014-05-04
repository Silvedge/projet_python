from django.conf.urls import patterns, include, url
from django.contrib import admin

from twitter_like_app import views

urlpatterns = patterns('',
	url(r'^$', views.Index, name='Index'),
	url(r'^inscription$', views.Inscription, name='Inscription'),
	url(r'^login$', views.Login, name='Login'),
	url(r'^logout$', views.Logout, name='Logout'),
	url(r'^ok$', views.ConnexionOK, name='ConnexionOK'),
	url(r'^(?P<user_name>\w+)$', views.Profil, name='Profil'),
	url(r'^utilisateurs$', views.UtilisateurView.as_view(), name='Utilisateurs'),
	url(r'^modif_profil$', views.ModifProfil, name='ModifProfil'),
	url(r'^message$', views.EnvoiMessage, name='EnvoiMessage'),
	url(r'^supp_message/(?P<user_name>\w+)/(?P<pk_speech>\d+)$', views.SupprMessage, name='SupprMessage'),
	url(r'^abonnement/(?P<user_name>\w+)$', views.AbonnementUtilisateur, name='Abonnement'),
	url(r'^desabonnement/(?P<user_name>\w+)$', views.DesbonnementUtilisateur, name='Desbaonnement'),
)
