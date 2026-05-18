import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import psycopg2

# ── Database Connection ────────────────────────────────────────────────────────
# TODO: Update these credentials to match your PostgreSQL setup
DB_CONFIG = {
    "host":     "127.0.0.1",
    "port":     5432,
    "dbname":   "MyMetropolitanTheaterDatabase",   # change to your actual DB name
    "user":     "postgres",                # change to your DB user
    "password":  "AKOSICYAN69",            # change to your DB password
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# ── DB helpers: Personnel ─────────────────────────────────────────────────────
def db_load_departments():
    """Returns list of (department_id, name) from DB."""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT department_id, name FROM Department ORDER BY name;")
        rows = cur.fetchall()
        cur.close(); conn.close()
        return rows
    except Exception as e:
        messagebox.showerror("DB Error", f"Could not load departments:\n{e}")
        return []

def db_load_staff_by_department(department_id):
    """Returns list of staff dicts for the given department_id."""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            SELECT s.staff_id, s.name, s.type, d.name AS dept_name
            FROM   Staff s
            JOIN   Department d ON d.department_id = s.department_id
            WHERE  s.department_id = %s
            ORDER  BY s.name;
        """, (department_id,))
        rows = cur.fetchall()
        cur.close(); conn.close()
        return [
            {"id": f"STAFF-{r[0]:02d}", "name": r[1],
             "role": r[2], "dept": r[3], "staff_id": r[0]}
            for r in rows
        ]
    except Exception as e:
        messagebox.showerror("DB Error", f"Could not load staff:\n{e}")
        return []

def db_load_work_logs(staff_id):
    """Returns work-log rows for a given staff_id."""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            SELECT p.date, wl.staff_id, wl.hours_worked
            FROM   Work_Log wl
            JOIN   Performance p ON p.performance_id = wl.performance_id
            WHERE  wl.staff_id = %s
            ORDER  BY p.date;
        """, (staff_id,))
        rows = cur.fetchall()
        cur.close(); conn.close()
        return [(str(r[0]), f"STAFF-{r[1]:02d}", str(r[2])) for r in rows]
    except Exception as e:
        messagebox.showerror("DB Error", f"Could not load work logs:\n{e}")
        return []

def db_load_entertainment_performers():
    """Returns hourly staff from the Entertainment department."""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            SELECT s.staff_id, s.name, h.hourly_rate, h.famous_level
            FROM   Staff s
            JOIN   Hourly h     ON h.staff_id     = s.staff_id
            JOIN   Department d ON d.department_id = s.department_id
            WHERE  d.name = 'Entertainment'
            ORDER  BY s.name;
        """)
        rows = cur.fetchall()
        cur.close(); conn.close()
        return rows
    except Exception as e:
        messagebox.showerror("DB Error", f"Could not load entertainment performers:\n{e}")
        return []

def db_save_department_change(staff_id, new_dept_id):
    """Updates a staff member's department in the DB."""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            "UPDATE Staff SET department_id = %s WHERE staff_id = %s;",
            (new_dept_id, staff_id)
        )
        conn.commit()
        cur.close(); conn.close()
        messagebox.showinfo("Saved", "Department updated successfully.")
    except Exception as e:
        messagebox.showerror("DB Error", f"Could not save changes:\n{e}")

# ── DB helpers: Customers ─────────────────────────────────────────────────────
def db_load_customers():
    """Returns all customers as a list of dicts from DB."""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            SELECT customer_id, name, email, mobile_number
            FROM   Customer
            ORDER  BY name;
        """)
        rows = cur.fetchall()
        cur.close(); conn.close()
        return [
            {"customer_id": r[0], "name": r[1],
             "email": r[2], "mobile": r[3]}
            for r in rows
        ]
    except Exception as e:
        messagebox.showerror("DB Error", f"Could not load customers:\n{e}")
        return []

def db_load_transaction_history(customer_id):
    """Returns ticket/transaction rows for a given customer_id."""
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            SELECT
                t.ticket_number,
                t.sale_date,
                p.title              AS production,
                tr.amount,
                t.status
            FROM   Ticket t
            JOIN   Transactions tr     ON tr.ticket_id           = t.ticket_id
            JOIN   Performance_Seat ps ON ps.performance_seat_id  = t.performance_seat_id
            JOIN   Performance perf    ON perf.performance_id     = ps.performance_id
            JOIN   Production p        ON p.production_id          = perf.production_id
            WHERE  t.customer_id = %s
            ORDER  BY t.sale_date DESC;
        """, (customer_id,))
        rows = cur.fetchall()
        cur.close(); conn.close()
        return [
            (r[0], str(r[1]), r[2], f"Php {r[3]:,.2f}", r[4])
            for r in rows
        ]
    except Exception as e:
        messagebox.showerror("DB Error", f"Could not load history:\n{e}")
        return []

# ── Colors ────────────────────────────────────────────────────────────────────
BG_MAIN      = "#B0B0B0"
BG_TOPBAR    = "#1E1E1E"
BG_SIDEBAR   = "#9A9A9A"
BG_SIDEBAR_H = "#888888"
BG_ACTIVE    = "#C8C8C8"
BG_PANEL     = "#F0F0F0"
BG_INPUT     = "#E8E8E8"
BG_INPUT_HOV = "#DEDEDE"
BG_LIST      = "#F5F5F5"
BG_DETAIL    = "#F0F0F0"
BG_SEARCH    = "#E8E8E8"
BG_TABLE_ROW = "#FFFFFF"
BG_TABLE_ALT = "#F5F5F5"
BG_RECEIPT   = "#F8F8F8"
BG_STAGE     = "#D0D0D0"
BG_CARD      = "#F0F0F0"
SEAT_AVAIL   = "#2ECC40"
SEAT_AVAIL_H = "#27AE34"
SEAT_SOLD    = "#CC1111"
SEAT_SOLD_H  = "#AA0000"
SEAT_SEL     = "#F39C12"
SEAT_SEL_H   = "#D4850A"
ACCENT       = "#CC1111"
ACCENT_HOV   = "#AA0000"
TEXT_LIGHT   = "#FFFFFF"
TEXT_DARK    = "#1A1A1A"
TEXT_MID     = "#555555"
TEXT_MUTED   = "#AAAAAA"
DIVIDER      = "#DDDDDD"

FONT   = "Helvetica"
RADIUS = 10

# ── All nav items ─────────────────────────────────────────────────────────────
ALL_NAV = [
    ("🎭", "Catalog"),
    ("🎟",  "Sales"),
    ("👤", "Personnel"),
    ("💰", "Finances"),
    ("👥", "Customers"),
]

SALES_NAV = [
    ("🎟", "Sales"),
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    canvas.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,  style="pieslice", **kw)
    canvas.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,  style="pieslice", **kw)
    canvas.create_rectangle(x1+r, y1,   x2-r, y2,   **kw)
    canvas.create_rectangle(x1,   y1+r, x2,   y2-r, **kw)

