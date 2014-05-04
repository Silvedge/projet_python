# Create your views here.
from django import forms
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.timezone import utc
from django.template.defaultfilters import stringfilter
from django.templatetags.static import static
from twitter_like_app.models import Utilisateur, Message, Abonnement
from twitter_like_app.forms import FormInscription, FormLogin, FormMessage, FormModifProfil
import datetime
import os.path
# Create your views here.

from django.views import generic
class UtilisateurView(generic.ListView):
	model = Utilisateur
	template_name = 'utilisateurs.html'
	context_object_name = 'Utilisateur'

@stringfilter
def int_to_string(value):
    return value

@login_required(login_url='twitter_like:Login')
def Profil(request,Utilisateur_name,display_abo=False):
	if request.user.is_authenticated():
		user_log = Utilisateur.objects.get(pk = request.user.pk)
		Utilisateur = get_object_or_404(Utilisateur, username = Utilisateur_name)
		if user_log != Utilisateur or display_abo == False:
			abo = Abonnement.objects.filter(UtilisateurSuivi = Utilisateur).filter(utilisateurQuiSuit = user_log)
			texts = Message.objects.filter(Utilisateur = Utilisateur).order_by('-date')
		else:
			abo = []
			UtilisateurSuivi = Abonnement.objects.filter(utilisateurQuiSuit = user_log)
			texts = []
			for i in UtilisateurSuivi:
				texts += Message.objects.filter(Utilisateur = i.UtilisateurSuivi)
			texts.sort(key=lambda x: x.date, reverse=True)
		count_messages = Message.objects.filter(Utilisateur = Utilisateur).count()
		count_abonnes = Abonnement.objects.filter(UtilisateurSuivi = Utilisateur).count()-1
		count_abonnements = Abonnement.objects.filter(utilisateurQuiSuit = Utilisateur).count()-1
		formulaire = FormMessage()

		contexte = {'formulaire' : formulaire,
				'Utilisateur' : Utilisateur,
				'user_log' : user_log,
				'texts' : texts,
				'count_Message' : count_Message,
				'count_abonnements' : count_abonnements,
				'count_abonnes' : count_abonnes,
				'avatar' : avatar,
				'abo' : abo,}
		return render(request,'Utilisateur.html',contexte)
	return Index(request)

@csrf_protect
def Inscription(request):
        if request.method == 'POST':
                formulaire = FormInscription(request.POST)
                if formulaire.is_valid():
                        Utilisateur = Utilisateur()
                        Utilisateur.username = formulaire.cleaned_data['username']
                        Utilisateur.first_name = formulaire.cleaned_data['first_name']
                        Utilisateur.last_name = formulaire.cleaned_data['last_name']
                        Utilisateur.set_password(formulaire.cleaned_data['password'])
                        Utilisateur.email = formulaire.cleaned_data['email']
                        Utilisateur.description_profil = formulaire.cleaned_data['description_profil']
                        Utilisateur.save()
			abo = Abonnement()
			abo.utilisateurQuiSuit = Utilisateur
			abo.UtilisateurSuivi = Utilisateur
			abo.save()
			Login(request)
			return render(request,'index.html')
        else:
                formulaire = FormInscription()     
        contexte = {'formulaire' : formulaire}
        return render(request,'subscribe.html',contexte)

def Login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		Utilisateur = authenticate(username=username, password=password)
		if Utilisateur is not None:
			if Utilisateur.is_active:
				login(request, Utilisateur)
				contexte = {'user_log' : Utilisateur,}
				return render(request,'index.html',contexte)
			else:
				return Index(request)
		else:
				return Index(request)
	else:
		formulaire = FormLogin()
	contexte = {'formulaire' : formulaire}
	return render(request,'login.html',contexte)

@csrf_protect
@login_required(login_url='twitter_like:Login')
def EnvoiMessage(request):
	if request.user.is_authenticated():
		user_log = Utilisateur.objects.get(pk = request.user.pk)
		if request.method == 'POST':
			formulaire = FormMessage(request.POST)
			if formulaire.is_valid():
				post = Message()
				post.text = formulaire.cleaned_data['text']
				post.Utilisateur = user_log
				post.date = datetime.datetime.now().replace(tzinfo=utc)
				post.save()
				return Index(request)
		else:
			formulaire = FormMessage()
		contexte = {'formulaire' : formulaire, 'user_log' : user_log,}
		return render(request,'post.html',contexte)
	return Index(request)

