import os
from urllib.request import urlopen
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from catalog.models import Category, Product
from pricing.models import ProductPrice
from decimal import Decimal


class Command(BaseCommand):
    help = 'Popula o banco de dados com produtos de exemplo com imagens reais'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando população de produtos...')

        # Produtos com URLs de imagens reais do Unsplash
        produtos_data = [
            {
                'categoria': 'hortifruti',
                'produtos': [
                    {
                        'nome': 'Alface Americana',
                        'codigo': 'ALF001',
                        'unidade': 'un',
                        'preco': Decimal('3.99'),
                        'preco_promocional': Decimal('2.99'),
                        'imagem_url': 'https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?w=500&h=500&fit=crop'
                    },
                    {
                        'nome': 'Tomate Italiano',
                        'codigo': 'TOM001',
                        'unidade': 'kg',
                        'preco': Decimal('5.99'),
                        'preco_promocional': Decimal('4.49'),
                        'imagem_url': 'https://images.unsplash.com/photo-1546094096-0df4bcaaa337?w=500&h=500&fit=crop'
                    },
                    {
                        'nome': 'Banana Prata',
                        'codigo': 'BAN001',
                        'unidade': 'kg',
                        'preco': Decimal('4.99'),
                        'preco_promocional': None,
                        'imagem_url': 'https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=500&h=500&fit=crop'
                    },
                    {
                        'nome': 'Maçã Fuji',
                        'codigo': 'MAC001',
                        'unidade': 'kg',
                        'preco': Decimal('6.99'),
                        'preco_promocional': Decimal('5.99'),
                        'imagem_url': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=500&h=500&fit=crop'
                    },
                ],
            },
            {
                'categoria': 'bebidas',
                'produtos': [
                    {
                        'nome': 'Coca-Cola 2L',
                        'codigo': 'COC001',
                        'unidade': 'un',
                        'preco': Decimal('8.99'),
                        'preco_promocional': Decimal('6.99'),
                        'imagem_url': 'https://images.unsplash.com/photo-1554866585-cd94860890b7?w=500&h=500&fit=crop'
                    },
                    {
                        'nome': 'Suco de Laranja Natural 1L',
                        'codigo': 'SUC001',
                        'unidade': 'un',
                        'preco': Decimal('12.99'),
                        'preco_promocional': None,
                        'imagem_url': 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=500&h=500&fit=crop'
                    },
                ],
            },
            {
                'categoria': 'padaria',
                'produtos': [
                    {
                        'nome': 'Pão Francês',
                        'codigo': 'PAO001',
                        'unidade': 'kg',
                        'preco': Decimal('12.90'),
                        'preco_promocional': Decimal('9.90'),
                        'imagem_url': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500&h=500&fit=crop'
                    },
                    {
                        'nome': 'Pão de Forma Integral',
                        'codigo': 'PAO002',
                        'unidade': 'un',
                        'preco': Decimal('7.99'),
                        'preco_promocional': None,
                        'imagem_url': 'https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=500&h=500&fit=crop'
                    },
                ],
            },
            {
                'categoria': 'laticinios',
                'produtos': [
                    {
                        'nome': 'Leite Integral 1L',
                        'codigo': 'LEI001',
                        'unidade': 'un',
                        'preco': Decimal('4.99'),
                        'preco_promocional': Decimal('3.99'),
                        'imagem_url': 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=500&h=500&fit=crop'
                    },
                    {
                        'nome': 'Queijo Mussarela Fatiado 200g',
                        'codigo': 'QUE001',
                        'unidade': 'un',
                        'preco': Decimal('15.99'),
                        'preco_promocional': Decimal('12.99'),
                        'imagem_url': 'https://images.unsplash.com/photo-1618164436241-4473940d1f5c?w=500&h=500&fit=crop'
                    },
                ],
            },
        ]

        for cat_data in produtos_data:
            # Buscar ou criar categoria
            try:
                categoria = Category.objects.get(slug=cat_data['categoria'])
                self.stdout.write(f'Categoria encontrada: {categoria.name}')
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Categoria {cat_data["categoria"]} não encontrada, pulando...'))
                continue

            for prod_data in cat_data['produtos']:
                # Verificar se produto já existe
                if Product.objects.filter(code=prod_data['codigo']).exists():
                    self.stdout.write(self.style.WARNING(f'Produto {prod_data["nome"]} já existe, pulando...'))
                    continue

                # Baixar imagem
                try:
                    self.stdout.write(f'Baixando imagem para {prod_data["nome"]}...')
                    with urlopen(prod_data['imagem_url'], timeout=10) as response:
                        image_content = response.read()
                    
                    # Criar produto
                    produto = Product.objects.create(
                        name=prod_data['nome'],
                        code=prod_data['codigo'],
                        category=categoria,
                        unit=prod_data['unidade'],
                        is_active=True,
                        is_featured=True if prod_data['preco_promocional'] else False,
                        description=f'{prod_data["nome"]} de alta qualidade, fresquinho e selecionado.'
                    )

                    # Salvar imagem
                    image_name = f"{prod_data['codigo']}.jpg"
                    produto.image.save(image_name, ContentFile(image_content), save=True)

                    # Criar preço
                    ProductPrice.objects.create(
                        product=produto,
                        regular_price=prod_data['preco'],
                        sale_price=prod_data['preco_promocional'],
                        is_active=True
                    )

                    self.stdout.write(self.style.SUCCESS(f'✓ Produto criado: {produto.name}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ Erro ao criar {prod_data["nome"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('População de produtos concluída!'))