def make_canvas_btn(parent, text, command, w=80, h=32,
                    fill=ACCENT, fill_hov=ACCENT_HOV,
                    bg=BG_MAIN, fg=TEXT_LIGHT, font_size=10):
    c = tk.Canvas(parent, width=w, height=h, bg=bg, highlightthickness=0, bd=0)
    def draw(color):
        c.delete("all")
        rounded_rect(c, 0, 0, w, h, 5, fill=color, outline=color)
        c.create_text(w//2, h//2, text=text, fill=fg, font=(FONT, font_size, "bold"))
    draw(fill)
    c.bind("<Enter>",    lambda _: draw(fill_hov))
    c.bind("<Leave>",    lambda _: draw(fill))
    c.bind("<Button-1>", lambda _: command())
    c.config(cursor="hand2")
    return c

def center_on(win, parent, w, h):
    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width()  - w) // 2
    y = parent.winfo_y() + (parent.winfo_height() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB BUILDERS — each function receives a parent frame and builds content in it
# ══════════════════════════════════════════════════════════════════════════════

# ── CATALOG TAB ───────────────────────────────────────────────────────────────
def build_catalog_tab(parent):
    productions = [
        {
            "name": "Hamlet",
            "start": "January 10, 2026",
            "end":   "January 30, 2026",
            "showtimes": [
                ("January 10", "7:00 PM", 30, 30, "Open"),
                ("January 11", "7:00 PM", 30, 30, "Open"),
                ("January 12", "2:00 PM", 30, 30, "Open"),
            ],
        },
        {
            "name": "The Phantom of the Opera",
            "start": "January 15, 2026",
            "end":   "February 28, 2026",
            "showtimes": [
                ("January 15", "7:00 PM", 30, 30, "Open"),
                ("January 16", "7:00 PM", 30, 30, "Open"),
                ("January 17", "3:00 PM", 30, 30, "Open"),
            ],
        },
    ]

    content = tk.Frame(parent, bg=BG_MAIN)
    content.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(content, text="Productions and Scheduling",
             fg=ACCENT, bg=BG_MAIN, font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))

    panels_row = tk.Frame(content, bg=BG_MAIN)
    panels_row.pack(fill="both", expand=True)

    # Left panel
    left_panel = tk.Frame(panels_row, bg=BG_LIST, width=310)
    left_panel.pack(side="left", fill="y", padx=(0, 14))
    left_panel.pack_propagate(False)

    search_frame = tk.Frame(left_panel, bg=BG_SEARCH)
    search_frame.pack(fill="x", padx=10, pady=(10, 6))
    tk.Label(search_frame, text="🔍", bg=BG_SEARCH, fg=TEXT_MID, font=("Arial", 11)).pack(side="left", padx=(6, 2), pady=6)
    search_entry = tk.Entry(search_frame, font=(FONT, 11), bg=BG_SEARCH, fg=TEXT_MID, relief="flat", bd=0)
    search_entry.insert(0, "Search")
    search_entry.pack(side="left", fill="x", expand=True, pady=6, padx=4)

    def sf_in(_):
        if search_entry.get() == "Search":
            search_entry.delete(0, "end"); search_entry.config(fg=TEXT_DARK)
    def sf_out(_):
        if search_entry.get() == "":
            search_entry.insert(0, "Search"); search_entry.config(fg=TEXT_MID)
    search_entry.bind("<FocusIn>", sf_in)
    search_entry.bind("<FocusOut>", sf_out)

    tk.Frame(left_panel, bg=DIVIDER, height=1).pack(fill="x", padx=10)

    list_frame = tk.Frame(left_panel, bg=BG_LIST)
    list_frame.pack(fill="both", expand=True, padx=4, pady=4)

    right_panel = tk.Frame(panels_row, bg=BG_DETAIL)
    right_panel.pack(side="left", fill="both", expand=True)

    def show_production_detail(prod):
        for w in right_panel.winfo_children():
            w.destroy()
        container = tk.Frame(right_panel, bg=BG_DETAIL)
        container.pack(fill="both", expand=True, padx=24, pady=24)
        tk.Label(container, text=f"Production Title: {prod['name']}",
                 fg=ACCENT, bg=BG_DETAIL, font=(FONT, 17, "bold"), anchor="w").pack(anchor="w")
        tk.Label(container, text=f"Season: {prod['start']} – {prod['end']}",
                 fg=TEXT_MID, bg=BG_DETAIL, font=(FONT, 11), anchor="w").pack(anchor="w", pady=(2, 18))
        table = tk.Frame(container, bg=BG_DETAIL)
        table.pack(fill="x")
        headers = ["Date", "Time", "Total Seats", "Seats Available", "Status"]
        col_widths = [16, 12, 14, 18, 10]
        header_row = tk.Frame(table, bg=BG_DETAIL)
        header_row.pack(fill="x", pady=(0, 4))
        for col, (h, cw) in enumerate(zip(headers, col_widths)):
            tk.Label(header_row, text=h, fg=ACCENT, bg=BG_DETAIL,
                     font=(FONT, 11, "bold"), width=cw, anchor="w").grid(row=0, column=col, padx=4, pady=6, sticky="w")
        tk.Frame(table, bg=DIVIDER, height=1).pack(fill="x")
        rows_frame = tk.Frame(table, bg=BG_DETAIL)
        rows_frame.pack(fill="x")
        for r_idx, (date, time, total, avail, status) in enumerate(prod["showtimes"]):
            row_bg = BG_TABLE_ROW if r_idx % 2 == 0 else BG_TABLE_ALT
            row_frame = tk.Frame(rows_frame, bg=row_bg)
            row_frame.pack(fill="x")
            tk.Frame(row_frame, bg=DIVIDER, height=1).pack(fill="x")
            data_row = tk.Frame(row_frame, bg=row_bg)
            data_row.pack(fill="x")
            for col, (val, cw) in enumerate(zip([date, time, str(total), str(avail), status], col_widths)):
                tk.Label(data_row, text=val, fg=TEXT_DARK, bg=row_bg,
                         font=(FONT, 11), width=cw, anchor="w").grid(row=0, column=col, padx=4, pady=10, sticky="w")

    selected_item = [None]
    def make_list_item(idx, prod):
        name, ds, de = prod["name"], prod["start"], prod["end"]
        ds_short = ds.split(",")[0].replace("January", "Jan").replace("February", "Feb")
        de_short = de.split(",")[0].replace("January", "Jan").replace("February", "Feb")
        label_text = f"{idx}. {name} ({ds_short}–{de_short})"
        if len(label_text) > 44:
            label_text = label_text[:41] + "..."
        item = tk.Label(list_frame, text=label_text, bg=BG_LIST, fg=TEXT_DARK,
                        font=(FONT, 11), anchor="w", cursor="hand2", padx=10, pady=8)
        item.pack(fill="x")
        def on_select(_):
            for w in list_frame.winfo_children():
                w.config(bg=BG_LIST)
            item.config(bg="#E0E0E0")
            selected_item[0] = item
            show_production_detail(prod)
        item.bind("<Button-1>", on_select)
        item.bind("<Enter>", lambda _: item.config(bg="#E8E8E8") if item.cget("bg") != "#E0E0E0" else None)
        item.bind("<Leave>", lambda _: item.config(bg=BG_LIST)   if item.cget("bg") != "#E0E0E0" else None)

    for i, prod in enumerate(productions, 1):
        make_list_item(i, prod)

    btn_row = tk.Frame(content, bg=BG_MAIN)
    btn_row.pack(anchor="w", pady=(10, 0))
    for lbl in ["EDIT", "ADD", "DELETE"]:
        make_canvas_btn(btn_row, lbl, lambda: None, w=72, h=30, bg=BG_MAIN).pack(side="left", padx=(0, 8))

    placeholder = tk.Frame(right_panel, bg=BG_DETAIL)
    placeholder.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(placeholder, text="Select a production from the list to manage\nshowtimes or click 'Add' to create a season.",
             fg=TEXT_MUTED, bg=BG_DETAIL, font=(FONT, 13), justify="center").pack()


