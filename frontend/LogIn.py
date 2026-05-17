import tkinter as tk
import tkinter.messagebox

# ── Colors ───────────────────────────────────────────────────────────────────
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

RADIUS = 14   # corner radius for fields & buttons

# ── Rounded-rect canvas helper ────────────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    """Draw a rounded rectangle on a Canvas."""
    canvas.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,  style="pieslice", **kw)
    canvas.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,  style="pieslice", **kw)
    canvas.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,  style="pieslice", **kw)
    canvas.create_rectangle(x1+r, y1,   x2-r, y2,   **kw)
    canvas.create_rectangle(x1,   y1+r, x2,   y2-r, **kw)

# ── Rounded field (icon + entry) ──────────────────────────────────────────────
def make_field(parent, icon, placeholder, is_pass=False, field_width=280, bg=None):
    """Returns a Frame containing icon label + rounded canvas entry."""
    bg = bg or BG_LIGHT
    h  = 46   # total height of the field row

    row = tk.Frame(parent, bg=bg)
    row.pack(pady=8)

    # Icon
    tk.Label(row, text=icon, font=FONT_ICON, bg=bg, fg=ACCENT).pack(side="left", padx=(0, 8))

    # Canvas draws the rounded background
    canvas = tk.Canvas(row, width=field_width, height=h,
                    bg=bg, highlightthickness=0, bd=0)
    canvas.pack(side="left")

    def draw(color):
        canvas.delete("bg")
        rounded_rect(canvas, 0, 0, field_width, h, RADIUS,
                    fill=color, outline=color, tags="bg")
        canvas.tag_lower("bg")

    draw(INPUT_BG)

    # Actual entry sits on top of the canvas
    entry = tk.Entry(canvas, font=FONT_INPUT, bg=INPUT_BG, fg=TEXT_MID,
                    relief="flat", bd=0, insertbackground=TEXT_DARK,
                    highlightthickness=0)
    PAD_X = RADIUS + 14   # inner left padding (keeps text away from rounded edge)
    entry_win = canvas.create_window(PAD_X, h // 2, anchor="w",
                                    window=entry, width=field_width - PAD_X*2)

    # Placeholder
    entry.insert(0, placeholder)
    active = [False]

    def focus_in(_):
        if not active[0]:
            entry.delete(0, "end")
            entry.config(fg=TEXT_DARK)
            if is_pass:
                entry.config(show="*")
            active[0] = True

    def focus_out(_):
        if entry.get() == "":
            entry.config(show="", fg=TEXT_MID)
            entry.insert(0, placeholder)
            active[0] = False

    entry.bind("<FocusIn>",  focus_in)
    entry.bind("<FocusOut>", focus_out)

    # Hover
    def on_enter(_): draw(INPUT_HOV); entry.config(bg=INPUT_HOV)
    def on_leave(_): draw(INPUT_BG);  entry.config(bg=INPUT_BG)
    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    entry.bind("<Enter>",  on_enter)
    entry.bind("<Leave>",  on_leave)

    return entry

# ── Rounded button ────────────────────────────────────────────────────────────
def make_button(parent, text, command, btn_width=130, bg=None):
    """Canvas-drawn rounded button."""
    bg_parent = bg or BG_LIGHT
    h = 48

    canvas = tk.Canvas(parent, width=btn_width, height=h,
                    bg=bg_parent, highlightthickness=0, bd=0)

    def draw(color):
        canvas.delete("all")
        rounded_rect(canvas, 0, 0, btn_width, h, RADIUS,
                    fill=color, outline=color)
        canvas.create_text(btn_width // 2, h // 2, text=text,
                        fill=TEXT_LIGHT, font=FONT_BTN)

    draw(ACCENT)
    canvas.bind("<Enter>",    lambda _: draw(ACCENT_HOV))
    canvas.bind("<Leave>",    lambda _: draw(ACCENT))
    canvas.bind("<Button-1>", lambda _: command())
    canvas.config(cursor="hand2")
    return canvas

