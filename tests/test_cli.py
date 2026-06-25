from zai_coder.cli import build_parser


def test_parser_has_new_commands():
    parser = build_parser()
    for args in (["scan"], ["audit"], ["serve"], ["memory", "list"], ["patch", "x.diff"]):
        ns = parser.parse_args(args)
        assert hasattr(ns, "func")