# ── SALES TAB ─────────────────────────────────────────────────────────────────
def build_sales_tab(parent):
    productions_list = [
        "Hamlet – Jan 10, 7:00 PM",
        "Hamlet – Jan 11, 7:00 PM",
        "The Phantom of the Opera – Jan 15, 7:00 PM",
        "The Phantom of the Opera – Jan 16, 7:00 PM",
    ]

    selected_seats  = []
    seat_buttons    = {}
    seat_states     = {}

    SW, SH = 46, 36

    content = tk.Frame(parent, bg=BG_MAIN)
    content.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(content, text="Box Office (Ticketing)",
             fg=ACCENT, bg=BG_MAIN, font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))

    main_row = tk.Frame(content, bg=BG_MAIN)
    main_row.pack(fill="both", expand=True)

    left_col = tk.Frame(main_row, bg=BG_PANEL)
    left_col.pack(side="left", fill="both", expand=True, padx=(0, 14))

    prod_header = tk.Frame(left_col, bg=BG_PANEL)
    prod_header.pack(fill="x", padx=16, pady=(14, 8))
    tk.Label(prod_header, text="Production", bg=BG_PANEL, fg=TEXT_DARK, font=(FONT, 12, "bold")).pack(anchor="w")

    production_var = tk.StringVar(value="Select")

    receipt_seat_var = tk.StringVar(value="Seat(s): —")
    receipt_prod_var = tk.StringVar(value="Production: —")

    def update_receipt():
        seats_txt = ", ".join(selected_seats) if selected_seats else "—"
        receipt_seat_var.set(f"Seat(s): {seats_txt}")
        prod = production_var.get()
        receipt_prod_var.set(f"Production: {prod if prod != 'Select' else '—'}")

    prod_menu = ttk.Combobox(prod_header, textvariable=production_var,
                             values=productions_list, state="readonly", font=(FONT, 11), width=34)
    prod_menu.pack(anchor="w", pady=(4, 0))
    prod_menu.bind("<<ComboboxSelected>>", lambda _: update_receipt())

    seat_area = tk.Frame(left_col, bg=BG_PANEL)
    seat_area.pack(fill="both", expand=True, padx=16, pady=(4, 16))

    stage_frame = tk.Frame(seat_area, bg=BG_STAGE, height=38)
    stage_frame.pack(fill="x", pady=(0, 18))
    stage_frame.pack_propagate(False)
    tk.Label(stage_frame, text="STAGE", bg=BG_STAGE, fg=TEXT_DARK, font=(FONT, 13, "bold")).place(relx=0.5, rely=0.5, anchor="center")

    def make_seat(row_frame, label):
        seat_states[label] = "available"
        c = tk.Canvas(row_frame, width=SW, height=SH, bg=BG_PANEL, highlightthickness=0, bd=0, cursor="hand2")

        def color_for(s):
            if s == "sold":     return SEAT_SOLD, SEAT_SOLD_H
            if s == "selected": return SEAT_SEL,  SEAT_SEL_H
            return SEAT_AVAIL, SEAT_AVAIL_H

        def draw(hover=False):
            s = seat_states.get(label, "available")
            normal, hov = color_for(s)
            col = hov if hover else normal
            c.delete("all")
            rounded_rect(c, 1, 1, SW-1, SH-1, 5, fill=col, outline=col)
            c.create_text(SW//2, SH//2, text=label, fill=TEXT_LIGHT, font=(FONT, 8, "bold"))

        def on_click(_):
            s = seat_states.get(label, "available")
            if s == "sold": return
            if s == "available":
                seat_states[label] = "selected"
                if label not in selected_seats: selected_seats.append(label)
            else:
                seat_states[label] = "available"
                if label in selected_seats: selected_seats.remove(label)
            draw()
            update_receipt()

        c.bind("<Enter>",    lambda _: draw(hover=True))
        c.bind("<Leave>",    lambda _: draw(hover=False))
        c.bind("<Button-1>", on_click)
        draw()
        seat_buttons[label] = c
        return c

    BG_ROW = BG_PANEL

    def add_seat_row(labels, row_label=None):
        row = tk.Frame(seat_area, bg=BG_ROW)
        row.pack(pady=4)
        if row_label:
            tk.Label(row, text=row_label, bg=BG_ROW, fg=TEXT_MID, font=(FONT, 10), width=2).pack(side="left")
        for lbl in labels:
            make_seat(row, lbl).pack(side="left", padx=3)
        if row_label:
            tk.Label(row, text=row_label, bg=BG_ROW, fg=TEXT_MID, font=(FONT, 10), width=2).pack(side="left")

    add_seat_row(["A1","A2","A3","A4"], "A")

    row_b = tk.Frame(seat_area, bg=BG_ROW); row_b.pack(pady=4)
    tk.Label(row_b, text=" ", bg=BG_ROW, width=2).pack(side="left")
    make_seat(row_b, "B1").pack(side="left", padx=3)
    tk.Label(row_b, text="B", bg=BG_ROW, fg=TEXT_MID, font=(FONT, 10), width=2).pack(side="left")
    for lbl in ["B2","B3","B4","B5"]: make_seat(row_b, lbl).pack(side="left", padx=3)
    tk.Label(row_b, text="B", bg=BG_ROW, fg=TEXT_MID, font=(FONT, 10), width=2).pack(side="left")
    make_seat(row_b, "B6").pack(side="left", padx=3)

    for row_lbl, left_seats, right_seats in [("C", ["C1","C2"], ["C3","C4","C5","C6"], ), ("D", ["D1","D2"], ["D3","D4","D5","D6"])]:
        row = tk.Frame(seat_area, bg=BG_ROW); row.pack(pady=4)
        for lbl in left_seats: make_seat(row, lbl).pack(side="left", padx=3)
        tk.Label(row, text=row_lbl, bg=BG_ROW, fg=TEXT_MID, font=(FONT, 10), width=2).pack(side="left")
        for lbl in right_seats: make_seat(row, lbl).pack(side="left", padx=3)
        tk.Label(row, text=row_lbl, bg=BG_ROW, fg=TEXT_MID, font=(FONT, 10), width=2).pack(side="left")
        extra = "C7" if row_lbl == "C" else "D7"
        extra2 = "C8" if row_lbl == "C" else "D8"
        for lbl in [extra, extra2]: make_seat(row, lbl).pack(side="left", padx=3)

    add_seat_row(["E1","E2","E3","E4"], "E")

    legend = tk.Frame(seat_area, bg=BG_ROW)
    legend.pack(anchor="w", pady=(12, 0))
    for color, label in [(SEAT_AVAIL, "Available"), (SEAT_SOLD, "Sold"), (SEAT_SEL, "Selected")]:
        dot = tk.Canvas(legend, width=18, height=18, bg=BG_ROW, highlightthickness=0)
        dot.pack(side="left", padx=(0, 4))
        dot.create_rectangle(2, 2, 16, 16, fill=color, outline=color)
        tk.Label(legend, text=label, bg=BG_ROW, fg=TEXT_DARK, font=(FONT, 10)).pack(side="left", padx=(0, 14))

    # Receipt panel
    receipt_panel = tk.Frame(main_row, bg=BG_RECEIPT, width=240)
    receipt_panel.pack(side="left", fill="y")
    receipt_panel.pack_propagate(False)

    def label_receipt(text, bold=False, size=9, fg=TEXT_DARK, pady=0):
        tk.Label(receipt_panel, text=text, bg=BG_RECEIPT, fg=fg,
                 font=(FONT, size, "bold" if bold else "normal"),
                 justify="center", wraplength=210).pack(pady=pady)

    def divider_receipt():
        tk.Label(receipt_panel, text="- " * 22, bg=BG_RECEIPT, fg=DIVIDER, font=(FONT, 7)).pack()

    tk.Frame(receipt_panel, height=18, bg=BG_RECEIPT).pack()
    label_receipt("My Metropolitan Theater", bold=True, size=10)
    label_receipt("OFFICIAL RECEIPT", size=9, fg=TEXT_MID)
    tk.Frame(receipt_panel, height=6, bg=BG_RECEIPT).pack()
    label_receipt("Transaction ID: #TXN-0001")
    label_receipt("Date: May 10, 2026")
    label_receipt("Staff: Sales Agent")
    tk.Frame(receipt_panel, height=4, bg=BG_RECEIPT).pack()
    divider_receipt()
    label_receipt("CUSTOMER DETAILS", bold=True, size=9, fg=TEXT_MID)
    divider_receipt()
    tk.Frame(receipt_panel, height=4, bg=BG_RECEIPT).pack()
    label_receipt("Name: Juan Dela Cruz")
    label_receipt("Email: juan@email.com")
    label_receipt("Mobile: 0912-345-6789")
    tk.Frame(receipt_panel, height=4, bg=BG_RECEIPT).pack()
    divider_receipt()
    label_receipt("TICKET INFORMATION", bold=True, size=9, fg=TEXT_MID)
    divider_receipt()
    tk.Frame(receipt_panel, height=4, bg=BG_RECEIPT).pack()
    label_receipt("Ticket No: TKT-1025")
    tk.Label(receipt_panel, textvariable=receipt_prod_var, bg=BG_RECEIPT, fg=TEXT_DARK,
             font=(FONT, 9), justify="center", wraplength=210).pack()
    label_receipt("Performance: May 20, 2026 at 7:00 PM")
    tk.Label(receipt_panel, textvariable=receipt_seat_var, bg=BG_RECEIPT, fg=TEXT_DARK,
             font=(FONT, 9), justify="center", wraplength=210).pack()
    label_receipt("Status: Paid")
    tk.Frame(receipt_panel, height=4, bg=BG_RECEIPT).pack()
    divider_receipt()
    label_receipt("PAYMENT SUMMARY", bold=True, size=9, fg=TEXT_MID)
    divider_receipt()
    tk.Frame(receipt_panel, height=4, bg=BG_RECEIPT).pack()
    label_receipt("Payment Method: Cash")
    label_receipt("Total Amount: ₱1,500.00")


# ── PERSONNEL TAB ─────────────────────────────────────────────────────────────
def build_personnel_tab(parent):

    content = tk.Frame(parent, bg=BG_MAIN)
    content.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(content, text="Staff and Payroll", fg=ACCENT, bg=BG_MAIN,
             font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))

    main_row = tk.Frame(content, bg=BG_MAIN)
    main_row.pack(fill="both", expand=True)

    # ── Left panel: Employee Directory ────────────────────────────────────────
    left_panel = tk.Frame(main_row, bg=BG_PANEL, width=270)
    left_panel.pack(side="left", fill="y", padx=(0, 12))
    left_panel.pack_propagate(False)

    tk.Label(left_panel, text="Employee Directory", fg=TEXT_DARK, bg=BG_PANEL,
             font=(FONT, 12, "bold")).pack(anchor="w", padx=16, pady=(16, 8))

    # ── Search bar (functional — live search) ─────────────────────────────────
    search_frame = tk.Frame(left_panel, bg=BG_INPUT)
    search_frame.pack(fill="x", padx=16, pady=(0, 12))
    tk.Label(search_frame, text="🔍", bg=BG_INPUT, fg=TEXT_MID,
             font=("Arial", 10)).pack(side="left", padx=6, pady=6)
    search_entry = tk.Entry(search_frame, font=(FONT, 10), bg=BG_INPUT,
                            fg=TEXT_MID, relief="flat", bd=0)
    search_entry.insert(0, "Search")
    search_entry.pack(side="left", fill="x", expand=True, pady=6)

    def sf_in(_):
        if search_entry.get() == "Search":
            search_entry.delete(0, "end"); search_entry.config(fg=TEXT_DARK)
    def sf_out(_):
        if search_entry.get() == "":
            search_entry.insert(0, "Search"); search_entry.config(fg=TEXT_MID)
    search_entry.bind("<FocusIn>",  sf_in)
    search_entry.bind("<FocusOut>", sf_out)

    tk.Label(left_panel, text="Departments", fg=TEXT_DARK, bg=BG_PANEL,
             font=(FONT, 11, "bold")).pack(anchor="w", padx=16, pady=(0, 8))

    dir_canvas = tk.Canvas(left_panel, bg=BG_PANEL, highlightthickness=0, bd=0)
    dir_scroll  = ttk.Scrollbar(left_panel, orient="vertical", command=dir_canvas.yview)
    dir_canvas.configure(yscrollcommand=dir_scroll.set)
    dir_scroll.pack(side="right", fill="y")
    dir_canvas.pack(side="left", fill="both", expand=True)

    dir_inner = tk.Frame(dir_canvas, bg=BG_PANEL)
    dir_win   = dir_canvas.create_window((0, 0), window=dir_inner, anchor="nw")

    def on_dir_cfg(_):
        dir_canvas.configure(scrollregion=dir_canvas.bbox("all"))
        dir_canvas.itemconfig(dir_win, width=dir_canvas.winfo_width())
    dir_inner.bind("<Configure>", on_dir_cfg)
    dir_canvas.bind("<Configure>", lambda e: dir_canvas.itemconfig(dir_win, width=e.width))

    # ── Right panel ───────────────────────────────────────────────────────────
    right_panel = tk.Frame(main_row, bg=BG_MAIN)
    right_panel.pack(side="left", fill="both", expand=True)

    placeholder = tk.Frame(right_panel, bg=BG_MAIN)
    placeholder.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(placeholder, text="Select an employee from the directory\nto view their details.",
             fg=TEXT_MUTED, bg=BG_MAIN, font=(FONT, 13), justify="center").pack()

    selected_emp_row = [None]
    selected_emp_lbl = [None]

    # ── Show employee detail (right panel) ────────────────────────────────────
    def show_employee(emp):
        for w in right_panel.winfo_children():
            w.destroy()

        rsc    = tk.Canvas(right_panel, bg=BG_MAIN, highlightthickness=0, bd=0)
        sb     = ttk.Scrollbar(right_panel, orient="vertical", command=rsc.yview)
        rsc.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        rsc.pack(side="left", fill="both", expand=True)
        inner  = tk.Frame(rsc, bg=BG_MAIN)
        win_id = rsc.create_window((0, 0), window=inner, anchor="nw")

        def on_cfg(_):
            rsc.configure(scrollregion=rsc.bbox("all"))
            rsc.itemconfig(win_id, width=rsc.winfo_width())
        inner.bind("<Configure>", on_cfg)
        rsc.bind("<Configure>", lambda e: rsc.itemconfig(win_id, width=e.width))

        # Card 1 — Employee info + Department dropdown (DB-connected)
        card1 = tk.Frame(inner, bg=BG_PANEL)
        card1.pack(fill="x", pady=(0, 10))

        top_row = tk.Frame(card1, bg=BG_PANEL)
        top_row.pack(fill="x", padx=20, pady=(16, 4))

        name_col = tk.Frame(top_row, bg=BG_PANEL)
        name_col.pack(side="left", fill="x", expand=True)
        tk.Label(name_col, text=emp["name"], fg=TEXT_DARK, bg=BG_PANEL,
                 font=(FONT, 15, "bold"), anchor="w").pack(anchor="w")
        tk.Label(name_col, text=emp["role"], fg=TEXT_MID,  bg=BG_PANEL,
                 font=(FONT, 11), anchor="w").pack(anchor="w")

        # Department dropdown — loaded from DB
        dept_col = tk.Frame(top_row, bg=BG_PANEL)
        dept_col.pack(side="right")
        tk.Label(dept_col, text="Department", fg=TEXT_DARK, bg=BG_PANEL,
                 font=(FONT, 10, "bold")).pack(anchor="e")

        dept_rows   = db_load_departments()
        dept_names  = [r[1] for r in dept_rows]
        dept_id_map = {r[1]: r[0] for r in dept_rows}

        dept_var   = tk.StringVar(value=emp["dept"])
        dept_combo = ttk.Combobox(dept_col, textvariable=dept_var,
                                  values=dept_names,
                                  state="readonly", font=(FONT, 10), width=18)
        dept_combo.set(emp["dept"])
        dept_combo.pack(anchor="e", pady=(4, 8))

        def save_dept():
            chosen = dept_var.get()
            if chosen in dept_id_map:
                db_save_department_change(emp["staff_id"], dept_id_map[chosen])
            else:
                messagebox.showwarning("Warning", "Please select a valid department.")

        make_canvas_btn(dept_col, "Save Changes", save_dept,
                        w=130, h=30, bg=BG_PANEL).pack(anchor="e")

        info_row = tk.Frame(card1, bg=BG_PANEL)
        info_row.pack(fill="x", padx=20, pady=(8, 16))
        id_col = tk.Frame(info_row, bg=BG_PANEL)
        id_col.pack(side="left", padx=(0, 60))
        tk.Label(id_col, text="ID",      fg=TEXT_DARK, bg=BG_PANEL, font=(FONT, 10, "bold")).pack(anchor="w")
        tk.Label(id_col, text=emp["id"], fg=TEXT_DARK, bg=BG_PANEL, font=(FONT, 11)).pack(anchor="w")
        di_col = tk.Frame(info_row, bg=BG_PANEL)
        di_col.pack(side="left")
        tk.Label(di_col, text="Department",  fg=TEXT_DARK, bg=BG_PANEL, font=(FONT, 10, "bold")).pack(anchor="w")
        tk.Label(di_col, text=emp["dept"],   fg=TEXT_DARK, bg=BG_PANEL, font=(FONT, 11)).pack(anchor="w")

        # Card 2 — Payroll info (pay type from DB staff type)
        card2 = tk.Frame(inner, bg=BG_PANEL)
        card2.pack(fill="x", pady=(0, 10))
        tk.Label(card2, text="Payroll Information", fg=TEXT_DARK, bg=BG_PANEL,
                 font=(FONT, 13, "bold")).pack(anchor="w", padx=20, pady=(16, 10))
        tk.Frame(card2, bg=DIVIDER, height=1).pack(fill="x", padx=20)
        pay_row = tk.Frame(card2, bg=BG_PANEL)
        pay_row.pack(fill="x", padx=20, pady=(14, 16))
        pt_col = tk.Frame(pay_row, bg=BG_PANEL)
        pt_col.pack(side="left", padx=(0, 30))
        tk.Label(pt_col, text="Pay Type", fg=TEXT_DARK, bg=BG_PANEL,
                 font=(FONT, 10, "bold")).pack(anchor="w")
        pay_var   = tk.StringVar(value=emp.get("role", "Select"))
        pay_combo = ttk.Combobox(pt_col, textvariable=pay_var,
                                 values=["Full_Time", "Hourly", "Commissioned"],
                                 state="readonly", font=(FONT, 10), width=14)
        pay_combo.set(emp.get("role", "Select"))
        pay_combo.pack(anchor="w", pady=(6, 0))

        # Card 2b — Entertainment performer roster (shown only for Entertainment dept)
        if emp["dept"] == "Entertainment":
            card_ent = tk.Frame(inner, bg=BG_PANEL)
            card_ent.pack(fill="x", pady=(0, 10))
            tk.Label(card_ent, text="Entertainment — Performer Roster",
                     fg=TEXT_DARK, bg=BG_PANEL,
                     font=(FONT, 13, "bold")).pack(anchor="w", padx=20, pady=(16, 10))
            tk.Frame(card_ent, bg=DIVIDER, height=1).pack(fill="x", padx=20)
            th_row = tk.Frame(card_ent, bg=BG_PANEL)
            th_row.pack(fill="x", padx=20, pady=(8, 2))
            for col_text, col_w in [("Name", 24), ("Hourly Rate", 14), ("Famous Level", 14)]:
                tk.Label(th_row, text=col_text, fg=ACCENT, bg=BG_PANEL,
                         font=(FONT, 10, "bold"), width=col_w, anchor="w").pack(side="left")
            tk.Frame(card_ent, bg=DIVIDER, height=1).pack(fill="x", padx=20)
            performers = db_load_entertainment_performers()
            for i, (sid, pname, rate, lvl) in enumerate(performers):
                row_bg = TEXT_LIGHT if i % 2 == 0 else BG_TABLE_ALT
                rw = tk.Frame(card_ent, bg=row_bg)
                rw.pack(fill="x", padx=20)
                for val, cw in [(pname, 24), (f"₱{rate:.2f}/hr", 14), (str(lvl), 14)]:
                    tk.Label(rw, text=val, fg=TEXT_DARK, bg=row_bg,
                             font=(FONT, 10), width=cw, anchor="w").pack(side="left", pady=8)
                tk.Frame(card_ent, bg=DIVIDER, height=1).pack(fill="x", padx=20)
            tk.Frame(card_ent, height=10, bg=BG_PANEL).pack()

        # Card 3 — Time Tracking from DB
        card3 = tk.Frame(inner, bg=BG_PANEL)
        card3.pack(fill="x", pady=(0, 10))
        tk.Label(card3, text="Time Tracking", fg=TEXT_DARK, bg=BG_PANEL,
                 font=(FONT, 13, "bold")).pack(anchor="w", padx=20, pady=(16, 10))
        tk.Frame(card3, bg=DIVIDER, height=1).pack(fill="x", padx=20)
        th_row = tk.Frame(card3, bg=BG_PANEL)
        th_row.pack(fill="x", padx=20, pady=(6, 2))
        for col_text, col_w in [("Date", 14), ("Staff ID", 16), ("Hours Worked", 16)]:
            tk.Label(th_row, text=col_text, fg=ACCENT, bg=BG_PANEL,
                     font=(FONT, 10, "bold"), width=col_w, anchor="w").pack(side="left")
        tk.Frame(card3, bg=DIVIDER, height=1).pack(fill="x", padx=20)

        logs = db_load_work_logs(emp["staff_id"])
        for i, (date, sid, hrs) in enumerate(logs):
            row_bg = TEXT_LIGHT if i % 2 == 0 else BG_TABLE_ALT
            rw = tk.Frame(card3, bg=row_bg)
            rw.pack(fill="x", padx=20)
            for val, cw in [(date, 14), (sid, 16), (hrs, 16)]:
                tk.Label(rw, text=val, fg=TEXT_DARK, bg=row_bg,
                         font=(FONT, 10), width=cw, anchor="w").pack(side="left", pady=8)
            tk.Frame(card3, bg=DIVIDER, height=1).pack(fill="x", padx=20)
        tk.Frame(card3, height=12, bg=BG_PANEL).pack()

    # ── Build accordion from DB ───────────────────────────────────────────────
    def build_accordion(search_query=""):
        for w in dir_inner.winfo_children():
            w.destroy()

        dept_rows = db_load_departments()
        q = search_query.strip().lower()

        for dept_id, dept_name in dept_rows:
            staff_list = db_load_staff_by_department(dept_id)

            if q:
                staff_list = [e for e in staff_list
                              if q in e["name"].lower()
                              or q in e["id"].lower()
                              or q in e["dept"].lower()]

            if q and not staff_list:
                continue

            wrapper  = tk.Frame(dir_inner, bg=BG_PANEL)
            wrapper.pack(fill="x", pady=2, padx=8)
            dept_row = tk.Frame(wrapper, bg=BG_INPUT, cursor="hand2")
            dept_row.pack(fill="x")
            dept_lbl = tk.Label(dept_row, text=dept_name, bg=BG_INPUT, fg=TEXT_DARK,
                                font=(FONT, 10), anchor="w")
            dept_lbl.pack(side="left", padx=8, pady=8, fill="x", expand=True)
            arrow = tk.Label(dept_row, text="∨", bg=BG_INPUT, fg=TEXT_MID, font=(FONT, 10))
            arrow.pack(side="right", padx=8)
            emp_container = tk.Frame(wrapper, bg=BG_PANEL)
            is_open = [False]

            def toggle(ec=emp_container, a=arrow, flag=is_open):
                flag[0] = not flag[0]
                if flag[0]:
                    ec.pack(fill="x"); a.config(text="∧")
                else:
                    ec.pack_forget();  a.config(text="∨")

            if q and staff_list:
                emp_container.pack(fill="x")
                arrow.config(text="∧")
                is_open[0] = True

            for emp_data in staff_list:
                e = emp_data
                emp_row = tk.Frame(emp_container, bg=BG_PANEL, cursor="hand2")
                emp_row.pack(fill="x")
                emp_lbl = tk.Label(emp_row, text=f"  • {e['name']}", bg=BG_PANEL,
                                   fg=TEXT_DARK, font=(FONT, 9), anchor="w")
                emp_lbl.pack(side="left", padx=12, pady=5, fill="x", expand=True)

                def on_click(_, emp=e, er=emp_row, el=emp_lbl):
                    if selected_emp_row[0]: selected_emp_row[0].config(bg=BG_PANEL)
                    if selected_emp_lbl[0]: selected_emp_lbl[0].config(bg=BG_PANEL)
                    er.config(bg="#E0E0E0"); el.config(bg="#E0E0E0")
                    selected_emp_row[0] = er; selected_emp_lbl[0] = el
                    show_employee(emp)

                for w in (emp_row, emp_lbl):
                    w.bind("<Button-1>", on_click)
                    w.bind("<Enter>", lambda _, r=emp_row, l=emp_lbl:
                        (r.config(bg="#E8E8E8"), l.config(bg="#E8E8E8"))
                        if r != selected_emp_row[0] else None)
                    w.bind("<Leave>", lambda _, r=emp_row, l=emp_lbl:
                        (r.config(bg=BG_PANEL), l.config(bg=BG_PANEL))
                        if r != selected_emp_row[0] else None)

            for w in (dept_row, dept_lbl, arrow):
                w.bind("<Button-1>", lambda _, t=toggle: t())
                w.bind("<Enter>",  lambda _, r=dept_row, l=dept_lbl, a=arrow:
                    (r.config(bg=BG_SIDEBAR_H), l.config(bg=BG_SIDEBAR_H), a.config(bg=BG_SIDEBAR_H)))
                w.bind("<Leave>",  lambda _, r=dept_row, l=dept_lbl, a=arrow:
                    (r.config(bg=BG_INPUT), l.config(bg=BG_INPUT), a.config(bg=BG_INPUT)))

        dir_canvas.update_idletasks()
        dir_canvas.configure(scrollregion=dir_canvas.bbox("all"))

    def do_search(*_):
        q = search_entry.get()
        if q == "Search": q = ""
        build_accordion(q)

    search_entry.bind("<KeyRelease>", do_search)
    build_accordion()


