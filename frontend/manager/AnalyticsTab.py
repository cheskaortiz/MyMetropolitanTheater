import tkinter as tk
from tkinter import ttk

# ── Colors ────────────────────────────────────────────────────────────────────
BG_MAIN      = "#B0B0B0"
BG_TOPBAR    = "#1E1E1E"
BG_SIDEBAR   = "#9A9A9A"
BG_SIDEBAR_H = "#888888"
BG_ACTIVE    = "#C8C8C8"
BG_PANEL     = "#F0F0F0"
BG_BAR       = "#8B0000"
BG_BAR_TRACK = "#CCCCCC"
BG_BTN_GREY  = "#CCCCCC"
BG_BTN_HOV   = "#BBBBBB"
ACCENT       = "#CC1111"
ACCENT_HOV   = "#AA0000"
TEXT_LIGHT   = "#FFFFFF"
TEXT_DARK    = "#1A1A1A"
TEXT_MID     = "#555555"
TEXT_MUTED   = "#AAAAAA"
DIVIDER      = "#DDDDDD"

FONT   = "Helvetica"
RADIUS = 3

# ── Data ──────────────────────────────────────────────────────────────────────
profitability = [
    ("Hamilton", 1000),
    ("Wicked",   1000),
]

ledger = [
    ("T1001", "2026-01-01", "Hamilton", "2026-01-01 19:00", "Php 1000.00"),
    ("T1001", "2026-01-01", "Hamilton", "2026-01-01 19:00", "Php 1000.00"),
]

occupancy = [
    ("T1001", 50),
    ("T1001", 50),
]

nav_items = [
    ("📈", "Analytics"),
    ("💵", "Payroll"),
    ("📅", "Scheduler"),
    ("🏛",  "Venue"),
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    canvas.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,  style="pieslice", **kw)
    canvas.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,  style="pieslice", **kw)
    canvas.create_rectangle(x1+r, y1,   x2-r, y2,   **kw)
    canvas.create_rectangle(x1,   y1+r, x2,   y2-r, **kw)

def make_canvas_btn(parent, text, command, w=70, h=26,
                    fill=BG_BTN_GREY, fill_hov=BG_BTN_HOV,
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
    make_nav_item(icon, label, is_active=(i == 0))

# ── Content ───────────────────────────────────────────────────────────────────
content = tk.Frame(body, bg=BG_MAIN)
content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

tk.Label(content, text="Revenue and Analytics",
        fg=ACCENT, bg=BG_MAIN,
        font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))

# Scrollable content
scroll_canvas = tk.Canvas(content, bg=BG_MAIN, highlightthickness=0, bd=0)
scrollbar     = ttk.Scrollbar(content, orient="vertical", command=scroll_canvas.yview)
scroll_canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
scroll_canvas.pack(side="left", fill="both", expand=True)

inner  = tk.Frame(scroll_canvas, bg=BG_MAIN)
win_id = scroll_canvas.create_window((0, 0), window=inner, anchor="nw")

def on_cfg(_):
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
    scroll_canvas.itemconfig(win_id, width=scroll_canvas.winfo_width())
inner.bind("<Configure>", on_cfg)
scroll_canvas.bind("<Configure>", lambda e: scroll_canvas.itemconfig(win_id, width=e.width))

# ══ Card 1: Production Profitability ══════════════════════════════════════════
card1 = tk.Frame(inner, bg=BG_PANEL)
card1.pack(fill="x", pady=(0, 12))

tk.Label(card1, text="Production Profitability", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 13, "bold")).pack(anchor="w", padx=20, pady=(16, 10))

chart_row = tk.Frame(card1, bg=BG_PANEL)
chart_row.pack(fill="x", padx=20, pady=(0, 16))

# Bar chart canvas
BAR_W   = 480
BAR_H   = 220
MAX_VAL = max(v for _, v in profitability) or 1
BAR_WID = 140
BAR_GAP = 160
Y_STEPS = 8
Y_AXIS  = 50

bar_canvas = tk.Canvas(chart_row, width=BAR_W, height=BAR_H,
                        bg=BG_PANEL, highlightthickness=0, bd=0)
bar_canvas.pack(side="left")

def draw_bar_chart():
    bar_canvas.delete("all")
    chart_h = BAR_H - 40   # leave room for x labels and top
    chart_y0 = BAR_H - 30

    # Y-axis labels
    for i in range(Y_STEPS + 1):
        val  = int(MAX_VAL * i / Y_STEPS)
        y    = chart_y0 - int(chart_h * i / Y_STEPS)
        bar_canvas.create_text(Y_AXIS - 4, y, text=f"Php {val:,}.00",
                                anchor="e", font=(FONT, 7), fill=TEXT_MID)
        bar_canvas.create_line(Y_AXIS, y, BAR_W, y, fill=DIVIDER, dash=(2, 4))

    # Bars
    for idx, (name, val) in enumerate(profitability):
        x0 = Y_AXIS + 10 + idx * BAR_GAP
        x1 = x0 + BAR_WID
        bar_h = int(chart_h * val / MAX_VAL)
        y0 = chart_y0 - bar_h
        y1 = chart_y0
        bar_canvas.create_rectangle(x0, y0, x1, y1, fill=BG_BAR, outline=BG_BAR)
        bar_canvas.create_text((x0 + x1) // 2, chart_y0 + 12,
                                text=name, font=(FONT, 9), fill=TEXT_DARK)

