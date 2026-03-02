# Gestion de Commissions

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![GitHub last commit](https://img.shields.io/github/last-commit/votre-utilisateur/gestion-commission)
![GitHub repo size](https://img.shields.io/github/repo-size/votre-utilisateur/gestion-commission)

## 📋 Description

Application web développée avec Django pour la gestion des commissions. Ce projet permet de gérer les utilisateurs, les rôles, les permissions, et de calculer automatiquement les commissions selon des règles paramétrables.

## ✨ Fonctionnalités

- **Gestion des utilisateurs** : Authentification, profils avec nom, prénom, GSM
- **Système de rôles et permissions** : Contrôle d'accès granulaire
- **Types de commission** : Catégorisation des différentes commissions
- **Règles de calcul** : Définition de formules de calcul personnalisées
- **Paliers de commission** : Configuration de seuils et taux progressifs
- **Calcul automatique** des commissions pour chaque utilisateur
- **Audit log** : Traçabilité de toutes les actions importantes
- **Interface d'administration** Django personnalisée

## 🛠️ Technologies utilisées

| Technologie | Version |
|-------------|---------|
| **Framework** | Django 4.2 LTS |
| **Base de données** | MySQL (via XAMPP) |
| **Langage** | Python 3.10+ |
| **Frontend** | HTML/CSS (templates Django) |
| **Versionnement** | Git & GitHub |

## 📦 Installation

### Prérequis

- Python 3.10 ou supérieur
- MySQL (XAMPP recommandé)
- Git
- Pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le dépôt**

```bash
git clone https://github.com/votre-utilisateur/gestion-commission.git
cd gestion-commission/backend

2. **Créer un environnement virtuel**
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

3. **Installer les dépendances**
pip install -r requirements.txt

4. **Configurer la base de données MySQL**
Démarrer MySQL dans XAMPP

Ouvrir phpMyAdmin : http://localhost/phpmyadmin

Créer une base de données : CREATE DATABASE gestion_commission_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

5. **Configurer les variables d'environnement**
Créer un fichier .env à la racine du dossier backend/ :
env
SECRET_KEY=django-insecure-79$^46x!2-1jts4h)0e)s65ok_&fn)e)2$i39@35@%ev5=(!6=
DB_NAME=gestion_commission_db
DB_USER=root
DB_PASSWORD=
DEBUG=True


6. **Modifier le fichier settings.py**

python
# incentives_project/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'commissions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'incentives_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'incentives_project.wsgi.application'

# Configuration MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Modèle utilisateur personnalisé
AUTH_USER_MODEL = 'commissions.Utilisateur'


7. **Appliquer les migrations**
python manage.py makemigrations commissions
python manage.py migrate

8. **Créer un superutilisateur**
python manage.py createsuperuser

9. **Lancer le serveur**
bash
python manage.py runserver


10. **Accéder à l'application**
Site principal : http://127.0.0.1:8000

Interface d'administration : http://127.0.0.1:8000/admin

📁 Structure du projet

backend/
├── incentives_project/          # Configuration du projet
│   ├── __init__.py
│   ├── settings.py              # Paramètres Django
│   ├── urls.py                   # URLs principales
│   └── wsgi.py
├── commissions/                  # Application principale
│   ├── migrations/               # Migrations de base de données
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                  # Configuration de l'admin
│   ├── apps.py
│   ├── models.py                  # Modèles de données
│   ├── tests.py
│   └── views.py                   # Vues (à développer)
├── manage.py
├── requirements.txt               # Dépendances Python
├── .env                           # Variables d'environnement
├── .gitignore                      # Fichiers ignorés par Git
└── README.md                       # Documentation

📊 Modèles de données

Utilisateur ────┬──── Role ────┬──── Permission
                │               │
                ├──── Commission
                │
                └──── AuditLog

TypeCommission ──── RegleCalcul ──── PalierCommission
                        │
                        └──── Commission


