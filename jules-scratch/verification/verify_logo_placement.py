import os
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Get the absolute path to the verification directory
    base_path = os.path.abspath('jules-scratch/verification')

    # Verify login page
    page.goto(f"file://{base_path}/verify_login.html")
    page.screenshot(path="jules-scratch/verification/login_page.png")

    # Verify registration page
    page.goto(f"file://{base_path}/verify_register.html")
    page.screenshot(path="jules-scratch/verification/register_page.png")

    # Verify add machine page
    page.goto(f"file://{base_path}/verify_add_machine.html")
    page.screenshot(path="jules-scratch/verification/add_machine_page.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)