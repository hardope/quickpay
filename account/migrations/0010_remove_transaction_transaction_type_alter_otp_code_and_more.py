# Generated by Django 5.0.3 on 2024-03-05 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_rename_transaction_id_transaction_id_alter_otp_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='transaction_type',
        ),
        migrations.AlterField(
            model_name='otp',
            name='code',
            field=models.IntegerField(default=131493),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='acc_no',
            field=models.CharField(default=5573983446, max_length=10, unique=True),
        ),
    ]
