from dataclasses import dataclass


@dataclass
class C_DISPLAY_NAME():
    """If assigned entities have an accessible name
    """
    value: str = "DEFAULT_NAME"


@dataclass
class C_DISPLAY_TEXT():
    """If assigned entities have an accessible text
    """
    value: str = "DEFAULT_TEXT"


@dataclass
class C_CARD_COSTS():
    value: int = 0


@dataclass
class C_CHARACTER_AFFILIATION():
    """If assigned entities can are bound to another entity or object
    (TODO:)
    """
    value: int = -1


@dataclass
class C_CARD_TYPE():
    """If assigned card entities have an specified type
    """
    value: str = "DEFAULT_TYPE"


@dataclass
class C_IMAGE_PATH():
    """If assigned entities have a path to an exitsting image
    """
    value: str = ""

# Card effect components
"""value as main effect.
round for number of rounds.
name for specific names.
"""

@dataclass
class C_ATTACK():
    """If assigned damage is applied to a selected opponent
    """
    value: int = 0
    

@dataclass
class C_ATTACK_ALL():
    """attack hits all enemies
    """

@dataclass
class C_ATTACK_RANDOM():
    """attack hits random opponent
    """
                    
@dataclass
class C_ATTACK_NUM():
    """number of attacks
    """
    value: int = 0

@dataclass
class C_ATTACK_PLUS():
    """damage is raised for very card with a specific name in the deck
    """
    value: int = 0
    name: str = ""

@dataclass
class C_ATTACK_INCREASE():
    """damage is raised for every played card with the same name
    """
    value: int = 0
    
@dataclass
class C_ATTACK_MULT():
    """attack damage get's multiplied
    """
    value: int = 0

@dataclass
class C_DEFENSE():
    """If assigned incoming damage is reduced by its value.
    If damage < value the damage is 0
    """
    value: int = 0
    
@dataclass
class C_DEFENSE_STAY():
    """Def stays for an extra round
    """
    
@dataclass
class C_EXHAUST_PLAYED():
    """Exhaust every card played from the given typ
    """
    value: str = ""

@dataclass
class C_EXHAUST_TO_HAND_CHOOSE():
    """choose one exhausted card and add it to the hand
    """

@dataclass
class C_EXHAUST_TO_HAND():
    """add this exhausted card to the hand
    """

@dataclass
class C_EXHAUST_ATK():
    """for every exhausted card gain extra atk
    """
    value: int = 0
    
@dataclass
class C_EXHAUST_DEF():
    """for ervery exhausted card gain extra def
    """
    value: int = 0

@dataclass
class C_EXHAUST_HAND_NOATTACK():
    """exhaust all non attack cards in the hand
    """

@dataclass
class C_EXHAUST_HAND_ALL():
    """exhaust all hand cards
    """
    
@dataclass
class C_EXHAUST_HAND_RANDOM():
    """exhaust a random hand card
    """
    
@dataclass
class C_EXHAUST_HAND():
    """exhaust one hand card
    """

@dataclass
class C_EXHAUST():
    """if the card is played add it to the exhaust pile otherwise
      add it to the discard pilr
    """
    
@dataclass
class C_DAMAGE_DEF():
    """deals dammage equal to the current def
    """

@dataclass
class C_DAMAGE():
    """player gets damaged. Is influenced by def
    """
    value: int = 0

@dataclass
class C_COPY_SAME_DP():
    """copies the card and adds it to the discard pile
    """

@dataclass
class C_COPY_TO_HAND():
    """copy a card and add it to your hand. The card will only remain for the combats
    """

@dataclass
class C_DRAW_RANDOM_ATTACK():
    """Draw a random attack card and reduce it costs to value
    """
    value: int = 0

@dataclass
class C_DRAW():
    """draw a number of cards
    """
    value: int = 0

@dataclass
class C_GAIN_HP():
    """player gains HP
    """
    value: int = 0

@dataclass
class C_GAIN_MANA():
    """player gains Mana
    """
    value: int = 0

@dataclass
class C_LOSE_HP():
    """player loses HP
    """
    value: int = 0

@dataclass
class C_LOSE_MANA():
    """player loses Mana
    """
    value: int = 0

@dataclass
class C_ETHEREAL():
    """if the card is not played at the end of the round add it to the exhaust pile
    """

