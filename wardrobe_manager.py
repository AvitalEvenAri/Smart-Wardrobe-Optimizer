import random
import json
import os

class Wardrobe:
    def __init__(self, storage_file="wardrobe_data.json"):
        """
        Initializes the wardrobe and loads saved data.
        """
        self.items = []
        self.storage_file = storage_file
        self.load_from_file()

    def add_item(self, item):
        self.items.append(item)
        self.save_to_file()
        print(f"Added {item.name} to your wardrobe.")

    def save_to_file(self):
        """Saves current items to JSON."""
        data = [vars(item) for item in self.items]
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_file(self):
        """Loads items from JSON and reconstructs objects."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    from models import ClothingItem
                    data = json.load(f)
                    self.items = [ClothingItem(**item) for item in data]
            except (json.JSONDecodeError, FileNotFoundError):
                self.items = []

    def suggest_outfit(self, weather_score, formal_level):
        tops = [i for i in self.items if i.category.capitalize() == "Top" and
                i.weather == weather_score and i.formal_level == formal_level]
        bottoms = [i for i in self.items if i.category.capitalize() == "Bottom" and
                   i.weather == weather_score and i.formal_level == formal_level]

        if not tops or not bottoms:
            return None

        # במקום רנדומלי - מיון לפי הציון הגבוה ביותר (העדפת המשתמש)
        tops.sort(key=lambda x: x.preference_score, reverse=True)
        bottoms.sort(key=lambda x: x.preference_score, reverse=True)

        chosen_top = tops[0]
        chosen_bottom = bottoms[0]

        return chosen_top, chosen_bottom

    def update_preference(self, item, liked):
        """מעדכן את הציון של הפריט לפי המשוב"""
        if liked:
            item.preference_score += 2
        else:
            item.preference_score -= 1
        self.save_to_file()
    def get_wardrobe_analytics(self):
        """
        Analyzes the wardrobe and returns insights.
        """
        if not self.items:
            return "Wardrobe is empty."

        # Sort items by usage_count
        sorted_items = sorted(self.items, key=lambda x: x.usage_count, reverse=True)
        most_worn = sorted_items[:3]

        # Find items never worn
        never_worn = [i.name for i in self.items if i.usage_count == 0]

        analytics = "\n--- Wardrobe Analytics ---"
        analytics += "\nMost worn items:\n" + "\n".join([f"- {i}" for i in most_worn])
        if never_worn:
            analytics += f"\n\nItems you might want to donate (never worn):\n- " + ", ".join(never_worn)

        return analytics

    def remove_item(self, item_name):
        """Removes an item by name and updates the file."""
        initial_count = len(self.items)
        self.items = [i for i in self.items if i.name.lower() != item_name.lower()]

        if len(self.items) < initial_count:
            self.save_to_file()
            print(f"Removed '{item_name}' from your wardrobe.")
            return True
        else:
            print(f"Item '{item_name}' not found.")
            return False

    def plan_packing_list(self, daily_weather_scores, formal_level, max_volume=10):
        """
        Optimized Packing with Volume Constraint (Knapsack-style logic).
        Prioritizes items already in the suitcase to respect volume limits.
        """
        packing_list = set()
        daily_plan = []
        current_volume = 0

        for day, score in enumerate(daily_weather_scores):
            # Filtering potential items
            tops = [i for i in self.items if i.category.capitalize() == "Top" and
                    i.weather == score and i.formal_level == formal_level]
            bottoms = [i for i in self.items if i.category.capitalize() == "Bottom" and
                       i.weather == score and i.formal_level == formal_level]

            if not tops or not bottoms:
                daily_plan.append(f"Day {day + 1}: No suitable items found")
                continue

            # Check if we can reuse what's already in the suitcase
            chosen_top = next((t for t in tops if t in packing_list), None)
            chosen_bottom = next((b for b in bottoms if b in packing_list), None)

            # If not in suitcase, try to add new items only if volume allows
            if not chosen_top:
                # Sort by smallest volume to be efficient
                tops.sort(key=lambda x: x.volume)
                if current_volume + tops[0].volume <= max_volume:
                    chosen_top = tops[0]
                    packing_list.add(chosen_top)
                    current_volume += chosen_top.volume
                else:
                    daily_plan.append(f"Day {day + 1}: Suitcase full! Couldn't pack a Top.")
                    continue

            if not chosen_bottom:
                bottoms.sort(key=lambda x: x.volume)
                if current_volume + bottoms[0].volume <= max_volume:
                    chosen_bottom = bottoms[0]
                    packing_list.add(chosen_bottom)
                    current_volume += chosen_bottom.volume
                else:
                    daily_plan.append(f"Day {day + 1}: Suitcase full! Couldn't pack a Bottom.")
                    continue

            # Update usage
            chosen_top.usage_count += 1
            chosen_bottom.usage_count += 1
            daily_plan.append(f"Day {day + 1}: {chosen_top.name} + {chosen_bottom.name}")

        self.save_to_file()
        efficiency = ((len(daily_weather_scores) * 2 - len(packing_list)) / (
                    len(daily_weather_scores) * 2)) * 100 if daily_weather_scores else 0

        return list(packing_list), daily_plan, efficiency, current_volume