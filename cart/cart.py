from decimal import Decimal
from catalog.models import Product
from pricing.models import ProductPrice


class Cart:
    """Shopping cart stored in session"""
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        """Add a product to the cart"""
        product_id = str(product.id)
        
        if product_id not in self.cart:
            # Get price for product (OneToOne relationship)
            try:
                price_obj = product.price
                price = float(price_obj.get_best_price())
            except (ProductPrice.DoesNotExist, AttributeError):
                price = 0.0
            
            self.cart[product_id] = {
                'quantity': 0,
                'price': price,
                'name': product.name,
                'code': product.code,
            }
        
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """Remove a product from the cart"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update_quantity(self, product_id, quantity):
        """Update product quantity"""
        product_id = str(product_id)
        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]['quantity'] = quantity
            else:
                del self.cart[product_id]
            self.save()

    def clear(self):
        """Clear the cart"""
        self.session['cart'] = {}
        self.save()

    def save(self):
        """Save cart to session"""
        self.session.modified = True

    def __iter__(self):
        """Iterate over cart items"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['total_price'] = Decimal(str(item['price'])) * item['quantity']
            yield item

    def __len__(self):
        """Count total items in cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Get total cart price"""
        return sum(
            Decimal(str(item['price'])) * item['quantity']
            for item in self.cart.values()
        )

    def get_discount(self):
        """Calculate total discount"""
        return Decimal('0.00')

    def get_subtotal(self):
        """Get subtotal (total - discount)"""
        return self.get_total_price() - self.get_discount()
