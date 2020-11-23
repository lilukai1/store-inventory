from peewee import *
import csv

from datetime import datetime

db = SqliteDatabase('inventory.db')


# Create your Product model
# Create a model called Product that the Peewee ORM will use to build the database. The Product model should have five attributes: product_id, product_name, product_quantity, product_price, and date_updated. Use PeeWee's built in primary_key functionality for the product_id field, so that each product will have an automatically generated unique identifier.


class Product(Model):
    class Meta:
        database = db

    product_id = PrimaryKeyField()
    product_name = CharField(max_length=50)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField()

    def __str__(self):
        return f"{self.product_id}, {self.product_name}, ${self.product_price/100:.2f}, {self.date_updated}"

def load_data():
    with open("inventory.csv") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        for row in rows[1:5]:
            Product.create(
                product_name = row[0], 
                product_quantity = row[2],
                product_price = clean_price(row[1]),
                date_updated = row[3],
                )

def backup_products():
    print("backup selected")
    all_product = Product.select()

    with open("inventory1.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # writer.writerows(all_product)
        for selected_product in all_product:
            # writer.writerow(f"{self.product_name}, ${self.product_price/100:.2f}, {self.date_updated}")
            writer.writerow([selected_product.product_name,(selected_product.product_price/100),selected_product.date_updated])

def main_menu():
    selections = """
    Options:
    V - View Product. 
    A - Add Product.
    B - Backup to database.
    Q - Quit.
"""
    print(selections)
    get_selection()

def get_selection():

    selection = input("What would you like to do?  >>  \n")
    if selection.upper() == "Q":
        exit("Thanks, have a great day!")
    elif selection.upper() not in selection_dict.keys():
        print("Selection unavailable.")
        main_menu()
    else:
        selector(selection.upper())

def clean_price(price):
    return price.strip("$").replace(".","")

def show_price(price):
    return price

def selector(argument):
    func = selection_dict.get(argument)
    return func()

def add_product():
    product_name = input("What is the product called? >>  \n")
    product_price = input("Price?  >>  \n")
    clean_price(product_price)
    date_updated = datetime.now()
    product_quantity = input("Product quantity in stock?  >>  \n")
    Product.create(product_name = product_name, product_price = clean_price(product_price),
                     date_updated = date_updated, product_quantity = product_quantity)
    

def view_product():
    select = input("What is the product id?  >>  \n")
    if select == "all":
        all_product = Product.select()
        for selected_product in all_product:
            print(selected_product)
    else:
        selected_product = Product.get_by_id(select, "No product with that ID.")
        print(selected_product)







## https://jaxenter.com/implement-switch-case-statement-python-138315.html
#         
selection_dict = {
    "V" : view_product,
    "A" : add_product,
    "B" : backup_products,
}


if __name__ == "__main__":
    db.connect()
    db.create_tables([Product], safe=True)
    # load_data()
    while True:
        main_menu()
