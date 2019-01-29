from nltk.chat.util import Chat, reflections
import re
import random
import requests
import json

# === This is the extension code for the NLTK library ===
#        === You dont have to understand it ===

class ContextChat(Chat):
    def respond(self, str):
        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)    # pick a random response

                if callable(resp):
                    resp = resp(match.groups())
                
                resp = self._wildcards(resp, match) # process wildcards

                # fix munged punctuation at the end3
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                return resp

    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos+1:pos+2])
            response = response[:pos] + \
                self._substitute(match.group(num + 1)) + \
                response[pos+2:]
            pos = response.find('%')
        return response

    def converse(self, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try: user_input = input(">")
            except EOFError:
                print(user_input)
            if user_input:
                while user_input[-1] in "!.": user_input = user_input[:-1]    
                print(self.respond(user_input))

# === Your code should go here === 

def Translate(text):
    x = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20190117T111401Z.41b0b90520ee3441.a470c2577a468ca5f0498c50445d260a1f09c7c6&text=' + text + '&lang=en-es')
    resp_dict = json.loads(x.content)
    return resp_dict["text"][0]

shopping_list = []

def add_to_list(item):
    '''
    This function adds an item to the shopping list.
    If given item is already in the list it returns
    False, otherwise it returns True
    '''

    if item in shopping_list:
        return False
    else:
        shopping_list.append(item)
        return True

pairs = [
    [
        r'(.*)(What)(.*)(your)(.*)(name)(.*)', 
        [lambda matches: 'Me llamo Profesora Segurado bot.' if add_to_list(matches[3]) else 'I already answered that']
    ],
    [ 
        r'(.*)(hard)(.*)()(.*)', 
        ["Not harder than most languages, if you focus in class it shouldn't be a problem."]
    ],
    [
        r'(.*)(Like)(.*)(spanish)(.*)', 
        ['Yes!']
    ],
        [
        r'(.*)(Blocks)(.*)(teach)(.*)', 
        ['My favorite class is the block 5 spanish 2.2.']
    ],
            [
        r'(.*)(Go)(.*)(bathroom)(.*)', 
        ['I am teaching right now, and if it is important, wait until I finish, and then go. Be quick!']
    ],
                [
        r'(.*)(Are)(.*)(robot|bot)(.*)', 
        ['Yes, I am a chatbot.']
    ],
                    [
        r'(.*)(Get)(.*)(water|drink)(.*)', 
        ['If I am teaching right now, and if it is important, wait until I finish, and then go. Be quick!']
    ],
                        [
        r'(.*)(Can)(.*)(sleep)(.*)', 
        ['No.']
    ],
                            [
        r'(.*)(Can)(.*)(eat)(.*)', 
        ['If it is not disturbing the class.']
    ],
    [
        r'(.*)(When)(.*)(test)(.*)', 
        ['You should check your class calendar for that!']
    ],
    [
        r'(.*)(What)(.*)(learning)(.*)', 
        ['Check your google classroom. Our unit should be marked over there.']
    ],
    [
        r'(.*)(How are you)(.*)', 
        ['I am doing great, how about you?']
    ],
    [
        r'(.*)(Who)(.*)(created|made)(.*)', 
        ['I was created by Antonio, Alex and David from grade 10.']
    ],
   [
        r'(.*)(What)(.*)(room)(.*)', 
        ['We are in room - - ']
    ],
       [
        r'(.*)(Hello)(.*)()(.*)', 
        ['¡Hola!,¡Bueno!']
    ],
           [
        r'(.*)(Hey)(.*)()(.*)', 
        ['¡Hola!,¡Bueno!']
    ],
               [
        r'(.*)()(.*)(school)(.*)', 
        ['Warszawska 202, 05-520 Bielawa, The school is located on Warszawska 202, 05-520 Bielawa']
    ],
                   [
        r'(.*)(Where)(.*)(classroom)(.*)', 
        ['The classroom is located in the middle near the middle school office, next to the science room.']
    ],
    [
        r'(.*)',
        ['I am afraid I dont understand.', 'Please focus on the shopping.'],
    ],
    [
        r'What is on the list?',
        [lambda matches: ','.join(shopping_list)],
    ],
    [
        r'(How do you say)( )(.*)( )(in Spanish)(.*)', 
        [lambda matches: Translate(matches[2])] 
    ],
]


    
if __name__ == "__main__":
    print("Hola, mi nombre es Professora Segurado bot")
    print("¡Hazme algunas preguntas!")
    chat = ContextChat(pairs, reflections)
    chat.converse()



myText = input("What do you want translated? ")

payload = {'key': 'YOUR SECRET KEY HERE', 'text': myText, 'lang':'en-ru'}
r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=payload)
print(r.text)
