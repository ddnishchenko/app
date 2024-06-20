import random
import json
import pandas as pd
from playwright.sync_api import sync_playwright
from django.utils.translation import gettext_lazy as _
from django.core.management import BaseCommand, CommandError
from collisionconf.models import Person


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


class Command(BaseCommand):
    """
    Description
    """
    help = _("scrap_attend <ticket>")

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "ticket",
            help=_('Ticket code'),
            nargs="+",
            type=str
        )
        """ 
        parser.add_argument(
            "location",
            help=_("Location name city or country, for example: san-francisco, new-york, chicago. Special is remote"),
            nargs="+",
            type=str
        )

        parser.add_argument(
            "--page",
            help=_("page number in the search query"),
            nargs="+",
            type=int
        )

        parser.add_argument(
            "--api-key",
            help=_("Scraply API key"),
            nargs="+",
            type=str
        ) """
    
    def update_database(self, hit_copy):
        Person.objects.update_or_create(
            object_id=hit_copy['object_id'],
            person_id=hit_copy['person_id'],
            first_name=hit_copy['first_name'],
            last_name=hit_copy['last_name'],
            country=hit_copy['country'],
            city=hit_copy['city'],
            job_title=hit_copy['job_title'],
            industry=hit_copy['industry'],
            company_name=hit_copy['company_name'],
            pronoun=hit_copy['pronoun'],
            role=hit_copy['role'],
            topics=hit_copy['topics'],
            bio=hit_copy['bio'],
            defaults=hit_copy
        )

    def handle(self, *args, **options):
        print(options)
        ticket = options.get('ticket')[0]
        if not ticket:
            raise CommandError("ticket is required")
        # filter_persons()
        # return None
        try:
            self.stdout.write(self.style.HTTP_INFO("Start scrapping:"))
            self.stdout.write(self.style.HTTP_INFO(f"Ticket ID: {ticket}"))
            key_list = {
                'Object ID': 'id',
                'Person ID': 'person_id',
                'First name': 'first_name',
                'Last name': 'last_name',
                'Country': 'country',
                'City': 'city',
                'Job title': 'job_title',
                'Industry': 'industry',
                'Company name': 'company_name',
                'Pronoun': 'pronoun',
                'Role': 'role',
                'Topics': 'topics',
                'Bio': 'bio',
            }
            attendees_data = {
                    'Object ID': [],
                    'Person ID': [],
                    'First name': [],
                    'Last name': [],
                    'Country': [],
                    'City': [],
                    'Job title': [],
                    'Industry': [],
                    'Company name': [],
                    'Pronoun': [],
                    'Role': [],
                    'Topics': [],
                    'Bio': [],
                }
                
            attendees_list = list()
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
                self.stdout.write(self.style.HTTP_INFO("Enter the verification code from the tickets email:"))
                code = input("Please enter the verification code: ")
                
                # Step 7: Fill in the input with id="code" from the input from the console
                input_code.fill(code)
                verify_button.click()
                
                page.wait_for_url('https://live.collisionconf.com/cc24/attendees')
                
                # Step 8: Load all persons
                persons = Person.objects.all()
                
                # Step 8.1: Loop thought persons
                for person in persons:
                    # Step 9: Search for a person
                    page.locator('.search-box__input').fill(f'{person.first_name} {person.last_name}')
                    page.wait_for_timeout(random.randint(300, 500))
                    
                    # Step 10: Navigate to a person detail
                    search_result = page.locator('.directory-list.attendee-list .attendee-item.directory-item.card.-link .li-link')
                    if search_result.count() > 0:
                        search_result.first.click()
                        page.wait_for_timeout(random.randint(300, 500))
                    else:
                        continue
                    
                    # Step 11: Check if connected
                    connected_button = page.query_selector('.sc-gueYoa.dzmqOl')
                    pending_button = page.query_selector('.sc-gueYoa.cllBLh')
                    connect_button = page.query_selector('.sc-gueYoa.ffGAmT.sc-dmqHEX.eydzYY')
                    if connected_button is not None or pending_button is not None:
                        # Step 11.1: Navigate to search page
                        page.locator('.btn.-invisible.-svg[href="/cc24/attendees"]')
                        page.wait_for_url('https://live.collisionconf.com/cc24/attendees')
                        continue
                    else:
                        # Step 12: If not connected -> send connect and write message and open conversation, otherwise go back to the next person to search page and repeat 9-12
                        page.wait_for_timeout(random.randint(300, 500))
                        connect_button.click()
                        page.locator('.sc-gueYoa.ffGAmT.sc-dmqHEX.eydzYY').click() # click on send request button in modal
                        page.wait_for_timeout(random.randint(300, 500))
                        chat_button = page.locator('.sc-gueYoa.ffGAmT')
                        page.wait_for_timeout(random.randint(300, 500))
                        chat_button.click() # Navigate to chat
                        page.wait_for_timeout(random.randint(1000, 2000))
                        message_field = page.locator('.chat-form.-textarea textarea')
                        # add logic for choosing a message depends on the person's industry
                        message_field.fill('Message to industry')
                        page.wait_for_timeout(random.randint(300, 500))
                        # Step 13: In conversation check if there is no messaged had been sent, send a message, otherwise go back to the next person to search page and repeat 9-13
                        send_button = page.locator('.chat-form.-textarea button[type="submit"]')
                        send_button.click()
                        page.wait_for_timeout(random.randint(300, 500))
                        # Go to search page
                        page.locator('.btn.-invisible.-svg[href="/cc24/attendees"]')
                        page.wait_for_url('https://live.collisionconf.com/cc24/attendees')


                stop_input = ''
                while stop_input != 'stop':
                    stop_input = input('Enter "stop": ')
                page.wait_for_timeout(5000)
                self.stdout.write(self.style.HTTP_INFO("Scraping data from browser is finished."))    
                
                browser.close()
            
            
            print('attendees_list: ', len(attendees_list))
            df = pd.DataFrame(attendees_data)
            # df.to_csv('output.csv', index=False)
            df.to_excel('output.xlsx', sheet_name='Attendees', index=False)
            
            self.stdout.write(self.style.HTTP_INFO("Start to save data to database."))
            for attendee in attendees_list:
                self.update_database(attendee)
            
            self.stdout.write(self.style.HTTP_INFO("Data saved to database."))

            # self.stdout.write(self.style.HTTP_INFO("It will be scrapped pages {} in total by this query".format(0)))
            
        except Exception as e:
            raise CommandError(e)
        
        self.stdout.write(self.style.SUCCESS("Everything is scrapped and stored in database"))
