from ast import Assign, Str
from chameleon import PageTemplate, PageTemplateFile
from chameleon.codegen import template
from urllib.parse import quote_plus

def test_expr(string):
    def compiler(target, engine):
        compiler = engine.parse(string)
        body = compiler.assign_value(target)
        value = Str(string + "OK")
        print()
        return [Assign(targets=[target], value=value)]
    return compiler

class URLExpr(object):

    def __init__(self, expression):
        self.expression = expression

    def __call__(self, target, engine):
        compiler = engine.parse(self.expression)
        body = compiler.assign_value(target)
        return body + template("from urllib.parse import quote_plus; target = quote_plus(target)", target=target)

class RDFExpr(object):

    def __init__(self, expression):
        self.expression = expression

    def get_parse_expression(self):
        subject, predicate = self.expression.strip().split()
        return 'rdf.get_objects(' + subject + ', ' + predicate +')'

    def __call__(self, target, engine):
        compiler = engine.parse(self.get_parse_expression())
        body = compiler.assign_value(target)
        return body + template("target = target", target=target)

class CodeExpr(object):

    def __init__(self, expression):
        self.expression = expression

    def __call__(self, target, engine):
        compiler = engine.parse(self.expression)
        body = compiler.assign_value(target)
        return body + template("from base64 import b64encode; target = b64encode(bytes(target, 'utf-8'))", target=target)


PageTemplateFile.expression_types['test'] = test_expr
PageTemplateFile.expression_types['url'] = URLExpr
PageTemplateFile.expression_types['rdf'] = RDFExpr
PageTemplateFile.expression_types['code'] = CodeExpr

