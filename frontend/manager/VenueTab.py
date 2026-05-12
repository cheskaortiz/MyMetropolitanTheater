import tkinter as tk
from tkinter import ttk

# ── Colors ────────────────────────────────────────────────────────────────────
BG_MAIN      = "#B0B0B0"
BG_TOPBAR    = "#1E1E1E"
BG_SIDEBAR   = "#9A9A9A"
BG_SIDEBAR_H = "#888888"
BG_ACTIVE    = "#C8C8C8"
BG_PANEL     = "#F0F0F0"
BG_STAGE     = "#D0D0D0"
BG_INPUT     = "#E8E8E8"
BG_INPUT_HOV = "#DEDEDE"
SEAT_VIP     = "#E8C832"
SEAT_VIP_H   = "#CBA820"
SEAT_STD     = "#2ECC40"
SEAT_STD_H   = "#27AE34"
ACCENT       = "#CC1111"
ACCENT_HOV   = "#AA0000"
BTN_GREY     = "#DDDDDD"
BTN_GREY_H   = "#CCCCCC"
TEXT_LIGHT   = "#FFFFFF"
TEXT_DARK    = "#1A1A1A"
TEXT_MID     = "#555555"
TEXT_MUTED   = "#AAAAAA"
DIVIDER      = "#DDDDDD"

FONT   = "Helvetica"
RADIUS = 5
SW, SH = 40, 30   # seat width, height

nav_items = [
    ("📈", "Analytics"),
    ("💵", "Payroll"),
    ("📅", "Scheduler"),
    ("🏛",  "Venue"),
]

staff_data = [
    ("Production", "Mary Ruth",  ""),
    ("Production", "Francheska", ""),
    ("Production", "Eli Mistica",""),
]

# ── Seat type map: label -> "vip" or "std" ────────────────────────────────────
# Rows A & B = VIP (yellow), Rows C-E = Standard (green)
def seat_type(label):
    return "vip" if label[0] in ("A", "B") else "std"

# ── Helpers ───────────────────────────────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    canvas.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,  style="pieslice", **kw)
    canvas.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,  style="pieslice", **kw)
    canvas.create_rectangle(x1+r, y1,   x2-r, y2,   **kw)
    canvas.create_rectangle(x1,   y1+r, x2,   y2-r, **kw)

def make_canvas_btn(parent, text, command, w=90, h=26,
                    fill=BTN_GREY, fill_hov=BTN_GREY_H,
                    bg=BG_PANEL, fg=TEXT_DARK, font_size=9):
    c = tk.Canvas(parent, width=w, height=h, bg=bg, highlightthickness=0, bd=0)
    def draw(color):
        c.delete("all")
        rounded_rect(c, 0, 0, w, h, RADIUS, fill=color, outline=color)
        c.create_text(w//2, h//2, text=text, fill=fg, font=(FONT, font_size))
    draw(fill)
    c.bind("<Enter>",    lambda _: draw(fill_hov))
    c.bind("<Leave>",    lambda _: draw(fill))
    c.bind("<Button-1>", lambda _: command())
    c.config(cursor="hand2")
    return c

def make_seat(parent, label, bg_frame):
    stype  = seat_type(label)
    normal = SEAT_VIP   if stype == "vip" else SEAT_STD
    hover  = SEAT_VIP_H if stype == "vip" else SEAT_STD_H
    fg_col = TEXT_DARK  if stype == "vip" else TEXT_LIGHT

    c = tk.Canvas(parent, width=SW, height=SH, bg=bg_frame,
                highlightthickness=0, bd=0, cursor="hand2")

    def draw(col):
        c.delete("all")
        rounded_rect(c, 1, 1, SW-1, SH-1, RADIUS, fill=col, outline=col)
        c.create_text(SW//2, SH//2, text=label, fill=fg_col,
                    font=(FONT, 7, "bold"))

    draw(normal)
    c.bind("<Enter>",    lambda _: draw(hover))
    c.bind("<Leave>",    lambda _: draw(normal))
    return c

def center_on(win, parent, w, h):
    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width()  - w) // 2
    y = parent.winfo_y() + (parent.winfo_height() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

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
                    bg=TEXT_LIGHT, fg=TEXT_LIGHT, font_size=11).pack(side="left")

