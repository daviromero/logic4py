from logic4py.formula import AtomFormula, PredicateFormula, NegationFormula, BinaryFormula, AndFormula, OrFormula, ImplicationFormula, BiImplicationFormula, QuantifierFormula, ExistentialFormula, UniversalFormula

import traceback
## File lexer.py
from rply import LexerGenerator, ParserGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        #Comma
        self.lexer.add('COMMA', r'\,')

        # Dot
        self.lexer.add('DOT', r'\.')

        # Parentheses
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')

        #Brackets
        self.lexer.add('OPEN_BRACKET', r'\{')
        self.lexer.add('CLOSE_BRACKET', r'\}')

        #rules
        self.lexer.add('IMP_INTROD', r'->i')
        self.lexer.add('IMP_ELIM', r'->e')
        self.lexer.add('OR_INTROD', r'\|i')
        self.lexer.add('OR_ELIM', r'\|e')
        self.lexer.add('AND_INTROD', r'&i')
        self.lexer.add('AND_ELIM', r'&e')
        self.lexer.add('NEG_INTROD', r'~i')
        self.lexer.add('NEG_ELIM', r'~e')
        self.lexer.add('RAA', r'raa')
        self.lexer.add('BOTTOM_ELIM', r'@e')
        self.lexer.add('COPY', r'copie')

        # Connectives
        self.lexer.add('BOTTOM', r'@')
        self.lexer.add('NOT', r'~')
        self.lexer.add('AND', r'&')
        self.lexer.add('OR', r'\|')
        self.lexer.add('IMPLIE', r'->')
        self.lexer.add('IFF', r'<->')

        #First order rules
        self.lexer.add('EXT_INTROD', r'Ei')
        self.lexer.add('EXT_ELIM', r'Ee')
        self.lexer.add('ALL_INTROD', r'Ai')
        self.lexer.add('ALL_ELIM', r'Ae')

        #First order connectives
        self.lexer.add('EXT', r'E[a-z][a-z0-9]*')
        self.lexer.add('ALL', r'A[a-z][a-z0-9]*')

        # definitions
        self.lexer.add('DEF_NOT', r'def\~')
        self.lexer.add('DEF_IMPLIE', r'def\->')
        self.lexer.add('DEF_AND', r'def\&')
        self.lexer.add('DEF_OR', r'def\|')
        self.lexer.add('DEF_IFF', r'def\<->')
        self.lexer.add('DEF_BASE', r'defAtomos')

        # Dash
        self.lexer.add('DASH', r'-')

        # Number
        self.lexer.add('NUM', r'\d+')

        #justification
        self.lexer.add('HYPOTHESIS', r'hip')
        self.lexer.add('PREMISE', r'pre')

        #Variable
        self.lexer.add('VAR', r'(?!pre|hip)[a-z][a-z0-9]*')

        # Atom
        self.lexer.add('ATOM', r'[A-Z][A-Z0-9]*' )

        # Ignore spaces and comments
        self.lexer.ignore('##[^##]*##')
        self.lexer.ignore('#[^\n]*\n?')
        self.lexer.ignore('\s+')  

        # Detect symbols out of grammar
        self.lexer.add('OUT', r'.*' )      

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()



