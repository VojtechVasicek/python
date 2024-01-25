# Autor: Vojtěch Vašíček (xvasic31)
#
# Toto je třída instrukce, která ukládá opcode, order a argumenty jednotlivých instrukcí

import sys
import label
import frame
import variable
import argument


class Instruction:
    def __init__(self, opcode, order, arguments):
        self.opcode = opcode.upper()
        self.order = order
        self.arguments = arguments

    # Kontrola počtu argumentů
    # Funkce očekává parametr expected_number, která značí očekávaný počet argumentů
    # Vrácená 0 znamená že počet argumentů odpovídá jeho očekávanému počtu
    # Vrácená 1 znamená že počet neodpovídá
    def count_check(self, expected_number):
        if expected_number == len(self.arguments):
            return 0
        else:
            return 1

    # Kontrola validity argumentů
    # Funkce očekává parametr expected_types, který značí očekávané typy argumentů, seřazené podle očekávaného pořadí argumentů
    # Funkce nic nevrací
    def argument_parse(self, expected_types):
        if len(expected_types) != len(self.arguments):
            exit(32)
        else:
            i = 0
            for argument in self.arguments:
                argument.parse(expected_types[i])
                i += 1
        return

    # Vrací pomozici skoku
    # Funkce očekává parametr stack, který se využívá pro řetězec labels, aby se v něm mohla nají pozice skoku
    # Funkce vrací pozici skoku
    def jump(self, stack):
        for l in stack.labels:
            if l.name == self.arguments[0].value:
                return l.position
        exit(52)

    # Interpretace instrukcí
    # Funkce očekává parametry stack, inp a j
    # stack reprezentuje objekt třídy FrameStack
    # inp reprezentuje input získaný buď z stdinu nebo pomocí parametru --input
    # j reprezentuje pozici v kódu
    # Funkce vrací j, tedy pozici v kódu, důležité pro skoky
    def interpret(self, stack, inp, j):
        if self.opcode == 'CREATEFRAME':
            stack.tmpFrame = frame.Frame()
        elif self.opcode == 'PUSHFRAME':
            if stack.tmpFrame is None:
                exit(55)
            else:
                for var in stack.tmpFrame.variables:
                    var.name = 'LF' + '@' + var.name.split('@')[1]
                stack.localFrames.append(stack.tmpFrame)
                stack.tmpFrame = None
        elif self.opcode == 'POPFRAME':
            if not stack.localFrames:
                exit(55)
            else:
                stack.tmpFrame = stack.localFrames.pop()
                for var in stack.tmpFrame.variables:
                    var.name = 'TF' + '@' + var.name.split('@')[1]
        elif self.opcode == 'RETURN':
            if stack.calls:
                return stack.calls.pop()
            else:
                exit(56)
        elif self.opcode == 'BREAK':
            i = j+1
            print('Pozice v kódu: {}'.format(j), file=sys.stderr)
            print('Obsah zásobníku lokálních rámců: ', file=sys.stderr, end='')
            print(stack.localFrames, file=sys.stderr)
            print('Obsah globálního rámce: ', file=sys.stderr, end='')
            print(stack.globalFrame.variables, file=sys.stderr)
            if stack.tmpFrame is not None:
                print('Obsah dočasného rámce: ', file=sys.stderr, end='')
                print(stack.tmpFrame.variables)
            print('Počet vykonaných instrukcí včetně této: {}'.format(i), file=sys.stderr)
        elif self.opcode == 'DEFVAR':
            var = self.arguments[0].value.split('@')
            if var[0] == 'GF':
                for v in stack.globalFrame.variables:
                    if v.name == self.arguments[0].value:
                        exit(52)
                stack.globalFrame.variables.append(variable.Variable(self.arguments[0].value, None, None))
            elif var[0] == 'TF':
                if stack.tmpFrame is not None:
                    for v in stack.tmpFrame.variables:
                        if v.name == self.arguments[0].value:
                            exit(52)
                    stack.tmpFrame.variables.append(variable.Variable(self.arguments[0].value, None, None))
                else:
                    exit(55)
            elif var[0] == 'LF':
                if stack.localFrames is not None and stack.localFrames:
                    for v in stack.localFrames[-1].variables:
                        if v.name == self.arguments[0].value:
                            exit(52)
                    stack.localFrames[-1].variables.append(variable.Variable(self.arguments[0].value, None, None))
                else:
                    exit(55)
        elif self.opcode == 'POPS':
            if len(stack.stack) > 0:
                arg = stack.stack.pop()
                v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, arg.vartype)
                v.value = arg.value
                v.vartype = arg.vartype
            else:
                exit(56)
        elif self.opcode == 'CALL':
            stack.calls.append(j)
            for l in stack.labels:
                if l.name == self.arguments[0].value:
                    return l.position
            exit(52)
        elif self.opcode == 'JUMP':
            return self.jump(stack)
        elif self.opcode == 'PUSHS':
            if self.arguments[0].vartype == 'var':
                v = stack.find_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, None)
                stack.stack.append(argument.Argument(v.vartype, v.value, 1))
            else:
                stack.stack.append(self.arguments[0])
        elif self.opcode == 'WRITE':
            if self.arguments[0].vartype == 'var':
                v = stack.find_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, None)
                print(v.value, end='')
            elif self.arguments[0].vartype == 'nil':
                print('', end='')
            else:
                print(self.arguments[0].value, end='')
        elif self.opcode == 'DPRINT':
            if self.arguments[0].vartype == 'var':
                v = stack.find_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, None)
                print(v.value, file=sys.stderr)
            else:
                print(self.arguments[0].value, file=sys.stderr)
        elif self.opcode == 'EXIT':
            if self.arguments[0].vartype == 'var':
                v = stack.find_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'int')
            else:
                v = self.arguments[0]
            if 49 >= int(v.value) >= 0:
                exit(int(v.value))
            else:
                exit(57)
        elif self.opcode == 'MOVE':
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, None)
            else:
                w = self.arguments[1]
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, w.vartype)
            v.value = w.value
            v.vartype = w.vartype
        elif self.opcode == 'TYPE':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'string')
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, None)
            else:
                w = self.arguments[1]
            if w.vartype is None:
                v.value = ''
            else:
                v.value = w.vartype
        elif self.opcode == 'STRLEN':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'int')
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'string')
            else:
                w = self.arguments[1]
            v.value = len(w.value)
        elif self.opcode == 'INT2CHAR':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'string')
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'int')
            else:
                w = self.arguments[1]
            char = chr(int(w.value))
            if char == ValueError:
                exit(58)
            else:
                v.value = char
        elif self.opcode == 'READ':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, self.arguments[1].value)
            arg1 = self.arguments[1].value
            if self.arguments[1].vartype == 'var':
                x = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'type')
                arg1 = x.value
            if not inp:
                v.value = 'nil'
                v.vartype = 'nil'
            if arg1 == 'int':
                v.value = inp[stack.inputs]
                v.vartype = 'int'
            elif arg1 == 'string':
                v.value = inp[stack.inputs]
                v.vartype = 'string'
            elif arg1 == 'bool':
                if inp[stack.inputs].lower() == 'true':
                    v.value = 'true'
                else:
                    v.value = 'false'
                v.vartype = 'bool'
            stack.inputs += 1
        elif self.opcode == 'ADD':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'int')
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'int')
            else:
                w = self.arguments[1]
            if self.arguments[2].vartype == 'var':
                vv = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, 'int')
            else:
                vv = self.arguments[2]
            v.value = int(w.value) + int(vv.value)
        elif self.opcode == 'SUB':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'int')
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'int')
            else:
                w = self.arguments[1]
            if self.arguments[2].vartype == 'var':
                vv = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, 'int')
            else:
                vv = self.arguments[2]
            v.value = int(w.value) - int(vv.value)
        elif self.opcode == 'MUL':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'int')
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'int')
            else:
                w = self.arguments[1]
            if self.arguments[2].vartype == 'var':
                vv = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, 'int')
            else:
                vv = self.arguments[2]
            v.value = int(w.value) * int(vv.value)
        elif self.opcode == 'IDIV':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'int')
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'int')
            else:
                w = self.arguments[1]
            if self.arguments[2].vartype == 'var':
                vv = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, 'int')
            else:
                vv = self.arguments[2]
            if int(vv.value) == 0:
                exit(57)
            v.value = int(w.value) / int(vv.value)
        elif self.opcode == 'AND':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'bool')
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'bool')
            else:
                w = self.arguments[1]
            if self.arguments[2].vartype == 'var':
                vv = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, 'bool')
            else:
                vv = self.arguments[2]
            v.value = bool(bool(w.value) and bool(vv.value))
        elif self.opcode == 'OR':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'bool')
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'bool')
            else:
                w = self.arguments[1]
            if self.arguments[2].vartype == 'var':
                vv = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, 'bool')
            else:
                vv = self.arguments[2]
            v.value = bool(bool(w.value) or bool(vv.value))
        elif self.opcode == 'NOT':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'bool')
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'bool')
            else:
                w = self.arguments[1]
            v.value = not bool(w.value)
        elif self.opcode == 'STRI2INT':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'int')
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'string')
            else:
                w = self.arguments[1]
            if self.arguments[2].vartype == 'var':
                vv = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, 'int')
            else:
                vv = self.arguments[2]
            if len(self.arguments[1].value) < int(self.arguments[2].value):
                v.value = ord(w.value[int(vv.value)])
        elif self.opcode == 'CONCAT':
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'string')
            else:
                w = self.arguments[1]
            if self.arguments[2].vartype == 'var':
                vv = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, 'string')
            else:
                vv = self.arguments[2]
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'string')
            v.value = w.value + vv.value
        elif self.opcode == 'GETCHAR':
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'string')
            else:
                w = self.arguments[1]
            if self.arguments[2].vartype == 'var':
                vv = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, 'int')
            else:
                vv = self.arguments[2]
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'string')
            if len(w.value) < int(vv.value):
                v.value = w.value[int(vv.value)]
            else:
                exit(58)
        elif self.opcode == 'SETCHAR':
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'int')
            else:
                w = self.arguments[1]
            if self.arguments[2].vartype == 'var':
                vv = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, 'string')
            else:
                vv = self.arguments[2]
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'string')
            if v.vartype == 'string' and len(v.value) < int(w.value) and vv.value is not None:
                v.value[int(w.value)] = vv.value[0]
            else:
                exit(58)
        elif self.opcode == 'LT':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'bool')
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, None)
            else:
                w = self.arguments[1]
            if self.arguments[2].vartype == 'var':
                vv = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, None)
            else:
                vv = self.arguments[2]
            if w.vartype == 'nil' or vv.vartype == 'nil':
                exit(53)
            elif w.vartype == vv.vartype:
                if w.vartype == 'int':
                    if int(w.value) < int(vv.value):
                        v.value = 'true'
                    else:
                        v.value = 'false'
                elif w.vartype == 'bool':
                    if w.value == 'false' and vv.value == 'true':
                        v.value = 'true'
                    else:
                        v.value = 'false'
                elif w.vartype == 'string':
                    if w.value < vv.value:
                        v.value = 'true'
                    else:
                        v.value = 'false'
            else:
                exit(53)
        elif self.opcode == 'GT':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'bool')
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, None)
            else:
                w = self.arguments[1]
            if self.arguments[2].vartype == 'var':
                vv = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, None)
            else:
                vv = self.arguments[2]
            if w.vartype == 'nil' or vv.vartype == 'nil':
                exit(53)
            elif w.vartype == vv.vartype:
                if w.vartype == 'int':
                    if int(w.value) > int(vv.value):
                        v.value = 'true'
                    else:
                        v.value = 'false'
                elif w.vartype == 'bool':
                    if w.value == 'true' and vv.value == 'false':
                        v.value = 'true'
                    else:
                        v.value = 'false'
                elif w.vartype == 'string':
                    if w.value > vv.value:
                        v.value = 'true'
                    else:
                        v.value = 'false'
                else:
                    exit(53)
        elif self.opcode == 'EQ':
            v = stack.find_retype_var(self.arguments[0].value.split('@')[0], self.arguments[0].value, 'bool')
            if self.arguments[1].vartype == 'var':
                w = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, None)
            else:
                w = self.arguments[1]
            if self.arguments[2].vartype == 'var':
                vv = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, None)
            else:
                vv = self.arguments[2]
            if w.vartype == 'nil' or vv.vartype == 'nil':
                if w.value == 'nil' and vv.value == 'nil':
                    v.value = 'true'
                else:
                    v.value = 'false'
            elif w.vartype == vv.vartype:
                if w.vartype == 'int':
                    if int(w.value) == int(vv.value):
                        v.value = 'true'
                    else:
                        v.value = 'false'
                elif w.vartype == 'bool':
                    if w.value == 'true' and vv.value == 'true':
                        v.value = 'true'
                    elif w.value == 'false' and vv.value == 'false':
                        v.value = 'true'
                    else:
                        v.value = 'false'
                elif w.vartype == 'string':
                    if w.value == vv.value:
                        v.value = 'true'
                    else:
                        v.value = 'false'
            else:
                exit(53)
        elif self.opcode == 'JUMPIFEQ':
            arg1 = self.arguments[1].value
            arg1type = self.arguments[1].vartype
            arg2 = self.arguments[2].value
            arg2type = self.arguments[2].vartype
            if arg1type == 'var':
                x = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'int')
                arg1 = x.value
                arg1type = x.vartype
            if arg2type == 'var':
                y = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, 'int')
                arg2 = y.value
                arg2type = y.vartype
            if arg1type == arg2type and int(arg1) == int(arg2):
                return self.jump(stack)
        elif self.opcode == 'JUMPIFNEQ':
            arg1 = self.arguments[1].value
            arg1type = self.arguments[1].vartype
            arg2 = self.arguments[2].value
            arg2type = self.arguments[2].vartype
            if arg1type == 'var':
                x = stack.find_var(self.arguments[1].value.split('@')[0], self.arguments[1].value, 'int')
                arg1 = x.value
                arg1type = x.vartype
            if arg2type == 'var':
                y = stack.find_var(self.arguments[2].value.split('@')[0], self.arguments[2].value, 'int')
                arg2 = y.value
                arg2type = y.vartype
            if arg1type == arg2type or arg1type == 'nil' or arg2type == 'nil':
                if arg1 != arg2:
                    return self.jump(stack)
            else:
                exit(53)
        elif self.opcode == 'LABEL':
            return j
        return j

    # Syntaktická a lexikální kontrola instrukcí a jejich argumentů
    # Funkce očekává parametry stack a i
    # stack reprezentuje objekt třídy FrameStack, využívá se zejména při tvorbě návěští
    # i reprezentuje pozici v kódu, využívá se zejména při tvorbě návěští
    # Funkce nic nevrací
    def parse(self, stack, i):
        if self.opcode == 'CREATEFRAME':
            self.argument_parse([])
        elif self.opcode == 'PUSHFRAME':
            self.argument_parse([])
        elif self.opcode == 'POPFRAME':
            self.argument_parse([])
        elif self.opcode == 'RETURN':
            self.argument_parse([])
        elif self.opcode == 'BREAK':
            self.argument_parse([])
        elif self.opcode == 'DEFVAR' or self.opcode == 'POPS':
            self.argument_parse(['var'])
        elif self.opcode == 'LABEL':
            self.argument_parse(['label'])
            for l in stack.labels:
                if self.arguments[0].value == l.name:
                    exit(52)
            stack.labels.append(label.Label(self.arguments[0].value, i))
        elif self.opcode == 'CALL' or self.opcode == 'JUMP':
            self.argument_parse(['label'])
        elif self.opcode == 'PUSHS' or self.opcode == 'WRITE' or self.opcode == 'DPRINT':
            self.argument_parse(['symb'])
        elif self.opcode == 'EXIT':
            self.argument_parse(['int'])
        elif self.opcode == 'MOVE' or self.opcode == 'TYPE':
            self.argument_parse(['var', 'symb'])
        elif self.opcode == 'STRLEN':
            self.argument_parse(['var', 'string'])
        elif self.opcode == 'INT2CHAR':
            self.argument_parse(['var', 'int'])
        elif self.opcode == 'READ':
            self.argument_parse(['var', 'type'])
        elif self.opcode == 'ADD' or self.opcode == 'SUB' or self.opcode == 'MUL' or self.opcode == 'IDIV':
            self.argument_parse(['var', 'int', 'int'])
        elif self.opcode == 'AND' or self.opcode == 'OR':
            self.argument_parse(['var', 'bool', 'bool'])
        elif self.opcode == 'NOT':
            self.argument_parse(['var', 'bool'])
        elif self.opcode == 'STRI2INT':
            self.argument_parse(['var', 'symb', 'int'])
        elif self.opcode == 'CONCAT':
            self.argument_parse(['var', 'string', 'string'])
        elif self.opcode == 'GETCHAR':
            self.argument_parse(['var', 'string', 'int'])
        elif self.opcode == 'SETCHAR':
            self.argument_parse(['var', 'int', 'string'])
        elif self.opcode == 'LT' or self.opcode == 'GT' or self.opcode == 'EQ':
            self.argument_parse(['var', 'symb', 'symb'])
        elif self.opcode == 'JUMPIFEQ' or self.opcode == 'JUMPIFNEQ':
            self.argument_parse(['label', 'symb', 'symb'])
        else:
            exit(32)
        return
