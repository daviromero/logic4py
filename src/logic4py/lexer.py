from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        #Comma
        self.lexer.add('COMMA', r'\,')

        # Dot
        self.lexer.add('DOT', r'\.')

        # Vdash
        self.lexer.add('V_DASH', r'\|-|\|=')

        # Parentheses
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')

        #Brackets
        self.lexer.add('OPEN_BRACKET', r'\{')
        self.lexer.add('CLOSE_BRACKET', r'\}')

        # Connectives
        self.lexer.add('BOTTOM', r'@')
        self.lexer.add('NOT', r'~')
        self.lexer.add('AND', r'&')
        self.lexer.add('OR', r'\|')
        self.lexer.add('IMPLIE', r'->')
        self.lexer.add('IFF', r'<->')

        #First order connectives
        self.lexer.add('EXT', r'E[a-z][a-z0-9]*')
        self.lexer.add('ALL', r'A[a-z][a-z0-9]*')

        #Variable
        self.lexer.add('VAR', r'(?!pre)[a-z][a-z0-9]*')

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
