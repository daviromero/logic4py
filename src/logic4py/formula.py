import pandas as pd
from random import randrange


## File formula.py
class BinaryFormula():
    def __init__(self, key = '', left = None, right = None):
        self.key = key
        self.left = left
        self.right = right

    def __eq__(self, other): 
        if not isinstance(other, BinaryFormula):
            return NotImplemented

        return self.key == other.key and self.left == other.left and self.right == other.right

    def __ne__(self, other): 
        if not isinstance(other, BinaryFormula):
            return NotImplemented

        return self.key != other.key or self.left != other.left or self.right != other.right

    def __hash__(self):
      return hash(self.toString())

    def create_string_representation(self, formula, parentheses= False):
        if(parentheses):
          return formula.toString(parentheses=parentheses)
        elif isinstance(formula, BinaryFormula):
            return'({})'.format(formula.toString())
        else:
            return formula.toString()

    def create_latex_representation(self, formula, parentheses= False):
        if(parentheses):
          return formula.toLatex(parentheses=parentheses)
        elif isinstance(formula, BinaryFormula):
            return'({})'.format(formula.toLatex())
        else:
            return formula.toLatex()

    def is_implication(self):
      return self.key=='->'
    def is_conjunction(self):
      return self.key=='&'
    def is_disjunction(self):
      return self.key=='|'

    def toLatex(self, parentheses= False):
        operators = {
            '->': '\\rightarrow ',
            '&': '\\land ',
            '|': '\\lor ',
            '<->': '\\leftrightarrow ',
        }
        string = self.create_latex_representation(self.left, parentheses=parentheses)
        string += operators[self.key]
        string += self.create_latex_representation(self.right, parentheses=parentheses)
        if parentheses:
          return '('+string+')'
        return string

    def toString(self, parentheses= False):
        string = self.create_string_representation(self.left, parentheses=parentheses)
        string += self.key
        string += self.create_string_representation(self.right, parentheses=parentheses)
        if parentheses:
          return '('+string+')'
        return string

    def all_variables(self):
      return self.left.all_variables().union(self.right.all_variables())

    def bound_variables(self):
      return self.all_variables().difference(self.free_variables())

    def free_variables(self):
      return self.left.free_variables().union(self.right.free_variables())

    def is_substitutable(self, x, y):
      return self.left.substitutable(x,y) and self.right.substitutable(x,y) 

    def substitution(self, var_x, a):
      return BinaryFormula(self.key, self.left.substitution(var_x, a), self.right.substitution(var_x, a))

    def get_values_x_substitution(self, var_x, formula):
      if not (isinstance(formula,BinaryFormula) and self.key==formula.key):
        return set()
      else:
        return self.left.get_values_x_substitution(var_x, formula.left).union(self.right.get_values_x_substitution(var_x, formula.right))

    def is_first_order_formula(self):
      return self.left.is_first_order_formula() or self.right.is_first_order_formula()

class AndFormula(BinaryFormula):
    def __init__(self, left = None, right = None):
        super().__init__(key = '&', left=left, right = right)

class OrFormula(BinaryFormula):
    def __init__(self, left = None, right = None):
        super().__init__(key = '|', left=left, right = right)

class ImplicationFormula(BinaryFormula):
    def __init__(self, left = None, right = None):
        super().__init__(key = '->', left=left, right = right)

class BiImplicationFormula(BinaryFormula):
    def __init__(self, left = None, right = None):
        super().__init__(key = '<->', left=left, right = right)

class NegationFormula():
    def __init__(self, formula = None):
        self.formula = formula

    def __eq__(self, other): 
        if not isinstance(other, NegationFormula):
            return NotImplemented

        return self.formula == other.formula

    def __ne__(self, other): 
        if not isinstance(other, NegationFormula):
            return NotImplemented

        return self.formula != other.formula

    def __hash__(self):
      return hash(self.toString())

    def toLatex(self, parentheses= False):
        if(parentheses):
          return '('+'\\lnot ' + self.formula.toLatex(parentheses=parentheses)+')'
        if not isinstance(self.formula, BinaryFormula):
            string = '\\lnot ' + self.formula.toLatex()
        else:
            string = '\\lnot({})'.format(self.formula.toLatex())
        return string   

    def toString(self, parentheses= False):
        if parentheses:
            string = '(~' + self.formula.toString()+')'
        elif not isinstance(self.formula, BinaryFormula):
            string = '~' + self.formula.toString()
        else:
            string = '~({})'.format(self.formula.toString())
        return string 

    def all_variables(self):
      return self.formula.all_variables()

    def bound_variables(self):
      return self.all_variables().difference(self.free_variables())

    def free_variables(self):
      return self.formula.free_variables()

    def is_substitutable(self, x, y):
      return self.formula.substitutable(x,y)

    def substitution(self, var_x, a):
      return NegationFormula(self.formula.substitution(var_x, a))

    def get_values_x_substitution(self, var_x, formula):
      values = set()
      if not isinstance(formula,NegationFormula):
        return values
      else:
        return self.formula.get_values_x_substitution(var_x, formula.formula)

    def is_first_order_formula(self):
      return self.formula.is_first_order_formula()


