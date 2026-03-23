class ClothingItem:
    """
    Represents a single piece of clothing with its physical and stylistic attributes.
    This class handles automatic volume calculation based on item category.
    """
    def __init__(self, name, category, color, weather, formal_level, usage_count=0, volume=None, preference_score=10):
        self.name = name
        self.category = category
        self.color = color
        self.weather = weather
        self.formal_level = formal_level
        self.usage_count = usage_count
        self.preference_score = preference_score

        # Auto-calculate item volume if not explicitly provided during instantiation
        if volume is not None:
            self.volume = volume
        else:
            cat_lower = self.category.lower()
            # Logic: Coats and heavy items occupy more space (volume = 4)
            if "coat" in self.name.lower() or "heavy" in self.name.lower():
                self.volume = 4
            # Standard Tops occupy minimal space (volume = 1)
            elif "top" in cat_lower:
                self.volume = 1
            # Bottoms and other categories occupy moderate space (volume = 2)
            else:
                self.volume = 2

    def __repr__(self):
        """
        Provides a formatted string representation for the CLI wardrobe display.
        Uses string padding to ensure clean alignment in the terminal.
        """
        return f"{self.category.capitalize():<8} | {self.name:<15} ({self.color:<8}) | Vol: {self.volume} | Worn: {self.usage_count:<3} | Score: {self.preference_score}"