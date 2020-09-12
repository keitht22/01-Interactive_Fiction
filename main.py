#!/usr/bin/env python3
import sys,os,json,re
assert sys.version_info >= (3,8), "This script requires at least Python 3.8"

def load(l):
    f = open(os.path.join(sys.path[0], l))
    data = f.read()
    j = json.loads(data)
    return j

def find_passage(game_desc, pid):
    for p in game_desc["passages"]:
        if p["pid"] == pid:
            return p
    return {}

def format_passage(description):
    description = re.sub(r'//([^/]*)//',r'\1',description)
    description = re.sub(r"''([^']*)''",r'\1',description)
    description = re.sub(r'~~([^~]*)~~',r'\1',description)
    description = re.sub(r'\*\*([^\*]*)\*\*',r'\1',description)
    description = re.sub(r'\*([^\*]*)\*',r'\1',description)
    description = re.sub(r'\^\^([^\^]*)\^\^',r'\1',description)
    description = re.sub(r'(\[\[[^\|]*)\|([^\]]*\]\])',r'\1->\2',description)
    description = re.sub(r'\[\[([^(->)]*)->[^\]]*\]\]',r'[ \1 ]',description)
    return description


# ------------------------------------------------------

def update(current, game_desc, choice):
    if choice == "":
        return current
    for l in current["links"]:
        if choice == l["name"].lower():
            current = find_passage(game_desc, l["pid"])
            if current:
                return current
    print("\n\n---------------------\n\nI don't understand what you are asking me to do. Please try again.")
    return current

def render(current):
    print("\n\nYou are at the " + current["name"])
    print(format_passage(current["text"]))
    

def get_input(current):
    choice = input("\nWhat would you like to do? (type quit to exit)")
    choice = choice.lower()
    if choice in ["quit","q","exit"] and current["pid"] == "5":
        return "quit"
    return choice

# ------------------------------------------------------

def main():
    game_desc = load("game.json")
    current = find_passage(game_desc, game_desc["startnode"])
    choice = ""

    while choice != "quit" and current != {}:
        current = update(current, game_desc, choice)
        render(current)
        choice = get_input(current)

    print("Thanks for playing!")




if __name__ == "__main__":
    main()