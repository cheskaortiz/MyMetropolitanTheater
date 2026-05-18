import os
import sys
import tkinter as tk
from tkinter import messagebox
from datetime import datetime 

# ── Backend Path Fix (same as personnel tab) ──────────────────────────────────
def setup_backend_path():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    for _ in range(8):
        backend_start = os.path.join(current_dir, "backend", "start_database.py")
        if os.path.exists(backend_start):
            root_dir    = current_dir
            backend_dir = os.path.join(root_dir, "backend")
            if root_dir    not in sys.path: sys.path.insert(0, root_dir)
            if backend_dir not in sys.path: sys.path.insert(0, backend_dir)
            return True
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            break
        current_dir = parent_dir
    return False

setup_backend_path()

BACKEND_IMPORT_ERROR = None
try:
    from backend.start_database import start_database
except Exception as e:
    start_database        = None
    BACKEND_IMPORT_ERROR  = e

try:
    from backend.objects.production import Production
except Exception:
    class Production:
        def __init__(self, title=None, startDate=None, endDate=None, productionId=None):
            self.productionId = productionId
            self.title        = title
            self.startDate    = startDate
            self.endDate      = endDate

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
BG_TABLE_ALT = "#F9F9F9"
ACCENT       = "#CC1111"
ACCENT_HOV   = "#AA0000"
TEXT_LIGHT   = "#FFFFFF"
TEXT_DARK    = "#1A1A1A"
TEXT_MID     = "#555555"
TEXT_MUTED   = "#AAAAAA"
DIVIDER      = "#DDDDDD"
BTN_GREY     = "#888888"
BTN_GREY_HOV = "#666666"

FONT   = "Helvetica"
RADIUS = 3

nav_items = [
    ("🎭", "Catalog"),
    ("🎟", "Sales"),
    ("👤", "Personnel"),
    ("💰", "Finances"),
    ("👥", "Customers"),
]

db                    = None
BACKEND_RUNTIME_ERROR = None

def connect_backend():
    global db, BACKEND_RUNTIME_ERROR
    if start_database is None:
        BACKEND_RUNTIME_ERROR = BACKEND_IMPORT_ERROR
        return None
    try:
        db = start_database()
        return db
    except Exception as e:
        BACKEND_RUNTIME_ERROR = e
        return None

connect_backend()

# ── Shared widget helpers ──────────────────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    canvas.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,  style="pieslice", **kw)
    canvas.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,  style="pieslice", **kw)
    canvas.create_rectangle(x1+r, y1,   x2-r, y2,   **kw)
    canvas.create_rectangle(x1,   y1+r, x2,   y2-r, **kw)

def make_canvas_btn(parent, text, command, w=80, h=28,
                    fill=ACCENT, fill_hov=ACCENT_HOV,
                    bg=BG_MAIN, fg=TEXT_LIGHT, font_size=9):
    c = tk.Canvas(parent, width=w, height=h, bg=bg, highlightthickness=0, bd=0)

    def draw(color):
        c.delete("all")
        rounded_rect(c, 0, 0, w, h, RADIUS, fill=color, outline=color)
        c.create_text(w // 2, h // 2, text=text, fill=fg,
                      font=(FONT, font_size, "bold"))

    draw(fill)
    c.bind("<Enter>",    lambda _: draw(fill_hov))
    c.bind("<Leave>",    lambda _: draw(fill))
    c.bind("<Button-1>", lambda e: [command(), "break"][1])
    c.config(cursor="hand2")
    return c

