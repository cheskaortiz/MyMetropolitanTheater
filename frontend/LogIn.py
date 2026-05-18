import tkinter as tk
import tkinter.messagebox
import sys
import os
import psycopg2

# ── Database Connection ───────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     "127.0.0.1",
    "port":     5432,
    "dbname":   "MyMetropolitanTheaterDatabase",
    "user":     "postgres",
    "password": "AKOSICYAN69",
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# ── Colors ────────────────────────────────────────────────────────────────────
BG_LIGHT   = "#F0F0F0"
BG_DARK    = "#1E1E1E"
ACCENT     = "#E50914"
ACCENT_HOV = "#B0060F"
INPUT_BG   = "#E0E0E0"
INPUT_HOV  = "#D4D4D4"
TEXT_DARK  = "#222222"
TEXT_MID   = "#888888"
TEXT_LIGHT = "#FFFFFF"

FONT       = "Helvetica"
FONT_INPUT = (FONT, 12)
FONT_BTN   = (FONT, 14, "bold")
FONT_TITLE = (FONT, 43, "bold")
FONT_BRAND = (FONT, 40, "bold")
FONT_ICON  = ("Arial", 20)
FONT_SMALL = (FONT, 11)
FONT_LINK  = ("Arial", 12, "underline")

RADIUS = 14

# ── Rounded-rect canvas helper ────────────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    canvas.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,  style="pieslice", **kw)
    canvas.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,  style="pieslice", **kw)
    canvas.create_rectangle(x1+r, y1,   x2-r, y2,   **kw)
    canvas.create_rectangle(x1,   y1+r, x2,   y2-r, **kw)

