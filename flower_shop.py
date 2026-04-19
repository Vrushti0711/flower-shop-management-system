import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("System Login")
        self.root.geometry("400x350")
        self.root.configure(bg="#2c3e50")

        tk.Label(
            root,
            text="FLOWER SHOP LOGIN",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=30)

        tk.Label(root, text="Username:", fg="white", bg="#2c3e50").pack()
        self.user_entry = tk.Entry(root, font=("Arial", 11))
        self.user_entry.pack(pady=5)
        self.user_entry.insert(0, "admin")

        tk.Label(root, text="Password:", fg="white", bg="#2c3e50").pack()
        self.pass_entry = tk.Entry(root, show="*", font=("Arial", 11))
        self.pass_entry.pack(pady=5)
        self.pass_entry.insert(0, "admin123")

        tk.Button(
            root,
            text="Login",
            command=self.validate_login,
            bg="#27ae60",
            fg="white",
            width=15,
            font=("Arial", 11, "bold")
        ).pack(pady=25)

    def validate_login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Vrushti@07",
                database="flower_shop",
                charset="utf8",
                use_pure=True
            )
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            user = cursor.fetchone()
            conn.close()

            if user:
                self.root.destroy()
                main_root = tk.Tk()
                FlowerShopApp(main_root, username)
                main_root.mainloop()
            else:
                messagebox.showerror("Error", "Invalid username or password!")

        except Exception as e:
            messagebox.showerror("DB Error", f"Connection failed: {e}")


