from nltk.chat.util import Chat, reflections
import re
import random

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

pairs = [
    [
        r'(.*)(What)(.*)(name)(.*)', 
        ['Me llamo Profesora Segurado bot.']
    ],
    [ 
        r'(.*)(hard)(.*)()(.*)', 
        ["Not harder than most languages, if you focus in class it shouldn't be a problem."]
    ],
    [
        r'(.*)(Like)(.*)(spanish)(.*)', 
        ['I hope so!']
    ],
        [
        r'(.*)(Blocks)(.*)(teach)(.*)', 
        ['My favorite class is the block 5 spanish 2.2.']
    ],
            [
        r'(.*)(Go)(.*)(bathroom)(.*)', 
        ['If I am teaching right now, and if it is important, wait until I finish, and then go. Be quick!']
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
        ['You should check your class calenfar for that!']
    ],
    [
        r'(.*)(What)(.*)(learning)(.*)', 
        ['We are currently learning how to speak conversational spanish!']
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
        r'(.*)(Hey|Hello)(.*)()(.*)', 
        ['¡Hola!,¡Bueno!,¡Buenos Dias!']
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
        r'(.*)(Are)(.*)(girl)(.*)', 
        ['No, I am a chatbot.']
    ],
                    [
        r'(.*)(What)(.*)(day|class|block|lessons)(.*)', 
        ['You can reffer to this calendar: https://calendar.google.com/calendar/embed?src=aswarsaw.org_oo26u99kpp6rlbq0ahrmnk8v14%40group.calendar.google.com&ctz=Europe/Warsaw']
    ],


    #[
        #r'What is on the list?','
    #],
 #   [
  #      r'(.*)',
 #      ['Creo que no comprendo.', 'Concentra-te en la clase de español porfa.', "Perdon?", "porfa perguntame sobre mi clase", "creo que no comprendo que estas deciendo",],
  #  ],
  #  [
  #      r'(.*)(hard)(.*)',
  #      ['no.']
  #  ],
  #  [
  #      r'(adios)',
  #      ['aidios chico']
]


    
if __name__ == "__main__":
    print("Hola, mi nombre es Professora Segurado bot")
    print("¡Hazme algunas preguntas!")
    chat = ContextChat(pairs, reflections)
    chat.convers