class ParserDefFormula():
    ERROR_NUM_NOT_DEFINED_BEFORE = 1
    ERROR_NUM_LINE_IS_ALREADY_DEFINED = 2
    ERROR_FORMULA_IS_NOT_VALID_FOR_RULE = 3
    def __init__(self, state):
        self.state = state
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUM', 'DOT', 'COMMA', 'OPEN_PAREN', 'CLOSE_PAREN', 'NOT',
             'AND', 'OR',  'BOTTOM','ATOM', 'IMPLIE', 'IFF',
             'VAR','EXT','ALL',
             'DEF_BASE', 'DEF_NOT','DEF_IFF', 'DEF_IMPLIE', 'DEF_AND', 'DEF_OR'],
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
        self.symbol_table = {}
        self.formule_latex = ''
        self.error = {
            'messages': []
        }



    def parse(self):
        @self.pg.production('program : steps')
        def program(p):
            if len(self.error['messages']):
                erro_msg = rf'**<font color="red">Os seguintes erros foram encontrados:</font>**' 
                #display(Markdown(rf'**<font color="red">Os seguintes erros foram encontrados:</font>**')) 
                #print('Os seguintes erros foram encontrados:')

                error_number = 1
                errorList = []

                for error_message in self.error['messages']:
                    errorList.append('Erro {}: {}'.format(error_number, error_message))
                    #print('Erro {}: {}'.format(error_number, error_message))
                    error_number += 1
                return erro_msg, errorList
            else:
                last_index = sorted(self.symbol_table.keys())[-1]
                return rf'**<font color="blue">A demonstração da fórmula {self.symbol_table[last_index][0].toString(parentheses=True)} está correta.</font>**',[]
                #display(Markdown(rf'**<font color="blue">A demonstração da fórmula {self.symbol_table[last_index][0].toString(parentheses=True)} está correta.</font>**')) 
                #print('A demonstração da fórmula {} está correta'.format(self.symbol_table[last_index][0].toString(parentheses=True))) 



        @self.pg.production('steps : steps step')
        @self.pg.production('steps : step')
        def steps(p):
            return self.symbol_table

        @self.pg.production('step : NUM DOT atoms DEF_BASE')
        def step_base(p):
            number_line = p[0].value
            atoms = p[2][1]

            if number_line in self.symbol_table:
                source_position = p[0].getsourcepos()
                line_error = source_position.lineno
                self.set_error(ParserDefFormula.ERROR_NUM_LINE_IS_ALREADY_DEFINED, line_error, number_line)
                return
                
            self.symbol_table[number_line] = []
            for athom in atoms:
                self.symbol_table[number_line].append(AtomFormula(key=athom))

        @self.pg.production('step : NUM DOT formula DEF_NOT NUM')
        def step_negation(p):
            number_line = p[0].value
            formula = p[2][1]

            source_position = p[0].getsourcepos()
            line_error = source_position.lineno

            #Se o número já tiver sido referenciado. 
            if number_line in self.symbol_table:
                self.symbol_table[number_line] = [formula]
                self.set_error(ParserDefFormula.ERROR_NUM_LINE_IS_ALREADY_DEFINED, line_error, number_line)
                return
            
            #Se o número referenciado não tiver na tabela de símbolos
            if not(p[4].value in self.symbol_table):
                #self.variables[number_line] = [formula]
                self.set_error(ParserDefFormula.ERROR_NUM_NOT_DEFINED_BEFORE, line_error, p[4].value)
                return
            
            if not (isinstance(formula,NegationFormula)):
                self.set_error(ParserDefFormula.ERROR_FORMULA_IS_NOT_VALID_FOR_RULE, line_error, formula.toString())
                return
            else:
                is_negation = False
                for f in self.symbol_table[p[4].value]:
                    if(formula==NegationFormula(f)):
                      is_negation=True
                      break
                if is_negation:
                  self.symbol_table[number_line] = [formula]
                else:
                  self.set_error(ParserDefFormula.ERROR_FORMULA_IS_NOT_VALID_FOR_RULE, line_error, formula.toString())

        @self.pg.production('step : NUM DOT formula DEF_AND NUM COMMA NUM')
        @self.pg.production('step : NUM DOT formula DEF_OR NUM COMMA NUM')
        @self.pg.production('step : NUM DOT formula DEF_IMPLIE NUM COMMA NUM')
        @self.pg.production('step : NUM DOT formula DEF_IFF NUM COMMA NUM')
        def step(p):
            number_line = p[0].value
            formula = p[2][1]

            source_position = p[0].getsourcepos()
            line_error = source_position.lineno

            #Se o número já tiver sido referenciado. 
            if number_line in self.symbol_table:
                self.symbol_table[number_line] = [formula]
                self.set_error(ParserDefFormula.ERROR_NUM_LINE_IS_ALREADY_DEFINED, line_error, number_line)
                return
            
            #Se os números referenciados não estiverem na tabela de símbolos
            if not(p[4].value in self.symbol_table):
                #self.variables[number_line] = [formula]
                self.set_error(ParserDefFormula.ERROR_NUM_NOT_DEFINED_BEFORE, line_error, p[4].value)
                return
            if not(p[6].value in self.symbol_table):
                #self.variables[number_line] = [formula]
                self.set_error(ParserDefFormula.ERROR_NUM_NOT_DEFINED_BEFORE, line_error, p[6].value)
                return
            
            if not (isinstance(formula,BinaryFormula)):
                self.set_error(ParserDefFormula.ERROR_FORMULA_IS_NOT_VALID_FOR_RULE, line_error, formula.toString())
                return
            else:
                is_binary = False
                for f1 in self.symbol_table[p[4].value]:
                  for f2 in self.symbol_table[p[6].value]:
                    if(p[3].gettokentype()=='DEF_AND' and (formula==AndFormula(f1,f2)or formula==AndFormula(f2,f1))):
                      is_binary=True
                      break
                    elif(p[3].gettokentype()=='DEF_OR' and (formula==OrFormula(f1,f2)or formula==OrFormula(f2,f1))):
                      is_binary=True
                      break
                    elif(p[3].gettokentype()=='DEF_IMPLIE' and (formula==ImplicationFormula(f1,f2)or formula==ImplicationFormula(f2,f1))):
                      is_binary=True
                      break
                    elif(p[3].gettokentype()=='DEF_IFF' and (formula==BiImplicationFormula(f1,f2)or formula==BiImplicationFormula(f2,f1))):
                      is_binary=True
                      break
                if is_binary:
                  self.symbol_table[number_line] = [formula]
                else:
                  self.set_error(ParserDefFormula.ERROR_FORMULA_IS_NOT_VALID_FOR_RULE, line_error, formula.toString())


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

        @self.pg.production('atoms : ATOM')
        @self.pg.production('atoms : ATOM COMMA atoms')
        def atomsList(p):
             if len(p) == 1:
                 return p[0], [p[0].value]
             else:
                result = p[2]
             return p[0], [p[0].value] + result[1]


        @self.pg.error
        def error_handle(token):
            productions = self.state.splitlines()
            error = ''  

            if(productions == ['']):
                error = 'Nenhuma linha foi recebida, verifique a entrada.'
            if token.gettokentype() == '$end':
                error = 'Nenhuma linha foi recebida, verifique a entrada.'
            else:
                source_position = token.getsourcepos()
                error = 'A demostração da fórmula não está correta, verifique se todas regras foram aplicadas corretamente.\nLembre-se que uma uma fórmula é definida pela seguinte BNF:\nF :== P | ~ P | P & Q | P | Q | P -> Q | P <-> Q | (P), onde P,Q são átomos.\n'
                error += 'Lembre-se que uma regra de inferência sempre inicia com um número seguido de um . (linha de referência), tem uma fórmula e uma justificativa (defAtomos, def~, def&, def->, def<-> com suas respectivas referências para fórmulas anteriores).'
                error += "Erro de sintaxe:\n"
                error += productions[source_position.lineno - 1]
                string = '\n'
                for i in range(source_position.colno -1):
                    string += ' '
                string += '^'
                if token.gettokentype() == 'OUT':
                    string += ' Símbolo não pertence a linguagem.'
                error += string
                
            raise ValueError("@@"+error)


    def set_error(self, type, line_error, token_error):
        productions = self.state.splitlines()
        if type == ParserDefFormula.ERROR_NUM_LINE_IS_ALREADY_DEFINED:
            self.error['messages'].append("A linha {} utiliza uma mesma numeração que já foi definida anteriormente a linha {}:\n  {}".format(token_error, line_error, productions[line_error-1]))
        elif type == ParserDefFormula.ERROR_NUM_NOT_DEFINED_BEFORE:
            self.error['messages'].append("A linha {} não foi definida anteriormente a linha {}:\n  {}".format(token_error, line_error, productions[line_error-1]))
        elif type == ParserDefFormula.ERROR_FORMULA_IS_NOT_VALID_FOR_RULE:
            self.error['messages'].append("A fórmula {} na linha {} não é uma conclusão válida para a regra definida com a linha referenciada:\n  {}".format(token_error, line_error, productions[line_error-1]))
            
    def get_parser(self):
        return self.pg.build()

    @staticmethod
    def getProof(input_text=''):
      lexer = Lexer().get_lexer()
      tokens = lexer.lex(input_text)

      pg = ParserDefFormula(state=input_text)
      pg.parse()
      parser = pg.get_parser()
      result, errors = parser.parse(tokens)
      return result, errors

def check_proof(input_proof, latex=True):
    try:
        return ParserDefFormula.getProof(input_proof)
    except ValueError:
        #s = traceback.format_exc()
        return None, []
    else:
        return None, []
        pass

