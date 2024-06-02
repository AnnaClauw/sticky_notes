# sticky_notes/urls.py
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path, include
from sticky_notes_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', include('sticky_notes_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # for login/logout
    path('signup/', views.signup, name='signup'),  # custom signup view
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False))
]
