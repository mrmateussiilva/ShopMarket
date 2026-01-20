from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decimal import Decimal
from stores.models import Store
from catalog.models import Category, Product, ProductImage
from pricing.models import ProductPrice
from cms.models import Banner


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Create stores
        self.stdout.write('Creating stores...')
        store1, _ = Store.objects.get_or_create(
            slug='loja-centro',
            defaults={
                'name': 'ShopMarket Centro',
                'address': 'Rua das Flores, 123 - Centro - São Paulo/SP',
                'phone': '(11) 3456-7890',
                'is_active': True,
            }
        )
        
        store2, _ = Store.objects.get_or_create(
            slug='loja-zona-sul',
            defaults={
                'name': 'ShopMarket Zona Sul',
                'address': 'Av. Paulista, 456 - Bela Vista - São Paulo/SP',
                'phone': '(11) 3456-7891',
                'is_active': True,
            }
        )
        
        # Create categories
        self.stdout.write('Creating categories...')
        cat_hortifruti, _ = Category.objects.get_or_create(
            slug='hortifruti',
            defaults={'name': 'Hortifrúti', 'is_active': True, 'order': 1}
        )
        
        cat_padaria, _ = Category.objects.get_or_create(
            slug='padaria',
            defaults={'name': 'Padaria', 'is_active': True, 'order': 2}
        )
        
        cat_bebidas, _ = Category.objects.get_or_create(
            slug='bebidas',
            defaults={'name': 'Bebidas', 'is_active': True, 'order': 3}
        )
        
        cat_laticinios, _ = Category.objects.get_or_create(
            slug='laticinios',
            defaults={'name': 'Laticínios', 'is_active': True, 'order': 4}
        )
        
        cat_limpeza, _ = Category.objects.get_or_create(
            slug='limpeza',
            defaults={'name': 'Limpeza', 'is_active': True, 'order': 5}
        )
        
        # Create products
        self.stdout.write('Creating products...')
        products_data = [
            # Hortifruti
            ('Banana Prata', 'BAN001', cat_hortifruti, 'kg', 'Banana prata fresca', 5.99, 4.99, None),
            ('Maçã Gala', 'MAC001', cat_hortifruti, 'kg', 'Maçã gala importada', 8.99, 7.49, 6.99),
            ('Tomate', 'TOM001', cat_hortifruti, 'kg', 'Tomate fresco', 6.49, 5.99, None),
            ('Alface', 'ALF001', cat_hortifruti, 'un', 'Alface crespa', 2.99, None, None),
            
            # Padaria
            ('Pão Francês', 'PAO001', cat_padaria, 'kg', 'Pão francês fresquinho', 12.90, 11.90, None),
            ('Pão de Forma', 'PAO002', cat_padaria, 'un', 'Pão de forma integral', 8.99, 7.99, 6.99),
            ('Bolo de Chocolate', 'BOL001', cat_padaria, 'un', 'Bolo de chocolate caseiro', 25.00, 22.00, None),
            
            # Bebidas
            ('Refrigerante Cola 2L', 'REF001', cat_bebidas, 'un', 'Refrigerante sabor cola', 7.99, 5.99, 4.99),
            ('Suco de Laranja 1L', 'SUC001', cat_bebidas, 'un', 'Suco de laranja integral', 9.99, 8.49, None),
            ('Água Mineral 1.5L', 'AGU001', cat_bebidas, 'un', 'Água mineral sem gás', 2.49, 1.99, None),
            ('Cerveja Lata 350ml', 'CER001', cat_bebidas, 'un', 'Cerveja pilsen', 3.99, 3.49, 2.99),
            
            # Laticínios
            ('Leite Integral 1L', 'LEI001', cat_laticinios, 'un', 'Leite integral UHT', 4.99, 4.49, None),
            ('Queijo Mussarela', 'QUE001', cat_laticinios, 'kg', 'Queijo mussarela fatiado', 45.90, 39.90, 35.90),
            ('Iogurte Natural', 'IOG001', cat_laticinios, 'un', 'Iogurte natural 170g', 3.49, 2.99, None),
            ('Manteiga 200g', 'MAN001', cat_laticinios, 'un', 'Manteiga com sal', 12.90, 11.90, None),
            
            # Limpeza
            ('Detergente', 'DET001', cat_limpeza, 'un', 'Detergente líquido 500ml', 2.49, 1.99, None),
            ('Sabão em Pó 1kg', 'SAB001', cat_limpeza, 'un', 'Sabão em pó multiuso', 15.90, 13.90, 12.90),
            ('Desinfetante 2L', 'DES001', cat_limpeza, 'un', 'Desinfetante lavanda', 9.90, 8.90, None),
            ('Esponja de Limpeza', 'ESP001', cat_limpeza, 'un', 'Esponja dupla face', 3.99, 2.99, None),
            ('Papel Higiênico 12un', 'PAP001', cat_limpeza, 'un', 'Papel higiênico folha dupla', 18.90, 16.90, 14.90),
        ]
        
        for name, code, category, unit, description, regular, sale, club in products_data:
            product, created = Product.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'category': category,
                    'unit': unit,
                    'description': description,
                    'is_active': True,
                }
            )
            
            if created:
                # Create prices for both stores
                ProductPrice.objects.get_or_create(
                    product=product,
                    store=store1,
                    defaults={
                        'regular_price': Decimal(str(regular)),
                        'sale_price': Decimal(str(sale)) if sale else None,
                        'club_price': Decimal(str(club)) if club else None,
                        'is_active': True,
                    }
                )
                
                # Store 2 with slightly different prices
                store2_regular = regular * 1.05  # 5% more expensive
                store2_sale = sale * 1.05 if sale else None
                store2_club = club * 1.05 if club else None
                
                ProductPrice.objects.get_or_create(
                    product=product,
                    store=store2,
                    defaults={
                        'regular_price': Decimal(str(store2_regular)),
                        'sale_price': Decimal(str(store2_sale)) if store2_sale else None,
                        'club_price': Decimal(str(store2_club)) if store2_club else None,
                        'is_active': True,
                    }
                )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded database!'))
        self.stdout.write(f'- Created 2 stores')
        self.stdout.write(f'- Created 5 categories')
        self.stdout.write(f'- Created {len(products_data)} products')
        self.stdout.write(f'- Created {len(products_data) * 2} prices')
