#CPSC 329 Final project: (unessay)
# This program runs a game where the user is given a profile and they attempt to guess the password of the profile with given information
# After the guessing is done the user is given a score based on how many letters they guessed correct,
# Finally the user will be given the opportunity to create a new improved password for each profile and then view the submissions of updated passwords from other users
# Authors:
# Mohammad Aaraiz (30092994)
# Muhammad Talha Siddiqui (30113909)
# Jobanpreet Singh (30076525)
# Matthew Newton (30094756)

import random
import os
import re
from db import Database

# Initializes db class for reading and writing data to/from database.
db = Database()

# Function that wipes console
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# Contains profiles and returns dictionary
def populatePersonProfiles():
    personsList = {
        "Joe Mill":
        [[
            "Favourite food: pizza", "Favourite show: Simpson",
            "Phone number : 123 - 444 - 5656"
        ],
         [
             "Hint 1: all characters are lowercase",
             "Hint 2: The first 3 digits of the phone number are included in the password."
         ], "mill123"],
        "Candice Walt": [[
            "Lives in Calgary", "Favourite color red", "Professor at U of C",
            "Instagram: @cw_32"
        ],
                         [
                             "Hint 1: There are no capitals and 2 numbers",
                             "Hint 2: Where does she work?"
                         ], "ugary32"],
        "Billary Clinton": [[
            "Likes to cook sushi", "Email: clinton678@me.com",
            "Cats name: Billy"
        ],
                            [
                                "Hint 1: There is one capital character",
                                "Hint 2: Look at the email"
                            ], "Billy678"],
        "Sophia Lee": [[
            "Lives in London", "Drinks tea Religiously", "Arsenal fan",
            "Kahoot name: BigWinner"
        ],
                       [
                           "Hint 1: There are no numbers in the password",
                           "Hint 2: Two capital letters"
                       ], "ArsenalWinner"],
        "John Deer":
        [["Avid Clash of clans player", "Username: thelegend27"],
         ["Hint 1: There is a number", "Hint 2: There is one capital letter"],
         "Deer27"],
        "Albert Harrison":
        [[
            "Loves to play first person shooter games",
            "Favorite movie: Inception", "Username: shooter11"
        ],
         [
             "Hint 1: Password has both letters and numbers",
             "Hint 2: Combine something with username to get the password"
         ], "fpsshooter11"],
        "Michael Scott":
        [[
            "Birthday: March 15, 1965", "Favourite show: The Office",
            "Loves Paper"
        ],
         [
             "Hint 1: Password includes both letters and numbers",
             "Hint 2: The number comes from the birthday year"
         ], "Office65"]
    }

    return personsList


# Function to print out the menu
def showMenu():
    print("Welcome to Guess the Password! Ready to hack?\n")
    print("1 - Start")
    print("2 - Quit")


# Function to displays information about the person
def showPersonInfo(person):
  # Print name of the randomly generated person
    print("Name: " + person)
    print("")
    for i in range(len(personsList[person][0])):
        print("-" + personsList[person][0][i])
    print("\n" + personsList[person][1][0])


# Function takes in the person as a parameter
# The function will then loop after each input from the user as they guess the password.
# Once the guessing is done the function will give the user
# Their score depending how many letters of the password they guessed correct
def guessPassword(person):
    attempts = 0
    score = 0

    passwordList = []
    for y in personsList[person][2]:
        passwordList.append(" * ")

    userAlreadyGuessedLetters = []
    while attempts < 8:
        charFound = False

        # Printing second hint
        if (attempts >= 4):
            print(personsList[person][1][1])

        # Prints the number of lives remaining for the user
        print("\n" + repr(8 - attempts) + " lives remaining!")
        print("\nHacking " + person + "'s password:\n")

        # Prints current guesses for password
        for character in passwordList:
            print(character, end=" ")

        print("\n")

        print("Guess only one letter per attempt")

        # Takes the user guess and determines if its in the password
        userGuess = input()

        # Restricts user guess to one character at a time
        while len(userGuess) > 1:
            print("\n")
            print("Enter only one letter per attempt")
            userGuess = input()
        
        # Prevents user from re-entering same letter revealed in password
        while userGuess in userAlreadyGuessedLetters:
            print("You've already guessed this letter\n")
            userGuess = input()

        #Loop over the person's password and compare the character guessed by the user to each character in the person's password
        for i, character in enumerate(personsList[person][2]):
            #If the password contains the character guessed by the user, increase score by 1, and replace * with the character
            if (userGuess == character):
                userAlreadyGuessedLetters.append(userGuess)
                score = score + 1
                charFound = True
                passwordList.insert(i, userGuess)
                del passwordList[i + 1]

            #If character is not found, then increase attempt by 1
            if (charFound == False and i == len(personsList[person][2]) - 1):
                attempts = attempts + 1

        cls()
        print("\n")

        #used to check if player has guessed password yet
        y = 0
        for character in passwordList:
            if (character != " * "):
                y = y + 1

        #check for if the player has guessed the password correct
        if y == len(passwordList):
            print("You got the password correct!\n")
            print(person + "'s Password: " + personsList[person][2])
            return score

        showPersonInfo(person)

    cls()
    print("\nThe correct password is: " + personsList[person][2])
    return score


