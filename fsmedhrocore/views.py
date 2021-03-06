from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from fsmedhrocore.forms import UserForm, FachschaftUserForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def fachschaft_index(request):
    messages.info(request, 'Info: Diese Seite befindet sich noch im Aufbau...')
    return render(request, 'fsmedhrocore/index.html')


@login_required
def user_profile(request, username):
    p_user = get_object_or_404(User, username=username)

    try:
        f_user = p_user.fachschaftuser
    except ObjectDoesNotExist:
        f_user = None
        if request.user == p_user:
            # wenn eigenes profil, aber noch kein Fachschaft-Profil, dann bearbeiten/hinzufügen
            return redirect(user_edit)

    context = {'p_user': p_user, 'f_user': f_user}

    return render(request, 'fsmedhrocore/user_profile.html', context)


@login_required
def user_self_redirect(request):

    # view personal profile
    return redirect('fachschaft:fsmedhro_user_profile', username=request.user.username)


@login_required
def user_edit(request):
    """
    context = {'user': request.user}
    if hasattr(request.user, 'fachschaftuser'):
        # Fachschaft-User schon vorhanden -> zum Profil
        return redirect('user_profile', username=request.user.username)
    else:
        # neuen Fachschaft-User anlegen
        return render(request, 'fsmedhrocore/user_edit.html', context)
    """

    if request.method == 'POST':

        try:
            # FachschaftUser bereits vorhanden?
            fuform = FachschaftUserForm(data=request.POST, instance=request.user.fachschaftuser)
        except ObjectDoesNotExist:
            fuform = FachschaftUserForm(data=request.POST)

        if fuform.is_valid():

            fuser = fuform.save(commit=False)
            fuser.user = request.user
            fuser.save()
            return redirect('fachschaft:fsmedhro_user_profile', username=request.user.username)
    else:
        try:
            # FachschaftUser bereits vorhanden?
            fuform = FachschaftUserForm(instance=request.user.fachschaftuser)
        except ObjectDoesNotExist:
            fuform = FachschaftUserForm()

    return render(request, 'fsmedhrocore/user_edit.html', {'fuform': fuform})
