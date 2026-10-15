
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()
console.print("Here is some initial data:", style="bold green")
output_file = Path("heisman_winners.json")

heisman = [
    {
        "first_name": "Fernando",
        "last_name": "Mendoza",
        "position": "Quarterback",
        "school": "Indiana University",
        "year": 2025,
        "touchdowns": 39
    },
    {
        "first_name": "Travis",
        "last_name": "Hunter",
        "position": "Wide Reciever / Corner Back",
        "school": "University of Colorado",
        "year": 2024,
        "touchdowns": 14
    }
]

def display_heisman_winners(heisman):
    table = Table(title="Heisman Trophy Winners")
    table.add_column("First Name", style="cyan")
    table.add_column("Last Name", style="cyan")
    table.add_column("Position", style="magenta")
    table.add_column("School", style="green")
    table.add_column("Year", style="yellow")
    table.add_column("Touchdowns", style="red")

    for winner in heisman:
        table.add_row(
            winner['first_name'],
            winner['last_name'],
            winner['position'],
            winner['school'],
            str(winner['year']),
            str(winner['touchdowns'])
        )

    console.print(table)

def collect_heisman():
    first_name = console.input("Enter the player's first name: ")
    last_name = console.input("Enter the player's last name: ")
    position = console.input("Enter the player's position: ")
    school = console.input("Enter the player's school: ")
    year = int(console.input("Enter the year they won the Heisman Trophy: "))
    touchdowns = int(console.input("Enter the number of touchdowns they scored that season: "))

    winner = {
        "first_name": first_name,
        "last_name": last_name,
        "position": position,
        "school": school,
        "year": int(year),
        "touchdowns": int(touchdowns)
    }

    return winner

def confirm_winner(winner):
    display_heisman_winners([winner])
    confirmation = console.input("Is this information correct? (y/n): ")
    return confirmation in ['y', 'Y']

console.print("Welcome to the Heisman Trophy Data Entry: ", style="bold blue")
display_heisman_winners(heisman)

for entry_number in range(5):
    console.print(f"\nEntering data for Heisman Trophy winner #{entry_number + 1}:", style="bold yellow")
    new_winner = collect_heisman()
    confirmed = confirm_winner(new_winner)

    if confirmed is False:
        console.print("Let's enter the winner again.")
        new_winner = collect_heisman()
        confirmed = confirm_winner(new_winner)

    if confirmed:
        heisman.append(new_winner)
        console.print("Movie added.")
    else:
        console.print("This movie will not be saved.")

output_file.write_text(json.dumps(heisman, indent=4), encoding="utf-8")

console.print("Your heisman winner entry has been saved.")
console.print("File saved at heisman_winners.json")
    
