import sqlite3
from datetime import datetime
import json
import urllib.request

class EiEngine:
    def __init__(self,db_name="e_items.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.setup_table()      #metana awul

    def search_items(self):
        item=input("Enter item name: ").strip()
        self.cursor.execute("SELECT * FROM e_items WHERE LOWER(Item_Name)=LOWER(?)",(item,))
        result = self.cursor.fetchall()
        if len(result) == 0:
            print("❌ No item found!")
        else:
            for dt, name, qty, unit_usd, tot_usd, tot_lkr in result:
                print(f" [{dt}]  {name} | Qty: {qty} | Unit: ${unit_usd} | Total: ${tot_usd} (Rs. {tot_lkr})")





    def setup_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS e_items(
                Date_Time TEXT,
                Item_Name TEXT,
                Quantity INTEGER,
                Price_of_a_item REAL,
                Total_in_USD REAL,
                Total_in_LKR REAL
            )
            """)
        self.connection.commit()


    def get_live_lkr_rate(self):
        d_r_url = "https://api.exchangerate-api.com/v4/latest/USD"
        try:
            response = urllib.request.urlopen(d_r_url,timeout=5) #metana awul
            data = json.loads(response.read())
            return data['rates']["LKR"]
        except  Exception:
            print("⚠️ Internet Error! Getting average price as 1$ = 300 LKR")
            return 300            #metana awl

    def add_items(self):
        now_full = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        a1=now_full
        a2= input("Enter an item name: ").strip()

        while True:
            try:
                a3 = int(input("Enter a quantity: "))
                a4 = float(input("Enter a price in $: "))

                if a3 > 0 and a4 > 0:
                    break
                else:
                    print("❌ Quantity and Price must be greater than 0!")

            except ValueError:
                print("❌ Invalid input! Please enter numbers only.")

        calc_total = lambda x,y:round(x*y,2)
        lkr_rate = self.get_live_lkr_rate()

        a5 = calc_total(a3,a4)
        a6 = calc_total(a5,lkr_rate)

        self.cursor.execute(
                "INSERT INTO e_items Values(?,?,?,?,?,?)",
                        (a1,a2,a3,a4,a5,a6)
        )
        self.connection.commit()
        print(f"✅ Saved! {a2} (x{a3}) | Total: ${a5} (Rs. {a6} @ Rate: {lkr_rate})")

    def watch_inventory(self):
        self.cursor.execute("SELECT * FROM e_items")
        inventory = self.cursor.fetchall()

        print("\n================  INVENTORY RECORDS ================")
        if len(inventory) == 0:
            print("📭 Inventory is currently empty!")
            return

        for dt, name, qty, unit_usd, tot_usd, tot_lkr in inventory:
            print(f"🕒 [{dt}] 📦 {name} | Qty: {qty} | Unit: ${unit_usd} | Total: ${tot_usd} (Rs. {tot_lkr})")

        lkr_totals = [row[5] for row in inventory]
        high_value_items = [row[1] for row in inventory if row[5] > 50000]
        low_stock_items = [row[1] for row in inventory if row[2] < 5]           #79 idan 81 wenakan awul

        print("\n---------------- 📈 BUSINESS ANALYTICS ----------------")
        print(f" Total Item Records (n)      : {len(inventory)}")
        print(f" Grand Total Value (∑ LKR)   : Rs. {sum(lkr_totals):.2f}")
        print(f" High Value Stock (>50k LKR) : {high_value_items}")
        print(f" Low Stock Alert (Qty < 5)   : {low_stock_items}")
        print("=======================================================\n")


    def close_connection(self):
        self.connection.close()

engine = EiEngine()

while True:
    print("\n===================")
    print("=====USER MENU=====")
    print("===================")
    print("1. Add an item")
    print("2. Watch inventory & Analytics")
    print("3. Search an item")
    print("4. Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("❌ Please enter a valid number (1, 2, or 3)!")
        continue

    if choice == 1:
        engine.add_items()
    elif choice == 2:
        engine.watch_inventory()
    elif choice == 3:
        engine.search_items()
    elif choice == 4:
        engine.close_connection()
        print("Exiting... Database closed safely! 👋")
        break
    else:
        print("❌ Invalid choice! Please choose 1, 2,3, or 4.")