class FlowerShopApp:
    def __init__(self, root, current_user):
        self.root = root
        self.user = current_user
        self.root.title(f"Flower Shop Management - {self.user}")
        self.root.geometry("1150x720")

        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "Vrushti@07",
            "database": "flower_shop",
            "charset": "utf8",
            "use_pure": True
        }

        self.setup_ui()
        self.refresh_all()
        messagebox.showinfo("Welcome", f"Welcome {self.user} to Flower Shop System")

    def connect_db(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except Exception as e:
            messagebox.showerror("Error", f"Connection Error: {e}")
            return None

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#34495e", pady=10)
        header.pack(fill="x")
        tk.Label(
            header,
            text="FLOWER SHOP MANAGEMENT DASHBOARD",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#34495e"
        ).pack()
        tk.Label(
            header,
            text=f"User: {self.user}",
            fg="#bdc3c7",
            bg="#34495e"
        ).pack()

        # Business Overview
        stats_frame = tk.LabelFrame(self.root, text=" Business Overview ", padx=15, pady=10)
        stats_frame.pack(fill="x", padx=20, pady=10)

        self.rev_val = tk.StringVar(value="Rs. 0.00")
        self.order_val = tk.StringVar(value="0")

        tk.Label(stats_frame, text="Total Revenue:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        tk.Label(stats_frame, textvariable=self.rev_val, font=("Arial", 14, "bold"), fg="#27ae60").grid(row=0, column=1, padx=10)

        tk.Label(stats_frame, text="Total Orders:", font=("Arial", 12)).grid(row=0, column=2, padx=20)
        tk.Label(stats_frame, textvariable=self.order_val, font=("Arial", 14, "bold"), fg="#2980b9").grid(row=0, column=3, padx=10)

        # Search
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(search_frame, text="Search Flower:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.load_inventory_data())
        tk.Entry(search_frame, textvariable=self.search_var, width=40).pack(side="left", padx=10)
        tk.Button(search_frame, text="Clear Search", command=lambda: self.search_var.set("")).pack(side="left")

        # Table
        self.tree = ttk.Treeview(
            self.root,
            columns=("ID", "Name", "Category", "Price", "Stock", "Supplier"),
            show="headings"
        )

        cols = {
            "ID": 60,
            "Name": 220,
            "Category": 150,
            "Price": 100,
            "Stock": 100,
            "Supplier": 180
        }

        for c, w in cols.items():
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="center")

        self.tree.pack(expand=True, fill="both", padx=20, pady=10)
        self.tree.tag_configure("low", background="#ffcccc")

        # Buttons
        btn_frame = tk.Frame(self.root, pady=20)
        btn_frame.pack()

        tk.Button(btn_frame, text=" Add Flower", command=self.add_flower_window, bg="#27ae60", fg="white", width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text=" Update Stock", command=self.update_stock, bg="#f39c12", fg="white", width=15).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text=" Delete Flower", command=self.delete_flower, bg="#c0392b", fg="white", width=15).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text=" QUICK SELL", command=self.quick_sell, bg="#8e44ad", fg="white", width=15, font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text=" Customers", command=self.open_customers_window, bg="#16a085", fg="white", width=15).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text=" Logout", command=self.logout, bg="#7f8c8d", fg="white", width=10).grid(row=0, column=5, padx=5)

    def refresh_all(self):
        self.load_inventory_data()
        self.update_dashboard()

    def load_inventory_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            query = """
                SELECT flower_id, flower_name, category, price, quantity, supplier_name
                FROM flowers
                WHERE flower_name LIKE %s
            """
            cursor.execute(query, (f"%{self.search_var.get()}%",))
            for row in cursor.fetchall():
                tag = ("low",) if row[4] < 10 else ()
                self.tree.insert("", "end", values=row, tags=tag)
            conn.close()

    def show_low_stock(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = self.connect_db()
        if conn:
           cursor = conn.cursor()

        cursor.execute("""
            SELECT flower_id, flower_name, category, price, quantity, supplier_name
            FROM flowers
            WHERE quantity < 10
        """)

        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row, tags=("low",))

        conn.close()


    def update_dashboard(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()

            try:
                cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM payments")
                revenue = cursor.fetchone()[0]
                self.rev_val.set(f"Rs. {revenue:,.2f}")
            except:
                self.rev_val.set("Rs. 0.00")

            try:
                cursor.execute("SELECT COUNT(*) FROM orders")
                orders = cursor.fetchone()[0]
                self.order_val.set(str(orders))
            except:
                self.order_val.set("0")

            conn.close()

    def add_flower_window(self):
        top = tk.Toplevel(self.root)
        top.title("Add New Flower")
        top.geometry("320x420")

        fields = ["Name", "Category", "Price", "Stock", "Supplier"]
        entries = {}

        for f in fields:
            tk.Label(top, text=f).pack()
            e = tk.Entry(top)
            e.pack(pady=5)
            entries[f] = e

        def save():
            try:
                conn = self.connect_db()
                cursor = conn.cursor()
                sql = """
                    INSERT INTO flowers (flower_name, category, price, quantity, supplier_name)
                    VALUES (%s, %s, %s, %s, %s)
                """
                vals = (
                    entries["Name"].get(),
                    entries["Category"].get(),
                    float(entries["Price"].get()),
                    int(entries["Stock"].get()),
                    entries["Supplier"].get()
                )
                cursor.execute(sql, vals)
                conn.commit()
                conn.close()
                top.destroy()
                self.refresh_all()
                messagebox.showinfo("Success", "Flower added successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Check inputs: {e}")

        tk.Button(top, text="Save Flower", command=save, bg="#27ae60", fg="white").pack(pady=20)

    def update_stock(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showwarning("Wait", "Select a flower!")

        f_id = self.tree.item(selected)["values"][0]
        new_s = simpledialog.askinteger("Stock", "Enter new stock level:")
        if new_s is not None:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE flowers SET quantity = %s WHERE flower_id = %s", (new_s, f_id))
            conn.commit()
            conn.close()
            self.refresh_all()

    def delete_flower(self):
        selected = self.tree.selection()
        if not selected:
            return

        f_id = self.tree.item(selected)["values"][0]
        if messagebox.askyesno("Confirm", "Delete this flower permanently?"):
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM flowers WHERE flower_id = %s", (f_id,))
            conn.commit()
            conn.close()
            self.refresh_all()

    def quick_sell(self):
        selected = self.tree.selection()
        if not selected:
          return messagebox.showwarning("Wait", "Select a flower to sell!")

        f_id, f_name, _, f_price, f_stock, _ = self.tree.item(selected)["values"]
        qty = simpledialog.askinteger("Sell", f"Qty for {f_name}?")

        if qty and qty > 0 and qty <= f_stock:
           conn = self.connect_db()
           try:
               conn.start_transaction()
               cursor = conn.cursor()
               total = float(f_price) * qty

               cursor.execute(
                  "INSERT INTO orders (customer_id, order_date, total_amount) VALUES (%s, CURDATE(), %s)",
                   (1, total)
              )
               order_id = cursor.lastrowid

               cursor.execute(
                  "INSERT INTO order_details (order_id, flower_id, quantity, subtotal) VALUES (%s, %s, %s, %s)",
                  (order_id, f_id, qty, total)
              )   

               cursor.execute(
                "INSERT INTO payments (order_id, payment_date, amount, payment_method) VALUES (%s, CURDATE(), %s, %s)",
                (order_id, total, "Cash")
              )

               cursor.execute(
                 "UPDATE flowers SET quantity = quantity - %s WHERE flower_id = %s",
                 (qty, f_id)
              )

               conn.commit()

               bill_text = f"""
========= FLOWER SHOP BILL =========
Flower: {f_name}
Quantity: {qty}
Price per unit: Rs. {f_price}

TOTAL: Rs. {total}
===================================
"""
               messagebox.showinfo("Invoice", bill_text)

           except Exception as e:
               conn.rollback()
               messagebox.showerror("Error", str(e))

           finally:
              conn.close()
              self.refresh_all()

        else:
         messagebox.showerror("Error", "Insufficient stock or invalid quantity")
    def open_customers_window(self):
        top = tk.Toplevel(self.root)
        top.title("Customer Management")
        top.geometry("850x500")

        tree = ttk.Treeview(
            top,
            columns=("ID", "Name", "Phone", "Address"),
            show="headings"
        )

        tree.heading("ID", text="ID")
        tree.heading("Name", text="Customer Name")
        tree.heading("Phone", text="Phone")
        tree.heading("Address", text="Address")

        tree.column("ID", width=60)
        tree.column("Name", width=220)
        tree.column("Phone", width=150)
        tree.column("Address", width=300)

        tree.pack(expand=True, fill="both", padx=20, pady=20)

        def load_customers():
            for item in tree.get_children():
                tree.delete(item)

            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT customer_id, customer_name, phone, address FROM customers")
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            conn.close()

        def add_customer():
            name = simpledialog.askstring("Customer", "Enter customer name:")
            phone = simpledialog.askstring("Phone", "Enter phone number:")
            address = simpledialog.askstring("Address", "Enter address:")

            if not name:
                return messagebox.showwarning("Warning", "Customer name is required")

            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO customers (customer_name, phone, address) VALUES (%s, %s, %s)",
                (name, phone, address)
            )
            conn.commit()
            conn.close()
            load_customers()

        def delete_customer():
            selected = tree.selection()
            if not selected:
                return messagebox.showwarning("Warning", "Select a customer first")

            c_id = tree.item(selected)["values"][0]
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE customer_id = %s", (c_id,))
            conn.commit()
            conn.close()
            load_customers()

        btns = tk.Frame(top)
        btns.pack(pady=10)

        tk.Button(btns, text="Add Customer", command=add_customer, bg="#27ae60", fg="white").grid(row=0, column=0, padx=10)
        tk.Button(btns, text="Delete Customer", command=delete_customer, bg="#c0392b", fg="white").grid(row=0, column=1, padx=10)
        tk.Button(btns, text="Refresh", command=load_customers, bg="#3498db", fg="white").grid(row=0, column=2, padx=10)

        load_customers()

    def logout(self):
        self.root.destroy()
        login_root = tk.Tk()
        LoginWindow(login_root)
        login_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()