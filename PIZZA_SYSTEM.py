import tkinter as tk
from tkinter import messagebox

pizza_prices = {
    "Pepperoni": 299,
    "Sausage": 329,
    "Hawaiian": 269,
    "Mushroom": 349,
}

size_prices = {
    "Small": 30,
    "Medium": 80,
    "Large": 150,
}

topping_prices = {
    "Extra Cheese": 35,
    "Mushrooms": 45,
    "Olives": 40,
    "Bacon": 60,
}

BG = "#fff4e0"        
HEADER = "#1f5130"    
CARD = "#fffaf0"     
ACCENT = "#e8672a"   
TEXT = "#2b2b2b"
MUTED = "#6b6b6b"
RECEIPT_BG = "#1f2a24"
RECEIPT_FG = "#f4efe2"

window = tk.Tk()
window.title("Pizza Ordering System")
window.geometry("800x580")
window.minsize(720, 540)
window.configure(bg=BG)

pizza_var = tk.StringVar(value="Pepperoni")
size_var = tk.StringVar(value="Small")
quantity_var = tk.IntVar(value=1)
topping_vars = {t: tk.BooleanVar(value=False) for t in topping_prices}

header = tk.Frame(window, bg=HEADER)
header.pack(fill="x")
tk.Label(
    header,
    text="PIZZA ORDERING SYSTEM",
    font=("Arial", 18, "bold"),
    bg=HEADER,
    fg="white",
).pack(pady=(12, 0))
tk.Label(
    header,
    text="Build your pizza, then place your order",
    font=("Arial", 10),
    bg=HEADER,
    fg="#cfe3d4",
).pack(pady=(0, 12))

body = tk.Frame(window, bg=BG)
body.pack(fill="both", expand=True, padx=14, pady=14)
body.columnconfigure(0, weight=3)
body.columnconfigure(1, weight=2)
body.rowconfigure(0, weight=1)

form = tk.Frame(body, bg=CARD, padx=16, pady=12, highlightthickness=1,
                highlightbackground="#e3d6b8")
form.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
form.columnconfigure(0, weight=1)
form.columnconfigure(1, weight=1)


def section_label(text, row):
    tk.Label(
        form,
        text=text,
        font=("Arial", 11, "bold"),
        bg=CARD,
        fg=HEADER,
    ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 4))


def styled_choice(widget_class, parent, **kwargs):
    return widget_class(
        parent,
        bg=CARD,
        fg=TEXT,
        activebackground=CARD,
        activeforeground=ACCENT,
        selectcolor="white",
        font=("Arial", 10),
        anchor="w",
        **kwargs,
    )


