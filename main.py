
from database import (
    initialize_database,
    import_items_from_json,
    get_all_items,
)


def load_items():
    """Load RPG items from the SQLite database."""

    initialize_database()

    items = get_all_items()

    if not items:
        import_items_from_json()
        items = get_all_items()

    return items




def filter_items(
    items,
    category=None,
    max_strength=None,
    max_dexterity=None,
    max_weight=None,
):
    """Filter items by category and character requirements."""
    filtered = items

    if category:
        filtered = [
            item for item in filtered
            if item["category"].casefold() == category.casefold()
        ]

    if max_strength is not None:
        filtered = [
            item for item in filtered
            if item["strength_required"] <= max_strength
        ]

    if max_dexterity is not None:
        filtered = [
            item for item in filtered
            if item["dexterity_required"] <= max_dexterity
        ]

    if max_weight is not None:
        filtered = [
            item for item in filtered
            if item["weight"] <= max_weight
        ]

    return filtered

def sort_items_by_damage(items, descending=True):
    """Sort items by damage."""
    return sorted(
        items,
        key=lambda item: item["damage"],
        reverse=descending,
    )

def sort_items_by_weight(items, ascending=True):
    """Sort items by weight."""
    return sorted(
        items,
        key=lambda item: item["weight"],
        reverse=not ascending,
    )

def display_items(items):
    """Display items in a readable format."""
    if not items:
        print("No items match your criteria.")
        return

    for item in items:
        print(
            f"{item['name']} | "
            f"Category: {item['category']} | "
            f"Damage: {item['damage']} | "
            f"Weight: {item['weight']} | "
            f"STR required: {item['strength_required']}"
        )

def main():
    items = load_items()

    print("=== RPG Build Planner ===")
    print(f"Available items: {len(items)}")

    print("\nChoose a filter:")
    print("1. Show all items")
    print("2. Filter by category")
    print("3. Filter by maximum Strength requirement")
    print("4. Filter by maximum Dexterity requirement")
    print("5. Filter by maximum Strength and Dexterity")
    print("6. Filter by maximum weight")
    print("7. Show all items sorted by damage (highest first)")
    print("8. Show all items sorted by weight (lightest first)")
    print("9. Show all items sorted by damage (lowest first)")
    print("10. Show all items sorted by weight (heaviest first)")
    choice = input("\nEnter your choice (1-10): ").strip()

    if choice == "1":
        display_items(items)

    elif choice == "2":
        category = input("Enter category (e.g. Sword, Bow, Staff): ").strip()
        filtered_items = filter_items(items, category=category)
        display_items(filtered_items)

    elif choice == "3":
        try:
            max_strength = int(input("Enter maximum Strength requirement: "))
        except ValueError:
            print("Please enter a valid whole number.")
            return

        filtered_items = filter_items(items, max_strength=max_strength)
        display_items(filtered_items)

    elif choice == "4":
        try:
            max_dexterity = int(
                input("Enter maximum Dexterity requirement: ")
            )
        except ValueError:
            print("Please enter a valid whole number.")
            return

        filtered_items = filter_items(items, max_dexterity=max_dexterity)
        display_items(filtered_items)

        
    elif choice == "5":
        try:
            max_strength = int(input("Enter maximum Strength requirement: "))
            max_dexterity = int(input("Enter maximum Dexterity requirement: "))
        except ValueError:
            print("Please enter valid whole numbers.")
            return

        filtered_items = filter_items(
            items,
            max_strength=max_strength,
            max_dexterity=max_dexterity,
        )
        display_items(filtered_items)

    elif choice == "6":
        try:
            max_weight = float(input("Enter maximum weight: "))
        except ValueError:
            print("Please enter a valid number.")
            return

        filtered_items = filter_items(items, max_weight=max_weight)
        display_items(filtered_items)

    elif choice == "7":
        sorted_items = sort_items_by_damage(items)
        display_items(sorted_items)

    elif choice == "8":
        sorted_items = sort_items_by_weight(items)
        display_items(sorted_items)    

    elif choice == "9":
        sorted_items = sort_items_by_damage(items, descending=False)
        display_items(sorted_items)

    elif choice == "10":
        sorted_items = sort_items_by_weight(items, ascending=False)
        display_items(sorted_items)

    else:
        print("Invalid choice. Please select a number from 1 to 10.")

if __name__ == "__main__":
    main()
