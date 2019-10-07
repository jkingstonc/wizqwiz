from generator import Parser
from lex import Token

p = Parser()
result = p.parse([
    Token(Token.Q_AND_A),
    Token(Token.LITERAL, "What is the capital of England?"),
    Token(Token.LITERAL, "London"),
    Token(Token.END)
    ])

print(result)
f = open("C:\\Users\\44778\\Desktop\\revis.html", "w")
f.write(result)
f.close()
