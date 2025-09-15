import tkinter as tk
from tkinter import ttk, messagebox

class PizzaOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lukes Pizzaria")
        self.root.configure(bg="#fff8e7")  # soft background color

        self.cart = []

        self.size_var = tk.StringVar(value="Medium")
        self.crust_var = tk.StringVar(value="Regular")
        self.sauce_var = tk.StringVar(value="Tomato")
        self.notes_var = tk.StringVar()
        self.qty_var = tk.IntVar(value=1)
        self.topping_vars = {}
        self.topping_amounts = {}

        self.create_customer_info_frame()
        self.create_pizza_builder_frame()
        self.create_cart_frame()

    def create_customer_info_frame(self):
        frame = tk.Frame(self.root, bg="#ffe6e6", bd=2, relief="ridge")
        frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(3, weight=1)

        tk.Label(frame, text="Name:", bg="#ffe6e6", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.name_entry = ttk.Entry(frame)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(frame, text="Phone:", bg="#ffe6e6", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky="w", padx=5, pady=3)
        self.phone_entry = ttk.Entry(frame)
        self.phone_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=3)

        tk.Label(frame, text="Order Type:", bg="#ffe6e6", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.order_type_var = tk.StringVar(value="Pickup")
        ttk.Radiobutton(frame, text="Pickup", variable=self.order_type_var, value="Pickup").grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(frame, text="Delivery", variable=self.order_type_var, value="Delivery").grid(row=1, column=2, sticky="w")

        tk.Label(frame, text="Address:", bg="#ffe6e6", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=3)
        self.address_entry = ttk.Entry(frame)
        self.address_entry.grid(row=2, column=1, columnspan=3, sticky="ew", padx=5, pady=3)

    def create_pizza_builder_frame(self):
        frame = tk.Frame(self.root, bg="#e6f7ff", bd=2, relief="ridge")
        frame.grid(row=1, column=0, padx=10, pady=5, sticky="n")
        frame.grid_columnconfigure(1, weight=1)


        tk.Label(frame, text="Size:", bg="#e6f7ff", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        for i, size in enumerate(["Small", "Medium", "Large"]):
            ttk.Radiobutton(frame, text=size, variable=self.size_var, value=size, command=self.update_price).grid(row=0, column=i+1, sticky="w")


        tk.Label(frame, text="Crust:", bg="#e6f7ff", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5)
        for i, crust in enumerate(["Thin", "Regular", "Deep Dish"]):
            ttk.Radiobutton(frame, text=crust, variable=self.crust_var, value=crust, command=self.update_price).grid(row=1, column=i+1, sticky="w")


        tk.Label(frame, text="Sauce:", bg="#e6f7ff", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=5)
        sauces = ["Tomato", "BBQ", "Alfredo", "Garlic Parmesan", "Pesto"]
        for i, sauce in enumerate(sauces):
            ttk.Radiobutton(frame, text=sauce, variable=self.sauce_var, value=sauce, command=self.update_price).grid(row=2, column=i+1, sticky="w")


        tk.Label(frame, text="Toppings:", bg="#e6f7ff", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", padx=5)
        toppings = [
            "Pepperoni", "Mushrooms", "Onions", "Sausage", "Bacon",
            "Extra cheese", "Black olives", "Green peppers", "Pineapple", "Spinach",
            "Tomatoes", "Garlic", "Ham", "Jalapeños", "Ground beef",
            "Chicken", "Red peppers", "Broccoli", "Artichokes", "Anchovies"
        ]
        amounts = ["Little", "Normal", "Extra"]

        for i, topping in enumerate(toppings):
            row = 4 + (i // 2)
            col = (i % 2) * 2
            var = tk.IntVar()
            chk = ttk.Checkbutton(frame, text=topping, variable=var, command=self.update_price)
            chk.grid(row=row, column=col, sticky="w", padx=2, pady=2)
            amt_var = tk.StringVar(value="Normal")
            opt = ttk.OptionMenu(frame, amt_var, "Normal", *amounts, command=lambda e=None: self.update_price())
            opt.grid(row=row, column=col + 1, sticky="w", padx=2, pady=2)
            opt.config(state="disabled")
            self.topping_vars[topping] = var
            self.topping_amounts[topping] = (amt_var, opt)


        tk.Label(frame, text="Special Notes:", bg="#e6f7ff", font=("Arial", 10, "bold")).grid(row=14, column=0, sticky="w", padx=5, pady=3)
        self.notes_entry = ttk.Entry(frame, textvariable=self.notes_var, width=35)
        self.notes_entry.grid(row=14, column=1, columnspan=3, sticky="ew", padx=5, pady=3)


        tk.Label(frame, text="Qty:", bg="#e6f7ff", font=("Arial", 10, "bold")).grid(row=15, column=0, sticky="w", padx=5, pady=3)
        self.qty_spinbox = ttk.Spinbox(frame, from_=1, to=100, textvariable=self.qty_var, width=5, command=self.update_price)
        self.qty_spinbox.grid(row=15, column=1, sticky="w", padx=5, pady=3)


        self.price_label = tk.Label(frame, text="Price: $0.00", font=("Arial", 12, "bold"), bg="#e6f7ff", fg="#b30000")
        self.price_label.grid(row=16, column=0, columnspan=3, pady=5)


        add_btn = tk.Button(frame, text="Add Pizza 🍕", bg="#ff9999", fg="white", font=("Arial", 10, "bold"), command=self.add_pizza)
        add_btn.grid(row=17, column=0, columnspan=3, pady=10)

        self.update_price()


        for topping, var in self.topping_vars.items():
            def toggle(var=var, topping=topping):
                amt_var, opt = self.topping_amounts[topping]
                if var.get():
                    opt.config(state="normal")
                else:
                    opt.config(state="disabled")
                    amt_var.set("Normal")
                self.update_price()
            var.trace_add("write", lambda *_, v=var, t=topping: toggle(v, t))

    def create_cart_frame(self):
        frame = tk.Frame(self.root, bg="#e6ffe6", bd=2, relief="ridge")
        frame.grid(row=1, column=1, padx=10, pady=5, sticky="n")

        self.cart_listbox = tk.Listbox(frame, width=100, height=20)
        self.cart_listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.total_label = tk.Label(frame, text="Total: $0.00", font=("Arial", 12, "bold"), bg="#e6ffe6", fg="#004d00")
        self.total_label.grid(row=1, column=0, columnspan=2, pady=5)

        remove_btn = tk.Button(frame, text="Remove Selected", bg="#b3b3ff", command=self.remove_selected)
        remove_btn.grid(row=2, column=0, pady=5, padx=5)

        checkout_btn = tk.Button(frame, text="Place Order ✅", bg="#66cc66", fg="white", font=("Arial", 10, "bold"), command=self.place_order)
        checkout_btn.grid(row=2, column=1, pady=5, padx=5)


    def calculate_pizza_price(self):
        base_prices = {"Small": 8, "Medium": 10, "Large": 12}
        crust_prices = {"Thin": 0, "Regular": 0, "Deep Dish": 2}

        price = base_prices[self.size_var.get()] + crust_prices[self.crust_var.get()]
        for topping, var in self.topping_vars.items():
            if var.get():
                amt_var, _ = self.topping_amounts[topping]
                amt = amt_var.get()
                if amt == "Little":
                    price += 1
                elif amt == "Normal":
                    price += 1.5
                elif amt == "Extra":
                    price += 2
        return price * self.qty_var.get()

    def update_price(self):
        self.price_label.config(text=f"Price: ${self.calculate_pizza_price():.2f}")

    def add_pizza(self):
        toppings = [f"{t} ({self.topping_amounts[t][0].get()})" for t, v in self.topping_vars.items() if v.get()]
        pizza = {
            "size": self.size_var.get(),
            "crust": self.crust_var.get(),
            "sauce": self.sauce_var.get(),
            "toppings": toppings,
            "notes": self.notes_entry.get(),
            "qty": self.qty_var.get(),
            "price": self.calculate_pizza_price(),
        }
        self.cart.append(pizza)
        self.update_cart()
        self.update_total()
        self.reset_builder()

    def reset_builder(self):
        self.size_var.set("Medium")
        self.crust_var.set("Regular")
        self.sauce_var.set("Tomato")
        for v in self.topping_vars.values():
            v.set(0)
        for amt_var, opt in self.topping_amounts.values():
            amt_var.set("Normal")
            opt.config(state="disabled")
        self.notes_entry.delete(0, tk.END)
        self.qty_var.set(1)
        self.update_price()

    def update_cart(self):
        self.cart_listbox.delete(0, tk.END)
        for item in self.cart:
            toppings = ", ".join(item["toppings"]) if item["toppings"] else "No toppings"
            notes_text = f" [Notes: {item['notes']}]" if item['notes'] else ""
            self.cart_listbox.insert(
                tk.END,
                f'{item["qty"]}x {item["size"]} {item["crust"]} Pizza with {item["sauce"]} Sauce ({toppings}){notes_text} - ${item["price"]:.2f}'
            )

    def update_total(self):
        total = sum(item["price"] for item in self.cart)
        self.total_label.config(text=f"Total: ${total:.2f}")

    def remove_selected(self):
        selected = self.cart_listbox.curselection()
        if selected:
            self.cart.pop(selected[0])
            self.update_cart()
            self.update_total()

    def place_order(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add at least one pizza before placing order.")
            return
        summary = f"Order for {self.name_entry.get()} ({self.phone_entry.get()})\nType: {self.order_type_var.get()}\n"
        if self.order_type_var.get() == "Delivery":
            summary += f"Address: {self.address_entry.get()}\n"
        summary += "\nPizzas:\n"
        for item in self.cart:
            toppings = ", ".join(item["toppings"]) if item["toppings"] else "No toppings"
            notes_text = f" [Notes: {item['notes']}]" if item['notes'] else ""
            summary += f'- {item["qty"]}x {item["size"]} {item["crust"]} Pizza with {item["sauce"]} Sauce ({toppings}){notes_text} - ${item["price"]:.2f}\n'
        summary += self.total_label.cget("text")
        messagebox.showinfo("Order Placed", summary)


        self.cart.clear()
        self.update_cart()
        self.update_total()
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.order_type_var.set("Pickup")
        self.reset_builder()

if __name__ == "__main__":
    root = tk.Tk()
    app = PizzaOrderApp(root)
    root.mainloop()
