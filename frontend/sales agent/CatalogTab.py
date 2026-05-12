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

nav_items = [
    ("🎭", "Catalog"),
    ("🎟", "Sales"),
    ("👤", "Personnel"),
    ("💰", "Finances"),
    ("👥", "Customers"),
]

# ── Rounded rect helper ───────────────────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    canvas.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,  style="pieslice", **kw)
    canvas.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,  style="pieslice", **kw)
    canvas.create_rectangle(x1+r, y1,   x2-r, y2,   **kw)
    canvas.create_rectangle(x1,   y1+r, x2,   y2-r, **kw)

def make_canvas_btn(parent, text, command, w=80, h=32, fill=ACCENT, fill_hov=ACCENT_HOV,
                    bg=BG_MAIN, fg=TEXT_LIGHT, font_size=10):
    c = tk.Canvas(parent, width=w, height=h, bg=bg, highlightthickness=0, bd=0)
    def draw(color):
        c.delete("all")
        rounded_rect(c, 0, 0, w, h, RADIUS, fill=color, outline=color)
        c.create_text(w//2, h//2, text=text, fill=fg, font=(FONT, font_size, "bold"))
    draw(fill)
    c.bind("<Enter>",    lambda _: draw(fill_hov))
    c.bind("<Leave>",    lambda _: draw(fill))
    c.bind("<Button-1>", lambda _: command())
    c.config(cursor="hand2")
    return c

# ── Center a Toplevel over parent ─────────────────────────────────────────────
def center_on(win, parent, w, h):
    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width()  - w) // 2
    y = parent.winfo_y() + (parent.winfo_height() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

# ── Logout confirm dialog ─────────────────────────────────────────────────────
def open_logout_dialog():
    dlg = tk.Toplevel(root)
    dlg.title("")
    dlg.configure(bg=TEXT_LIGHT)
    dlg.resizable(False, False)
    dlg.transient(root)
    dlg.grab_set()
    center_on(dlg, root, 380, 240)

    # Icon circle
    icon_canvas = tk.Canvas(dlg, width=90, height=90, bg=TEXT_LIGHT, highlightthickness=0)
    icon_canvas.pack(pady=(28, 0))
    icon_canvas.create_oval(5, 5, 85, 85, fill="#EEEEEE", outline="#EEEEEE")
    icon_canvas.create_text(45, 47, text="⬛→", font=("Arial", 22), fill="#AAAAAA")

    tk.Label(
        dlg,
        text="Are you sure you want to logout?",
        fg=TEXT_DARK, bg=TEXT_LIGHT,
        font=(FONT, 13),
    ).pack(pady=(14, 20))

    btn_row = tk.Frame(dlg, bg=TEXT_LIGHT)
    btn_row.pack()

    # Cancel — outlined grey style
    cancel_btn = tk.Button(
        btn_row,
        text="Cancel",
        bg="#EEEEEE", fg=TEXT_DARK,
        font=(FONT, 11),
        relief="flat", bd=0,
        padx=18, pady=8,
        cursor="hand2",
        command=dlg.destroy,
        activebackground="#DDDDDD",
    )
    cancel_btn.pack(side="left", padx=(0, 12))

    make_canvas_btn(
        btn_row, "Logout", lambda: root.destroy(),
        w=90, h=36, fill=ACCENT, fill_hov=ACCENT_HOV, bg=TEXT_LIGHT,
    ).pack(side="left")

# ── Right panel detail: show production info + showtime table ─────────────────
def show_production_detail(prod):
    # Clear right panel
    for widget in right_panel.winfo_children():
        widget.destroy()

    container = tk.Frame(right_panel, bg=BG_DETAIL)
    container.pack(fill="both", expand=True, padx=24, pady=24)

    # Title
    tk.Label(
        container,
        text=f"Production Title: {prod['name']}",
        fg=ACCENT, bg=BG_DETAIL,
        font=(FONT, 17, "bold"),
        anchor="w",
    ).pack(anchor="w")

    tk.Label(
        container,
        text=f"Season: {prod['start']} – {prod['end']}",
        fg=TEXT_MID, bg=BG_DETAIL,
        font=(FONT, 11),
        anchor="w",
    ).pack(anchor="w", pady=(2, 18))

    # Table frame
    table = tk.Frame(container, bg=BG_DETAIL)
    table.pack(fill="x")

    headers = ["Date", "Time", "Total Seats", "Seats Available", "Status"]
    col_widths = [16, 12, 14, 18, 10]

    # Header row
    header_row = tk.Frame(table, bg=BG_DETAIL)
    header_row.pack(fill="x", pady=(0, 4))
    for col, (h, cw) in enumerate(zip(headers, col_widths)):
        tk.Label(
            header_row,
            text=h,
            fg=ACCENT, bg=BG_DETAIL,
            font=(FONT, 11, "bold"),
            width=cw, anchor="w",
        ).grid(row=0, column=col, padx=4, pady=6, sticky="w")

    # Divider
    tk.Frame(table, bg=DIVIDER, height=1).pack(fill="x")

    # Data rows
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
            tk.Label(
                data_row,
                text=val,
                fg=TEXT_DARK, bg=row_bg,
                font=(FONT, 11),
                width=cw, anchor="w",
            ).grid(row=0, column=col, padx=4, pady=10, sticky="w")

# ── Main window ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("My Metropolitan Theater")
root.geometry("1920x1080")
root.configure(bg=BG_MAIN)

# ── Top bar ───────────────────────────────────────────────────────────────────
topbar = tk.Frame(root, bg=BG_TOPBAR, height=45)
topbar.pack(fill="x", side="top")
topbar.pack_propagate(False)

tk.Label(
    topbar,
    text="MY METROPOLITAN THEATER",
    fg=ACCENT, bg=BG_TOPBAR,
    font=(FONT, 13, "bold"),
).pack(side="left", padx=18, pady=10)

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

for i, (icon, label) in enumerate(nav_items):
    make_nav_item(icon, label, is_active=(i == 0))

# ── Content ───────────────────────────────────────────────────────────────────
content = tk.Frame(body, bg=BG_MAIN)
content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

tk.Label(
    content,
    text="Productions and Scheduling",
    fg=ACCENT, bg=BG_MAIN,
    font=(FONT, 22, "bold"),
).pack(anchor="w", pady=(0, 14))

panels_row = tk.Frame(content, bg=BG_MAIN)
panels_row.pack(fill="both", expand=True)

# ── Left panel ────────────────────────────────────────────────────────────────
left_panel = tk.Frame(panels_row, bg=BG_LIST, width=310)
left_panel.pack(side="left", fill="y", padx=(0, 14))
left_panel.pack_propagate(False)

# Search
search_frame = tk.Frame(left_panel, bg=BG_SEARCH)
search_frame.pack(fill="x", padx=10, pady=(10, 6))
tk.Label(search_frame, text="🔍", bg=BG_SEARCH, fg=TEXT_MID,
        font=("Arial", 11)).pack(side="left", padx=(6, 2), pady=6)
search_entry = tk.Entry(search_frame, font=(FONT, 11), bg=BG_SEARCH, fg=TEXT_MID,
                        relief="flat", bd=0, insertbackground=TEXT_DARK)
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

selected_item = [None]

def make_list_item(idx, prod):
    name, ds, de = prod["name"], prod["start"], prod["end"]
    # Short display for list
    ds_short = ds.split(",")[0].replace("January", "Jan").replace("February", "Feb")
    de_short = de.split(",")[0].replace("January", "Jan").replace("February", "Feb")
    label_text = f"{idx}. {name} ({ds_short}–{de_short})"
    if len(label_text) > 44:
        label_text = label_text[:41] + "..."

    item = tk.Label(
        list_frame, text=label_text,
        bg=BG_LIST, fg=TEXT_DARK,
        font=(FONT, 11), anchor="w",
        cursor="hand2", padx=10, pady=8,
    )
    item.pack(fill="x")

    def on_select(_):
        # Reset all items
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

# EDIT / ADD / DELETE
btn_row = tk.Frame(content, bg=BG_MAIN)
btn_row.pack(anchor="w", pady=(10, 0))
for lbl in ["EDIT", "ADD", "DELETE"]:
    make_canvas_btn(btn_row, lbl, lambda: None, w=72, h=30, bg=BG_MAIN).pack(side="left", padx=(0, 8))

# ── Right panel ───────────────────────────────────────────────────────────────
right_panel = tk.Frame(panels_row, bg=BG_DETAIL)
right_panel.pack(side="left", fill="both", expand=True)

# Placeholder shown by default
placeholder = tk.Frame(right_panel, bg=BG_DETAIL)
placeholder.place(relx=0.5, rely=0.5, anchor="center")
tk.Label(
    placeholder,
    text="Select a production from the list to manage\nshowtimes or click 'Add' to create a season.",
    fg=TEXT_MUTED, bg=BG_DETAIL,
    font=(FONT, 13), justify="center",
).pack()

root.mainloop()