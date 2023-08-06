import libcst as cst
import libcst.matchers as m
from libcst.codemod import CodemodContext, ContextAwareTransformer
from libcst.codemod.visitors import AddImportsVisitor

__all__ = (
    "ReplaceAssertEqualTransfomer",
    "ReplaceAssertTrueTransformer",
    "ReplaceAssertRaisesTransformer",
)

AssertTrue = m.Attribute(
    value=m.Name(value="self"),
    attr=m.Name(value="assertTrue"),
)
AssertEqual = m.Attribute(
    value=m.Name(value="self"),
    attr=m.Name(value="assertEqual"),
)
AssertRaises = m.Attribute(
    value=m.Name(value="self"),
    attr=m.Name(value="assertRaises"),
)


class ReplaceAssertTrueTransformer(ContextAwareTransformer):
    def __init__(self, context: CodemodContext) -> None:
        super().__init__(context)

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        if m.matches(updated_node.func, AssertTrue):
            return cst.Assert(updated_node.args[0].value)
        return updated_node


class ReplaceAssertEqualTransfomer(ContextAwareTransformer):
    def __init__(self, context: CodemodContext) -> None:
        super().__init__(context)

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        if m.matches(updated_node.func, AssertEqual):
            return cst.Assert(
                test=cst.Comparison(
                    left=updated_node.args[0].value,
                    comparisons=[
                        cst.ComparisonTarget(
                            operator=cst.Equal(),
                            comparator=updated_node.args[1].value,
                        )
                    ],
                )
            )
        return updated_node


class ReplaceAssertRaisesTransformer(ContextAwareTransformer):
    def __init__(self, context: CodemodContext) -> None:
        super().__init__(context)

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        if m.matches(updated_node.func, AssertRaises):
            AddImportsVisitor.add_needed_import(self.context, "pytest")
            return updated_node.with_changes(
                func=cst.Attribute(
                    value=cst.Name(
                        value="pytest",
                    ),
                    attr=cst.Name(
                        value="raises",
                    ),
                ),
            )
        return updated_node
