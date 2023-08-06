from typing import Callable, List, Type, Union

import libcst as cst
from libcst.codemod import CodemodContext, ContextAwareTransformer
from libcst.codemod.visitors import AddImportsVisitor

from u2p.transformers import (
    ReplaceAssertEqualTransfomer,
    ReplaceAssertRaisesTransformer,
    ReplaceAssertTrueTransformer,
)
from u2p.transformers.generic import RemoveBaseClassTransformer


class U2PTransformer(ContextAwareTransformer):
    def transform_module_impl(self, tree: cst.Module) -> cst.Module:
        transformer_classes: List[
            Union[
                Type[ContextAwareTransformer],
                Callable[[CodemodContext], ContextAwareTransformer],
            ]
        ] = [
            ReplaceAssertEqualTransfomer,
            ReplaceAssertRaisesTransformer,
            ReplaceAssertTrueTransformer,
            RemoveBaseClassTransformer.for_base_class("TestCase"),
            RemoveBaseClassTransformer.for_base_class("unittest.TestCase"),
            AddImportsVisitor,
        ]

        for transformer_class in transformer_classes:
            tree = transformer_class(self.context).transform_module(tree)

        return tree
