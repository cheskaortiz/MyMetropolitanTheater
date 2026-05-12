import tkinter as tk
from tkinter import ttk

# ── Colors ────────────────────────────────────────────────────────────────────
BG_MAIN      = "#B0B0B0"
BG_TOPBAR    = "#1E1E1E"
BG_SIDEBAR   = "#9A9A9A"
BG_SIDEBAR_H = "#888888"
BG_ACTIVE    = "#C8C8C8"
BG_PANEL     = "#EFEFEF"
BG_STAGE     = "#D0D0D0"
BG_RECEIPT   = "#F8F8F8"
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
DIVIDER      = "#CCCCCC"

FONT   = "Helvetica"
RADIUS = 5

# ── Seat layout (row label, [seat labels], row label) ─────────────────────────
# None = aisle gap
seat_layout = [
    ("A", ["A1","A2","A3","A4"], "A"),
    ("B", ["B1","B2","B3","B4","B5"], "B", "B6"),
    ("C", ["C1","C2"], "C", ["C3","C4","C5","C6"], "C", ["C7","C8"]),
    ("D", ["D1","D2"], "D", ["D3","D4","D5","D6"], "D", ["D7","D8"]),
    ("E", ["E1","E2","E3","E4"], "E"),
]

# Pre-mark some seats as sold for demo
SOLD_SEATS = set()  # start all available; click to toggle

# ── Productions ───────────────────────────────────────────────────────────────
productions = [
    "Hamlet — Jan 10, 7:00 PM",
    "Hamlet — Jan 11, 7:00 PM",
    "The Phantom of the Opera — Jan 15, 7:00 PM",
    "The Phantom of the Opera — Jan 16, 7:00 PM",
]

# ── State ─────────────────────────────────────────────────────────────────────
selected_seats  = []   # list of seat labels currently selected
seat_buttons    = {}   # seat_label -> canvas widget
seat_states     = {}   # seat_label -> "available" | "sold"

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
        rounded_rect(c, 0, 0, w, h, RADIUS, fill=color, outline=color)
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

# ── Logout dialog ─────────────────────────────────────────────────────────────
def open_logout_dialog():
    dlg = tk.Toplevel(root)
    dlg.title("")
    dlg.configure(bg=TEXT_LIGHT)
    dlg.resizable(False, False)
    dlg.transient(root)
    dlg.grab_set()
    center_on(dlg, root, 380, 240)

    ic = tk.Canvas(dlg, width=90, height=90, bg=TEXT_LIGHT, highlightthickness=0)
    ic.pack(pady=(28, 0))
    ic.create_oval(5, 5, 85, 85, fill="#EEEEEE", outline="#EEEEEE")
    ic.create_text(45, 47, text="⬛→", font=("Arial", 22), fill="#AAAAAA")

    tk.Label(dlg, text="Are you sure you want to logout?",
            fg=TEXT_DARK, bg=TEXT_LIGHT, font=(FONT, 13)).pack(pady=(14, 20))

    br = tk.Frame(dlg, bg=TEXT_LIGHT)
    br.pack()
    tk.Button(br, text="Cancel", bg="#EEEEEE", fg=TEXT_DARK,
            font=(FONT, 11), relief="flat", bd=0, padx=18, pady=8,
            cursor="hand2", command=dlg.destroy,
            activebackground="#DDDDDD").pack(side="left", padx=(0, 12))
    make_canvas_btn(br, "Logout", root.destroy,
                    w=90, h=36, fill=ACCENT, fill_hov=ACCENT_HOV,
                    bg=TEXT_LIGHT).pack(side="left")

# ── Seat button ───────────────────────────────────────────────────────────────
SW, SH = 46, 36   # seat width, height

