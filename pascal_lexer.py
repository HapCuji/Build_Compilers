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

	def str(self):
		result = ''
		while self.current_char is not None:
			result += self.current_char
			self.advance()
			if self.current_char == '\'':
				self.advance()
				break

		return Token(STRING, result)


	def peek(self):
		peek_pos = self.pos + 1
		if peek_pos > len(self.text) - 1:
			return None
		else:
			return self.text[peek_pos]

	def _id(self):
		result = ''
		while self.current_char is not None and self.current_char.isalnum():
			result += self.current_char
			self.advance()

		token = RESERVED_KEYWORDS.get(result.upper(), Token(ID, result)) #if there is no key value, returns None
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

			if self.current_char == ':' and self.peek() == '=':
				self.advance()
				self.advance()
				return Token(ASSIGN, ':=')

			if self.current_char == ';':
				self.advance()
				return Token(SEMI, ';')

			if self.current_char == '+':
				self.advance()
				return Token(PLUS, '+')

			if self.current_char == '-':
				self.advance()
				return Token(MINUS, '-')

			if self.current_char == '*':
				self.advance()
				return Token(MUL, '*')

			if self.current_char == '/':
				self.advance()
				return Token(FLOAT_DIV, '/')

			if self.current_char == '(':
				self.advance()
				return Token(LPAREN, '(')

			if self.current_char == ')':
				self.advance()
				return Token(RPAREN, ')')

			if self.current_char == '.':
				self.advance()
				return Token(DOT, '.')

			if self.current_char == '{':
				self.advance()
				self.skip_comment()
				continue

			if self.current_char == ':':
				self.advance()
				return Token(COLON, ':')

			if self.current_char == ',':
				self.advance()
				return Token(COMMA, ',')

			if self.current_char == '\'':
				self.advance()
				return self.str()

			self.error()

		return Token(EOF, None)


def main():
	import sys
	text = open("test_case.pas", 'r').read()

	lexer = Lexer(text)
	while True:
		token = lexer.get_next_token()
		if (token.type == EOF):
			break
		print(token)
	
if __name__ == '__main__':
	main()