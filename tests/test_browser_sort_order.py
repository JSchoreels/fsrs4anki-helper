import unittest

from browser.sort_order import target_retrievability_order


class TestBrowserSortOrder(unittest.TestCase):
    def test_uses_builtin_retrievability_order_when_available(self):
        builtin = object()
        columns = {"retrievability": builtin}
        fallback = "c.id"
        self.assertIs(target_retrievability_order(columns, fallback), builtin)

    def test_falls_back_when_builtin_retrievability_order_unavailable(self):
        columns = {"deck": object()}
        fallback = "c.id"
        self.assertEqual(target_retrievability_order(columns, fallback), fallback)


if __name__ == "__main__":
    unittest.main()
