import tkinter as tk
from itertools import product

# =========================
# LOGIC HELPERS
# =========================
def implies(a, b):
    return (not a) or b

def equiv(a, b):
    return a == b

def normalize(expr):
    return (expr.replace("¬", " not ")
                .replace("∧", " and ")
                .replace("∨", " or ")
                .replace("→", " implies ")
                .replace("≡", " equiv "))

# =========================
# MAIN FUNCTION
# =========================
def generate():
    for w in table.winfo_children():
        w.destroy()
    explanation_box.delete("1.0", tk.END)

    expr = expr_entry.get()
    vars_ = list(dict.fromkeys(var_entry.get().replace(" ", "")))

    if not expr or not vars_:
        return

    py_expr = normalize(expr)
    n = len(vars_)

    # Header
    for c, v in enumerate(vars_):
        tk.Label(table, text=v, width=5, bg="#1f2933", fg="white",
                 font=("Consolas", 10, "bold"),
                 relief="solid").grid(row=0, column=c)

    tk.Label(table, text=expr, width=30, bg="#2563eb", fg="white",
             font=("Consolas", 10, "bold"),
             relief="solid").grid(row=0, column=n)

    results = []

    # Rows
    for r, values in enumerate(product([True, False], repeat=n), start=1):
        env = dict(zip(vars_, values))
        env.update({"implies": implies, "equiv": equiv})

        row_desc = f"Row {r}: "

        for c, val in enumerate(values):
            tk.Label(table,
                     text="T" if val else "F",
                     bg="#22c55e" if val else "#ef4444",
                     fg="black", width=5,
                     relief="solid").grid(row=r, column=c)
            row_desc += f"{vars_[c]}={'T' if val else 'F'} "

        try:
            res = eval(py_expr, {}, env)
            results.append(res)

            color = "#16a34a" if res else "#dc2626"
            tk.Label(table,
                     text="T" if res else "F",
                     bg=color, fg="white",
                     width=30,
                     font=("Consolas", 10, "bold"),
                     relief="solid").grid(row=r, column=n)

            if res:
                row_desc += "→ Expression is TRUE ✅\n"
            else:
                row_desc += "→ Expression is FALSE ❌ because condition failed\n"

        except:
            row_desc += "→ ERROR in expression\n"
            tk.Label(table,
                     text="ERR", bg="gray",
                     width=30,
                     relief="solid").grid(row=r, column=n)

        explanation_box.insert(tk.END, row_desc)

    # Classification
    if all(results):
        result_label.config(text="TAUTOLOGY: Always True", fg="#22c55e")
    elif not any(results):
        result_label.config(text="CONTRADICTION: Always False", fg="#ef4444")
    else:
        result_label.config(text="CONTINGENCY: Sometimes True, Sometimes False", fg="#facc15")

# =========================
# GUI (DARK MODE)
# =========================
root = tk.Tk()
root.title("Truth Table Generator – CS Demo")
root.geometry("1150x650")
root.configure(bg="#111827")

top = tk.Frame(root, bg="#111827")
top.pack(pady=10)

tk.Label(top, text="Variables:", fg="white", bg="#111827").grid(row=0, column=0)
var_entry = tk.Entry(top, width=10, bg="#1f2933", fg="white",
                     insertbackground="white")
var_entry.grid(row=0, column=1, padx=6)

tk.Label(top, text="Expression:", fg="white", bg="#111827").grid(row=1, column=0)
expr_entry = tk.Entry(top, width=45, bg="#1f2933", fg="white",
                      insertbackground="white")
expr_entry.grid(row=1, column=1, padx=6)

tk.Button(top, text="Generate Truth Table",
          command=generate,
          bg="#2563eb", fg="white",
          font=("Arial", 10, "bold"),
          width=25).grid(row=2, column=0, columnspan=2, pady=8)

result_label = tk.Label(root, text="", bg="#111827",
                        font=("Arial", 12, "bold"))
result_label.pack(pady=6)

table = tk.Frame(root, bg="#111827")
table.pack(pady=10)

# Explanation Box
tk.Label(root, text="Row-by-Row Explanation:",
         fg="white", bg="#111827",
         font=("Arial", 10, "bold")).pack(anchor="w", padx=20)

explanation_box = tk.Text(root, height=10, bg="#020617",
                          fg="#e5e7eb",
                          font=("Consolas", 9))
explanation_box.pack(fill="x", padx=20, pady=6)

root.mainloop()
