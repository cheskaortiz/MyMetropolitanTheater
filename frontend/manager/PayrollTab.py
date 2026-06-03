import tkinter as tk
from tkinter import ttk

# ── Colors ────────────────────────────────────────────────────────────────────
BG_MAIN      = "#B0B0B0"
BG_TOPBAR    = "#1E1E1E"
BG_SIDEBAR   = "#9A9A9A"
BG_SIDEBAR_H = "#888888"
BG_ACTIVE    = "#C8C8C8"
BG_PANEL     = "#F0F0F0"
BG_INPUT     = "#E8E8E8"
BG_INPUT_HOV = "#DEDEDE"
BG_TABLE_ALT = "#F5F5F5"
ACCENT       = "#CC1111"
ACCENT_HOV   = "#AA0000"
BTN_GREEN    = "#27AE60"
BTN_GREEN_H  = "#1E8449"
BTN_GREY     = "#AAAAAA"
BTN_GREY_H   = "#888888"
BTN_RED      = "#CC1111"
BTN_RED_H    = "#AA0000"
TEXT_LIGHT   = "#FFFFFF"
TEXT_DARK    = "#1A1A1A"
TEXT_MID     = "#555555"
TEXT_MUTED   = "#AAAAAA"
DIVIDER      = "#DDDDDD"

FONT   = "Helvetica"
RADIUS = 6

# ── Data ──────────────────────────────────────────────────────────────────────
departments = [
    "Productions", "Box Offices/Sales", "Venue Operations",
    "Management/Administration", "Human Resources", "Technical Crew",
]

employees = {
    "Productions": [
        {"name": "Mary Ruth Cathryn Suello", "role": "Lead Producer",  "id": "STAFF-01"},
        {"name": "Jose Miguel Santos",        "role": "Stage Director", "id": "STAFF-02"},
    ],
    "Box Offices/Sales": [
        {"name": "Ana Reyes",   "role": "Box Office Head", "id": "STAFF-03"},
        {"name": "Carlo Dizon", "role": "Sales Associate", "id": "STAFF-04"},
    ],
    "Venue Operations":          [{"name": "Lito Fernandez", "role": "Venue Manager",  "id": "STAFF-05"}],
    "Management/Administration": [{"name": "Grace Dela Cruz","role": "Admin Officer",  "id": "STAFF-06"}],
    "Human Resources":           [{"name": "Patricia Lim",   "role": "HR Manager",     "id": "STAFF-07"}],
    "Technical Crew": [
        {"name": "Ramon Cruz",  "role": "Lighting Tech", "id": "STAFF-08"},
        {"name": "Ella Torres", "role": "Sound Tech",    "id": "STAFF-09"},
    ],
}

payroll_data = [
    ("STAFF-01", "Hourly", "8 hrs + Bonus", "Php 1000.00"),
    ("STAFF-01", "Hourly", "8 hrs + Bonus", "Php 1000.00"),
]

work_logs = [
    "STAFF-01: 8.0 h, 2026-01-01",
    "STAFF-01: 8.0 h, 2026-01-01",
    "STAFF-01: 8.0 h, 2026-01-01",
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

def make_canvas_btn(parent, text, command, w=110, h=32,
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

def make_icon_btn(parent, text, fill, fill_hov, command, bg=BG_PANEL):
    c = tk.Canvas(parent, width=22, height=22, bg=bg,
                highlightthickness=0, bd=0, cursor="hand2")
    def draw(color):
        c.delete("all")
        c.create_rectangle(0, 0, 22, 22, fill=color, outline=color)
        c.create_text(11, 11, text=text, fill=TEXT_LIGHT,
                    font=("Arial", 11, "bold"))
    draw(fill)
    c.bind("<Enter>",    lambda _: draw(fill_hov))
    c.bind("<Leave>",    lambda _: draw(fill))
    c.bind("<Button-1>", lambda _: command())
    return c

def make_rounded_entry(parent, width_px=200, bg_parent=BG_PANEL, height=32):
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
    make_nav_item(icon, label, is_active=(i == 1))

# ── Content ───────────────────────────────────────────────────────────────────
content = tk.Frame(body, bg=BG_MAIN)
content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

tk.Label(content, text="Personnel and Payroll",
        fg=ACCENT, bg=BG_MAIN,
        font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))

three_col = tk.Frame(content, bg=BG_MAIN)
three_col.pack(fill="both", expand=True)

# ══ Left panel: Employee Directory ═══════════════════════════════════════════
left = tk.Frame(three_col, bg=BG_PANEL, width=290)
left.pack(side="left", fill="y", padx=(0, 10))
left.pack_propagate(False)

tk.Label(left, text="Employee Directory", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 12, "bold")).pack(anchor="w", padx=16, pady=(16, 8))

