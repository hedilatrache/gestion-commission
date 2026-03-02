from django.contrib import admin
from .models import *

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'nom', 'prenom', 'is_active', 'date_creation']
    list_filter = ['is_active', 'date_creation']
    search_fields = ['username', 'email', 'nom', 'prenom']
    # Pas de filter_horizontal pour 'roles' car c'est un ManyToMany avec through


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'etat', 'description']
    list_filter = ['etat']
    search_fields = ['nom']
    # 🔥 CORRECTION : Supprimer filter_horizontal pour 'permissions' car c'est aussi un ManyToMany avec through
    # filter_horizontal = ['permissions']  ← À supprimer


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['nom']
    search_fields = ['nom']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'permission', 'utilisateur', 'date_attribution']
    list_filter = ['date_attribution', 'role', 'permission']
    search_fields = ['role__nom', 'permission__nom', 'utilisateur__username']
    raw_id_fields = ['role', 'permission', 'utilisateur']  # Alternative plus légère


@admin.register(TypeCommission)
class TypeCommissionAdmin(admin.ModelAdmin):
    list_display = ['nom', 'etat']
    list_filter = ['etat']


@admin.register(RegleCalcul)
class RegleCalculAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type_commission', 'active', 'date_creation']
    list_filter = ['active', 'type_commission']
    search_fields = ['nom', 'description']


@admin.register(PalierCommission)
class PalierCommissionAdmin(admin.ModelAdmin):
    list_display = ['regle', 'seuil_min', 'seuil_max', 'taux', 'actif']
    list_filter = ['actif', 'regle']


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'montant', 'regle', 'statut', 'date_calcul']
    list_filter = ['statut', 'date_calcul']
    search_fields = ['utilisateur__username', 'utilisateur__nom', 'description']
    raw_id_fields = ['utilisateur', 'regle']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'entite', 'utilisateur', 'date_action']
    list_filter = ['action', 'entite', 'date_action']
    readonly_fields = ['action', 'entite', 'utilisateur', 'date_action', 'details']
    search_fields = ['action', 'entite']