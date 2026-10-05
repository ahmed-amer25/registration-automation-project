import time
import random
from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class RegisterPage:
    def __init__(self, driver):
        self.driver = driver
        self.fake = Faker()
        self.wait = WebDriverWait(driver, 20)

    # Locators
    CREATE_ACCOUNT_LINK = (By.XPATH, "//a[contains(@href, '/register') or contains(text(), 'حساب') or contains(text(), 'Create')]")
    CLINIC_IMAGE = (By.XPATH, "//img[@alt='clinic image']")

    UNIFIED_NUMBER_INPUT = (By.XPATH, "//input[contains(@placeholder, '7X') or contains(@placeholder, '7')]")
    EMAIL_INPUT = (By.XPATH, "//input[@type='email' or contains(@placeholder, 'example')]")
    PHONE_INPUT = (By.XPATH, "//input[@aria-describedby='phone-help' or contains(@placeholder, 'XX-XXX-XXXX')]")
    NATIONAL_ID_INPUT = (By.XPATH, "//input[contains(@placeholder, '1X') or contains(@placeholder, '1')]")
    VERIFY_SUBMIT_BUTTON = (By.XPATH, "//button[contains(., 'متابعة') or contains(., 'Continue')]")

    # Step 3 (OTP) & Post-OTP Modal Locators
    OTP_INPUTS = (By.XPATH, "//input[contains(@class, 'p-inputotp-input')]")
    OTP_SUBMIT_BUTTON = (By.XPATH, "//button[contains(., 'التحقق والمتابعة') or contains(., 'Verify')]")
    COMPLETE_INFO_MODAL_BTN = (By.XPATH, "//button[contains(., 'Complete your information') or contains(., 'إكمال البيانات') or contains(., 'متابعة')]")

    # Step 4 (Signature) Locators
    SIGNATURE_CANVAS = (By.XPATH, "//canvas")
    SAVE_SIGNATURE_BTN = (By.XPATH, "//button[.//span[text()='Save'] or contains(., 'Save') or contains(., 'حفظ')]")
    CONTINUE_TO_AGREEMENT_BTN = (By.XPATH, "//button[@aria-label='Continue to Agreement' or contains(., 'Continue to Agreement') or contains(., 'المتابعة للاتفاقية')]")

    # Step 5 (Agreements) Locators
    AGREEMENT_SIGN_BTN = (By.XPATH, "//button[@aria-label='Sign & Approve Agreement' or contains(., 'Sign & Approve Agreement') or contains(., 'التوقيع والموافقة')]")
    
    # Steps 6, 7 Locators
    CONTRACT_PROCEED_BTN = (By.XPATH, "//button[@aria-label='Proceed to Contract' or contains(., 'Proceed to Contract') or contains(., 'المتابعة للعقد')] | //*[self::button or self::a][contains(., 'Proceed to Contract')]")
    DASHBOARD_BTN = (By.XPATH, "//*[@aria-label='Go to Dashboard' or contains(., 'Go to Dashboard') or contains(., 'الانتقال إلى لوحة التحكم')]")

    # Final Auth Modal Locator
    LOGOUT_MODAL_BTN = (By.XPATH, "//button[contains(., 'تسجيل الخروج') or contains(., 'Logout')] | //a[contains(., 'تسجيل الخروج')]")

    # Generators
    def generate_unified_number(self):
        return "7" + "".join([str(random.randint(0, 9)) for _ in range(9)])

    def generate_saudi_phone(self):
        valid_second_digits = ["0", "3", "4", "5", "6", "7", "8", "9"]
        second_digit = random.choice(valid_second_digits)
        rest_of_digits = "".join([str(random.randint(0, 9)) for _ in range(7)])
        return "5" + second_digit + rest_of_digits

    def generate_national_id(self):
        return "1" + "".join([str(random.randint(0, 9)) for _ in range(9)])

    # Helper Action for Safe Click
    def safe_click(self, locator, timeout=20):
        element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(1)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    # Actions
    def open_page(self, url):
        self.driver.get(url)

    def click_create_account(self):
        self.safe_click(self.CREATE_ACCOUNT_LINK)

    def select_clinic_and_proceed(self):
        self.safe_click(self.CLINIC_IMAGE)

    def fill_registration_form(self):
        unified_num = self.generate_unified_number()
        email = self.fake.email()
        phone = self.generate_saudi_phone()
        national_id = self.generate_national_id()

        self.wait.until(EC.presence_of_element_located(self.UNIFIED_NUMBER_INPUT)).send_keys(unified_num)
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)

        phone_field = self.wait.until(EC.presence_of_element_located(self.PHONE_INPUT))
        phone_field.clear()
        phone_field.send_keys(phone)

        self.driver.find_element(*self.NATIONAL_ID_INPUT).send_keys(national_id)

        return {
            "unified_num": unified_num,
            "email": email,
            "phone": phone,
            "national_id": national_id,
        }

    def click_verify_and_submit(self):
        self.safe_click(self.VERIFY_SUBMIT_BUTTON)

    def enter_otp_and_submit(self, otp_code="1234"):
        inputs = self.wait.until(EC.presence_of_all_elements_located(self.OTP_INPUTS))
        for i, digit in enumerate(otp_code):
            self.driver.execute_script(
                "arguments[0].value = arguments[1];"
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
                "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
                inputs[i], digit
            )
        self.safe_click(self.OTP_SUBMIT_BUTTON)
        time.sleep(2)

    def click_complete_your_information(self):
        self.safe_click(self.COMPLETE_INFO_MODAL_BTN)
        time.sleep(1.5)

    def draw_signature(self):
        canvas = self.wait.until(EC.presence_of_element_located(self.SIGNATURE_CANVAS))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", canvas)
        time.sleep(1)

        actions = ActionChains(self.driver)
        actions.move_to_element(canvas)\
               .click_and_hold()\
               .move_by_offset(80, 0)\
               .move_by_offset(0, 40)\
               .move_by_offset(-80, 0)\
               .release()\
               .perform()

        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));"
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
            canvas
        )
        time.sleep(1.5)

    def click_save_signature(self):
        save_btn = self.wait.until(EC.presence_of_element_located(self.SAVE_SIGNATURE_BTN))
        self.driver.execute_script("arguments[0].click();", save_btn)
        time.sleep(2)

    def click_proceed_to_agreement(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        btn = self.wait.until(EC.presence_of_element_located(self.CONTINUE_TO_AGREEMENT_BTN))
        self.driver.execute_script("""
            var el = arguments[0];
            el.removeAttribute('disabled');
            el.classList.remove('disabled:opacity-50', 'disabled:cursor-not-allowed', 'disabled:pointer-events-none');
            el.click();
        """, btn)
        time.sleep(2)

    def click_sign_agreement(self):
        self.driver.execute_script("""
            var containers = document.querySelectorAll('div, iframe');
            containers.forEach(c => { if(c.scrollHeight > c.clientHeight) c.scrollTop = c.scrollHeight; });
            window.scrollTo(0, document.body.scrollHeight);
        """)
        time.sleep(1.5)

        clicked = self.driver.execute_script("""
            var btn = document.querySelector('button[aria-label="Sign & Approve Agreement"]') || 
                      Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Sign & Approve'));
            if (btn) {
                btn.removeAttribute('disabled');
                btn.classList.remove('disabled:opacity-50', 'disabled:cursor-not-allowed', 'disabled:pointer-events-none');
                btn.click();
                return true;
            }
            return false;
        """)

        if not clicked:
            try:
                btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.AGREEMENT_SIGN_BTN))
                self.driver.execute_script("arguments[0].click();", btn)
            except Exception:
                pass
        time.sleep(2)

    def click_proceed_to_contract(self):
        self.driver.execute_script("""
            var containers = document.querySelectorAll('div, iframe');
            containers.forEach(c => { if(c.scrollHeight > c.clientHeight) c.scrollTop = c.scrollHeight; });
            window.scrollTo(0, document.body.scrollHeight);
        """)
        time.sleep(1.5)

        clicked = self.driver.execute_script("""
            var btn = document.querySelector('button[aria-label="Proceed to Contract"]') || 
                      Array.from(document.querySelectorAll('button, a')).find(b => b.innerText && b.innerText.includes('Proceed to Contract'));
            if (btn) {
                btn.removeAttribute('disabled');
                btn.classList.remove('disabled:opacity-50', 'disabled:cursor-not-allowed', 'disabled:pointer-events-none');
                btn.click();
                return true;
            }
            return false;
        """)

        if not clicked:
            try:
                btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CONTRACT_PROCEED_BTN))
                self.driver.execute_script("arguments[0].click();", btn)
            except Exception:
                pass
        time.sleep(2)

    def click_go_to_dashboard(self):
        # 1. نزول اسكروال تدريجي وبطيء في الشاشة 7 لرؤية بنود العقد بالكامل
        for i in range(1, 5):
            self.driver.execute_script(f"window.scrollTo(0, (document.body.scrollHeight / 4) * {i});")
            time.sleep(0.8)

        self.driver.execute_script("""
            var containers = document.querySelectorAll('div, iframe');
            containers.forEach(c => { if(c.scrollHeight > c.clientHeight) c.scrollTop = c.scrollHeight; });
        """)
        time.sleep(2)

        # 2. النقر على زر Go to Dashboard
        clicked = self.driver.execute_script("""
            var elements = Array.from(document.querySelectorAll('button, a, span, div[role="button"]'));
            var target = elements.find(el => 
                (el.getAttribute('aria-label') && el.getAttribute('aria-label').includes('Dashboard')) ||
                (el.innerText && (el.innerText.includes('Go to Dashboard') || el.innerText.includes('لوحة التحكم')))
            );
            
            if (target) {
                var btn = target.closest('button') || target.closest('a') || target;
                btn.removeAttribute('disabled');
                btn.classList.remove('disabled:opacity-50', 'disabled:cursor-not-allowed', 'disabled:pointer-events-none');
                btn.click();
                return true;
            }
            return false;
        """)

        if not clicked:
            try:
                btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.DASHBOARD_BTN))
                self.driver.execute_script("arguments[0].click();", btn)
            except Exception:
                pass

        time.sleep(3)

    def click_logout_from_modal(self):
        try:
            self.safe_click(self.LOGOUT_MODAL_BTN, timeout=5)
            time.sleep(2)
        except Exception:
            pass