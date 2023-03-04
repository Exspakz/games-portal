from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.decorators.cache import never_cache

from ckeditor_uploader.views import browse, upload

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('ckeditor/upload/', login_required(upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(browse)), name='ckeditor_browse'),

    path('', views.HomePageView.as_view(), name='home'),
    path('posts/', include('board.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
