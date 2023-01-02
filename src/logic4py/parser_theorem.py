import traceback
from rply import ParserGenerator
from logic4py.formula import AtomFormula, PredicateFormula, NegationFormula, BinaryFormula, AndFormula, OrFormula, ImplicationFormula, BiImplicationFormula, QuantifierFormula, ExistentialFormula, UniversalFormula
from logic4py.lexer import Lexer

# Parser of Theorem
class ParserTheorem():
    def __init__(self, state):
        self.state = state
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['COMMA', 'OPEN_PAREN', 'CLOSE_PAREN', 'NOT',
             'AND', 'OR',  'BOTTOM','ATOM', 'IMPLIE', 'IFF',
             'VAR','EXT','ALL', 'V_DASH' ],
            #The precedence $\lnot,\forall,\exists,\land,\lor,\rightarrow,\leftrightarrow$
            precedence=[
                ('right', ['IFF']),
                ('right', ['IMPLIE']),
                ('right', ['OR']),
                ('right', ['AND']),
                ('right', ['EXT']),
                ('right', ['ALL']),
                ('right', ['NOT']),
            ]
        )

    def parse(self):
        @self.pg.production('program : formulaslist V_DASH formula')
        @self.pg.production('program : V_DASH formula')
        def program(p):
            if len(p) == 2:
              return [], p[1][1]
            else:
              return p[0][1], p[2][1]

        @self.pg.production('formula : EXT formula')
        @self.pg.production('formula : ALL formula')
        @self.pg.production('formula : formula OR formula')
        @self.pg.production('formula : formula AND formula')
        @self.pg.production('formula : formula IMPLIE formula')
        @self.pg.production('formula : formula IFF formula')
        @self.pg.production('formula : NOT formula')
        @self.pg.production('formula : ATOM OPEN_PAREN variableslist CLOSE_PAREN')
        @self.pg.production('formula : ATOM')
        @self.pg.production('formula : BOTTOM')
        def formula(p):
            if len(p) < 3:
                if p[0].gettokentype() == 'ATOM':
                    return p[0], AtomFormula(key=p[0].value)
                elif p[0].gettokentype() == 'BOTTOM':
                    return p[0], AtomFormula(key=p[0].value)
                elif p[0].gettokentype() == 'NOT':
                    result = p[1]
                    return p[0], NegationFormula(formula=result[1])  
                elif( not type(p[0]) is tuple):
                  result1 = p[0]
                  result2 = p[1]
                  # Universal Formula
                  if p[0].gettokentype() == 'EXT':  
                    var = p[0].value.split('E')[1]
                    return p[0], ExistentialFormula(variable=var, formula=p[1][1])
                  elif p[0].gettokentype() == 'ALL':  
                    var = p[0].value.split('A')[1]
                    return p[0], UniversalFormula(variable=var, formula=p[1][1])
            elif len(p)==4:
              # Predicate Formula
              name = p[0]
              varlist = p[2]
              return p[0], PredicateFormula(name=p[0].value,variables=varlist[1])            
            elif len(p) == 3:
              # Binary Formula
              result1 = p[0]
              result2 = p[2]
              if(p[1].value=='&'):
                return result1[0], AndFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='|'):
                return result1[0], OrFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='->'):
                return result1[0], ImplicationFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='<->'):
                return result1[0], BiImplicationFormula(left=result1[1], right=result2[1])
              else:
                return result1[0], BinaryFormula(key=p[1].value, left=result1[1], right=result2[1])

        @self.pg.production('formula : OPEN_PAREN formula CLOSE_PAREN')
        def paren_formula(p):
            result = p[1]
            return p[0], result[1]

        @self.pg.production('variableslist : VAR')
        @self.pg.production('variableslist : VAR COMMA variableslist')
        def variablesList(p):
             if len(p) == 1:
                 return p[0], [p[0].value]
             else:
                result = p[2]
             return p[0], [p[0].value] + result[1]

        @self.pg.production('formulaslist : formula')
        @self.pg.production('formulaslist : formula COMMA formulaslist')
        def formulasList(p):
             if len(p) == 1:
                 return p[0], [p[0][1]]
             else:
                result = p[2]
             return p[0], [p[0][1]] + result[1]


        @self.pg.error
        def error_handle(token):
            productions = self.state.splitlines()
            error = ''  

            if(productions == ['']):
                error = 'None formula was submitted.'
            if token.gettokentype() == '$end':
                error = 'None formula was submitted.'
            else:
                source_position = token.getsourcepos()
                error = 'The formula definition is not correct, check that all rules were applied correctly.\n Remember that a formula is defined by the following BNF:\nF :== P | ~ P | Q&A | P | Q | P -> Q | P <-> Q | (P), where P,Q are atoms'
                error += "Sintax error:\n"
                error += productions[source_position.lineno - 1]
                string = '\n'
                for i in range(source_position.colno -1):
                    string += ' '
                string += '^'
                if token.gettokentype() == 'OUT':
                    string += ' Symbol does not belong to language.'
                error += string
                
            raise ValueError("@@"+error)

    def get_error(self, type_error, token_error, rule):
        productions = self.state.splitlines()
        column_error = token_error.getsourcepos().colno
        erro = "Syntax error in line {}:\n".format(token_error.getsourcepos().lineno)
        erro += productions[token_error.getsourcepos().lineno-1] + "\n"
        for i in range(column_error-1):
            erro += ' '
        
        return erro
    
    def get_parser(self):
        return self.pg.build()
    
    @staticmethod
    def getTheorem(input_text=''):
        lexer = Lexer().get_lexer()
        tokens = lexer.lex(input_text)
        pg = ParserTheorem(state=input_text)
        pg.parse()
        parser = pg.get_parser()
        premises, conclusion = parser.parse(tokens)
        return premises, conclusion

    @staticmethod
    def toString(premisses,conclusion,parentheses=False, symbol_vdash=True):
      symbol = '|- ' if symbol_vdash else '|= '
      if (premisses==[]):
        return symbol+conclusion.toString(parentheses=parentheses)
      else:
        return ", ".join(f.toString(parentheses=parentheses) for f in premisses)+symbol+conclusion.toString(parentheses=parentheses)

    @staticmethod
    def toLatex(premisses,conclusion,parentheses=False, symbol_vdash=True):
      latex = '\\vdash ' if not symbol_vdash else '\\models '
      if (premisses==[]):
        return +conclusion.toLatex(parentheses=parentheses)
      else:
        return ", ".join(f.toLatex(parentheses=parentheses) for f in premisses) +latex+conclusion.toLatex(parentheses=parentheses)


def get_theorem(input_theorem=''):
    try:
        return ParserTheorem.getTheorem(input_theorem)
    except ValueError:
        #s = traceback.format_exc()
        return None
    else:
        return None
        pass

def theorem_toString(premisses,conclusion,parentheses=False, symbol_vdash=True):
    return ParserTheorem.toString(premisses,conclusion,parentheses=parentheses,symbol_vdash=symbol_vdash)

def theorem_toLatex(premisses,conclusion,parentheses=False, symbol_vdash=True):
    return ParserTheorem.toLatex(premisses,conclusion,parentheses=parentheses,symbol_vdash=symbol_vdash)
