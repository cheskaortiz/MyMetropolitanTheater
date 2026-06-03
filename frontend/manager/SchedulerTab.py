import tkinter as tk
from tkinter import ttk

# ── Colors ────────────────────────────────────────────────────────────────────
BG_MAIN      = "#B0B0B0"
BG_TOPBAR    = "#1E1E1E"
BG_SIDEBAR   = "#9A9A9A"
BG_SIDEBAR_H = "#888888"
BG_ACTIVE    = "#C8C8C8"
BG_PANEL     = "#F0F0F0"
BG_INPUT     = "#E0E0E0"
BG_INPUT_HOV = "#D4D4D4"
ACCENT       = "#CC1111"
ACCENT_HOV   = "#AA0000"
TEXT_LIGHT   = "#FFFFFF"
TEXT_DARK    = "#1A1A1A"
TEXT_MID     = "#555555"
TEXT_MUTED   = "#AAAAAA"
DIVIDER      = "#DDDDDD"

FONT   = "Helvetica"
RADIUS = 6

nav_items = [
    ("📈", "Analytics"),
    ("💵", "Payroll"),
    ("📅", "Scheduler"),
    ("🏛",  "Venue"),
]

performances_preview = [
    "Jan 1 – 7 PM",
    "Jan 1 – 7 PM",
    "Jan 1 – 7 PM",
    "Jan 1 – 7 PM",
]

seat_pricing = [
    ("Orchestra", "A1", "Php 1000.00", ""),
    ("Section",   "A1", "Php 1000.00", ""),
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    canvas.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,  style="pieslice", **kw)
    canvas.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,  style="pieslice", **kw)
    canvas.create_rectangle(x1+r, y1,   x2-r, y2,   **kw)
    canvas.create_rectangle(x1,   y1+r, x2,   y2-r, **kw)

def make_canvas_btn(parent, text, command, w=160, h=34,
                    fill=ACCENT, fill_hov=ACCENT_HOV,
                    bg=BG_PANEL, fg=TEXT_LIGHT, font_size=10):
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

def make_rounded_entry(parent, width_px=300, bg_parent=BG_PANEL, height=30):
    PAD_X = RADIUS + 8
    c = tk.Canvas(parent, width=width_px, height=height,
                bg=bg_parent, highlightthickness=0, bd=0)
    def draw(color):
        c.delete("bg")
        rounded_rect(c, 0, 0, width_px, height, RADIUS,
                    fill=color, outline=color, tags="bg")
        c.tag_lower("bg")
    draw(BG_INPUT)
    entry = tk.Entry(c, font=(FONT, 10), bg=BG_INPUT, fg=TEXT_DARK,
                    relief="flat", bd=0, insertbackground=TEXT_DARK,
                    highlightthickness=0)
    c.create_window(PAD_X, height//2, anchor="w",
                    window=entry, width=width_px - PAD_X*2)
    def on_enter(_): draw(BG_INPUT_HOV); entry.config(bg=BG_INPUT_HOV)
    def on_leave(_): draw(BG_INPUT);     entry.config(bg=BG_INPUT)
    c.bind("<Enter>", on_enter); c.bind("<Leave>", on_leave)
    entry.bind("<Enter>", on_enter); entry.bind("<Leave>", on_leave)
    return c, entry

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
                    bg=TEXT_LIGHT).pack(side="left")

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
    make_nav_item(icon, label, is_active=(i == 2))   # Scheduler active

# ── Content ───────────────────────────────────────────────────────────────────
content = tk.Frame(body, bg=BG_MAIN)
content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

tk.Label(content, text="Master Scheduler",
        fg=ACCENT, bg=BG_MAIN,
        font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))

three_col = tk.Frame(content, bg=BG_MAIN)
three_col.pack(fill="both", expand=True)

# ══ Left panel: New Production ════════════════════════════════════════════════
left = tk.Frame(three_col, bg=BG_PANEL)
left.pack(side="left", fill="both", expand=True, padx=(0, 10))

tk.Label(left, text="New Production", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 13, "bold")).pack(anchor="w", padx=20, pady=(18, 14))

# Production Title
tk.Label(left, text="Production Title", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 10)).pack(anchor="w", padx=20)
pt_c, pt_e = make_rounded_entry(left, width_px=280, bg_parent=BG_PANEL, height=30)
pt_c.pack(anchor="w", padx=20, pady=(4, 16))

# Season Range
tk.Label(left, text="Season Range", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 10)).pack(anchor="w", padx=20)
sr_c, sr_e = make_rounded_entry(left, width_px=280, bg_parent=BG_PANEL, height=30)
sr_c.pack(anchor="w", padx=20, pady=(4, 0))

