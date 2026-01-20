import os
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from stores.models import ShopConfig
from catalog.models import Category, Product, ProductImage
from pricing.models import ProductPrice
from cms.models import Banner


class Command(BaseCommand):
    help = 'Seed database with sample data for single store'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Create ShopConfig
        self.stdout.write('Creating ShopConfig...')
        shop = ShopConfig.get_config()
        shop.whatsapp = '(11) 99999-9999'
        shop.phone = '(11) 3456-7890'
        shop.email = 'contato@shopmarket.com'
        shop.save()
        
        # Create Banners
        self.stdout.write('Creating Banners...')
        Banner.objects.all().delete()
        Banner.objects.create(title='Ofertas da Semana', order=1, is_active=True)
        Banner.objects.create(title='Produtos Frescos', order=2, is_active=True)
        Banner.objects.create(title='Entrega no Mesmo Dia', order=3, is_active=True)
        
        # Create categories
        self.stdout.write('Creating categories...')
        Category.objects.all().delete()
        categories_data = [
            ('Hortifrúti', 'hortifruti', 1),
            ('Padaria', 'padaria', 2),
            ('Bebidas', 'bebidas', 3),
            ('Laticínios', 'laticinios', 4),
            ('Limpeza', 'limpeza', 5),
            ('Carnes', 'carnes', 6),
            ('Congelados', 'congelados', 7),
            ('Mercearia', 'mercearia', 8),
        ]
        
        categories = {}
        for name, slug, order in categories_data:
            cat = Category.objects.create(name=name, slug=slug, order=order, is_active=True)
            categories[slug] = cat
        
        # Create products
        self.stdout.write('Creating products...')
        Product.objects.all().delete()
        products_data = [
            # Hortifruti
            ('Banana Prata', 'BAN01', 'hortifruti', 'kg', 'Banana prata selecionada', 5.99, 4.99),
            ('Maçã Gala', 'MAC01', 'hortifruti', 'kg', 'Maçã gala importada', 8.99, 7.49),
            ('Tomate', 'TOM01', 'hortifruti', 'kg', 'Tomate cereja fresco', 6.49, 5.99),
            ('Alface', 'ALF01', 'hortifruti', 'un', 'Alface crespa orgânica', 2.99, None),
            
            # Padaria
            ('Pão Francês', 'PAO01', 'padaria', 'kg', 'Pão francês fresquinho', 12.90, 11.90),
            ('Pão de Forma', 'PAO02', 'padaria', 'un', 'Pão de forma integral', 8.99, 7.99),
            ('Bolo de Chocolate', 'BOL01', 'padaria', 'un', 'Bolo de chocolate artesanal', 25.00, 22.00),
            ('Croissant', 'CRO01', 'padaria', 'un', 'Croissant de manteiga', 6.50, None),
            
            # Bebidas
            ('Refrigerante Cola 2L', 'REF01', 'bebidas', 'un', 'Refrigerante sabor cola', 7.99, 5.99),
            ('Suco de Laranja 1L', 'SUC01', 'bebidas', 'un', 'Suco de laranja natural', 9.99, 8.49),
            ('Água Mineral 1.5L', 'AGU01', 'bebidas', 'un', 'Água mineral sem gás', 2.49, 1.99),
            ('Cerveja Lata 350ml', 'CER01', 'bebidas', 'un', 'Cerveja pilsen', 3.99, 3.49),
            ('Vinho Tinto 750ml', 'VIN01', 'bebidas', 'un', 'Vinho tinto reserva', 45.00, 39.90),
            
            # Laticinios
            ('Leite Integral 1L', 'LEI01', 'laticinios', 'un', 'Leite integral UHT', 4.99, 4.49),
            ('Queijo Mussarela', 'QUE01', 'laticinios', 'kg', 'Queijo mussarela fatiado', 45.90, 39.90),
            ('Iogurte Natural', 'IOG01', 'laticinios', 'un', 'Iogurte natural 170g', 3.49, 2.99),
            ('Manteiga 200g', 'MAN01', 'laticinios', 'un', 'Manteiga com sal', 12.90, 11.90),
            
            # Limpeza
            ('Detergente', 'DET01', 'limpeza', 'un', 'Detergente líquido 500ml', 2.49, 1.99),
            ('Sabão em Pó 1kg', 'SAB01', 'limpeza', 'un', 'Sabão em pó multiuso', 15.90, 13.90),
            ('Desinfetante 2L', 'DES01', 'limpeza', 'un', 'Desinfetante lavanda', 9.90, 8.90),
            ('Papel Higiênico 12un', 'PAP01', 'limpeza', 'un', 'Papel higiênico folha dupla', 18.90, 16.90),
        ]
        
        for name, code, cat_slug, unit, desc, reg, sale in products_data:
            product = Product.objects.create(
                name=name,
                code=code,
                category=categories[cat_slug],
                unit=unit,
                description=desc,
                is_active=True
            )
            
            # Create price
            ProductPrice.objects.create(
                product=product,
                regular_price=Decimal(str(reg)),
                sale_price=Decimal(str(sale)) if sale else None,
                is_active=True
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded database!'))
        self.stdout.write(f'- Created 1 shop config')
        self.stdout.write(f'- Created 8 categories')
        self.stdout.write(f'- Created {len(products_data)} products')
