# Generated by Django 4.1.6 on 2023-05-05 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('ciudad_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('codigo', models.CharField(max_length=255, unique=True)),
                ('familia', models.IntegerField()),
                ('gastronomia', models.IntegerField()),
                ('cultura', models.IntegerField()),
                ('transporte', models.IntegerField()),
                ('pareja', models.IntegerField()),
                ('alojamiento', models.IntegerField()),
                ('ocio', models.IntegerField()),
                ('fiesta', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Mensajes_Toast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje_cabecera', models.CharField(max_length=255)),
                ('mensaje_detalle', models.CharField(max_length=255)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toasts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad_Mes',
            fields=[
                ('ciudad_mes_id', models.AutoField(primary_key=True, serialize=False)),
                ('mes', models.IntegerField()),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Meses', to='Gestion.ciudad')),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad_Image',
            fields=[
                ('imagen_id', models.AutoField(primary_key=True, serialize=False)),
                ('img', models.ImageField(default=None, upload_to='Image')),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Imagenes', to='Gestion.ciudad')),
            ],
        ),
    ]