# ── Main window ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("My Metropolitan Theater")
root.geometry("1920x1080")
root.configure(bg=BG_MAIN)

style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground=BG_INPUT, background=BG_INPUT,
                foreground=TEXT_DARK, arrowcolor=TEXT_DARK)

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
    il = tk.Label(frame, text=icon, bg=bg,
                fg=ACCENT if is_active else TEXT_LIGHT,
                font=("Arial", 13), width=3)
    il.pack(side="left", padx=(10, 4), pady=12)
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
    make_nav_item(icon, label, is_active=(i == 3))   # Venue active

# ── Content ───────────────────────────────────────────────────────────────────
content = tk.Frame(body, bg=BG_MAIN)
content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

tk.Label(content, text="Venue and Inventory",
        fg=ACCENT, bg=BG_MAIN,
        font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))

two_col = tk.Frame(content, bg=BG_MAIN)
two_col.pack(fill="both", expand=True)

# ══ Left panel: Seat map ══════════════════════════════════════════════════════
left = tk.Frame(two_col, bg=BG_PANEL)
left.pack(side="left", fill="both", expand=True, padx=(0, 14))

seat_area = tk.Frame(left, bg=BG_PANEL)
seat_area.pack(fill="both", expand=True, padx=16, pady=16)

# STAGE banner
stage = tk.Frame(seat_area, bg=BG_STAGE, height=38)
stage.pack(fill="x", pady=(0, 16))
stage.pack_propagate(False)
tk.Label(stage, text="STAGE", bg=BG_STAGE, fg=TEXT_DARK,
        font=(FONT, 13, "bold")).place(relx=0.5, rely=0.5, anchor="center")

BG_ROW = BG_PANEL

def lbl(parent, text, w=2):
    return tk.Label(parent, text=text, bg=BG_ROW, fg=TEXT_MID,
                    font=(FONT, 9), width=w)

def add_seat_row(seats_left, row_label, seats_center, row_label2=None, seats_right=None):
    row = tk.Frame(seat_area, bg=BG_ROW)
    row.pack(pady=3)

    # Left gap seats
    if seats_left:
        for s in seats_left:
            make_seat(row, s, BG_ROW).pack(side="left", padx=2)
    # Left row label
    lbl(row, row_label).pack(side="left", padx=2)
    # Center seats
    for s in seats_center:
        make_seat(row, s, BG_ROW).pack(side="left", padx=2)
    # Right row label
    if row_label2:
        lbl(row, row_label2).pack(side="left", padx=2)
    # Right gap seats
    if seats_right:
        for s in seats_right:
            make_seat(row, s, BG_ROW).pack(side="left", padx=2)

# Row A — VIP (yellow), aisle in middle
add_seat_row(None,          "A", ["A1","A2","A3","A4"], "A")

# Row B — VIP
add_seat_row(["B1"],        "B", ["B2","B3","B4","B5"], "B", ["B6"])

# Row C — Standard (green)
add_seat_row(["C1","C2"],   "C", ["C3","C4","C5","C6"], "C", ["C7","C8"])

# Row D — Standard
add_seat_row(["D1","D2"],   "D", ["D3","D4","D5","D6"], "D", ["D7","D8"])

# Row E — Standard
add_seat_row(None,          "E", ["E1","E2","E3","E4"], "E")

# Legend
legend = tk.Frame(seat_area, bg=BG_ROW)
legend.pack(anchor="w", pady=(14, 0))

