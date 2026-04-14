import unittest
import os
from playwright.sync_api import sync_playwright

class TestYearCardToggle(unittest.TestCase):
    def setUp(self):
        # We need absolute path for the script.js since we might run from another dir
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.script_path = os.path.join(base_dir, 'script.js')

    def test_toggle_expanded_class(self):
        """
        Tests that the 'expanded' class is correctly toggled on '.year-card'
        elements when their '.year-card-header' is clicked.
        Also verifies the first '.year-card' is expanded by default.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            with open(self.script_path, "r") as f:
                js_content = f.read()

            # Mocked DOM
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head></head>
            <body>
                <div class="year-card" id="card1">
                    <div class="year-card-header">2023</div>
                    <div class="year-card-content">Content 2023</div>
                </div>
                <div class="year-card" id="card2">
                    <div class="year-card-header">2022</div>
                    <div class="year-card-content">Content 2022</div>
                </div>
                <!-- Include a rogue card without header to ensure it doesn't break -->
                <div class="year-card" id="card3">
                    No header here
                </div>
                <script>
                    {js_content}
                </script>
            </body>
            </html>
            """

            page.set_content(html_content)

            card1 = page.locator('#card1')
            header1 = card1.locator('.year-card-header')

            card2 = page.locator('#card2')
            header2 = card2.locator('.year-card-header')

            # card1 should be expanded by default (script.js adds 'expanded' to the first .year-card)
            self.assertIn("expanded", card1.get_attribute("class") or "")

            # card2 should not be expanded initially
            self.assertNotIn("expanded", card2.get_attribute("class") or "")

            # Action: Toggle card1
            header1.click()
            # Verification: card1 should no longer be expanded
            self.assertNotIn("expanded", card1.get_attribute("class") or "")

            # Action: Toggle card2
            header2.click()
            # Verification: card2 should now be expanded
            self.assertIn("expanded", card2.get_attribute("class") or "")

            # Action: Toggle card1 back
            header1.click()
            # Verification: card1 should be expanded again
            self.assertIn("expanded", card1.get_attribute("class") or "")

            browser.close()

if __name__ == '__main__':
    unittest.main()
