
import tkinter as tk
from tkinter import ttk, messagebox

from main import (
    load_items,
    filter_items,
    sort_items_by_damage,
    sort_items_by_weight,
)


# ==========================================
# COLOR PALETTE
# ==========================================

BG = "#171614"
PANEL = "#24211D"
CARD = "#302A23"
CARD_HOVER = "#3A3228"
GOLD = "#C5A15B"
GOLD_DARK = "#8F713D"
TEXT = "#E8DFC9"
MUTED = "#A69A83"
BORDER = "#514532"
INPUT_BG = "#1D1B18"
ROW_ALT = "#29251F"


def create_main_window():
    """Create the main RPG Build Planner window."""

    root = tk.Tk()
    root.title("RPG Build Planner | Arsenal")
    root.geometry("1180x780")
    root.minsize(950, 650)
    root.configure(bg=BG)

    items = load_items()

    # ==========================================
    # GENERAL STYLING
    # ==========================================

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Dark.TCombobox",
        fieldbackground=INPUT_BG,
        background=CARD,
        foreground=TEXT,
        arrowcolor=GOLD,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        padding=7,
    )

    style.map(
        "Dark.TCombobox",
        fieldbackground=[("readonly", INPUT_BG)],
        foreground=[("readonly", TEXT)],
        selectbackground=[("readonly", INPUT_BG)],
        selectforeground=[("readonly", TEXT)],
    )

    style.configure(
        "Dark.Treeview",
        background=PANEL,
        foreground=TEXT,
        fieldbackground=PANEL,
        rowheight=32,
        borderwidth=0,
        font=("Segoe UI", 10),
    )

    style.configure(
        "Dark.Treeview.Heading",
        background=CARD,
        foreground=GOLD,
        font=("Segoe UI", 9, "bold"),
        relief="flat",
        padding=9,
    )

    style.map(
        "Dark.Treeview",
        background=[("selected", GOLD_DARK)],
        foreground=[("selected", "#FFFFFF")],
    )

    # ==========================================
    # HELPER FUNCTIONS
    # ==========================================

    def create_label(parent, text, size=10, color=TEXT,
                     bold=False, **kwargs):
        """Create a consistently styled label."""

        return tk.Label(
            parent,
            text=text,
            bg=kwargs.pop("bg", parent.cget("bg")),
            fg=color,
            font=(
                "Segoe UI",
                size,
                "bold" if bold else "normal",
            ),
            **kwargs,
        )

    def create_button(parent, text, command, primary=False):
        """Create a styled application button."""

        background = GOLD_DARK if primary else CARD
        foreground = "#FFFFFF" if primary else TEXT

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=background,
            fg=foreground,
            activebackground=GOLD,
            activeforeground=BG,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            borderwidth=0,
            padx=15,
            pady=8,
            cursor="hand2",
        )

        return button

    def create_input(parent, variable, width=12):
        """Create a styled text input."""

        return tk.Entry(
            parent,
            textvariable=variable,
            width=width,
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=GOLD,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=GOLD,
            font=("Segoe UI", 10),
        )

    # ==========================================
    # MAIN CONTAINER
    # ==========================================

    main_frame = tk.Frame(root, bg=BG)
    main_frame.pack(fill="both", expand=True, padx=24, pady=20)

    # ==========================================
    # HEADER
    # ==========================================

    header = tk.Frame(main_frame, bg=BG)
    header.pack(fill="x", pady=(0, 18))

    title_frame = tk.Frame(header, bg=BG)
    title_frame.pack(side="left")

    create_label(
        title_frame,
        "RPG BUILD PLANNER",
        size=23,
        color=GOLD,
        bold=True,
    ).pack(anchor="w")

    create_label(
        title_frame,
        "ARSENAL  |  WEAPON DATABASE",
        size=9,
        color=MUTED,
    ).pack(anchor="w", pady=(3, 0))

    header_info = tk.Frame(header, bg=BG)
    header_info.pack(side="right", anchor="center")

    create_label(
        header_info,
        f"AVAILABLE ITEMS: {len(items)}",
        size=10,
        color=GOLD,
        bold=True,
    ).pack(anchor="e")

    create_label(
        header_info,
        "EQUIPMENT MANAGEMENT",
        size=8,
        color=MUTED,
    ).pack(anchor="e", pady=(4, 0))

    # ==========================================
    # FILTER PANEL
    # ==========================================

    filter_panel = tk.Frame(
        main_frame,
        bg=PANEL,
        highlightbackground=BORDER,
        highlightthickness=1,
    )
    filter_panel.pack(fill="x", pady=(0, 14))

    filter_content = tk.Frame(filter_panel, bg=PANEL)
    filter_content.pack(fill="x", padx=16, pady=14)

    create_label(
        filter_content,
        "WEAPON FILTERS",
        size=11,
        color=GOLD,
        bold=True,
    ).grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 12))

    categories = ["All"] + sorted(
        {item["category"] for item in items}
    )

    category_var = tk.StringVar(value="All")
    strength_var = tk.StringVar()
    dexterity_var = tk.StringVar()
    weight_var = tk.StringVar()

    sort_var = tk.StringVar(value="Default")

    def create_filter_field(parent, label_text, column,
                            variable, width=12, values=None):

        create_label(
            parent,
            label_text,
            size=8,
            color=MUTED,
            bold=True,
        ).grid(
            row=1,
            column=column,
            sticky="w",
            padx=(0, 8),
            pady=(0, 6),
        )

        if values is not None:
            widget = ttk.Combobox(
                parent,
                textvariable=variable,
                values=values,
                state="readonly",
                width=width,
                style="Dark.TCombobox",
            )
        else:
            widget = create_input(
                parent,
                variable,
                width,
            )

        widget.grid(
            row=2,
            column=column,
            sticky="ew",
            padx=(0, 10),
        )

        return widget

    create_filter_field(
        filter_content,
        "CATEGORY",
        0,
        category_var,
        width=14,
        values=categories,
    )

    create_filter_field(
        filter_content,
        "MAX STRENGTH",
        1,
        strength_var,
        width=10,
    )

    create_filter_field(
        filter_content,
        "MAX DEXTERITY",
        2,
        dexterity_var,
        width=10,
    )

    create_filter_field(
        filter_content,
        "MAX WEIGHT",
        3,
        weight_var,
        width=10,
    )

    # ==========================================
    # SORTING AND FILTER BUTTONS
    # ==========================================

    sorting_frame = tk.Frame(filter_content, bg=PANEL)
    sorting_frame.grid(
        row=3,
        column=0,
        columnspan=8,
        sticky="ew",
        pady=(14, 0),
    )

    create_label(
        sorting_frame,
        "SORT BY",
        size=8,
        color=MUTED,
        bold=True,
    ).pack(side="left", padx=(0, 8))

    sort_box = ttk.Combobox(
        sorting_frame,
        textvariable=sort_var,
        values=[
            "Default",
            "Damage: Highest first",
            "Damage: Lowest first",
            "Weight: Lightest first",
            "Weight: Heaviest first",
        ],
        state="readonly",
        width=24,
        style="Dark.TCombobox",
    )
    sort_box.pack(side="left", padx=(0, 12))

    # ==========================================
    # FEATURED WEAPONS
    # ==========================================

    featured_panel = tk.Frame(main_frame, bg=BG)
    featured_panel.pack(fill="x", pady=(0, 16))

    featured_header = tk.Frame(featured_panel, bg=BG)
    featured_header.pack(fill="x", pady=(0, 10))

    create_label(
        featured_header,
        "FEATURED WEAPONS",
        size=11,
        color=GOLD,
        bold=True,
    ).pack(side="left")

    create_label(
        featured_header,
        "TOP 3 BY DAMAGE",
        size=8,
        color=MUTED,
    ).pack(side="right")

    cards_frame = tk.Frame(featured_panel, bg=BG)
    cards_frame.pack(fill="x")

    def display_featured(items_to_display):
        """Display up to three weapons with the highest damage."""

        for widget in cards_frame.winfo_children():
            widget.destroy()

        featured_items = sorted(
            items_to_display,
            key=lambda item: item["damage"],
            reverse=True,
        )[:3]

        if not featured_items:
            create_label(
                cards_frame,
                "No weapons match the selected filters.",
                size=10,
                color=MUTED,
            ).pack(anchor="w", pady=12)

            return

        for index, item in enumerate(featured_items):
            card = tk.Frame(
                cards_frame,
                bg=CARD,
                highlightbackground=BORDER,
                highlightthickness=1,
            )

            card.grid(
                row=0,
                column=index,
                sticky="nsew",
                padx=(0 if index == 0 else 7, 0),
            )

            cards_frame.grid_columnconfigure(
                index,
                weight=1,
                uniform="weapon_cards",
            )

            content = tk.Frame(card, bg=CARD)
            content.pack(fill="both", expand=True, padx=13, pady=12)

            create_label(
                content,
                f"#{index + 1}  {item['category'].upper()}",
                size=8,
                color=GOLD,
                bold=True,
            ).pack(anchor="w")

            create_label(
                content,
                item["name"],
                size=12,
                color=TEXT,
                bold=True,
            ).pack(anchor="w", pady=(5, 10))

            create_label(
                content,
                f"DAMAGE     {item['damage']}",
                size=10,
                color=GOLD,
                bold=True,
            ).pack(anchor="w")

            create_label(
                content,
                f"WEIGHT     {item['weight']}",
                size=9,
                color=MUTED,
            ).pack(anchor="w", pady=(4, 0))

            create_label(
                content,
                f"STR {item['strength_required']}   |   "
                f"DEX {item['dexterity_required']}",
                size=9,
                color=TEXT,
            ).pack(anchor="w", pady=(7, 0))

            create_label(
                content,
                f"SCALING: {item['scaling_attribute']}",
                size=8,
                color=MUTED,
            ).pack(anchor="w", pady=(5, 0))

    # ==========================================
    # ALL WEAPONS TABLE
    # ==========================================

    table_header = tk.Frame(main_frame, bg=BG)
    table_header.pack(fill="x", pady=(0, 9))

    create_label(
        table_header,
        "ALL WEAPONS",
        size=11,
        color=GOLD,
        bold=True,
    ).pack(side="left")

    info = create_label(
        table_header,
        f"Showing {len(items)} of {len(items)} items",
        size=9,
        color=MUTED,
    )
    info.pack(side="right")

    table_panel = tk.Frame(
        main_frame,
        bg=PANEL,
        highlightbackground=BORDER,
        highlightthickness=1,
    )
    table_panel.pack(fill="both", expand=True)

    columns = (
        "name",
        "category",
        "damage",
        "weight",
        "strength",
        "dexterity",
        "scaling",
    )

    tree = ttk.Treeview(
        table_panel,
        columns=columns,
        show="headings",
        style="Dark.Treeview",
    )

    headings = {
        "name": "NAME",
        "category": "CATEGORY",
        "damage": "DAMAGE",
        "weight": "WEIGHT",
        "strength": "STR REQUIRED",
        "dexterity": "DEX REQUIRED",
        "scaling": "SCALING ATTRIBUTE",
    }

    for column, heading in headings.items():
        tree.heading(column, text=heading)

    tree.column("name", width=190, minwidth=130)
    tree.column("category", width=110, minwidth=85)
    tree.column("damage", width=90, anchor="center")
    tree.column("weight", width=90, anchor="center")
    tree.column("strength", width=105, anchor="center")
    tree.column("dexterity", width=105, anchor="center")
    tree.column("scaling", width=150, minwidth=110)

    scrollbar = ttk.Scrollbar(
        table_panel,
        orient="vertical",
        command=tree.yview,
    )

    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(8, 0),
        pady=8,
    )

    scrollbar.pack(
        side="right",
        fill="y",
        padx=(0, 8),
        pady=8,
    )

    tree.tag_configure("even", background=PANEL)
    tree.tag_configure("odd", background=ROW_ALT)

    # ==========================================
    # DISPLAY FUNCTIONS
    # ==========================================

    def display_items(items_to_display):
        """Refresh weapon cards and the complete table."""

        for row in tree.get_children():
            tree.delete(row)

        for index, item in enumerate(items_to_display):
            tree.insert(
                "",
                tk.END,
                values=(
                    item["name"],
                    item["category"],
                    item["damage"],
                    item["weight"],
                    item["strength_required"],
                    item["dexterity_required"],
                    item["scaling_attribute"],
                ),
                tags=("even" if index % 2 == 0 else "odd",),
            )

        display_featured(items_to_display)

        info.config(
            text=(
                f"Showing {len(items_to_display)} "
                f"of {len(items)} items"
            )
        )

    # ==========================================
    # FILTERING AND SORTING
    # ==========================================

    def apply_filter():
        """Apply all filters and sorting options."""

        selected_category = category_var.get()

        if selected_category == "All":
            selected_category = None

        strength_text = strength_var.get().strip()
        dexterity_text = dexterity_var.get().strip()
        weight_text = weight_var.get().strip()

        try:
            max_strength = (
                int(strength_text) if strength_text else None
            )

            max_dexterity = (
                int(dexterity_text) if dexterity_text else None
            )

            max_weight = (
                float(weight_text) if weight_text else None
            )

            if max_strength is not None and max_strength < 0:
                raise ValueError

            if max_dexterity is not None and max_dexterity < 0:
                raise ValueError

            if max_weight is not None and max_weight < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid input",
                "Strength and Dexterity must be non-negative "
                "whole numbers. Weight must be a non-negative number.",
            )
            return

        filtered_items = filter_items(
            items,
            category=selected_category,
            max_strength=max_strength,
            max_dexterity=max_dexterity,
            max_weight=max_weight,
        )

        sort_option = sort_var.get()

        if sort_option == "Damage: Highest first":
            filtered_items = sort_items_by_damage(
                filtered_items,
                descending=True,
            )

        elif sort_option == "Damage: Lowest first":
            filtered_items = sort_items_by_damage(
                filtered_items,
                descending=False,
            )

        elif sort_option == "Weight: Lightest first":
            filtered_items = sort_items_by_weight(
                filtered_items,
                ascending=True,
            )

        elif sort_option == "Weight: Heaviest first":
            filtered_items = sort_items_by_weight(
                filtered_items,
                ascending=False,
            )

        display_items(filtered_items)

    def reset_filters():
        """Reset all filters and sorting options."""

        category_var.set("All")
        strength_var.set("")
        dexterity_var.set("")
        weight_var.set("")
        sort_var.set("Default")

        display_items(items)

    # ==========================================
    # BUTTONS AND EVENTS
    # ==========================================

    create_button(
        sorting_frame,
        "APPLY FILTERS",
        apply_filter,
        primary=True,
    ).pack(side="left", padx=(0, 7))

    create_button(
        sorting_frame,
        "CLEAR FILTERS",
        reset_filters,
    ).pack(side="left")

    sort_box.bind(
        "<<ComboboxSelected>>",
        lambda event: apply_filter(),
    )

    # ==========================================
    # INITIAL DISPLAY
    # ==========================================

    display_items(items)

    root.mainloop()


if __name__ == "__main__":
    create_main_window()
