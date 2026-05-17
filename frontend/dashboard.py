import tkinter as tk
from tkinter import ttk

# ── Shared Styling Constants ──────────────────────────────────────────────────
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
FONT         = "Helvetica"
RADIUS       = 5
SW, SH       = 46, 36   # seat width, height

# ── Helpers ───────────────────────────────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    canvas.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,  style="pieslice", **kw)
    canvas.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,  style="pieslice", **kw)
    canvas.create_rectangle(x1+r, y1,   x2-r, y2,   **kw)
    canvas.create_rectangle(x1,   y1+r, x2,   y2-r, **kw)

def make_canvas_btn(parent, text, command, w=80, h=32, fill=ACCENT, fill_hov=ACCENT_HOV, bg=BG_MAIN, fg=TEXT_LIGHT, font_size=10):
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

# ── Sales Tab ─────────────────────────────────────────────────────────────────
class SalesTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_MAIN)
        self.selected_seats = []
        self.seat_states = {}
        self.productions = [
            "Hamlet — Jan 10, 7:00 PM",
            "Hamlet — Jan 11, 7:00 PM",
            "The Phantom of the Opera — Jan 15, 7:00 PM",
            "The Phantom of the Opera — Jan 16, 7:00 PM",
        ]
        self.init_ui()

    def init_ui(self):
        container = tk.Frame(self, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        tk.Label(container, text="🎟 Box Office (Ticketing)", fg=ACCENT, bg=BG_MAIN, font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 14))
        
        main_row = tk.Frame(container, bg=BG_MAIN)
        main_row.pack(fill="both", expand=True)

        left_col = tk.Frame(main_row, bg=BG_PANEL)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 14))
        
        prod_header = tk.Frame(left_col, bg=BG_PANEL)
        prod_header.pack(fill="x", padx=16, pady=(14, 8))
        tk.Label(prod_header, text="Production", bg=BG_PANEL, fg=TEXT_DARK, font=(FONT, 12, "bold")).pack(anchor="w")
        
        self.production_var = tk.StringVar(value="Select")
        prod_menu = ttk.Combobox(prod_header, textvariable=self.production_var, values=self.productions, state="readonly", font=(FONT, 11), width=34)
        prod_menu.pack(anchor="w", pady=(4, 0))
        prod_menu.bind("<<ComboboxSelected>>", lambda _: self.update_receipt())

        seat_area = tk.Frame(left_col, bg=BG_PANEL)
        seat_area.pack(fill="both", expand=True, padx=16, pady=(4, 16))
        stage = tk.Frame(seat_area, bg=BG_STAGE, height=35)
        stage.pack(fill="x", pady=(0, 18))
        tk.Label(stage, text="STAGE", bg=BG_STAGE, font=(FONT, 12, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        self.build_seating_layout(seat_area)
        
        legend = tk.Frame(seat_area, bg=BG_PANEL)
        legend.pack(anchor="w", pady=(12, 0))
        for color, label in [(SEAT_AVAIL, "Available"), (SEAT_SOLD, "Sold"), (SEAT_SEL, "Selected")]:
            dot = tk.Canvas(legend, width=18, height=18, bg=BG_PANEL, highlightthickness=0)
            dot.pack(side="left", padx=(0, 4))
            dot.create_rectangle(2, 2, 16, 16, fill=color, outline=color)
            tk.Label(legend, text=label, bg=BG_PANEL, fg=TEXT_DARK, font=(FONT, 10)).pack(side="left", padx=(0, 14))

        self.receipt_panel = tk.Frame(main_row, bg=BG_RECEIPT, width=300)
        self.receipt_panel.pack(side="left", fill="y")
        self.receipt_panel.pack_propagate(False)
        self.setup_receipt()

    def make_seat(self, parent, label):
        self.seat_states[label] = "available"
        c = tk.Canvas(parent, width=SW, height=SH, bg=BG_PANEL, highlightthickness=0, cursor="hand2")
        def draw(hov=False):
            st = self.seat_states[label]
            color, hov_color = (SEAT_SEL, SEAT_SEL_H) if st=="selected" else (SEAT_AVAIL, SEAT_AVAIL_H)
            if st == "sold": color, hov_color = (SEAT_SOLD, SEAT_SOLD_H)
            c.delete("all")
            fill = hov_color if hov else color
            rounded_rect(c, 1, 1, SW-1, SH-1, RADIUS, fill=fill, outline=fill)
            c.create_text(SW//2, SH//2, text=label, fill=TEXT_LIGHT, font=(FONT, 8, "bold"))
        def click(_):
            if self.seat_states[label] == "sold": return
            self.seat_states[label] = "selected" if self.seat_states[label] == "available" else "available"
            if self.seat_states[label] == "selected": self.selected_seats.append(label)
            else: self.selected_seats.remove(label)
            draw(); self.update_receipt()
        c.bind("<Enter>", lambda _: draw(True)); c.bind("<Leave>", lambda _: draw(False)); c.bind("<Button-1>", click)
        draw(); return c

    def build_seating_layout(self, area):
        # Unified layout from SalesTab.py requirements
        def add_row(lbl, seats, has_spacer=False):
            row_f = tk.Frame(area, bg=BG_PANEL)
            row_f.pack(pady=4)
            tk.Label(row_f, text=lbl, bg=BG_PANEL, fg=TEXT_MID, font=(FONT, 10), width=2).pack(side="left")
            for s in seats:
                self.make_seat(row_f, s).pack(side="left", padx=3)
            tk.Label(row_f, text=lbl, bg=BG_PANEL, fg=TEXT_MID, font=(FONT, 10), width=2).pack(side="left")

        add_row("A", ["A1","A2","A3","A4"])
        add_row("B", ["B1","B2","B3","B4","B5","B6"])
        add_row("C", ["C1","C2","C3","C4","C5","C6","C7","C8"])
        add_row("D", ["D1","D2","D3","D4","D5","D6","D7","D8"])
        add_row("E", ["E1","E2","E3","E4"])

    def setup_receipt(self):
        def lbl(txt, bold=False, size=9, fg=TEXT_DARK, pady=0):
            tk.Label(self.receipt_panel, text=txt, bg=BG_RECEIPT, fg=fg, 
                     font=(FONT, size, "bold" if bold else "normal"), wraplength=260, justify="center").pack(pady=pady)
        
        def divider():
            tk.Label(self.receipt_panel, text="- " * 28, bg=BG_RECEIPT, fg=DIVIDER, font=(FONT, 7)).pack()

        tk.Frame(self.receipt_panel, height=20, bg=BG_RECEIPT).pack()
        lbl("My Metropolitan Theater", bold=True, size=11)
        lbl("OFFICIAL RECEIPT", size=9, fg=TEXT_MID)
        tk.Frame(self.receipt_panel, height=10, bg=BG_RECEIPT).pack()
        
        lbl("Transaction ID: #TXN-0001")
        lbl("Date: May 10, 2026")
        divider()
        lbl("CUSTOMER DETAILS", bold=True, fg=TEXT_MID)
        divider()
        lbl("Name: Juan Dela Cruz")
        lbl("Email: juandelacruz@email.com")
        divider()
        lbl("TICKET INFORMATION", bold=True, fg=TEXT_MID)
        divider()
        
        self.receipt_prod_var = tk.StringVar(value="Production: —")
        tk.Label(self.receipt_panel, textvariable=self.receipt_prod_var, bg=BG_RECEIPT, font=(FONT, 9), wraplength=260).pack()
        
        self.receipt_seat_var = tk.StringVar(value="Seat(s): —")
        tk.Label(self.receipt_panel, textvariable=self.receipt_seat_var, bg=BG_RECEIPT, font=(FONT, 9), wraplength=260).pack()
        
        divider()
        lbl("PAYMENT SUMMARY", bold=True, fg=TEXT_MID)
        divider()
        lbl("Total Amount: ₱1,500.00", bold=True, size=12, pady=10)
        
        make_canvas_btn(self.receipt_panel, "Print Receipt", lambda: None, w=180, h=40).pack(pady=20)

    def update_receipt(self):
        self.receipt_seat_var.set(f"Seat(s): {', '.join(self.selected_seats) if self.selected_seats else '—'}")
        prod = self.production_var.get()
        self.receipt_prod_var.set(f"Production: {prod if prod != 'Select' else '—'}")

# ── Catalog Tab ───────────────────────────────────────────────────────────────
class CatalogTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_MAIN)
        self.productions = [
            ("P-001", "Hamlet", "Drama", "John Doe", "Jan 10-12", "Ongoing", "Shakespeare's classic tragedy of the Prince of Denmark."),
            ("P-002", "Phantom of the Opera", "Musical", "Jane Smith", "Jan 15-18", "Draft", "A masked musical genius haunts the Paris Opera House."),
            ("P-003", "Lion King", "Musical", "C. Evans", "Feb 01-05", "Upcoming", "Disney's pride lands come to life on the stage.")
        ]
        self.init_ui()

    def init_ui(self):
        container = tk.Frame(self, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        tk.Label(container, text="🎭 Production Catalog", fg=ACCENT, bg=BG_MAIN, font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 15))

        main_row = tk.Frame(container, bg=BG_MAIN)
        main_row.pack(fill="both", expand=True)

        left_col = tk.Frame(main_row, bg=BG_PANEL)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        toolbar = tk.Frame(left_col, bg=BG_PANEL)
        toolbar.pack(fill="x", padx=10, pady=10)
        
        search_ent = tk.Entry(toolbar, font=(FONT, 11), width=30, fg=TEXT_MID)
        search_ent.insert(0, "Search productions...")
        search_ent.pack(side="left", padx=5)
        
        make_canvas_btn(toolbar, "Search", lambda: None, w=80).pack(side="left", padx=5)
        make_canvas_btn(toolbar, "Add Show", lambda: None, w=100).pack(side="right", padx=5)

        cols = ("ID", "Title", "Genre", "Director", "Status")
        self.tree = ttk.Treeview(left_col, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        for d in self.productions: self.tree.insert("", "end", values=d[:5])
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.detail_panel = tk.Frame(main_row, bg=BG_RECEIPT, width=300)
        self.detail_panel.pack(side="left", fill="y")
        self.detail_panel.pack_propagate(False)
        
        self.det_title = tk.StringVar(value="Select a Production")
        self.det_desc = tk.StringVar(value="Details will appear here.")
        tk.Label(self.detail_panel, textvariable=self.det_title, bg=BG_RECEIPT, font=(FONT, 14, "bold"), wraplength=260).pack(pady=20)
        tk.Label(self.detail_panel, textvariable=self.det_desc, bg=BG_RECEIPT, font=(FONT, 10), wraplength=260, justify="left").pack(padx=20)

    def on_select(self, _):
        item = self.tree.selection()[0]
        val = self.tree.item(item, "values")[0]
        prod = next(p for p in self.productions if p[0] == val)
        self.det_title.set(prod[1])
        self.det_desc.set(f"ID: {prod[0]}\nGenre: {prod[2]}\nDirector: {prod[3]}\nSchedule: {prod[4]}\nStatus: {prod[5]}\n\nDescription:\n{prod[6]}")

# ── Personnel Tab ─────────────────────────────────────────────────────────────
class PersonnelTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_MAIN)
        self.staff = [
            ("ST-001", "Maria Santos", "Box Office", "0917-123-4567", "₱25,000", "Active"),
            ("ST-002", "Jose Rizal", "Stage Crew", "0918-456-7890", "₱22,000", "Active"),
            ("ST-003", "Andres Bonifacio", "Security", "0919-789-1234", "₱20,000", "On Leave")
        ]
        self.init_ui()

    def init_ui(self):
        container = tk.Frame(self, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        tk.Label(container, text="👤 Personnel Management", fg=ACCENT, bg=BG_MAIN, font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 15))

        main_row = tk.Frame(container, bg=BG_MAIN)
        main_row.pack(fill="both", expand=True)

        left_col = tk.Frame(main_row, bg=BG_PANEL)
        left_col.pack(side="left", fill="both", expand=True)
        
        toolbar = tk.Frame(left_col, bg=BG_PANEL)
        toolbar.pack(fill="x", padx=10, pady=10)
        make_canvas_btn(toolbar, "+ Add Staff", lambda: None, w=120).pack(side="left", padx=5)
        make_canvas_btn(toolbar, "Payroll Report", lambda: None, w=140).pack(side="right", padx=5)

        cols = ("EmpID", "Name", "Role", "Phone", "Salary", "Status")
        tree = ttk.Treeview(left_col, columns=cols, show="headings")
        for c in cols: tree.heading(c, text=c)
        tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        for s in self.staff: tree.insert("", "end", values=s)

# ── Finances Tab ──────────────────────────────────────────────────────────────
class FinancesTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_MAIN)
        self.init_ui()

    def init_ui(self):
        container = tk.Frame(self, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        tk.Label(container, text="💰 Financial Records", fg=ACCENT, bg=BG_MAIN, font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 15))

        summary = tk.Frame(container, bg=BG_PANEL, height=100)
        summary.pack(fill="x", pady=(0, 15))
        summary.pack_propagate(False)
        
        stats = [("Total Revenue", "₱1,240,500", "#2ECC40"), ("Total Expenses", "₱450,200", "#CC1111"), ("Net Profit", "₱790,300", "#2196F3")]
        for i, (l, v, c) in enumerate(stats):
            f = tk.Frame(summary, bg=BG_PANEL)
            f.place(relx=i*0.33, rely=0.5, anchor="w", relwidth=0.33)
            tk.Label(f, text=l, bg=BG_PANEL, font=(FONT, 10), fg=TEXT_MID).pack()
            tk.Label(f, text=v, bg=BG_PANEL, font=(FONT, 16, "bold"), fg=c).pack()

        cols = ("ID", "Date", "Description", "Type", "Amount", "Status")
        tree = ttk.Treeview(container, columns=cols, show="headings")
        for c in cols: tree.heading(c, text=c)
        tree.pack(fill="both", expand=True)
        
        data = [
            ("T-501", "2026-05-10", "Ticket Sale #TXN-0001", "Income", "₱1,500", "Completed"),
            ("T-502", "2026-05-10", "Utility Payment", "Expense", "-₱5,000", "Pending"),
            ("T-503", "2026-05-09", "Hamlet Royalties", "Expense", "-₱20,000", "Completed")
        ]
        for d in data: tree.insert("", "end", values=d)

# ── Customers Tab ─────────────────────────────────────────────────────────────
class CustomersTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_MAIN)
        self.customers = [
            ("C-001", "Juan Dela Cruz", "juan@email.com", "0920-111-2222", "5", "₱7,500"),
            ("C-002", "Pedro Penduko", "pedro@email.com", "0921-222-3333", "2", "₱3,000")
        ]
        self.init_ui()

    def init_ui(self):
        container = tk.Frame(self, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        tk.Label(container, text="👥 Customer Database", fg=ACCENT, bg=BG_MAIN, font=(FONT, 22, "bold")).pack(anchor="w", pady=(0, 15))

        main_row = tk.Frame(container, bg=BG_MAIN)
        main_row.pack(fill="both", expand=True)

        left_col = tk.Frame(main_row, bg=BG_PANEL)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        cols = ("ID", "Full Name", "Email", "Phone", "Tickets", "Spent")
        self.tree = ttk.Treeview(left_col, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        for c in self.customers: self.tree.insert("", "end", values=c)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.detail_panel = tk.Frame(main_row, bg=BG_RECEIPT, width=300)
        self.detail_panel.pack(side="left", fill="y")
        self.detail_panel.pack_propagate(False)
        
        self.cust_name = tk.StringVar(value="Customer Profile")
        self.cust_details = tk.StringVar(value="Select a customer to view details.")
        tk.Label(self.detail_panel, textvariable=self.cust_name, bg=BG_RECEIPT, font=(FONT, 14, "bold"), wraplength=260).pack(pady=20)
        tk.Label(self.detail_panel, textvariable=self.cust_details, bg=BG_RECEIPT, font=(FONT, 10), wraplength=260, justify="left").pack(padx=20)

    def on_select(self, _):
        item = self.tree.selection()[0]
        vals = self.tree.item(item, "values")
        self.cust_name.set(vals[1])
        self.cust_details.set(f"ID: {vals[0]}\nEmail: {vals[2]}\nPhone: {vals[3]}\nTotal Tickets: {vals[4]}\nTotal Spent: {vals[5]}")

# ── Main Dashboard Application ────────────────────────────────────────────────
class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Metropolitan Theater")
        self.root.geometry("1440x900")
        self.root.configure(bg=BG_MAIN)

        self.current_content = None
        self.active_nav_frame = None
        self.nav_items_widgets = []

        self.setup_ui()
        self.switch_tab("Sales")

    def setup_ui(self):
        topbar = tk.Frame(self.root, bg=BG_TOPBAR, height=50)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="MY METROPOLITAN THEATER", fg=ACCENT, bg=BG_TOPBAR, font=(FONT, 14, "bold")).pack(side="left", padx=20)
        logout_btn = tk.Label(topbar, text="Logout ⬛→", fg=TEXT_LIGHT, bg=BG_TOPBAR, font=(FONT, 11), cursor="hand2")
        logout_btn.pack(side="right", padx=20)
        logout_btn.bind("<Button-1>", lambda _: self.confirm_logout())

        body = tk.Frame(self.root, bg=BG_MAIN)
        body.pack(fill="both", expand=True)

        sidebar = tk.Frame(body, bg=BG_SIDEBAR, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Frame(sidebar, bg=BG_SIDEBAR, height=20).pack()

        nav_tabs = [("🎭", "Catalog"), ("🎟", "Sales"), ("👤", "Personnel"), ("💰", "Finances"), ("👥", "Customers")]
        for icon, label in nav_tabs:
            self.create_nav_item(sidebar, icon, label)

        self.content_area = tk.Frame(body, bg=BG_MAIN)
        self.content_area.pack(side="left", fill="both", expand=True)

    def create_nav_item(self, parent, icon, label):
        frame = tk.Frame(parent, bg=BG_SIDEBAR, cursor="hand2")
        frame.pack(fill="x")
        il = tk.Label(frame, text=icon, bg=BG_SIDEBAR, fg=TEXT_LIGHT, font=("Arial", 14), width=3)
        il.pack(side="left", padx=(15, 5), pady=15)
        tl = tk.Label(frame, text=label, bg=BG_SIDEBAR, fg=TEXT_LIGHT, font=(FONT, 12))
        tl.pack(side="left")

        widgets = (frame, il, tl)
        self.nav_items_widgets.append((label, widgets))

        def on_enter(_):
            if frame != self.active_nav_frame:
                for w in (frame, il, tl): w.config(bg=BG_SIDEBAR_H)
        def on_leave(_):
            if frame != self.active_nav_frame:
                for w in (frame, il, tl): w.config(bg=BG_SIDEBAR)
        def on_click(_):
            self.switch_tab(label)

        for w in widgets:
            w.bind("<Enter>", on_enter); w.bind("<Leave>", on_leave); w.bind("<Button-1>", on_click)

    def switch_tab(self, label):
        for tab_label, widgets in self.nav_items_widgets:
            frame, il, tl = widgets
            if tab_label == label:
                self.active_nav_frame = frame
                frame.config(bg=BG_ACTIVE)
                il.config(bg=BG_ACTIVE, fg=ACCENT)
                tl.config(bg=BG_ACTIVE, fg=ACCENT, font=(FONT, 12, "bold"))
            else:
                frame.config(bg=BG_SIDEBAR)
                il.config(bg=BG_SIDEBAR, fg=TEXT_LIGHT)
                tl.config(bg=BG_SIDEBAR, fg=TEXT_LIGHT, font=(FONT, 12, "normal"))

        if self.current_content: self.current_content.destroy()
        
        mapping = {"Sales": SalesTab, "Catalog": CatalogTab, "Personnel": PersonnelTab, "Finances": FinancesTab, "Customers": CustomersTab}
        TabClass = mapping.get(label)
        if TabClass:
            self.current_content = TabClass(self.content_area)
            self.current_content.pack(fill="both", expand=True)

    def confirm_logout(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Logout")
        dlg.configure(bg=TEXT_LIGHT); dlg.resizable(False, False)
        dlg.transient(self.root); dlg.grab_set()
        center_on(dlg, self.root, 380, 240)

        ic = tk.Canvas(dlg, width=90, height=90, bg=TEXT_LIGHT, highlightthickness=0)
        ic.pack(pady=(28, 0))
        ic.create_oval(5, 5, 85, 85, fill="#EEEEEE", outline="#EEEEEE")
        ic.create_text(45, 47, text="⬛→", font=("Arial", 22), fill="#AAAAAA")

        tk.Label(dlg, text="Logout of the system?", fg=TEXT_DARK, bg=TEXT_LIGHT, font=(FONT, 12)).pack(pady=20)
        btns = tk.Frame(dlg, bg=TEXT_LIGHT); btns.pack()
        tk.Button(btns, text="Cancel", command=dlg.destroy, bg="#EEEEEE", relief="flat", padx=15, pady=5).pack(side="left", padx=10)
        make_canvas_btn(btns, "Logout", self.root.destroy, w=100, h=35).pack(side="left", padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox", fieldbackground=BG_PANEL, background=BG_PANEL, foreground=TEXT_DARK, arrowcolor=TEXT_DARK)
    style.configure("Treeview", background=BG_PANEL, fieldbackground=BG_PANEL, foreground=TEXT_DARK, font=(FONT, 10), rowheight=30)
    style.configure("Treeview.Heading", background=BG_SIDEBAR, foreground=TEXT_LIGHT, font=(FONT, 10, "bold"))
    style.map("Treeview", background=[('selected', ACCENT)], foreground=[('selected', TEXT_LIGHT)])
    app = DashboardApp(root)
    root.mainloop()