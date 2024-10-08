
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'EQUAL NUMBER OCTOTHORPE PLUS REGISTER SEMICOLON VARNAMEprogram : statement SEMICOLON program \n               | emptystatement : normal_assignment \n                 | register_assignmentnormal_assignment : VARNAME EQUAL NUMBERregister_assignment : OCTOTHORPE REGISTER VARNAME EQUAL VARNAME PLUS VARNAMEempty :'
    
_lr_action_items = {'$end':([0,1,3,8,11,],[-7,0,-2,-7,-1,]),'VARNAME':([0,8,10,14,16,],[6,6,13,15,17,]),'OCTOTHORPE':([0,8,],[7,7,]),'SEMICOLON':([2,4,5,12,17,],[8,-3,-4,-5,-6,]),'EQUAL':([6,13,],[9,14,]),'REGISTER':([7,],[10,]),'NUMBER':([9,],[12,]),'PLUS':([15,],[16,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,8,],[1,11,]),'statement':([0,8,],[2,2,]),'empty':([0,8,],[3,3,]),'normal_assignment':([0,8,],[4,4,]),'register_assignment':([0,8,],[5,5,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement SEMICOLON program','program',3,'p_program','main.py',58),
  ('program -> empty','program',1,'p_program','main.py',59),
  ('statement -> normal_assignment','statement',1,'p_statement','main.py',62),
  ('statement -> register_assignment','statement',1,'p_statement','main.py',63),
  ('normal_assignment -> VARNAME EQUAL NUMBER','normal_assignment',3,'p_normal_assignment','main.py',66),
  ('register_assignment -> OCTOTHORPE REGISTER VARNAME EQUAL VARNAME PLUS VARNAME','register_assignment',7,'p_register_assignment','main.py',71),
  ('empty -> <empty>','empty',0,'p_empty','main.py',78),
]
