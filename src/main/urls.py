# encoding: utf-8

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpResponse


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.login, {'template_name': 'bima_back/users/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^django-rq/', include('django_rq.urls')),
    url(r'^robots\.txt', include('robots.urls')),
    url(r'^', include('bima_back.urls')),
]


# Testing for the health check
def _healthz(request):
    return HttpResponse("ok")


urlpatterns += [
    url(r'^health/$', _healthz, name="health_check"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if settings.ENABLE_DEBUG_TOOLBAR:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
