# Will ask user if each table supported in the application should
# be reloaded into sqlite table with data in csv files

# this function is intended for application startup and development

# updates to tables after go-live should be done in Django's admin interface

# tables must first be created using Django before uploading

# csv files must match table layout and cofiguration

import csv, sqlite3
db_file = 'db.sqlite3'

# main - ask user for each table load
def main():

    db = sqlite3.connect(db_file);

    if (not db):
        print(f"Cannot connet to database {db_file}")
        return

    print("WARNING: Each table load will erase all exting data.")

    # sizes table
    print("ERASE & RELOAD 'sizes' table? (Y/N): ", end="")
    response=get_Y_or_N()
    if response is 'Y':
        delete_table_data("orders_sizes", db)
        load_table("sizes.csv", "orders_sizes", db, 2)

    # toppings (menu option)
    print("ERASE & RELOAD 'toppings' (menu options) table? (Y/N): ", end="")
    response=get_Y_or_N()
    if response is 'Y':
        delete_table_data("orders_toppings", db)
        load_table("toppings.csv", "orders_toppings", db, 2)

    # menu_categories table
    print("ERASE & RELOAD 'menu_cateogries' table? (Y/N): ", end="")
    response=get_Y_or_N()
    if response is 'Y':
        delete_table_data("orders_menu_categories", db)
        load_table("menu_categories.csv", "orders_menu_categories", db, 2)

    # sub_addons table
    print("ERASE & RELOAD 'sub_addons' table? (Y/N): ", end="")
    response=get_Y_or_N()
    if response is 'Y':
        delete_table_data("orders_sub_addons", db)
        load_table("sub_addons.csv", "orders_sub_addons", db, 5)

    # menu_items table
    print("ERASE & RELOAD 'menu_items' table? (Y/N): ", end="")
    response=get_Y_or_N()
    if response is 'Y':
        delete_table_data("orders_menu_items", db)
        load_table("menu_items.csv", "orders_menu_items", db, 7)

    # pizza_toppings table
    print("ERASE & RELOAD 'pizza_toppings' table? (Y/N): ", end="")
    response=get_Y_or_N()
    if response is 'Y':
        delete_table_data("orders_pizza_toppings", db)
        load_table("pizza_toppings.csv", "orders_pizza_toppings", db, 3)

    print("ERASE 'Order and Order_line' tables? (Y/N): ", end="")
    response=get_Y_or_N()
    if response is 'Y':
        delete_table_data("orders_order", db)
        delete_table_data("orders_order_line", db)

    print("ERASE 'Order_status' table? (Y/N): ", end="")
    response=get_Y_or_N()
    if response is 'Y':
        delete_table_data("orders_order_status", db)



def delete_table_data(table, db):
    sql = f"DELETE FROM {table}"
    cur = db.cursor()
    cur.execute(sql)
    db.commit()


def load_table(csv_file, table, db, cols):
    f = open_file(csv_file)
    if f is None:
        return
    reader = csv.reader(f)

    values = '(?'

    c = 1
    while (c < cols):
        values = values + ',?'
        c += 1

    values = values + ')'

    i = 0
    for line in reader:
        if i>0:
            print(f"Loading record: {i}: {line}")
            db.execute(f"INSERT INTO {table} VALUES {values}", line)
        i += 1
    print("...Done")
    print("Committing to database...")
    db.commit()
    print("Data committed.  Data load complete.")

    f.close()


def load_addons(reader):
    i = 0
    for row in reader:
        if i>0:
            print(f"Loading record: {i}: {row}")
            Sub_addons.objects.get_or_create(
                id = row[0],
                add_on = row[1],
                size = row[2],
                available = row[3],
                price = row[4])
        i += 1




# get a Y or N response from command line
# returns False if something else is typed
def get_Y_or_N():
    response=input()
    print("\r")
    if response=='Y' or response=='N':
        return response
    else:
        return False

# open file based on filename of file in working directory
def open_file(file_name):
    f = open(file_name)
    if f is None:
        print(f"File '{csv_file}' not found.")
        return None
    else:
        print(f"Loading data from {file_name}...")
        return f

if __name__ == '__main__': main()
