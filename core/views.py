from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.utils import translation
from django.conf import settings
from django.http import JsonResponse


class HomeView(TemplateView):
    template_name = "core/home.html"


class ProgramView(TemplateView):
    template_name = "core/program.html"


def language_switch(request, lang):
    """Change la langue de l'application et la stocke en session + cookie."""
    lang = str(lang).split('-')[0]  # normalise
    translation.activate(lang)

    # Assure que la session existe et set la langue
    if hasattr(request, 'session'):
        request.session['django_language'] = lang

    # Redirect + cookie pour persistance
    response = redirect(request.META.get("HTTP_REFERER", "/"))
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        lang,
        max_age=365 * 24 * 3600,
        path='/'
    )
    return response


def debug_language(request):
    """Retourne les infos liées à la langue pour debug."""
    return JsonResponse({
        'settings.LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'request.LANGUAGE_CODE': getattr(request, 'LANGUAGE_CODE', None),
        'session_django_language': request.session.get('django_language'),
        'cookie_django_language': request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME),
        'accept_language_header': request.META.get('HTTP_ACCEPT_LANGUAGE'),
    })
