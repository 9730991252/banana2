# Generated by Django 5.1.3 on 2025-01-04 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0028_alter_company_bill_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_bill',
            name='leaf_weight',
            field=models.IntegerField(default=0),
        ),
    ]
