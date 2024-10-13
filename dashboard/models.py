# dashboard/models.py

from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
        
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    ipfs_hash = models.CharField(max_length=255)
    solana_tx_hash = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, default="Farm")
    certificate_image = models.ImageField(upload_to='product_certificates/', blank=True, null=True)

    def __str__(self):
        return self.name
