import tkinter as tk

# ── Colors ────────────────────────────────────────────────────────────────────
BG_MAIN      = "#B0B0B0"
BG_TOPBAR    = "#1E1E1E"
BG_SIDEBAR   = "#9A9A9A"
BG_SIDEBAR_H = "#888888"
BG_ACTIVE    = "#C8C8C8"
BG_LIST      = "#F5F5F5"
BG_DETAIL    = "#F0F0F0"
BG_SEARCH    = "#E8E8E8"
BG_TABLE_ROW = "#FFFFFF"
BG_TABLE_ALT = "#F5F5F5"
ACCENT       = "#CC1111"
ACCENT_HOV   = "#AA0000"
TEXT_LIGHT   = "#FFFFFF"
TEXT_DARK    = "#1A1A1A"
TEXT_MID     = "#555555"
TEXT_MUTED   = "#AAAAAA"
DIVIDER      = "#DDDDDD"

FONT   = "Helvetica"
RADIUS = 3

# ── Sample data ───────────────────────────────────────────────────────────────
CUSTOMERS = [
    {
        "name":   "Mary Ruth Cathryn Suello",
        "email":  "toothiefruthie@gmail.com",
        "mobile": "09284713504",
        "transactions": [
            ("TKT-001", "2026-05-10", "Hamlet",                   "Php 100.00"),
            ("TKT-002", "2026-05-10", "The Phantom of the Opera",  "Php 100.00"),
            ("TKT-003", "2026-05-10", "Wicked",                   "Php 100.00"),
        ],
    },
    {
        "name":   "Francheska Ortiz",
        "email":  "cheskamalatek@gmail.com",
        "mobile": "09284713504",
        "transactions": [
            ("TKT-004", "2026-04-22", "Hamlet",  "Php 200.00"),
            ("TKT-005", "2026-04-23", "Wicked",  "Php 150.00"),
        ],
    },
    {
        "name":   "Elicxia Geighnel Mistica",
        "email":  "eli@gmail.com",
        "mobile": "09284713504",
        "transactions": [
            ("TKT-006", "2026-03-15", "The Phantom of the Opera", "Php 300.00"),
        ],
    },
]

NAV_ITEMS = [
    ("🎭", "Catalog"),
    ("🎟", "Sales"),
    ("👤", "Personnel"),
    ("💰", "Finances"),
    ("👥", "Customers"),
]

# ── Column spec shared by header AND rows ─────────────────────────────────────
# (label, char-width for Label widgets)
COL_SPEC = [
    ("Customer Name",  28),
    ("Email Address",  28),
    ("Mobile Number",  16),
    ("Actions",        20),
]
BTN_W, BTN_H = 160, 28   # pixel size of the action button

# ── Rounded rect helper ───────────────────────────────────────────────────────
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
    c = tk.Canvas(parent, width=w, height=h, bg=bg,
                highlightthickness=0, bd=0)
    def draw(color):
        c.delete("all")
        rounded_rect(c, 0, 0, w, h, RADIUS, fill=color, outline=color)
        c.create_text(w//2, h//2, text=text, fill=fg,
                    font=(FONT, font_size, "bold"))
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

# ── Logout dialog ─────────────────────────────────────────────────────────────
def open_logout_dialog():
    dlg = tk.Toplevel(root)
    dlg.title("")
    dlg.configure(bg=TEXT_LIGHT)
    dlg.resizable(False, False)
    dlg.transient(root)
    dlg.grab_set()
    center_on(dlg, root, 380, 240)

    icon_canvas = tk.Canvas(dlg, width=90, height=90,
                            bg=TEXT_LIGHT, highlightthickness=0)
    icon_canvas.pack(pady=(28, 0))
    icon_canvas.create_oval(5, 5, 85, 85, fill="#EEEEEE", outline="#EEEEEE")
    icon_canvas.create_text(45, 47, text="⬛→", font=("Arial", 22), fill="#AAAAAA")

    tk.Label(dlg,
            text="Are you sure you want to logout?",
            fg=TEXT_DARK, bg=TEXT_LIGHT,
            font=(FONT, 13)).pack(pady=(14, 20))

    btn_row = tk.Frame(dlg, bg=TEXT_LIGHT)
    btn_row.pack()

    tk.Button(btn_row, text="Cancel",
            bg="#EEEEEE", fg=TEXT_DARK,
            font=(FONT, 11), relief="flat", bd=0,
            padx=18, pady=8, cursor="hand2",
            command=dlg.destroy,
            activebackground="#DDDDDD").pack(side="left", padx=(0, 12))

    make_canvas_btn(btn_row, "Logout", lambda: root.destroy(),
                    w=90, h=36, fill=ACCENT, fill_hov=ACCENT_HOV,
                    bg=TEXT_LIGHT).pack(side="left")