def make_seat(parent, label, bg_frame):
    state = seat_states.get(label, "available")
    c = tk.Canvas(parent, width=SW, height=SH, bg=bg_frame,
                highlightthickness=0, bd=0, cursor="hand2")

    def color_for(s):
        if s == "sold":      return SEAT_SOLD,  SEAT_SOLD_H
        if s == "selected":  return SEAT_SEL,   SEAT_SEL_H
        return SEAT_AVAIL, SEAT_AVAIL_H

    def draw(hover=False):
        s = seat_states.get(label, "available")
        normal, hov = color_for(s)
        col = hov if hover else normal
        c.delete("all")
        rounded_rect(c, 1, 1, SW-1, SH-1, RADIUS, fill=col, outline=col)
        c.create_text(SW//2, SH//2, text=label, fill=TEXT_LIGHT,
                    font=(FONT, 8, "bold"))

    def on_click(_):
        s = seat_states.get(label, "available")
        if s == "sold":
            return   # can't select already-sold seats
        if s == "available":
            seat_states[label] = "selected"
            if label not in selected_seats:
                selected_seats.append(label)
        else:  # selected → back to available
            seat_states[label] = "available"
            if label in selected_seats:
                selected_seats.remove(label)
        draw()
        update_receipt()

    c.bind("<Enter>",    lambda _: draw(hover=True))
    c.bind("<Leave>",    lambda _: draw(hover=False))
    c.bind("<Button-1>", on_click)
    draw()
    seat_buttons[label] = c
    return c

# ── Receipt panel update ──────────────────────────────────────────────────────
receipt_seat_var  = None
receipt_prod_var  = None

def update_receipt():
    if receipt_seat_var:
        seats_txt = ", ".join(selected_seats) if selected_seats else "—"
        receipt_seat_var.set(f"Seat(s): {seats_txt}")
    if receipt_prod_var:
        prod = production_var.get()
        receipt_prod_var.set(f"Production: {prod if prod != 'Select' else '—'}")

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

nav_items  = [("🎭","Catalog"),("🎟","Sales"),("👤","Personnel"),("💰","Finances"),("👥","Customers")]
active_nav = [None]

def make_nav_item(icon, label, is_active=False):
    bg = BG_ACTIVE if is_active else BG_SIDEBAR
    frame = tk.Frame(sidebar, bg=bg, cursor="hand2")
    frame.pack(fill="x")
    il = tk.Label(frame, text=icon, bg=bg,
                fg=ACCENT if is_active else TEXT_LIGHT,
                font=("Arial", 13), width=3)
    il.pack(side="left", padx=(10,4), pady=12)
    tl = tk.Label(frame, text=label, bg=bg,
                fg=ACCENT if is_active else TEXT_LIGHT,
                font=(FONT, 12, "bold" if is_active else "normal"))
    tl.pack(side="left")
    def on_enter(_):
        if frame != active_nav[0]:
            for w in (frame, il, tl): w.config(bg=BG_SIDEBAR_H)
    def on_leave(_):
        if frame != active_nav[0]:
            for w in (frame, il, tl): w.config(bg=BG_SIDEBAR)
    for w in (frame, il, tl):
        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)
    if is_active:
        active_nav[0] = frame

for i, (icon, label) in enumerate(nav_items):
    make_nav_item(icon, label, is_active=(i == 1))   # Sales active

# ── Content ───────────────────────────────────────────────────────────────────
content = tk.Frame(body, bg=BG_MAIN)
content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

tk.Label(content, text="Box Office (Ticketing)",
        fg=ACCENT, bg=BG_MAIN,
        font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))

main_row = tk.Frame(content, bg=BG_MAIN)
main_row.pack(fill="both", expand=True)

# ── Left: production selector + seat map ─────────────────────────────────────
left_col = tk.Frame(main_row, bg=BG_PANEL)
left_col.pack(side="left", fill="both", expand=True, padx=(0, 14))

# Production dropdown
prod_header = tk.Frame(left_col, bg=BG_PANEL)
prod_header.pack(fill="x", padx=16, pady=(14, 8))

tk.Label(prod_header, text="Production", bg=BG_PANEL,
        fg=TEXT_DARK, font=(FONT, 12, "bold")).pack(anchor="w")

production_var = tk.StringVar(value="Select")
prod_menu = ttk.Combobox(prod_header, textvariable=production_var,
                        values=productions, state="readonly",
                        font=(FONT, 11), width=34)
prod_menu.pack(anchor="w", pady=(4, 0))
prod_menu.bind("<<ComboboxSelected>>", lambda _: update_receipt())

# Style the combobox
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground=BG_PANEL, background=BG_PANEL,
                foreground=TEXT_DARK, arrowcolor=TEXT_DARK)

