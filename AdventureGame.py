
# Author:           Aaron Topping
# Assignment:       Project 03 - Adventure Game
# Tools             Generating some of the text word art required assistance with a free resource:
#                   https://tools.picsart.com/text/font-generator/text-art/

# Description       This is a text-based adventure game, with multiple layers deep. 
#                   Each scenario has multiple layers of depth, and multiple endings. There are good and bad endings. You only will be counted towards a "win" if you complete a "good" ending. Your adventure is up for you to decide! It will also record the number of times you win as you return to the title screen.

# Additional Notes: An attempt to add an text animation is rewarded at the end of some GOOD and BAD endings. You can view this by typing "N". Just for fun.

# 2 users Exp:      First User: My 12 year-old daughter was the first to try it. She restarted multiple paths and loved it. She commented that it seems like she kept winning, so I showed
#                   her a path where she could die, and her exact words were "So I was just lucky!" Yes, yes she was! 

#                   Second User: My wife was the second to try it. She started multiple paths and oddly, chose literally the exact same path as my daughter the first try. So I had her try
#                   again. I guess it is just more fun to attack than to retreat!


## BASE ASSIGNMENT

# imports:
import time         # for animation
import os           # for determining width of terminal for sake of animation and center spacing

# Variables
terminalWidth = os.get_terminal_size().columns  # Width of the terminal
title = """
       _____                          ___       __                 __                      
      / ___/____  ____ _________     /   | ____/ /   _____  ____  / /___  __________  _____
      \__ \/ __ \/ __ `/ ___/ _ \   / /| |/ __  / | / / _ \/ __ \/ __/ / / / ___/ _ \/ ___/
     ___/ / /_/ / /_/ / /__/  __/  / ___ / /_/ /| |/ /  __/ / / / /_/ /_/ / /  /  __/ /    
    /____/ .___/\__,_/\___/\___/  /_/  |_\__,_/ |___/\___/_/ /_/\__/\__,_/_/   \___/_/     
        /_/                                                                                
    """
centeredTitle = "\n".join(line.center(terminalWidth) for line in title.splitlines())
# This code splits the title string into lines, centers each line individually, and then joins them back together with newline characters to create the centered title output. This is necessary as due to the formatting for the terminal of multiple lines I cannot do a single .center() for just the title.

endMessage = """
      ________            ______          __
     /_  __/ /_  ___     / ____/___  ____/ /
      / / / __ \/ _ \   / __/ / __ \/ __  / 
     / / / / / /  __/  / /___/ / / / /_/ /  
    /_/ /_/ /_/\___/  /_____/_/ /_/\__,_/   
    """
centeredEndMessage = "\n".join(line.center(terminalWidth) for line in endMessage.splitlines())

# For when your ship explodes
explosion = """
     ____   ____   ____  __  __ 
    |  _ \ / __ \ / __ \|  \/  |
    | |_) | |  | | |  | | \  / |
    |  _ <| |  | | |  | | |\/| |
    | |_) | |__| | |__| | |  | |
    |____/ \____/ \____/|_|  |_|                            
    """

# Player Details
name = ''
numWins = 0
spaceship = "🚀"

# Need to check input and return True if it is valid - function can ahndle any desired strings or chars to match by just adding an array of options
def InputCorrect ( text , options ):
    result = False

     # all text should be automatically lowered on input, so no need to lower() it here
    if text in options:
        result = True

    return result

# Error handling to assist player with input
def ErrorReport ( choices ):
    # We want the options to be capitalized, so capitalize them again
    # To not morph the original array, since it can be reused, create a new table
    tableString = ''

    for i in range ( len ( choices ) ):
        tableString += choices[i].upper()
        if i < ( len ( choices ) - 1 ):
            tableString += ', '

    print(f'Please try again: {tableString}')

# I want the player to be able to return to the title screen at the end, but it should be
# after they have confirmed, so there is enough time to read the final text.
def GameEndRestart():
    
    choice = ''
    choices = ['y','n']
    # while loops serves as input protection
    while not InputCorrect( choice , choices ):
        choice = input("Return to Title Screen? ( Y / N ) ").lower()
        if not InputCorrect( choice , choices ):
            ErrorReport( choices )

    if choice == 'y':
        gameTitle()
    else:
        GameEndRestart()

    
