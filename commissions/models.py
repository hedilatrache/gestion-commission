from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from decimal import Decimal

# -------------------------------
# 1. MODÈLE UTILISATEUR PERSONNALISÉ
# -------------------------------
class Utilisateur(AbstractUser):
    """
    Modèle utilisateur personnalisé basé sur AbstractUser
    """
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    gsm = models.CharField(max_length=20, blank=True, null=True)
    date_creation = models.DateTimeField(default=timezone.now)
    
    # RELATIONS
    roles = models.ManyToManyField('Role', related_name='utilisateurs')

    REQUIRED_FIELDS = ['email', 'nom', 'prenom']  # username est obligatoire par défaut

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


# -------------------------------
# 2. MODÈLE ROLE
# -------------------------------
class Role(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    etat = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"


# -------------------------------
# 3. MODÈLE TYPE COMMISSION
# -------------------------------
class TypeCommission(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    etat = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Type de commission"
        verbose_name_plural = "Types de commission"


# -------------------------------
# 4. MODÈLE REGLE DE CALCUL
# -------------------------------
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


# -------------------------------
# 5. MODÈLE PALIER COMMISSION
# -------------------------------
class PalierCommission(models.Model):
    seuil_min = models.DecimalField(max_digits=10, decimal_places=2)
    seuil_max = models.DecimalField(max_digits=10, decimal_places=2)
    taux = models.DecimalField(max_digits=5, decimal_places=2)
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


# -------------------------------
# 6. MODÈLE COMMISSION
# -------------------------------
class Commission(models.Model):
    STATUT_CHOICES = [
        ('calculee', 'Calculée'),
        ('validee', 'Validée'),
        ('payee', 'Payée'),
        ('annulee', 'Annulée'),
    ]
    
    montant = models.DecimalField(max_digits=12, decimal_places=2)
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


# -------------------------------
# 7. MODÈLE AUDIT LOG
# -------------------------------
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