# ── Seat map ─────────────────────────────────────────────────────────────────
seat_area = tk.Frame(left_col, bg=BG_PANEL)
seat_area.pack(fill="both", expand=True, padx=16, pady=(4, 16))

# STAGE banner
stage_frame = tk.Frame(seat_area, bg=BG_STAGE, height=38)
stage_frame.pack(fill="x", pady=(0, 18))
stage_frame.pack_propagate(False)
tk.Label(stage_frame, text="STAGE", bg=BG_STAGE, fg=TEXT_DARK,
        font=(FONT, 13, "bold")).place(relx=0.5, rely=0.5, anchor="center")

# Each row
BG_ROW = BG_PANEL

def add_row_A():
    row = tk.Frame(seat_area, bg=BG_ROW)
    row.pack(pady=4)
    tk.Label(row, text="A", bg=BG_ROW, fg=TEXT_MID, font=(FONT,10), width=2).pack(side="left")
    for lbl in ["A1","A2","A3","A4"]:
        seat_states[lbl] = "available"
        make_seat(row, lbl, BG_ROW).pack(side="left", padx=3)
    tk.Label(row, text="A", bg=BG_ROW, fg=TEXT_MID, font=(FONT,10), width=2).pack(side="left")

def add_row_B():
    row = tk.Frame(seat_area, bg=BG_ROW)
    row.pack(pady=4)
    tk.Label(row, text=" ", bg=BG_ROW, width=2).pack(side="left")
    seat_states["B1"] = "available"
    make_seat(row, "B1", BG_ROW).pack(side="left", padx=3)
    tk.Label(row, text="B", bg=BG_ROW, fg=TEXT_MID, font=(FONT,10), width=2).pack(side="left")
    for lbl in ["B2","B3","B4","B5"]:
        seat_states[lbl] = "available"
        make_seat(row, lbl, BG_ROW).pack(side="left", padx=3)
    tk.Label(row, text="B", bg=BG_ROW, fg=TEXT_MID, font=(FONT,10), width=2).pack(side="left")
    seat_states["B6"] = "available"
    make_seat(row, "B6", BG_ROW).pack(side="left", padx=3)

def add_row_C():
    row = tk.Frame(seat_area, bg=BG_ROW)
    row.pack(pady=4)
    for lbl in ["C1","C2"]:
        seat_states[lbl] = "available"
        make_seat(row, lbl, BG_ROW).pack(side="left", padx=3)
    tk.Label(row, text="C", bg=BG_ROW, fg=TEXT_MID, font=(FONT,10), width=2).pack(side="left")
    for lbl in ["C3","C4","C5","C6"]:
        seat_states[lbl] = "available"
        make_seat(row, lbl, BG_ROW).pack(side="left", padx=3)
    tk.Label(row, text="C", bg=BG_ROW, fg=TEXT_MID, font=(FONT,10), width=2).pack(side="left")
    for lbl in ["C7","C8"]:
        seat_states[lbl] = "available"
        make_seat(row, lbl, BG_ROW).pack(side="left", padx=3)

def add_row_D():
    row = tk.Frame(seat_area, bg=BG_ROW)
    row.pack(pady=4)
    for lbl in ["D1","D2"]:
        seat_states[lbl] = "available"
        make_seat(row, lbl, BG_ROW).pack(side="left", padx=3)
    tk.Label(row, text="D", bg=BG_ROW, fg=TEXT_MID, font=(FONT,10), width=2).pack(side="left")
    for lbl in ["D3","D4","D5","D6"]:
        seat_states[lbl] = "available"
        make_seat(row, lbl, BG_ROW).pack(side="left", padx=3)
    tk.Label(row, text="D", bg=BG_ROW, fg=TEXT_MID, font=(FONT,10), width=2).pack(side="left")
    for lbl in ["D7","D8"]:
        seat_states[lbl] = "available"
        make_seat(row, lbl, BG_ROW).pack(side="left", padx=3)

def add_row_E():
    row = tk.Frame(seat_area, bg=BG_ROW)
    row.pack(pady=4)
    tk.Label(row, text="E", bg=BG_ROW, fg=TEXT_MID, font=(FONT,10), width=2).pack(side="left")
    for lbl in ["E1","E2","E3","E4"]:
        seat_states[lbl] = "available"
        make_seat(row, lbl, BG_ROW).pack(side="left", padx=3)
    tk.Label(row, text="E", bg=BG_ROW, fg=TEXT_MID, font=(FONT,10), width=2).pack(side="left")

