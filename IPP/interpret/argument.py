# Autor: Vojtěch Vašíček (xvasic31)
#
# Toto je třída argumentu instrukce. Ukládá typ, hodnotu a tag argumentu

class Argument:
    def __init__(self, vartype, value, tag):
        self.vartype = vartype
        self.value = value
        self.tag = tag

    # Parsování argumentů a kotrola jejich typu na základě povolených typů argumentů u jednotlivých instrukcí
    # Funkce přijímá parametr expected_type, který reprezentuje očekávaný typ argument podle operačního kódu dané instrukce
    # Funkce nic nevrací
    def parse(self, expected_type):
        if self.vartype != expected_type and expected_type != 'symb' and self.vartype != 'var':
            exit(53)
        elif self.vartype == 'var':
            val_tmp = self.value.split('@')
            if val_tmp[0] != 'GF' and val_tmp[0] != 'LF' and val_tmp[0] != 'TF':
                exit(32)
            elif len(val_tmp) != 2:
                exit(32)
            elif val_tmp[1] is None:
                exit(32)
            else:
                for char in val_tmp[1]:
                    if not char.isalnum() and char != '_' and char != '-' and char != '$' and char != '&' and char != '%' and char != '*' and char != '!' and char != '?':
                        exit(32)
                if val_tmp[1][0].isnumeric():
                    exit(32)
        elif self.vartype == 'int':
            if not self.value.isnumeric():
                if self.value[0] == '-' and self.value[1:len(self.value)].isnumeric():
                    return
                else:
                    exit(32)
        elif self.vartype == 'bool':
            if self.value != 'true' and self.value != 'false':
                exit(32)
        elif self.vartype == 'label':
            for char in self.value:
                if not char.isalnum() and char != '_' and char != '-' and char != '$' and char != '&' and char != '%' and char != '*' and char != '!' and char != '?':
                    exit(32)
            if self.value[0].isnumeric():
                exit(32)
        elif self.vartype == 'nil':
            if self.value != 'nil':
                exit(32)
        elif self.vartype == 'string':
            i = 0
            for char in self.value:
                if int(ord(char)) < 0:
                    exit(32)
                elif char == '#':
                    exit(32)
                elif char == '\\':
                    if not self.value[i+1].isnumeric() or not self.value[i+2].isnumeric() or not self.value[i+3].isnumeric():
                        exit(32)
                    if int(self.value[i+1]) == 0:
                        if int(self.value[i+2]) == 0:
                            if int(self.value[i+3]) == 0:
                                tmp = 0
                            else:
                                tmp = self.value[i+3]
                        else:
                            tmp = self.value[i+2] + self.value[i+3]
                    else:
                        tmp = self.value[i+1] + self.value[i+2] + self.value[i+3]
                    tmp2 = self.value[i] + self.value[i+1] + self.value[i+2] + self.value[i+3]
                    self.value = self.value.replace(tmp2, chr(int(tmp)))

                i += 1
        elif self.vartype == 'type':
            if self.value != 'int' and self.value != 'string' and self.value != 'bool' and self.value != 'nil':
                exit(32)
        else:
            exit(32)
        return