class AtomFormula():
    def __init__(self, key = None):
        self.key = key

    def __hash__(self):
      return hash(self.toString())

    def __eq__(self, other): 
        if not isinstance(other, AtomFormula):
            return NotImplemented

        return self.key == other.key
    
    def __ne__(self, other): 
        if not isinstance(other, AtomFormula):
            return NotImplemented

        return self.key != other.key

    def toLatex(self, parentheses= False):
        if(self.key != '@'):
            return self.key  
        else:
            return '\\bot' 

    def toString(self, parentheses= False):
        return self.key  

    def all_variables(self):
      return set()

    def bound_variables(self):
      return set()

    def free_variables(self):
      return set()

    def is_substitutable(self, x, y):
      return True 

    def substitution(self, var_x, a):
      return AtomFormula(self.key)

    def get_values_x_substitution(self, var_x, formula):
      return set()
    def is_first_order_formula(self):
      return False

class BottonFormula(AtomFormula):
    def __init__(self):
      super().__init__(key='@')


class PredicateFormula():
    def __init__(self, name = '', variables = []):
        self.variables = variables
        self.name = name

    def __eq__(self, other): 
        if not isinstance(other, PredicateFormula):
            return NotImplemented
        return self.variables == other.variables and self.name == other.name
    
    def __ne__(self, other): 
        if not isinstance(other, PredicateFormula):
            return NotImplemented

        return self.variables != other.variables or self.name != other.name

    def __hash__(self):
      return hash(self.toString())

    def toLatex(self, parentheses= False):
        if self.variables: 
            return self.name+'('+','.join(self.variables)+')'
        else:
            return self.name

    def toString(self, parentheses= False):
        if self.variables: 
            return self.name+'('+','.join(self.variables)+')'
        else:
            return self.name

    def get_values_x_substitution(self, var_x, formula):
      values = set()
      if isinstance(formula, PredicateFormula) and formula.name==self.name and len(formula.variables)==len(self.variables):
        for i in range(len(self.variables)):
          if self.variables[i]==var_x:
            values.add(formula.variables[i])
      return values

    def all_variables(self):
      return set(self.variables)

    def bound_variables(self):
      return set()

    def free_variables(self):
      return set(self.variables)

    def is_substitutable(self, x, y):
      return True

    def substitution(self, var_x, a):
      aux_variables = []
      for v in self.variables:
        if(v==var_x): aux_variables.append(a)
        else: aux_variables.append(v)
      return PredicateFormula(self.name, aux_variables)

    def is_first_order_formula(self):
      return True

