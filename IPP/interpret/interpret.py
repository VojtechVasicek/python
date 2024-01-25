# Autor: Vojtěch Vašíček (xvasic31)
#
# Toto je základní soubor interpret.py, který se volá při spouštění interpretu

import sys
import os.path
import xml.etree.ElementTree as ET
import instruction
import argument
import frameStack


# Zkontroluje order jednotlivých instrukcí a ty pak podle něj seřadí
# Funkce očekává parametr instructions, který reprezentuje řetězec všech zadaných instrukcí ze souboru xml
# Funkce nic nevrací
def check_order(instructions):
    orders = []
    for instruct in instructions:
        if instruct.order is None:
            exit(32)
        if not instruct.order.isdigit():
            exit(32)
        orders.append(int(instruct.order))
    u_orders = []
    for uniq in orders:
        if uniq not in u_orders:
            u_orders.append(uniq)
        else:
            exit(32)
    n = len(instructions)
    for i in range(n - 1):   # Seřazení instrukcí pomocí bubble sortu
        for j in range(0, n - i - 1):
            if int(instructions[j].order) > int(instructions[j + 1].order):
                instructions[j], instructions[j + 1] = instructions[j + 1], instructions[j]
    for order in orders:
        if int(order) < 1:
            exit(32)


# Seřazení jednotlivých argumentů podle jejich tagu
# Funkce očekává parametr args, což je řetězec reprezentující všechny argumenty dané instrukce
# Funkce nic nevrací
def order_args(args):
    n = len(args)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if args[j].tag > args[j + 1].tag:
                args[j], args[j + 1] = args[j + 1], args[j]
    if n == 1:
        if args[0].tag != '1':
            exit(32)
    if n == 2:
        if args[0].tag != '1' or args[1].tag != '2':
            exit(32)
    if n == 3:
        if args[0].tag != '1' or args[1].tag != '2' or args[2].tag != '3':
            exit(32)


# Funkce převede xml pomocí knihovny, pak volá parsování jednotlivých intstrukcí a jejich interpretaci
# Funkce očekává parametry source a inp
# source reprezentuje vstupní xml
# inp reprezentuje vstup (input) intepretovaného programu
# Funkce nic nevrací
def parse_xml(source, inp):
    tree = ET.parse(source)
    root = tree.getroot()
    inpu = open(inp, 'r')
    inputi = []
    for line in inpu:
        inputi.append(line)
    stack = frameStack.FrameStack()
    i = 0
    # Vytváření objektů instrukcí a argumentů
    for child in root:
        args = []
        if child.tag != 'instruction' or child.get('opcode') is None:
            exit(32)
        for arg in child:
            if arg.tag != 'arg1' and arg.tag != 'arg2' and arg.tag != 'arg3':
                exit(32)
            argum = argument.Argument(arg.get('type'), arg.text, arg.tag.split('g')[1])
            args.append(argum)
        order_args(args)
        instr = instruction.Instruction(child.get('opcode'), child.get('order'), args)
        # Syntaktická a lexikální analýza instrukce a jejích argumentů
        instr.parse(stack, i)
        i += 1
        stack.instructions.append(instr)
    check_order(stack.instructions)
    j = 0
    # Samotná interpretace
    while j < i:
        j = stack.instructions[j].interpret(stack, inputi, j)
        j += 1


# Hlavní tělo skriptu, slouží zejména pro parsování argumentů a načítání jednoho nebo žádného obsahu argumentu z stdinu
def main():
    # Parsování argumentů
    if len(sys.argv) > 4:
        exit(10)
    if '--help' in sys.argv:
        print('Tento skript interpretuje kod v jazyce IPPcode21.')
        exit(0)
    source = [s for s in sys.argv if '--source=' in s]
    input = [s for s in sys.argv if '--input=' in s]
    f = 'src.src'
    inp = 'input.in'
    # Získání source a input podle jejich zadání pomocí parametrů a stdinu
    if source and input:
        source = source[0].split('=')
        if not os.path.isfile(source[1]):
            exit(11)
        f = source[1]
        input = input[0].split('=')
        if not os.path.isfile(input[1]):
            exit(11)
        inp = input[1]
    elif not source and input:
        fi = open(f, 'w')
        for line in sys.stdin:
            fi.write(line)
        fi.close()
        input = input[0].split('=')
        if not os.path.isfile(input[1]):
            exit(11)
        inp = input[1]
    elif not input and source:
        source = source[0].split('=')
        if not os.path.isfile(source[1]):
            exit(11)
        f = source[1]
        inpu = open(inp, 'w')
        for line in sys.stdin:
            inpu.write(line)
        inpu.close()
    else:
        exit(10)

    parse_xml(f, inp)
    return 0


main()
