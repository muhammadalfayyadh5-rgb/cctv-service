from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pelanggan
from urllib.parse import quote
from django.contrib.auth import logout

ADMIN_WA = "6281262713159"


# =======================
# HOME
# =======================
@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('login')


# =======================
# DASHBOARD
# =======================
@login_required(login_url='login')
def dashboard(request):
    pelanggan = Pelanggan.objects.all()

    selesai = Pelanggan.objects.filter(status="Selesai").count()
    proses = Pelanggan.objects.filter(status="Sedang Diproses").count()
    pending = Pelanggan.objects.filter(status="Menunggu Instalasi").count()

    return render(request, 'dashboard.html', {
        'pelanggan': pelanggan,
        'selesai': selesai,
        'pending': pending,
        'proses': proses
    })


# =======================
# PESAN
# =======================
@login_required(login_url='login')
def pesan(request):
    if request.method == "POST":

        nama = request.POST.get('nama')
        alamat = request.POST.get('alamat')
        no_hp = request.POST.get('no_hp')
        paket = request.POST.get('paket')

        bukti = request.FILES.get('bukti_pembayaran')

        print("FILES:", request.FILES)
        print("BUKTI:", bukti)

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
@login_required(login_url='login')
def edit_pelanggan(request, id):
    pelanggan = get_object_or_404(Pelanggan, id=id)

    if request.method == "POST":
        pelanggan.nama = request.POST['nama']
        pelanggan.alamat = request.POST['alamat']
        pelanggan.no_hp = request.POST['no_hp']
        pelanggan.paket = request.POST['paket']
        pelanggan.status = request.POST['status']

        if request.FILES.get('bukti_pembayaran'):
            pelanggan.bukti_pembayaran = request.FILES.get('bukti_pembayaran')

        pelanggan.save()

        return redirect('dashboard')

    return render(request, 'edit.html', {
        'pelanggan': pelanggan
    })


# =======================
# HAPUS KONFIRMASI
# =======================
@login_required(login_url='login')
def konfirmasi_hapus(request, id):
    pelanggan = get_object_or_404(Pelanggan, id=id)
    return render(request, 'hapus.html', {'pelanggan': pelanggan})


# =======================
# HAPUS FINAL
# =======================
@login_required(login_url='login')
def hapus_pelanggan(request, id):
    pelanggan = get_object_or_404(Pelanggan, id=id)

    if request.method == "POST":
        pelanggan.delete()

    return redirect('dashboard')


# =======================
# ABOUT
# =======================
@login_required(login_url='login')
def about(request):
    return render(request, 'about.html')

# =======================
# RATING
# =======================
def rating(request):
    return render(request,'rating.html')

# =======================
# KOMENTAR
# =======================
def rating(request):
    return render(request,'komentar_rating.html')

# =======================
# RATING + KOMENTAR
# =======================

from .models import Pelanggan, Rating


def rating(request):

    if request.method == "POST":

        nama = request.POST.get('nama')

        nilai = request.POST.get('rating')

        komentar = request.POST.get('komentar')


        Rating.objects.create(

            nama=nama,

            rating=nilai,

            komentar=komentar

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