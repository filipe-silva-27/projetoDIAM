# Generated by Django 4.0.3 on 2022-05-09 20:03

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
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.IntegerField()),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.CharField(max_length=300)),
                ('personalizavel', models.BooleanField(default=False)),
                ('pic', models.ImageField(blank=True, null=True, upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Questao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('who', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestaoDoProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.produto')),
                ('questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.questao')),
            ],
        ),
        migrations.CreateModel(
            name='ProdutoCarrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('carrinho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.cart')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.produto')),
            ],
        ),
        migrations.AddField(
            model_name='produto',
            name='questoes',
            field=models.ManyToManyField(through='loja.QuestaoDoProduto', to='loja.questao'),
        ),
        migrations.AddField(
            model_name='produto',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='loja.vendedor'),
        ),
        migrations.CreateModel(
            name='Opcao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=200)),
                ('produto', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='loja.produto')),
                ('questao', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='loja.questao')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='produtos',
            field=models.ManyToManyField(through='loja.ProdutoCarrinho', to='loja.produto'),
        ),
    ]