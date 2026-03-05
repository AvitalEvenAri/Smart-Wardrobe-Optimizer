class ClothingItem:
    def __init__(self, name, category, color, weather, formal_level, usage_count=0, volume=None, preference_score=10):
        self.name = name
        self.category = category
        self.color = color
        self.weather = weather
        self.formal_level = formal_level
        self.usage_count = usage_count
        self.preference_score = preference_score

        # חישוב נפח אוטומטי אם לא הוזן
        if volume is not None:
            self.volume = volume
        else:
            cat_lower = self.category.lower()
            if "coat" in self.name.lower() or "heavy" in self.name.lower():
                self.volume = 4
            elif "top" in cat_lower:
                self.volume = 1
            else:
                self.volume = 2

    def __repr__(self):
        # תצוגה נקייה ומאורגנת לכל פריט
        return f"{self.category.capitalize():<8} | {self.name:<15} ({self.color:<8}) | Vol: {self.volume} | Worn: {self.usage_count:<3} | Score: {self.preference_score}"