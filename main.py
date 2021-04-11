import random   # For number generation
import re       # For regular expression functionality
import pandas as pd
import json
import os


def core_game(name):
 
    # Establish a list of words that can be chosen for the game
    #with open("words.txt") as f:
        #word_list = f.read().splitlines()
    #with open('words.txt','r') as word_list:
    f = open('values.json')
    data = json.load(f)
    word_list =[(v) for v in data.values()]
    word_list = [each_string.lower() for each_string in word_list]
    
    
    # Pick a random word from the list
    random_num = random.randint(0, len(word_list)-1)
    word_chosen = word_list[random_num]
    
    # Encode the word with dashess
    encoded_word = re.sub('[0-9a-zA-Z]', '-', word_chosen)
    number_of_lives=5
    score=0
  
    # Define a function for handling guesses
    def guess(letter, word, encoded):
        # Does the letter exist within the word?
        found = False
        if letter in word:
            found = True
            # Replace the dashes with the letter
            for i in range(0, len(word)):
                if word[i] == letter:
                    encoded = encoded[0:i] + letter + encoded[i+1:len(encoded)]
        return (found, encoded)
    
    
    # Initiate the game and prompt the user for their first selection
    print("\nTime to guess a letter! You have %d lives remaining." % number_of_lives)
    print(encoded_word)
    
    while(number_of_lives > 0):
        guessed_letter = input("Your guess: ")[:1]
    
        letter_found, encoded_word = guess(guessed_letter, word_chosen, encoded_word)
    
        if not letter_found:
            number_of_lives -= 1
            if number_of_lives == 0:
                print("\nGame over, you lost! :( The word or phrase was '%s'" % word_chosen)
                
                break
            else:
                print("\nWhoops! That letter was not found. You now have %d lives remaining." % number_of_lives)
                print(encoded_word)
        else:
            if "-" not in encoded_word:
                score += 10
                print("\nHooray! You won with %d lives remaining. The word or phrase was '%s'" % (number_of_lives, word_chosen))
                break
            else:
                print("\nGood job! That letter was found. You still have %d lives remaining." % number_of_lives)
                print(encoded_word)
        #play_again = input("Would you like to play again?(y/n) ")
         #if play_again == "y" or play_again == "yes":
            #core_game()
              #else:
                #Cont = False
    return name,score


#core_game()
def status_report(out):
    if len(out)>0:
        print(out)
    else:
        print('no stauts report found')
    

if __name__=='__main__':
    out=pd.DataFrame()
    

    name = input("What is your name? ")
    print("Welcome to Hangman!",name)
    while True:
        
        name,score=core_game(name)
        if len(out)==0:
            out=out.append([[name,score]])
            out.columns=['Players','Score']
        else:
            temp=out
            temp['Players']=out['Players'].str.lower()  
            if len(temp.loc[temp['Players'].isin([name.lower()])])>0:
                out.loc[temp.Players == name.lower(),'Score']=int(out.loc[temp.Players == name.lower(),'Score'])+score

            else:
                out=out.append(pd.DataFrame([[name,score]],columns=({'Players','Score'})))
            
        play_again = input("Would you like to play again?(y/n) ").lower()
        if play_again == "y" or play_again == "yes":
            play_again = input("Are you "+name+" press Y else diffenet payer press 'N' to register : ").lower()
            if play_again == "y" or play_again == "yes":
            
                print("Chance for other payer!!")
                continue
            elif play_again == "n" or play_again == "no":
                temp=out['Players'].str.lower()  
                name = input("What is your name? ")
                if len(temp.loc[temp.isin([name.lower()])])>0:
                    print("found the same player in the score card Reusing User name "+name )
                
                print("Welcome to Hangman!",name)
                continue
            else:
                break
        else:
            break
        
    status_report(out)