for color, label in [(SEAT_VIP, "VIP"), (SEAT_STD, "Standard")]:
    dot = tk.Canvas(legend, width=18, height=18, bg=BG_ROW, highlightthickness=0)
    dot.pack(side="left", padx=(0, 4))
    dot.create_rectangle(1, 1, 17, 17, fill=color, outline=color)
    tk.Label(legend, text=label, bg=BG_ROW, fg=TEXT_DARK,
            font=(FONT, 10)).pack(side="left", padx=(0, 16))

# ══ Right panel: Staff directory ══════════════════════════════════════════════
right = tk.Frame(two_col, bg=BG_PANEL, width=300)
right.pack(side="left", fill="y")
right.pack_propagate(False)

# Search bar
SEARCH_W = 260
s_outer = tk.Frame(right, bg=BG_PANEL)
s_outer.pack(fill="x", padx=16, pady=(16, 12))

s_c = tk.Canvas(s_outer, width=SEARCH_W, height=30,
                bg=BG_PANEL, highlightthickness=0, bd=0)
s_c.pack(fill="x")

def draw_sbg(col):
    s_c.delete("sbg")
    rounded_rect(s_c, 0, 0, SEARCH_W, 30, RADIUS,
                fill=col, outline=col, tags="sbg")
    s_c.tag_lower("sbg")

draw_sbg(BG_INPUT)
s_icon = tk.Label(s_c, text="🔍", bg=BG_INPUT, fg=TEXT_MID, font=("Arial", 10))
s_c.create_window(8, 15, anchor="w", window=s_icon)
s_e = tk.Entry(s_c, font=(FONT, 10), bg=BG_INPUT, fg=TEXT_MUTED,
            relief="flat", bd=0, insertbackground=TEXT_DARK, highlightthickness=0)
s_c.create_window(30, 15, anchor="w", window=s_e, width=SEARCH_W - 38)
s_e.insert(0, "Search")

def sf_in(_):
    if s_e.get() == "Search": s_e.delete(0, "end"); s_e.config(fg=TEXT_DARK)
def sf_out(_):
    if s_e.get() == "": s_e.insert(0, "Search"); s_e.config(fg=TEXT_MUTED)
s_e.bind("<FocusIn>", sf_in); s_e.bind("<FocusOut>", sf_out)

def s_in(_):  draw_sbg(BG_INPUT_HOV); s_icon.config(bg=BG_INPUT_HOV); s_e.config(bg=BG_INPUT_HOV)
def s_out(_): draw_sbg(BG_INPUT);     s_icon.config(bg=BG_INPUT);     s_e.config(bg=BG_INPUT)
for w in (s_c, s_e): w.bind("<Enter>", s_in); w.bind("<Leave>", s_out)

# Table headers
th = tk.Frame(right, bg=BG_PANEL)
th.pack(fill="x", padx=16, pady=(0, 4))
for h, cw in [("Department", 12), ("Manager", 12), ("Assigned Staff", 13)]:
    tk.Label(th, text=h, fg=ACCENT, bg=BG_PANEL,
            font=(FONT, 10, "bold"), width=cw, anchor="w").pack(side="left")

tk.Frame(right, bg=DIVIDER, height=1).pack(fill="x", padx=16)

# Staff rows
for i, (dept, mgr, _) in enumerate(staff_data):
    row_bg = "#FFFFFF" if i % 2 == 0 else "#F5F5F5"
    rw = tk.Frame(right, bg=row_bg)
    rw.pack(fill="x", padx=16)
    tk.Label(rw, text=dept, fg=TEXT_DARK, bg=row_bg,
            font=(FONT, 10), width=12, anchor="w").pack(side="left", pady=10)
    tk.Label(rw, text=mgr,  fg=TEXT_DARK, bg=row_bg,
            font=(FONT, 10), width=12, anchor="w").pack(side="left")
    make_canvas_btn(rw, "View Details", lambda: None,
                    w=84, h=24, fill=BTN_GREY, fill_hov=BTN_GREY_H,
                    bg=row_bg, fg=TEXT_DARK, font_size=9).pack(side="left", padx=4)
    tk.Frame(right, bg=DIVIDER, height=1).pack(fill="x", padx=16)

root.mainloop()