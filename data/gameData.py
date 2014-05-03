__author__ = 'Synergy'

#Rules to be evaluated on each choice. One is added each game day.
RULES = ['The same sentence should not be used more than twice consecutively.',
         'Proletariat are not members of the party and thus to be vaporized.',
         'People over 42 are past peak and thus to be vaporized.',
         'Inner Party under 40 must be reeducated.',
         'Prominent members are public figures and are not to be imprisoned.']

#Various crimes, & suggested punishments [Definition, 1st offense, 2nd]
CRIMES = {'Oldthink': ["Holding ideas and/or patterns of thought not consistent with The Party's",
                      'Imprisonment', 
                      'Reeducation'],
          'Thoughtcrime': ['The criminal act of holding unspoken beliefs\n or doubts that oppose or question The Party',
                            'Vaporization',
                            'Vaporization'],
          'Violence': ['The behavior involving physical force intended to\n hurt, damage, or kill a fellow comrade.',
                        'Imprisonment',
                        'Reeducation'],
          'Facecrime': ['To wear an improper expression on your face,\n i.e. to grimace at a victory announcement',
                         'Imprisonment',
                         'Vaporization'],
          'Sexcrime': ['The act of sex for any reason other than procreation.',
                        'Reeducation',
                        'Vaporization']
                            
          }
                           
                           
MONEY_C = 10
SANITY_C = 10
LOYALTY_C = 5
FOOD_COST = 10
FOOD_EFFECT = 10