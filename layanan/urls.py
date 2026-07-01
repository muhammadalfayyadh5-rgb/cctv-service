from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pesan/', views.pesan, name='pesan'),
    path('about/', views.about, name='about'),
    path('riwayat/', views.riwayat, name='riwayat'),
    path('rating/', views.rating, name='rating'),

    path('edit/<int:id>/', views.edit_pelanggan, name='edit'),
    path('hapus/<int:id>/', views.konfirmasi_hapus, name='konfirmasi_hapus'),
    path('hapus/<int:id>/delete/', views.hapus_pelanggan, name='hapus_pelanggan'),
    path("webhook/", views.webhook_fonnte, name="webhook_fonnte"),
]