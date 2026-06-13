from django.shortcuts import render, redirect, get_object_or_404
from urllib.parse import quote

from .models import (
    Pelanggan,
    Produk,
    Testimoni,
    Layanan,
    Pembayaran,
    Galeri,
    Rating
)

ADMIN_WA = "6281262713159"


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

    selesai = Pelanggan.objects.filter(
        status="Selesai"
    ).count()

    proses = Pelanggan.objects.filter(
        status="Diproses"
    ).count()

    verifikasi = Pelanggan.objects.filter(
        status="Menunggu Verifikasi"
    ).count()

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

        bukti = request.FILES.get("bukti_pembayaran")

        Pelanggan.objects.create(
            nama=nama,
            alamat=alamat,
            no_hp=no_hp,
            paket=paket,
            status="Menunggu Verifikasi",
            bukti_pembayaran=bukti
        )

        pesan_wa = f"""
PESANAN BARU CCTV

Nama: {nama}
No HP: {no_hp}
Paket: {paket}
Alamat: {alamat}

Bukti pembayaran telah diupload.
"""

        wa_url = f"https://wa.me/{ADMIN_WA}?text={quote(pesan_wa)}"
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

        if request.FILES.get('bukti_pembayaran'):
            pelanggan.bukti_pembayaran = request.FILES.get(
                'bukti_pembayaran'
            )

        pelanggan.save()
        return redirect('riwayat')

    return render(
        request,
        'edit.html',
        {'pelanggan': pelanggan}
    )


# =======================
# HAPUS
# =======================
def konfirmasi_hapus(request, id):
    pelanggan = get_object_or_404(Pelanggan, id=id)
    return render(
        request,
        'hapus.html',
        {'pelanggan': pelanggan}
    )


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

    return render(
        request,
        'komentar_rating.html',
        {
            'komentar': komentar
        }
    )