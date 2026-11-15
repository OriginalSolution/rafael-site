import unittest

from guardian_core import advance, backoff_delays, health_doc, summarize, with_backoff

OK = {"name": "Home", "ok": True, "detail": "200"}
BAD = {"name": "Home", "ok": False, "detail": "answered 503"}


class BackoffTest(unittest.TestCase):
    def test_delays_double_and_cap(self):
        self.assertEqual(backoff_delays(4), [2, 4, 8])
        self.assertEqual(backoff_delays(6, base=10, cap=30), [10, 20, 30, 30, 30])
        self.assertEqual(backoff_delays(1), [])

    def test_retries_until_ok(self):
        seq, slept = iter([1, 2, 3]), []
        r, n = with_backoff(lambda: next(seq), lambda v: v == 3, tries=4, sleep=slept.append)
        self.assertEqual((r, n), (3, 3))
        self.assertEqual(slept, [2, 4])

    def test_gives_up(self):
        slept = []
        r, n = with_backoff(lambda: 0, lambda v: False, tries=3, sleep=slept.append)
        self.assertEqual((r, n, slept), (0, 3, [2, 4]))


class AdvanceTest(unittest.TestCase):
    def test_ok(self):
        st = {}
        o = advance(st, [OK], "t1")
        self.assertEqual((o["status"], o["reason"], o["dispatch"], o["incidents"]), ("ok", "All checks passed.", False, []))
        self.assertEqual(st["last_ok_at"], "t1")

    def test_persisting_problem_dispatches_once_then_every_4(self):
        st, sent = {}, []
        for i in range(1, 11):
            sent.append(advance(st, [BAD], f"t{i}")["dispatch"])
        # runs 2, 6, 10 dispatch
        self.assertEqual([i + 1 for i, s in enumerate(sent) if s], [2, 6, 10])

    def test_incidents_open_resolve_repair(self):
        st = {}
        o1 = advance(st, [dict(BAD, fixes=["re-requested a Pages build (201)"])], "t1")
        self.assertEqual([i["kind"] for i in o1["incidents"]], ["opened", "repair"])
        o2 = advance(st, [BAD], "t2")
        self.assertEqual([i["kind"] for i in o2["incidents"]], ["dispatch"])
        o3 = advance(st, [OK], "t3")
        self.assertEqual([i["kind"] for i in o3["incidents"]], ["resolved"])
        self.assertEqual((o3["status"], st["consecutive_attention"], st["failing"]), ("ok", 0, {}))

    def test_reason_is_plain(self):
        self.assertEqual(summarize([OK, {"name": "APK", "ok": False, "detail": "no asset"}]), ("attention", "APK: no asset"))

    def test_health_doc(self):
        st = {}
        o = advance(st, [BAD], "t1")
        h = health_doc("userafael.com", o, [BAD], st, "t1", "u")
        self.assertEqual((h["status"], h["checked_at"], h["checks"][0]["ok"]), ("attention", "t1", False))


if __name__ == "__main__":
    unittest.main()
