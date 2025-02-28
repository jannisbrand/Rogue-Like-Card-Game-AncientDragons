
from enum import Enum


class UniquePlayerBuffs(Enum):
    Accuracy = 0
    After_Image = 1
    Amplify = 2
    Battle_Hymn = 3
    Berserk = 4
    Blasphemer = 5
    Strength = 6


class UniqueEnemyBuffs(Enum):
    Angry = 0
    Back_Attack = 1
    Beat_Of_Death = 2
    Curiosity = 3
    Curl_Up = 4
    Enrage = 5


class SharedBuffs(Enum):
    Artifact = 0
    Barricade = 1
    Buffer = 2
    Dexterity = 3
    Draw_Card = 4
    Energized = 5


class UniquePlayerDebuff(Enum):
    Bias = 0
    Constricted = 1
    Draw_Reduction = 2
    Entangled = 3
    Fasting = 4
    Hex = 5
    No_Block = 6
    Wraith_Form = 7


class UniqueEnemyBuffs(Enum):
    Block_Return = 0
    Chocked = 1
    Corpse_Explosion = 2
    Lock_On = 3


class SharedDebuffs(Enum):
    Confused = 0
    Dexterity = 1
    Dexterity_Down = 2
    Focus = 3
    Frail = 4
    No_Draw = 5
