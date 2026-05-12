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
TEXT_LIGHT   = "#FFFFFF"
TEXT_DARK    = "#1A1A1A"
TEXT_MID     = "#555555"
TEXT_MUTED   = "#AAAAAA"
DIVIDER      = "#DDDDDD"

FONT    = "Helvetica"
RADIUS  = 10   # rounded corner radius for inputs

# ── Data ──────────────────────────────────────────────────────────────────────
departments = [
    "Productions",
    "Box Offices/Sales",
    "Venue Operations",
    "Management/Administration",
    "Human Resources",
    "Technical Crew",
]

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
    "STAFF-01": [
        ("10/01", "STAFF-01", "8.00"),
        ("10/02", "STAFF-01", "8.30"),
        ("10/03", "STAFF-01", "4.00"),
        ("10/04", "STAFF-01", "8.50"),
    ],
    "STAFF-02": [
        ("10/01", "STAFF-02", "7.00"),
        ("10/02", "STAFF-02", "8.00"),
    ],
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    canvas.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,  style="pieslice", **kw)
    canvas.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,  style="pieslice", **kw)
    canvas.create_rectangle(x1+r, y1,   x2-r, y2,   **kw)
    canvas.create_rectangle(x1,   y1+r, x2,   y2-r, **kw)

def make_rounded_entry(parent, width_px=180, bg_parent=BG_PANEL):
    """Canvas-backed rounded entry with inner padding so text never touches the edges."""
    H     = 36
    PAD_X = RADIUS + 10

    canvas = tk.Canvas(parent, width=width_px, height=H,
                    bg=bg_parent, highlightthickness=0, bd=0)

    def draw(color):
        canvas.delete("bg")
        rounded_rect(canvas, 0, 0, width_px, H, RADIUS,
                    fill=color, outline=color, tags="bg")
        canvas.tag_lower("bg")

    draw(BG_INPUT)

    entry = tk.Entry(canvas, font=(FONT, 10), bg=BG_INPUT, fg=TEXT_DARK,
                    relief="flat", bd=0, insertbackground=TEXT_DARK,
                    highlightthickness=0)
    canvas.create_window(PAD_X, H // 2, anchor="w",
                         window=entry, width=width_px - PAD_X * 2)

    def on_enter(_): draw(BG_INPUT_HOV); entry.config(bg=BG_INPUT_HOV)
    def on_leave(_): draw(BG_INPUT);     entry.config(bg=BG_INPUT)
    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    entry.bind("<Enter>",  on_enter)
    entry.bind("<Leave>",  on_leave)

    return canvas, entry

