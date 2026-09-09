class PilhaCheiaErro(Exception):
    """Levantada ao tentar empilhar em uma pilha que atingiu a capacidade máxima."""
    pass

class PilhaVaziaErro(Exception):
    """Levantada ao tentar desempilhar ou acessar elementos de uma pilha vazia."""
    pass

class TipoErro(TypeError):
    """Levantada ao tentar empilhar um dado de tipo incompatível com a pilha."""
    pass