# Search — rounded with 🔍 icon
SEARCH_W = 240
s_outer  = tk.Frame(left, bg=BG_PANEL)
s_outer.pack(fill="x", padx=16, pady=(0, 10))
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

# ID field — rounded
id_row = tk.Frame(left, bg=BG_PANEL)
id_row.pack(fill="x", padx=16, pady=(0, 10))
tk.Label(id_row, text="ID:", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 10, "bold")).pack(side="left", padx=(0, 6))
id_c, id_e = make_rounded_entry(id_row, width_px=190, bg_parent=BG_PANEL, height=28)
id_c.pack(side="left")

tk.Label(left, text="Departments", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 11, "bold")).pack(anchor="w", padx=16, pady=(4, 8))

# Scrollable dept accordion
dir_c  = tk.Canvas(left, bg=BG_PANEL, highlightthickness=0, bd=0)
dir_sb = ttk.Scrollbar(left, orient="vertical", command=dir_c.yview)
dir_c.configure(yscrollcommand=dir_sb.set)
dir_sb.pack(side="right", fill="y")
dir_c.pack(side="left", fill="both", expand=True)

dir_inner = tk.Frame(dir_c, bg=BG_PANEL)
dir_win   = dir_c.create_window((0, 0), window=dir_inner, anchor="nw")
def on_dir_cfg(_):
    dir_c.configure(scrollregion=dir_c.bbox("all"))
    dir_c.itemconfig(dir_win, width=dir_c.winfo_width())
dir_inner.bind("<Configure>", on_dir_cfg)
dir_c.bind("<Configure>", lambda e: dir_c.itemconfig(dir_win, width=e.width))

dept_open        = {}
sel_emp_row      = [None]
sel_emp_lbl      = [None]

def toggle_dept(dept, emp_cont, arrow):
    dept_open[dept] = not dept_open.get(dept, False)
    if dept_open[dept]:
        emp_cont.pack(fill="x", after=arrow.master)
        arrow.config(text="∧")
    else:
        emp_cont.pack_forget()
        arrow.config(text="∨")

for dept in departments:
    dept_open[dept] = False
    wrapper  = tk.Frame(dir_inner, bg=BG_PANEL)
    wrapper.pack(fill="x", pady=2, padx=6)

    dept_row = tk.Frame(wrapper, bg=BG_INPUT, cursor="hand2")
    dept_row.pack(fill="x")
    d_lbl = tk.Label(dept_row, text=dept, bg=BG_INPUT, fg=TEXT_DARK,
                    font=(FONT, 10), anchor="w")
    d_lbl.pack(side="left", padx=8, pady=7, fill="x", expand=True)
    arrow = tk.Label(dept_row, text="∨", bg=BG_INPUT, fg=TEXT_MID, font=(FONT, 10))
    arrow.pack(side="right", padx=8)

    emp_cont = tk.Frame(wrapper, bg=BG_PANEL)

    for ed in employees.get(dept, []):
        e = ed
        er = tk.Frame(emp_cont, bg=BG_PANEL, cursor="hand2")
        er.pack(fill="x")
        el = tk.Label(er, text=f"  • {e['name']}", bg=BG_PANEL,
                    fg=TEXT_DARK, font=(FONT, 9), anchor="w")
        el.pack(side="left", padx=10, pady=4, fill="x", expand=True)

        def on_emp(_, emp=e, r=er, l=el):
            if sel_emp_row[0]: sel_emp_row[0].config(bg=BG_PANEL)
            if sel_emp_lbl[0]: sel_emp_lbl[0].config(bg=BG_PANEL)
            r.config(bg="#E0E0E0"); l.config(bg="#E0E0E0")
            sel_emp_row[0] = r; sel_emp_lbl[0] = l
            id_e.delete(0, "end"); id_e.insert(0, emp["id"])

        for w in (er, el):
            w.bind("<Button-1>", on_emp)
            w.bind("<Enter>", lambda _, r=er, l=el:
                (r.config(bg="#E8E8E8"), l.config(bg="#E8E8E8")) if r != sel_emp_row[0] else None)
            w.bind("<Leave>", lambda _, r=er, l=el:
                (r.config(bg=BG_PANEL), l.config(bg=BG_PANEL)) if r != sel_emp_row[0] else None)

    for w in (dept_row, d_lbl, arrow):
        w.bind("<Button-1>", lambda _, d=dept, ec=emp_cont, a=arrow: toggle_dept(d, ec, a))
        w.bind("<Enter>", lambda _, r=dept_row, l=d_lbl, a=arrow:
            (r.config(bg=BG_SIDEBAR_H), l.config(bg=BG_SIDEBAR_H), a.config(bg=BG_SIDEBAR_H)))
        w.bind("<Leave>", lambda _, r=dept_row, l=d_lbl, a=arrow:
            (r.config(bg=BG_INPUT), l.config(bg=BG_INPUT), a.config(bg=BG_INPUT)))

