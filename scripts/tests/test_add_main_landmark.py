#!/usr/bin/env python3
"""
Tests for scripts/add_main_landmark.py

Verifies the HTMLParser-based implementation correctly handles:
- Basic case: standard <div id="content"> gets role="main"
- Idempotency: re-running is a no-op
- The >-in-attribute edge case (the bug the regex version had)
- Files without #content are skipped
- Files already having role="main" are skipped

Run: python3 scripts/tests/test_add_main_landmark.py
"""
import sys
import tempfile
import unittest
from pathlib import Path

# Make the script importable via direct file path (no __init__.py needed)
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "add_main_landmark",
    Path(__file__).parent.parent / "add_main_landmark.py"
)
assert _spec is not None and _spec.loader is not None
add_main_landmark = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(add_main_landmark)
process_file = add_main_landmark.process_file


class TestAddMainLandmark(unittest.TestCase):

    def _write_and_process(self, html: str, dry_run: bool = False) -> str:
        """Write html to a temp file, process it, return new content."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html)
            tmp = Path(f.name)
        try:
            process_file(tmp, dry_run=dry_run)
            return tmp.read_text()
        finally:
            tmp.unlink()

    def test_basic_addition(self):
        """Standard case: <div id="content"> gets role="main" added."""
        before = '<html><body><div id="content">Hi</div></body></html>'
        after = self._write_and_process(before)
        self.assertIn('id="content" role="main"', after)
        self.assertIn('Hi', after)

    def test_idempotent(self):
        """Re-running on already-modified file is a no-op."""
        before = '<html><body><div id="content" role="main">Hi</div></body></html>'
        after = self._write_and_process(before)
        self.assertEqual(before, after)

    def test_gt_in_attribute(self):
        """The bug case: data-foo='>' should not malform the tag."""
        before = '''<html><body>
<div id="content" class="site-content" data-foo=">">Content</div>
</body></html>'''
        after = self._write_and_process(before)
        self.assertIn('data-foo=">"', after)
        self.assertIn('role="main"', after)
        self.assertIn('Content', after)
        self.assertNotIn('data-foo=" role=', after, "Regex bug regression: data attribute broken")

    def test_no_content_div(self):
        """Files without id='content' are skipped."""
        before = '<html><body><div class="other">Content</div></body></html>'
        after = self._write_and_process(before)
        self.assertEqual(before, after)
        self.assertNotIn('role="main"', after)

    def test_other_role_preserved(self):
        """Tags with non-main roles should not get role=main added."""
        before = '<html><body><div id="content" role="navigation">Nav</div></body></html>'
        after = self._write_and_process(before)
        self.assertIn('role="navigation"', after)

    def test_dry_run_does_not_write(self):
        """--dry-run flag should report change but not modify the file."""
        before = '<html><body><div id="content">Hi</div></body></html>'
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(before)
            tmp = Path(f.name)
        try:
            modified = process_file(tmp, dry_run=True)
            after = tmp.read_text()
            self.assertTrue(modified, "dry_run should report modified=True")
            self.assertEqual(before, after, "dry_run should NOT write changes")
        finally:
            tmp.unlink()

    def test_class_id_order_preserved(self):
        """The order of attributes should be preserved exactly."""
        before = '<div class="site-content" id="content">X</div>'
        after = self._write_and_process(before)
        self.assertRegex(after, r'class="site-content"\s+id="content"\s+role="main"')

    def test_real_world_sample(self):
        """Use an actual pattern from the AOT mirror site."""
        before = '<html><body><div id="page" class="hfeed site">\n  <div id="content" class="site-content">\n    <p>Hello</p>\n  </div>\n</div></body></html>'
        after = self._write_and_process(before)
        self.assertIn('id="content" class="site-content" role="main"', after)
        self.assertIn('<p>Hello</p>', after)


if __name__ == '__main__':
    unittest.main(verbosity=2)