import zai_coder


def test_portable_uname_has_cli_expected_fields():
    result = zai_coder._portable_uname()

    assert result.sysname
    assert result.release
    assert hasattr(result, "nodename")
    assert hasattr(result, "version")
    assert hasattr(result, "machine")
