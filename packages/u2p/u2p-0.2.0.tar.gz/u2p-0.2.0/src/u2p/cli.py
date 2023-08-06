import argparse

import libcst as cst
from libcst.codemod import CodemodContext

from u2p.transformers import U2PTransformer


def _run_transformer(source: str) -> str:
    tree = cst.parse_module(source)
    transformer = U2PTransformer(CodemodContext())
    tree = transformer.transform_module(tree)
    return tree.code


def run(argv=None):
    parser = argparse.ArgumentParser("u2p")
    parser.add_argument("file")
    parser.add_argument(
        "-w",
        "--write",
        action="store_true",
        help="Write back modified files.",
    )

    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return exc.code

    with open(args.file) as f:
        out = _run_transformer(f.read())

    if args.write:
        with open(args.file, "w") as f:
            f.write(out)
    else:
        print(out)

    return 0
