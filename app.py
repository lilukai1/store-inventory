from peewee import *
import csv
from datetime import date, datetime

db = SqliteDatabase('inventory.db')


class Product(Model):
    class Meta:
        database = db

    product_id = PrimaryKeyField()
    product_name = CharField(max_length=50)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField()

    def __str__(self):
        return (f"{self.product_quantity} of {self.product_name} are in stock,"
                f" at ${self.product_price/100:.2f}.Last Updated: "
                f"{self.date_updated.strftime('%m/%d/%Y')}")

def load_data():
    """Writes products in inventory.csv to database"""
    with open("inventory.csv") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        # for row in rows[1:5]:
        for row in rows[1:]:
            Product.create(
                product_name = row[0], 
                product_quantity = row[2],
                product_price = clean_price(row[1]),
                date_updated = datetime.strptime(row[3],"%m/%d/%Y"),
                )



def backup_products():
    """Makes a backup of database to backup.csv"""
    all_product = Product.select()
    with open("backup.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = csv.DictWriter(csvfile,
            fieldnames = [
                'product_name',
                'product_price',
                'product_quantity',
                'date_updated'
                ])
        header.writeheader()
        for selected_product in all_product:
            writer.writerow([
                selected_product.product_name,
                (selected_product.product_price/100),
                selected_product.product_quantity,
                selected_product.date_updated
                ])
    print("Backup Complete.")


def main_menu():
    selections = """
    Options:
    V - View a Product. 
    A - Add a Product.
    B - Backup database.
    Q - Quit.
"""
    print(selections)
    get_selection()

def get_selection():
    """Main menu selection, hidden option of L to load data from
    inventory.csv"""

    selection = input("What would you like to do?  >>  \n")
    if selection.upper() == "Q":
        exit("Thanks, have a great day!")
    elif selection.upper() not in selection_dict.keys():
        print("Selection unavailable.  Available options are:")
        main_menu()
    else:
        menu_selector(selection.upper())

def clean_price(price):
    return price.strip("$").replace(".","")

def get_price():
    """Gets price for a product from the user, in order to enter it into database"""
    while True:
        try:
            price = int(input("Product price?  >>  \n"))
            if price < 0:
                raise
            break
        except:
            print("Price must be a whole, positive number. "
                "Enter in price in pennies.  IE-> $4.99 should be entered as 499.")
    return(price)

def menu_selector(argument):
    """Selector for the main menu, uses a dictionary to run the function"""
    func = selection_dict.get(argument)
    return func()

def get_product_quantity():
    """Gets in stock quantity from user to add new or update a product in database"""
    while True:
        try:
            qty = int(input("Product quantity in stock?  >>  \n"))
            if qty < 0:
                raise
            break
        except:
            print("Quantity must be a whole, positive number.")
    return qty
        
def add_product():
    """Option 'A', prompts user for product addition"""
    product_name = input("What is the product called? >>  \n")
    product = Product.get_or_none(Product.product_name == product_name)
    if product != None:
        print(f"{product_name} is already in the database. " 
            "Updating existing values...")
        product.product_price = get_price()
        product.product_quantity = get_product_quantity()
        product.date_updated = date.today()
        product.save()
    else:
        product_price = get_price()
        product_quantity = get_product_quantity()
        Product.get_or_create(
                    product_name = product_name, 
                    defaults={
                        'product_price' : product_price,
                        'date_updated' : date.today(), 
                        'product_quantity' : product_quantity
                        })    


def view_product():
    """Allows a view of a product by a known ID number.  Can use 'all' 
    in order to view every product in the database"""

    select = input("What is the product id?  >>  \n")
    if select == "all":
        all_product = Product.select()
        for selected_product in all_product:
            print(selected_product)
    else:
        try:
            selected_product = Product.get_by_id(select)
            print(selected_product)
        except DoesNotExist:
            print("No product with that ID.")

## https://jaxenter.com/implement-switch-case-statement-python-138315.html
#         
selection_dict = {
    "V" : view_product,
    "A" : add_product,
    "B" : backup_products,
    "L" : load_data,
}


if __name__ == "__main__":
    db.connect()
    db.create_tables([Product], safe=True)
    while True:
        main_menu()
