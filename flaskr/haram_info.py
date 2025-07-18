from deep_translator import GoogleTranslator
from typing import Dict, List


class Info:
    def __init__(self):
        self.translated_info = {}
        self.info = {
            "enzymes": "If the enzyme is microbial or plant-based, it is considered halal. If it is animal-based, like rennet, it is only halal provided that the animal itself is halal and the way it was slaughtered is halal.",
            "whey": "Rennet, the enzyme used to make whey, can come from an animal which is either not halal or was not slaughtered in a halal way.",
            "lard": "Lard is a fat derived from pigs, which are haram.",
            "meat": "If the meat comes from an animal which is not halal or which was not slaughtered in a halal way, then it is considered haram to consume that meat.",
            "bacon": "Bacon is made from pork, which is haram.",
            "pepperoni": "Pepperoni is almost always made out of pork, which is haram. If it is made from beef, then it is only halal provided that the way the cow was slaughtered is halal.",
            "pork": "Pork is haram.",
            "ham": "Ham is made from pork, which is haram.",
            "chicken": "If the chicken was not slaughtered in a halal way, then it is considered haram to consume its meat.",
            "beef": "If the cow was not slaughtered in a halal way, then it is considered haram to consume its meat.",
            "lamb": "If the lamb was not slaughtered in a halal way, then it is considered haram to consume its meat.",
            "goat": "If the goat was not slaughtered in a halal way, then it is considered haram to consume its meat.",
            "gelatin": "If this protein comes from an animal which is not halal or which was not slaughtered in a halal way, then it is considered haram.",
            "rennet": "If this enzyme is derived from an animal which is either not halal or was not slaughtered in a halal way, then it is considered haram.",
            "l-cysteine": "If this amino acid is sourced from fish, microbial, or plant-based materials, it is considered halal. If it is animal-based, it is only halal provided that the animal itself is halal and the way it was slaughtered is halal.",
            "pepsin": "If this enzyme is derived from an animal which is either not halal or was not slaughtered in a halal way, then it is considered haram.",
            "alcohol": "Alcohol is haram.",
            "ethanol": "Ethanol is an intoxicant, which makes it haram.",
            "vanilla extract": "Since vanilla extract contains alcohol, it is considered haram.",
            "wine vinegar": "Wine vinegar is made by fermenting wine, which is haram.",
            "malt extract": "Due to its alcohol association and use of enzymes which might come from non-halal sources, it is mostly considered haram.",
            "monoglycerides": "If this emulsifier is derived from an animal which is either not halal or was not slaughtered in a halal way, then it is considered haram.",
            "diglycerides": "If this emulsifier is derived from an animal which is either not halal or was not slaughtered in a halal way, then it is considered haram.",
            "e471": "If the E471 (i.e., monoglyceride/diglyceride) emulsifier is derived from an animal which is either not halal or was not slaughtered in a halal way, then it is considered haram.",
            "glycerin": "If this syrupy liquid is derived from an animal which is either not halal or was not slaughtered in a halal way, then it is considered haram.",
            "glycerol": "If this syrupy liquid is derived from an animal which is either not halal or was not slaughtered in a halal way, then it is considered haram.",
            "e422": "If this syrupy liquid (i.e., glycerol) is derived from an animal which is either not halal or was not slaughtered in a halal way, then it is considered haram.",
            "shortening": "If this fat is derived from an animal which is either not halal or was not slaughtered in a halal way, then it is considered haram.",
            "magensium stearate": "If the stearic acid is derived from an animal which is either not halal or was not slaughtered in a halal way, then it is considered haram.",
            "carmine": "Carmine is a red pigment extracted from cochineal insect, which is considered impure or filthy, and therefore haram.",
            "e120": "E120 (i.e., carmine) is a red pigment extracted from cochineal insect, which is considered impure or filthy, and therefore haram.",
        }

    def get_info(self, haram_list: List[str], language: str) -> Dict[str, str]:
        for ingredient in haram_list:
            translated_key = GoogleTranslator(source="auto", target=language).translate(
                text=ingredient
            )
            translated_val = GoogleTranslator(source="auto", target=language).translate(
                text=self.info[ingredient]
            )
            self.translated_info[translated_key] = translated_val
        return self.translated_info
