import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

# ── Path Fix ──────────────────────────────────────────────────────────────────
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
    start_database       = None
    BACKEND_IMPORT_ERROR = e

try:
    from backend.objects.transaction import Transaction
except Exception:
    class Transaction:
        def __init__(self, ticketId=None, staffId=None, transactionDate=None,
                     type=None, amount=None):
            self.ticketId        = ticketId
            self.staffId         = staffId
            self.transactionDate = transactionDate
            self.type            = type
            self.amount          = amount

# ── Palette ───────────────────────────────────────────────────────────────────
BG_MAIN      = "#B0B0B0"
BG_TOPBAR    = "#1E1E1E"
BG_SIDEBAR   = "#9A9A9A"
BG_ACTIVE    = "#C8C8C8"
BG_PANEL     = "#EFEFEF"
BG_STAGE     = "#D0D0D0"
BG_RECEIPT   = "#F5F5F5"

ACCENT       = "#CC1111"
ACCENT_HOVER = "#A30E0E"
TEXT_LIGHT   = "#FFFFFF"
TEXT_DARK    = "#1A1A1A"
TEXT_MID     = "#555555"

SEAT_AVAIL   = "#2ECC40"
SEAT_SOLD    = "#CC1111"
SEAT_SEL     = "#F39C12"
SEAT_AVAIL_H = "#27AE36"

FONT = "Helvetica"


# ── Simple session object — replace with your real login session ──────────────
class AppSession:
    def __init__(self, staff_id=23, staff_name="Marius Aquino",
                 staff_type="Commissioned"):
        self.staff_id   = staff_id
        self.staff_name = staff_name
        self.staff_type = staff_type          # 'Full_Time' | 'Hourly' | 'Commissioned'

    @property
    def is_manager(self):
        return self.staff_type == "Full_Time"

    @property
    def can_transact(self):
        """Only commissioned (sales agents) may issue tickets."""
        return self.staff_type == "Commissioned"


# ── Utilities ─────────────────────────────────────────────────────────────────
def fmt_short_date(v):
    if v is None: return "—"
    if isinstance(v, (datetime, date)): return v.strftime("%b %d")
    v = str(v).strip()
    for f in ("%Y-%m-%d", "%m/%d/%Y"):
        try: return datetime.strptime(v, f).strftime("%b %d")
        except ValueError: pass
    return v

def fmt_time(v):
    if v is None: return "—"
    import datetime as _dt
    if isinstance(v, _dt.time): return v.strftime("%I:%M %p").lstrip("0")
    v = str(v).strip()
    for f in ("%H:%M:%S", "%H:%M"):
        try: return datetime.strptime(v, f).strftime("%I:%M %p").lstrip("0")
        except ValueError: pass
    return v


# ── ModernButton ──────────────────────────────────────────────────────────────
class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=140, height=36,
                 radius=6, bg=ACCENT, hbg=ACCENT_HOVER, fg=TEXT_LIGHT,
                 state="normal"):
        super().__init__(parent, width=width, height=height,
                         bg=parent["bg"], highlightthickness=0,
                         cursor="hand2" if state == "normal" else "arrow")
        self.text      = text
        self.command   = command
        self.w         = width
        self.h         = height
        self.r         = radius
        self.normal_bg = bg
        self.hover_bg  = hbg
        self.fg        = fg
        self._state    = state
        self._draw(self.normal_bg)
        if self._state == "normal":
            self.bind("<Enter>",    lambda e: self._draw(self.hover_bg))
            self.bind("<Leave>",    lambda e: self._draw(self.normal_bg))
            self.bind("<Button-1>", lambda e: self._click())

    def _draw(self, color):
        self.delete("all")
        c = "#CCCCCC" if self._state == "disabled" else color
        r = self.r
        for ox, oy in [(0,0),(self.w-r*2,0),(0,self.h-r*2),(self.w-r*2,self.h-r*2)]:
            self.create_oval(ox, oy, ox+r*2, oy+r*2, fill=c, outline=c)
        self.create_rectangle(r, 0, self.w-r, self.h, fill=c, outline=c)
        self.create_rectangle(0, r, self.w, self.h-r, fill=c, outline=c)
        tc = "#888888" if self._state == "disabled" else self.fg
        self.create_text(self.w//2, self.h//2, text=self.text,
                         fill=tc, font=(FONT, 10, "bold"))

    def _click(self):
        if self.command and self._state == "normal":
            self.command()

    def set_state(self, state):
        self._state = state
        self.config(cursor="hand2" if state == "normal" else "arrow")
        self._draw(self.normal_bg)
        if state == "normal":
            self.bind("<Enter>",    lambda e: self._draw(self.hover_bg))
            self.bind("<Leave>",    lambda e: self._draw(self.normal_bg))
            self.bind("<Button-1>", lambda e: self._click())
        else:
            self.unbind("<Enter>")
            self.unbind("<Leave>")
            self.unbind("<Button-1>")


