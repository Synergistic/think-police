__author__ = 'Synergy'
from random import choice, randrange
from kivy.core.audio import SoundLoader

#Rules to be evaluated on each choice. One is added each game day.
RULES = ['The same sentence should not be used more than twice consecutively.',
         'People over 40 are past peak and thus to be vaporized.',
         'Inner Party under 35 are not to be sent to joycamp.',
         'The Outer Party population must be maintained, they cannot be vaporized.',
         'Proletariat are not members of the party and reeducation should not be wasted.']

def set_random_crimes():
    possible_crimes = ['Room 101', 'Vaporization', 'Reeducation', 'Joycamp']
    possible_crimes.append(choice(possible_crimes))
    for crime in CRIMES:
        CRIMES[crime][1] =  possible_crimes.pop(randrange(len(possible_crimes)))

#Various crimes, & suggested punishments [Definition, randomized recommended punishment]
CRIMES = {'Oldthink': ["Holding ideas and/or patterns of thought not consistent with The Party's",
                       ''],
          'Thoughtcrime': ['The criminal act of holding unspoken beliefs\n or doubts that oppose or question The Party',
                       ''],
          'Hurtcrime': ['The behavior involving physical force intended to\n hurt, damage, or kill a fellow comrade.',
                       ''],
          'Facecrime': ['To wear an improper expression on your face,\n i.e. to grimace at a victory announcement',
                       ''],
          'Sexcrime': ['The act of sex for any reason other than procreation.',
                       ''],
          }
                     
MONEY_C = 10
FOOD_COST = 10
FOOD_EFFECT = 25


room_sound = SoundLoader.load('data/audio/room.wav')
vapor_sound = SoundLoader.load('data/audio/vapor.wav')
edu_sound = SoundLoader.load('data/audio/edu.wav')
joy_sound = SoundLoader.load('data/audio/joy.wav')
ticket_sound = SoundLoader.load('data/audio/ticket.wav')