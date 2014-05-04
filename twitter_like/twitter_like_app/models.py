from django.db import models
from django.contrib.auth.models import User

class Utilisateur(User):
	description_profil = models.CharField(max_length=180, blank=True)

""" Classe qui symbolise les messages """
class Message(models.Model):
	texte = models.CharField(max_length=140)
	date_publication = models.DateTimeField()
	utilisateur = models.ForeignKey(Utilisateur)
	#utilisateur = models.ForeignKey(Utilisateur, related_name='utilisateur+')
	# Si c'est un retweet, il faut indiquer le nom de l'utilisateur qui retweet
	#retweeteur = models.ForeignKey(Utilisateur, related_name='retweeteur+', null=True) 

	def __unicode__(self):
		return self.texte

""" Classe pour de gerer les abonnements """
class Abonnement(models.Model):
	# References sur deux utilisateurs
	# Exemple : A s'abonne a B
	# A est l'utilisateur qui suit
	# B est l'utilisateur suivi
	utilisateurSuivi = models.ForeignKey(Utilisateur,related_name="utilisateurSuivi")
	utilisateurQuiSuit = models.ForeignKey(Utilisateur,related_name="utilisateurQuiSuit")
