import re
from playwright.sync_api import Page, expect

ticket_code = 'X0VD-CC'

def test_has_title(page: Page):
    # Step 1: Go to the login page
    page.goto('https://live.collisionconf.com/cc24/login/otp')
    
    # Step 2: Fill in the input with id="email"
    page.fill('input#email', ticket_code)
    
    # Step 3: Click a button with the text "Log in"
    page.click('button:has-text("Log in")')
    
    # Step 4: Wait for the button with the text "Verify code" and check if it exists
    verify_button = page.locator('button:has-text("Verify code")')
    expect(verify_button).to_be_disabled()
    
    random_code = 'RANDOM'
    
    # Step 5: Find an input with id="code"
    input_code = page.locator('input#code')
    expect(input_code).to_have_value("")
    
    error_message = 'Verification failed. Please check that the code is correct, or request a new code.'
    
    # Step 6: Get input from the console
    # code = input("Please enter the verification code: ")
    
    # Step 7: Fill in the input with id="code" from the input from the console
    input_code.fill(random_code)
    verify_button.click()
    
    page.wait_for_timeout(5000)
    error_notification = page.locator('.notification__msg')
    expect(error_notification).to_contain_text(error_message)
    # input_code = page.locator('.notification__msg')
    
    