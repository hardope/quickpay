# Generated by Django 5.0.3 on 2024-03-05 23:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_transaction_user_transaction_receiver_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='code',
            field=models.IntegerField(default=153329),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='receiver',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='account.userprofile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='acc_no',
            field=models.CharField(default=8328814751, max_length=10, unique=True),
        ),
    ]