# ── FINANCE TAB ───────────────────────────────────────────────────────────────
def build_finance_tab(parent):
    content = tk.Frame(parent, bg=BG_MAIN)
    content.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(content, text="Finance and Transactions", fg=ACCENT, bg=BG_MAIN,
             font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))

    summary_row = tk.Frame(content, bg=BG_MAIN)
    summary_row.pack(fill="x", pady=(0, 16))

    for title, value in [("Total Revenue", "₱125,400.00"), ("Tickets Sold", "312"), ("Refunds", "8"), ("Net Income", "₱118,200.00")]:
        card = tk.Frame(summary_row, bg=BG_CARD, padx=20, pady=14)
        card.pack(side="left", padx=(0, 12), fill="y")
        tk.Label(card, text=title, fg=TEXT_MID, bg=BG_CARD, font=(FONT, 10)).pack(anchor="w")
        tk.Label(card, text=value, fg=ACCENT,   bg=BG_CARD, font=(FONT, 16, "bold")).pack(anchor="w")

    table_frame = tk.Frame(content, bg=BG_PANEL)
    table_frame.pack(fill="both", expand=True)

    headers = ["Transaction ID", "Date", "Customer", "Production", "Seats", "Amount", "Status"]
    col_widths = [14, 12, 20, 24, 8, 14, 10]

    header_row = tk.Frame(table_frame, bg=BG_PANEL)
    header_row.pack(fill="x", padx=16, pady=(12, 4))
    for h, cw in zip(headers, col_widths):
        tk.Label(header_row, text=h, fg=ACCENT, bg=BG_PANEL,
                 font=(FONT, 10, "bold"), width=cw, anchor="w").pack(side="left")

    tk.Frame(table_frame, bg=DIVIDER, height=1).pack(fill="x", padx=16)

    sample_rows = [
        ("#TXN-001", "May 10", "Juan Dela Cruz",      "Hamlet",              "A1",     "₱500",   "Paid"),
        ("#TXN-002", "May 11", "Maria Santos",        "Phantom of the Opera","B2,B3",  "₱1,000", "Paid"),
        ("#TXN-003", "May 12", "Pedro Reyes",         "Hamlet",              "C5",     "₱500",   "Refunded"),
        ("#TXN-004", "May 13", "Ana Garcia",          "Phantom of the Opera","D1",     "₱500",   "Paid"),
    ]

    for i, row_data in enumerate(sample_rows):
        row_bg = BG_TABLE_ROW if i % 2 == 0 else BG_TABLE_ALT
        row = tk.Frame(table_frame, bg=row_bg)
        row.pack(fill="x", padx=16)
        for val, cw in zip(row_data, col_widths):
            fg = ACCENT if val == "Refunded" else TEXT_DARK
            tk.Label(row, text=val, fg=fg, bg=row_bg,
                     font=(FONT, 10), width=cw, anchor="w").pack(side="left", pady=10)
        tk.Frame(table_frame, bg=DIVIDER, height=1).pack(fill="x", padx=16)


