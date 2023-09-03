from dataclasses import dataclass

@dataclass
class UIOptions:
    windowMainSize:str="700x800"
    windowPopinSize:str= "250x150"
    colorPrimary:str="red"
    colorSecondary:str="white"