class QuantifierFormula():
    def __init__(self, forAll = True, variable=None, formula=None):
        self.forAll = forAll
        self.variable = variable
        self.formula = formula

    def __eq__(self, other): 
        if not isinstance(other, QuantifierFormula):
            return NotImplemented

        return self.forAll == other.forAll and self.variable == other.variable and self.formula == other.formula
    
    def __ne__(self, other): 
        if not isinstance(other, QuantifierFormula):
            return NotImplemented

        return self.forAll != other.forAll and self.variable != other.variable and self.formula != other.formula

    def __hash__(self):
      return hash(self.toString())

    def is_universal(self):
      return self.forAll

    def is_existential(self):
      return not self.forAll

    def toLatex(self, parentheses= False):
        if parentheses:
          if self.forAll:        
              return '(\\forall {} {})'.format(self.variable, self.formula.toLatex(parentheses=parentheses))
          else:
              return '(\\exists {} {})'.format(self.variable, self.formula.toLatex(parentheses=parentheses))
        elif not isinstance(self.formula, BinaryFormula):
          if self.forAll:        
              return '\\forall {} {}'.format(self.variable, self.formula.toLatex())
          else:
              return '\\exists {} {}'.format(self.variable, self.formula.toLatex())
        else:
          if self.forAll:        
              return '\\forall {} ({})'.format(self.variable, self.formula.toLatex())
          else:
              return '\\exists {} ({})'.format(self.variable, self.formula.toLatex())

    def toString(self, parentheses= False):
        if parentheses:
          if self.forAll:        
              return '(A{} {})'.format(self.variable, self.formula.toString(parentheses=parentheses))
          else:
              return '(E{} {})'.format(self.variable, self.formula.toString(parentheses=parentheses))
        if not isinstance(self.formula, BinaryFormula):
          if self.forAll:        
              return 'A{} {}'.format(self.variable, self.formula.toString())
          else:
              return 'E{} {}'.format(self.variable, self.formula.toString())
        else:
          if self.forAll:        
              return 'A{} ({})'.format(self.variable, self.formula.toString())
          else:
              return 'E{} ({})'.format(self.variable, self.formula.toString())

    def all_variables(self):
      result = self.formula.all_variables()
      result.add(self.variable)
      return result
      
    def bound_variables(self):
      return self.all_variables().difference(self.free_variables())

    def free_variables(self):
      result = self.formula.free_variables()
      result.discard(self.variable)
      return result 

    def is_substitutable(self, x, y):
      if (self.variable == y and x in self.formula.free_variables()):
        return False
      return self.formula.is_substitutable(x,y)# and (self.variable == y or x in self.formula.free_variables())

    def valid_substitution(self, formula):
      free_vars = formula.free_variables()
      for v in free_vars:
        fAux = self.formula.substitution(self.variable, v)
        if (fAux==formula):
          return True
      return False

    def substitution(self, var_x, a):
      if self.variable == var_x:
        return self#.formula#.clone()
      else:
        return QuantifierFormula(self.forAll,self.variable, self.formula.substitution(var_x, a))

    def get_values_x_substitution(self, var_x, formula):
      if not (isinstance(formula,QuantifierFormula) and self.forAll==formula.forAll):
        return set()
      #elif self.variable != var_x:
      #  return set()
      else:
        return self.formula.get_values_x_substitution(var_x, formula.formula)
    def is_first_order_formula(self):
      return True

class UniversalFormula(QuantifierFormula):
    def __init__(self, variable=None, formula=None):
      super().__init__( forAll = True, variable=variable, formula=formula)

class ExistentialFormula(QuantifierFormula):
    def __init__(self, variable=None, formula=None):
      super().__init__( forAll = False, variable=variable, formula=formula)


def num_atoms(formula):
  if isinstance(formula, AtomFormula) or isinstance(formula, PredicateFormula):
    return 1
  elif isinstance(formula, NegationFormula ):
    r1 = num_atoms(formula.formula)
    return r1
  elif isinstance(formula, BinaryFormula ):
    r1 = num_atoms(formula.left)
    r2 = num_atoms(formula.right)
    r_set = r1+r2
    return r_set    
  elif isinstance(formula, QuantifierFormula ):
    return num_atoms(formula.formula)

def num_negations(formula):
  if isinstance(formula, AtomFormula) or isinstance(formula, PredicateFormula):
    return 0
  elif isinstance(formula, NegationFormula ):
    r1 = num_negations(formula.formula)
    return 1+r1
  elif isinstance(formula, BinaryFormula ):
    r1 = num_negations(formula.left)
    r2 = num_negations(formula.right)
    r_set = r1+r2
    return r_set    
  elif isinstance(formula, QuantifierFormula ):
    return num_negations(formula.formula)

def num_binary_conectives(formula):
  if isinstance(formula, AtomFormula) or isinstance(formula, PredicateFormula):
    return 0
  elif isinstance(formula, NegationFormula ):
    r1 = num_binary_conectives(formula.formula)
    return r1
  elif isinstance(formula, BinaryFormula ):
    r1 = num_binary_conectives(formula.left)
    r2 = num_binary_conectives(formula.right)
    r_set = r1+r2+1
    return r_set    
  elif isinstance(formula, QuantifierFormula ):
    return num_negations(formula.formula)

def num_conectives(formula):
  if isinstance(formula, AtomFormula) or isinstance(formula, PredicateFormula):
    return 0
  elif isinstance(formula, NegationFormula ):
    r1 = num_conectives(formula.formula)
    return r1+1
  elif isinstance(formula, BinaryFormula ):
    r1 = num_conectives(formula.left)
    r2 = num_conectives(formula.right)
    r_set = r1+r2+1
    return r_set    
  elif isinstance(formula, QuantifierFormula ):
    return num_conectives(formula.formula)+1

