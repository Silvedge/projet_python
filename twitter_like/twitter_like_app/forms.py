# coding: utf-8

from django import forms
from django.core.files.images import get_image_dimensions
from twitter_like_app.models import Utilisateur, Message

class FormInscription(forms.ModelForm):
	password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirmer le mot de passe")
	email_confirm = forms.EmailField(label=u"Confirmer l'adresse électronique")

	class Meta:
		model = Utilisateur
		fields = ['username','last_name','first_name','password','password_confirm','email','email_confirm','description_profil',]
		widgets = { 'password' : forms.PasswordInput(), }

	""" Pour verifier mdp"""
	def clean_password(self):
		if self.data['password'] != self.data['password_confirm']:
			# en cas d'erreur, lever une exception
			raise forms.ValidationError(u'Les mots de passe sont différents !')
		return self.data['password']

	""" Pour verifier adresse mail """
	def clean_email(self):
		if self.data['email'] != self.data['email_confirm']:
			# en cas d'erreur, lever une exception
			raise forms.ValidationError(u'Les adresses électroniques sont différentes')
		return self.data['email']

class FormLogin(forms.ModelForm):
	class Meta:
		model = Utilisateur
		fields = ['username','password']
		widgets = { 'password' : forms.PasswordInput(), }

class FormMessage(forms.ModelForm):
	text = forms.CharField(label=u"Postez un message")
	class Meta:
		model = Message
		fields = {'text'}

class FormModifProfil(forms.ModelForm):
	password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirmer le mot de passe")

	class Meta:
		model = Utilisateur
		fields = ['first_name', 'last_name', 'password', 'password_confirm', 'email', 'description_profil',]
		widgets = { 'password' : forms.PasswordInput(), }

	def clean_password(self):
		if self.data['password'] != self.data['password_confirm']:
			raise forms.ValidationError(u'Les mots de passe sont différents !')
		return self.data['password']

