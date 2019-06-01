from collections import OrderedDict

INTEGER       = 'INTEGER'
REAL          = 'REAL'
STRING        = 'STRING'
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST    = 'REAL_CONST'
PLUS          = 'PLUS'
MINUS         = 'MINUS'
MUL           = 'MUL'
INTEGER_DIV   = 'INTEGER_DIV'
FLOAT_DIV     = 'FLOAT_DIV'
LPAREN        = 'LPAREN'
RPAREN        = 'RPAREN'
ID            = 'ID'
ASSIGN        = 'ASSIGN'
BEGIN         = 'BEGIN'
END           = 'END'
SEMI          = 'SEMI'
DOT           = 'DOT'
PROGRAM       = 'PROGRAM'
VAR           = 'VAR'
COLON         = 'COLON'
COMMA         = 'COMMA'
EOF           = 'EOF'
FUNCTION	  = 'FUNCTION'

class Token(object):
	def __init__(self, type, value):
		self.type = type
		self.value = value

	def __str__(self):
		return 'Token({type}, {value})'.format(
			type = self.type,
			value = repr(self.value)
		)

	def __repr__(self):
		return self.__str__()

RESERVED_KEYWORDS = {
    'PROGRAM': Token('PROGRAM', 'PROGRAM'),
    'VAR': Token('VAR', 'VAR'),
    'DIV': Token('INTEGER_DIV', 'DIV'),
    'INTEGER': Token('INTEGER', 'INTEGER'),
    'REAL': Token('REAL', 'REAL'),
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END'),
    'FUNCTION': Token('FUNCTION', 'FUNCTION'), 
}

class Lexer(object):
	def __init__(self,text):
		self.text = text
		self.pos = 0
		self.current_char = self.text[self.pos]

	def error(self):
		raise Exception('Invalid character')

	def advance(self):
		self.pos += 1
		if self.pos > len(self.text) - 1:
			self.current_char = None   		
		else:
			self.current_char = self.text[self.pos]
	
	def skip_comment(self):
		while self.current_char != '}':
			self.advance()
		self.advance()				

	def skip_whitespace(self):
		while self.current_char is not None and self.current_char.isspace():
			self.advance()

	def number(self):
		result = ''
		while self.current_char is not None and self.current_char.isdigit():
			result += self.current_char
			self.advance()

		if self.current_char == '.':
			result += self.current_char
			self.advance()

			while self.current_char is not None and self.current_char.isdigit():
				result += self.current_char
				self.advance()

			token = Token('REAL_CONST', float(result))
		
		else:
			token = Token('INTEGER_CONST', int(result))
		
		return token

	def _id(self):
		result = ''
		while self.current_char is not None and self.current_char.isalnum(): #Returns True if the string has at least one character and all the characters of the string are numbers and / or letters, otherwise False.
			result += self.current_char
			self.advance()

		token = RESERVED_KEYWORDS.get(result, Token(ID, result))
		return token		

	def get_next_token(self):
		while self.current_char is not None:
			
			if self.current_char.isspace():
				self.skip_whitespace()
				continue

			if self.current_char.isalpha():
				return self._id()

			if self.current_char.isdigit():
				return self.number()

			#self.error()
			self.current_char = None
			self.advance()

		return Token(EOF, None)


def main():
	import sys
	text = open("test.pas", 'r').read()

	lexer = Lexer(text)
	while True:
		token = lexer.get_next_token()
		if (token.type == EOF):
			break
		print(token)
	
if __name__ == '__main__':
	main()