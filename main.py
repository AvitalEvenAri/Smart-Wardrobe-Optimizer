import os
from colorama import Fore, Style, init
from dotenv import load_dotenv
from models import ClothingItem
from wardrobe_manager import Wardrobe
from weather_service import WeatherService

# Setup Colorama to work on Windows and Mac
init(autoreset=True)

# Load the secret API key from the .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def display_menu():
    """Shows the main menu to the user."""
    print(Fore.CYAN + Style.BRIGHT + "\n--- My Smart Wardrobe (Engineering Edition) ---")
    print(f"{Fore.YELLOW}1.{Fore.WHITE} Add a new item")
    print(f"{Fore.YELLOW}2.{Fore.WHITE} Get an outfit suggestion (Personalized)")
    print(f"{Fore.YELLOW}3.{Fore.WHITE} Show all items")
    print(f"{Fore.YELLOW}4.{Fore.WHITE} Remove an item")
    print(f"{Fore.YELLOW}5.{Fore.WHITE} Plan a trip (Constraint-based Packing)")
    print(f"{Fore.YELLOW}6.{Fore.WHITE} Wardrobe Analytics")
    print(f"{Fore.RED}7.{Fore.WHITE} Exit")
    return input(Fore.GREEN + "Choose an option: " + Style.RESET_ALL)

def main():
    """The main part of the program that runs everything."""
    if not API_KEY:
        print(Fore.RED + "Error: API Key not found. Please check your .env file.")
        return

    # Create the wardrobe and weather service objects
    my_wardrobe = Wardrobe()
    weather_service = WeatherService(API_KEY)

    while True:
        choice = display_menu()

        if choice == '1':
            # Get details from the user for a new clothing item
            name = input("Item name: ")
            cat = input("Category (Top/Bottom): ")
            color = input("Color: ")
            try:
                weather = int(input("Weather Suitability (1-5): "))
                formal = int(input("Formal Level (1-5): "))
                my_wardrobe.add_item(ClothingItem(name, cat, color, weather, formal))
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter numbers.")

        elif choice == '2':
            # Suggest an outfit and ask if the user likes it
            city = input("Enter city: ")
            score = weather_service.get_weather_score(city)
            if score:
                try:
                    formal = int(input("Formal level (1-5): "))
                    result = my_wardrobe.suggest_outfit(score, formal)

                    if result:
                        top, bottom = result
                        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Suggested Outfit:")
                        print(f"{Fore.WHITE}Top:    {top}")
                        print(f"{Fore.WHITE}Bottom: {bottom}")

                        # Get feedback to learn what the user likes
                        feedback = input(Fore.CYAN + "\nDid you like this suggestion? (y/n): ").lower()
                        if feedback == 'y':
                            my_wardrobe.update_preference(top, True)
                            my_wardrobe.update_preference(bottom, True)
                            print(Fore.GREEN + "Awesome! I'll prioritize items like these.")
                        else:
                            my_wardrobe.update_preference(top, False)
                            my_wardrobe.update_preference(bottom, False)
                            print(Fore.YELLOW + "Understood. I'll adjust my recommendations.")
                    else:
                        print(Fore.RED + "No suitable items found in your wardrobe.")
                except ValueError:
                    print(Fore.RED + "Invalid formal level.")
            else:
                print(Fore.RED + "Could not retrieve weather data.")

        elif choice == '3':
            # Show all the clothes in the wardrobe
            print(Fore.BLUE + Style.BRIGHT + "\n--- Current Wardrobe ---")
            if not my_wardrobe.items:
                print("Your wardrobe is empty.")
            else:
                for item in my_wardrobe.items:
                    print(item)

        elif choice == '4':
            # Remove a specific item by its name
            name = input("Enter the name of the item to remove: ")
            my_wardrobe.remove_item(name)

        elif choice == '5':
            # Plan what to pack for a trip based on suitcase space
            city = input("Destination city: ")
            try:
                days = int(input("Duration (1-5 days): "))
                formal = int(input("Formality (1-5): "))
                max_vol = int(input("Suitcase Capacity: "))

                scores = weather_service.get_forecast_scores(city, days)

                if scores:
                    packed, schedule, efficiency, final_vol = my_wardrobe.plan_packing_list(scores, formal, max_vol)

                    print(Fore.BLUE + Style.BRIGHT + f"\n--- Optimized Packing List for {city.capitalize()} ---")
                    print(f"Used Capacity: {final_vol}/{max_vol}")

                    if not packed:
                        print(Fore.RED + "No items were packed. Check constraints.")
                    else:
                        for item in packed:
                            print(f"- {item}")

                        print(Fore.YELLOW + "\n--- Daily Outfit Schedule ---")
                        for entry in schedule:
                            if "full!" in entry:
                                print(Fore.RED + entry)
                            else:
                                print(entry)

                        print(Fore.GREEN + Style.BRIGHT + f"\n[Efficiency Report] Space Saved: {efficiency:.1f}%")
                        if final_vol >= max_vol:
                            print(Fore.RED + Style.BRIGHT + "Warning: Suitcase at maximum capacity!")
                        print("------------------------------------------")
            except ValueError:
                print(Fore.RED + "Invalid input parameters.")

        elif choice == '6':
            # Show interesting facts about the wardrobe
            print(Fore.CYAN + my_wardrobe.get_wardrobe_analytics())

        elif choice == '7':
            # Close the program
            print(Fore.RED + Style.BRIGHT + "Closing My Smart Wardrobe. Stay Stylish!")
            break

if __name__ == "__main__":
    main()