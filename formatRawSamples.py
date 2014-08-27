from __future__ import division

from slimit.lexer import Lexer
from slimit.parser import Parser
from slimit.visitors.nodevisitor import ASTVisitor

text = open('test.js').read();

linecount = len(text.splitlines())

tokenList = []
tokens = {}

lexer = Lexer()
lexer.input(text)
for token in lexer:
    tokens[token.lexpos] = dict(
        t = token.type[:],
        v = token.value[:],
        prior = [t.value for t in tokenList[-5:]] + [''] * (5 - len(tokenList[-5:]))
    )
    tokenList.append(token)

parser = Parser(yacc_tracking=True)
tree = parser.parse(text)

class TrainingSample(object):
    def __init__(self, structure, lineno, prior, match, completion):
        self._structure = structure

        self._slno = lineno
        self._slpc = self._slno / linecount
        self._elno = linecount - self._slno
        self._elpc = self._elno / linecount

        self._prior = prior
        self._match = match
        self._completion = completion

    def __repr__(self):
        return str((self._structure, 'slno=', self._slno, 'slpc=', self._slpc, 'elno=', self._elno, 'elpc=', self._elpc, 'prior=', self._prior, 'value=', self._match, 'completion', self._completion))

trainingSamples = []

class TrainingVisitor(ASTVisitor):
    def visitChildren(self, node):
        for child in node.children():
            self.visit(child)

    def visit_VarStatement(self, node):
        """Visit var statement"""
        token = tokens[node.lexpos]
        sample = TrainingSample('VarStmt', node.lineno, token['prior'], token['v'], node.to_ecma())
        trainingSamples.append(sample);
        self.visitChildren(node)

    def visit_VarDecl(self, node):
        """Visit var declaration"""
        token = tokens[node.lexpos]
        sample = TrainingSample('VarDecl', node.lineno, token['prior'], token['v'], node.to_ecma())
        trainingSamples.append(sample);

visitor = TrainingVisitor()
visitor.visit(tree)
for sample in trainingSamples:
    print sample