add_row_A()
add_row_B()
add_row_C()
add_row_D()
add_row_E()

# Legend
legend = tk.Frame(seat_area, bg=BG_ROW)
legend.pack(anchor="w", pady=(12, 0))

for color, label in [(SEAT_AVAIL, "Available"), (SEAT_SOLD, "Sold"), (SEAT_SEL, "Selected")]:
    dot = tk.Canvas(legend, width=18, height=18, bg=BG_ROW, highlightthickness=0)
    dot.pack(side="left", padx=(0, 4))
    dot.create_rectangle(2, 2, 16, 16, fill=color, outline=color)
    tk.Label(legend, text=label, bg=BG_ROW, fg=TEXT_DARK,
            font=(FONT, 10)).pack(side="left", padx=(0, 14))

# ── Right: receipt panel ──────────────────────────────────────────────────────
receipt_panel = tk.Frame(main_row, bg=BG_RECEIPT, width=240)
receipt_panel.pack(side="left", fill="y")
receipt_panel.pack_propagate(False)

def label_receipt(text, bold=False, size=9, fg=TEXT_DARK, pady=0):
    tk.Label(receipt_panel, text=text, bg=BG_RECEIPT, fg=fg,
            font=(FONT, size, "bold" if bold else "normal"),
            justify="center", wraplength=210).pack(pady=pady)

def divider_receipt():
    tk.Label(receipt_panel, text="- " * 22, bg=BG_RECEIPT,
            fg=DIVIDER, font=(FONT, 7)).pack()

tk.Frame(receipt_panel, height=18, bg=BG_RECEIPT).pack()
label_receipt("My Metropolitan Theater", bold=True, size=10)
label_receipt("OFFICIAL RECEIPT", bold=False, size=9, fg=TEXT_MID)
tk.Frame(receipt_panel, height=6, bg=BG_RECEIPT).pack()

label_receipt("Transaction ID: #TXN-0001")
label_receipt("Date: May 10, 2026")
label_receipt("Staff: Maria Santos (ID: ST-001)")
tk.Frame(receipt_panel, height=4, bg=BG_RECEIPT).pack()
divider_receipt()
label_receipt("CUSTOMER DETAILS", bold=True, size=9, fg=TEXT_MID)
divider_receipt()
tk.Frame(receipt_panel, height=4, bg=BG_RECEIPT).pack()
label_receipt("Name: Juan Dela Cruz")
label_receipt("Email: juandelacruz@email.com")
label_receipt("Mobile: 0912-345-6789")
tk.Frame(receipt_panel, height=4, bg=BG_RECEIPT).pack()
divider_receipt()
label_receipt("TICKET INFORMATION", bold=True, size=9, fg=TEXT_MID)
divider_receipt()
tk.Frame(receipt_panel, height=4, bg=BG_RECEIPT).pack()
label_receipt("Ticket No: TKT-1025")

receipt_prod_var = tk.StringVar(value="Production: —")
tk.Label(receipt_panel, textvariable=receipt_prod_var,
        bg=BG_RECEIPT, fg=TEXT_DARK,
        font=(FONT, 9), justify="center", wraplength=210).pack()

label_receipt("Performance: May 20, 2026 at 7:00 PM")

receipt_seat_var = tk.StringVar(value="Seat(s): —")
tk.Label(receipt_panel, textvariable=receipt_seat_var,
        bg=BG_RECEIPT, fg=TEXT_DARK,
        font=(FONT, 9), justify="center", wraplength=210).pack()

label_receipt("Status: Paid")
tk.Frame(receipt_panel, height=4, bg=BG_RECEIPT).pack()
divider_receipt()
label_receipt("PAYMENT SUMMARY", bold=True, size=9, fg=TEXT_MID)
divider_receipt()
tk.Frame(receipt_panel, height=4, bg=BG_RECEIPT).pack()
label_receipt("Payment Method: Cash")
label_receipt("Total Amount: ₱1,500.00")

root.mainloop()