# ── Transaction History popup ─────────────────────────────────────────────────
def open_transaction_history(customer):
    dlg = tk.Toplevel(root)
    dlg.title("Transaction History")
    dlg.configure(bg=BG_DETAIL)
    dlg.resizable(False, False)
    dlg.transient(root)
    dlg.grab_set()
    center_on(dlg, root, 640, 360)

    hdr = tk.Frame(dlg, bg=BG_DETAIL)
    hdr.pack(fill="x", padx=28, pady=(22, 6))
    tk.Label(hdr, text="Transaction History",
            fg=ACCENT, bg=BG_DETAIL,
            font=(FONT, 16, "bold")).pack(anchor="w")
    tk.Label(hdr, text=customer["name"],
            fg=TEXT_MID, bg=BG_DETAIL,
            font=(FONT, 11)).pack(anchor="w", pady=(2, 0))
    tk.Frame(dlg, bg=DIVIDER, height=1).pack(fill="x", padx=28, pady=(8, 0))

    HEADERS    = ["Ticket ID", "Date", "Production", "Total Spent"]
    COL_WIDTHS = [12, 14, 22, 13]

    tbl = tk.Frame(dlg, bg=BG_DETAIL)
    tbl.pack(fill="both", expand=True, padx=28, pady=(0, 6))

    hdr_row = tk.Frame(tbl, bg=BG_DETAIL)
    hdr_row.pack(fill="x", pady=(10, 4))
    for col, (h, cw) in enumerate(zip(HEADERS, COL_WIDTHS)):
        tk.Label(hdr_row, text=h,
                fg=ACCENT, bg=BG_DETAIL,
                font=(FONT, 11, "bold"),
                width=cw, anchor="w").grid(row=0, column=col, padx=4, sticky="w")

    tk.Frame(tbl, bg=DIVIDER, height=1).pack(fill="x")

    rows_frame = tk.Frame(tbl, bg=BG_DETAIL)
    rows_frame.pack(fill="both", expand=True)

    txns = customer["transactions"]
    if not txns:
        tk.Label(rows_frame, text="No transactions found.",
                fg=TEXT_MUTED, bg=BG_DETAIL,
                font=(FONT, 11)).pack(pady=20)
    else:
        for r_idx, (tid, date, prod, spent) in enumerate(txns):
            row_bg = BG_TABLE_ROW if r_idx % 2 == 0 else BG_TABLE_ALT
            row_frame = tk.Frame(rows_frame, bg=row_bg)
            row_frame.pack(fill="x")
            tk.Frame(row_frame, bg=DIVIDER, height=1).pack(fill="x")
            data_row = tk.Frame(row_frame, bg=row_bg)
            data_row.pack(fill="x")
            prod_display = prod if len(prod) <= 16 else prod[:13] + "..."
            for col, (val, cw) in enumerate(
                    zip([tid, date, prod_display, spent], COL_WIDTHS)):
                tk.Label(data_row, text=val,
                        fg=TEXT_DARK, bg=row_bg,
                        font=(FONT, 11),
                        width=cw, anchor="w").grid(
                    row=0, column=col, padx=4, pady=10, sticky="w")

    close_row = tk.Frame(dlg, bg=BG_DETAIL)
    close_row.pack(pady=(4, 16))
    make_canvas_btn(close_row, "Close", dlg.destroy,
                    w=80, h=32, fill=ACCENT, fill_hov=ACCENT_HOV,
                    bg=BG_DETAIL).pack()

# ── Main window ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("My Metropolitan Theater")
root.geometry("1920x1080")
root.configure(bg=BG_MAIN)

# ── Top bar ───────────────────────────────────────────────────────────────────
topbar = tk.Frame(root, bg=BG_TOPBAR, height=45)
topbar.pack(fill="x", side="top")
topbar.pack_propagate(False)

tk.Label(topbar, text="MY METROPOLITAN THEATER",
        fg=ACCENT, bg=BG_TOPBAR,
        font=(FONT, 13, "bold")).pack(side="left", padx=18, pady=10)

logout_lbl = tk.Label(topbar, text="⬛→", fg=TEXT_LIGHT, bg=BG_TOPBAR,
                    font=(FONT, 14), cursor="hand2")
