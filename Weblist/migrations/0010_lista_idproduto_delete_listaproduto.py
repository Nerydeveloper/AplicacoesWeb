# Generated by Django 4.1.7 on 2023-06-05 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Weblist', '0009_userprofile_remove_lista_idmyusertest_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lista',
            name='idproduto',
            field=models.ManyToManyField(to='Weblist.produto'),
        ),
        migrations.DeleteModel(
            name='ListaProduto',
        ),
    ]
