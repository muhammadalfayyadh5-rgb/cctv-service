from django.contrib import admin
from .models import Pelanggan

@admin.register(Pelanggan)
class PelangganAdmin(admin.ModelAdmin):
    list_display = (
        'nama',
        'no_hp',
        'paket',
        'status'
    )