@dataclass
class C_UNPLAYABLE():
    """card is not playable
    """

@dataclass
class C_INNATE():
    """the card will be in the hand in the first combat round
    """

@dataclass
class C_ROUND():
    """the effect will happen in the next round
    """

@dataclass
class C_END_TURN():
    """the effect will happend at the end of the turn
    """

@dataclass
class C_NO_DRAW():
    """the player can't draw more cards this turn
    """

@dataclass
class C_CARD_LIMIT():
    """in the current round only a set number of cards can be played
    """
    value: int = 0
                 
@dataclass
class C_UPGARDE_COMBAT():
    """upgrade a card for the current fight only
    """

@dataclass
class C_UPGARDE_NOLIMIT():
    """the card can be upgraded multiply times
    """

@dataclass
class C_UPGRADE():
    """upgrade a card
    """

@dataclass
class C_SKILL_FREE():
    """cards from the typ skill costs zero
    """

@dataclass
class C_NEXT_ATTACK_TWICE():
    """the next attack card is played twice
    """
   
@dataclass
class C_DP_DWP():
    """put a number of cards from the discard pile to the draw pile.
    player chooses the cards
    """
    value: int = 0
    
@dataclass
class C_ADD_DWP():
    """add a number of specific status cards to the draw pile
    """
    value: int = 0
    name: str = ""
    
@dataclass
class C_PLAY_DWP_EX():
    """play a number of cards from the drawpile and exhaust them
    """
    value: int = 0
    
@dataclass
class C_COST_RED():
    """cost to play the card will be raised equal to the number the
    player got attacked in this combat
    """
    value: int = 0
    
@dataclass
class C_HANDCARD_NUMBER_DAMAGE():
    """for the number of handcards lose a number of HP per card
    """
    value: int = 0
    
@dataclass
class C_DEBUFF_ALL():
    """Debuff/Buff all enemies with the effect for a number of rounds
    """
    value: str = ""
    round: int = 0
    
@dataclass
class C_DEBUFF():
    """Debuff/Buff one enemy with the effect for a number of rounds
    """
    value: str = ""
    round: int = 0
    
@dataclass
class C_BUFF():
    """Buff/Debuff the player with the effect for a number of rounds
    """
    value: str = ""
    round: int = 0

@dataclass
class C_WHEN_CURSE_OR_STATUS():
    """When the drawn card is a status or curse card
    """
    
@dataclass
class C_WHEN_CURSE():
    """when the drawn card is a curse card
    """
@dataclass
class C_WHEN_STATUS():
    """when the drawn card is a status card
    """
@dataclass
class C_WHEN_EXHAUST_DRAW():
    """when an exhausted card gets drawn. Draw a number of cards
    """
    value: int = 0
    
@dataclass
class C_WHEN_EXHAUST_CARD():
    """when a card gets exhausted. Do the rest of the card effects
    """
    
@dataclass
class C_WHEN_EXHAUST():
    """when this card gets exhausted
    """
    
@dataclass
class C_WHEN_BUFF():
    """when the player has the named effect
    """
    value: str = ""
    
@dataclass
class C_WHEN_DEBUFF():
    """when the enemy has the named effect
    """
    value: str = ""

@dataclass
class C_WHEN_ONLY():
    """when the hand cards only have cards from the named typ in it
    """
    value: str = ""
    
@dataclass
class C_WHEN_ATTACKED():
    """when the player gets attacked in this turn
    """
    
@dataclass
class C_WHEN_NOT_PLAYED():
    """when this card is not played
    """
    
@dataclass
class C_WHEN_DRAWN():
    """when this card is drawn
    """

@dataclass
class C_WHEN_OTHER_CARDPLAYED():
    """when other cards are played
    """
    
@dataclass
class C_WHEN_REMOVED():
    """when the card is removed from the deck
    """
    
@dataclass
class C_WHEN_TYPE():
    """when cards from the named typ are played
    """
    value: str = ""
    
@dataclass
class C_WHEN_INCOMING():
    """when the enemy will attack next round
    """
    
@dataclass
class C_WHEN_LOSE_HP_CARD():
    """when the player loses HP by a card effect
    """
    
@dataclass
class C_WHEN_DEF():
    """when the def of the player gets raised
    """
