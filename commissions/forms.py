from django import forms
from .models import Utilisateur, Role

# --- Formulaire Utilisateur avec dropdown pour un rôle ---
class UtilisateurForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Direction', 'Direction'),
        ('Admin_vente', 'Admin_Vente'),
        ('Chef_zone', 'Chef_zone'),
        ('Revendeur', 'Revendeur'),
    ]

    # Dropdown fixe pour le rôle
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label='Rôle')

    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'nom', 'prenom', 'gsm', 'is_active', 'role']

# --- Formulaire Rôle ---
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['nom', 'description', 'etat']
        # suppression de permissions puisque le modèle n'a plus ce champ
        widgets = {}



class UploadExcelForm(forms.Form):
    fichier = forms.FileField(label="Fichier Excel (.xlsx)")