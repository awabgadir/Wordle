import random
from urllib.request import urlopen
import re

class WordSelect:
  """ Class for parsing a web page with a list of 5-letter words, as well as picking a random one """
  
  def __init__(self, url):
    self.url = url
    self.fivers = []

  def get_fivers(self):
    """ Parses self.url with a regular expression to extract 5-letter words and returns a list of them """
    if self.fivers:
      return self.fivers

    page_content = urlopen(self.url).read().decode()

    self.fivers = []
    regex_matches = re.findall(r'<a href="([a-z]{5})"', page_content)
    for word in regex_matches:
      if word not in self.fivers:
        self.fivers.append(word)

    return self.fivers
  
  def random_word(self):
    """ Returns a random 5-letter word """
    return random.choice(self.get_fivers())


class Checking:
  """ Checks the guess word against the target word """
  
  def __init__(self, target):
    self.target = list(target)
    self.base = ["_", "_", "_", "_", "_"]

  def confirm(self, guess):
    """ Checks the guess against the target and returns a pattern indicating letters that are in correct positions """
    
    for i in range(5):
      if guess[i] == self.target[i]:
        self.base[i] = guess[i]
      
    return ''.join(self.base)

  def hinting(self, guess):
    """ Checks guess against the target and returns letters that are present but are in wrong positions """
    
    elements = []
      
    for element in guess:
      if element not in self.base:
        if element in self.target:
          elements.append(element)

    return elements


word_select = WordSelect('https://www.thefreedictionary.com/5-letter-words.htm')

while True:

    target_word = word_select.random_word()
    checking = Checking(target_word)

    print("You have 5 tries to guess a 5 letter word. ", end='')
    try_num = 5
    while try_num >= 1:
        word_guess = str(input()).lower()
        
        if re.search('^[a-z]{5}$', word_guess):

            if target_word == word_guess:
                print('You got it!')
                break

            elif try_num != 1:
                print(checking.confirm(word_guess))
                
                for element in checking.hinting(word_guess):
                  print("There is an", element, "in this word!")

            try_num -= 1
            
            if try_num > 0:
                print(try_num, 'tries left: ', end='')

        
        else:
          print("Please guess 5 letters.")

    if target_word != word_guess:
        print('Nope! You lost. The word was', target_word)
        print('Do you want to play again? (Y/N): ', end='')
      

        if input().upper() == 'N':
            break
    else:
        break