# Heisman Trophy Data Entry

This Python program lets you type in information about Heisman Trophy winners and saves it to a specific file.

## Collection

The program starts with the two most recent Heisman winners already in the list. Then it asks you to enter up to 5 more winners. For each winner, it asks for:

- First name
- Last name
- Position
- School
- Year they won the Heisman
- Number of touchdowns that season

After you type in a winner, the program will show you what you entered and ask you to confirm.

Upon completion, the program will save everything to a file called heisman_winners.json.

## Installing requirements

You need Python 3 and rich installed.

To install, open a terminal and type:
pip install -r requirements.txt

## Running program

In the same terminal, type:
python3 cli_data_entry.py

## Output

The program creates a file called heisman_winners.json in this folder. It will include the two most recent winners, alongside any new winners that get added. 