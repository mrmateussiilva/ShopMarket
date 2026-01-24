import time
import urllib.request
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from catalog.models import Product
from django.db.models import Q

class Command(BaseCommand):
    help = 'Updates products with random grocery images from the internet'

    def handle(self, *args, **options):
        # Filter for both empty string and null
        products = Product.objects.filter(Q(image='') | Q(image__isnull=True))
        total = products.count()
        self.stdout.write(f'Found {total} products without images.')

        for i, product in enumerate(products, 1):
            self.stdout.write(f'[{i}/{total}] Updating {product.name}...')
            
            try:
                # Using loremflickr for grocery category
                url = 'https://loremflickr.com/640/480/grocery'
                with urllib.request.urlopen(url, timeout=10) as response:
                    if response.status == 200:
                        # Create a filename based on product slug
                        filename = f"{product.slug}.jpg"
                        product.image.save(filename, ContentFile(response.read()), save=True)
                        self.stdout.write(self.style.SUCCESS(f'Successfully updated image for {product.name}'))
                    else:
                        self.stdout.write(self.style.ERROR(f'Failed to download image for {product.name}: {response.status}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error updating {product.name}: {str(e)}'))
            
            # Sleep briefly to be nice to the API
            time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Finished updating product images'))
