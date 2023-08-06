from typing import Optional

import libcst as cst
from libcst.codemod import CodemodContext, ContextAwareTransformer
from libcst.codemod.visitors import AddImportsVisitor, RemoveImportsVisitor

__all__ = (
    "AddImportTransformer",
    "RemoveImportTransformer",
)


class AddImportTransformer(ContextAwareTransformer):
    """
    A wrapper for AddImportsVisitor from libcst providing
    an interface consistent with all other transformers.
    """

    def __init__(
        self,
        context: CodemodContext,
        module: str,
        obj: Optional[str] = None,
        asname: Optional[str] = None,
        relative: int = 0,
    ) -> None:
        super().__init__(context)
        self._args = (module, obj, asname, relative)

    def transform_module_impl(self, tree: cst.Module) -> cst.Module:
        AddImportsVisitor.add_needed_import(self.context, *self._args)
        return AddImportsVisitor(self.context).transform_module(tree)


class RemoveImportTransformer(ContextAwareTransformer):
    """
    A wrapper for RemoveImportsVisitor from libcst providing
    an interface consistent with all other transformers.
    """

    def __init__(
        self,
        context: CodemodContext,
        module: str,
        obj: Optional[str] = None,
        asname: Optional[str] = None,
    ) -> None:
        super().__init__(context)
        self._args = (module, obj, asname)

    def transform_module_impl(self, tree: cst.Module) -> cst.Module:
        RemoveImportsVisitor.remove_unused_import(self.context, *self._args)
        return RemoveImportsVisitor(self.context).transform_module(tree)
