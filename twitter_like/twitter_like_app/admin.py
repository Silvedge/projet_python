from django.contrib import admin
from twitter_like_app.models import Utilisateur, Message, Abonnement

class Messages(admin.TabularInline):
	model = Message

class AdministrationUtilisateur(admin.ModelAdmin):
	fields = ['username','password','first_name','last_name','email','description_profil']    
	list_display = ('username','first_name','last_name','email','description_profil')    
	search_fields = ['username']
	inlines = [Messages]


admin.site.register(Utilisateur,AdministrationUtilisateur)
admin.site.register(Message)
admin.site.register(Abonnement)
