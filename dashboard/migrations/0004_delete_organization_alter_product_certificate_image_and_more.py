# Generated by Django 5.1.2 on 2024-10-13 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_product_certificate_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Organization',
        ),
        migrations.AlterField(
            model_name='product',
            name='certificate_image',
            field=models.ImageField(blank=True, null=True, upload_to='certificates/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ipfs_hash',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('Farm', 'Farm'), ('Processing', 'Processing'), ('Distribution', 'Distribution'), ('Retail', 'Retail')], max_length=20),
        ),
    ]