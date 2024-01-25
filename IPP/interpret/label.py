# Autor: Vojtěch Vašíček (xvasic31)
#
# Toto je třída návěští, která ukláda své jméno a pozici v kódu, na kterou se má skočit.

class Label:
    def __init__(self, name, position):
        self.name = name
        self.position = position
