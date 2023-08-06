#!/opt/homebrew/bin/python3
#CHANGE FIRST LINE TO YOUR PYTHON PATH

#User input the word he tried in wordle. 
# - Capital letters indicate letter in correct position
# - Lowercase letters indicate letter in wrong position
# - Underscore indicates empty position

# Output:
# - List of words that match the user input

# Example:
# User input: _a__E
# Output: ['apple', 'angle', 'alive', 'alone', 'agile', 'ample', 'amaze', 'amuse', 'awake', 'aware', 'abate', 'abide', 'abuse']

#Imports
import argparse as ap
import os
import json
from . import words

#Class that stores a letter and position and whether it is correct or not
class Letter:
    def __init__(self, letter: str, position: int, correct: bool):
        self.letter = letter
        self.position = position
        self.correct = correct

    def __repr__(self): #Printable representation of the object
        return f"{self.letter} - {self.position} - {self.correct}"
    
#Text colour class
class TextColour:
   PURPLE = '\033[1;35;48m'
   CYAN = '\033[1;36;48m'
   BOLD = '\033[1;37;48m'
   BLUE = '\033[1;34;48m'
   GREEN = '\033[1;32;48m'
   YELLOW = '\033[1;33;48m'
   RED = '\033[1;31;48m'
   BLACK = '\033[1;30;48m'
   UNDERLINE = '\033[4;37;48m'
   END = '\033[1;37;0m'
    
#Function to print possible words
def printPossibleWords(args, possibleWords: list, output_json: bool, user_input: str, correctLetters: list, misplacedLetters: list, wrong_letters: str, sort_output: bool):
    if output_json:
        addToInput = ""
        if wrong_letters != None:
            addToInput = " -w " + wrong_letters.lower()
        wrongOutput = ""
        if wrong_letters != None:
            wrongOutput = wrong_letters.lower()

        jsonOutput = {
            "possible-words": possibleWords,
            "sorted": sort_output,
            "input": {
                "user-input": user_input + addToInput,
                "correct-letters": [{"char": letter.letter, "pos": letter.position} for letter in correctLetters],
                "misplaced-letters": [{"char": letter.letter, "pos": letter.position} for letter in misplacedLetters],
                "excluded-letters": wrongOutput
            }
        }
        print(json.dumps(jsonOutput, indent=4))
    else:
        if len(possibleWords) == 0:
            print(TextColour.RED + "No words found with this combination" + TextColour.END)
            return
        
        termColumns = os.get_terminal_size().columns - 1
        WORD_SIZE = 8

        wordChunksperColumn = termColumns // WORD_SIZE
        #print(wordChunksperColumn)

        print("Possible words: ")
        wordCount = 1
        for word in possibleWords:
            if (wordCount) % wordChunksperColumn == 0:
                print(TextColour.PURPLE + " > " + TextColour.END + word.rstrip())
            else:
                print(TextColour.PURPLE + " > " + TextColour.END + word.rstrip(), end="")
            wordCount += 1

        #if (wordCount) % wordChunksperColumn != 0:
        print() #For new line

        if args.definition:
            url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + possibleWords[0] #Get the first word
            import requests
            try:
                response = requests.get(url, timeout=2)
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(TextColour.RED + "Http Error:" + TextColour.END,errh)
                return
            except requests.exceptions.ConnectionError as errc:
                print(TextColour.RED + "Error Connecting:" + TextColour.END,errc)
                return
            except requests.exceptions.Timeout as errt:
                print(TextColour.RED + "Timeout Error:" + TextColour.END,errt)
                return
            except requests.exceptions.RequestException as err:
                print(TextColour.RED + "Oops: Something Else" + TextColour.END,err)
                return
            
            data = response.json()

            if len(data) == 0:
                print(TextColour.RED + "No definition found" + TextColour.END)
                return
            
            #Print the definition and extra info
            print(TextColour.GREEN + "Definition: " + TextColour.YELLOW + possibleWords[0] + TextColour.END)
            #Phonetic
            if "phonetic" in data[0]:
                print(TextColour.CYAN + "   Phonetic: " + TextColour.YELLOW + data[0]["phonetic"] + TextColour.END)
            #Origin
            if "origin" in data[0]:
                print(TextColour.CYAN + "   Origin: " + TextColour.YELLOW + data[0]["origin"] + TextColour.END)
            #Meanings
            if "meanings" in data[0]:
                for pos,meaning in enumerate(data[0]["meanings"]):
                    print(TextColour.CYAN + f"   ({pos+1}, {meaning['partOfSpeech']}): " + TextColour.YELLOW + meaning["definitions"][0]["definition"] + TextColour.END)
                    #Example
                    if "example" in meaning["definitions"][0]:
                        print(TextColour.CYAN + "       |-> Example: " + TextColour.GREEN + TextColour.UNDERLINE + meaning["definitions"][0]["example"] + TextColour.END)


