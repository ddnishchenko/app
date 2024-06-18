
import random
from playwright.sync_api import sync_playwright

ticket_code = 'X0VD-CC'
roles = ['ALPHA', 'BETA', 'GROWTH', 'Attendee', 'Partner']
induestries = [
    'AI & machine learning',
    'E-commerce & retail',
    'Education',
    'Energy & utilities',
    'Event management',
    'Fintech & financial services',
    'Hardware, robotics & IoT',
    'Healthtech & wellness',
    'Proptech & real estate',
    'SaaS',
    'Telecommunications & IT',
    'Travel & hospitality'
]
locations = [
    'Austria',
    'Australia',
    'Belgium',
    'Canada',
    'Denmark',
    'France',
    'Finland',
    'Germany',
    'Ireland',
    'Netherlands',
    'Norway',
    'Sweden',
    'Switzerland',
    'United Arab Emirates',
    'United Kingdom',
    'United States',
]

job_titles = [
    'Founder',
    'CO-Founder',
    'CTO',
    'CEO',
    'COO',
    'Product Manager',
    'Director of IT',
    'Product Owner',
    'Director of Technology',
    'Director of product',
    'Partner',
]

algolia_url = 'https://x0o1h31a99-dsn.algolia.net/1/indexes/*/queries'

def test_login_and_verify_code():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Step 1: Go to the login page
        page.goto('https://live.collisionconf.com/cc24/login/otp')
        
        # Step 2: Fill in the input with id="email"
        page.fill('input#email', ticket_code)  # Replace with your test email
        
        # Step 3: Click a button with the text "Log in"
        page.click('button:has-text("Log in")')
        
        # Step 4: Wait for the button with the text "Verify code" and check if it exists
        verify_button = page.locator('button:has-text("Verify code")')
        # expect(verify_button).to_be_disabled()
        
        # Step 5: Find an input with id="code"
        input_code = page.locator('input#code')
        
        # Step 6: Get input from the console
        code = input("Please enter the verification code: ")
        
        # Step 7: Fill in the input with id="code" from the input from the console
        input_code.fill(code)
        verify_button.click()
        
        
        
        page.wait_for_url('https://live.collisionconf.com/cc24/attendees')
        
        # Open filters
        page.click('.search-bar__filter-button.popper__activation')
        page.wait_for_timeout(random.randint(800, 1000))
        
        # select roles
        for role in roles:
            page.click(f'.checkbox-control__label:has-text("{role}")')
            page.wait_for_timeout(random.randint(100, 300))
        
        # select industries
        for industry in induestries:
            page.click('#downshift-0-label')
            page.wait_for_timeout(random.randint(100, 200))
            page.click(f'#downshift-0-menu .multi-select__list-item:has-text("{industry}")')
            page.wait_for_timeout(random.randint(100, 300))
        
        # select industries
        for location in locations:
            page.click('#downshift-1-label')
            page.wait_for_timeout(random.randint(100, 200))
            print('Click on: ', location)
            page.click(f'#downshift-1-menu .multi-select__list-item:has-text("{location}")')
            page.wait_for_timeout(random.randint(100, 300))
            
            
        # close filters
        page.wait_for_timeout(random.randint(100, 300))
        page.click('.popper.search-bar__popper .popper__overlay[role="presentation"]', timeout=5000)
        
        # Handle request START
        def handle_request(request):
            if algolia_url in request.url:  # Replace with a part of the URL you're looking for
                print(f"Captured request: {request.url}")
                # print(f"Request method: {request.method}")
                # print(f"Request headers: {request.headers}")
                # print(f"Request post data: {request.post_data}")

        page.on('request', handle_request)
        
        def handle_response(response):
            if algolia_url in response.url:  # Replace with a part of the URL you're looking for
                json_response = response.json()
                print(f"Captured response: {response.url}")
                print(f"Captured response data: ", json_response)
                print('Info about response: ')
                print(type(json_response))
                print(dir(json_response))
                hits = json_response['results'][0]['hits']
                for hit in hits:
                    pass
                # print(f"Request method: {request.method}")
                # print(f"Request headers: {request.headers}")
                # print(f"Request post data: {request.post_data}")
        page.on('response', handle_response)
        # Handle request END
            
        # search job titles
        index = 0
        for job_title in job_titles:
            page.locator('.search-box__input').fill(job_title)
            print('Going though: ', job_title)
            next_button = page.locator('.pagination__button').nth(1)
            if index > 3:
                break
            while next_button.is_disabled() is not True:
                next_button.click()
                page.wait_for_timeout(random.randint(500, 1000))
                index = index + 1
            page.locator('.search-box__input').fill("")

        
        stop_input = ''
        while stop_input != 'stop':
            stop_input = input('Enter "stop": ')
        page.wait_for_timeout(20000)
        browser.close()


test_login_and_verify_code()