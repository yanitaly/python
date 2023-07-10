from ShoppingAssistant import ShoppingAssistant
import unittest 

class TestShoppingAssistant(unittest.TestCase):
    INITIAL_BALANCE = 100
    PRICE_LIST= {
        'banana'        :   0.5,
        'peanutbutter'  :   5.0,
        'jelly'         :   2.0,
        'rice'          :   1.0
    }

    def setUp(self):
        '''initialize the class '''
        self.sa = ShoppingAssistant(self.INITIAL_BALANCE)

    def tearDown(self):
        '''not necessary in this case, just an example'''
        del self.sa 

    def test_increase_balance(self): # name needs to start with "test_xxx"
        '''increase balance with certain amount should increase the __balance attribute'''
        self.sa.increase_balance(50)
        cur_bal = self.sa._ShoppingAssistant__balance
        self.assertEqual(cur_bal, self.INITIAL_BALANCE + 50)

    def test_add_items(self):
        '''should be able to add item in cart'''
        self.sa.add_items(['banana', 'melon'])
        cart = self.sa.shopping_cart
        self.assertEqual(cart, ['banana', 'melon'])

    def test_checkout(self):
        '''checkout out should return all items currently in shopping cart'''
        self.sa.add_items(['banana', 'melon'])
        items = self.sa.checkout()
        self.assertEqual(self.sa.shopping_cart, [])

    def test_checkout_reduce_balance(self):
        '''checkout should reduce balance accordingly'''
        self.sa.update_prices(banana=5, melon=5)
        self.sa.add_items(['banana','melon'])
        items = self.sa.checkout()

        cur_bal = self.sa._ShoppingAssistant__balance
        item_total = 10
        self.assertEqual(cur_bal, self.INITIAL_BALANCE - item_total)

    def test_checkout_insufficient_balance(self):
        '''checkout attempt with insufficient balance'''
        cur_bal = self.sa._ShoppingAssistant__balance
        self.sa.update_prices(banana=5, melon=5)
        self.sa.add_items(['banana',]*100)
        with self.assertRaises(Exception):
            self.sa.checkout()
        self.assertEqual(cur_bal, self.INITIAL_BALANCE)       

    def test_update_price(self):
        '''update prices should copy the new prices to the prices dict '''
        new_prices = {
        'banana' :   5,
        'melon'  :   2,
        'chocolate' :3
        }
        self.sa.update_prices(**new_prices)
        self.assertEqual(self.sa.prices, new_prices)

if __name__ == '__main__':
    unittest.main()