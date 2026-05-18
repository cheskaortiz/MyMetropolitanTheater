import tkinter as tk
from tkinter import ttk

# ── Colors (matching the reference app) ───────────────────────────────────────
BG_MAIN      = "#B0B0B0"
BG_TOPBAR    = "#1E1E1E"
BG_SIDEBAR   = "#9A9A9A"
BG_SIDEBAR_H = "#888888"    
BG_ACTIVE    = "#C8C8C8"
BG_CARD      = "#F0F0F0"
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

FONT = "Helvetica"

nav_items = [
    ("🎭", "Catalog"),
    ("🎟",  "Sales"),
    ("👤", "Personnel"),
    ("💰", "Finances"),
    ("👥", "Customers"),
]
ACTIVE_NAV_INDEX = 3   # Finances

# ── Canvas rounded-rect button (same helper as reference) ─────────────────────
def make_canvas_btn(parent, text, command, w=80, h=32,
                    fill=ACCENT, fill_hov=ACCENT_HOV,
                    bg=BG_MAIN, fg=TEXT_LIGHT, font_size=10):
    c = tk.Canvas(parent, width=w, height=h, bg=bg,
                highlightthickness=0, bd=0)

    def draw(color):
        c.delete("all")
        r = 4
        c.create_arc(0,     0,     2*r, 2*r, start=90,  extent=90,  style="pieslice", fill=color, outline=color)
        c.create_arc(w-2*r, 0,     w,   2*r, start=0,   extent=90,  style="pieslice", fill=color, outline=color)
        c.create_arc(0,     h-2*r, 2*r, h,   start=180, extent=90,  style="pieslice", fill=color, outline=color)
        c.create_arc(w-2*r, h-2*r, w,   h,   start=270, extent=90,  style="pieslice", fill=color, outline=color)
        c.create_rectangle(r, 0,   w-r, h,   fill=color, outline=color)
        c.create_rectangle(0, r,   w,   h-r, fill=color, outline=color)
        c.create_text(w//2, h//2, text=text, fill=fg,
                    font=(FONT, font_size, "bold"))

    draw(fill)
    c.bind("<Enter>",    lambda _: draw(fill_hov))
    c.bind("<Leave>",    lambda _: draw(fill))
    c.bind("<Button-1>", lambda _: command())
    c.config(cursor="hand2")
    return c

# ── Create a rounded search bar container ──────────────────────────────────────
def make_rounded_search_bar(parent, bg_color="#E8E8E8"):
    """Create a rounded container for search bar with entry field."""
    container = tk.Frame(parent, bg=parent.cget("bg"), highlightthickness=0, bd=0)

    # Canvas for rounded background
    canvas = tk.Canvas(
        container,
        width=280, height=32,
        bg=parent.cget("bg"),
        highlightthickness=0, bd=0
    )
    canvas.pack()

    # Draw rounded rectangle
    r = 6
    canvas.create_arc(0, 0, 2*r, 2*r, start=90, extent=90, style="pieslice",
                    fill=bg_color, outline=bg_color)
    canvas.create_arc(280-2*r, 0, 280, 2*r, start=0, extent=90, style="pieslice",
                    fill=bg_color, outline=bg_color)
    canvas.create_arc(0, 32-2*r, 2*r, 32, start=180, extent=90, style="pieslice",
                    fill=bg_color, outline=bg_color)
    canvas.create_arc(280-2*r, 32-2*r, 280, 32, start=270, extent=90, style="pieslice",
                    fill=bg_color, outline=bg_color)
    canvas.create_rectangle(r, 0, 280-r, 32, fill=bg_color, outline=bg_color)
    canvas.create_rectangle(0, r, 280, 32-r, fill=bg_color, outline=bg_color)

    # Create frame for content inside rounded background
    inner_frame = tk.Frame(container, bg=bg_color, highlightthickness=0, bd=0)
    canvas.create_window(140, 16, window=inner_frame, width=270, height=20)

    return container, inner_frame