def center_on(win, parent, w, h):
    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width()  - w) // 2
    y = parent.winfo_y() + (parent.winfo_height() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

def open_logout_dialog(root):
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

# ══════════════════════════════════════════════════════════════════════════════
#  CATALOG TAB
# ══════════════════════════════════════════════════════════════════════════════
def build_catalog_tab(parent, root):
    selected = {"data": None}

    # ── page heading ──────────────────────────────────────────────────────────
    tk.Label(parent, text="Productions and Scheduling",
             fg=ACCENT, bg=BG_MAIN,
             font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))

    # ── top action bar ────────────────────────────────────────────────────────
    top_bar = tk.Frame(parent, bg=BG_MAIN)
    top_bar.pack(fill="x", pady=(0, 10))

    tk.Label(top_bar, text="All Productions", fg=TEXT_DARK, bg=BG_MAIN,
             font=(FONT, 13, "bold")).pack(side="left")

    make_canvas_btn(
        top_bar, "+ ADD PRODUCTION", lambda: open_add_dialog(root),
        w=160, h=32, fill=ACCENT, fill_hov=ACCENT_HOV, bg=BG_MAIN
    ).pack(side="right")

    # ── two-column layout ─────────────────────────────────────────────────────
    panels_row = tk.Frame(parent, bg=BG_MAIN)
    panels_row.pack(fill="both", expand=True)

    # ══ LEFT: production list ═════════════════════════════════════════════════
    left_panel = tk.Frame(panels_row, bg=BG_LIST, width=340)
    left_panel.pack(side="left", fill="y", padx=(0, 14))
    left_panel.pack_propagate(False)

    sf = tk.Frame(left_panel, bg=BG_SEARCH)
    sf.pack(fill="x", padx=10, pady=(10, 6))
    tk.Label(sf, text="🔍", bg=BG_SEARCH, fg=TEXT_MID,
             font=("Arial", 11)).pack(side="left", padx=(8, 2), pady=6)
    
    search_var = tk.StringVar()
    se = tk.Entry(sf, textvariable=search_var, font=(FONT, 11),
                  bg=BG_SEARCH, fg=TEXT_MID, relief="flat", bd=0,
                  insertbackground=TEXT_DARK)
    se.insert(0, "Search")
    se.pack(side="left", fill="x", expand=True, pady=6, padx=4)

    def sf_in(_):
        if se.get() == "Search":
            se.delete(0, "end")
            se.config(fg=TEXT_DARK)
    def sf_out(_):
        if se.get() == "":
            se.insert(0, "Search")
            se.config(fg=TEXT_MID)
            
    se.bind("<FocusIn>",  sf_in)
    se.bind("<FocusOut>", sf_out)

    tk.Frame(left_panel, bg=DIVIDER, height=1).pack(fill="x", padx=10)

    # scrollable list
    lc = tk.Canvas(left_panel, bg=BG_LIST, highlightthickness=0, bd=0)
    ls = tk.Scrollbar(left_panel, orient="vertical", command=lc.yview)
    lc.configure(yscrollcommand=ls.set)
    ls.pack(side="right", fill="y")
    lc.pack(side="left", fill="both", expand=True)
    list_frame = tk.Frame(lc, bg=BG_LIST)
    lf_id = lc.create_window((0, 0), window=list_frame, anchor="nw")

    def on_lf_cfg(e):
        lc.configure(scrollregion=lc.bbox("all"))
        lc.itemconfig(lf_id, width=lc.winfo_width())
    list_frame.bind("<Configure>", on_lf_cfg)
    lc.bind("<Configure>", lambda e: lc.itemconfig(lf_id, width=e.width))

    # ══ RIGHT: detail panel ═══════════════════════════════════════════════════
    right_panel = tk.Frame(panels_row, bg=BG_DETAIL)
    right_panel.pack(side="left", fill="both", expand=True)

    def show_placeholder():
        for w in right_panel.winfo_children():
            w.destroy()
        ph = tk.Frame(right_panel, bg=BG_DETAIL)
        ph.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(ph,
                 text="Select a production from the list\n"
                      "to view showtimes and details.\n\n"
                      "Click  '+ ADD PRODUCTION'  to create a new one.",
                 fg=TEXT_MUTED, bg=BG_DETAIL,
                 font=(FONT, 13), justify="center").pack()

    show_placeholder()

    def show_error(msg):  messagebox.showerror("Error",   msg, parent=root)
    def show_info(msg):   messagebox.showinfo ("Success", msg, parent=root)

    def backend_ok():
        if db is None:
            show_error(f"Backend not connected.\n{BACKEND_RUNTIME_ERROR or BACKEND_IMPORT_ERROR}")
            return False
        return True

    # ── refresh left list ─────────────────────────────────────────────────────
    def refresh_list(filter_text=""):
        for w in list_frame.winfo_children():
            w.destroy()

        if not backend_ok():
            tk.Label(list_frame, text="Backend not connected.\nCheck terminal for details.",
                     fg=ACCENT, bg=BG_LIST, font=(FONT, 10),
                     justify="left", wraplength=260).pack(anchor="w", padx=12, pady=12)
            return

        result = db.service.production.viewAllProductions()

        if isinstance(result, str):
            tk.Label(list_frame, text=result, fg=TEXT_MUTED, bg=BG_LIST, font=(FONT, 11)).pack(pady=20)
            return

        ft = filter_text.strip().lower()
        filtered = [p for p in result if ft in p["title"].lower()] if ft and ft != "search" else result

        if not filtered:
            tk.Label(list_frame, text="No productions found.", fg=TEXT_MUTED, bg=BG_LIST, font=(FONT, 11)).pack(pady=20)
            return

        for idx, prod in enumerate(filtered, 1):
            _make_list_item(idx, prod)

    search_var.trace_add("write", lambda *_: refresh_list(search_var.get()))

    # ── build one list row ────────────────────────────────────────────────────
    def _make_list_item(idx, prod):
        title = prod["title"]
        start = prod.get("start_date", prod.get("startDate", ""))
        end   = prod.get("end_date",   prod.get("endDate", ""))

        wrapper = tk.Frame(list_frame, bg=BG_LIST, cursor="hand2")
        wrapper.pack(fill="x")
        tk.Frame(wrapper, bg=DIVIDER, height=1).pack(fill="x")

        row = tk.Frame(wrapper)
        row.pack(fill="x", padx=4)

        badge = tk.Label(row, text=str(idx), fg=TEXT_LIGHT, bg=ACCENT,
                         font=(FONT, 8, "bold"), width=3, anchor="center")
        badge.pack(side="left", padx=(6, 8), pady=12)

        text_col = tk.Frame(row)
        text_col.pack(side="left", fill="x", expand=True)

        short = title if len(title) <= 24 else title[:21] + "..."
        title_lbl = tk.Label(text_col, text=short, fg=TEXT_DARK,
                             font=(FONT, 10, "bold"), anchor="w")
        title_lbl.pack(anchor="w")

        date_lbl = tk.Label(text_col, text=f"{start} – {end}", fg=TEXT_MID,
                            font=(FONT, 8), anchor="w")
        date_lbl.pack(anchor="w")

        # ── Sleek and Smaller Action Buttons ──
        btn_col = tk.Frame(row, bg=BG_LIST)
        btn_col.pack(side="right", padx=(4, 2))

        edit_btn = make_canvas_btn(
            btn_col, "Edit", lambda p=prod: open_edit_dialog(p, root),
            w=36, h=18, fill=BTN_GREY, fill_hov=BTN_GREY_HOV, bg=BG_LIST, font_size=8
        )
        edit_btn.pack(pady=(0, 2))

        del_btn = make_canvas_btn(
            btn_col, "Del", lambda p=prod: do_delete(p),
            w=36, h=18, fill=ACCENT, fill_hov=ACCENT_HOV, bg=BG_LIST, font_size=8
        )
        del_btn.pack()

        def set_row_color(container, color):
            container.config(bg=color)
            for child in container.winfo_children():
                # Target the inner row layout holding the text
                if child == row:
                    child.config(bg=color)
                    for gchild in child.winfo_children():
                        # Keep the number badge box safely red
                        if gchild == badge:
                            gchild.config(bg=ACCENT, fg=TEXT_LIGHT)
                        # Force the title label and date label to perfectly match the row color
                        elif isinstance(gchild, tk.Label):
                            gchild.config(bg=color)
                elif not isinstance(child, tk.Canvas):
                    child.config(bg=color)

        def on_select(_prod=prod, _wrapper=wrapper):
            # Reset backgrounds of all items back to native default list style
            for w in list_frame.winfo_children():
                if isinstance(w, tk.Frame):
                    set_row_color(w, BG_LIST)
            
            selected["data"] = _prod
            set_row_color(_wrapper, "#E0E0E0")  # Persistent selection styling
            show_detail(_prod)

        def on_hover(enter, _wrapper=wrapper, _prod=prod):
            if selected["data"] == _prod:
                return
            col = "#EBEBEB" if enter else BG_LIST
            set_row_color(_wrapper, col)

        # Bind row selectors explicitly to all UI visual text tracks to fix block clicks
        for widget in (wrapper, row, text_col, title_lbl, date_lbl, badge):
            widget.bind("<Button-1>", lambda _: on_select())
            widget.bind("<Enter>",    lambda _, w=wrapper, p=prod: on_hover(True, w, p))
            widget.bind("<Leave>",    lambda _, w=wrapper, p=prod: on_hover(False, w, p))

    # ══ RIGHT DETAIL PANEL ════════════════════════════════════════════════════
    def show_detail(prod):
        for w in right_panel.winfo_children():
            w.destroy()

        rc = tk.Canvas(right_panel, bg=BG_DETAIL, highlightthickness=0, bd=0)
        rs = tk.Scrollbar(right_panel, orient="vertical", command=rc.yview)
        rc.configure(yscrollcommand=rs.set)
        rs.pack(side="right", fill="y")
        rc.pack(side="left", fill="both", expand=True)
        inner = tk.Frame(rc, bg=BG_DETAIL)
        r_win = rc.create_window((0, 0), window=inner, anchor="nw")

        def on_r_cfg(_):
            rc.configure(scrollregion=rc.bbox("all"))
            rc.itemconfig(r_win, width=rc.winfo_width())
        inner.bind("<Configure>", on_r_cfg)
        rc.bind("<Configure>", lambda e: rc.itemconfig(r_win, width=e.width))

        container = tk.Frame(inner, bg=BG_DETAIL)
        container.pack(fill="both", expand=True, padx=24, pady=20)

        # Header card 
        card_top = tk.Frame(container, bg=BG_TABLE_ROW, highlightbackground=DIVIDER, highlightthickness=1)
        card_top.pack(fill="x", pady=(0, 16))

        card_body = tk.Frame(card_top, bg=BG_TABLE_ROW)
        card_body.pack(fill="x", padx=16, pady=12)

        tk.Label(card_body, text=prod["title"], fg=ACCENT, bg=BG_TABLE_ROW, font=(FONT, 15, "bold"), anchor="w").pack(anchor="w")

        p_start = prod.get("start_date", prod.get("startDate", "—"))
        p_end = prod.get("end_date", prod.get("endDate", "—"))
        tk.Label(card_body, text=f"Season:   {p_start}  →  {p_end}", fg=TEXT_MID, bg=BG_TABLE_ROW, font=(FONT, 10), anchor="w").pack(anchor="w", pady=(4, 0))

        prod_id = prod.get("production_id", prod.get("productionId", "—"))
        tk.Label(card_body, text=f"Production ID:   {prod_id}", fg=TEXT_MUTED, bg=BG_TABLE_ROW, font=(FONT, 9), anchor="w").pack(anchor="w", pady=(2, 0))

        # Performances sub-table
        tk.Label(container, text="Scheduled Performances", fg=TEXT_DARK, bg=BG_DETAIL, font=(FONT, 12, "bold"), anchor="w").pack(anchor="w", pady=(0, 6))

        perf_card = tk.Frame(container, bg=BG_TABLE_ROW, highlightbackground=DIVIDER, highlightthickness=1)
        perf_card.pack(fill="x")

        headers    = ["Date", "Start", "End", "Total Seats", "Available"]
        col_widths = [14,      10,      8,     13,            10]

        hdr_row = tk.Frame(perf_card, bg="#EDEDED")
        hdr_row.pack(fill="x")
        for h, cw in zip(headers, col_widths):
            tk.Label(hdr_row, text=h, fg=ACCENT, bg="#EDEDED", font=(FONT, 9, "bold"), width=cw, anchor="w").pack(side="left", padx=6, pady=6)
        tk.Frame(perf_card, bg=DIVIDER, height=1).pack(fill="x")

        performances = []
        target_id = prod.get("production_id", prod.get("productionId"))
        if db and target_id:
            r = db.service.performance.locatePerformanceByProductionId(target_id)
            if isinstance(r, list):
                performances = r

        if not performances:
            tk.Label(perf_card, text="No performances scheduled yet.", fg=TEXT_MUTED, bg=BG_TABLE_ROW, font=(FONT, 10), anchor="w").pack(anchor="w", padx=14, pady=12)
        else:
            for ri, perf in enumerate(performances):
                row_bg = BG_TABLE_ROW if ri % 2 == 0 else BG_TABLE_ALT
                pr = tk.Frame(perf_card, bg=row_bg)
                pr.pack(fill="x")

                avail = "—"
                if db:
                    perf_target_id = perf.get("performance_id", perf.get("performanceId", ""))
                    ar = db.service.performanceSeat.viewAvailableSeatsByPerformance(perf_target_id)
                    if isinstance(ar, list):
                        avail = str(len(ar))

                vals = [
                    perf.get("date", "—"),
                    perf.get("start_time", perf.get("startTime", "—")),
                    perf.get("end_time", perf.get("endTime", "—")),
                    str(perf.get("total_seats", perf.get("totalSeats", "—"))),
                    avail,
                ]
                for v, cw in zip(vals, col_widths):
                    tk.Label(pr, text=v, fg=TEXT_DARK, bg=row_bg, font=(FONT, 10), width=cw, anchor="w").pack(side="left", padx=6, pady=8)
                tk.Frame(perf_card, bg=DIVIDER, height=1).pack(fill="x")

    # ══ ADD DIALOG ════════════════════════════════════════════════════════════
    def open_add_dialog(root):
        if not backend_ok():
            return

        dlg = tk.Toplevel(root)
        dlg.title("Add Production")
        dlg.configure(bg=TEXT_LIGHT)
        dlg.resizable(False, False)
        dlg.transient(root)
        dlg.grab_set()
        center_on(dlg, root, 460, 320)

        tk.Label(dlg, text="New Production", fg=ACCENT, bg=TEXT_LIGHT, font=(FONT, 14, "bold")).pack(pady=(16, 2))
        tk.Label(dlg, text="Fill in the production details below.", fg=TEXT_MID, bg=TEXT_LIGHT, font=(FONT, 10)).pack(pady=(0, 12))
        tk.Frame(dlg, bg=DIVIDER, height=1).pack(fill="x", padx=16)

        form = tk.Frame(dlg, bg=TEXT_LIGHT)
        form.pack(padx=24, pady=12, fill="x")

        fields = {}
        rows   = [
            ("Title", "title"),
            ("Start Date (YYYY-MM-DD)", "startDate"),
            ("End Date   (YYYY-MM-DD)", "endDate"),
        ]
        for r, (label, key) in enumerate(rows):
            tk.Label(form, text=label, fg=TEXT_DARK, bg=TEXT_LIGHT, font=(FONT, 9, "bold"), anchor="w").grid(row=r, column=0, sticky="w", pady=6)
            var = tk.StringVar()
            
            ent = tk.Entry(form, textvariable=var, font=(FONT, 11), relief="solid", bd=1)
            ent.grid(row=r, column=1, padx=(16, 0), pady=6, sticky="ew")
            fields[key] = var
            
        form.columnconfigure(1, weight=1)

        tk.Label(form, text="⚠  Max 4 concurrent productions not allowed.", fg="#AA6600", bg=TEXT_LIGHT, font=(FONT, 8, "italic")).grid(row=3, column=0, columnspan=2, sticky="w", pady=(6, 0))
        tk.Frame(dlg, bg=DIVIDER, height=1).pack(fill="x", padx=16)

        btn_row = tk.Frame(dlg, bg=TEXT_LIGHT)
        btn_row.pack(pady=14)

        def do_add():
            prod_obj = Production(
                title     = fields["title"].get().strip(),
                startDate = fields["startDate"].get().strip(),
                endDate   = fields["endDate"].get().strip(),
            )
            result = db.service.production.createProduction(prod_obj)

            if result == "Successfully created production.":
                all_p = db.service.production.viewAllProductions()
                if isinstance(all_p, list) and len(all_p) > 4:
                    messagebox.showwarning(
                        "Overlap Warning",
                        "More than 4 productions now overlap in running cycles inside schedule parameters.",
                        parent=dlg
                    )
                show_info(result)
                dlg.destroy()
                refresh_list()
            else:
                show_error(result)

        make_canvas_btn(btn_row, "Save Production", do_add, w=130, h=32, bg=TEXT_LIGHT).pack(side="left", padx=(0, 10))
        tk.Button(btn_row, text="Cancel", font=(FONT, 10), bg="#EEEEEE", fg=TEXT_DARK, relief="flat", padx=14, pady=6, cursor="hand2", command=dlg.destroy, activebackground="#DDDDDD").pack(side="left")

    # ══ EDIT DIALOG ═══════════════════════════════════════════════════════════
    def open_edit_dialog(prod, root):
        if not backend_ok():
            return

        # --- ADD THIS DATE REFORMATTING HELPER ---
        def convert_to_iso(date_str):
            if not date_str:
                return ""
            try:
                # Parses MM/DD/YYYY and converts it to YYYY-MM-DD
                return datetime.strptime(date_str.strip(), "%m/%d/%Y").strftime("%Y-%m-%d")
            except ValueError:
                # If the format is already correct or matches something else, return it as-is
                return date_str
        # ----------------------------------------

        dlg = tk.Toplevel(root)
        dlg.title("Edit Production")
        dlg.configure(bg=TEXT_LIGHT)
        dlg.resizable(False, False)
        dlg.transient(root)
        dlg.grab_set()
        center_on(dlg, root, 460, 320)

        tk.Label(dlg, text="Edit Production", fg=ACCENT, bg=TEXT_LIGHT, font=(FONT, 14, "bold")).pack(pady=(16, 2))
        tk.Label(dlg, text=f"Editing:  {prod['title']}", fg=TEXT_MID, bg=TEXT_LIGHT, font=(FONT, 9, "italic")).pack(pady=(0, 12))
        tk.Frame(dlg, bg=DIVIDER, height=1).pack(fill="x", padx=16)

        form = tk.Frame(dlg, bg=TEXT_LIGHT)
        form.pack(padx=24, pady=12, fill="x")

        # Extract raw dates cleanly
        raw_start = prod.get("start_date", prod.get("startDate", ""))
        raw_end = prod.get("end_date", prod.get("endDate", ""))

        fields = {}
        # --- UPDATE YOUR ROWS ARRAY TO CONVERT VALUES HERE ---
        rows = [
            ("Title",                   "title",     prod.get("title", "")),
            ("Start Date (YYYY-MM-DD)", "startDate", convert_to_iso(raw_start)),
            ("End Date   (YYYY-MM-DD)", "endDate",   convert_to_iso(raw_end)),
        ]
        
        for r, (label, key, default) in enumerate(rows):
            tk.Label(form, text=label, fg=TEXT_DARK, bg=TEXT_LIGHT, font=(FONT, 9, "bold"), anchor="w").grid(row=r, column=0, sticky="w", pady=6)
            var = tk.StringVar(value=default)
            ent = tk.Entry(form, textvariable=var, font=(FONT, 11), relief="solid", bd=1)
            ent.grid(row=r, column=1, padx=(16, 0), pady=6, sticky="ew")
            fields[key] = var
            
        form.columnconfigure(1, weight=1)

        tk.Frame(dlg, bg=DIVIDER, height=1).pack(fill="x", padx=16)

        btn_row = tk.Frame(dlg, bg=TEXT_LIGHT)
        btn_row.pack(pady=14)

        def do_update():
            prod_obj = Production(
                productionId = prod.get("production_id", prod.get("productionId")),
                title        = fields["title"].get().strip(),
                startDate    = fields["startDate"].get().strip(),
                endDate      = fields["endDate"].get().strip(),
            )
            result = db.service.production.updateProduction(prod_obj)

            if isinstance(result, dict):
                show_info(result.get("message", "Updated successfully."))
                dlg.destroy()
                refresh_list()
                updated = result.get("production")
                if updated:
                    selected["data"] = updated
                    show_detail(updated)
            else:
                show_error(str(result))

        make_canvas_btn(btn_row, "Save Changes", do_update, w=120, h=32, bg=TEXT_LIGHT).pack(side="left", padx=(0, 10))
        tk.Button(btn_row, text="Cancel", font=(FONT, 10), bg="#EEEEEE", fg=TEXT_DARK, relief="flat", padx=14, pady=6, cursor="hand2", command=dlg.destroy, activebackground="#DDDDDD").pack(side="left")

    # ══ DELETE ════════════════════════════════════════════════════════════════
    def do_delete(prod):
        if not backend_ok():
            return

        target_id = prod.get("production_id", prod.get("productionId"))
        confirmed = messagebox.askyesno(
            "Delete Production",
            f"Delete \"{prod['title']}\"?\n\nProductions containing scheduled performances cannot be removed.",
            parent=root
        )
        if not confirmed:
            return

        result = db.service.production.deleteProduction(target_id)

        if result == "Production deleted.":
            show_info("Production deleted successfully.")
            current_selected_id = selected["data"].get("production_id", selected["data"].get("productionId")) if selected["data"] else None
            if current_selected_id == target_id:
                selected["data"] = None
                show_placeholder()
            refresh_list()
        else:
            show_error(str(result))

    refresh_list()

