# Generated by Django 5.1.3 on 2024-11-22 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0011_bank_account_farmer_bank_transition'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bank_account',
            old_name='phonepe_name',
            new_name='bank_name',
        ),
        migrations.RenameField(
            model_name='bank_account',
            old_name='phonepe_number',
            new_name='number',
        ),
    ]