def make_canvas_btn(parent, text, command, w=120, h=32,
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

# ── Right-panel rendering ─────────────────────────────────────────────────────
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

    # ── Card 1: Employee info ─────────────────────────────────────────────────
    card1 = tk.Frame(inner, bg=BG_PANEL)
    card1.pack(fill="x", pady=(0, 10))

    top_row = tk.Frame(card1, bg=BG_PANEL)
    top_row.pack(fill="x", padx=20, pady=(16, 4))

    name_col = tk.Frame(top_row, bg=BG_PANEL)
    name_col.pack(side="left", fill="x", expand=True)
    tk.Label(name_col, text=emp["name"], fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 15, "bold"), anchor="w").pack(anchor="w")
    tk.Label(name_col, text=emp["role"], fg=TEXT_MID, bg=BG_PANEL,
            font=(FONT, 11), anchor="w").pack(anchor="w")

    dept_col = tk.Frame(top_row, bg=BG_PANEL)
    dept_col.pack(side="right")
    tk.Label(dept_col, text="Department", fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 10, "bold")).pack(anchor="e")

    dept_var   = tk.StringVar(value="Select")
    dept_combo = ttk.Combobox(dept_col, textvariable=dept_var,
                            values=["Select"] + departments,
                            state="readonly", font=(FONT, 10), width=18)
    dept_combo.set("Select")
    dept_combo.pack(anchor="e", pady=(4, 8))

    make_canvas_btn(dept_col, "Save Changes", lambda: None,
                    w=130, h=30, bg=BG_PANEL).pack(anchor="e")

    info_row = tk.Frame(card1, bg=BG_PANEL)
    info_row.pack(fill="x", padx=20, pady=(8, 16))

    id_col = tk.Frame(info_row, bg=BG_PANEL)
    id_col.pack(side="left", padx=(0, 60))
    tk.Label(id_col, text="ID", fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 10, "bold")).pack(anchor="w")
    tk.Label(id_col, text=emp["id"], fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 11)).pack(anchor="w")

    di_col = tk.Frame(info_row, bg=BG_PANEL)
    di_col.pack(side="left")
    tk.Label(di_col, text="Department", fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 10, "bold")).pack(anchor="w")
    tk.Label(di_col, text=emp["dept"], fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 11)).pack(anchor="w")

    # ── Card 2: Payroll ───────────────────────────────────────────────────────
    card2 = tk.Frame(inner, bg=BG_PANEL)
    card2.pack(fill="x", pady=(0, 10))

    tk.Label(card2, text="Payroll Information", fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 13, "bold")).pack(anchor="w", padx=20, pady=(16, 10))
    tk.Frame(card2, bg=DIVIDER, height=1).pack(fill="x", padx=20)

    pay_row = tk.Frame(card2, bg=BG_PANEL)
    pay_row.pack(fill="x", padx=20, pady=(14, 16))

    # Pay Type — combobox with "Select" default
    pt_col = tk.Frame(pay_row, bg=BG_PANEL)
    pt_col.pack(side="left", padx=(0, 30))
    tk.Label(pt_col, text="Pay Type", fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 10, "bold")).pack(anchor="w")
    pay_var   = tk.StringVar(value="Select")
    pay_combo = ttk.Combobox(pt_col, textvariable=pay_var,
                            values=["Select", "Hourly", "Monthly", "Contract"],
                            state="readonly", font=(FONT, 10), width=14)
    pay_combo.set("Select")
    pay_combo.pack(anchor="w", pady=(6, 0))

    # Hourly Rate — rounded entry
    hr_col = tk.Frame(pay_row, bg=BG_PANEL)
    hr_col.pack(side="left", padx=(0, 30))
    tk.Label(hr_col, text="Hourly Rate", fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 10, "bold")).pack(anchor="w")
    hr_canvas, hr_entry = make_rounded_entry(hr_col, width_px=160, bg_parent=BG_PANEL)
    hr_canvas.pack(pady=(6, 0))

    # Famous Level — rounded entry
    fl_col = tk.Frame(pay_row, bg=BG_PANEL)
    fl_col.pack(side="left")
    tk.Label(fl_col, text="Famous Level [1-5]", fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 10, "bold")).pack(anchor="w")
    fl_canvas, fl_entry = make_rounded_entry(fl_col, width_px=160, bg_parent=BG_PANEL)
    fl_canvas.pack(pady=(6, 0))

    # ── Card 3: Time Tracking ─────────────────────────────────────────────────
    card3 = tk.Frame(inner, bg=BG_PANEL)
    card3.pack(fill="x", pady=(0, 10))

    hdr = tk.Frame(card3, bg=BG_PANEL)
    hdr.pack(fill="x", padx=20, pady=(16, 10))
    tk.Label(hdr, text="Time Tracking", fg=TEXT_DARK, bg=BG_PANEL,
            font=(FONT, 13, "bold")).pack(side="left")

    btn_frame = tk.Frame(hdr, bg=BG_PANEL)
    btn_frame.pack(side="right")

    dr_var   = tk.StringVar(value="Date Range")
    dr_combo = ttk.Combobox(btn_frame, textvariable=dr_var,
                            values=["Date Range", "All", "This Week", "This Month", "Custom"],
                            state="readonly", font=(FONT, 10), width=12)
    dr_combo.set("Date Range")
    dr_combo.pack(side="left", padx=(0, 8))

    make_canvas_btn(btn_frame, "Add New Work Log", lambda: None,
                    w=140, h=30, bg=BG_PANEL).pack(side="left")

    tk.Frame(card3, bg=DIVIDER, height=1).pack(fill="x", padx=20)

    th_row = tk.Frame(card3, bg=BG_PANEL)
    th_row.pack(fill="x", padx=20, pady=(6, 2))
    for col_text, col_w in [("Date", 12), ("Staff ID", 16), ("Hours Worked", 16)]:
        tk.Label(th_row, text=col_text, fg=ACCENT, bg=BG_PANEL,
                font=(FONT, 10, "bold"), width=col_w, anchor="w").pack(side="left")

    tk.Frame(card3, bg=DIVIDER, height=1).pack(fill="x", padx=20)

    logs = time_logs.get(emp["id"], [])
    for i, (date, sid, hrs) in enumerate(logs):
        row_bg = TEXT_LIGHT if i % 2 == 0 else BG_TABLE_ALT
        rw = tk.Frame(card3, bg=row_bg)
        rw.pack(fill="x", padx=20)
        for val, cw in [(date, 12), (sid, 16), (hrs, 16)]:
            tk.Label(rw, text=val, fg=TEXT_DARK, bg=row_bg,
                    font=(FONT, 10), width=cw, anchor="w").pack(side="left", pady=8)
        tk.Frame(card3, bg=DIVIDER, height=1).pack(fill="x", padx=20)

    tk.Frame(card3, height=12, bg=BG_PANEL).pack()

