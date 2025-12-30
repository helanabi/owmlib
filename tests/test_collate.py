from owmlib.core import collate

def test_collate():
    test_sample = (
        ((0,), '0'),
        ((1,), '1'),
        ((None, [], {}), ''),
        (('', ''), ''),
        (("one", ''), "one"),
        (('', "two"), "two"),
        (("one", "two"), "one,two"),
        (('', "two", ''), "two"),
        (("one", 2, "three"), "one,2,three")
    )

    for args, result in test_sample:
        assert collate(*args) == result
