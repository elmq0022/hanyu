# from django.test import TestCase
from .management.commands import load_cedict


ellipsis_entry = "省略號 省略号 [sheng3 lu:e4 hao4] /the ellipsis …… (punct., consisting of six dots)/"

def test_ellipsis():
    load = load_cedict.Command()
    results = load.valid_entries.findall(ellipsis_entry)
    assert len(results) > 0
