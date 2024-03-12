# Generated by Django 5.0.3 on 2024-03-12 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_remove_transaction_transaction_type_alter_otp_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='pin',
            field=models.CharField(default=2992, max_length=4),
        ),
        migrations.AlterField(
            model_name='otp',
            name='code',
            field=models.IntegerField(default=205668),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='acc_no',
            field=models.CharField(default=7457236082, max_length=10, unique=True),
        ),
    ]