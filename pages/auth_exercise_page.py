from playwright.sync_api import Page, expect

class AuthExercisePage:
    def __init__(self, page: Page):
        self.page = page
        
        # --- Navigasi & Login/Signup Awal ---
        self.home_link = page.get_by_role("link", name=" Home")
        self.signup_login_link = page.get_by_role("link", name=" Signup / Login")
        self.signup_heading = page.get_by_role("heading", name="New User Signup!")
        self.name_input = page.get_by_role("textbox", name="Name")
        self.email_input = page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address")
        self.signup_button = page.get_by_role("button", name="Signup")
        
        # --- Form Pendaftaran Detail (Menggunakan ID Stabil) ---
        self.form_heading = page.get_by_text("Enter Account Information")
        self.mr_radio = page.locator("#id_gender1")
        self.password_input = page.locator("#password")
        self.days_select = page.locator("#days")
        self.months_select = page.locator("#months")
        self.years_select = page.locator("#years")
        
        self.newsletter_checkbox = page.locator("#newsletter")
        self.offers_checkbox = page.locator("#optin")
        
        self.first_name_input = page.locator("#first_name")
        self.last_name_input = page.locator("#last_name")
        self.company_input = page.locator("#company")
        self.address1_input = page.locator("#address1")
        self.address2_input = page.locator("#address2")
        self.country_select = page.locator("#country")
        self.state_input = page.locator("#state")
        self.city_input = page.locator("#city")
        self.zipcode_input = page.locator("#zipcode")
        self.mobile_input = page.locator("#mobile_number")
        self.create_account_button = page.get_by_role("button", name="Create Account")
        
        # --- Status & Pembersihan Akhir ---
        self.account_created_text = page.get_by_text("Account Created!")
        self.account_deleted_text = page.get_by_text("Account Deleted!")
        self.continue_button = page.locator("[data-qa='continue-button']")
        self.delete_account_link = page.get_by_role("link", name=" Delete Account")

    def navigate(self):
        self.page.goto("https://automationexercise.com")
        expect(self.home_link).to_be_visible()

    def go_to_signup(self):
        self.signup_login_link.click()
        expect(self.signup_heading).to_be_visible()

    def submit_initial_signup(self, name: str, email: str):
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.signup_button.click()
        self.page.wait_for_url("**/signup")
        expect(self.form_heading).to_be_visible()

    def fill_account_details(self, password: str, day: str, month: str, year: str):
        self.mr_radio.check()
        self.password_input.fill(password)
        self.days_select.select_option(day)
        self.months_select.select_option(month)
        self.years_select.select_option(year)
        self.newsletter_checkbox.check()
        self.offers_checkbox.check()

    def fill_address_details(self, first: str, last: str, company: str, addr1: str, addr2: str, country: str, state: str, city: str, zip_code: str, mobile: str):
        self.first_name_input.fill(first)
        self.last_name_input.fill(last)
        self.company_input.fill(company)
        self.address1_input.fill(addr1)
        self.address2_input.fill(addr2)
        self.country_select.select_option(country)
        self.state_input.fill(state)
        self.city_input.fill(city)
        self.zipcode_input.fill(zip_code)
        self.mobile_input.fill(mobile)
        self.create_account_button.click()

    def verify_and_continue_registration(self, username: str):
        expect(self.account_created_text).to_be_visible()
        self.continue_button.click()
        if "id=google_ads" in self.page.url:
            self.page.goto("https://automationexercise.com")
        expect(self.page.get_by_text(f"Logged in as {username}")).to_be_visible()

    def clean_up_account(self):
        self.delete_account_link.click()
        expect(self.account_deleted_text).to_be_visible()
        self.continue_button.click()
