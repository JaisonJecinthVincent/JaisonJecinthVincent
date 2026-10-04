import os

def test_workflow_file_exists_and_has_schedule():
    path = ".github/workflows/update-profile.yml"
    assert os.path.exists(path)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    assert 'cron: "17 12 * * *"' in text
    assert "workflow_dispatch:" in text
