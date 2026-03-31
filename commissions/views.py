from django.shortcuts import render, get_object_or_404, redirect
from .models import Utilisateur, Role
from .forms import UtilisateurForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

# --- Vérifier si l'utilisateur est admin ---
def is_admin(user):
    return user.is_superuser or user.roles.filter(nom='Admin').exists()

# --- Liste utilisateurs avec recherche, filtre par rôle et pagination ---
@login_required
@user_passes_test(is_admin)
def utilisateurs_list(request):
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')

    utilisateurs = Utilisateur.objects.all().order_by('nom', 'prenom')

    # Filtrer par recherche
    if search_query:
        utilisateurs = utilisateurs.filter(
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Filtrer par rôle
    if role_filter:
        utilisateurs = utilisateurs.filter(roles__nom=role_filter)

    # Pagination : 8 utilisateurs par page
    paginator = Paginator(utilisateurs.distinct(), 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Tous les rôles pour le filtre
    roles = Role.objects.all()

    context = {
        'utilisateurs': page_obj,
        'search_query': search_query,
        'role_filter': role_filter,
        'roles': roles,
    }
    return render(request, 'commissions/utilisateurs_list.html', context)


# --- Ajouter utilisateur ---
@login_required
@user_passes_test(is_admin)
def utilisateur_add(request):
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            utilisateur.save()
            role_name = form.cleaned_data['role']
            try:
                role_obj = Role.objects.get(nom=role_name)
                utilisateur.roles.set([role_obj])
            except Role.DoesNotExist:
                messages.error(request, f"Le rôle '{role_name}' n'existe pas.")
                return redirect('utilisateur_add')
            messages.success(request, "Utilisateur ajouté avec succès !")
            return redirect('utilisateurs_list')
    else:
        form = UtilisateurForm()
    return render(request, 'commissions/utilisateur_add.html', {'form': form})


# --- Ajouter utilisateur d'aprés exel ---

@login_required
@user_passes_test(is_admin)
def utilisateurs_import_excel(request):
    from .forms import UploadExcelForm
    import pandas as pd
    from django.contrib import messages
    from .models import Utilisateur, Role

    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            fichier = request.FILES['fichier']
            try:
                df = pd.read_excel(fichier)
                required_columns = ['nom', 'prenom', 'username', 'email', 'gsm', 'role']
                for col in required_columns:
                    if col not in df.columns:
                        messages.error(request, f"Colonne manquante : {col}")
                        return redirect('utilisateurs_import_excel')

                for _, row in df.iterrows():
                    nom = str(row['nom']).strip()
                    prenom = str(row['prenom']).strip()
                    username = str(row['username']).strip()
                    email = str(row['email']).strip()
                    gsm = str(row['gsm']).strip()
                    role_name = str(row['role']).strip()

                    if Utilisateur.objects.filter(username=username).exists():
                        continue

                    utilisateur = Utilisateur.objects.create_user(
                        username=username,
                        email=email,
                        gsm=gsm,
                        nom=nom,
                        prenom=prenom
                    )

                    role_obj, _ = Role.objects.get_or_create(nom=role_name)
                    utilisateur.roles.set([role_obj])

                messages.success(request, "Importation terminée avec succès !")
                return redirect('utilisateurs_list')

            except Exception as e:
                messages.error(request, f"Erreur lors de l'import : {str(e)}")
    else:
        form = UploadExcelForm()

    return render(request, 'commissions/utilisateurs_import_excel.html', {'form': form})






# --- Modifier utilisateur ---
@login_required
@user_passes_test(is_admin)
def utilisateur_edit(request, pk):
    utilisateur = get_object_or_404(Utilisateur, pk=pk)
    if request.method == 'POST':
        form = UtilisateurForm(request.POST, instance=utilisateur)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            utilisateur.save()
            role_name = form.cleaned_data['role']
            try:
                role_obj = Role.objects.get(nom=role_name)
                utilisateur.roles.set([role_obj])
            except Role.DoesNotExist:
                messages.error(request, f"Le rôle '{role_name}' n'existe pas.")
                return redirect('utilisateur_edit', pk=utilisateur.pk)
            messages.success(request, "Utilisateur modifié avec succès !")
            return redirect('utilisateurs_list')
    else:
        initial_role = utilisateur.roles.first()
        form = UtilisateurForm(instance=utilisateur, initial={'role': initial_role.nom if initial_role else ''})
    return render(request, 'commissions/utilisateur_edit.html', {'form': form, 'utilisateur': utilisateur})

# --- Supprimer utilisateur ---
@login_required
@user_passes_test(is_admin)
def utilisateur_delete(request, pk):
    utilisateur = get_object_or_404(Utilisateur, pk=pk)
    if request.method == 'POST':
        utilisateur.delete()
        messages.success(request, "Utilisateur supprimé avec succès !")
        return redirect('utilisateurs_list')
    return render(request, 'commissions/utilisateur_delete.html', {'utilisateur': utilisateur})