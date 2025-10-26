
class Product:

    def __init__(self, name: str, price: float, stock: int):
        self.name = name
        self.price = price
        self.stock = stock

    def __repr__(self):
        return f"{self.name} {self.price} {self.stock}"

    def update_stock(self, quantity: int) -> int:
        if self.stock + quantity >= 0:
            self.stock = self.stock + quantity
        else:
            print("вещей на складе не может быть меньше 0")
        return self.stock

class Order:

    def __init__(self):
        self.products: dict[Product, int] = {}

    def __repr__(self):
        return f"{self.products}"

    def add_product(self, product, quantity) -> None:
        if product.stock < quantity:
            print("на складе недостаточно товара")
            return
        else:
             if product in self.products:
                self.products[product] += quantity
             else:
                self.products[product] = quantity

        product.update_stock(-quantity)

    def calculate_total(self) -> float:
        res = 0
        for product, quantity in self.products.items():
            res = res + product.price * quantity
        return res

    def remove_product(self, product, quantity):
        if product not in self.products:
            print("этого товара нет в заказе")
            return
        if self.products[product] < quantity:
            print("в заказе недостаточно товара для удаления")
            return
        self.products[product] -= quantity
        product.update_stock(quantity)
        if self.products[product] == 0:
            self.products.pop(product)

    def return_product(self, product, quantity):
        if product not in self.products:
            print("этого товара нет в заказе")
            return
        if self.products[product] < quantity:
            print("вш заказе недостаточно товара для возврата")
            return
        self.products[product] -= quantity
        product.update_stock(quantity)

        if self.products[product] == 0:
            self.products.pop(product)
class Store:
    def __init__(self):
        self.products = []
    def __repr__(self):
        return f"{self.products}"

    def add_product(self, product: Product):
        for p in self.products:
            if p.name == product.name:
                p.stock = p.stock + product.stock
                break
        else:
            self.products.append(product)

    def list_products(self):
        return print(self.products)

    def create_order(self):
        return Order()