# ── Center a Toplevel over a parent window ────────────────────────────────────
def center_on(win, parent, w, h):
    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width()  - w) // 2
    y = parent.winfo_y() + (parent.winfo_height() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

# ── Main application ──────────────────────────────────────────────────────────
class MetropolitanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Metropolitan Theater")
        self.geometry("1200x720")
        self.minsize(960, 580)
        self.configure(bg=BG_MAIN)
        self.resizable(True, True)

        self._build_topbar()
        self._build_body()

    # ── Top bar ───────────────────────────────────────────────────────────────
    def _build_topbar(self):
        bar = tk.Frame(self, bg=BG_TOPBAR, height=45)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)

        tk.Label(
            bar,
            text="MY METROPOLITAN THEATER",
            fg=ACCENT, bg=BG_TOPBAR,
            font=(FONT, 13, "bold"),
        ).pack(side="left", padx=18, pady=10)

        logout_lbl = tk.Label(
            bar, text="⬛→",
            fg=TEXT_LIGHT, bg=BG_TOPBAR,
            font=(FONT, 14), cursor="hand2",
        )
        logout_lbl.pack(side="right", padx=16)
        logout_lbl.bind("<Enter>",    lambda _: logout_lbl.config(fg=ACCENT))
        logout_lbl.bind("<Leave>",    lambda _: logout_lbl.config(fg=TEXT_LIGHT))
        logout_lbl.bind("<Button-1>", lambda _: self._open_logout_dialog())

    # ── Logout confirmation dialog ────────────────────────────────────────────
    def _open_logout_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("")
        dlg.configure(bg=TEXT_LIGHT)
        dlg.resizable(False, False)
        dlg.transient(self)
        dlg.grab_set()
        center_on(dlg, self, 380, 240)

        # Icon circle
        ic = tk.Canvas(dlg, width=90, height=90, bg=TEXT_LIGHT, highlightthickness=0)
        ic.pack(pady=(28, 0))
        ic.create_oval(5, 5, 85, 85, fill="#EEEEEE", outline="#EEEEEE")
        ic.create_text(45, 47, text="⬛→", font=("Arial", 22), fill="#AAAAAA")

        tk.Label(
            dlg,
            text="Are you sure you want to logout?",
            fg=TEXT_DARK, bg=TEXT_LIGHT,
            font=(FONT, 13),
        ).pack(pady=(14, 20))

        btn_row = tk.Frame(dlg, bg=TEXT_LIGHT)
        btn_row.pack()

        tk.Button(
            btn_row,
            text="Cancel",
            bg="#EEEEEE", fg=TEXT_DARK,
            font=(FONT, 11),
            relief="flat", bd=0,
            padx=18, pady=8,
            cursor="hand2",
            command=dlg.destroy,
            activebackground="#DDDDDD",
        ).pack(side="left", padx=(0, 12))

        make_canvas_btn(
            btn_row, "Logout",
            command=self.destroy,
            w=90, h=36,
            fill=ACCENT, fill_hov=ACCENT_HOV,
            bg=TEXT_LIGHT,
        ).pack(side="left")

    # ── Body ──────────────────────────────────────────────────────────────────
    def _build_body(self):
        body = tk.Frame(self, bg=BG_MAIN)
        body.pack(fill="both", expand=True)

        self._build_sidebar(body)
        self._build_content(body)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=BG_SIDEBAR, width=175)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Frame(sidebar, bg=BG_SIDEBAR, height=20).pack()

        active_ref = [None]

        for i, (icon, label) in enumerate(nav_items):
            is_active = (i == ACTIVE_NAV_INDEX)
            bg = BG_ACTIVE if is_active else BG_SIDEBAR
            fg = ACCENT    if is_active else TEXT_LIGHT
            fw = "bold"    if is_active else "normal"

            frame    = tk.Frame(sidebar, bg=bg, cursor="hand2")
            icon_lbl = tk.Label(frame, text=icon, bg=bg, fg=fg,
                                font=("Arial", 13), width=3)
            text_lbl = tk.Label(frame, text=label, bg=bg, fg=fg,
                                font=(FONT, 12, fw))

            frame.pack(fill="x")
            icon_lbl.pack(side="left", padx=(10, 4), pady=12)
            text_lbl.pack(side="left")

            if is_active:
                active_ref[0] = (frame, icon_lbl, text_lbl)

            def on_enter(_, f=frame, il=icon_lbl, tl=text_lbl):
                if (f, il, tl) != active_ref[0]:
                    for w in (f, il, tl):
                        w.config(bg=BG_SIDEBAR_H)

            def on_leave(_, f=frame, il=icon_lbl, tl=text_lbl):
                if (f, il, tl) != active_ref[0]:
                    for w in (f, il, tl):
                        w.config(bg=BG_SIDEBAR)

            for w in (frame, icon_lbl, text_lbl):
                w.bind("<Enter>", on_enter)
                w.bind("<Leave>", on_leave)

    # ── Main content ──────────────────────────────────────────────────────────
    def _build_content(self, parent):
        content = tk.Frame(parent, bg=BG_MAIN)
        content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            content,
            text="Transactions and Records",
            fg=ACCENT, bg=BG_MAIN,
            font=(FONT, 22, "bold"),
        ).pack(anchor="w", pady=(0, 14))

        card = tk.Frame(content, bg=BG_CARD)
        card.pack(fill="both", expand=True)

        self._build_toolbar(card)
        self._build_table(card)

    # ── Toolbar ───────────────────────────────────────────────────────────────
    def _build_toolbar(self, parent):
        toolbar = tk.Frame(parent, bg=BG_CARD)
        toolbar.pack(fill="x", padx=14, pady=12)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Theater.TCombobox",
            fieldbackground=TEXT_LIGHT,
            background=TEXT_LIGHT,
            foreground=TEXT_DARK,
            arrowcolor=TEXT_DARK,
            bordercolor=DIVIDER,
            lightcolor=DIVIDER,
            darkcolor=DIVIDER,
        )

        self.date_var = tk.StringVar(value="")
        ttk.Combobox(
            toolbar,
            textvariable=self.date_var,
            values=["Today", "This Week", "This Month", "Custom..."],
            width=18,
            state="readonly",
            style="Theater.TCombobox",
            font=(FONT, 10),
        ).pack(side="left")

        # Search bar with rounded corners
        sf_container, sf = make_rounded_search_bar(toolbar, bg_color=BG_SEARCH)
        sf_container.pack(side="right")

        tk.Label(sf, text="🔍", bg=BG_SEARCH, fg=TEXT_MID,
                font=("Arial", 9)).pack(side="left", padx=(6, 0))

        self.search_entry = tk.Entry(
            sf, bg=BG_SEARCH, fg=TEXT_MID,
            bd=0, width=28,
            font=(FONT, 10),
            insertbackground=TEXT_DARK,
        )
        self.search_entry.insert(0, "Search")
        self.search_entry.pack(side="left", padx=(2, 8))
        self.search_entry.bind("<FocusIn>",    self._search_focus_in)
        self.search_entry.bind("<FocusOut>",   self._search_focus_out)
        self.search_entry.bind("<KeyRelease>", self._filter_rows)

    def _search_focus_in(self, _):
        if self.search_entry.get() == "Search":
            self.search_entry.delete(0, "end")
            self.search_entry.config(fg=TEXT_DARK)

    def _search_focus_out(self, _):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search")
            self.search_entry.config(fg=TEXT_MID)

    # ── Transactions table ────────────────────────────────────────────────────
    def _build_table(self, parent):
        columns = ("datetime", "amount", "payment_type", "handled_by", "status")
        col_labels = {
            "datetime":     "Date and Time",
            "amount":       "Amount",
            "payment_type": "Payment Type",
            "handled_by":   "Handled By",
            "status":       "Status",
        }
        col_widths = {
            "datetime":     185,
            "amount":       120,
            "payment_type": 155,
            "handled_by":   155,
            "status":       110,
        }

        style = ttk.Style()
        style.configure(
            "Theater.Treeview",
            background=BG_CARD,
            foreground=TEXT_DARK,
            rowheight=30,
            fieldbackground=BG_CARD,
            borderwidth=0,
            font=(FONT, 11),
        )
        style.configure(
            "Theater.Treeview.Heading",
            background=BG_CARD,
            foreground=ACCENT,
            font=(FONT, 11, "bold"),
            relief="flat",
            borderwidth=0,
        )
        style.map("Theater.Treeview",
                background=[("selected", "#DCDCDC")],
                foreground=[("selected", TEXT_DARK)])
        style.map("Theater.Treeview.Heading",
                background=[("active", BG_CARD)])

        # Thin divider above table headers
        tk.Frame(parent, bg=DIVIDER, height=1).pack(fill="x", padx=14)

        table_frame = tk.Frame(parent, bg=BG_CARD)
        table_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Theater.Treeview",
            selectmode="browse",
        )

        for col in columns:
            self.tree.heading(col, text=col_labels[col])
            self.tree.column(col, width=col_widths[col], minwidth=80, anchor="w")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure("odd",  background=BG_TABLE_ROW)
        self.tree.tag_configure("even", background=BG_TABLE_ALT)

        self.all_rows = [
            ("2026-04-07 14:35:10", "Php 1000.00", "Credit Card", "Mary Ruth",        "Completed"),
            ("2026-04-07 14:35:10", "Php 1000.00", "Credit Card", "Francheska Ortiz", "Completed"),
            ("2026-04-07 14:35:10", "Php 1000.00", "Credit Card", "Elicxia Mistica",  "Completed"),
        ]
        self._populate(self.all_rows)

    def _populate(self, rows):
        self.tree.delete(*self.tree.get_children())
        for i, row in enumerate(rows):
            self.tree.insert("", "end", values=row,
                            tags=("odd" if i % 2 == 0 else "even",))

    def _filter_rows(self, _=None):
        q = self.search_entry.get().lower()
        if not q or q == "search":
            self._populate(self.all_rows)
            return
        self._populate([r for r in self.all_rows
                        if any(q in str(v).lower() for v in r)])

if __name__ == "__main__":
    app = MetropolitanApp()
    app.mainloop()