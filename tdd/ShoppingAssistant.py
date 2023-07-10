class ShoppingAssistant():
    def __init__(self,  starting_balance):
        self.__balance = starting_balance 
        self.shopping_cart = []
        self.prices = {} 

    def increase_balance(self, amount):
        self.__balance += amount

    def add_items(self, new_items):
        self.shopping_cart.extend(new_items)

    def checkout(self):
        total = self._calculate_total()
        if self.__balance < total:
            raise Exception
        self.__balance -= total
        items, self.shopping_cart = self.shopping_cart, []
        return items
    
    def update_prices(self, **new_pirces):
        self.prices.update(new_pirces)
    
    def _calculate_total(self):
        return sum(self.prices.get(item, 0) for item in self.shopping_cart)