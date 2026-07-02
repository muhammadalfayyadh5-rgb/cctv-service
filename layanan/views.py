import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from urllib.parse import quote
from datetime import datetime

from .models import (
    Pelanggan,
    Produk,
    Testimoni,
    Layanan,
    Pembayaran,
    Galeri,
    Rating
)


# =======================
# HOME
# =======================
def home(request):
    context = {
        'produk': Produk.objects.all(),
        'layanan': Layanan.objects.all(),
        'testimoni': Testimoni.objects.all(),
        'pembayaran': Pembayaran.objects.all(),
        'galeri': Galeri.objects.all(),
    }
    return render(request, 'home.html', context)


# =======================
# RIWAYAT
# =======================
def riwayat(request):

    pelanggan = Pelanggan.objects.all()

    selesai = pelanggan.filter(status="Selesai").count()
    proses = pelanggan.filter(status="Diproses").count()
    verifikasi = pelanggan.filter(status="Menunggu Verifikasi").count()

    return render(request, 'riwayat.html', {
        'pelanggan': pelanggan,
        'selesai': selesai,
        'proses': proses,
        'verifikasi': verifikasi,
    })


# =======================
# PESAN
# =======================
def pesan(request):

    if request.method == "POST":

        nama = request.POST.get("nama")
        alamat = request.POST.get("alamat")
        no_hp = request.POST.get("no_hp")
        paket = request.POST.get("paket")

        if no_hp.startswith("0"):
            no_hp = "62" + no_hp[1:]

        Pelanggan.objects.create(
            user=request.user if request.user.is_authenticated else None,
            nama=nama,
            alamat=alamat,
            no_hp=no_hp,
            paket=paket,
            status="Menunggu Verifikasi"
        )

        pesan_wa = "Halo Admin CCTV"

        wa_url = f"https://wa.me/6281262713159?text={quote(pesan_wa)}"

        return redirect(wa_url)

    return render(request, 'pesan.html')


# =======================
# EDIT
# =======================
def edit_pelanggan(request, id):
    pelanggan = get_object_or_404(Pelanggan, id=id)

    if request.method == "POST":
        pelanggan.nama = request.POST['nama']
        pelanggan.alamat = request.POST['alamat']
        pelanggan.no_hp = request.POST['no_hp']
        pelanggan.paket = request.POST['paket']
        pelanggan.status = request.POST['status']
        pelanggan.save()
        return redirect('riwayat')

    return render(request, 'edit.html', {'pelanggan': pelanggan})


# =======================
# HAPUS
# =======================
def konfirmasi_hapus(request, id):
    pelanggan = get_object_or_404(Pelanggan, id=id)
    return render(request, 'hapus.html', {'pelanggan': pelanggan})


def hapus_pelanggan(request, id):
    pelanggan = get_object_or_404(Pelanggan, id=id)

    if request.method == "POST":
        pelanggan.delete()

    return redirect('riwayat')


# =======================
# ABOUT
# =======================
def about(request):
    return render(request, 'about.html')


# =======================
# RATING
# =======================
def rating(request):

    if request.method == "POST":
        Rating.objects.create(
            nama=request.POST.get('nama'),
            rating=request.POST.get('rating'),
            komentar=request.POST.get('komentar')
        )
        return redirect('rating')

    komentar = Rating.objects.all().order_by('-tanggal')

    return render(request, 'komentar_rating.html', {
        'komentar': komentar
    })