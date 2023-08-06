from clint.textui import puts, colored, indent
from pick import pick
import colorama

colorama.init()

class Choice(object):
    def __init__(self, index, option):
        self.index = index
        self.option = option

def choose_from_list(title, options):
    option, index = pick(options, title)
    index += 1
    return Choice(index, option)

def progress_bar(current, total, name="Progress", bar_length=50):
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '
    ending = '\n' if current >= total else '\r'
    print(f'{name}: [{arrow}{padding}] {int(fraction*100)}%', end=ending)

def ask_bool(prompt):
    while True:
        try:
            return {"true":True,"yes":True,"y":True,"false":False,"no":False,"n":False}[input(prompt).lower()]
        except KeyError:
            print("invalid input")

def ask_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("not a number")

def printc(n, d = '', f = False, sepL = 0, sepC = ' ', Beg = colored.green('//|'), BegL = 4):
    sep = ''
    for i in range(sepL):
        sep =+ sepC
    with indent(BegL, quote=Beg):
        if f == False:
            puts(colored.blue(n) + sep + d)
        else:
            puts(colored.blue(d) + sep + n)

def printd(n, d = '', f = False, A = False, sepL = 0, sepC = ' ', Beg = colored.red('>>|'), BegL = 4):
    if A == True:
        sep = ''
        for i in range(sepL):
            sep =+ sepC
        with indent(BegL, quote=Beg):
            if f == False:
                puts(colored.blue(n) + sep + d)
            else:
                puts(colored.blue(d) + sep + n)

def clearsc(type=1):
    if type == 1:
        print('\033[2J')
    elif type == 2:
        for i in range(25):
            print('\n')

if __name__ == '__main__':
    exit()