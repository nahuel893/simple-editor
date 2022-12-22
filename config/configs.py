
# Global variables
CHANGE_FLAG = '•'
# color configs
main_color = '#3a3c42'
active_color = '#83868f'
second_color = '#373737'
text_color = 'white'

# style configs

settings = {
    "tnotebook": {"configure": {"background": main_color}
                    },
    "tnotebook.tab": {"configure": {"padding": [5, 1],
                                    "background": main_color,
                                    "foreground": 'white'
                                    },
                        "map": {"background": [("selected", active_color),
                                                ("active", active_color)],
                                "foreground": [("selected", 'white'),
                                                ("active", 'white')]
                                }
                        }
}
    
    