# ── CUSTOMERS TAB ─────────────────────────────────────────────────────────────
def build_customers_tab(parent):

    content = tk.Frame(parent, bg=BG_MAIN)
    content.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(content, text="Customer Management", fg=ACCENT, bg=BG_MAIN,
             font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))

    # ── Search bar (functional) ───────────────────────────────────────────────
    search_var = tk.StringVar()
    placeholder_text = "Search customers..."

    search_frame = tk.Frame(content, bg=BG_SEARCH)
    search_frame.pack(anchor="w", pady=(0, 12))
    tk.Label(search_frame, text="🔍", bg=BG_SEARCH, fg=TEXT_MID,
             font=("Arial", 11)).pack(side="left", padx=(6, 2), pady=6)
    search_entry = tk.Entry(search_frame, textvariable=search_var,
                            font=(FONT, 11), bg=BG_SEARCH, fg=TEXT_MID,
                            relief="flat", bd=0, width=30)
    search_entry.insert(0, placeholder_text)
    search_entry.pack(side="left", pady=6, padx=4)

    def sf_in(_):
        if search_entry.get() == placeholder_text:
            search_entry.delete(0, "end"); search_entry.config(fg=TEXT_DARK)
    def sf_out(_):
        if search_entry.get() == "":
            search_entry.insert(0, placeholder_text); search_entry.config(fg=TEXT_MID)
    search_entry.bind("<FocusIn>",  sf_in)
    search_entry.bind("<FocusOut>", sf_out)

    # ── Transaction History popup — connected to DB ───────────────────────────
    def open_transaction_history(customer):
        dlg = tk.Toplevel(parent.winfo_toplevel())
        dlg.title("Transaction History")
        dlg.configure(bg=BG_DETAIL)
        dlg.resizable(False, False)
        dlg.transient(parent.winfo_toplevel())
        dlg.grab_set()
        root_win = parent.winfo_toplevel()
        root_win.update_idletasks()
        x = root_win.winfo_x() + (root_win.winfo_width()  - 700) // 2
        y = root_win.winfo_y() + (root_win.winfo_height() - 420) // 2
        dlg.geometry(f"700x420+{x}+{y}")

        hdr = tk.Frame(dlg, bg=BG_DETAIL)
        hdr.pack(fill="x", padx=28, pady=(22, 6))
        tk.Label(hdr, text="Transaction History",
                 fg=ACCENT, bg=BG_DETAIL, font=(FONT, 16, "bold")).pack(anchor="w")
        tk.Label(hdr, text=customer["name"],
                 fg=TEXT_MID, bg=BG_DETAIL, font=(FONT, 11)).pack(anchor="w", pady=(2, 0))
        tk.Frame(dlg, bg=DIVIDER, height=1).pack(fill="x", padx=28, pady=(8, 0))

        HEADERS    = ["Ticket #",  "Date", "Production", "Amount",  "Status"]
        COL_WIDTHS = [14,           13,     22,            13,        10]

        tbl = tk.Frame(dlg, bg=BG_DETAIL)
        tbl.pack(fill="both", expand=True, padx=28, pady=(0, 6))

        hdr_row = tk.Frame(tbl, bg=BG_DETAIL)
        hdr_row.pack(fill="x", pady=(10, 4))
        for h, cw in zip(HEADERS, COL_WIDTHS):
            tk.Label(hdr_row, text=h, fg=ACCENT, bg=BG_DETAIL,
                     font=(FONT, 11, "bold"), width=cw, anchor="w").pack(side="left", padx=4)

        tk.Frame(tbl, bg=DIVIDER, height=1).pack(fill="x")

        rows_frame = tk.Frame(tbl, bg=BG_DETAIL)
        rows_frame.pack(fill="both", expand=True)

        txns = db_load_transaction_history(customer["customer_id"])

        if not txns:
            tk.Label(rows_frame, text="No transactions found.",
                     fg=TEXT_MUTED, bg=BG_DETAIL, font=(FONT, 11)).pack(pady=20)
        else:
            canvas_h = tk.Canvas(rows_frame, bg=BG_DETAIL, highlightthickness=0)
            scrollbar = tk.Scrollbar(rows_frame, orient="vertical", command=canvas_h.yview)
            canvas_h.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            canvas_h.pack(side="left", fill="both", expand=True)
            scroll_inner = tk.Frame(canvas_h, bg=BG_DETAIL)
            win_id = canvas_h.create_window((0, 0), window=scroll_inner, anchor="nw")
            scroll_inner.bind("<Configure>",
                lambda e: canvas_h.configure(scrollregion=canvas_h.bbox("all")))
            canvas_h.bind("<Configure>",
                lambda e: canvas_h.itemconfig(win_id, width=e.width))

            status_colors = {"sold": "#2ECC40", "reserved": "#F39C12", "refunded": "#CC1111"}

            for r_idx, (tkt_num, date, prod, amount, status) in enumerate(txns):
                row_bg = BG_TABLE_ROW if r_idx % 2 == 0 else BG_TABLE_ALT
                row_f  = tk.Frame(scroll_inner, bg=row_bg)
                row_f.pack(fill="x")
                tk.Frame(row_f, bg=DIVIDER, height=1).pack(fill="x")
                data_row = tk.Frame(row_f, bg=row_bg)
                data_row.pack(fill="x")
                prod_display = prod if len(prod) <= 18 else prod[:15] + "..."
                for val, cw in zip([tkt_num, date, prod_display, amount], COL_WIDTHS[:4]):
                    tk.Label(data_row, text=val, fg=TEXT_DARK, bg=row_bg,
                             font=(FONT, 10), width=cw, anchor="w").pack(side="left", padx=4, pady=8)
                tk.Label(data_row, text=status.capitalize(),
                         fg=status_colors.get(status.lower(), TEXT_DARK),
                         bg=row_bg, font=(FONT, 10, "bold"),
                         width=COL_WIDTHS[4], anchor="w").pack(side="left", padx=4, pady=8)

        close_row = tk.Frame(dlg, bg=BG_DETAIL)
        close_row.pack(pady=(4, 16))
        make_canvas_btn(close_row, "Close", dlg.destroy,
                        w=80, h=32, fill=ACCENT, fill_hov=ACCENT_HOV,
                        bg=BG_DETAIL).pack()

    # ── Table ─────────────────────────────────────────────────────────────────
    table_frame = tk.Frame(content, bg=BG_PANEL)
    table_frame.pack(fill="both", expand=True)

    headers    = ["Name", "Email", "Mobile", "Actions"]
    col_widths = [24, 28, 16, 20]

    header_row = tk.Frame(table_frame, bg=BG_PANEL)
    header_row.pack(fill="x", padx=16, pady=(12, 4))
    for h, cw in zip(headers, col_widths):
        tk.Label(header_row, text=h, fg=ACCENT, bg=BG_PANEL,
                 font=(FONT, 10, "bold"), width=cw, anchor="w").pack(side="left")

    tk.Frame(table_frame, bg=DIVIDER, height=1).pack(fill="x", padx=16)

    rows_container = tk.Frame(table_frame, bg=BG_PANEL)
    rows_container.pack(fill="both", expand=True)

    # Load all customers from DB once
    ALL_CUSTOMERS = db_load_customers()

    def render_rows(data):
        for w in rows_container.winfo_children():
            w.destroy()
        if not data:
            tk.Label(rows_container, text="No customers found.",
                     fg=TEXT_MUTED, bg=BG_PANEL, font=(FONT, 11)).pack(pady=20)
            return
        for i, cust in enumerate(data):
            row_bg = BG_TABLE_ROW if i % 2 == 0 else BG_TABLE_ALT
            row = tk.Frame(rows_container, bg=row_bg)
            row.pack(fill="x", padx=16)
            for val, cw in zip([cust["name"], cust["email"], cust["mobile"]], col_widths[:3]):
                tk.Label(row, text=val, fg=TEXT_DARK, bg=row_bg,
                         font=(FONT, 10), width=cw, anchor="w").pack(side="left", pady=10)
            make_canvas_btn(row, "View History",
                            lambda c=cust: open_transaction_history(c),
                            w=110, h=28, bg=row_bg).pack(side="left", padx=4)
            tk.Frame(rows_container, bg=DIVIDER, height=1).pack(fill="x", padx=16)

    def on_search(*_):
        q = search_var.get().strip().lower()
        if q == placeholder_text.lower(): q = ""
        filtered = [c for c in ALL_CUSTOMERS
                    if q in c["name"].lower()
                    or q in c["email"].lower()
                    or q in c["mobile"]] if q else ALL_CUSTOMERS
        render_rows(filtered)

    search_var.trace_add("write", on_search)
    render_rows(ALL_CUSTOMERS)


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD WINDOW
# ══════════════════════════════════════════════════════════════════════════════

