# Generated by Django 5.1.3 on 2025-01-21 10:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0033_alter_company_recived_payment_transaction_date'),
        ('sunil', '0002_shope_edit_pin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company_cash_transition',
            name='company_bill',
        ),
        migrations.RemoveField(
            model_name='company_cash_transition',
            name='office_employee',
        ),
        migrations.RemoveField(
            model_name='company_cash_transition',
            name='shope',
        ),
        migrations.RemoveField(
            model_name='company_phonepe_transition',
            name='company_bill',
        ),
        migrations.RemoveField(
            model_name='company_phonepe_transition',
            name='office_employee',
        ),
        migrations.RemoveField(
            model_name='company_phonepe_transition',
            name='shope',
        ),
        migrations.CreateModel(
            name='Farmer_services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.IntegerField(default=1)),
                ('shope', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='sunil.shope')),
            ],
        ),
        migrations.DeleteModel(
            name='Company_bank_transition',
        ),
        migrations.DeleteModel(
            name='Company_cash_transition',
        ),
        migrations.DeleteModel(
            name='Company_Phonepe_transition',
        ),
    ]