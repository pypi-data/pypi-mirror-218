import libcst as cst
from libcst.codemod import ContextAwareTransformer


def transform(transformer: ContextAwareTransformer, source: str) -> str:
    tree = cst.parse_module(source)
    tree = transformer.transform_module(tree)
    return tree.code
