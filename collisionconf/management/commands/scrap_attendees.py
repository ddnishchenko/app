import random
import json
import pandas as pd
from playwright.sync_api import sync_playwright
from asgiref.sync import sync_to_async
from django.utils.translation import gettext_lazy as _
from django.core.management import BaseCommand, CommandError
from collisionconf.models import Person

from ._filter_attendees import filter_persons


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
                # def handle_request(request):
                    # if algolia_url in request.url:  # Replace with a part of the URL you're looking for
                        # self.stdout.write(self.style.HTTP_INFO(f"Captured request: {request.url}"))
                        # print(f"Captured request: {request.url}")
                        # print(f"Request method: {request.method}")
                        # print(f"Request headers: {request.headers}")
                        # print(f"Request post data: {request.post_data}")

                # page.on('request', handle_request)
                
                def handle_response(response):
                    if algolia_url in response.url:  # Replace with a part of the URL you're looking for
                        json_response = response.json()
                        self.stdout.write(self.style.HTTP_INFO(f"Captured response: {response.url}"))
                        print(f"Captured response: {response.url}")
                        print("DATA: ", json_response['results'][0]['hits'])
                        hits = list(json_response['results'][0]['hits'])
                        
                        for hit in hits:
                            print('HIT:', hit)
                            hit_copy = dict(hit)
                            hit_copy['topics'] = json.dumps(hit_copy['topics'])
                            hit_dict = dict()
                            for key, value in key_list.items():
                                for jt in job_titles:
                                    if jt.lower() in hit_copy['job_title'].lower():
                                        attendees_data[key].append(hit_copy[value])
                                        if value == 'id':
                                            hit_dict.update({'object_id': hit_copy[value]})
                                        else:
                                            hit_dict.update({value: hit_copy[value]})
                                        attendees_list.append(hit_dict)
                                        break
                                            
                                            
                                            
                            # self.update_database(hit)
                            # sync_to_async(self.update_database)(hit_copy)
                        # print(f"Request method: {request.method}")
                        # print(f"Request headers: {request.headers}")
                        # print(f"Request post data: {request.post_data}")
                page.on('response', handle_response)
                # Handle request END
                
                
                # search job titles
                
                for job_title in job_titles:
                    page.locator('.search-box__input').fill(job_title)
                    self.stdout.write(self.style.HTTP_INFO(f"Going though: {job_title}"))
                    try:
                        next_button = page.locator('.pagination__button').nth(1)
                        while next_button.is_disabled() is not True:
                            next_button.click()
                            page.wait_for_timeout(random.randint(500, 1000))
                        page.locator('.search-box__input').fill("")
                    except Exception as e:
                        self.stdout.write(self.style.ERROR_OUTPUT(e))

                
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
