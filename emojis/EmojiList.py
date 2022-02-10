emojiLetters = [
    "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER E}", 
    "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"
]

option_columns = [
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "option_e",
    "option_f",
    "option_g",
    "option_h",
    "option_i",
    "option_j",
    "option_k",
    "option_l",
    "option_m",
    "option_n",
    "option_o",
    "option_p",
    "option_q",
    "option_r",
    "option_s",
    "option_t",
    "option_u",
    "option_v",
    "option_w",
    "option_x",
    "option_y",
    "option_z"
]

defaultEmojis = [
    '👍', 
    '👎', 
    '🤷'
]

default_options = [
    "up_vote_count",
    "down_vote_count",
    "shrug_vote_count"
]


def get_col_from_emoji(emoji):
    for i in range(len(defaultEmojis)):
        if emoji == defaultEmojis[i]:
            return default_options[i]

    for i in range(len(emojiLetters)):
        if emoji == emojiLetters[i]:
            return option_columns[i]

    return None