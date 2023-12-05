from game import location
import game.config as config
from game.display import announce
import random
import game.combat as combat
import game.event as event
from game.events import *
from game.player import Player
from game.context import Context
from game.items import Item
from game.display import menu

class mainIsland (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'L'
        self.visitable = True
        self.starting_location = Beach(self)
        self.locations = {}

        self.locations["Beach"] = self.starting_location
        self.locations["OakTree"] = OakTree(self)
        self.locations["PalmTreeWest"] = PalmTreeWest(self)
        self.locations["PalmTreeEast"] = PalmTreeEast(self)
        self.locations["Shack"] = Shack(self)



    def enter (self, ship):
        print ("You have arrived at a small random island.")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Beach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Beach"
        self.verbs['north'] = self
        self.verbs['south'] = self

        self.event_chance = 25
        self.events.append(Crab())

    def enter (self):
        announce ("You arrive at the beach of a peaceful island.\n" +
                  "Your ship is docked at the south beach.\n")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Shack"]


class Shack (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Shack"
        self.verbs['exit'] = self
        self.verbs['leave'] = self
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 25
        self.events.append(Crab())

    def enter (self):
        description = "Welcome to the shack! be prepared!"
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["OakTree"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["PalmTreeEast"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["PalmTreeWest"]

import random

class OakTree(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "OakTree"
        self.verbs['north'] = self
        self.oakUsed = False

    def enter(self):
        print("Welcome to Agent Oak's Tree!")
        print("Agent Oak's Spirit guards this treasure, solve his 3 riddles and you find the treasure!")

        self.event_chance = 25
        self.events.append(Crab())

        questions_asked = set()
        correct_answers = 0

        while correct_answers < 3:
            riddle = self.GetUniqueRiddleAndAnswer(questions_asked)
            guesses = 1

            while guesses > 0:
                print(riddle[0])
                plural = "" if guesses != 1 else "s"
                print(f"You may guess {guesses} more time{plural}.")
                choice = input("What is your guess? ")
                if riddle[1].lower() in choice.lower(): 
                    print("You have guessed correctly!")
                    correct_answers += 1
                    break
                else:
                    guesses -= 1
                    print("You have guessed incorrectly. Please try again.")

            if guesses <= 0:
                print(f"You've run out of guesses! The correct answer was {riddle[1]}. Restarting...")

        print("Congratulations! You've answered the three different riddles correctly and found the Gold Sword!")
        config.the_player.add_to_inventory([GoldSword()])

    def GetUniqueRiddleAndAnswer(self, questions_asked):
        riddleList = [
            ("What is black and white and red all over?", "newspaper"),
            ("What do you call a cow with no legs?", "ground beef"),
            ("What has many rings but no finger?", "phone"),
            ("What goes up but never goes down?", "age")
        ]
        available_questions = [riddle for riddle in riddleList if riddle[0] not in questions_asked]
        if not available_questions:
            questions_asked.clear()
            available_questions = riddleList

        chosen_riddle = random.choice(available_questions)
        questions_asked.add(chosen_riddle[0])
        return chosen_riddle


    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to the Shack!")
            config.the_player.next_loc = self.main_location.locations["Shack"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["PalmTreeEast"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["PalmTreeWest"]

class PalmTreeWest (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "PalmTreeWest"
        self.verbs['east'] = self

        self.event_chance = 25
        self.events.append(Crab())

    def enter (self):
        description = "You walk up to the palm tree... Oh no! its a trap! your crew lose 50hp!."
        announce(description)
        for i in config.the_player.get_pirates():
            i.inflict_damage(50, ' a trap')

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            announce ("You return to the Shack!")
            config.the_player.next_loc = self.main_location.locations["Shack"]

class PalmTreeEast (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "PalmTreeEast"
        self.verbs['west'] = self

        self.event_chance = 25
        self.events.append(Crab())

    def enter (self):
        description = "You walk up to the palm tree... Oh no! its a trap! your crew lose 50hp!."
        announce(description)
        for i in config.the_player.get_pirates():
            i.inflict_damage(50, ' a trap')


    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["Shack"]


    def HandleRiddles(self):
        riddle = self.GetRiddleAndAnswer()
        guesses = 3

        # While the player still has guesses, ask for their answer and respond appropriately.
        while guesses > 0:
            print(riddle[0])
            plural = ""
            if(guesses != 1):
                plural = "s"
            
            print(f"You may guess {guesses} more time{plural}.") 
            choice = input("What is your guess? ")
            if riddle[1] in choice:
                self.RiddleReward()
                announce("You have guessed correctly")
                return
            else:
                guesses -= 1
                announce("You have guessed incorrectly.")

        if(guesses <= 0):
            self.oakUsedUsed = True

    def GetRiddleAndAnswer(self):
        riddleList = [ # A list of tuples. The first item is the riddle, while the second item is the answer.
            ("What is black and white and red all over?", "newspaper"),
            ("What do you call a cow with no legs?", "ground beef"),
            ("what has many rings but no finger?", "phone"),
            ("what goes up but never goes down?", "age")
            ]
        return random.choice(riddleList)

    def RiddleReward(self):
        announce("You have guessed correctly. you have won the Gold!.")
        for i in config.the_player.get_pirates():
            i.lucky = True
            i.sick = False
            i.health = i.max_health
        self.oakUsed = True

class Crab (Context, event.Event):
    def __init__ (self):
        super().__init__()
        self.name = "crab visitor"
        self.crab = 1
        self.verbs['chase'] = self
        self.verbs['feed'] = self
        self.verbs['help'] = self
        self.result = {}
        self.go = False

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "chase"):
            self.go = True
            r = random.randint(1,10)
            if (r < 5):
                self.result["message"] = "the crab digs itself down."
                if (self.crab > 1):
                    self.crab = self.crab - 1
            else:
                c = random.choice(config.the_player.get_pirates())
                if (c.isLucky() == True):
                    self.result["message"] = "luckly, the crab digs itself down."
                else:
                    self.result["message"] = c.get_name() + " is attacked by the crab."
                    if (c.inflict_damage (self.crab, "pinched to death by the crab")):
                        self.result["message"] = ".. " + c.get_name() + " is pinched to death by the crab!"

        elif (verb == "feed"):
            self.crab = self.crab + 1
            self.result["newevents"].append (Crab())
            self.result["message"] = "the crabs are happy"
            self.go = True
        elif (verb == "help"):
            print ("the crabs will pester you until you feed them or chase them off")
            self.go = False
        else:
            print ("it seems the only options here are to feed or chase")
            self.go = False



    def process (self, world):

        self.go = False
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "default message"

        while (self.go == False):
            print (str (self.crab) + " crab has appeared what do you want to do?")
            Player.get_interaction ([self])

        return self.result

class GoldSword(Item):

    def __init__(self):
        super().__init__("Gold Sword", 10) 
        self.damage = (8,50) 
        self.skill = "swords"
        self.verb = "slam"
        self.verb2 = "slams"
        self.NUMBER_OF_ATTACKS = 2

    def pickTargets(self, action, attacker, allies, enemies):
        if (len(enemies) <= self.NUMBER_OF_ATTACKS): 
            return enemies
        else:
            options = []
            for t in enemies:
                options.append("attack " + t.name)
            targets = []

            while(len(targets) < self.NUMBER_OF_ATTACKS): 
                print(f"Pick target number {len(targets)}.")
                choice = menu(options)
                if(not choice in targets):
                    targets.append(enemies[choice])
            return targets
