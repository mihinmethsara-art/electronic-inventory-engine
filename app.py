import json
import urllib.request
import sqlite3
from urllib.error import URLError

class InventoryEngine:
    def __init__(self,db_name="electronic_items.db"):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()


    def add_items():

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS electronic_items(
        Date_Time TEXT,
        Item_Name TEXT,
        Quantity INTEGER,
        Price_of_a_item REAL,
        Total_in_USD REAL,
        Total_in_LKR REAL
        )
        """)


        from datetime import datetime
        now_full = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        a1= now_full
        a2 = input("Enter an item name:")
        a3 = int(input("Enter a quantity:"))

        while True:
            d_r_url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = urllib.request.urlopen(d_r_url)
            data = json.loads(response.read())
            lrk_rate = data["rates"]["LKR"]


            a4 = int(input("Enter a price in $:"))
            if a4 >0:
                a5 = a3 * a4

                try:
                    a6 = lrk_rate * a5

                except URLError:
                    print("Getting average price as 1$=300LKR")
                    a6 = 300 * a5

                cursor.execute("INSERT INTO electronic_items VALUES (?,?,?,?,?,?)", (a1, a2, a3, a4, a5, a6))
                connection.commit()
                return
            else:
                print("Enter a valid price")

    def watch_inventory():
        connection = sqlite3.connect('electricitems.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM electronic_items")
        inventory = cursor.fetchall()
        print(inventory)
while True:
    print("===================")
    print("=====USER MENU=====")
    print("===================")
    print("1. Add an item")
    print("2. Watch an item")
    print("3. Exit")
    choice=int(input("Enter your choice:"))

    if choice == 1:
        add_items()

    elif choice == 2:
        watch_inventory()

    elif choice == 3:
        print("Exiting...")
        break