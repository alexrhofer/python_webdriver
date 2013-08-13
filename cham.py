from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime as dt
from array import *
import random
import unittest
import time

# Yes, I know I could refactor this much better...
#  - dx
class Playtime(unittest.TestCase):

    def setUp(self):

        # Create driver and driver2, TOGGLE CHROME OR FIREFOX!
        self.driver = webdriver.Firefox()
        self.driver2 = webdriver.Firefox()

    def test_1(self):

        # TOGGLE THIS, TO PHASE 1.3.4 OR NOT TO PHASE 1.3.4
        is_onedotthreedotfour = True # Default to False
        # TOGGLE THIS, TO GERMAN OR NOT TO GERMAN
        is_german = False # Default to False

        # Variables
        my_first_name = 'dee'
        my_last_name = 'xio'
        my_password = 'asdfasdf'
        my_email = "" # Default my_email to blank
        my_address1 = '12345 Fake St'
        my_city = 'Fakesville'
        my_state = 'MN'
        my_zip = '55555'
        my_phone = '555-555-5555'
        my_url = [] # Default my_url to blank
        my_country = [] # Default my_url to blank
        selected_country = "N/A" # Default to None

        # Determine if Phase 1.3.4, or not, based on Toggle above and set my_url
        if is_onedotthreedotfour:
            my_url = ['http://www.myliftmaster.com/', \
                'http://www.myliftmaster.eu/', \
                'http://www.mychamberlain.com/', \
                'http://www.mychamberlain.eu/'] # Phase 1.3.4 Site URLs
            # Determine if German, or not, based on Toggle above and set my_country
            if is_german:
                my_country = ['Belgien', 'Deutschland', 'Frankreich', u'Gro\u00DFbritannien', 'Italien', 'Kanada', \
                    'Mexiko', 'Niederlande', 'Spanien', 'Vereinigte Staaten von Amerika'] # Set to German values
            else:
                my_country = ['Belgium', 'Canada', 'France', 'Germany', 'Italy', 'Mexico', \
                    'Netherlands', 'Spain', 'United Kingdom', 'United States'] # Set to English values
        else:
            my_url = ['http://www.myliftmaster.com/'] # Phase 1.3.4

        # Print out Toggles above.
        print "\n**** INITIALIZING TESTS FOR: Phase 1.3.4 == " + str(is_onedotthreedotfour) + \
            " AND German == " + str(is_german) + " ****\n"

        # Loop for each url
        for i in range(len(my_url)):
            # Create driver and open page
            driver = self.driver
            driver.get(my_url[i])

            # Change site to German, if is_german is true
            #  Need try block, in case site is already set to German
            if is_german:
                try:
                    driver.find_element_by_xpath("//a[text()='German']").click()
                except NoSuchElementException:
                    driver.find_element_by_xpath("//a[text()='Deutsch']").click()

            # Click Sign Up/Registrieren link
            time.sleep(2)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'username')))
            driver.find_element_by_class_name("btn-action-alt").click()

            # Fill out some information on the first page of registration
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'new_first_name')))
            driver.find_element_by_id('new_first_name').send_keys(my_first_name)
            driver.find_element_by_id('new_last_name').send_keys(my_last_name)
            driver.find_element_by_id('new_password').send_keys(my_password)
            driver.find_element_by_id('new_password_verify').send_keys(my_password)
            # Set Country dropdown to random my_country (this only applies to Phase 1.3.4, 
            #  since 1.3.3 does not have this feature)
            if is_onedotthreedotfour:
                random_num = random.randint(0, 9)
                selected_country = my_country[random_num]
                countryOption = Select(driver.find_element_by_id('new_country_code'))
                countryOption.select_by_visible_text(selected_country)

            # Create new driver to handle getting e-mails from www.mintemail.com
            driver2 = self.driver2
            driver2.get('http://www.mintemail.com/')
            WebDriverWait(driver2, 20).until(EC.visibility_of_element_located((By.ID, 'emailaddress')))

            # Grab my_email from the second browser
            my_email = driver2.find_element_by_id('emailaddress').text.split()[0]
            if is_onedotthreedotfour:
                print ' The site being tested is: ' + my_url[i] + " at " + dt.now().strftime("%d/%m, %H:%M:%S") + \
                    '\n The email being tested is: ' + my_email + "\n The Country selection is set to: " + \
                    selected_country
            else:
                print ' The site being tested is: ' + my_url[i] + " at " + dt.now().strftime("%d/%m, %H:%M:%S") + \
                    '\n The email being tested is: ' + my_email

            # Add my_email to the form
            driver.find_element_by_id('new_email').send_keys(my_email)
            # Check the terms box and hit the next button
            driver.find_element_by_id('terms_check').click()
            time.sleep(2)
            if is_german:
                driver.find_element_by_xpath("//a[text()='Weiter']").click()
            else:
                driver.find_element_by_xpath("//a[text()='Next']").click()

            # Setting to the location of the activation links
            activation_link = "//a[text()='Click here to complete your registration.']"
            # Need the u character for the non-unicode character in the string
            activation_link_german = u"//a[text()='Klicken Sie hier, um Ihre Registrierung abzuschlie\u00DFen.']"

            # Wait for the activation link to appear and copy it, then quit the browser
            if is_german:
                WebDriverWait(driver2, 300).until(EC.visibility_of_element_located((By.XPATH, activation_link_german)))
                activation_url = driver2.find_element_by_xpath(activation_link_german).get_attribute('href')
            else:
                WebDriverWait(driver2, 300).until(EC.visibility_of_element_located((By.XPATH, activation_link)))
                activation_url = driver2.find_element_by_xpath(activation_link).get_attribute('href')

            # Change URL so it goes to Staging server of 'stg3www'. Only needed if URL is not pointing to correct server...
            #  To debug, print out pre-change URL
            print ' Activation URL: ' + activation_url
            if 'dev' in activation_url:
                param_url, value_url = activation_url.split('dev',1)
                activation_url = 'http://' + value_url
                # To debug, print out post-change URL
                print ' Activation URL changed to: ' + activation_url

            # Navigate to the activation URL in the first broswer.
            driver.get(activation_url)

            # Input the password to validate login and hit login
            driver.find_element_by_id('password').send_keys(my_password)
            driver.find_element_by_id('registerLoginSubmit').click()

            # Fill out the rest of the information on the info field
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'address1')))
            driver.find_element_by_id('address1').send_keys(my_address1)
            driver.find_element_by_id('city').send_keys(my_city)
            driver.find_element_by_id('state').send_keys(my_state)
            driver.find_element_by_id('zip').send_keys(my_zip)
            driver.find_element_by_id('phone').send_keys(my_phone)
            driver.find_element_by_id('submitUserInfo').click()
            print ' Account [' + my_email + '] has been CREATED successfully.'

            # Bypass activating a gateway and just goto the Users account.
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'js-register-gateway')))
            driver.find_element_by_link_text('Home').click() # Luckily, this link is 'Home' in both languages
            # Navigate back to site (useful for Phase 1.3.4, since sometimes links do not redirect to the same site)
            #driver.get(my_url[i])

            # Log out
            time.sleep(5)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'logoutLink')))
            if is_german:
                driver.find_element_by_xpath("//a[text()='Abmelden']").click()
            else:
                driver.find_element_by_xpath("//a[text()='Logout']").click()

            # Forgot Password [in progress]
            #driver.find_element_by_xpath("//a[text()='Sie haben Ihr Passwort vergessen?']").click()
            #driver.find_element_by_id('email').send_keys(my_email)
            #driver.find_element_by_xpath("//a[text()='Absenden']").click()
            #driver.find_element_by_xpath(u"//a[text()='Gehen Sie zu \u201EAnmelden\"']")

            # Log back in
            time.sleep(5)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'username')))
            driver.find_element_by_id('username').send_keys(my_email)
            driver.find_element_by_id('password').send_keys(my_password)
            if is_german:
                driver.find_element_by_xpath("//a[text()='Anmelden']").click()
            else:
                driver.find_element_by_xpath("//a[text()='Login']").click()

            # Open the User account management modal.
            #  Super pro workaround because I can't click after waiting for it 
            #  because it's there but it does nothing for 5 seconds
            time.sleep(10)
            if is_german:
                user_account = "//a[text()='+ Benutzer bearbeiten']"
            else:
                user_account = "//a[text()='+ Edit User']"
            driver.find_element_by_xpath(user_account).click()

            # Hit the delete button
            time.sleep(2)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'delete')))
            driver.find_element_by_id('delete').click()
            # Confirm deletion
            delete_button  = "//button[@onclick='deleteAccount()']"
            driver.find_element_by_xpath(delete_button).click()
            print " Account [" + my_email + "] has been DELETED successfully."

            # Print out status and time amount, if successful
            print " TEST SUCCESS for " + my_url[i] + "! End time = " + dt.now().strftime("%d/%m, %H:%M:%S") + "\n"

            # Sleep, to allow deletion of account to redirect back to login page
            time.sleep(5)

    def tearDown(self):

        # Close driver and driver2
        self.driver.quit()
        self.driver2.quit()

if __name__ == '__main__':
    unittest.main()