## Spaceship chase animation - away from UFO or after the UFO
def spaceAnimation( failure , showTitle , showTitleAtEnd , showEnd , line ):
    global spaceship
    global centeredTitle
    global centeredEndMessage
    global name

    # For aesthetics Use
    clearTerminal = "\033[K\033[F" # Clears line (K) and jumps up to previous line (F)
    # Define the initial position of the spaceship
    ufo = '🛸'

    position = 0
    position2 = 0
    count = 0
    escapeLine = line or '  The UFO is ESCAPING!!!'
    heroEscape = line or f'  NOOOOO!!! {name} has the loot!'

    # Length of string so it ends animation at end of page
    extraL = len(heroEscape)
    if failure:
        extraL = len(escapeLine)

    clearedGraphic = False

    if showTitle:   
        # Clear entire terminal at start
        print("\033c", end="")
        print(centeredTitle)
    if showEnd:
        print(centeredEndMessage)

    print()

    # Only want the animation to run 10 seconds max on super wide terminals!
    while count < 10:

        # Create a string representing the current frame
        if failure:
            # Multiplying a number to the whitespace multiples the instances of that string
            if ( position2 * 2 ) >= terminalWidth:
                if not clearedGraphic:
                    print(clearTerminal)   # [K = Clear position' [F = Move cursor to previous line
                    clearedGraphic = True
                animationLine = ( " " * position ) + spaceship + escapeLine
            else:
                animationLine = ( " " * position ) + spaceship + escapeLine + ( " " * position2 )  + ufo
        else:
             if ( position2 * 2 ) >= terminalWidth:
                if not clearedGraphic:
                    print(clearTerminal)
                    clearedGraphic = True
                animationLine = ( " " * position ) + ufo + heroEscape
             else:
                animationLine = ( " " * position ) + ufo + heroEscape + ( " " * position2 ) + spaceship

        # Print the frame
        print(animationLine, end="\r")

        # Move the spaceship one position to the right
        position += 1
        position2 += 2

        # If the spaceship reaches the right edge, reset its position
        if ( position2 * 2 ) >= terminalWidth and ( extraL + position 
                                                   ) >= terminalWidth:
            position = 0
            position2 = 0
            break

        # Sleep for a short time to control the animation speed
        count += 0.1
        time.sleep(0.05)  # Adjust the sleep duration as needed
    
    # After animation is complete, go back to Title screen
    if showTitleAtEnd:
        gameTitle()
    
# Slight deviation in the title
def gameTitle():
    global numWins
    global centeredTitle

    print("\033c", end="")  # Refresh the window and clear this
    print(centeredTitle)

    print(("Author: Aaron Topping").center(terminalWidth))
    if numWins > 0:
        print((f"Total Wins: {numWins}").center(terminalWidth))
    print() # Add space padding
    
    begin = ''
    choices = ['y','n']
    # while loops serves as input protection
    while not InputCorrect( begin , choices ):
        begin = input("Would you like to begin? ( Y / N ) ").lower()
        if not InputCorrect( begin , choices ):
            ErrorReport( choices )

    if begin == "n":
        # Jumps up a line and clears line
        spaceAnimation ( True , True , True , False , None )
    else:
        print("Let's begin!")
        StartGame()

