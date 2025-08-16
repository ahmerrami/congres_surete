from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core import signing, mail
from django.urls import reverse
from django.conf import settings
from django.views.generic import ListView
from .forms import UserRegisterForm
from .models import User
from participants.models import Participant
from reservations.models import Reservation

def _activation_token(email: str) -> str:
    return signing.TimestampSigner().sign(email)

def _activation_link(token: str) -> str:
    return f"{settings.SITE_URL}{reverse('accounts:activate', args=[token])}".replace('%2F','/')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # allow login only after activation flag used; still create record
            user.is_confirmed = False
            user.save()
            # create a linked Participant row
            Participant.objects.create(
                first_name=user.first_name or '',
                last_name=user.last_name or '',
                email=user.email,
                phone='',
                nationality='',
                institution='',
                is_confirmed=False
            )
            token = _activation_token(user.email)
            link = _activation_link(token)
            subject = 'Account Activation — Security Congress'
            body = f'Hello {user.first_name},\n\nThank you for registering. Activate your account: {link}\n\nBest regards.'
            mail.send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            messages.success(request, 'Account created. An activation email has been sent to you.')
            return redirect('core:home')
    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {'form': form})

def activate_view(request, token: str):
    try:
        email = signing.TimestampSigner().unsign(token, max_age=60*60*24*7)
        user = get_object_or_404(User, email=email)
        if not user.is_confirmed:
            user.is_confirmed = True
            user.save(update_fields=['is_confirmed'])
            # update participant record
            try:
                p = Participant.objects.get(email=user.email)
                p.is_confirmed = True
                p.save(update_fields=['is_confirmed'])
            except Participant.DoesNotExist:
                pass
            messages.success(request, 'Your account is activated. You can now log in and make reservations.')
        else:
            messages.info(request, 'Account already activated.')
    except Exception:
        messages.error(request, 'Invalid or expired activation link.')
    return redirect('account_login')

def profile_view(request):
    return render(request, 'accounts/profile.html')

class MyReservationsView(ListView):
    template_name = 'accounts/my_reservations.html'
    context_object_name = 'reservations'
    def get_queryset(self):
        # find participant by email linked to user
        try:
            p = Participant.objects.get(email=self.request.user.email)
            return Reservation.objects.filter(participant=p).order_by('-created_at')
        except Participant.DoesNotExist:
            return Reservation.objects.none()