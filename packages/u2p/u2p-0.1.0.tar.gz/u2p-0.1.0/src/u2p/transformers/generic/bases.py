import libcst as cst
import libcst.matchers as m
from libcst.codemod import CodemodContext, ContextAwareTransformer


class RemoveBaseClassTransformer(ContextAwareTransformer):
    def __init__(self, context: CodemodContext, base: str) -> None:
        super().__init__(context)

        if len(parts := base.split(".", maxsplit=1)) == 2:
            value, attr = parts
            self._base = m.Attribute(
                value=m.Name(value=value),
                attr=m.Name(value=attr),
            )
        else:
            self._base = m.Name(value=base)

    def leave_ClassDef(self, original_node, updated_node):
        updated_bases = [
            base for base in updated_node.bases if not m.matches(base.value, self._base)
        ]
        updated = len(updated_bases) != len(updated_node.bases)

        if updated:
            updated_node = updated_node.with_changes(bases=updated_bases)

            # If no more bases, remove parentheses.
            if len(updated_node.bases) == 0:
                updated_node = updated_node.with_changes(
                    lpar=cst.MaybeSentinel.DEFAULT,
                    rpar=cst.MaybeSentinel.DEFAULT,
                )

        return updated_node