# Start the game after receiving a Y indication to continue
def StartGame():
    global name
    global spaceship

    print("You slowly open your eyes. Your mind is foggy. Where are you again? Your body feels like you have been asleep for a lifetime...\nThe room is dark, and only the glow of a small computer screen illumates. You rub your eyes and lean closer to see what it says.")

    name = input("Captain, please enter your name: ").capitalize()
    if name == '':
        name = 'Joe'
        print(f'No name selected. You will be called {name}')

    print()
    print(f"Computer Voice: \"Welcome to Alpha Centauri, Captain {name}!\"")
    print("The lights around the ship begin to turn on, as well as various computer control systems. Your memory starts to come back to you. You're on a spaceship!")

    print()
    print(f'As you awake from hyperspace sleep you remember what is going on. Traveling all the way to Alpha Centauri has been a dream of yours since you were a small child. The journey of 4.25 light years from Earth was a long one. Even with the newest hyperspace drives, the journey requires hybernation to spare resources.\nYou made it!!!\nYou are extremely excited to begin your adventure! You look out the window of your Explorer Class spaceship {spaceship} and see the binary star system for yourself. It is amazing! To observe 2 suns at the same time is quite the sight to behold! As you sit in amazement, your ship\'s censors pick up a an anomaly nearthe out rim of the solar system. How fascinating! Your adventure is already beginning!')
    print()

    choice1 = ''
    choices = [ 'y' ]
    while not InputCorrect( choice1 , choices ):
        choice1 = input('Are you ready to investigate the Outer Rim?: ( Y / N ) ').lower()
        if not InputCorrect( choice1 , choices ):
            ErrorReport( choices )
        elif choice1 == 'n':
            print('Please press \'Y\' when ready to investigate')

    print()
    if choice1 == 'y':
        OuterRim()

# CORE CHOICE #1
## Mysterious anomaly
def OuterRim():
    global spaceship

    print()
    print("Computer Voice: \"Input accepted. Setting a course for the Outer Rim.\"")
    print()
    print(f'You set your {spaceship} on autopilot and hear the engines roar on as you fly to your destination. As you arrive, the sensors on your ship start going off. It looks like space has distorted in front of you and light is bending around what you are seeing. Your sensors are struggling. You need to make a choice on what to do. Do you wish to move CLOSER, or continue scanning at a DISTANCE. However, power will need to be rerouted to the scanners to maintain a safe distance, which will temporarily lower your shields.')
    print()

    choice2 = ''
    choices = [ 'closer' , 'distance' ]
    while not InputCorrect( choice2 , choices ):
        choice2 = input("Tell the computer your choice: ( CLOSER / DISTANCE ) ").lower()
        if not InputCorrect( choice2 , choices ):
            ErrorReport( choices )
            
    if choice2 == 'closer':
        OuterRimChoice2_CLOSER()

    else:
        OuterRimChoice2_DISTANCE()
        
def OuterRimChoice2_CLOSER():
    global name

    print()
    print(f"Computer Voice: \"Input accepted. Due to the distortion, Captain {name}, you will need to manually take control of the spacecraft and move it in.\" As you override the autopilot and move closer, you feel the ship begin to shake. The anomaly appears to be some kind of a gravity distortion. While you had hoped this would make it easier for your sensors, in fact, it has produced wildly inconsistent data! What is happening in the field distortion should not be possible. The world around you seems to warp and twist, defying the laws of physics.")
    print("~~ A craft begins to emerge from the distortion ~~")
    print()
    print("Computer Voice: \"Unidentified spacecraft detected! EMERGENCY! EMERGENCY!\"")
    print()
    print("The unidentified spacecraft is slowly emerging and what appears to be a long weapon on the front of the ship appears, pointing directly at you. With no warning at all, a huge plasma weapon fires upon you. You are under attack! Shields appear to be holding! You have a choice. You must either ATTACK the enemy ship, RETREAT, or try sending them a MESSAGE.")
    print()

    choice3 = ''
    choices = [ 'attack' , 'retreat' , 'message' ]
    while not InputCorrect( choice3 , choices ):
        choice3 = input("Tell the computer your choice: ( ATTACK / RETREAT / MESSAGE ) ").lower()
        if not InputCorrect( choice3 , choices ):
            ErrorReport( choices )

    if choice3 == 'attack':
        OuterRimChoice3_ATTACK()
    elif choice3 == 'retreat':
        OuterRimChoice3_RETREAT()
    else:
        OuterRimChoice3_MESSAGE()