# ── Main window ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("My Metropolitan Theater")
root.geometry("1920x1080")
root.configure(bg=BG_MAIN)

# ttk style
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

nav_items  = [("🎭","Catalog"),("🎟","Sales"),("👤","Personnel"),("💰","Finances"),("👥","Customers")]
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
    make_nav_item(icon, label, is_active=(i == 2))

# ── Content ───────────────────────────────────────────────────────────────────
content = tk.Frame(body, bg=BG_MAIN)
content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

tk.Label(content, text="Staff and Payroll",
        fg=ACCENT, bg=BG_MAIN,
        font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))

main_row = tk.Frame(content, bg=BG_MAIN)
main_row.pack(fill="both", expand=True)

# ── Left panel: Employee Directory ────────────────────────────────────────────
left_panel = tk.Frame(main_row, bg=BG_PANEL, width=270)
left_panel.pack(side="left", fill="y", padx=(0, 12))
left_panel.pack_propagate(False)

tk.Label(left_panel, text="Employee Directory", fg=TEXT_DARK, bg=BG_PANEL,
        font=(FONT, 12, "bold")).pack(anchor="w", padx=16, pady=(16, 8))

# Search bar — rounded
search_outer = tk.Frame(left_panel, bg=BG_PANEL)
search_outer.pack(fill="x", padx=16, pady=(0, 12))

s_canvas = tk.Canvas(search_outer, height=34, bg=BG_PANEL,
                    highlightthickness=0, bd=0)
s_canvas.pack(fill="x")

def draw_search_bg(color):
    s_canvas.delete("sbg")
    w = s_canvas.winfo_width() or 230
    rounded_rect(s_canvas, 0, 0, w, 34, RADIUS,
                fill=color, outline=color, tags="sbg")
    s_canvas.tag_lower("sbg")

s_canvas.bind("<Configure>", lambda _: draw_search_bg(BG_INPUT))

icon_lbl = tk.Label(s_canvas, text="🔍", bg=BG_INPUT, fg=TEXT_MID,
                    font=("Arial", 10))
s_canvas.create_window(10, 17, anchor="w", window=icon_lbl)

search_entry = tk.Entry(s_canvas, font=(FONT, 10), bg=BG_INPUT,
                        fg=TEXT_MID, relief="flat", bd=0,
                        insertbackground=TEXT_DARK, highlightthickness=0)
search_entry.insert(0, "Search")
s_canvas.create_window(32, 17, anchor="w", window=search_entry, width=170)

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

# ── Scrollable accordion list ─────────────────────────────────────────────────
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

# ── Accordion — each dept row + its employee sub-list packed together ─────────
dept_open        = {}
selected_emp_row = [None]
selected_emp_lbl = [None]

