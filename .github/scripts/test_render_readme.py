import importlib.util
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "renderer", Path(__file__).with_name("render-readme.py")
)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


def repo(name, fork=False, private=False, description=None):
    return {"full_name": name, "html_url": "https://github.com/" + name,
            "description": description, "fork": fork, "private": private}


class RenderTests(unittest.TestCase):
    def test_contributions_filter_and_sort(self):
        def entry(name, day, private=False, empty=False):
            return {"repository": {"nameWithOwner": name, "url": "https://github.com/" + name,
                                   "description": None, "isPrivate": private},
                    "contributions": {"nodes": [] if empty else [{"occurredAt": day}]}}
        entries = [entry("user/old", "2026-01-01"), entry("user/private", "2026-10-01", True),
                   entry("User/User", "2026-10-01"), entry("user/empty", "", empty=True),
                   entry("user/new", "2026-09-01")]
        names = [r["nameWithOwner"] for r in renderer.recent_contributions(entries, "user")]
        self.assertEqual(names, ["user/new", "user/old"])

    def test_latest_repos_skip_those_already_shown(self):
        repos = [repo("user/a"), repo("user/b", fork=True), repo("user/c", private=True),
                 repo("user/user"), repo("user/d"), repo("user/e")]
        picked = renderer.latest_repos(repos, "user", exclude=["User/A"])
        self.assertEqual([r["full_name"] for r in picked], ["user/d", "user/e"])

    def test_empty_description_leaves_no_dash(self):
        self.assertEqual(renderer.repo_line("u/r", "https://x", None), "- [u/r](https://x)")
        self.assertEqual(renderer.repo_line("u/r", "https://x", " a\nb "),
                         "- [u/r](https://x) — a b")

    def test_markdown_metacharacters_are_escaped(self):
        line = renderer.repo_line("u/r", "https://x", "[click](https://evil) | <b>")
        self.assertEqual(line, r"- [u/r](https://x) — \[click\](https://evil) \| \<b\>")
        pr = {"title": "Fix [bug]", "html_url": "https://github.com/o/r/pull/1",
              "repository_url": "https://api.github.com/repos/o/r"}
        self.assertEqual(renderer.pr_line(pr),
                         r"- [Fix \[bug\]](https://github.com/o/r/pull/1) on [o/r](https://github.com/o/r)")

    def test_substituted_text_is_literal(self):
        template = "Header\n{{ /* RECENT_REPOS */ }}\n{{ /* RECENT_STARS */ }}\nFooter"
        result = renderer.render(template, {
            "RECENT_REPOS": ['{{ /* RECENT_STARS */ }} {{ dangerous }}'],
            "RECENT_STARS": ["a star"],
        })
        self.assertEqual(result, "Header\n{{ /* RECENT_STARS */ }} {{ dangerous }}\na star\nFooter")

    def test_empty_section_says_so(self):
        self.assertEqual(renderer.render("{{ /* RECENT_STARS */ }}", {"RECENT_STARS": []}),
                         "- Nothing yet.")

    def test_waka_section_survives_rerender(self):
        fresh = "a\n<!--START_SECTION:waka-->\nplaceholder\n<!--END_SECTION:waka-->\nb"
        old = "x\n<!--START_SECTION:waka-->\nPython 3 hrs\n<!--END_SECTION:waka-->\ny"
        self.assertEqual(renderer.keep_sections(fresh, old),
                         "a\n<!--START_SECTION:waka-->\nPython 3 hrs\n<!--END_SECTION:waka-->\nb")
        self.assertEqual(renderer.keep_sections(fresh, ""), fresh)

    def test_missing_or_duplicate_marker_fails(self):
        for template in ["", "{{ /* RECENT_REPOS */ }}" * 2]:
            with self.assertRaises(ValueError):
                renderer.render(template, {"RECENT_REPOS": []})

    @patch.object(renderer.time, "sleep")
    @patch.object(renderer.subprocess, "run")
    def test_transient_failure_retries(self, run, sleep):
        run.side_effect = [subprocess.CalledProcessError(1, "gh"),
                           subprocess.CompletedProcess("gh", 0, json.dumps({"ok": True}))]
        self.assertEqual(renderer.api(["test"]), {"ok": True})
        self.assertEqual(run.call_count, 2)
        sleep.assert_called_once_with(5)

    @patch.object(renderer.time, "sleep")
    @patch.object(renderer.subprocess, "run")
    def test_persistent_failure_is_not_silenced(self, run, sleep):
        run.side_effect = subprocess.TimeoutExpired("gh", 60)
        with self.assertRaisesRegex(RuntimeError, "after 3 attempts"):
            renderer.api(["test"])
        self.assertEqual(run.call_count, 3)

    @patch.object(renderer.time, "sleep")
    @patch.object(renderer.subprocess, "run")
    def test_graphql_errors_are_not_partial_success(self, run, sleep):
        run.return_value = subprocess.CompletedProcess("gh", 0, '{"errors": [{}], "data": {}}')
        with self.assertRaises(RuntimeError):
            renderer.api(["graphql"])


if __name__ == "__main__":
    unittest.main()
