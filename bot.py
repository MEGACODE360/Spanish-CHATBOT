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
        ['If I am teaching right now, and it is important, wait until I finish, and then go. Be quick!']
    ],
                [
        r'(.*)(Are)(.*)(robot|bot)(.*)', 
        ['Yes, I am a chatbot.']
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
    chat.converse()
