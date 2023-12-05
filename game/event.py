
# define the interface to events
from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class Zombie (Context, event.Event):
    def __init__ (self):
        super().__init__()
        self.name = "beat the zombie"
        self.zombie = 1
        self.verbs['punch'] = self
        self.verbs['swing'] = self
        self.verbs['run'] = self
        self.result = {}
        self.go = False

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "punch"):
            self.go = True
            r = random.randint(1,10)
            if (r < 5):
                self.result["message"] = "you punched the zombie."
                if (self.zombie > 1):
                    self.zombie = self.zombie - 1
            else:
                c = random.choice(config.the_player.get_pirates())
                if (c.isLucky() == True):
                    self.result["message"] = "you swung at the zombie with your sword."
                else:
                    self.result["message"] = c.get_name() + " the zombie fights back and tries to take a bite of you."
                    if (c.inflict_damage (self.zombie, "is getting scratched by the zombie")):
                        self.result["message"] = ".. " + c.get_name() + " gets eaten alive by the zombie"
        elif (verb == "swing"):
            self.zombie = self.zombie + 1
            self.result["newevents"].append (Zombie())
            self.result["message"] = "the seagulls are happy"
            self.go = True
        elif (verb == "run"):
            print ("you run back to your boat away from the zombie")
            self.go = False
        else:
            print ("it seems the only options here are to swing or run")
            self.go = False

    def process (self, world):

        self.go = False
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "default message"

        while (self.go == False):
            print (str (self.seagulls) + " There is a zombie guarding the treasure what do you do?")
            Player.get_interaction ([self])

        return self.result