draw_bar_chart()

# Legend
legend_frame = tk.Frame(chart_row, bg=BG_PANEL)
legend_frame.pack(side="left", padx=30, anchor="n", pady=10)

header_row = tk.Frame(legend_frame, bg=BG_PANEL)
header_row.pack(anchor="w")
tk.Label(header_row, text="Production", fg=ACCENT, bg=BG_PANEL,
        font=(FONT, 10, "bold"), width=14, anchor="w").pack(side="left")
tk.Label(header_row, text="Total Revenue", fg=ACCENT, bg=BG_PANEL,
        font=(FONT, 10, "bold"), width=14, anchor="w").pack(side="left")

tk.Frame(legend_frame, bg=DIVIDER, height=1).pack(fill="x", pady=4)

for name, val in profitability:
    row = tk.Frame(legend_frame, bg=BG_PANEL)
    row.pack(anchor="w", pady=2)
    tk.Label(row, text=name, fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 10), width=14, anchor="w").pack(side="left")
    tk.Label(row, text=f"Php {val:,}.00", fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 10), width=14, anchor="w").pack(side="left")

# ══ Card 2: Daily Ledger Audit ════════════════════════════════════════════════
card2 = tk.Frame(inner, bg=BG_PANEL)
card2.pack(fill="x", pady=(0, 12))

tk.Label(card2, text="Daily Ledger Audit", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 13, "bold")).pack(anchor="w", padx=20, pady=(16, 8))

# Table headers
headers = ["Transaction ID", "Date", "Production", "Performance", "Amount", "Actions"]
col_ws  = [16, 12, 12, 18, 12, 10]

th_row = tk.Frame(card2, bg=BG_PANEL)
th_row.pack(fill="x", padx=20, pady=(0, 4))
for h, cw in zip(headers, col_ws):
    tk.Label(th_row, text=h, fg=ACCENT, bg=BG_PANEL,
            font=(FONT, 10, "bold"), width=cw, anchor="w").pack(side="left")

tk.Frame(card2, bg=DIVIDER, height=1).pack(fill="x", padx=20)

for i, (txn, date, prod, perf, amt) in enumerate(ledger):
    row_bg = TEXT_LIGHT if i % 2 == 0 else "#F5F5F5"
    rw = tk.Frame(card2, bg=row_bg)
    rw.pack(fill="x", padx=20)
    for val, cw in zip([txn, date, prod, perf, amt], col_ws[:-1]):
        tk.Label(rw, text=val, fg=TEXT_DARK, bg=row_bg,
                font=(FONT, 10), width=cw, anchor="w").pack(side="left", pady=10)
    make_canvas_btn(rw, "Refund", lambda: None,
                    w=60, h=24, bg=row_bg).pack(side="left", padx=4)
    tk.Frame(card2, bg=DIVIDER, height=1).pack(fill="x", padx=20)

tk.Frame(card2, height=12, bg=BG_PANEL).pack()

# ══ Card 3: Occupancy Rates ═══════════════════════════════════════════════════
card3 = tk.Frame(inner, bg=BG_PANEL)
card3.pack(fill="x", pady=(0, 12))

tk.Label(card3, text="Occupancy Rates", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 13, "bold")).pack(anchor="w", padx=20, pady=(16, 12))

OCC_W = 680   # total track width

for label, pct in occupancy:
    row = tk.Frame(card3, bg=BG_PANEL)
    row.pack(fill="x", padx=20, pady=6)

    tk.Label(row, text=label, fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 10), width=6, anchor="w").pack(side="left", padx=(0, 10))

    # Track canvas
    track = tk.Canvas(row, width=OCC_W, height=20,
                    bg=BG_PANEL, highlightthickness=0, bd=0)
    track.pack(side="left")
    fill_w = int(OCC_W * pct / 100)
    # Background track
    track.create_rectangle(0, 4, OCC_W, 16, fill=BG_BAR_TRACK, outline=BG_BAR_TRACK)
    # Filled portion
    if fill_w > 0:
        track.create_rectangle(0, 4, fill_w, 16, fill=BG_BAR, outline=BG_BAR)

    tk.Label(row, text=f"{pct}%", fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 10)).pack(side="left", padx=(10, 0))

tk.Frame(card3, height=16, bg=BG_PANEL).pack()

# ttk style
style = ttk.Style()
style.theme_use("clam")

root.mainloop()