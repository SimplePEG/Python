class PegJsVisitor(object):
    """Visitor that allows you to return result similar to PEG.js"""

    def visit(self, node):
        return getattr(self, node.type)(node)

    def string(self, node):
        return node.match

    def regex_char(self, node):
        return node.match

    def sequence(self, node):
        return [self.visit(child) for child in node.children]

    def ordered_choice(self, node):
        return [self.visit(child) for child in node.children]

    def zero_or_more(self, node):
        return [self.visit(child) for child in node.children]

    def one_or_more(self, node):
        return [self.visit(child) for child in node.children]

    def optional(self, node):
        return [self.visit(child) for child in node.children]

    def and_predicate(self, node):
        return None

    def not_predicate(self, node):
        return None

    def end_of_file(self, node):
        return None


class SimplePegActionsVisitor(object):
    """This visitor allows you to visit actions property of AST"""

    def __init__(self, actions):
        self.actions = actions

    def visit(self, node):
        if node.children:
            children = [self.visit(child) for child in node.children]
            node.children = children
        if self.actions and node.action:
            return getattr(self.actions, node.action)(node)
        return node
