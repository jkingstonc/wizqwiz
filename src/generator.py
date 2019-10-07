# James Clarke
# 05/10/2019
# This file contains a recursive parser for
# generating a html quiz from a set of notes

from lex import Token

class Parser:

    def __init__(self):
        self.pos = 0
        self.html_string = ""
        self.js_string = ""

    def parse(self, tokens):
        self.tokens = tokens
        self.body()
        full_html = "<html><head><script>{}</script></head><body>{}</body></html>".format(self.js_string, self.html_string)
        return full_html

    def body(self):
        while not self.end():
            n = self.next()
            if n.tok == Token.MULTIPLE_CHOICE:
                self.multiple_choice()
            elif n.tok == Token.Q_AND_A:
                self.q_and_a()

    # Multiple choice question
    def multiple_choice(self):
        self.html("<h1>Multiple Choice Quiz</h1>")
    
    # Parse a single question and answer
    def q_and_a(self):
        title = self.consume(Token.LITERAL, "Expected question!")
        answer = self.consume(Token.LITERAL, "Expected answer for question!")
        button = "<button onclick='qafunc_{}()'>Try it</button>".format(self.sanitize(title))
        input_box = "<input id=qainput_{} placeholder='enter your answer here'>".format(self.sanitize(title))
        self.js("""
            function qafunc_{}() {{
                var x = document.getElementById("qa_{}");
                var answer = document.getElementById("qainput_{}");
                if(answer.value == "{}")
                {{
                    x.innerHTML = "Correct!";
                }}else{{
                    x.innerHTML = "Incorrect! Correct answer is {}";
                }}
                x.style.display = "block";
            }}
            """.format(self.sanitize(title), self.sanitize(title), self.sanitize(title), answer, answer))
        self.html("<h1>{}</h1>{}{}<div id='qa_{}'><p style='display:none;'>correct answer: {}</p></div>".format(title, input_box, button, self.sanitize(title), answer))

    def sanitize(self, literal):
        return literal.replace(" ", "_").replace("?", "")

    # Parse a line of text
    def line(self):
        pass

    def html(self, tag):
        self.html_string+=tag


    def js(self, code):
        self.js_string+=code

    def consume(self, expected, msg):
        if self.peek().tok != expected:
            print("{} [{}]".format(msg, expected))
        else:
            return self.next().value

    def next(self):
        n = self.tokens[self.pos]
        self.pos+=1
        return n

    def peek(self):
        n = self.tokens[self.pos]
        return n

    def end(self):
        if self.pos > len(self.tokens)-1 or self.peek().value == Token.END:
            return True
        return False