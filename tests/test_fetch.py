from tools.profile.fetch import should_commit_changes

def test_should_commit_when_json_differs():
    assert should_commit_changes({"a": 1}, {"a": 2}) is True

def test_should_skip_when_json_identical():
    assert should_commit_changes({"a": 1}, {"a": 1}) is False
