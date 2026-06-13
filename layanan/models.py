from django.db import models


class Pelanggan(models.Model):

    STATUS_CHOICES = [
        ('Menunggu Pembayaran', 'Menunggu Pembayaran'),
        ('Menunggu Verifikasi', 'Menunggu Verifikasi'),
        ('Diproses', 'Diproses'),
        ('Selesai', 'Selesai'),
    ]


    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    no_hp = models.CharField(max_length=20)
    paket = models.CharField(max_length=50)

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Menunggu Pembayaran'
    )


    bukti_pembayaran = models.ImageField(
    upload_to='bukti_pembayaran/',
    blank=True,
    null=True
)


    def __str__(self):
        return self.nama





class Rating(models.Model):

    nama = models.CharField(
        max_length=100
    )


    rating = models.IntegerField(
        default=5
    )


    komentar = models.TextField()


    tanggal = models.DateTimeField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return self.nama
    


class Produk(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField()
    harga = models.IntegerField()
    gambar = models.ImageField(upload_to='produk/')

    def __str__(self):
        return self.nama


class Testimoni(models.Model):
    nama = models.CharField(max_length=100)
    pesan = models.TextField()
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.nama


class Layanan(models.Model):
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField()
    icon = models.CharField(max_length=50, default="bi-cctv")

    def __str__(self):
        return self.judul


class Pembayaran(models.Model):
    metode = models.CharField(max_length=50)
    nomor = models.CharField(max_length=100)
    atas_nama = models.CharField(max_length=100)

    def __str__(self):
        return self.metode


class Galeri(models.Model):
    foto = models.ImageField(upload_to='galeri/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)