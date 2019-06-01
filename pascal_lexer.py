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
#<new>
CASE 		  = 'CASE'
OF 		 	  = 'OF'
CONST 		  = 'CONST'
TYPE 		  = 'TYPE'
ARRAY 		  = 'ARRAY'
PACKED 		  = 'PACKED'
RECORD 		  = 'RECORD'
FILE_OF 	  = 'FILE OF'
WHILE 		  = 'WHILE'
REPEAT 		  = 'REPEAT'
UNTIL 		  = 'UNTIL'
DIV 		  = 'DIV'
MOD 		  = 'MOD'
AND 		  = 'AND'
OR 		  	  = 'OR'
IF 		  	  = 'IF'
THEN 		  = 'THEN'
ELSE 		  = 'ELSE'
DOTDOT        = 'DOTDOT'	# need in subrange (for type in generall)
#<seldom use in coding on Pascal>
WITH 		  = 'WITH' 		#can work in python?
DO 		  	  = 'DO'
NIL 		  = 'NIL'
NOT 		  = 'NOT'
	
CURRENT_LINE_NUMBER =  1


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
    #new 
    'CASE': Token('CASE', 'CASE'),
    'OF': Token('OF', 'OF'),				# together with 'case', 'packege', 'array'
    'CONST': Token('CONST', 'CONST'),
    'TYPE': Token('TYPE', 'TYPE'),
    'ARRAY': Token('ARRAY', 'ARRAY'),
    'PACKED': Token('PACKED', 'PACKED'),
    'RECORD': Token('RECORD', 'RECORD'),
    'FILE OF': Token('FILE_OF', 'FILE OF'),
    'WHILE': Token('WHILE', 'WHILE'),
    'REPEAT': Token('REPEAT', 'REPEAT'),	
    'UNTIL': Token('UNTIL', 'UNTIL'),		# together with 'repeat'
    'DIV': Token('DIV', 'DIV'), 			
    'MOD': Token('MOD', 'MOD'), 		
    'AND': Token('AND', 'AND'), 		
    'OR': Token('OR', 'OR'), 				
    'IF': Token('IF', 'IF'), 		
    'THEN': Token('THEN', 'THEN'), 			# together with 'IF'
    'ELSE': Token('ELSE', 'ELSE'), 			# together with 'IF THEN' (can not be)
    #'DOTDOT': Token('DOTDOT', 'DOTDOT'), 	# together with 'of'
    #seldom
    'WITH': Token('WITH', 'WITH'), 		
    'DO': Token('DO', 'DO'), 				# together with 'while', 'with' (, 'for')
    'NIL': Token('NIL', 'NIL'), 		
    'NOT': Token('NOT', 'NOT'), 		

}

class Lexer(object):

	def __init__(self,text):
		self.text = text
		self.pos = 0
		self.current_char = self.text[self.pos]

	def error(self, message='Invalid character', result_intterupt=''):
		'''Can write any 'message' and reson why we have 'result_intterupt'.
		'''
		message = str(message) + " - on line (" + str(CURRENT_LINE_NUMBER) + ")." 	# from global var
		if result_intterupt != '':
			message = "In '" + str(result_intterupt) + "'. " + message
		raise Exception(message)

	def advance(self):
		self.pos += 1
		if self.pos > len(self.text) - 1:
			self.current_char = None   		
		else:
			self.current_char = self.text[self.pos]
	
	def retire(self):
		self.pos -= 1
		if self.pos < 1:
			self.current_char = None   		
		else:
			self.current_char = self.text[self.pos]

	def skip_comment(self):
		while self.current_char != '}':
			self.advance()
		self.advance()				

	def skip_whitespace(self):
		while self.current_char is not None and self.current_char.isspace():
			if(self.current_char == '\n'):
				global CURRENT_LINE_NUMBER
				CURRENT_LINE_NUMBER = CURRENT_LINE_NUMBER + 1
			self.advance()

	def number(self):
		result = ''
		while self.current_char is not None and self.current_char.isdigit():
			result += self.current_char
			self.advance()

		if self.current_char == '.':
			self.advance()
			if self.current_char.isdigit():
				result += '.'
				while self.current_char is not None and self.current_char.isdigit():
					result += self.current_char
					self.advance()
				token = Token('REAL_CONST', float(result))
			else: 									#if not digit
				if self.current_char == '.':		#check on 'duble dot'
					self.retire()					#return on one step ago
				else:								#after '.' was not 'count' and not 'duble dot'
					self.error('After point - must be count or range.', result)
				token = Token('INTEGER_CONST', int(result))
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
		while self.current_char is not None and self.current_char.isalnum(): #return true if all sim is num or from alphabet
			result += self.current_char
			self.advance()

		token = RESERVED_KEYWORDS.get(result.upper(), Token(ID, result)) #if there is no key value, returns None
		return token		

	def get_next_token(self):
		while self.current_char is not None:
			
			if self.current_char.isspace():
				self.skip_whitespace()
				continue

			if self.current_char.isalpha(): #return true if all sim from alphabet
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
				if self.current_char == '.':
					self.advance()
					return Token(DOTDOT, '..')
				else:
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