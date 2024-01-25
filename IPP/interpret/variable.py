# Autor: Vojtěch Vašíček (xvasic31)
#
# Toto je třída proměnné. Ukláda jméno, hodnotu a typ proměnné a je uložena ve framu do kterého byla deklarována.

class Variable:
    def __init__(self, name, value, vartype):
        self.name = name
        self.value = value
        self.vartype = vartype