def OuterRimChoice2_DISTANCE():
    print()
    print("Computer Voice: \"Input accepted. Rerouting power to continue scanning at a safe distance.\"")
    print("As you maintain your distance, the sensors analyze the anomaly. They appear to show some kind of graviational distortion that seemingly defies the laws of physics. Is this some kind of wormhole?")
    print('Suddenly, an unidentified vessel begins to emerge from the gravity distortion. While surprising, since you are such a great distance away, you are not within range of any weapons, so the sense of fear of being attacked with shields down does not concern you. However, as the ship fully emerges, different than any ship you had ever seen before, it zooms right at you and opens fire. How dangerous! Your shields are down! You quickly disengage the sensors and divert all your energy back to the shields. In this dangerous situation you need to decide if you should divert all POWER to escape, if you should ATTACK, or if you should try to enter the ANOMALY?' )
    print()

    choice3 = ''
    choices = [ 'power' , 'attack' , 'anomaly' ]
    while not InputCorrect( choice3 , choices ):
        choice3 = input("Tell the computer your choice: ( POWER / ATTACK / ANOMALY ) ").lower()
        if not InputCorrect( choice3 , choices ):
            ErrorReport( choices )

    if choice3 == 'POWER':
        OuterRimChoice4_POWER()
    elif choice3 == 'attack':
        OuterRimChoice3_ATTACK()
    else:
       OuterRimChoice3_ANOMALY() 


def OuterRimChoice3_ATTACK():
    global name
    global spaceship

    print()
    print(f"Computer Voice: \"Input accepted. Captain {name}, this seems rather unwise. You do not know the capabilities of this unidentified spaceship!\"")
    print(f"You respond, \"I trust my {spaceship} and her capabilities. I am here on an adventure, and nothing is going to stop me now!\"")
    print('~~ You ship spins around and zigs and zags, dodging shot after shot from the craft. Each subsequence hit lowers your shield power. You fire your own weapons, but nothing seems to be working. You have 1 last chance. The skills of the enemy pilot seem to be eerily matched to your own. You can either RETREAT, or fire the MISSILE!')
    print()

    choice4 = ''
    choices = [ 'retreat' , 'missile' ]
    while not InputCorrect( choice4 , choices ):
        choice4 = input("Tell the computer your choice: ( RETREAT / MISSILE ) ").lower()
        if not InputCorrect( choice4 , choices ):
            ErrorReport( choices )
            
    if choice4 == "missile":
        OuterRimChoice4_MISSILE()
    else:
        OuterRimChoice3_RETREAT()
          
def OuterRimChoice3_RETREAT():
    global spaceship

    print()
    print(f"Computer Voice: \"Input accepted. Plotting a retreat course. Moving reserve energy to engines to leave as quick as possible!\"")
    print(f'As your {spaceship} disengages with the object, choosing to flee rather than fight, you quickly maneuver away from the unidentified craft attacking you through the anomaly. You push your engines to the limit, evading the hostile ship that is firing at you, narrowly avoiding a direct hit. However, something unexpected happens. Their ship matches your speed and begins to gain on you. As it gets closer and closer, you know it is only a matter of time before it catches up and destroys you. Looking to the side, you see a large asteroid field that you can possibly HIDE in. Or, you can add every last bit of POWER to your engines, pushing them beyond their limits to escape. Your engines could very well cause the ship to explode if this fails.')
    print()

    choice4 = ''
    choices = [ 'hide' , 'power' ]
    while not InputCorrect( choice4 , choices ):
        choice4 = input("Tell the computer your choice: ( HIDE / POWER ) ").lower()
        if not InputCorrect( choice4 , choices ):
            ErrorReport( choices )
            
    if choice4 == "hide":
        OuterRimChoice4_HIDE()
    else:
        OuterRimChoice4_POWER()

