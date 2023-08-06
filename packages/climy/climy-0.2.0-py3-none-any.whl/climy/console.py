import shutil

CINIT = '\033[{}m'
CEND = '\033[0m'
CBLOCK = '\033[{}m{}\033[0m'

CBOLD = '1'
CDIM = '2'
CITALIC = '3'
CURL = '4'
CSBLINK = '5'
CFBLINK = '6'
CSELECTED = '7'

CBLACK = '30'
CRED = '31'
CGREEN = '32'
CYELLOW = '33'
CBLUE = '34'
CVIOLET = '35'
CCYAN = '36'
CGREY = '37'
CWHITE = '38'

CBLACKBG = '40'
CREDBG = '41'
CGREENBG = '42'
CYELLOWBG = '43'
CBLUEBG = '44'
CVIOLETBG = '45'
CCYANBG = '46'
CGREYBG = '47'
CWHITEBG = '48'

CBLACKH = '90'
CREDH = '91'
CGREENH = '92'
CYELLOWH = '93'
CBLUEH = '94'
CVIOLETH = '95'
CCYANH = '96'
CGREYH = '97'
CWHITEH = '98'

CBLACKBGH = '100'
CREDBGH = '101'
CGREENBGH = '102'
CYELLOWBGH = '103'
CBLUEBGH = '104'
CVIOLETBGH = '105'
CCYANBGH = '106'
CGREYBGH = '107'
CWHITE = '108'

PGBLOCK = '\u2588'

HSOLID = '\u2500'
VSOLID = '\u2502'

TLSOLID = '\u250C'
TRSOLID = '\u2510'
TDSOLID = '\u252C'

BLSOLID = '\u2514'
BRSOLID = '\u2518'
BUSOLID = '\u2534'

CLSOLID = '\u251C'
CSOLID = '\u253C'
CRSOLID = '\u2524'

cstyles = {
    'bold': '1',
    'dim': '2',
    'italic': '3',
    'underline': '4',
    'black': CBLACK,
    'red': CRED,
    'green': CGREEN,
    'yellow': CYELLOW,
    'blue': CBLUE,
    'violet': CVIOLET,
    'cyan': CCYAN,
    'grey': CGREY,
    'white': CWHITE,
    'bgblack': CBLACKBG,
    'bgred': CREDBG,
    'bggreen': CGREENBG,
    'bgyellow': CYELLOWBG,
    'bgblue': CBLUEBG,
    'bgviolet': CVIOLETBG,
    'bgcyan': CCYANBG,
    'bggrey': CGREYBG,
    'bgwhite': CWHITE,
    'hblack': CBLACKH,
    'hred': CREDH,
    'hgreen': CGREENH,
    'hyellow': CYELLOWH,
    'hblue': CBLUEH,
    'hviolet': CVIOLETH,
    'hcyan': CCYANH,
    'hgrey': CGREYH,
    'hwhite': CWHITEH,
    'hbgblack': CBLACKBGH,
    'hbgred': CREDBGH,
    'hbggreen': CGREENBGH,
    'hbgyellow': CYELLOWBGH,
    'hbgblue': CBLUEBGH,
    'hbgviolet': CVIOLETBGH,
    'hbgcyan': CCYANBGH,
    'hbggrey': CGREYBGH,
    'hbgwhite': CWHITE,
}


def stext(text: str, style: str):
    splt = style.split(' ')
    ccode = ';'.join([cstyles.get(item, '39') for item in splt])
    return CBLOCK.format(ccode, text)


def sprint(text: str, style='', align='<', end='\n'):
    ste = stext(text, style=style)
    if align == '>':
        tml_columns = shutil.get_terminal_size().columns
        size = len(text)
        ste = ' ' * (tml_columns - size) + ste
    elif align == '^':
        tml_columns = shutil.get_terminal_size().columns
        ste = ste.center(tml_columns)
    print(stext, end=end)


def cmove(x, y):
    print('\033[{x};{y}HTESTE'.format(x=x, y=y))


class CTable:
    def __init__(self, columns: list[str]):
        self.columns = columns


def ctable(
        data: list,
        columns: list[str],
        style='',
        end_last=True,
        print_header=True
):
    tml_columns = shutil.get_terminal_size().columns
    tml_rest = tml_columns
    tcols = {}
    thline = f'{TLSOLID}'
    bhline = f'{CLSOLID}'
    iline = f'{CLSOLID}'
    bline = f'{BLSOLID}'
    htext = f'{VSOLID}'
    for idx, col in enumerate(columns):
        splt = col.split(':')
        name = splt[0]
        if len(splt) > 1:
            align = splt[1][-1] if splt[1][-1] in ['<', '^', '>'] else '<'
            size = int(splt[1][:-1] if splt[1][-1] in ['<', '^', '>'] else splt[1])
            tml_rest -= size
        else:
            align = '<'
            size = 0
        cl = {
            'name': name,
            'align': align,
            'size': size,
            'last': idx == len(columns) - 1
        }
        tcols[idx] = cl
    for idx, col in tcols.items():
        if col['size'] == 0:
            col['size'] = tml_rest - (len(tcols) + 1)
        size = col['size']
        last = col['last']
        name = col['name']
        align = col['align']
        thline += HSOLID * size + (TRSOLID if last else TDSOLID)
        bhline += HSOLID * size + (CRSOLID if last else CSOLID)
        iline += HSOLID * size + (CRSOLID if last else CSOLID)
        bline += HSOLID * size + (BRSOLID if last else BUSOLID)
        match align:
            case '<':
                htext += ' ' + name.ljust(size - 1) + VSOLID
            case '^':
                htext += name.center(size) + VSOLID
            case '>':
                htext += name.rjust(size - 1) + ' ' + VSOLID
    if print_header:
        sprint(thline, style=style)
        sprint(htext, style=style)
        sprint(bhline, style=style)
    for item in data:
        dline = VSOLID
        for idx, val in enumerate(item):
            col = tcols[idx]
            match col['align']:
                case '<':
                    dline += ' ' + str(val).ljust(col['size'] - 1) + VSOLID
                case '^':
                    dline += str(val).center(col['size']) + VSOLID
                case '>':
                    dline += str(val).rjust(col['size'] - 1) + ' ' + VSOLID
        sprint(dline, style=style)
    if end_last:
        sprint(bline, style=style)
    else:
        sprint(iline, style=style)


def cprogress(
        size: int,
        max=0.0,
        value=0.0,
        color='grey',
        loop=True,
        hold=False,
        before: str = '',
        after: str = ''
):
    fator = size / max
    maked_size = int(value * fator)
    rest_size = size - maked_size
    maked = stext(('\u2501' * maked_size), style=f'{color} bold')
    rest = stext(('\u2500' * rest_size), style=f'{color} dim')
    if loop:
        if rest_size > 0:
            print(f'{before} {maked}{rest} {after}', end='\r' if loop else '\n')
        elif hold:
            print(f'{before} {maked}{rest} {after}')
    else:
        print(f'{before} {maked}{rest} {after}')