# ═════════════════════════════════════════════════════════════════════════════
#  SALES TAB
# ═════════════════════════════════════════════════════════════════════════════
class SalesTab(tk.Tk):
    """
    Sales workflow:
      1. Select Production → Performance → Seat
      2. Fill customer details
      3. Confirm & Issue Ticket
         - purchaseTicket()    → creates Ticket row + marks seat unavailable
         - createTransaction() → records commission-trackable transaction
         - Right panel updates to show the issued receipt (no popup)

    Access rules (from case study):
      • Commissioned staff  → full access (select + purchase/reserve)
      • Full_Time (manager) → view-only  (cannot issue tickets)
      • Hourly staff        → no access  (handled at login level)

    Commission tracking:
      Every createTransaction() call stores staff_id + amount in Transactions.
      Managers view commission via TransactionService.viewCommissionByStaff()
      in the Finances tab — no extra work needed here.
    """

    def __init__(self, session: AppSession = None):
        super().__init__()
        self.title("My Metropolitan Theater — Box Office")
        self._center(1420, 840)
        self.configure(bg=BG_MAIN)

        # session: who is logged in
        self.session = session or AppSession()

        self.db = start_database()
        if not self.db:
            messagebox.showerror("Database Error", "Database connection failed.")
            self.destroy()
            return

        # ── state ─────────────────────────────────────────────────────────────
        self.prod_map    = {}
        self.perf_map    = {}
        self.seat_map    = {}
        self.active_btns = {}

        self.sel_prod_id    = None
        self.sel_prod_title = None
        self.sel_perf_id    = None
        self.sel_perf_label = None
        self.sel_ps_id      = None
        self.sel_seat_name  = None
        self.sel_seat_price = 0.0
        self.sel_seat_view  = ""

        # receipt mode: "form" (input) or "issued" (show receipt)
        self._receipt_mode = "form"

        # ── build UI ──────────────────────────────────────────────────────────
        self._build_topbar()
        body = tk.Frame(self, bg=BG_MAIN)
        body.pack(fill="both", expand=True)
        self._build_sidebar(body)
        content = tk.Frame(body, bg=BG_MAIN)
        content.pack(side="left", fill="both", expand=True, padx=16, pady=16)

        # header row: title + logged-in staff badge
        hdr = tk.Frame(content, bg=BG_MAIN)
        hdr.pack(fill="x", pady=(0, 10))
        tk.Label(hdr, text="Box Office  —  Ticketing Interface",
                 fg=ACCENT, bg=BG_MAIN,
                 font=(FONT, 20, "bold")).pack(side="left")

        # staff badge top-right
        badge_bg = "#2E2E2E"
        badge = tk.Frame(hdr, bg=badge_bg, padx=10, pady=4)
        badge.pack(side="right")
        role_lbl = "Manager" if self.session.is_manager else "Sales Agent"
        tk.Label(badge,
                 text=f"👤  {self.session.staff_name}  ·  {role_lbl}",
                 bg=badge_bg, fg=TEXT_LIGHT,
                 font=(FONT, 9)).pack()

        main_row = tk.Frame(content, bg=BG_MAIN)
        main_row.pack(fill="both", expand=True)
        self._build_left(main_row)
        self._build_right(main_row)

        # if manager, show view-only notice on right panel
        if self.session.is_manager:
            self._show_manager_notice()

        self._load_productions()

    # ── window centering ──────────────────────────────────────────────────────
    def _center(self, w, h):
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(ws-w)//2}+{(hs-h)//2}")

    # ── top bar ───────────────────────────────────────────────────────────────
    def _build_topbar(self):
        tb = tk.Frame(self, bg=BG_TOPBAR, height=45)
        tb.pack(fill="x", side="top")
        tb.pack_propagate(False)
        tk.Label(tb, text="MY METROPOLITAN THEATER",
                 fg=ACCENT, bg=BG_TOPBAR,
                 font=(FONT, 13, "bold")).pack(side="left", padx=18, pady=10)

    # ── sidebar (DO NOT CHANGE — shared across tabs) ──────────────────────────
    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=BG_SIDEBAR, width=175)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)
        for icon, label in [("🎭","Catalog"),("🎟","Sales"),
                             ("👤","Personnel"),("💰","Finances"),("👥","Customers")]:
            active = label == "Sales"
            bg = BG_ACTIVE if active else BG_SIDEBAR
            fg = ACCENT    if active else TEXT_LIGHT
            fr = tk.Frame(sb, bg=bg); fr.pack(fill="x")
            tk.Label(fr, text=icon,  bg=bg, fg=fg,
                     font=("Arial",13), width=3).pack(side="left", padx=(10,4), pady=12)
            tk.Label(fr, text=label, bg=bg, fg=fg,
                     font=(FONT,12,"bold" if active else "normal")).pack(side="left")

    # ── left panel ────────────────────────────────────────────────────────────
    def _build_left(self, parent):
        lp = tk.Frame(parent, bg=BG_PANEL)
        lp.pack(side="left", fill="both", expand=True, padx=(0, 12))

        # combos
        sel_row = tk.Frame(lp, bg=BG_PANEL)
        sel_row.pack(fill="x", padx=16, pady=12)

        pf = tk.Frame(sel_row, bg=BG_PANEL)
        pf.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(pf, text="Select Production", bg=BG_PANEL, fg=TEXT_DARK,
                 font=(FONT, 10, "bold")).pack(anchor="w", pady=(0,2))
        self.prod_combo = ttk.Combobox(pf, state="readonly", font=(FONT, 10))
        self.prod_combo.pack(fill="x")
        self.prod_combo.bind("<<ComboboxSelected>>", self._on_prod_changed)

        perf_f = tk.Frame(sel_row, bg=BG_PANEL)
        perf_f.pack(side="left", fill="x", expand=True)
        tk.Label(perf_f, text="Available Schedule", bg=BG_PANEL, fg=TEXT_DARK,
                 font=(FONT, 10, "bold")).pack(anchor="w", pady=(0,2))
        self.perf_combo = ttk.Combobox(perf_f, state="disabled", font=(FONT, 10))
        self.perf_combo.pack(fill="x")
        self.perf_combo.bind("<<ComboboxSelected>>", self._on_perf_changed)

        # stage header
        stage = tk.Frame(lp, bg=BG_STAGE, height=30)
        stage.pack(fill="x", padx=16, pady=(4, 10))
        stage.pack_propagate(False)
        tk.Label(stage, text="THEATER STAGE  —  FRONT",
                 bg=BG_STAGE, fg=TEXT_DARK,
                 font=(FONT, 10, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        # seat matrix
        self.matrix_wrapper = tk.Frame(lp, bg=BG_PANEL)
        self.matrix_wrapper.pack(fill="both", expand=True, padx=16)
        self._render_empty_matrix()

        # legend
        leg = tk.Frame(lp, bg=BG_PANEL)
        leg.pack(fill="x", padx=16, pady=12)
        for color, lbl in [(SEAT_AVAIL,"Available"),(SEAT_SOLD,"Sold / Reserved"),(SEAT_SEL,"Selected")]:
            c = tk.Canvas(leg, width=14, height=14, bg=BG_PANEL, highlightthickness=0)
            c.pack(side="left", padx=(10,4))
            c.create_rectangle(0,0,14,14, fill=color, outline=color)
            tk.Label(leg, text=lbl, bg=BG_PANEL, fg=TEXT_DARK,
                     font=(FONT,9)).pack(side="left", padx=(0,10))

        # seat view preview
        cam_lf = tk.LabelFrame(lp, text="Seat View Preview",
                               bg=BG_PANEL, fg=TEXT_MID, font=(FONT,9,"italic"))
        cam_lf.pack(fill="x", padx=16, pady=(0,14))
        self.cam_canvas = tk.Canvas(cam_lf, height=85, bg="#D0D0D0",
                                    highlightthickness=1,
                                    highlightbackground="#CCCCCC")
        self.cam_canvas.pack(fill="x", padx=8, pady=6)
        self.cam_txt = self.cam_canvas.create_text(
            400, 42,
            text="[ Select an available seat to preview the stage view ]",
            fill=TEXT_MID, font=(FONT,10,"italic"))

    # ── right panel ───────────────────────────────────────────────────────────
    def _build_right(self, parent):
        self.rp = tk.Frame(parent, bg=BG_RECEIPT, width=340)
        self.rp.pack(side="right", fill="y")
        self.rp.pack_propagate(False)
        self._build_form_panel()

    def _build_form_panel(self):
        """Default right panel: ticket summary + customer form + confirm button."""
        self._clear_right_panel()
        self._receipt_mode = "form"

        # ── TICKET RECEIPT header ──────────────────────────────────────────────
        tk.Label(self.rp, text="TICKET RECEIPT", bg=BG_RECEIPT, fg=TEXT_DARK,
                 font=(FONT,11,"bold")).pack(pady=(14,4))
        tk.Frame(self.rp, height=2, bg=ACCENT).pack(fill="x", padx=20)

        # summary vars
        self.bill_prod  = tk.StringVar(value="Show: —")
        self.bill_perf  = tk.StringVar(value="Schedule: —")
        self.bill_seat  = tk.StringVar(value="Seat: None selected")
        self.bill_price = tk.StringVar(value="Price: Php 0.00")

        for var in (self.bill_prod, self.bill_perf, self.bill_seat):
            tk.Label(self.rp, textvariable=var, bg=BG_RECEIPT, fg=TEXT_DARK,
                     font=(FONT,10), anchor="w").pack(fill="x", padx=20, pady=4)
        tk.Label(self.rp, textvariable=self.bill_price, bg=BG_RECEIPT, fg=ACCENT,
                 font=(FONT,11,"bold"), anchor="w").pack(fill="x", padx=20, pady=4)

        tk.Frame(self.rp, height=1, bg="#DDDDDD").pack(fill="x", padx=20, pady=8)

        # ── customer fields (only for commissioned staff) ──────────────────────
        if self.session.can_transact:
            inp = tk.LabelFrame(self.rp, text="Customer Details",
                                bg=BG_RECEIPT, font=(FONT,9,"bold"))
            inp.pack(fill="x", padx=16, pady=(0,10))

            for label, attr in [("Full Name","ent_name"),
                                 ("Email Address","ent_email"),
                                 ("Mobile Number (11 digits)","ent_phone")]:
                tk.Label(inp, text=label, bg=BG_RECEIPT,
                         font=(FONT,9)).pack(anchor="w", padx=10, pady=(6,0))
                e = tk.Entry(inp, font=(FONT,10), relief="solid", bd=1)
                e.pack(fill="x", padx=10, pady=(2,0))
                setattr(self, attr, e)

            tk.Frame(inp, height=8, bg=BG_RECEIPT).pack()

            # transaction type
            tx_row = tk.Frame(self.rp, bg=BG_RECEIPT)
            tx_row.pack(fill="x", padx=16, pady=(0,6))
            tk.Label(tx_row, text="Transaction Type:", bg=BG_RECEIPT,
                     fg=TEXT_DARK, font=(FONT,9)).pack(side="left")
            self.tx_type = ttk.Combobox(tx_row, values=["purchased","reserved"],
                                        state="readonly", font=(FONT,9), width=12)
            self.tx_type.set("purchased")
            self.tx_type.pack(side="left", padx=(8,0))

            # confirm button
            self.btn_checkout = ModernButton(
                self.rp, text="CONFIRM & ISSUE TICKET",
                command=self._handle_checkout,
                width=260, height=40, radius=8,
                bg=ACCENT, hbg=ACCENT_HOVER
            )
            self.btn_checkout.pack(pady=10)

            self.status_lbl = tk.Label(self.rp, text="", bg=BG_RECEIPT, fg=TEXT_MID,
                                       font=(FONT,8), wraplength=280, justify="left")
            self.status_lbl.pack(padx=16, pady=(0,8))

    def _show_manager_notice(self):
        """Replaces the right panel form with a manager view-only notice."""
        self._clear_right_panel()
        tk.Label(self.rp, text="TICKET RECEIPT", bg=BG_RECEIPT, fg=TEXT_DARK,
                 font=(FONT,11,"bold")).pack(pady=(14,4))
        tk.Frame(self.rp, height=2, bg=ACCENT).pack(fill="x", padx=20)

        notice = tk.Frame(self.rp, bg="#FFF8E1", padx=12, pady=12)
        notice.pack(fill="x", padx=20, pady=20)
        tk.Label(notice,
                 text="👁  Manager View",
                 bg="#FFF8E1", fg="#7B5800",
                 font=(FONT,10,"bold")).pack(anchor="w")
        tk.Label(notice,
                 text="You are logged in as a manager.\n\n"
                      "Only commissioned sales agents\n"
                      "can issue or reserve tickets.\n\n"
                      "You may view the seat map and\n"
                      "check availability, but cannot\n"
                      "complete a transaction.",
                 bg="#FFF8E1", fg="#5C4000",
                 font=(FONT,9), justify="left").pack(anchor="w", pady=(6,0))

    def _show_issued_receipt(self, ticket_number, seat_name, prod_title,
                             perf_label, customer_name, customer_email,
                             customer_phone, amount, tx_type, tx_id):
        """
        Replaces the right panel with a formatted receipt after a successful sale.
        No popup — everything shows inline on the right panel.
        Matches the receipt layout in the project reference image.
        """
        self._clear_right_panel()
        self._receipt_mode = "issued"

        # ── header ────────────────────────────────────────────────────────────
        tk.Label(self.rp, text="My Metropolitan Theater",
                 bg=BG_RECEIPT, fg=TEXT_DARK,
                 font=(FONT, 11, "bold")).pack(pady=(14,0))
        tk.Label(self.rp, text="OFFICIAL RECEIPT",
                 bg=BG_RECEIPT, fg=TEXT_MID,
                 font=(FONT, 8)).pack()

        tk.Frame(self.rp, height=1, bg="#DDDDDD").pack(fill="x", padx=20, pady=6)

        # transaction meta
        tx_label = f"#TXN-{str(tx_id).zfill(4)}" if tx_id else "—"
        for text in [
            f"Transaction ID: {tx_label}",
            f"Date: {date.today().strftime('%B %d, %Y')}",
            f"Staff: {self.session.staff_name} (ID: ST-{str(self.session.staff_id).zfill(3)})",
        ]:
            tk.Label(self.rp, text=text, bg=BG_RECEIPT, fg=TEXT_DARK,
                     font=(FONT,9), anchor="center").pack()

        self._receipt_divider("CUSTOMER DETAILS")

        for text in [
            f"Name: {customer_name}",
            f"Email: {customer_email}",
            f"Mobile: {customer_phone}",
        ]:
            tk.Label(self.rp, text=text, bg=BG_RECEIPT, fg=TEXT_DARK,
                     font=(FONT,9), anchor="center").pack(pady=1)

        self._receipt_divider("TICKET INFORMATION")

        status_text = "Paid" if tx_type == "purchased" else "Reserved"
        for text in [
            f"Ticket No: {ticket_number}",
            f"Production: {prod_title}",
            f"Performance: {perf_label}",
            f"Seat: {seat_name}",
            f"Status: {status_text}",
        ]:
            tk.Label(self.rp, text=text, bg=BG_RECEIPT, fg=TEXT_DARK,
                     font=(FONT,9), anchor="center").pack(pady=1)

        self._receipt_divider("PAYMENT SUMMARY")

        tk.Label(self.rp, text="Payment Method: Cash",
                 bg=BG_RECEIPT, fg=TEXT_DARK,
                 font=(FONT,9), anchor="center").pack(pady=1)
        tk.Label(self.rp,
                 text=f"Total Amount:  ₱{amount:,.2f}",
                 bg=BG_RECEIPT, fg=ACCENT,
                 font=(FONT,11,"bold"), anchor="center").pack(pady=(4,2))

        tk.Frame(self.rp, height=1, bg="#DDDDDD").pack(fill="x", padx=20, pady=10)

        # ── New Transaction button ─────────────────────────────────────────────
        ModernButton(
            self.rp, text="NEW TRANSACTION",
            command=self._new_transaction,
            width=260, height=38, radius=8,
            bg="#2E7D32", hbg="#1B5E20"
        ).pack(pady=(0,6))

        # small print
        tk.Label(self.rp,
                 text=f"Commission recorded for {self.session.staff_name}",
                 bg=BG_RECEIPT, fg="#888888",
                 font=(FONT, 7, "italic")).pack(pady=(0,10))

    def _receipt_divider(self, title):
        """Draws a labelled divider line inside the receipt panel."""
        fr = tk.Frame(self.rp, bg=BG_RECEIPT)
        fr.pack(fill="x", padx=20, pady=(10,4))
        tk.Frame(fr, height=1, bg="#CCCCCC").pack(fill="x")
        tk.Label(fr, text=title, bg=BG_RECEIPT, fg=TEXT_MID,
                 font=(FONT, 8, "bold")).pack(pady=2)
        tk.Frame(fr, height=1, bg="#CCCCCC").pack(fill="x")

    def _clear_right_panel(self):
        for w in self.rp.winfo_children():
            w.destroy()

    def _new_transaction(self):
        """Reset everything for a fresh ticket sale."""
        self._build_form_panel()
        # restore selection state display vars (re-bound after rebuild)
        self.bill_prod.set(f"Show: {self.sel_prod_title}" if self.sel_prod_title else "Show: —")
        self.bill_perf.set(f"Schedule: {self.sel_perf_label}" if self.sel_perf_label else "Schedule: —")
        self.bill_seat.set("Seat: None selected")
        self.bill_price.set("Price: Php 0.00")
        self._reset_seat_selection_only()

    # ═══════════════════════════════════════════════════════════════════════════
    #  DATA LOADING
    # ═══════════════════════════════════════════════════════════════════════════

    def _load_productions(self):
        try:
            res = self.db.service.production.viewAllProductions()
            if not res or isinstance(res, str):
                self.prod_combo["values"] = ["No productions available"]
                return
            self.prod_map = {}
            titles = []
            for p in res:
                if isinstance(p, dict):
                    pid, title = p["production_id"], p["title"]
                else:
                    pid, title = p[0], p[1]
                self.prod_map[title] = pid
                titles.append(title)
            self.prod_combo["values"] = titles
        except Exception as ex:
            print(f"[SalesTab] load_productions error: {ex}")
            self.prod_combo["values"] = ["Error loading productions"]

    def _on_prod_changed(self, _=None):
        title = self.prod_combo.get()
        pid   = self.prod_map.get(title)
        if not pid:
            return

        self.sel_prod_id    = pid
        self.sel_prod_title = title

        # update form panel if it's visible
        if self._receipt_mode == "form" and hasattr(self, "bill_prod"):
            self.bill_prod.set(f"Show: {title}")

        self._reset_seat_state()
        self._render_empty_matrix()
        self.perf_combo.set("Loading schedules…")
        self.perf_combo.configure(state="disabled")

        try:
            schedules = self.db.service.performance.locatePerformanceByProductionId(pid)
            if not schedules or isinstance(schedules, str):
                self.perf_combo.set("No schedules found")
                return

            self.perf_map = {}
            entries = []
            for s in schedules:
                if isinstance(s, dict):
                    perf_id   = s["performance_id"]
                    perf_date = fmt_short_date(s.get("date"))
                    p_start   = fmt_time(s.get("start_time"))
                    p_end     = fmt_time(s.get("end_time"))
                else:
                    perf_id   = s[0]
                    perf_date = fmt_short_date(s[4])
                    p_start   = fmt_time(s[2])
                    p_end     = fmt_time(s[3])

                lbl = f"{perf_date}  {p_start} – {p_end}"
                self.perf_map[lbl] = s if isinstance(s, dict) else {
                    "performance_id": s[0], "start_time": s[2],
                    "end_time": s[3], "date": s[4], "total_seats": s[5]
                }
                entries.append(lbl)

            self.perf_combo["values"] = entries
            self.perf_combo.set("Select a schedule")
            self.perf_combo.configure(state="readonly")

        except Exception as ex:
            print(f"[SalesTab] load_performances error: {ex}")
            self.perf_combo.set("Error loading schedules")

    def _on_perf_changed(self, _=None):
        lbl  = self.perf_combo.get()
        perf = self.perf_map.get(lbl)
        if not perf:
            return

        perf_id = perf["performance_id"] if isinstance(perf, dict) else perf[0]
        self.sel_perf_id    = perf_id
        self.sel_perf_label = lbl

        if self._receipt_mode == "form" and hasattr(self, "bill_perf"):
            self.bill_perf.set(f"Schedule: {lbl}")

        self._reset_seat_state()
        self._build_seat_grid(perf_id)

    # ═══════════════════════════════════════════════════════════════════════════
    #  SEAT GRID
    # ═══════════════════════════════════════════════════════════════════════════

    def _render_empty_matrix(self):
        for w in self.matrix_wrapper.winfo_children():
            w.destroy()
        tk.Label(self.matrix_wrapper,
                 text="Select a production and schedule to load the seat map.",
                 bg=BG_PANEL, fg=TEXT_MID,
                 font=(FONT, 10, "italic")).pack(expand=True, pady=40)

    def _build_seat_grid(self, perf_id):
        for w in self.matrix_wrapper.winfo_children():
            w.destroy()
        self.active_btns.clear()
        self.seat_map.clear()

        grid = tk.Frame(self.matrix_wrapper, bg=BG_PANEL)
        grid.pack(pady=10)

        try:
            seats = self.db.service.performanceSeat.viewAllSeatsByPerformance(perf_id)

            if not seats or isinstance(seats, str):
                tk.Label(grid,
                         text=f"No seat data found for this performance.\n({seats})",
                         bg=BG_PANEL, fg=ACCENT).pack(pady=20)
                return

            COLS = 6
            for idx, s in enumerate(seats[:30]):
                r_idx = idx // COLS
                c_idx = idx % COLS

                if isinstance(s, dict):
                    ps_id     = s.get("performance_seat_id")
                    seat_num  = s.get("seat_number", f"S{idx+1}")
                    is_avail  = bool(s.get("is_available", False))
                    view_path = s.get("seat_view", "")
                    price     = float(s.get("price", 0))
                else:
                    ps_id     = s[0]
                    seat_num  = s[3] if len(s) > 3 else f"S{idx+1}"
                    is_avail  = str(s[6]).strip().lower() in ("true","1","t") if len(s) > 6 else False
                    view_path = s[4] if len(s) > 4 else ""
                    price     = float(s[5]) if len(s) > 5 else 0.0

                self.seat_map[ps_id] = {
                    "performance_seat_id": ps_id,
                    "seat_number":  seat_num,
                    "is_available": is_avail,
                    "seat_view":    view_path,
                    "price":        price,
                }

                base_color = SEAT_AVAIL if is_avail else SEAT_SOLD
                # managers see seats but cannot click to select for purchase
                can_click  = is_avail and self.session.can_transact
                btn_state  = "normal" if can_click else "disabled"

                btn = tk.Button(
                    grid,
                    text=seat_num,
                    bg=base_color,
                    fg=TEXT_LIGHT,
                    font=(FONT, 9, "bold"),
                    width=7, height=2,
                    relief="flat",
                    state=btn_state,
                    disabledforeground="#E0E0E0",
                    activebackground=SEAT_AVAIL_H,
                )
                btn.grid(row=r_idx, column=c_idx, padx=5, pady=5)

                if can_click:
                    btn.config(command=lambda sid=ps_id, b=btn: self._on_seat_click(sid, b))

                self.active_btns[ps_id] = (btn, base_color)

        except Exception as ex:
            tk.Label(grid, text=f"Error building seat grid:\n{ex}",
                     bg=BG_PANEL, fg=ACCENT).pack(pady=20)
            print(f"[SalesTab] build_seat_grid error: {ex}")

    def _on_seat_click(self, ps_id, clicked_btn):
        # restore previous selection
        if self.sel_ps_id and self.sel_ps_id in self.active_btns:
            old_btn, old_color = self.active_btns[self.sel_ps_id]
            old_btn.config(bg=old_color)

        self.sel_ps_id = ps_id
        clicked_btn.config(bg=SEAT_SEL)

        seat = self.seat_map.get(ps_id, {})
        self.sel_seat_name  = seat.get("seat_number", "—")
        self.sel_seat_price = seat.get("price",       0.0)
        self.sel_seat_view  = seat.get("seat_view",   "")

        if self._receipt_mode == "form" and hasattr(self, "bill_seat"):
            self.bill_seat.set(f"Seat: {self.sel_seat_name}")
            self.bill_price.set(f"Price:  Php {self.sel_seat_price:,.2f}")

        preview_text = (
            f"View from seat {self.sel_seat_name}  →  {self.sel_seat_view}"
            if self.sel_seat_view
            else f"No view image available for seat {self.sel_seat_name}."
        )
        self.cam_canvas.itemconfig(self.cam_txt, text=preview_text)

    # ═══════════════════════════════════════════════════════════════════════════
    #  CHECKOUT
    # ═══════════════════════════════════════════════════════════════════════════

    def _handle_checkout(self):
        """
        Full purchase flow:
          1. Validate seat + performance + customer fields
          2. getOrCreateCustomer
          3. purchaseTicket  → creates Ticket + marks seat FALSE
          4. createTransaction → records staff_id + amount (commission source)
          5. Show inline receipt on right panel (no popup)
        """
        # ── access guard ──────────────────────────────────────────────────────
        if not self.session.can_transact:
            messagebox.showwarning("Access Denied",
                                   "Only commissioned sales agents can issue tickets.",
                                   parent=self)
            return

        if not self.sel_ps_id:
            messagebox.showwarning("No Seat",
                                   "Please select a seat from the theater map first.",
                                   parent=self)
            return

        if not self.sel_perf_id:
            messagebox.showwarning("No Schedule",
                                   "Please select a performance schedule first.",
                                   parent=self)
            return

        raw_name  = self.ent_name.get().strip()
        raw_email = self.ent_email.get().strip()
        raw_phone = self.ent_phone.get().strip()
        tx_type   = self.tx_type.get().strip()

        if not raw_name or not raw_email or not raw_phone:
            messagebox.showwarning("Missing Info",
                                   "Please fill in all customer details.",
                                   parent=self)
            return

        # ── step 1: resolve or create customer ────────────────────────────────
        try:
            customer_result = self.db.service.customer.getOrCreateCustomer(
                name=raw_name,
                email=raw_email,
                mobileNumber=raw_phone,
            )
        except Exception as ex:
            messagebox.showerror("Customer Error",
                                 f"Could not resolve customer:\n{ex}", parent=self)
            return

        if isinstance(customer_result, str):
            messagebox.showerror("Customer Validation",
                                 customer_result, parent=self)
            return

        customer_id = customer_result

        # ── step 2: purchase ticket ───────────────────────────────────────────
        try:
            ticket_result = self.db.service.ticket.purchaseTicket(
                performanceSeatId = self.sel_ps_id,
                customerId        = customer_id,
                status            = "sold" if tx_type == "purchased" else "reserved",
                saleDate          = date.today(),
                ticketNumber      = None,
            )
        except Exception as ex:
            messagebox.showerror("Ticket Error",
                                 f"Could not issue ticket:\n{ex}", parent=self)
            return

        if isinstance(ticket_result, str):
            if "already has an existing ticket" in ticket_result.lower():
                messagebox.showwarning(
                    "Seat Already Booked",
                    "⚠  This seat has already been assigned a ticket.\n\n"
                    "Please select a different seat.",
                    parent=self
                )
            else:
                messagebox.showerror("Purchase Failed", ticket_result, parent=self)
            return

        ticket_number = ticket_result.get("ticket_number", "—")

        # ── step 3: create transaction (commission is auto-recorded here) ──────
        tx_id = None
        try:
            ticket_lookup = self.db.service.ticket.locateTicketByNumber(ticket_number)
            ticket_id = ticket_lookup["ticket_id"] if isinstance(ticket_lookup, dict) else None

            if ticket_id:
                tx = Transaction(
                    ticketId        = ticket_id,
                    staffId         = self.session.staff_id,   # ← logged-in staff
                    transactionDate = date.today().strftime("%Y-%m-%d"),
                    type            = tx_type,
                    amount          = self.sel_seat_price,
                )
                tx_result = self.db.service.transaction.createTransaction(tx)

                # try to get the new transaction_id for the receipt
                try:
                    all_tx = self.db.service.transaction.locateTransactionsByTicket(ticket_id)
                    if all_tx and isinstance(all_tx, list):
                        tx_id = all_tx[-1].get("transaction_id")
                except Exception:
                    pass

                if isinstance(tx_result, str) and tx_result != "Successfully created transaction.":
                    print(f"[SalesTab] transaction warning: {tx_result}")

        except Exception as ex:
            print(f"[SalesTab] transaction logging error (non-critical): {ex}")

        # ── step 4: mark seat red in grid ─────────────────────────────────────
        if self.sel_ps_id in self.active_btns:
            btn, _ = self.active_btns[self.sel_ps_id]
            btn.config(bg=SEAT_SOLD, state="disabled", command=lambda: None)
            self.active_btns[self.sel_ps_id] = (btn, SEAT_SOLD)

        # ── step 5: show inline receipt (replaces form, no popup) ─────────────
        self._show_issued_receipt(
            ticket_number  = ticket_number,
            seat_name      = self.sel_seat_name,
            prod_title     = self.sel_prod_title or "—",
            perf_label     = self.sel_perf_label or "—",
            customer_name  = raw_name,
            customer_email = raw_email,
            customer_phone = raw_phone,
            amount         = self.sel_seat_price,
            tx_type        = tx_type,
            tx_id          = tx_id,
        )

        # reset seat selection so the grid stays interactive for next ticket
        self._reset_seat_selection_only()

    # ── resets ────────────────────────────────────────────────────────────────
    def _reset_seat_selection_only(self):
        """Clears only the selected seat highlight — keeps production/perf choice."""
        self.sel_ps_id      = None
        self.sel_seat_name  = None
        self.sel_seat_price = 0.0
        self.sel_seat_view  = ""
        self.cam_canvas.itemconfig(
            self.cam_txt,
            text="[ Select an available seat to preview the stage view ]"
        )

    def _reset_seat_state(self):
        """Full reset including receipt vars."""
        self._reset_seat_selection_only()
        if self._receipt_mode == "form":
            if hasattr(self, "bill_seat"):
                self.bill_seat.set("Seat: None selected")
            if hasattr(self, "bill_price"):
                self.bill_price.set("Price: Php 0.00")


# ── entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Default: logged in as commissioned staff (sales agent)
    # Replace with your real login session before launching
    session = AppSession(
        staff_id   = 23,
        staff_name = "Marius Aquino",
        staff_type = "Commissioned"   # change to "Full_Time" to test manager view
    )
    app = SalesTab(session=session)
    app.mainloop()