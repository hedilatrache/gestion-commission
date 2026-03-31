from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from commissions import views
from django.shortcuts import redirect

# Rediriger la racine vers login
def home(request):
    return redirect('login')

urlpatterns = [
    path('', home, name='home'),   # page d'accueil → login
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('utilisateurs/', views.utilisateurs_list, name='utilisateurs_list'),
    path('utilisateur/add/', views.utilisateur_add, name='utilisateur_add'),
    path('utilisateur/<int:pk>/edit/', views.utilisateur_edit, name='utilisateur_edit'),
    path('utilisateur/<int:pk>/delete/', views.utilisateur_delete, name='utilisateur_delete'),
    path('utilisateurs/import/', views.utilisateurs_import_excel, name='utilisateurs_import_excel'),
]