def open_dashboard(role, staff_id):
    root = tk.Tk()
    root.title("My Metropolitan Theater")
    root.geometry("1920x1080")
    root.configure(bg=BG_MAIN)

    # Determine nav based on role
    nav_items = ALL_NAV if role == "MANAGER" else SALES_NAV

    # ── Top bar ───────────────────────────────────────────────────────────────
    topbar = tk.Frame(root, bg=BG_TOPBAR, height=45)
    topbar.pack(fill="x", side="top")
    topbar.pack_propagate(False)

    tk.Label(topbar, text="MY METROPOLITAN THEATER",
             fg=ACCENT, bg=BG_TOPBAR, font=(FONT, 13, "bold")).pack(side="left", padx=18, pady=10)

    role_lbl = tk.Label(topbar, text=f"👤  {role}  |  ID: {staff_id}",
                        fg=TEXT_LIGHT, bg=BG_TOPBAR, font=(FONT, 10))
    role_lbl.pack(side="right", padx=(0, 8))

    logout_lbl = tk.Label(topbar, text="⬛→", fg=TEXT_LIGHT, bg=BG_TOPBAR, font=(FONT, 14), cursor="hand2")
    logout_lbl.pack(side="right", padx=8)
    logout_lbl.bind("<Enter>",    lambda _: logout_lbl.config(fg=ACCENT))
    logout_lbl.bind("<Leave>",    lambda _: logout_lbl.config(fg=TEXT_LIGHT))

    def open_logout_dialog():
        dlg = tk.Toplevel(root)
        dlg.title("")
        dlg.configure(bg=TEXT_LIGHT)
        dlg.resizable(False, False)
        dlg.transient(root)
        dlg.grab_set()
        x = root.winfo_x() + (root.winfo_width() - 380) // 2
        y = root.winfo_y() + (root.winfo_height() - 240) // 2
        dlg.geometry(f"380x240+{x}+{y}")
        tk.Label(dlg, text="Are you sure you want to logout?",
                 fg=TEXT_DARK, bg=TEXT_LIGHT, font=(FONT, 13)).pack(pady=(50, 20))
        br = tk.Frame(dlg, bg=TEXT_LIGHT)
        br.pack()
        tk.Button(br, text="Cancel", bg="#EEEEEE", fg=TEXT_DARK, font=(FONT, 11),
                  relief="flat", bd=0, padx=18, pady=8, cursor="hand2",
                  command=dlg.destroy, activebackground="#DDDDDD").pack(side="left", padx=(0, 12))
        make_canvas_btn(br, "Logout", root.destroy, w=90, h=36, fill=ACCENT,
                        fill_hov=ACCENT_HOV, bg=TEXT_LIGHT).pack(side="left")

    logout_lbl.bind("<Button-1>", lambda _: open_logout_dialog())

    # ── Body ──────────────────────────────────────────────────────────────────
    body = tk.Frame(root, bg=BG_MAIN)
    body.pack(fill="both", expand=True)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    sidebar = tk.Frame(body, bg=BG_SIDEBAR, width=175)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    tk.Frame(sidebar, bg=BG_SIDEBAR, height=20).pack()

    # ── Content area ──────────────────────────────────────────────────────────
    content_area = tk.Frame(body, bg=BG_MAIN)
    content_area.pack(side="left", fill="both", expand=True)

    # Map tab name to builder function
    tab_builders = {
        "Catalog":    build_catalog_tab,
        "Sales":      build_sales_tab,
        "Personnel":  build_personnel_tab,
        "Finances":   build_finance_tab,
        "Customers":  build_customers_tab,
    }

    # Cache frames so switching is instant
    tab_frames = {}
    active_nav = [None]
    active_nav_widgets = [None]  # (frame, icon_lbl, text_lbl)

    def switch_tab(tab_name, nav_frame, icon_lbl, text_lbl):
        # Update sidebar highlight
        if active_nav_widgets[0]:
            pf, pi, pt = active_nav_widgets[0]
            pf.config(bg=BG_SIDEBAR); pi.config(bg=BG_SIDEBAR, fg=TEXT_LIGHT); pt.config(bg=BG_SIDEBAR, fg=TEXT_LIGHT)
        nav_frame.config(bg=BG_ACTIVE); icon_lbl.config(bg=BG_ACTIVE, fg=ACCENT); text_lbl.config(bg=BG_ACTIVE, fg=ACCENT)
        active_nav[0] = tab_name
        active_nav_widgets[0] = (nav_frame, icon_lbl, text_lbl)

        # Hide all tab frames
        for f in tab_frames.values():
            f.pack_forget()

        # Build tab if not yet built
        if tab_name not in tab_frames:
            frame = tk.Frame(content_area, bg=BG_MAIN)
            tab_builders[tab_name](frame)
            tab_frames[tab_name] = frame

        tab_frames[tab_name].pack(fill="both", expand=True)

    # Build sidebar nav items
    for i, (icon, label) in enumerate(nav_items):
        is_first = (i == 0)
        bg = BG_ACTIVE if is_first else BG_SIDEBAR
        nav_frame = tk.Frame(sidebar, bg=bg, cursor="hand2")
        nav_frame.pack(fill="x")
        icon_lbl = tk.Label(nav_frame, text=icon, bg=bg,
                            fg=ACCENT if is_first else TEXT_LIGHT,
                            font=("Arial", 13), width=3)
        icon_lbl.pack(side="left", padx=(10, 4), pady=12)
        text_lbl = tk.Label(nav_frame, text=label, bg=bg,
                            fg=ACCENT if is_first else TEXT_LIGHT,
                            font=(FONT, 12, "bold" if is_first else "normal"))
        text_lbl.pack(side="left")

        def on_enter(_, f=nav_frame, il=icon_lbl, tl=text_lbl, lbl=label):
            if active_nav[0] != lbl:
                f.config(bg=BG_SIDEBAR_H); il.config(bg=BG_SIDEBAR_H); tl.config(bg=BG_SIDEBAR_H)
        def on_leave(_, f=nav_frame, il=icon_lbl, tl=text_lbl, lbl=label):
            if active_nav[0] != lbl:
                f.config(bg=BG_SIDEBAR); il.config(bg=BG_SIDEBAR); tl.config(bg=BG_SIDEBAR)
        def on_click(_, lbl=label, f=nav_frame, il=icon_lbl, tl=text_lbl):
            switch_tab(lbl, f, il, tl)

        for w in (nav_frame, icon_lbl, text_lbl):
            w.bind("<Enter>",    on_enter)
            w.bind("<Leave>",    on_leave)
            w.bind("<Button-1>", on_click)

        if is_first:
            active_nav[0] = label
            active_nav_widgets[0] = (nav_frame, icon_lbl, text_lbl)

    # Load first tab
    first_tab = nav_items[0][1]
    frame = tk.Frame(content_area, bg=BG_MAIN)
    tab_builders[first_tab](frame)
    tab_frames[first_tab] = frame
    frame.pack(fill="both", expand=True)

    root.mainloop()


# ── Run standalone for testing ────────────────────────────────────────────────
if __name__ == "__main__":
    # Test as MANAGER
    open_dashboard("MANAGER", 1)