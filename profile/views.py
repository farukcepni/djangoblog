from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from forms import SignupForm, LoginForm, EditForm
from models import Profile
from django.core.signing import Signer, BadSignature
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    return redirect('profile', request.user.username)

@login_required()
def edit(request):
    profile = Profile.objects.select_related().get(user_id=request.user.id)
    if request.POST:
        form = EditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = EditForm(instance=profile)
    return render(request, 'profile/edit.html', {'form': form})


def activate_the_profile(request):
    if not request.GET:
        raise Http404('The page could not be found')
    try:
        email = Signer().unsign(request.GET.get('email'))
    except BadSignature:
        raise Http404()
    user = User.objects.select_related().get(email__iexact=email)
    user.profile.is_verified = True
    user.profile.save()
    return HttpResponse(_('Thank you to activate the your account'))


def change_email_via_mail(request):
    if not request.GET:
        raise Http404()
    try:
        email = Signer().unsign(request.GET.get('email'))
        to = Signer().unsign(request.GET.get('to'))
        user = User.objects.get(email__iexact=email)
        user.email = to
        user.save()
    except (BadSignature, User.DoesNotExist) as e:
        raise Http404()
    return HttpResponse('Changed your account email')

def profile(request, username):
    try:
        user = User.objects.select_related().get(username=username)
    except User.DoesNotExist:
        raise Http404("User Not Found")
    return render(request, 'profile/profile.html', {'user': user})


def signup(request):
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            profile = form.save()
            profile.send_activation_email()
            return redirect('signup_success')
    else:
        form = SignupForm()

    return render(request, 'profile/signup.html', {'form': form})


def signup_success(request):
    return render(request, 'profile/signup_success.html')


def login_view(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'],
                                password=form.cleaned_data['password'])
            if user is None:
                messages.error(request, _('The email or password are wrong!'))
            elif user.profile.is_verified is False:
                messages.error(request, _('Please verified your e-mail'))
            else:
                login(request, user)
                return redirect(request.GET.get('next') or reverse('index'))
    else:
        form = LoginForm
    return render(request, 'profile/login.html', {'form': form})