# ── Rounded field ─────────────────────────────────────────────────────────────
def make_field(parent, icon, placeholder, is_pass=False, field_width=280, bg=None):
    bg = bg or BG_LIGHT
    h  = 46
    row = tk.Frame(parent, bg=bg)
    row.pack(pady=8)
    tk.Label(row, text=icon, font=FONT_ICON, bg=bg, fg=ACCENT).pack(side="left", padx=(0, 8))
    canvas = tk.Canvas(row, width=field_width, height=h, bg=bg, highlightthickness=0, bd=0)
    canvas.pack(side="left")

    def draw(color):
        canvas.delete("bg")
        rounded_rect(canvas, 0, 0, field_width, h, RADIUS, fill=color, outline=color, tags="bg")
        canvas.tag_lower("bg")

    draw(INPUT_BG)
    entry = tk.Entry(canvas, font=FONT_INPUT, bg=INPUT_BG, fg=TEXT_MID,
                     relief="flat", bd=0, insertbackground=TEXT_DARK, highlightthickness=0)
    PAD_X = RADIUS + 14
    canvas.create_window(PAD_X, h // 2, anchor="w", window=entry, width=field_width - PAD_X*2)
    entry.insert(0, placeholder)
    active = [False]

    def focus_in(_):
        if not active[0]:
            entry.delete(0, "end")
            entry.config(fg=TEXT_DARK)
            if is_pass: entry.config(show="*")
            active[0] = True

    def focus_out(_):
        if entry.get() == "":
            entry.config(show="", fg=TEXT_MID)
            entry.insert(0, placeholder)
            active[0] = False

    entry.bind("<FocusIn>",  focus_in)
    entry.bind("<FocusOut>", focus_out)

    def on_enter(_): draw(INPUT_HOV); entry.config(bg=INPUT_HOV)
    def on_leave(_): draw(INPUT_BG);  entry.config(bg=INPUT_BG)
    canvas.bind("<Enter>", on_enter); canvas.bind("<Leave>", on_leave)
    entry.bind("<Enter>",  on_enter); entry.bind("<Leave>",  on_leave)
    return entry

# ── Rounded button ────────────────────────────────────────────────────────────
def make_button(parent, text, command, btn_width=130, bg=None):
    bg_parent = bg or BG_LIGHT
    h = 48
    canvas = tk.Canvas(parent, width=btn_width, height=h, bg=bg_parent, highlightthickness=0, bd=0)
    def draw(color):
        canvas.delete("all")
        rounded_rect(canvas, 0, 0, btn_width, h, RADIUS, fill=color, outline=color)
        canvas.create_text(btn_width // 2, h // 2, text=text, fill=TEXT_LIGHT, font=FONT_BTN)
    draw(ACCENT)
    canvas.bind("<Enter>",    lambda _: draw(ACCENT_HOV))
    canvas.bind("<Leave>",    lambda _: draw(ACCENT))
    canvas.bind("<Button-1>", lambda _: command())
    canvas.config(cursor="hand2")
    return canvas

# ── Center helper ─────────────────────────────────────────────────────────────
def center_on_parent(win, parent, w, h):
    parent.update_idletasks()
    px = parent.winfo_x(); py = parent.winfo_y()
    pw = parent.winfo_width(); ph = parent.winfo_height()
    win.geometry(f"{w}x{h}+{px + (pw-w)//2}+{py + (ph-h)//2}")

# ── Login logic ───────────────────────────────────────────────────────────────
def handle_login():
    # Import Dashboard from same directory
    dashboard_dir = os.path.dirname(os.path.abspath(__file__))
    if dashboard_dir not in sys.path:
        sys.path.insert(0, dashboard_dir)

    staff_id_str = username_entry.get().strip()
    password     = password_entry.get().strip()

    # Guard against placeholder text still in fields
    if staff_id_str in ("", "Staff ID"):
        tkinter.messagebox.showerror("Error", "Please enter your Staff ID.")
        return
    if password in ("", "Password"):
        tkinter.messagebox.showerror("Error", "Please enter your password.")
        return

    try:
        staff_id = int(staff_id_str)
    except ValueError:
        tkinter.messagebox.showerror("Error", "Staff ID must be a number.")
        return

    # ── Authenticate directly against the DB ──────────────────────────────────
    try:
        conn = get_connection()
        cur  = conn.cursor()

        # Check credentials
        cur.execute(
            "SELECT staff_id FROM Log_In WHERE staff_id = %s AND password = %s;",
            (staff_id, password)
        )
        login_row = cur.fetchone()

        if not login_row:
            cur.close(); conn.close()
            tkinter.messagebox.showerror("Login Failed", "Invalid Staff ID or password.")
            return

        # Determine role: check if this staff_id is a department manager
        cur.execute("SELECT COUNT(*) FROM Department WHERE manager_id = %s;", (staff_id,))
        is_manager = cur.fetchone()[0] > 0

        cur.close(); conn.close()

        role = "MANAGER" if is_manager else "SALES"

    except Exception as e:
        tkinter.messagebox.showerror("DB Error", f"Could not connect to database:\n{e}")
        return

    # ── Open Dashboard ────────────────────────────────────────────────────────
    try:
        from Dashboard import open_dashboard
    except ImportError as e:
        tkinter.messagebox.showerror("Error", f"Could not load Dashboard:\n{e}")
        return

    root.destroy()
    open_dashboard(role, staff_id)

# ── Main window ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("My Metropolitan Theater - Login")
root.geometry("1920x1080")
root.configure(bg=BG_LIGHT)

# Left frame
left_frame = tk.Frame(root, bg=BG_DARK)
left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

tk.Label(left_frame, text="MY\nMETROPOLITAN\nTHEATER",
         fg=ACCENT, bg=BG_DARK, font=FONT_BRAND, justify="right").place(relx=0.9, rely=0.5, anchor="e")

# Right frame
right_frame = tk.Frame(root, bg=BG_LIGHT)
right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

center_container = tk.Frame(right_frame, bg=BG_LIGHT)
center_container.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(center_container, text="Welcome!", fg=ACCENT, bg=BG_LIGHT, font=FONT_TITLE).pack(pady=(0, 10))
tk.Label(center_container, text="Log in to your account to continue",
         fg="#333333", bg=BG_LIGHT, font=(FONT, 14)).pack(pady=(0, 40))

username_entry = make_field(center_container, "👤", "Staff ID", False, field_width=320)
password_entry = make_field(center_container, "🔑", "Password", True,  field_width=320)

make_button(center_container, "LOG IN", handle_login, btn_width=130).pack(pady=36)

# Also allow pressing Enter to login
root.bind("<Return>", lambda _: handle_login())

root.mainloop()