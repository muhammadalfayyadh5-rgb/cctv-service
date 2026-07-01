import requests
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
# CONFIG FONNTE
# =======================
FONNTE_TOKEN = "hnqfiz2QMQsh5qBecVDi"
ADMIN_WA = "6281262713159"


# =======================
# CHATBOT WHATSAPP (WEBHOOK FONNTE)
# =======================
def webhook_fonnte(request):

    if request.method != "POST":
        return JsonResponse({"status": "invalid"})

    pesan = (request.POST.get("message") or "").lower().strip()
    nomor = request.POST.get("sender")

    if not nomor:
        return JsonResponse({"status": "no sender"})

    print("INCOMING:", pesan, nomor)

    # ================= MENU UTAMA =================
    if pesan in ["halo", "hi", "menu", "test"]:
        reply = (
            "👋 *Halo, selamat datang di CCTV Planet*\n\n"
            "📌 Silakan pilih menu:\n\n"
            "1️⃣ INFO PAKET & HARGA\n"
            "2️⃣ KONSULTASI GRATIS\n"
            "3️⃣ PEMESANAN CCTV\n"
            "4️⃣ ADMIN SUPPORT"
        )

    # ================= INFO PAKET =================
    elif pesan == "1":
        reply = (
            "📦 *INFO PAKET & HARGA*\n\n"
            "🏠 *Paket Rumah*\n"
            "• 2–4 CCTV\n"
            "💰 Rp 1.500.000\n\n"
            "🏪 *Paket Toko*\n"
            "• 4–6 CCTV\n"
            "💰 Rp 3.000.000\n\n"
            "🏢 *Paket Kantor*\n"
            "• 6–8 CCTV\n"
            "💰 Rp 5.500.000\n\n"
            "🏭 *Paket Pabrik*\n"
            "• 8–16 CCTV\n"
            "💰 Rp 10.000.000\n\n"
            "👉 Ketik *3* untuk pesan sekarang"
        )

    # ================= KONSULTASI =================
    elif pesan == "2":
        reply = (
            "🛠️ *KONSULTASI GRATIS*\n\n"
            "Silakan kirim:\n"
            "• Lokasi pemasangan\n"
            "• Luas area\n"
            "• Kebutuhan CCTV\n\n"
            "Tim kami akan bantu rekomendasi terbaik 👍"
        )

    # ================= PESAN =================
    elif pesan == "3":
        reply = (
            "📝 *PEMESANAN CCTV*\n\n"
            "Silakan isi data di website kami:\n"
            "👉 https://yourdomain.com/pesan\n\n"
            "Atau kirim langsung:\n"
            "• Nama\n"
            "• Alamat\n"
            "• No WhatsApp\n"
            "• Paket pilihan"
        )

    # ================= ADMIN =================
    elif pesan == "4":
        reply = (
            "👨‍💻 *ADMIN SUPPORT*\n\n"
            f"WhatsApp Admin:\nwa.me/{ADMIN_WA}\n\n"
            "Klik untuk langsung chat admin 👍"
        )

    # ================= DEFAULT =================
    else:
        reply = (
            "❗ *Menu tidak dikenal*\n\n"
            "Ketik:\n"
            "1 - Info Paket\n"
            "2 - Konsultasi\n"
            "3 - Pesan\n"
            "4 - Admin"
        )

    # ================= KIRIM KE FONNTE =================
    url = "https://api.fonnte.com/send"

    headers = {
        "Authorization": FONNTE_TOKEN
    }

    data = {
        "target": nomor,
        "message": reply
    }

    res = requests.post(url, headers=headers, data=data)
    print(res.text)

    return JsonResponse({"status": "ok"})


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

        # format nomor
        if no_hp.startswith("0"):
            no_hp = "62" + no_hp[1:]

        # simpan ke database
        Pelanggan.objects.create(
            user=request.user if request.user.is_authenticated else None,
            nama=nama,
            alamat=alamat,
            no_hp=no_hp,
            paket=paket,
            status="Menunggu Verifikasi"
        )

# =======================
# PESAN WA KE ADMIN
# =======================
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