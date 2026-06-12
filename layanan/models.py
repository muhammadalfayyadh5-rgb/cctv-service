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