logout_lbl.pack(side="right", padx=16)
logout_lbl.bind("<Enter>",    lambda _: logout_lbl.config(fg=ACCENT))
logout_lbl.bind("<Leave>",    lambda _: logout_lbl.config(fg=TEXT_LIGHT))
logout_lbl.bind("<Button-1>", lambda _: open_logout_dialog())

# ── Body ──────────────────────────────────────────────────────────────────────
body = tk.Frame(root, bg=BG_MAIN)
body.pack(fill="both", expand=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
sidebar = tk.Frame(body, bg=BG_SIDEBAR, width=175)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)
tk.Frame(sidebar, bg=BG_SIDEBAR, height=20).pack()

active_nav = [None]

def make_nav_item(icon, label, is_active=False):
    bg = BG_ACTIVE if is_active else BG_SIDEBAR
    frame = tk.Frame(sidebar, bg=bg, cursor="hand2")
    frame.pack(fill="x")
    icon_lbl = tk.Label(frame, text=icon, bg=bg,
                        fg=ACCENT if is_active else TEXT_LIGHT,
                        font=("Arial", 13), width=3)
    icon_lbl.pack(side="left", padx=(10, 4), pady=12)
    text_lbl = tk.Label(frame, text=label, bg=bg,
                        fg=ACCENT if is_active else TEXT_LIGHT,
                        font=(FONT, 12, "bold" if is_active else "normal"))
    text_lbl.pack(side="left")

    def on_enter(_):
        if frame != active_nav[0]:
            frame.config(bg=BG_SIDEBAR_H)
            icon_lbl.config(bg=BG_SIDEBAR_H)
            text_lbl.config(bg=BG_SIDEBAR_H)
    def on_leave(_):
        if frame != active_nav[0]:
            frame.config(bg=BG_SIDEBAR)
            icon_lbl.config(bg=BG_SIDEBAR)
            text_lbl.config(bg=BG_SIDEBAR)
    for w in (frame, icon_lbl, text_lbl):
        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)
    if is_active:
        active_nav[0] = frame

for i, (icon, label) in enumerate(NAV_ITEMS):
    make_nav_item(icon, label, is_active=(i == 4))

# ── Content area ──────────────────────────────────────────────────────────────
content = tk.Frame(body, bg=BG_MAIN)
content.pack(side="left", fill="both", expand=True, padx=28, pady=20)

tk.Label(content, text="Customer Database",
        fg=ACCENT, bg=BG_MAIN,
        font=(FONT, 20, "bold")).pack(anchor="w", pady=(0, 16))

# ── White card ────────────────────────────────────────────────────────────────
card = tk.Frame(content, bg=BG_DETAIL,
                highlightbackground="#CCCCCC", highlightthickness=1)
card.pack(fill="both", expand=True)

# ── Search bar ────────────────────────────────────────────────────────────────
search_row = tk.Frame(card, bg=BG_DETAIL)
search_row.pack(fill="x", padx=16, pady=(14, 6))

search_var = tk.StringVar()

search_canvas = tk.Canvas(search_row, width=200, height=32, bg=BG_DETAIL,
                        highlightthickness=0, bd=0)
search_canvas.pack(side="right")
rounded_rect(search_canvas, 0, 0, 200, 32, 6, fill=BG_SEARCH, outline="#CCCCCC")

sf = tk.Frame(search_canvas, bg=BG_SEARCH)
search_canvas.create_window(100, 16, window=sf)

tk.Label(sf, text="🔍", bg=BG_SEARCH,
        fg=TEXT_MID, font=("Arial", 10)).pack(side="left", padx=(6, 2), pady=4)

placeholder_text = "Search"

def on_focus_in(event):
    if search_entry.get() == placeholder_text:
        search_entry.delete(0, tk.END)
        search_entry.config(fg=TEXT_DARK)

def on_focus_out(event):
    if search_entry.get() == "":
        search_entry.insert(0, placeholder_text)
        search_entry.config(fg=TEXT_MID)

search_entry = tk.Entry(sf, textvariable=search_var,
                        font=(FONT, 10), bg=BG_SEARCH, fg=TEXT_MID,
                        relief="flat", bd=0,
                        insertbackground=TEXT_DARK, width=26)
search_entry.pack(side="left", pady=4, padx=(0, 6))
search_entry.insert(0, placeholder_text)
search_entry.bind("<FocusIn>", on_focus_in)
search_entry.bind("<FocusOut>", on_focus_out)

# ── Column headers ────────────────────────────────────────────────────────────
# Use a single grid container so headers and rows share the same column geometry
table_container = tk.Frame(card, bg=BG_DETAIL)
table_container.pack(fill="both", expand=True, padx=20, pady=(6, 12))