# Add New Production — pinned to bottom
add_bar = tk.Frame(left, bg=BG_PANEL)
add_bar.pack(side="bottom", pady=16, padx=20, anchor="w")
make_canvas_btn(add_bar, "Add New Production", lambda: None,
                w=180, h=34, fill=ACCENT, fill_hov=ACCENT_HOV, bg=BG_PANEL).pack()

# ══ Middle panel: Performance ═════════════════════════════════════════════════
mid = tk.Frame(three_col, bg=BG_PANEL)
mid.pack(side="left", fill="both", expand=True, padx=(0, 10))

tk.Label(mid, text="Performance", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 13, "bold")).pack(anchor="w", padx=20, pady=(18, 14))

# Time
tk.Label(mid, text="Time", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 10)).pack(anchor="w", padx=20)
ti_c, ti_e = make_rounded_entry(mid, width_px=280, bg_parent=BG_PANEL, height=30)
ti_c.pack(anchor="w", padx=20, pady=(4, 16))

# Date
tk.Label(mid, text="Date", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 10)).pack(anchor="w", padx=20)
da_c, da_e = make_rounded_entry(mid, width_px=280, bg_parent=BG_PANEL, height=30)
da_c.pack(anchor="w", padx=20, pady=(4, 16))

# Generate Performance button
make_canvas_btn(mid, "Generate Performance", lambda: None,
                w=190, h=34, fill=ACCENT, fill_hov=ACCENT_HOV, bg=BG_PANEL).pack(anchor="w", padx=20, pady=(0, 18))

tk.Frame(mid, bg=DIVIDER, height=1).pack(fill="x", padx=20)

# Performances Preview
tk.Label(mid, text="Performances Preview", fg=ACCENT, bg=BG_PANEL,
        font=(FONT, 11, "bold")).pack(anchor="w", padx=20, pady=(12, 6))

for perf in performances_preview:
    tk.Label(mid, text=perf, fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 10)).pack(anchor="w", padx=20, pady=2)

# ══ Right panel: Price Manager ════════════════════════════════════════════════
right = tk.Frame(three_col, bg=BG_PANEL)
right.pack(side="left", fill="both", expand=True)

tk.Label(right, text="Price Manager", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 13, "bold")).pack(anchor="w", padx=20, pady=(18, 12))

# Select Performance dropdown
perf_var = tk.StringVar(value="Select Performance")
perf_combo = ttk.Combobox(right, textvariable=perf_var,
                        values=["Select Performance", "Jan 1 – 7 PM", "Jan 2 – 7 PM"],
                        state="readonly", font=(FONT, 10), width=30)
perf_combo.pack(anchor="w", padx=20, pady=(0, 18))

tk.Frame(right, bg=DIVIDER, height=1).pack(fill="x", padx=20)

# Seat Pricing
tk.Label(right, text="Seat Pricing", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 11, "bold")).pack(anchor="w", padx=20, pady=(14, 8))

# Table headers
headers = ["Section", "Seat", "Price", "Status"]
col_ws  = [12, 8, 14, 10]

th_row = tk.Frame(right, bg=BG_PANEL)
th_row.pack(fill="x", padx=20, pady=(0, 4))
for h, cw in zip(headers, col_ws):
    tk.Label(th_row, text=h, fg=ACCENT, bg=BG_PANEL,
            font=(FONT, 10, "bold"), width=cw, anchor="w").pack(side="left")

tk.Frame(right, bg=DIVIDER, height=1).pack(fill="x", padx=20)

for i, (section, seat, price, status) in enumerate(seat_pricing):
    row_bg = TEXT_LIGHT if i % 2 == 0 else "#F5F5F5"
    rw = tk.Frame(right, bg=row_bg)
    rw.pack(fill="x", padx=20)
    for val, cw in zip([section, seat, price, status], col_ws):
        tk.Label(rw, text=val, fg=TEXT_DARK, bg=row_bg,
                font=(FONT, 10), width=cw, anchor="w").pack(side="left", pady=10)
    tk.Frame(right, bg=DIVIDER, height=1).pack(fill="x", padx=20)

# Set Price button — pinned to bottom
sp_bar = tk.Frame(right, bg=BG_PANEL)
sp_bar.pack(side="bottom", pady=16, padx=20, anchor="e")
make_canvas_btn(sp_bar, "Set Price", lambda: None,
                w=120, h=34, fill=ACCENT, fill_hov=ACCENT_HOV, bg=BG_PANEL).pack()

root.mainloop()