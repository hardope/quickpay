# Generated by Django 5.0.3 on 2024-03-05 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_otp_code_alter_transaction_receiver_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='code',
            field=models.IntegerField(default=742096),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(blank=True, choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=10),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='acc_no',
            field=models.CharField(default=7355304771, max_length=10, unique=True),
        ),
    ]