@login_required(login_url='twitter_like:Login')
def SupprMessage(request, Utilisateur_name, pk_Message):
	if request.user.is_authenticated():
		try:
			Message = Message.objects.get(pk = pk_Message)
		except:
			Message = None
		if Message != None and request.user.id == Message.Utilisateur.id:
			Message.delete()
	return Index(request)

@login_required(login_url='twitter_like:Login')
def Logout(request):
	if request.user.is_authenticated():
		logout(request)
	return Index(request)

def ConnexionOK(request):
	return render(request,'connexion_ok.html')

def Index(request):
	if request.user.is_authenticated():
		user_log = request.user
	else:
		user_log = Utilisateur()
	return Profil(request,user_log.username,True)

@login_required(login_url='twitter_like:Login')
def ModifProfil(request):
	if request.user.is_authenticated():
		Utilisateur = Utilisateur.objects.get(pk = request.user.pk)
		if request.method == 'POST':
			formulaire = FormModifProfil(request.POST,request.FILES)
			if formulaire.is_valid():
				Utilisateur.first_name = formulaire.cleaned_data['first_name']
				Utilisateur.last_name = formulaire.cleaned_data['last_name']
				Utilisateur.set_password(formulaire.cleaned_data['password'])
				Utilisateur.email = formulaire.cleaned_data['email']
				Utilisateur.description_profil = formulaire.cleaned_data['description_profil']
				Utilisateur.save()
				return Index(request)
		else:
			formulaire = FormModifProfil({'last_name': Utilisateur.last_name,
							'first_name' : Utilisateur.first_name,
							'email' : Utilisateur.email,
							'password': Utilisateur.password,
							'password_confirm': Utilisateur.password,
							'description_profil': Utilisateur.description_profil,
							})
		contexte = {'formulaire' : formulaire, 'user_log' : Utilisateur, }
		return render(request,'modify.html',contexte)
	return Index(request)

@login_required(login_url='twitter_like:Login')
def AbonnementUtilisateur(request,Utilisateur_name):
	if request.user.is_authenticated():
		# on recupere les Utilisateur
		Utilisateur_utilisateurQuiSuit = Utilisateur.objects.get(pk = request.user.pk)
		Utilisateur_UtilisateurSuivi = get_object_or_404(Utilisateur, username = Utilisateur_name)
		# on cherche s'il y a deja un abonnement
		abo = Abonnement.objects.filter(UtilisateurSuivi = Utilisateur_UtilisateurSuivi).filter(utilisateurQuiSuit = Utilisateur_utilisateurQuiSuit)
		# peut s'abonner que s'il n'existe pas d'abonnement
		if not abo and Utilisateur_utilisateurQuiSuit != Utilisateur_UtilisateurSuivi:
			Abonnement = Abonnement()
			Abonnement.utilisateurQuiSuit = Utilisateur_utilisateurQuiSuit
			Abonnement.UtilisateurSuivi = Utilisateur_UtilisateurSuivi
			Abonnement.save()
	return Profil(request,Utilisateur_UtilisateurSuivi.username)

@login_required(login_url='twitter_like:Login')
def DesbonnementUtilisateur(request,Utilisateur_name):
	if request.user.is_authenticated():
		Utilisateur_utilisateurQuiSuit = Utilisateur.objects.get(pk = request.user.pk)
		Utilisateur_UtilisateurSuivi = get_object_or_404(Utilisateur, username = Utilisateur_name)
		abo = Abonnement.objects.filter(UtilisateurSuivi = Utilisateur_UtilisateurSuivi).filter(utilisateurQuiSuit = Utilisateur_utilisateurQuiSuit)
		# peut se desabonner que s'il existe un abonnement
		if abo and Utilisateur_utilisateurQuiSuit != Utilisateur_UtilisateurSuivi:
			abo.delete()
	return Profil(request,Utilisateur_UtilisateurSuivi.username)
