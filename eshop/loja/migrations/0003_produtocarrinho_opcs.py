# Generated by Django 4.0.4 on 2022-05-15 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0002_alter_produtofinal_produto'),
    ]

    operations = [
        migrations.AddField(
            model_name='produtocarrinho',
            name='opcs',
            field=models.CharField(default='Questao1 Cor, Questao2 tamanho', max_length=100),
        ),
    ]
