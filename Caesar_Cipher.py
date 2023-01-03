"""
Caesar Cipher
Created by Braden Piper, bradenpiper.com
Created on Tue Jan 2, 2023
Version = 1.1
------------------------------------------
DESCRIPTION:
A classic Caesar Cipher that can be used to encrypt or decrypt a text message
input by the user.
------------------------------------------
NOTE: This program was completed as part of the course MITx 6.00.1x - Introduction
to Computer Science and Programming using Python. The general framework, and some
of the functions were provided materials. The majority of the implementation is
my own work.
The provided functions include:
    loadwords()
    is_word()
Several of the other function names were provided with pseudocode descriptions,
but the implementations are my own.
"""

import string
import random

# FUNCTIONS

def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    # print('Loading word list from file...')
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    # print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]
        
    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        has 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
        alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        shiftDict = {}
        
        lowerListShifted = []   # create a shifted list for lowercase letters
        for letter in alphabet_lower[shift:]:
            lowerListShifted.append(letter)
        for letter in alphabet_lower[(shift-shift):shift]:
            lowerListShifted.append(letter)
            
        upperListShifted = []  # create a shifted list for uppercase letters
        for letter in alphabet_upper[shift:]:
            upperListShifted.append(letter)
        for letter in alphabet_upper[(shift-shift):shift]:
            upperListShifted.append(letter)
        
        for letter in alphabet_lower:   # add the lowercase key-value pairs to shiftDict
            for value in lowerListShifted:
                shiftDict[letter] = value
                lowerListShifted.remove(value)
                break
        
        for letter in alphabet_upper:   # add the uppercase key-value pairs to shiftDict
            for value in upperListShifted:
                shiftDict[letter] = value
                upperListShifted.remove(value)
                break
        
        return shiftDict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        shiftDict = self.build_shift_dict(shift)
        shiftedString = ''
        
        for letter in self.message_text:
            if letter in alphabet:
                shiftedString += (shiftDict[letter])
            else:
                shiftedString += letter
        
        return shiftedString
    

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self,text)
        #self.message_text = Message.get_message_text(self)
        #self.valid_words = load_words('words.txt')

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are  equally good such that they all create 
        the maximum number of you may choose any of those shifts (and their
        corresponding decrypted messages) to return

        Returns: the "best" decrypted message
        '''
        bestWordCount = 0
        bestString = ''
        bestShift = 0
        # try every possible shift value
        for shift in range(27):
            decrypted = self.apply_shift(shift)   # decrypt
            
            decryptedSplit = decrypted.split(' ')    # split string by spaces
            validWordCount = 0   # set validWordCount var to 0
            for word in decryptedSplit:      # count valid words
                if word in self.valid_words:
                    validWordCount += 1
            if validWordCount > bestWordCount:   # compare count of valid words to best count
                bestWordCount = validWordCount   # if best count:
                bestString = decrypted           # assign bestString
                bestShift = shift                # assign bestShift
        return bestString                       # bestString
                


# FUNCTIONS
def encrypter():
    '''
    Accepts a text input from the user
    Returns an encoded version of the message
    '''
    # take a user input text and store it as a Message object called userInput
    userInput = Message(input('Please enter your message now, then press Enter: '))
    # randomly select a number between 1 and 25, and use apply_shift(Random Int)
    shiftedMessage = userInput.apply_shift(random.randint(0,25))
    return shiftedMessage

def decrypter():
    '''
    Accepts a text input from the user
    Returns a decoded version of the message
    '''
    # take a user input text and stores it as a CiphertextMessage object called userInput
    userInput = CiphertextMessage(input('Please enter your message now, then press Enter: '))
    decryptedMessage = userInput.decrypt_message()
    return decryptedMessage

def whichTask():
    '''
    Asks the user if they want to encode or decode.
    Returns an integer: 1 for encode, 2 for decode.
    '''       
    print('Do you need to encode[1] or decode[2]')
    print('Press 1 or 2. Then Enter.')
    answer = 0
    while answer != 1 or 2:    
        answer = input()
        if answer == '1':
            return 1
        elif answer == '2':
            return 2
        else:
            print('Invalid input. Please type 1 or 2. Then Enter.')


# PROGRAM
print('Welcome agent. I am Caesar Cipher, here to encode and decode your messages.')
userChoice = whichTask()
if userChoice == 1:
    encryptedMessage = encrypter()
    print('Your encrypted message is:', encryptedMessage)
elif userChoice == 2:
    decryptedMessage = decrypter()
    print('Your decrypted message is:', decryptedMessage)