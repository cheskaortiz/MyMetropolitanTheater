import tkinter as tk
from tkinter import ttk
import sys
import os

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
    departments = ["Productions", "Box Offices/Sales", "Venue Operations",
                   "Management/Administration", "Human Resources", "Technical Crew"]
    employees = {
        "Productions": [
            {"name": "Mary Ruth Cathryn Suello", "role": "Lead Producer",  "id": "STAFF-01", "dept": "Production"},
            {"name": "Jose Miguel Santos",        "role": "Stage Director", "id": "STAFF-02", "dept": "Production"},
        ],
        "Box Offices/Sales": [
            {"name": "Ana Reyes",   "role": "Box Office Head", "id": "STAFF-03", "dept": "Box Offices/Sales"},
            {"name": "Carlo Dizon", "role": "Sales Associate", "id": "STAFF-04", "dept": "Box Offices/Sales"},
        ],
        "Venue Operations": [
            {"name": "Lito Fernandez", "role": "Venue Manager", "id": "STAFF-05", "dept": "Venue Operations"},
        ],
        "Management/Administration": [
            {"name": "Grace Dela Cruz", "role": "Admin Officer", "id": "STAFF-06", "dept": "Management/Administration"},
        ],
        "Human Resources": [
            {"name": "Patricia Lim", "role": "HR Manager", "id": "STAFF-07", "dept": "Human Resources"},
        ],
        "Technical Crew": [
            {"name": "Ramon Cruz",  "role": "Lighting Tech", "id": "STAFF-08", "dept": "Technical Crew"},
            {"name": "Ella Torres", "role": "Sound Tech",    "id": "STAFF-09", "dept": "Technical Crew"},
        ],
    }
    time_logs = {
        "STAFF-01": [("10/01","STAFF-01","8.00"),("10/02","STAFF-01","8.30"),("10/03","STAFF-01","4.00")],
        "STAFF-02": [("10/01","STAFF-02","7.00"),("10/02","STAFF-02","8.00")],
    }

    content = tk.Frame(parent, bg=BG_MAIN)
    content.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(content, text="Staff and Payroll", fg=ACCENT, bg=BG_MAIN,
             font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))

    main_row = tk.Frame(content, bg=BG_MAIN)
    main_row.pack(fill="both", expand=True)

    left_panel = tk.Frame(main_row, bg=BG_PANEL, width=270)
    left_panel.pack(side="left", fill="y", padx=(0, 12))
    left_panel.pack_propagate(False)

    tk.Label(left_panel, text="Employee Directory", fg=TEXT_DARK, bg=BG_PANEL,
             font=(FONT, 12, "bold")).pack(anchor="w", padx=16, pady=(16, 8))

    search_frame = tk.Frame(left_panel, bg=BG_INPUT)
    search_frame.pack(fill="x", padx=16, pady=(0, 12))
    tk.Label(search_frame, text="🔍", bg=BG_INPUT, fg=TEXT_MID, font=("Arial", 10)).pack(side="left", padx=6, pady=6)
    search_entry = tk.Entry(search_frame, font=(FONT, 10), bg=BG_INPUT, fg=TEXT_MID, relief="flat", bd=0)
    search_entry.insert(0, "Search")
    search_entry.pack(side="left", fill="x", expand=True, pady=6)
    def sf_in(_):
        if search_entry.get() == "Search": search_entry.delete(0, "end"); search_entry.config(fg=TEXT_DARK)
    def sf_out(_):
        if search_entry.get() == "": search_entry.insert(0, "Search"); search_entry.config(fg=TEXT_MID)
    search_entry.bind("<FocusIn>", sf_in); search_entry.bind("<FocusOut>", sf_out)

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

    right_panel = tk.Frame(main_row, bg=BG_MAIN)
    right_panel.pack(side="left", fill="both", expand=True)

    placeholder = tk.Frame(right_panel, bg=BG_MAIN)
    placeholder.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(placeholder, text="Select an employee from the directory\nto view their details.",
             fg=TEXT_MUTED, bg=BG_MAIN, font=(FONT, 13), justify="center").pack()

    current_employee = [None]

    def show_employee(emp):
        current_employee[0] = emp
        for w in right_panel.winfo_children():
            w.destroy()
        rsc = tk.Canvas(right_panel, bg=BG_MAIN, highlightthickness=0, bd=0)
        sb  = ttk.Scrollbar(right_panel, orient="vertical", command=rsc.yview)
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

        card1 = tk.Frame(inner, bg=BG_PANEL)
        card1.pack(fill="x", pady=(0, 10))
        top_row = tk.Frame(card1, bg=BG_PANEL)
        top_row.pack(fill="x", padx=20, pady=(16, 4))
        name_col = tk.Frame(top_row, bg=BG_PANEL)
        name_col.pack(side="left", fill="x", expand=True)
        tk.Label(name_col, text=emp["name"], fg=TEXT_DARK, bg=BG_PANEL, font=(FONT, 15, "bold"), anchor="w").pack(anchor="w")
        tk.Label(name_col, text=emp["role"], fg=TEXT_MID,  bg=BG_PANEL, font=(FONT, 11), anchor="w").pack(anchor="w")
        info_row = tk.Frame(card1, bg=BG_PANEL)
        info_row.pack(fill="x", padx=20, pady=(8, 16))
        id_col = tk.Frame(info_row, bg=BG_PANEL)
        id_col.pack(side="left", padx=(0, 60))
        tk.Label(id_col, text="ID", fg=TEXT_DARK, bg=BG_PANEL, font=(FONT, 10, "bold")).pack(anchor="w")
        tk.Label(id_col, text=emp["id"], fg=TEXT_DARK, bg=BG_PANEL, font=(FONT, 11)).pack(anchor="w")
        di_col = tk.Frame(info_row, bg=BG_PANEL)
        di_col.pack(side="left")
        tk.Label(di_col, text="Department", fg=TEXT_DARK, bg=BG_PANEL, font=(FONT, 10, "bold")).pack(anchor="w")
        tk.Label(di_col, text=emp["dept"], fg=TEXT_DARK, bg=BG_PANEL, font=(FONT, 11)).pack(anchor="w")

        card3 = tk.Frame(inner, bg=BG_PANEL)
        card3.pack(fill="x", pady=(0, 10))
        tk.Label(card3, text="Time Tracking", fg=TEXT_DARK, bg=BG_PANEL, font=(FONT, 13, "bold")).pack(anchor="w", padx=20, pady=(16, 10))
        tk.Frame(card3, bg=DIVIDER, height=1).pack(fill="x", padx=20)
        th_row = tk.Frame(card3, bg=BG_PANEL)
        th_row.pack(fill="x", padx=20, pady=(6, 2))
        for col_text, col_w in [("Date", 12), ("Staff ID", 16), ("Hours Worked", 16)]:
            tk.Label(th_row, text=col_text, fg=ACCENT, bg=BG_PANEL, font=(FONT, 10, "bold"), width=col_w, anchor="w").pack(side="left")
        tk.Frame(card3, bg=DIVIDER, height=1).pack(fill="x", padx=20)
        logs = time_logs.get(emp["id"], [])
        for i, (date, sid, hrs) in enumerate(logs):
            row_bg = TEXT_LIGHT if i % 2 == 0 else BG_TABLE_ALT
            rw = tk.Frame(card3, bg=row_bg)
            rw.pack(fill="x", padx=20)
            for val, cw in [(date, 12), (sid, 16), (hrs, 16)]:
                tk.Label(rw, text=val, fg=TEXT_DARK, bg=row_bg, font=(FONT, 10), width=cw, anchor="w").pack(side="left", pady=8)
            tk.Frame(card3, bg=DIVIDER, height=1).pack(fill="x", padx=20)
        tk.Frame(card3, height=12, bg=BG_PANEL).pack()

    dept_open = {}
    selected_emp_row = [None]
    selected_emp_lbl = [None]

    def toggle_dept(dept, emp_container, arrow_lbl):
        dept_open[dept] = not dept_open.get(dept, False)
        if dept_open[dept]:
            emp_container.pack(fill="x")
            arrow_lbl.config(text="∧")
        else:
            emp_container.pack_forget()
            arrow_lbl.config(text="∨")

    for dept in departments:
        dept_open[dept] = False
        wrapper = tk.Frame(dir_inner, bg=BG_PANEL)
        wrapper.pack(fill="x", pady=2, padx=8)
        dept_row = tk.Frame(wrapper, bg=BG_INPUT, cursor="hand2")
        dept_row.pack(fill="x")
        dept_lbl = tk.Label(dept_row, text=dept, bg=BG_INPUT, fg=TEXT_DARK, font=(FONT, 10), anchor="w")
        dept_lbl.pack(side="left", padx=8, pady=8, fill="x", expand=True)
        arrow = tk.Label(dept_row, text="∨", bg=BG_INPUT, fg=TEXT_MID, font=(FONT, 10))
        arrow.pack(side="right", padx=8)
        emp_container = tk.Frame(wrapper, bg=BG_PANEL)

        for emp_data in employees.get(dept, []):
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

        for w in (dept_row, dept_lbl, arrow):
            w.bind("<Button-1>", lambda _, d=dept, ec=emp_container, a=arrow: toggle_dept(d, ec, a))


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
    CUSTOMERS = [
        {"name": "Mary Ruth Cathryn Suello", "email": "toothiefruthie@gmail.com", "mobile": "09284713504"},
        {"name": "Jose Miguel Santos",        "email": "josemiguel@email.com",     "mobile": "09171234567"},
        {"name": "Ana Reyes",                 "email": "ana.reyes@email.com",       "mobile": "09281234567"},
        {"name": "Carlo Dizon",               "email": "carlo.dizon@email.com",     "mobile": "09194567890"},
    ]

    content = tk.Frame(parent, bg=BG_MAIN)
    content.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(content, text="Customer Management", fg=ACCENT, bg=BG_MAIN,
             font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))

    search_frame = tk.Frame(content, bg=BG_SEARCH)
    search_frame.pack(anchor="w", pady=(0, 12))
    tk.Label(search_frame, text="🔍", bg=BG_SEARCH, fg=TEXT_MID, font=("Arial", 11)).pack(side="left", padx=(6, 2), pady=6)
    search_entry = tk.Entry(search_frame, font=(FONT, 11), bg=BG_SEARCH, fg=TEXT_MID, relief="flat", bd=0, width=30)
    search_entry.insert(0, "Search customers...")
    search_entry.pack(side="left", pady=6, padx=4)

    table_frame = tk.Frame(content, bg=BG_PANEL)
    table_frame.pack(fill="both", expand=True)

    headers = ["Name", "Email", "Mobile", "Actions"]
    col_widths = [24, 28, 16, 20]

    header_row = tk.Frame(table_frame, bg=BG_PANEL)
    header_row.pack(fill="x", padx=16, pady=(12, 4))
    for h, cw in zip(headers, col_widths):
        tk.Label(header_row, text=h, fg=ACCENT, bg=BG_PANEL,
                 font=(FONT, 10, "bold"), width=cw, anchor="w").pack(side="left")

    tk.Frame(table_frame, bg=DIVIDER, height=1).pack(fill="x", padx=16)

    for i, cust in enumerate(CUSTOMERS):
        row_bg = BG_TABLE_ROW if i % 2 == 0 else BG_TABLE_ALT
        row = tk.Frame(table_frame, bg=row_bg)
        row.pack(fill="x", padx=16)
        for val, cw in zip([cust["name"], cust["email"], cust["mobile"]], col_widths[:3]):
            tk.Label(row, text=val, fg=TEXT_DARK, bg=row_bg,
                     font=(FONT, 10), width=cw, anchor="w").pack(side="left", pady=10)
        btn = make_canvas_btn(row, "View History", lambda: None, w=110, h=28, bg=row_bg)
        btn.pack(side="left", padx=4)
        tk.Frame(table_frame, bg=DIVIDER, height=1).pack(fill="x", padx=16)


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