def toggle_dept(dept, emp_container, arrow_lbl):
    dept_open[dept] = not dept_open.get(dept, False)
    if dept_open[dept]:
        emp_container.pack(fill="x", after=arrow_lbl.master)
        arrow_lbl.config(text="∧")
    else:
        emp_container.pack_forget()
        arrow_lbl.config(text="∨")

for dept in departments:
    dept_open[dept] = False

    # Wrapper keeps dept_row + emp_container together
    wrapper = tk.Frame(dir_inner, bg=BG_PANEL)
    wrapper.pack(fill="x", pady=2, padx=8)

    dept_row = tk.Frame(wrapper, bg=BG_INPUT, cursor="hand2")
    dept_row.pack(fill="x")

    dept_lbl = tk.Label(dept_row, text=dept, bg=BG_INPUT, fg=TEXT_DARK,
                        font=(FONT, 10), anchor="w")
    dept_lbl.pack(side="left", padx=8, pady=8, fill="x", expand=True)

    arrow = tk.Label(dept_row, text="∨", bg=BG_INPUT, fg=TEXT_MID,
                    font=(FONT, 10))
    arrow.pack(side="right", padx=8)

    # Employee container lives inside the same wrapper, below dept_row
    emp_container = tk.Frame(wrapper, bg=BG_PANEL)
    # hidden initially — pack on toggle

    for emp_data in employees.get(dept, []):
        e = emp_data
        emp_row = tk.Frame(emp_container, bg=BG_PANEL, cursor="hand2")
        emp_row.pack(fill="x")
        emp_lbl = tk.Label(emp_row, text=f"  • {e['name']}", bg=BG_PANEL,
                            fg=TEXT_DARK, font=(FONT, 9), anchor="w")
        emp_lbl.pack(side="left", padx=12, pady=5, fill="x", expand=True)

        def on_click(_, emp=e, er=emp_row, el=emp_lbl):
            # Reset previous highlight
            if selected_emp_row[0]:
                selected_emp_row[0].config(bg=BG_PANEL)
            if selected_emp_lbl[0]:
                selected_emp_lbl[0].config(bg=BG_PANEL)
            er.config(bg="#E0E0E0")
            el.config(bg="#E0E0E0")
            selected_emp_row[0] = er
            selected_emp_lbl[0] = el
            show_employee(emp)

        for w in (emp_row, emp_lbl):
            w.bind("<Button-1>", on_click)
            w.bind("<Enter>", lambda _, r=emp_row, l=emp_lbl:
                (r.config(bg="#E8E8E8"), l.config(bg="#E8E8E8"))
                if r != selected_emp_row[0] else None)
            w.bind("<Leave>", lambda _, r=emp_row, l=emp_lbl:
                (r.config(bg=BG_PANEL), l.config(bg=BG_PANEL))
                if r != selected_emp_row[0] else None)

    # Bind toggle to dept row widgets
    for w in (dept_row, dept_lbl, arrow):
        w.bind("<Button-1>",
            lambda _, d=dept, ec=emp_container, a=arrow: toggle_dept(d, ec, a))
        w.bind("<Enter>", lambda _, r=dept_row, l=dept_lbl, ar=arrow:
            (r.config(bg=BG_SIDEBAR_H), l.config(bg=BG_SIDEBAR_H), ar.config(bg=BG_SIDEBAR_H)))
        w.bind("<Leave>", lambda _, r=dept_row, l=dept_lbl, ar=arrow:
            (r.config(bg=BG_INPUT), l.config(bg=BG_INPUT), ar.config(bg=BG_INPUT)))

# ── Right panel ───────────────────────────────────────────────────────────────
right_panel = tk.Frame(main_row, bg=BG_MAIN)
right_panel.pack(side="left", fill="both", expand=True)

placeholder = tk.Frame(right_panel, bg=BG_MAIN)
placeholder.place(relx=0.5, rely=0.5, anchor="center")
tk.Label(placeholder, text="Select an employee from the directory\nto view their details.",
        fg=TEXT_MUTED, bg=BG_MAIN, font=(FONT, 13), justify="center").pack()

root.after(100, lambda: show_employee(employees["Productions"][0]))

root.mainloop()