def num_atom_atoms(formula, atom):
  if isinstance(formula, AtomFormula) or isinstance(formula, PredicateFormula):
    return formula==atom
  elif isinstance(formula, NegationFormula ):
    r1 = num_atom_atoms(formula.formula, atom)
    return r1
  elif isinstance(formula, BinaryFormula ):
    r1 = num_atom_atoms(formula.left, atom)
    r2 = num_atom_atoms(formula.right, atom)
    r_set = r1+r2
    return r_set    
  elif isinstance(formula, QuantifierFormula ):
    return num_atom_atoms(formula.formula, atom)
    
def get_atoms(formula):
  if isinstance(formula, AtomFormula) or isinstance(formula, PredicateFormula) :
    return {formula}
#    return {formula.toString()}
  elif isinstance(formula, NegationFormula ):
    return get_atoms(formula.formula)
  elif isinstance(formula, BinaryFormula ):
    set1 = get_atoms(formula.left)
    set2 = get_atoms(formula.right)
    r_set = set1.union(set2)
    return r_set    
  elif isinstance(formula, QuantifierFormula ):
    return get_atoms(formula.formula)

def get_subformulas(formula):
  if isinstance(formula, AtomFormula) or isinstance(formula, PredicateFormula):
    return {formula}
  elif isinstance(formula, NegationFormula ):
    r1 = get_subformulas(formula.formula)
    r_set = r1.union({formula})
    return r_set    
  elif isinstance(formula, BinaryFormula ):
    r1 = get_subformulas(formula.left)
    r2 = get_subformulas(formula.right)
    r_set = r1.union(r2)
    r_set = r_set.union({formula})
    return r_set    
  elif isinstance(formula, QuantifierFormula ):
    r1 = get_subformulas(formula.formula)
    r_set = r1.union({formula})
    return r_set    

def num_parentheses(formula):
  if isinstance(formula, AtomFormula) or isinstance(formula, PredicateFormula):
    return 0
  elif isinstance(formula, NegationFormula ):
    r1 = num_parentheses(formula.formula)
    return r1+2
  elif isinstance(formula, BinaryFormula ):
    r1 = num_parentheses(formula.left)
    r2 = num_parentheses(formula.right)
    r_set = r1+r2+2
    return r_set    
  elif isinstance(formula, QuantifierFormula ):
    return num_parentheses(formula.formula)+4

## Teorema da Definição Recursiva
def F(formula, Hp, Hn, Hand, Hor, Himp, HBiImp):
  if isinstance(formula, AtomFormula) or isinstance(formula, PredicateFormula):
    return Hp(formula)
  elif isinstance(formula, NegationFormula):
    return Hn(F(formula.formula,Hp, Hn, Hand, Hor, Himp, HBiImp))
  elif isinstance(formula, AndFormula):
    return Hand(F(formula.left,Hp, Hn, Hand, Hor, Himp, HBiImp), F(formula.right,Hp, Hn, Hand, Hor, Himp, HBiImp))
  elif isinstance(formula, OrFormula):
    return Hor(F(formula.left,Hp, Hn, Hand, Hor, Himp, HBiImp), F(formula.right,Hp, Hn, Hand, Hor, Himp, HBiImp))
  elif isinstance(formula, ImplicationFormula):
    return Himp(F(formula.left,Hp, Hn, Hand, Hor, Himp, HBiImp), F(formula.right,Hp, Hn, Hand, Hor, Himp, HBiImp))
  elif isinstance(formula, BiImplicationFormula):
    return HBiImp(F(formula.left,Hp, Hn, Hand, Hor, Himp, HBiImp), F(formula.right,Hp, Hn, Hand, Hor, Himp, HBiImp))

def F_binario(formula, Hp, Hn, Hbinario):
  return F(formula, Hp, Hn, Hbinario, Hbinario, Hbinario, Hbinario)

# Exemplo de função que calcula o número de parênteses de uma fórmula, utilizando o Teorema da Definição Recursiva
def Hp(x): 
  return 0
def Hn(x):
  return x+2
def Hand(x,y):
  return x+y+2
def Hor(x,y):
  return x+y+2
def Himp(x,y):
  return x+y+2
def HBiImp(x,y):
  return x+y+2


def f_par(formula):
  return F(formula,Hp, Hn, Hand, Hor, Himp, HBiImp)

# Calcula o tamanho de uma fórmula
def Tp(x):
  return 1
def Tn(x):
  return x+1
