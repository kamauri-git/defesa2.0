from django.contrib import admin
from django.urls import path, include
from ocorrencias import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # raiz vai para login
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),    # página principal protegida
    path('', include('ocorrencias.urls')),     # outras URLs do app
]