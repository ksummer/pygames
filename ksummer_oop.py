# Virtual Pet Simulation
# Kaci Summerton
# CI PyGames
# 30 January 2014

class Critter(object):
    """A virtual pet"""
    def __init__(self, name, hunger = 0, boredom = 0):
        print("\nA new pet has been born!")  
        self.name = name
        print(self.name, ":  \"Hi, my name is", self.name, ".\"")
        self.hunger = hunger
        self.boredom = boredom

    def __str__(self):
        rep = "Critter object\n"
        rep += "name: " + self.name + "\n"
        rep += "hunger: " + self.hunger + "\n"
        rep += "boredom: " + self.boredom + "\n"
        return rep

    def __pass_time(self):
        self.hunger += 1
        self.boredom += 1

    @property
    def mood(self):
        count = self.hunger + self.boredom
        if count < 5:
            m = "happy"
        elif 5 <= count <= 10:
            m = "okay"
        elif 11 <= count <= 15:
            m = "unhappy"
        else:
            m = "angry"
        return m

    def talk(self):
        print("\n", self.name, ": \"Hi. I'm ", self.name, ".\"")
        print("\t\"Right now, I feel", self.mood, ".\"")
        self.__pass_time()

    def feed(self, food = 4):
        print("\n", self.name, ": \"Yummy, thank you!\"")
        self.hunger -= food
        if self.hunger < 0:
            self.hunger = 0
        self.__pass_time()

    def play(self, fun = 4):
        print("\n", self.name, ": \"Yay! This is fun!\"")
        self.boredom -= fun
        if self.boredom < 0:
            self.boredom = 0
        self.__pass_time()

    def setname(self, new_name):
        if new_name == "":
            print("Sorry, please enter a valid name.")
        else:
            self.name = new_name
            print(self.name, ": \"Hi! My name is now ", self.name, ".\"")

    def feel(self):
        print("\nRight now, I feel ", self.mood, ".")

# main

# define choice
choice = None

# define active pet count
crittercount = 0

# menu
print("--------------------")
while choice != "0":
    print \
    ("""
    Virtual Pet Simulator

    0 - Quit
    1 - Create Pet
    2 - Talk to Pet
    3 - Feed Pet
    4 - Play with Pet
    5 - Rename Pet
    """)
    print("--------------------")

    choice = input("\nChoice: ")
    print("--------------------")

    if choice == "0":
        print("\nGoodbye!")
    elif choice == "1":
        crittercount += 1
        if crittercount > 1:
            print("\nSorry! You can only play with one pet at a time.")
            again = input("\nWould you like to a create a new pet? [Y/N]: ")
            if again == "Y":
                crittercount = 0
            else:
                print()
        else:
            crit_name = input("What would you like to name your pet?: ")
            while crit_name == "":
                print("\nPlease enter a valid name.")
                crit_name = input("\nWhat would you like to name your pet?: ")
            crit = Critter(crit_name)
    elif choice == "2":
        if crittercount < 1:
            print("\nSorry! You need to create a pet first!")
        else:
            crit.talk()
    elif choice == "3":
        if crittercount < 1:
            print("\nSorry! You need to create a pet first!")
        else:
            crit.feed()
    elif choice == "4":
        if crittercount < 1:
            print("\nSorry! You need to create a pet first!")
        else:
            crit.play()
    elif choice == "5":
        if crittercount < 1:
            print("\nSorry! You need to create a pet first!")
        else:
            crit_name = input("\nWhat would you like to rename your pet?: ")
            crit.setname(crit_name)
    else:
        print("\nSorry, but ", choice, " isn't a valid choice.\nPlease try again.")
    print("--------------------")        
        

input("\n\nPress the enter key to exit.")