# ── Center a Toplevel over its parent ─────────────────────────────────────────
def center_on_parent(win, parent, w, h):
    parent.update_idletasks()
    px = parent.winfo_x()
    py = parent.winfo_y()
    pw = parent.winfo_width()
    ph = parent.winfo_height()
    x  = px + (pw - w) // 2
    y  = py + (ph - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

# ── Sign-up popup ─────────────────────────────────────────────────────────────
def open_signup_window(event=None):
    W, H = 480, 600
    win  = tk.Toplevel(root)
    win.title("Sign Up")
    win.configure(bg=BG_LIGHT)
    win.resizable(False, False)
    win.transient(root)
    win.grab_set()
    center_on_parent(win, root, W, H)

    container = tk.Frame(win, bg=BG_LIGHT)
    container.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(container, text="Sign Up", fg=ACCENT, bg=BG_LIGHT,
            font=(FONT, 28, "bold")).pack(pady=(0, 4))

    tk.Label(container, text="Create your account to get started",
            fg=TEXT_MID, bg=BG_LIGHT, font=FONT_SMALL).pack(pady=(0, 20))

    fields = [
        ("👤", "Username",         False),
        ("✉",  "Email",            False),
        ("🔒", "Password",         True),
        ("🔒", "Confirm Password", True),
    ]
    for icon, ph, isp in fields:
        make_field(container, icon, ph, isp, field_width=270)

    make_button(container, "SIGN UP", win.destroy, btn_width=160).pack(pady=28)

# ── Login logic ───────────────────────────────────────────────────────────────
def handle_login():
    import sys
    sys.path.append("backend")
    from start_database import start_database
    from objects.log_in_obj import LogIn

    db = start_database()
    if not db:
        tk.messagebox.showerror("Error", "Cannot connect to database.")
        return

    staff_id = username_entry.get()
    password = password_entry.get()

    try:
        staff_id = int(staff_id)
    except ValueError:
        tk.messagebox.showerror("Error", "Username must be your Staff ID number.")
        return

    result = db.service.log_in.log_in(LogIn(staff_id=staff_id, password=password))

    if result == "Invalid log in credentials. User not found":
        tk.messagebox.showerror("Error", result)
    elif result == "Wrong password.":
        tk.messagebox.showerror("Error", result)
    elif isinstance(result, list):
        role = result[1]
        tk.messagebox.showinfo("Success", f"Welcome! Access level: {role}")
        # TODO: open the correct window based on role

# ── Main window ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("My Metropolitan Theater - Login")
root.geometry("1920x1080")
root.configure(bg=BG_LIGHT)

# Left frame
left_frame = tk.Frame(root, bg=BG_DARK)
left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

tk.Label(
    left_frame,
    text="MY\nMETROPOLITAN\nTHEATER",
    fg=ACCENT, bg=BG_DARK,
    font=FONT_BRAND,
    justify="right",
).place(relx=0.9, rely=0.5, anchor="e")

# Right frame
right_frame = tk.Frame(root, bg=BG_LIGHT)
right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

center_container = tk.Frame(right_frame, bg=BG_LIGHT)
center_container.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(center_container, text="Welcome!", fg=ACCENT, bg=BG_LIGHT,
        font=FONT_TITLE).pack(pady=(0, 10))

tk.Label(center_container, text="Log in to your account to continue",
        fg="#333333", bg=BG_LIGHT, font=(FONT, 14)).pack(pady=(0, 40))

# Username
username_entry = make_field(center_container, "👤", "Username", False, field_width=320)

# Password
password_entry = make_field(center_container, "🔒", "Password", True,  field_width=320)

# Login button
make_button(center_container, "LOG IN", handle_login, btn_width=130).pack(pady=36)

# Sign up link
signup_label = tk.Label(
    center_container,
    text="Don't have an account? Sign up.",
    fg="#333333", bg=BG_LIGHT,
    font=FONT_LINK,
    cursor="hand2",
)
signup_label.pack(pady=(10, 0))
signup_label.bind("<Button-1>", open_signup_window)
signup_label.bind("<Enter>", lambda _: signup_label.config(fg=ACCENT))
signup_label.bind("<Leave>", lambda _: signup_label.config(fg="#333333"))

root.mainloop()