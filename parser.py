# -*- coding: utf-8 -*-
from lark import Lark
from lark.tree import pydot__tree_to_png 
#import sys
#file = open(sys.argv[1],'r')

grammar =  """

    inst : declaration | assign | if_begin | while_begin | do_begin 
        | for_begin | switch_begin
   
    if_begin : IF OPEN_P expr CLOSE_P next_if
        | IF OPEN_P expr CLOSE_P next_if "else" next_if
    next_if : inst | block  
    
    while_begin : WHILE OPEN_P expr CLOSE_P next_while
    next_while : inst | block
    
    do_begin : "do" block "while" OPEN_P expr CLOSE_P
    
    for_begin : FOR OPEN_P a ";" b ";" i CLOSE_P next_for
    next_for : block | inst
    a : a1 | a1 "," a2 "," a2 
    a1 : TYPE ID EQUALS d1
    a2 : ID | ID EQUALS d1
    d : NUMBER | ID 
    d1 : d | b
    b : ee | ee o | ee o OPLOG a2 | ee o OPNUM a2
    ee : ID | NUMBER | "true" | "false"
    o : OPLOG b | OPNUM b | OPCOMP b
    i : ID f | ID f i
    f : OPINCA | OPINCB d1 | ID a2
    
    switch_begin : sw_wrd opc "}" | sw_wrd opa "}"
    sw_wrd : SWITCH OPEN_P ID CLOSE_P "{"
    opa : CASE const ":" op? opb opa | DEFAULT ":" op? opb
    opc : CASE "'" ID "'" ":" op? opb opc | DEFAULT ":" op? opb
    opb : BREAK ";"
    op: inst 
    
    block : "{" inst "}"
    
    assign : ID next_assign ";"
    next_assign : EQUALS eq_expr | OPINCA | OPINCB eq_expr
    
    declaration : TYPE ID next_dclr? ";"
    next_dclr : EQUALS eq_expr end_dclr? | "," ID end_dclr?
    end_dclr :  "," ID next_dclr    

    eq_expr : const eq_expr_next? 
    eq_expr_next : OPNUM eq_expr
    
    expr : s OPCOMP s end_expr? | s
    s : OPEN_P e CLOSE_P | e
    e : const _e?
    _e : OPNUM e
    const : NUMBER | ID
    end_expr : OPLOG expr
    

       
    WHILE : /while/
    IF : /if/
    FOR : /for/
    SWITCH : /switch/
    CASE : /case/
    DEFAULT : /default/
    BREAK : /break/
    OPEN_P : /\(/
    CLOSE_P : /\)/
    OPLOG : /&&|\|\|/    
    OPCOMP : /<=|>=|<|>|==|!=/  
    OPNUM : /\+|-|\*|%|\//
    OPINCA : /\+\+|--/
    OPINCB : /\+=|-=|\*=|\/=/
    ID : /[_A-Za-z]([A-Za-z0-9_]*)/
    EQUALS : /=/
    TYPE : /int|float|double|boolean/

    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

file = open('test.txt', 'r')

# Creacion del objeto que representa la gramatica
parser = Lark(grammar, start='inst')


i = 1
nameTREE = ''

# Leer el archivo linea por linea
for line in file:
    try:
        result = parser.parse(line.rstrip())
    except Exception:
        print("Error sintactico en linea "+str(i))
    else:
        print(result.pretty()) 
        nameTREE = 'arbol_' + str(i) + '.png'
        i += 1
        pydot__tree_to_png(result, nameTREE)   

file.close()