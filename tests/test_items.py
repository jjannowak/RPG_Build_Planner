
import unittest

from main import (
    load_items,
    filter_items,
    sort_items_by_damage,
    sort_items_by_weight,
)


class TestItems(unittest.TestCase):

    def test_items_are_loaded(self):
        items = load_items()

        self.assertEqual(len(items), 40)

    def test_each_item_has_required_fields(self):
        items = load_items()

        required_fields = {
            "id",
            "name",
            "category",
            "weight",
            "strength_required",
            "dexterity_required",
            "damage",
            "scaling_attribute",
        }

        for item in items:
            with self.subTest(item=item["name"]):
                self.assertTrue(required_fields.issubset(item.keys()))

    def test_item_ids_are_unique(self):
        items = load_items()
        ids = [item["id"] for item in items]

        self.assertEqual(len(ids), len(set(ids)))

    def test_filter_by_category(self):
        items = load_items()
        swords = filter_items(items, category="Sword")

        expected = [
            item for item in items
            if item["category"].lower() == "sword"
        ]

        self.assertEqual(swords, expected)
        self.assertGreater(len(swords), 0)

    def test_filter_by_category_is_case_insensitive(self):
        items = load_items()

        swords = filter_items(items, category="sWoRd")
        expected = filter_items(items, category="Sword")

        self.assertEqual(swords, expected)

    def test_filter_by_max_strength(self):
        items = load_items()

        filtered_items = filter_items(items, max_strength=12)

        expected = [
            item for item in items
            if item["strength_required"] <= 12
        ]

        self.assertEqual(filtered_items, expected)

    def test_filter_by_max_dexterity(self):
        items = load_items()

        filtered_items = filter_items(items, max_dexterity=10)

        expected = [
            item for item in items
            if item["dexterity_required"] <= 10
        ]

        self.assertEqual(filtered_items, expected)

    def test_filter_by_strength_and_dexterity(self):
        items = load_items()

        filtered_items = filter_items(
            items,
            max_strength=12,
            max_dexterity=10,
        )

        expected = [
            item for item in items
            if item["strength_required"] <= 12
            and item["dexterity_required"] <= 10
        ]

        self.assertEqual(filtered_items, expected)

    def test_filter_by_max_weight(self):
        items = load_items()

        filtered_items = filter_items(items, max_weight=3.0)

        expected = [
            item for item in items
            if item["weight"] <= 3.0
        ]

        self.assertEqual(filtered_items, expected)

    def test_filter_returns_empty_list_for_unknown_category(self):
        items = load_items()

        result = filter_items(items, category="UnknownCategory")

        self.assertEqual(result, [])

    def test_filter_returns_all_items_without_criteria(self):
        items = load_items()

        result = filter_items(items)

        self.assertEqual(result, items)

    def test_sort_items_by_damage_descending(self):
        items = load_items()
        sorted_items = sort_items_by_damage(items)

        damages = [item["damage"] for item in sorted_items]

        self.assertEqual(damages, sorted(damages, reverse=True))

    def test_sort_items_by_weight_ascending(self):
        items = load_items()
        sorted_items = sort_items_by_weight(items)

        weights = [item["weight"] for item in sorted_items]

        self.assertEqual(weights, sorted(weights))

    def test_sort_items_by_damage_ascending(self):
        items = load_items()
        sorted_items = sort_items_by_damage(items, descending=False)

        damages = [item["damage"] for item in sorted_items]

        self.assertEqual(damages, sorted(damages))

    def test_sort_items_by_weight_descending(self):
        items = load_items()
        sorted_items = sort_items_by_weight(items, ascending=False)

        weights = [item["weight"] for item in sorted_items]

        self.assertEqual(weights, sorted(weights, reverse=True))


if __name__ == "__main__":
    unittest.main()