def OuterRimChoice3_MESSAGE():
    print()
    print('Computer Voice: \"Input accepted. Attempting to communicate with attacking vessel.\"')
    print("You shout through the comms, blanketing all frequencies, \"CEASE FIRE! CEASE FIRE! This is not a military vessel. I am on an exploratory mission!\"")
    print("No response. The enemy vessel fires at you again. Your shields are taking a beating. You try again and get no response. You wonder to yourself that maybe this vessel only thinks that you are a threat because you have your shields raised. Or, maybe the vessels' comms are being blocked by your shield? Do you take the risk and lower your SHIELD to try again, do you ATTACK, or do you now decided to RETREAT before it's too late?")
    print()

    choice4 = ''
    choices = [ 'shield' , 'attack' , 'retreat' ]
    while not InputCorrect( choice4 , choices ):
        choice4 = input("Tell the computer your choice: ( SHIELD / ATTACK / RETREAT ) ").lower()
        if not InputCorrect( choice4 , choices ):
            ErrorReport( choices )

    if choice4 == "shield":
        OuterRimChoice4_SHIELD()
    elif choice4 == "attack":
        OuterRimChoice3_ATTACK()
    else:
        OuterRimChoice3_RETREAT()

def OuterRimChoice3_ANOMALY():
    global spaceship

    print()
    print('Computer Voice: \"Input accepted. Setting a course to enter the gravity distortion. Enginges engaged!\"')
    print("As you zoom towards the distortion in space, the enemy vessel fires at you. Your skill as a pilot is unmatched in this sector and you are able to weave in and out, dodging the plasma blasts from the enemy ship's cannon. As you approach the distortion, your ship begins shake and rumble. There's no turning back. You kick on the thrusters, dodge a few more shots and you enter the distortion, not knowing where it lies.")
    print(f'As you enter, there appear to be two branches of where you can aim your {spaceship}. One to the LEFT and one to the RIGHT')
    print()

    choice4 = ''
    choices = [ 'left' , 'right' ]
    while not InputCorrect( choice4 , choices ):
        choice4 = input("Tell the computer your choice: ( LEFT / RIGHT ) ").lower()
        if not InputCorrect( choice4 , choices ):
            ErrorReport( choices )

    if choice4 == 'left':
        OuterRimChoice4_LEFT()
    else:
        OuterRimChoice4_RIGHT()

def OuterRimChoice4_LEFT():
    global explosion
    global centeredEndMessage

    print()
    print("You veer the ship down the left path. It appears you have entered some kind of gravity tunnel. The sensors are doing nothing for you. In an instant, the rumbling ends and you exit the gravity tunnel.")
    print("Sadly, you have exited the wormhole directly into a massive asteroid.")
    print()
    print(explosion)
    print("~~Your ship explodes and you die~~")
    print('You have lost')
    print()
    print(centeredEndMessage)
    GameEndRestart()

def OuterRimChoice4_RIGHT():
    global numWins

    print()
    print("You veer the ship down the right path. It appears you have entered some kind of gravity tunnel. The sensors are doing nothing for you. In an instant, the rumbling ends and you exit the gravity tunnel.")
    print("Amazing! You have somehow ended up back at Earth. You are now just beyond the moon. You have managed to escape the enemy vessel. You see the wormhole gravity distortion close behind you. What will be your adventure next? Should you enter back into hypersleep and start your adventure back to Alpha Centauri again, or should you end your adventure now and take a long-earned vacation back on Earth? The choice is yours!")
    print("You won!")
    print()

    numWins = numWins + 1
    spaceAnimation ( False , False , False , True , " You escaped me!" )
    GameEndRestart()

def OuterRimChoice4_MISSILE():
    global numWins
    global name

    print()
    print(f"Computer Voice: \"Input accepted. The Missile has been armed, ready to fire when you have a lock, Captain {name}! Shield power at 5%.\"")
    print("Your skills as a pilot finally have a moment to shine. If only those back on Earth, or on the colony planets could witness this moment! The unidentified craft spins. You juke to the side, flip upside down, and bear down behind it, finding your lock.")
    print("\"MISSILE AWAY!,\" you shout! The beeping of the locked missile increases as it homes in on its target.... closer... CLOSER... BOOOM!!! Direct hit! The ship is disabled. While not destroyed, it does not appear able to attack you further. Also, it appears that a large crate or object has broken off from the vessle. You swing your ship by the object and use your cargo arm to grab the loot. Quickly, you fly away." )
    print(f"Computer Voice: \"Congratulations Captain {name}! You have saved the ship!\"\n You are excited to discover the loot found in the mysterious crate that was dropped from the mysterious ship.\nYOU WON!")
    print()

    numWins = numWins + 1
    spaceAnimation ( False , False , False , True , None )
    GameEndRestart()