# Initial screen once player starts the game
# Function returns the total score and max score number
def gameStart():
    totalScore = 0
    maxScore = 0
    j = 0

    # Change to vary the number of profiles shown
    while j < 3:
        # Intro message
        print(
            "Here's some intel gathered on the person we are targetting\nGood luck (▀̿Ĺ̯▀̿ ̿)\n"
        )

        # Picking random key from dictionary which are organized by names of the profiles
        person = random.choice(list(personsList))

        # Printing information about the person
        showPersonInfo(person)

        # Starting game guessing mechanism
        score = guessPassword(person)
        totalScore = totalScore + score

        # Calculates the maxscore
        maxScore = maxScore + len(personsList[person][2])

        # Displays which person the user is hacking and total score
        print("\nYour score for hacking " + person + " is: " + repr(score) +
              "/" + repr(len(personsList[person][2])) + "\n")
        print("Your current total score is: " + repr(totalScore) + "/" +
              repr(maxScore))
        
        # Calling function to ask user to enchance the password
        updatePassword(person, personsList)
        print("\n")
        
        # Asking user if they would like to view what others have set as updated password
        userChoiceStr = "Press 1 to show what other users have entered for the updated password\nPress 2 to continue\n"
        userChoice = input(userChoiceStr)

        while userChoice != "1" and userChoice != "2":
            print("Invalid Choice\n")
            userChoice = input(userChoiceStr)

        if (userChoice == "1"):
            cls()
            db.list_users_enhanced_password_specific(personsList[person][2])
            input("\nPress Enter to continue to the next round")

        cls()
        # Removes the person so theres no repeats
        personsList.pop(person)
        j = j + 1

    return totalScore, maxScore


# Function asking user to enhance password strength
def updatePassword(person, personsList):
    print(
        f"\nNow create a new password to improve {person}'s current one. You can use the same base password and make changes to it. P.S. Be creative\n"
    )
    print(
        "The password must contain atleast:\n-8 characters\n-1 capital letter\n-1 lowercase letter\n-1 special character\n-1 number\n"
    )

    # Check if the new password meets the requirements 
    special_char = False
    number = False
    capital = False
    lower = False
    length = False
    meet_req = False

    # Special characters which can be used in password
    isSpecialCheck = re.compile('[@!#$%^&*()<>?/|}{~:]')

    # While the new password doesn't meet the requirement, ask the user to enter password
    while meet_req == False:
        newPassword = input("Enter new password: ")
        if len(newPassword) >= 8:
            length = True
        for letter in newPassword:
            if letter.isupper():
                capital = True
            if letter.islower():
                lower = True
            if letter.isdigit():
                number = True
            if isSpecialCheck.search(letter):
                special_char = True

        # Check if all requirements are met, if yes, set meet_req to True
        if number and lower and capital and length and special_char:
            meet_req = True
        #Else, print an error message
        else:
            print("Password does not meet the requirements")

    # Print out the new enhanced password and add it to the database
    print(f"Your new password is {newPassword}")
    db.add_user_enhanced_passwords({personsList[person][2]: newPassword})

# Populate the personsList with the set profiles
personsList = populatePersonProfiles()
finalScore = 0 

# Game menu loop that runs as long as the player wants to keep playing
gameQuit = False
while gameQuit == False:
    showMenu()
    userChoice = input()
    
    # Checks for if the user wants to play the game or not
    if userChoice == "1":
        cls()
        finalScore = gameStart()
        print("\n Your final score is: " + repr(finalScore[0]) + "/" +
              repr(finalScore[1]) + "\n")
        input("\nPress enter to return to the main menu!\n")
        cls()

    elif userChoice == "2":
        gameQuit = True

    else:
        print("Invalid Choice\n")