# Update Profile / Discard — inside scrollable area, below dropdowns
btn_bar = tk.Frame(dir_inner, bg=BG_PANEL)
btn_bar.pack(fill="x", pady=14, padx=8)
make_canvas_btn(btn_bar, "Update Profile", lambda: None,
                w=118, h=32, fill=ACCENT, fill_hov=ACCENT_HOV, bg=BG_PANEL).pack(side="left", padx=(0, 8))
make_canvas_btn(btn_bar, "Discard", lambda: None,
                w=80, h=32, fill=ACCENT, fill_hov=ACCENT_HOV, bg=BG_PANEL).pack(side="left")

# ══ Middle panel: Payroll Overview ════════════════════════════════════════════
mid = tk.Frame(three_col, bg=BG_PANEL)
mid.pack(side="left", fill="both", expand=True, padx=(0, 10))

tk.Label(mid, text="Payroll Overview", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 13, "bold")).pack(anchor="w", padx=20, pady=(16, 10))
tk.Frame(mid, bg=DIVIDER, height=1).pack(fill="x", padx=20)

# Table headers
headers = ["Staff ID", "Type", "Work Hours/Details", "Pay"]
col_ws  = [10, 8, 18, 12]
th = tk.Frame(mid, bg=BG_PANEL)
th.pack(fill="x", padx=20, pady=(8, 4))
for h, cw in zip(headers, col_ws):
    tk.Label(th, text=h, fg=ACCENT, bg=BG_PANEL,
            font=(FONT, 10, "bold"), width=cw, anchor="w").pack(side="left")

tk.Frame(mid, bg=DIVIDER, height=1).pack(fill="x", padx=20)

for i, (sid, ptype, details, pay) in enumerate(payroll_data):
    row_bg = TEXT_LIGHT if i % 2 == 0 else BG_TABLE_ALT
    rw = tk.Frame(mid, bg=row_bg)
    rw.pack(fill="x", padx=20)
    for val, cw in zip([sid, ptype, details, pay], col_ws):
        tk.Label(rw, text=val, fg=TEXT_DARK, bg=row_bg,
                font=(FONT, 10), width=cw, anchor="w").pack(side="left", pady=10)
    tk.Frame(mid, bg=DIVIDER, height=1).pack(fill="x", padx=20)

# ══ Right panel: Work Log Actions ════════════════════════════════════════════
right = tk.Frame(three_col, bg=BG_PANEL, width=280)
right.pack(side="left", fill="y")
right.pack_propagate(False)

tk.Label(right, text="Work Log Actions", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 13, "bold")).pack(anchor="w", padx=16, pady=(16, 10))
tk.Frame(right, bg=DIVIDER, height=1).pack(fill="x", padx=16)

for i, log in enumerate(work_logs):
    row_bg = TEXT_LIGHT if i % 2 == 0 else BG_TABLE_ALT
    rw = tk.Frame(right, bg=row_bg)
    rw.pack(fill="x", padx=16, pady=2)

    tk.Label(rw, text=log, fg=TEXT_DARK, bg=row_bg,
            font=(FONT, 9), anchor="w").pack(side="left", fill="x",
                                            expand=True, pady=8)

    # ✓ approve
    make_icon_btn(rw, "✓", BTN_GREEN, BTN_GREEN_H, lambda: None, bg=row_bg).pack(side="left", padx=2)
    # ✎ edit
    make_icon_btn(rw, "✎", BTN_GREY,  BTN_GREY_H,  lambda: None, bg=row_bg).pack(side="left", padx=2)
    # ✕ delete
    make_icon_btn(rw, "✕", BTN_RED,   BTN_RED_H,   lambda: None, bg=row_bg).pack(side="left", padx=2)

    tk.Frame(right, bg=DIVIDER, height=1).pack(fill="x", padx=16)

# Process All Logs button — bottom right
proc_bar = tk.Frame(right, bg=BG_PANEL)
proc_bar.pack(side="bottom", pady=14, padx=16, anchor="e")
make_canvas_btn(proc_bar, "Process All Logs", lambda: None,
                w=140, h=32, fill=ACCENT, fill_hov=ACCENT_HOV, bg=BG_PANEL).pack()

root.mainloop()