def Tb(x,y):
  return x+y+1
  
def tam(formula):
  return F(formula, Tp, Tn, Tb, Tb, Tb, Tb)


# Verfica se uma fórmula é satisfeita para uma função de valoração v

def v_bar(formula, v):
  if isinstance(formula, PredicateFormula):
    raise ValueError("Fórmula tem ser proposicional.")
  if isinstance(formula, AtomFormula):
    if formula.key =='@': 
      return 0
    elif formula.key in v.keys(): 
      return v[formula.key]
    else:
      raise ValueError(f"Átomo {formula.key} não está definido.")    
  elif isinstance(formula, NegationFormula):
    return 1 if not v_bar(formula.formula,v) else 0
  elif isinstance(formula, AndFormula):
    return 1 if v_bar(formula.left,v) and v_bar(formula.right,v) else 0
  elif isinstance(formula, OrFormula):
    return 1 if v_bar(formula.left,v) or v_bar(formula.right,v) else 0
  elif isinstance(formula, ImplicationFormula):
    return 1 if (not v_bar(formula.left,v)) or v_bar(formula.right,v) else 0
  elif isinstance(formula, BiImplicationFormula):
    return 1 if v_bar(formula.left,v) == v_bar(formula.right,v) else 0

def get_vs(formula,premises=[]):
  if premises !=[]:
    atoms = get_atoms(formula)
    for f in premises:
      atoms = atoms.union(get_atoms(f))
    atoms = sorted([a.toString() for a in atoms])
  else:
    atoms = sorted([a.toString() for a in get_atoms(formula)])
  return get_vs_atoms(atoms)

def get_vs_atoms(atoms):
  vs = []
  size = len(atoms)
  for i in range(2**size):
    v = dict()
    for j in range(size):
      v[atoms[j]] = 1 if i // (2**(size-j-1)) % 2 == 0 else 0
#      v[atoms[j]] = True if i // (2**(size-j-1)) % 2 == 0 else False
    vs.append(v)  
  return vs

def truth_table(formula, premises=[], show_subformulas=True,parentheses=False):
  vs = get_vs(formula,premises=premises)
  df = pd.DataFrame.from_records(vs)
  if(show_subformulas):
    subs = get_subformulas(formula)
    atoms = get_atoms(formula)
    for f in premises:
      subs = subs.union(get_subformulas(f))
      atoms = atoms.union(get_atoms(f))
    formulas = subs.difference(atoms) 
    for f in formulas:
      df[f.toString(parentheses=parentheses)] = [v_bar(f,v) for v in vs]  
  else:   
    for f in premises:
      df[f.toString(parentheses=parentheses)] = [v_bar(f,v) for v in vs]
  df_columns = sorted(df.columns,key=len)
  df.columns = df_columns  
  df[formula.toString(parentheses=parentheses)] = [v_bar(formula,v) for v in vs]
  df.head().style.hide_index()
  return df

def consequence_logic(formula, premises=[], show_subformulas=True,parentheses=False):
  df = truth_table(formula, premisses=premises, show_subformulas=show_subformulas,parentheses=parentheses)
  df_true = df
  for p in premises:
    df_true = df_true[df_true[p.toString(parentheses=parentheses)]==1]
  for index, row in df_true.iterrows():
    if not row[formula.toString(parentheses=parentheses)]:
      return index
  return None


def is_consequence_logic(formula, premises=[], show_subformulas=True,parentheses=False):
    row = consequence_logic(formula, premises=premises, show_subformulas=show_subformulas,parentheses=parentheses)
    if row==None:
      return True
    else:
      return False

def is_satisfiable(formula):
  for v in truth_table(formula)[formula.toString()]:
    if v:
      return True
  return False

def is_falsiable(formula):
  for v in truth_table(formula)[formula.toString()]:
    if not v:
      return True
  return False

def is_unsatisfiable(formula):
  return not is_satisfiable(formula)

def is_valid(formula):
  return not is_falsiable(formula)

def generate_proposicional_formula(len_binary_formula = 2):
  atoms = ['A', 'B', 'C', 'D', 'E']
  conectivss = ['&', '|', '->', '<->']
  f = '~'+atoms[randrange(0,5)] if randrange(0,2) else atoms[randrange(0,5)]
  while len_binary_formula>0:
    f+= conectivss[randrange(0,4)]
    f+= '~'+atoms[randrange(0,5)] if randrange(0,2) else atoms[randrange(0,5)]
    len_binary_formula -= 1
  return f
