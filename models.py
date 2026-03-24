class ClothingItem:
    """
    Represents one piece of clothing (like a shirt or pants).
    It automatically calculates how much space (volume) it takes.
    """
    def __init__(self, name, category, color, weather, formal_level, usage_count=0, volume=None, preference_score=10):
        self.name = name
        self.category = category
        self.color = color
        self.weather = weather
        self.formal_level = formal_level
        self.usage_count = usage_count
        self.preference_score = preference_score

        # Automatically decide volume if it's not given
        if volume is not None:
            self.volume = volume
        else:
            cat_lower = self.category.lower()
            # Big items like coats take more space (4 points)
            if "coat" in self.name.lower() or "heavy" in self.name.lower():
                self.volume = 4
            # Small tops take little space (1 point)
            elif "top" in cat_lower:
                self.volume = 1
            # Pants and others take medium space (2 points)
            else:
                self.volume = 2

    def __repr__(self):
        """
        How the item looks when we print it in a list.
        It uses spacing to make sure the columns are straight.
        """
        return f"{self.category.capitalize():<8} | {self.name:<15} ({self.color:<8}) | Vol: {self.volume} | Worn: {self.usage_count:<3} | Score: {self.preference_score}"