def OuterRimChoice4_HIDE():
    global numWins
    global name

    print()
    print(f"Computer Voice: \"Input accepted. Setting a course to navigate the asteroid field. Warning Captain {name}. The shields are already at lower power. Autopilot must be disengaged and all resources routed to the shields.\"")
    print("While the computer's statement alarms you, a sense calm also comes across you. You've flown the asteroid belt simulator a thousand times. You had this. No one in the galaxy was a better pilot than you at navigating tight spots like this. You hit the thrusters and make your way into the belt, weaving in and out, dodging the asteroids as they float around. You see behind you the unidentified shop follow in pursuit, but as it nears the edge of the belt it slows down.")
    print("You quickly find a large crater on the other side of an asteroid and land your ship in it, hidden by the shadows. Your turn off your engines and all power except a few minor sensors. Before you know it, the enemy ship disengages and flies away. You made it!!")
    print("After some time you turn the engines back on, navigate back out of the asteroid belt, and set a course to the nearest space station for repairs. While the ship remains a mystery, you still survived.")
    print("You won!")
    print()

    numWins = numWins + 1
    spaceAnimation ( False , False , False , True , " Aww, I can't find his ship!" )
    GameEndRestart()

def OuterRimChoice4_POWER():
    global name

    print()
    print(f"Computer Voice: \"Input accepted. Captain {name}, you must be warned, the amount of power necessary to do what you are asking could put the integrity of the ship at stake. If it does not go well, the ship may explode. Are you sure you want to CONTINUE or should we try to HIDE?\"")
    print()

    choice5 = ''
    choices = [ 'continue' , 'hide' ]
    while not InputCorrect( choice5 , choices ):
        choice5 = input("Tell the computer your choice: ( CONTINUE / HIDE ) ").lower()
        if not InputCorrect( choice5 , choices ):
            ErrorReport( choices )

    if choice5 == "continue":
        OuterRimChoice5_CONTINUE()
    else:
        OuterRimChoice4_HIDE()

def OuterRimChoice4_SHIELD():
    global numWins
    global name

    print()
    print(f'Computer Voice: \"Input accepted. Captain {name}, I don\'t like this at all, but here we go! Shields deactivated!\"')
    print('You blanket the frequencies again, shouting for a cease fire. A sound begins to break through, staticky at first, but then gaining clarity. A voice comes through, \"Who are you and why did you attack us?\"')
    print(f'Captain {name} says, \"I never attacked you. What are you talking about!?\"')
    print('Enemy Vessel says, \"3 hours ago we were attacked by a ship. We thought it was you! This is Commander Jim Holden on a secret mission for the U.N.. We must have gotten caught in a wormhole. Our ship needs repairs, but maybe you can deliver our special alien artifact in our cargo bay back to the U.N.. You would be a hero!\"')
    print("What a relief! You happily agree. After swining by their ship and collecting the cargo and say your farewells, you plot a course back to the nearest U.N. starbase. What an adventure!")
    print("You won!")
    print()

    numWins = numWins + 1
    spaceAnimation ( False , False , False , True , " Goodbye Friend!" )
    GameEndRestart()
          
def OuterRimChoice5_CONTINUE():
    global spaceship

    print()
    print('Computer Voice: \"Input accepted. Diverting all remaining power to the engines, even thought a superhuman AI recommended against it!\"')
    print(f'As the engines roar to more power than they ever experienced, the g-forces you face slam your back against your seat. Your arms are pinned to your sides unable to control the ship, unable to stop the acceleration. The ship shakes and roars, and the metal aches and groans as the forces threaten to rip it to pieces. But, as you can see, you begin to pull away from the attacking vessel. Your {spaceship} appears to be escaping...')
    print()
    print(explosion)
    print("~~Your ship explodes and you die~~")
    print('You have lost')
    print()
    print(centeredEndMessage)
    GameEndRestart()


# First Trigger
gameTitle()