# Configure columns with uniform weights so they don't drift
for col, (_, cw) in enumerate(COL_SPEC):
    table_container.columnconfigure(col, minsize=cw * 7, weight=1 if col < 3 else 0)

# Header labels placed directly into table_container so their columns
# share the same geometry as the data rows in table_frame below.
for col, (label, cw) in enumerate(COL_SPEC):
    tk.Label(table_container, text=label,
            fg=ACCENT, bg=BG_DETAIL,
            font=(FONT, 11, "bold"),
            width=cw, anchor="w").grid(row=0, column=col,
                                        padx=(0, 8), pady=(0, 2), sticky="w")

tk.Frame(table_container, bg=DIVIDER, height=1).grid(
    row=1, column=0, columnspan=len(COL_SPEC), sticky="ew")

# ── Table rows ────────────────────────────────────────────────────────────────
table_frame = tk.Frame(table_container, bg=BG_DETAIL)
table_frame.grid(row=2, column=0, columnspan=len(COL_SPEC), sticky="nsew")
table_container.rowconfigure(2, weight=1)

# Mirror header column widths inside the rows frame so they stay in sync
for col, (_, cw) in enumerate(COL_SPEC):
    table_frame.columnconfigure(col, minsize=cw * 7, weight=1 if col < 3 else 0)

def render_rows(data):
    for w in table_frame.winfo_children():
        w.destroy()

    for r_idx, cust in enumerate(data):
        row_bg = BG_TABLE_ROW if r_idx % 2 == 0 else BG_TABLE_ALT

        # Divider line
        tk.Frame(table_frame, bg=DIVIDER, height=1).grid(
            row=r_idx * 2, column=0, columnspan=len(COL_SPEC), sticky="ew")

        # Customer name
        tk.Label(table_frame, text=cust["name"],
                fg=TEXT_DARK, bg=row_bg,
                font=(FONT, 10), anchor="w",
                width=COL_SPEC[0][1]).grid(
            row=r_idx * 2 + 1, column=0, padx=(0, 8), pady=8, sticky="w")

        # Email
        tk.Label(table_frame, text=cust["email"],
                fg=TEXT_DARK, bg=row_bg,
                font=(FONT, 10), anchor="w",
                width=COL_SPEC[1][1]).grid(
            row=r_idx * 2 + 1, column=1, padx=(0, 8), pady=8, sticky="w")

        # Mobile
        tk.Label(table_frame, text=cust["mobile"],
                fg=TEXT_DARK, bg=row_bg,
                font=(FONT, 10), anchor="w",
                width=COL_SPEC[2][1]).grid(
            row=r_idx * 2 + 1, column=2, padx=(0, 8), pady=8, sticky="w")

        # Action button — canvas with rounded rect, redrawn with tags
        btn_canvas = tk.Canvas(table_frame, width=BTN_W, height=BTN_H,
                            bg=row_bg, highlightthickness=0, bd=0,
                            cursor="hand2")
        btn_canvas.grid(row=r_idx * 2 + 1, column=3, padx=(0, 4), pady=6, sticky="w")

        def _draw_btn(canvas, fill):
            canvas.delete("btn")
            rounded_rect(canvas, 0, 0, BTN_W, BTN_H, 5,
                        fill=fill, outline="#CCCCCC", tags="btn")
            canvas.create_text(BTN_W // 2, BTN_H // 2,
                                text="View Transaction History",
                                fill=TEXT_DARK, font=(FONT, 9), tags="btn")

        _draw_btn(btn_canvas, "#E8E8E8")

        def _make_handlers(canvas, customer):
            def on_enter(e):  _draw_btn(canvas, "#D0D0D0")
            def on_leave(e):  _draw_btn(canvas, "#E8E8E8")
            def on_click(e):  open_transaction_history(customer)
            return on_enter, on_leave, on_click

        on_enter, on_leave, on_click = _make_handlers(btn_canvas, cust)
        btn_canvas.bind("<Enter>",    on_enter)
        btn_canvas.bind("<Leave>",    on_leave)
        btn_canvas.bind("<Button-1>", on_click)

def on_search(*_):
    q = search_var.get().lower()
    if q == placeholder_text.lower():
        q = ""
    filtered = [c for c in CUSTOMERS
                if q in c["name"].lower()
                or q in c["email"].lower()
                or q in c["mobile"]]
    render_rows(filtered)

search_var.trace_add("write", on_search)
render_rows(CUSTOMERS)

root.mainloop()