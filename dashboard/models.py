from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    ipfs_hash = models.CharField(max_length=255, blank=True, null=True)
    solana_tx_hash = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('Farm', 'Farm'),
        ('Processing', 'Processing'),
        ('Distribution', 'Distribution'),
        ('Retail', 'Retail')
    ])
    certificate_image = models.ImageField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'ipfs_hash': self.ipfs_hash,
            'solana_tx_hash': self.solana_tx_hash,
        }