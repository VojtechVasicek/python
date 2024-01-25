# Autor: Vojtěch Vašíček (xvasic31)
#
# Toto je třída FrameStack, která slouží k ukládání všech globálních listů a framů.

import frame


class FrameStack:
    def __init__(self):
        self.globalFrame = frame.Frame()
        self.tmpFrame = None
        self.localFrames = []
        self.labels = []
        self.calls = []
        self.instructions = []
        self.stack = []
        self.inputs = 0

    # Najde proměnnou s daným jménem v daném framu a přetypuje ji na zadaný typ
    # Funkce očekává proměnné scope, name a vartype.
    # scope značí rámec, ve kterém se má proměnná hledat
    # name značí jméno proměnné
    # vartype značí typ proměnné (string, int,...)
    # Funkce vrací samotnou hledanou proměnnou
    def find_retype_var(self, scope, name, vartype):
        if scope == 'GF':
            for v in self.globalFrame.variables:
                if v.name == name:
                    v.vartype = vartype
                    return v
            exit(54)
        elif scope == 'TF':
            if self.tmpFrame is not None:
                for v in self.tmpFrame.variables:
                    if v.name == name:
                        v.vartype = vartype
                        return v
                exit(54)
            else:
                exit(55)
        elif scope == 'LF':
            if self.localFrames is not None and self.localFrames:
                for v in self.localFrames[-1].variables:
                    if v.name == name:
                        v.vartype = vartype
                        return v
                exit(54)
            else:
                exit(55)

    # Najde proměnnou s daným jménem v daném framu, a zkontroluje zda očekávaný typ sedí s typem proměnné
    # Funkce očekává proměnné scope, name a vartype.
    # scope značí rámec, ve kterém se má proměnná hledat
    # name značí jméno proměnné
    # vartype značí typ proměnné (string, int,...)
    # Funkce vrací samotnou hledanou proměnnou
    def find_var(self, scope, name, vartype):
        if scope == 'GF':
            for v in self.globalFrame.variables:
                if v.name == name:
                    if v.vartype == vartype or v.vartype is None or vartype is None:
                        return v
                    else:
                        exit(53)
            exit(54)
        elif scope == 'TF':
            if self.tmpFrame is not None:
                for v in self.tmpFrame.variables:
                    if v.name == name:
                        if v.vartype == vartype or v.vartype is None or vartype is None:
                            return v
                        else:
                            exit(53)
                exit(54)
            else:
                exit(55)
        elif scope == 'LF':
            if self.localFrames is not None and self.localFrames:
                for v in self.localFrames[-1].variables:
                    if v.name == name:
                        if v.vartype == vartype or v.vartype is None or vartype is None:
                            return v
                        else:
                            exit(53)
                exit(54)
            else:
                exit(55)
