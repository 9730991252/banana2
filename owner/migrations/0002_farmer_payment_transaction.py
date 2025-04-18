# Generated by Django 5.1.3 on 2025-01-22 07:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0001_initial'),
        ('sunil', '0002_shope_edit_pin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Farmer_payment_transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('bank_number', models.IntegerField(null=True)),
                ('phonepe_number', models.IntegerField(null=True)),
                ('payment_type', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('farmer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='owner.farmer')),
                ('office_employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='owner.office_employee')),
                ('shope', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='sunil.shope')),
            ],
        ),
    ]
