# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 01:05:49 2017
@author: svart
"""

from lark import Lark
from lark.tree import pydot__tree_to_png 
#import sys

#file = open(sys.argv[1],'r')
file = open('test.txt', 'r')

grammar =  """

    inst : declaration | assign | if_begin | while_begin | do_begin
   
    if_begin : "if" "(" expr ")" next_if
        | "if" "(" expr ")" next_if "else" next_if
    next_if : assign | declaration | if_begin | block  
    
    while_begin : "while" "(" expr ")" next_while
    next_while : inst | block
    
    do_begin : "do" block "while" "(" expr ")"
    
    block : "{" inst "}"
    
    assign : ID next_assign ";"
    next_assign : "=" eq_expr | OPINCA | OPINCB eq_expr
    
    declaration : TYPE ID next_dclr? ";"
    next_dclr : EQUALS eq_expr end_dclr? | "," ID end_dclr?
    end_dclr :  "," ID next_dclr    

    eq_expr : const eq_expr_next? 
    eq_expr_next : OPNUM eq_expr
    
    expr : s OPCOMP s end_expr? | s
    s : "(" e ")" | e
    e : const _e?
    _e : OPNUM e
    const : NUMBER | ID
    end_expr : OPLOG expr
    

    
    
    
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

#parser = Lark(expr_grammar, start='expr')
parser = Lark(grammar, start='inst')

#result = parser.parse('if(i==j) a=2; else {a=3;}')
#res_1 = parser.parse('if(a) if(b) b=1; else a=3; else { b=2; }')
#result = parser.parse('while(a==3 && b<=2) { if(a) a=3; else b=3;}')
#result = parser.parse('do { a+=2; } while(s)')
try:
    result = parser.parse('a=d;')
except Exception:
    print("No match")
else:
    print(result)
    pydot__tree_to_png(result, "test.png")
#print(result)
'''
for line in file:
    result = parser.parse(line)
    print(result)    
'''
file.close()