section_label("Pizza Flavor", 0)
row = 1
for i, (flavor, price) in enumerate(pizza_prices.items()):
    styled_choice(
        tk.Radiobutton,
        form,
        text=f"{flavor}  -  ₱{price}",
        variable=pizza_var,
        value=flavor,
    ).grid(row=row + i // 2, column=i % 2, sticky="w")
row += 2

section_label("Pizza Size", row)
row += 1
size_frame = tk.Frame(form, bg=CARD)
size_frame.grid(row=row, column=0, columnspan=2, sticky="w")
for size, price in size_prices.items():
    styled_choice(
        tk.Radiobutton,
        size_frame,
        text=f"{size} (+₱{price})",
        variable=size_var,
        value=size,
    ).pack(side="left", padx=(0, 12))
row += 1

section_label("Extra Toppings", row)
row += 1
for i, (topping, price) in enumerate(topping_prices.items()):
    styled_choice(
        tk.Checkbutton,
        form,
        text=f"{topping} (+₱{price})",
        variable=topping_vars[topping],
    ).grid(row=row + i // 2, column=i % 2, sticky="w")
row += 2

section_label("Quantity", row)
row += 1
qty_frame = tk.Frame(form, bg=CARD)
qty_frame.grid(row=row, column=0, columnspan=2, sticky="w")


def change_quantity(delta):
    new_value = quantity_var.get() + delta
    if 1 <= new_value <= 50:
        quantity_var.set(new_value)


tk.Button(
    qty_frame, text="-", width=3, font=("Arial", 11, "bold"),
    bg=HEADER, fg="white", relief="flat",
    command=lambda: change_quantity(-1),
).pack(side="left")
tk.Label(
    qty_frame, textvariable=quantity_var, width=4,
    font=("Arial", 12, "bold"), bg=CARD, fg=TEXT,
).pack(side="left")
tk.Button(
    qty_frame, text="+", width=3, font=("Arial", 11, "bold"),
    bg=HEADER, fg="white", relief="flat",
    command=lambda: change_quantity(1),
).pack(side="left")
row += 1

live_price_label = tk.Label(
    form,
    font=("Arial", 12, "bold"),
    bg=CARD,
    fg=ACCENT,
)
live_price_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(16, 0))


def price_per_pizza():
    toppings_total = sum(
        topping_prices[t] for t, v in topping_vars.items() if v.get()
    )
    return pizza_prices[pizza_var.get()] + size_prices[size_var.get()] + toppings_total


def refresh_live_price(*_):
    live_price_label.config(text=f"Price per pizza: ₱{price_per_pizza():,.2f}")


pizza_var.trace_add("write", refresh_live_price)
size_var.trace_add("write", refresh_live_price)
for var in topping_vars.values():
    var.trace_add("write", refresh_live_price)
refresh_live_price()

summary = tk.Frame(body, bg=CARD, padx=12, pady=12, highlightthickness=1,
                   highlightbackground="#e3d6b8")
summary.grid(row=0, column=1, sticky="nsew")
summary.rowconfigure(1, weight=1)
summary.columnconfigure(0, weight=1)

tk.Label(
    summary,
    text="ORDER SUMMARY",
    font=("Arial", 12, "bold"),
    bg=CARD,
    fg=HEADER,
).grid(row=0, column=0, sticky="w", pady=(0, 6))

receipt_text = tk.Text(
    summary,
    height=12,
    width=30,
    font=("Consolas", 10),
    bg=RECEIPT_BG,
    fg=RECEIPT_FG,
    insertbackground="white",
    relief="flat",
    padx=8,
    pady=8,
)
receipt_text.grid(row=1, column=0, sticky="nsew")


def calculate_total():
    pizza = pizza_var.get()
    size = size_var.get()
    quantity = quantity_var.get()

    if not messagebox.askyesno(
        "Confirm Order", "Are you sure you want to place this order?"
    ):
        return

    pizza_price = pizza_prices[pizza]
    size_price = size_prices[size]
    selected_toppings = [t for t, v in topping_vars.items() if v.get()]
    per_pizza = price_per_pizza()
    total = per_pizza * quantity

    receipt_text.delete("1.0", tk.END)
    receipt_text.insert(tk.END, "===== ORDER RECEIPT =====\n\n")
    receipt_text.insert(tk.END, f"Flavor: {pizza} (₱{pizza_price})\n")
    receipt_text.insert(tk.END, f"Size:   {size} (+₱{size_price})\n")

    if selected_toppings:
        for topping in selected_toppings:
            receipt_text.insert(
                tk.END, f"+ {topping}: ₱{topping_prices[topping]}\n"
            )
    else:
        receipt_text.insert(tk.END, "No extra toppings\n")

    receipt_text.insert(tk.END, f"\nPrice per Pizza: ₱{per_pizza:,.2f}\n")
    receipt_text.insert(tk.END, f"Quantity: {quantity}\n")
    receipt_text.insert(tk.END, "-" * 26 + "\n")
    receipt_text.insert(tk.END, f"TOTAL: ₱{total:,.2f}\n")
    receipt_text.insert(tk.END, "\nThank you for ordering!\n")


def reset_order():
    pizza_var.set("Pepperoni")
    size_var.set("Small")
    quantity_var.set(1)
    for var in topping_vars.values():
        var.set(False)
    receipt_text.delete("1.0", tk.END)


button_frame = tk.Frame(summary, bg=CARD)
button_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
button_frame.columnconfigure(0, weight=2)
button_frame.columnconfigure(1, weight=1)

tk.Button(
    button_frame,
    text="PLACE ORDER",
    font=("Arial", 11, "bold"),
    bg=ACCENT,
    fg="white",
    relief="flat",
    command=calculate_total,
).grid(row=0, column=0, sticky="ew", padx=(0, 4), ipady=6)

tk.Button(
    button_frame,
    text="RESET",
    font=("Arial", 11, "bold"),
    bg=HEADER,
    fg="white",
    relief="flat",
    command=reset_order,
).grid(row=0, column=1, sticky="ew", padx=(4, 0), ipady=6)

window.mainloop()