def main():
    parser = ap.ArgumentParser(prog="wordle-helper", description="Program to help you find the Wordle of the day", epilog="Made by Pedro Juan Royo")

    #Parser arguments
    parser.add_argument("-i", "--input", help="Words you tried in wordle", type=str, required=True, nargs='*')
    parser.add_argument("-w", "--wrong", help="All wrong letters", type=str)
    parser.add_argument("-j", "--json-output", help="Output the results in json format", action="store_true")
    parser.add_argument("-s", "--sorted", help="Sort output by word usage", action="store_true")
    parser.add_argument("--definition", help="Get the definition of the first word.", action="store_true")
    parser.add_argument('--version', action='version', version='%(prog)s 0.2.0')

    args = parser.parse_args()

    #Ask for user input
    #user_input = input("Enter the word you tried in wordle: ")
    user_inputs = args.input
    wrong_letters = args.wrong
    output_json = args.json_output
    sort_output = args.sorted


    for user_input in user_inputs:
        if len(user_input) != 5:
            if not output_json:
                print(TextColour.RED + "Input must be 5 characters long" + TextColour.END)
            exit(1)

    buildString = ""
    for user_input in user_inputs:
        for letter in user_input:
            if letter.islower():
                buildString += TextColour.YELLOW + letter.upper() + TextColour.END
            elif letter.isupper():
                buildString += TextColour.GREEN + letter + TextColour.END
            elif letter == "_":
                buildString += TextColour.BLACK + TextColour.UNDERLINE + letter + TextColour.END
            else:
                if not output_json:
                    print(TextColour.RED + "Invalid character in input: " + TextColour.CYAN + letter + TextColour.END)
                exit(2)

        buildString += " "

    if not output_json:
        print("Input: " + buildString) #For new line

    if wrong_letters != None:
        if not output_json:
            #print("Letters NOT in word: " + TextColour.RED + wrong_letters.upper().split(",") + TextColour.END)
            print("Letters NOT in word: ", end="")
            for letter in wrong_letters.upper():
                print(TextColour.RED + letter + " " + TextColour.END, end="")

            print() #For new line

    #Parse the user input
    correctLetters = []
    misplacedLetters = []
    emptySpaces = []
    for user_input in user_inputs:
        for i in range(len(user_input)):
            if user_input[i].isupper():
                #Check that the letter is not already in the correct letters
                alreadyAdded = False
                for letter in correctLetters:
                    if letter.letter == user_input[i].lower() and letter.position == i:
                        alreadyAdded = True

                if not alreadyAdded:
                    correctLetters.append(Letter(user_input[i].lower(), i, True))
            elif user_input[i].islower():
                misplacedLetters.append(Letter(user_input[i], i, False))
            elif user_input[i] == "_":
                emptySpaces.append(Letter(None, i, False))

    #print(correctLetters)

    #Find unique letters in both correct and misplaced letters together
    uniqueLetters = []
    for letter in correctLetters:
        if letter.letter not in uniqueLetters:
            uniqueLetters.append(letter.letter)

    for letter in misplacedLetters:
        if letter.letter not in uniqueLetters:
            uniqueLetters.append(letter.letter)

    #print(uniqueLetters)

    #Check that letters in user input are not in the wrong_letters string
    if wrong_letters != None:
        for letter in wrong_letters.lower():
            for correctLetter in correctLetters:
                if correctLetter.letter == letter:
                    if not output_json:
                        print(TextColour.RED + "Letter in input is in wrong letters: " + TextColour.CYAN + letter.upper() + TextColour.END)
                    exit(3)

            for misplacedLetter in misplacedLetters:
                if misplacedLetter.letter == letter:
                    if not output_json:
                        print(TextColour.RED + "Letter in input is in wrong letters: " + TextColour.CYAN + letter.lower() + TextColour.END)
                    exit(3)

    #Read the wordlist file and compare each word to the user input
    # with open("words.txt", "r") as wordlist:
    #     #Eliminate words with letters in the wrong_letters string
    #     searchWords = []
    #     for line in wordlist:
    #         word = line.strip()
    #         if wrong_letters != None:
    #             for letter in wrong_letters.lower():
    #                 if letter in word:
    #                     break
    #             else:
    #                 searchWords.append(word)
    #         else:
    #             searchWords.append(word)

    searchWords = words.WORD_LIST
    #Eliminate the words with letters in the wrong_letters string
    if wrong_letters != None:
        for letter in wrong_letters.lower():
            searchWords = [word for word in searchWords if letter not in word]

    possibleWords = []
    for word in searchWords:
        #word = line.strip()
        #Check correct letters
        correctCount = 0
        for pos,letter in enumerate(word):
            for correctLetter in correctLetters:
                if correctLetter.position == pos and correctLetter.letter == letter:
                    correctCount += 1
                    break
        
        if correctCount != len(correctLetters):
            #print("Correct letters don't match")
            continue

        #Check misplaced letters
        misplacedCount = 0
        skipWord = False
        for misplacedLetter in misplacedLetters:
            for pos,letter in enumerate(word):
                if misplacedLetter.letter == letter and misplacedLetter.position != pos:
                    misplacedCount += 1
                    #break
                elif misplacedLetter.letter == letter and misplacedLetter.position == pos:
                    skipWord = True
                    break

        if misplacedCount < len(misplacedLetters) or skipWord:
            #print("misplaced letters don't match")
            continue

        #Check that all unique letters are in the word
        skipWord = False
        for letter in uniqueLetters:
            #print(word)
            if letter not in word:
                #print("Unique letters don't match")
                skipWord = True
                break

        if skipWord:
            continue

        possibleWords.append(word)

    if sort_output:
        #load the csv file with word usage in Wrds/unigram_freq.csv
        # with open("unigram_freq.csv", "r") as wordUsage:
        #     wordUsageDict = {}
        #     for line in wordUsage:
        #         word, usage = line.split(",")
        #         if len(word) == 5:
        #             wordUsageDict[word] = int(usage)
        #     #print(wordUsageDict)

        wordUsageDict = words.WORD_FREQUENCY

        #sort the possible words by usage
        for word in possibleWords:
            if word not in wordUsageDict:
                wordUsageDict[word] = 0

        possibleWords.sort(key=lambda x: wordUsageDict[x], reverse=True)
        # print(wordUsageDict[possibleWords[0]])
        # print(wordUsageDict[possibleWords[-1]])

    printPossibleWords(args, possibleWords, output_json, user_inputs, correctLetters, misplacedLetters, wrong_letters, sort_output)

if __name__ == "__main__":
    main()