# ── STANDALONE RUNNER ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.title("My Metropolitan Theater — Catalog")
    root.geometry("1280x720")
    root.configure(bg=BG_MAIN)

    topbar = tk.Frame(root, bg=BG_TOPBAR, height=45)
    topbar.pack(fill="x", side="top")
    topbar.pack_propagate(False)
    tk.Label(topbar, text="MY METROPOLITAN THEATER", fg=ACCENT, bg=BG_TOPBAR, font=(FONT, 13, "bold")).pack(side="left", padx=18, pady=10)
    
    lo = tk.Label(topbar, text="⬛→", fg=TEXT_LIGHT, bg=BG_TOPBAR, font=(FONT, 14), cursor="hand2")
    lo.pack(side="right", padx=16)
    lo.bind("<Enter>",    lambda _: lo.config(fg=ACCENT))
    lo.bind("<Leave>",    lambda _: lo.config(fg=TEXT_LIGHT))
    lo.bind("<Button-1>", lambda _: open_logout_dialog(root))

    body = tk.Frame(root, bg=BG_MAIN)
    body.pack(fill="both", expand=True)

    sidebar = tk.Frame(body, bg=BG_SIDEBAR, width=175)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    tk.Frame(sidebar, bg=BG_SIDEBAR, height=20).pack()
    active_nav = [None]

    def make_nav_item(icon, label, is_active=False):
        bg = BG_ACTIVE if is_active else BG_SIDEBAR
        frame = tk.Frame(sidebar, bg=bg, cursor="hand2")
        frame.pack(fill="x")
        il = tk.Label(frame, text=icon, bg=bg, fg=ACCENT if is_active else TEXT_LIGHT, font=("Arial", 13), width=3)
        il.pack(side="left", padx=(10, 4), pady=12)
        tl = tk.Label(frame, text=label, bg=bg, fg=ACCENT if is_active else TEXT_LIGHT, font=(FONT, 12, "bold" if is_active else "normal"))
        tl.pack(side="left")

        def on_enter(_):
            if frame != active_nav[0]:
                frame.config(bg=BG_SIDEBAR_H); il.config(bg=BG_SIDEBAR_H); tl.config(bg=BG_SIDEBAR_H)
        def on_leave(_):
            if frame != active_nav[0]:
                frame.config(bg=BG_SIDEBAR);   il.config(bg=BG_SIDEBAR);   tl.config(bg=BG_SIDEBAR)
                
        for w in (frame, il, tl):
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
        if is_active:
            active_nav[0] = frame

    for i, (icon, label) in enumerate(nav_items):
        make_nav_item(icon, label, is_active=(i == 0))

    content = tk.Frame(body, bg=BG_MAIN)
    content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    build_catalog_tab(content, root)
    root.mainloop()