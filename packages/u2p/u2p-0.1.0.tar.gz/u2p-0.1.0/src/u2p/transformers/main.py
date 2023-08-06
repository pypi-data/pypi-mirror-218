import libcst as cst
from libcst.codemod import ContextAwareTransformer

from u2p.transformers import (
    ReplaceAssertEqualTransfomer,
    ReplaceAssertRaisesTransformer,
    ReplaceAssertTrueTransformer,
)
from u2p.transformers.generic import RemoveBaseClassTransformer


class U2PTransformer(ContextAwareTransformer):
    def transform_module_impl(self, tree: cst.Module) -> cst.Module:
        transformers: list[ContextAwareTransformer] = [
            ReplaceAssertEqualTransfomer(self.context),
            ReplaceAssertRaisesTransformer(self.context),
            ReplaceAssertTrueTransformer(self.context),
            RemoveBaseClassTransformer(self.context, "TestCase"),
            RemoveBaseClassTransformer(self.context, "unittest.TestCase"),
        ]

        for transformer in transformers:
            tree = transformer.transform_module(tree)

        return tree
