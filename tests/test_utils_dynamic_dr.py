import importlib
import sys
import types
import unittest


def _install_anki_stubs():
    anki = types.ModuleType("anki")

    decks = types.ModuleType("anki.decks")
    decks.DeckManager = object

    stats = types.ModuleType("anki.stats")
    stats.REVLOG_LRN = 0
    stats.REVLOG_REV = 1
    stats.REVLOG_RELRN = 2
    stats.REVLOG_CRAM = 3

    stats_pb2 = types.ModuleType("anki.stats_pb2")
    stats_pb2.CardStatsResponse = type(
        "CardStatsResponse",
        (),
        {"StatsRevlogEntry": object},
    )

    cards = types.ModuleType("anki.cards")
    cards.Card = object

    aqt = types.ModuleType("aqt")
    aqt.mw = types.SimpleNamespace(col=object())

    aqt_utils = types.ModuleType("aqt.utils")
    aqt_utils.askUser = lambda *_args, **_kwargs: False

    sys.modules.update(
        {
            "anki": anki,
            "anki.decks": decks,
            "anki.stats": stats,
            "anki.stats_pb2": stats_pb2,
            "anki.cards": cards,
            "aqt": aqt,
            "aqt.utils": aqt_utils,
        }
    )


class TestDynamicDesiredRetentionIntegration(unittest.TestCase):
    def setUp(self):
        _install_anki_stubs()
        sys.modules.pop("utils", None)
        self.utils = importlib.import_module("utils")

    def tearDown(self):
        sys.modules.pop("dynamic_desired_retention", None)

    def test_get_effective_dr_falls_back_when_resolver_is_missing(self):
        sys.modules.pop("dynamic_desired_retention", None)

        self.assertEqual(self.utils.get_effective_dr(object(), 0.9), 0.9)

    def test_get_effective_dr_falls_back_when_resolver_is_not_exported(self):
        sys.modules["dynamic_desired_retention"] = types.ModuleType(
            "dynamic_desired_retention"
        )

        with self.assertLogs("utils", level="WARNING") as logs:
            self.assertEqual(self.utils.get_effective_dr(object(), 0.9), 0.9)

        self.assertIn(
            "dynamic desired retention resolver is unavailable",
            "\n".join(logs.output),
        )

    def test_get_effective_dr_uses_optional_resolver(self):
        module = types.ModuleType("dynamic_desired_retention")
        module.effective_desired_retention = (
            lambda *, collection, card, current_desired_retention: 0.95
        )
        sys.modules["dynamic_desired_retention"] = module

        self.assertEqual(self.utils.get_effective_dr(object(), 0.9), 0.95)

    def test_get_effective_dr_falls_back_when_resolver_fails(self):
        module = types.ModuleType("dynamic_desired_retention")

        def fail(**_kwargs):
            raise RuntimeError("resolver failed")

        module.effective_desired_retention = fail
        sys.modules["dynamic_desired_retention"] = module

        self.assertEqual(self.utils.get_effective_dr(object(), 0.9), 0.9)


if __name__ == "__main__":
    unittest.main()
