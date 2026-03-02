from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# 1. MODÈLE UTILISATEUR PERSONNALISÉ (CORRIGÉ)
class Utilisateur(AbstractUser):
    """
    Modèle utilisateur personnalisé basé sur AbstractUser
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    gsm = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    
    # RELATIONS
    roles = models.ManyToManyField('Role', through='RolePermission', related_name='utilisateurs')
    
    # 🔥 CORRECTION : Désactiver les groupes et permissions par défaut de Django
    groups = None
    user_permissions = None
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nom', 'prenom']
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


# 2. MODÈLE PERMISSION
class Permission(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"


# 3. MODÈLE ROLE
class Role(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    etat = models.BooleanField(default=True)
    
    # RELATIONS
    permissions = models.ManyToManyField(Permission, through='RolePermission', related_name='roles')
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"


# 4. MODÈLE DE JONCTION Role - Permission
class RolePermission(models.Model):
    """
    Table de jonction entre Role et Permission avec métadonnées
    """
    # RELATIONS
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='permission_roles')
    utilisateur = models.ForeignKey(
        Utilisateur, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='attributions_permissions'
    )
    
    # Métadonnées
    date_attribution = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['role', 'permission', 'utilisateur']
        verbose_name = "Attribution de permission"
        verbose_name_plural = "Attributions de permissions"
    
    def __str__(self):
        return f"{self.role} - {self.permission} pour {self.utilisateur}"


# 5. MODÈLE TYPE COMMISSION
class TypeCommission(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    etat = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Type de commission"
        verbose_name_plural = "Types de commission"


# 6. MODÈLE REGLE DE CALCUL
class RegleCalcul(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    formule = models.TextField()
    active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    
    # RELATIONS
    type_commission = models.ForeignKey(
        TypeCommission, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='regles_calcul'
    )
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Règle de calcul"
        verbose_name_plural = "Règles de calcul"


# 7. MODÈLE PALIER COMMISSION
class PalierCommission(models.Model):
    seuil_min = models.FloatField()
    seuil_max = models.FloatField()
    taux = models.FloatField()
    actif = models.BooleanField(default=True)
    
    # RELATIONS
    regle = models.ForeignKey(
        RegleCalcul, 
        on_delete=models.CASCADE,
        related_name='paliers'
    )
    
    def __str__(self):
        return f"{self.regle.nom} : {self.seuil_min} - {self.seuil_max} -> {self.taux}%"
    
    class Meta:
        verbose_name = "Palier de commission"
        verbose_name_plural = "Paliers de commission"
        unique_together = ['regle', 'seuil_min', 'seuil_max']


# 8. MODÈLE COMMISSION
class Commission(models.Model):
    STATUT_CHOICES = [
        ('calculee', 'Calculée'),
        ('validee', 'Validée'),
        ('payee', 'Payée'),
        ('annulee', 'Annulée'),
    ]
    
    montant = models.FloatField()
    description = models.TextField(blank=True, null=True)
    date_calcul = models.DateTimeField(default=timezone.now)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='calculee')
    
    # RELATIONS
    utilisateur = models.ForeignKey(
        Utilisateur, 
        on_delete=models.CASCADE,
        related_name='commissions'
    )
    regle = models.ForeignKey(
        RegleCalcul, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='commissions'
    )
    
    def __str__(self):
        return f"Commission {self.utilisateur} - {self.montant}€ ({self.statut})"
    
    class Meta:
        verbose_name = "Commission"
        verbose_name_plural = "Commissions"
        ordering = ['-date_calcul']


# 9. MODÈLE AUDIT LOG
class AuditLog(models.Model):
    action = models.CharField(max_length=255)
    entite = models.CharField(max_length=100)
    date_action = models.DateTimeField(default=timezone.now)
    details = models.JSONField(default=dict, blank=True)
    
    # RELATIONS
    utilisateur = models.ForeignKey(
        Utilisateur, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='audit_logs'
    )
    
    def __str__(self):
        return f"{self.date_action} - {self.action} sur {self.entite}"
    
    class Meta:
        verbose_name = "Audit log"
        verbose_name_plural = "Audit logs"
        ordering = ['-date_action']