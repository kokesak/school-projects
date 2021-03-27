from behave import *
import random

@given('user is not logged in')
def step_impl(context):
    context.browser.get("http://pat.fit.vutbr.cz:8066/")
    context.browser.find_element_by_xpath("//div[@id='top-links']/ul/li[2]/a/span").click()
    try:
        context.browser.find_element_by_xpath("//a[contains(text(),'Logout')]").click()
    except:
        pass

@given('web browser is at "Register Account" page')
def step_impl(context):
    context.browser.get("http://pat.fit.vutbr.cz:8066/index.php?route=account/register")

@when('user fills out correctly all required informations')
def step_impl(context):
    context.browser.find_element_by_xpath("//input[@id='input-firstname']").send_keys("Jan")

    context.browser.find_element_by_xpath("//input[@id='input-lastname']").send_keys("Novak")

    random_number = random.randint(1, 99999)
    context.browser.find_element_by_xpath("//input[@id='input-email']").send_keys("jannovak" + str(random_number) + "@seznam.cz")

    context.browser.find_element_by_xpath("//input[@id='input-telephone']").send_keys("123456789")

    context.browser.find_element_by_xpath("//input[@id='input-address-1']").send_keys("Nova")

    context.browser.find_element_by_xpath("//input[@id='input-city']").send_keys("Brno")

    context.browser.find_element_by_xpath("//input[@id='input-postcode']").send_keys("42000")

    context.browser.find_element_by_xpath("//select[@id='input-zone']").click()
    context.browser.find_element_by_xpath("//option[@value='3513']").click()

    context.browser.find_element_by_xpath("//input[@id='input-password']").send_keys("StrongPassword")

    context.browser.find_element_by_xpath("//input[@id='input-confirm']").send_keys("StrongPassword")

@when('user marks the "Privacy Policy" checkbox')
def step_impl(context):
    context.browser.find_element_by_xpath("//form/div/div/input").click()
    context.browser.find_element_by_xpath("//form/div/div/input[2]").click()

@then('user\'s account is succesfully created')
def step_impl(context):
    context.browser.find_element_by_xpath("//*[contains(text(), 'Congratulations! Your new account has been successfully created!')]")

@when('user leavs the "Privacy Policy" checkbox empty')
def step_impl(context):
    context.browser.find_element_by_xpath("//form/div/div/input[2]").click()

@then('user\'s account is not created')
def step_impl(context):
    context.browser.find_element_by_xpath("//*[contains(text(), 'Warning: You must agree to the Privacy Policy!')]")

@given('user is logged in')
def step_impl(context):
    context.execute_steps(u'''
        given user is not logged in
         and web browser is at "Login" page
         when user fills out correct login credentials
    ''')

@when('user clicks "Logout" under "My Account" button')
def step_impl(context):
    context.browser.find_element_by_xpath("//div[@id='top-links']/ul/li[2]/a/span").click()
    context.browser.find_element_by_xpath("//a[contains(text(),'Logout')]").click()

@then('user is successfully logged out')
def step_impl(context):
    context.browser.find_element_by_xpath("//*[contains(text(), 'You have been logged off your account.')]")

@given('web browser is at "Login" page')
def step_impl(context):
    context.browser.get("http://pat.fit.vutbr.cz:8066/index.php?route=account/login")

@when('user fills out correct login credentials')
def step_impl(context):
    context.browser.find_element_by_xpath("//input[@id='input-email']").send_keys("test@test.cz")
    context.browser.find_element_by_xpath("//input[@id='input-password']").send_keys("test")
    context.browser.find_element_by_xpath("//div[@id='content']/div/div[2]/div/form/input").click()

@then('user is successfully logged in')
def step_impl(context):
    context.browser.find_element_by_xpath("//a[contains(text(),'Edit your account information')]")

@given('web browser is at "Edit your account information" page')
def step_impl(context):
    context.browser.get("http://pat.fit.vutbr.cz:8066/index.php?route=account/edit")

@when('user changes e-mail address to "foo@foo"')
def step_impl(context):
    context.browser.find_element_by_xpath("//input[@id='input-email']").clear()
    context.browser.find_element_by_xpath("//input[@id='input-email']").send_keys("foo@foo")
    context.browser.find_element_by_xpath("//input[@value = 'Continue']").click()

@then('warning message about not valid e-mail is showed')
def step_impl(context):
    context.browser.find_element_by_xpath("//*[contains(text(), 'E-Mail Address does not appear to be valid!')]")

@when('user logs out of his account')
def step_impl(context):
    context.execute_steps(u'''
        when user clicks "Logout" under "My Account" button
    ''')

@given('logged user\'s shopping cart contains an "MacBook Air"')
def step_impl(context):
    context.browser.get("http://pat.fit.vutbr.cz:8066/index.php?route=product/category&path=18")
    context.browser.find_element_by_xpath("//div[@id='content']/div[4]/div[3]/div/div[2]/div[2]/button/span").click()

@when('successfully logs in back to his account')
def step_impl(context):
    context.execute_steps(u'''
        given web browser is at "Login" page
         when user fills out correct login credentials
    ''')

@then('user\'s shopping cart contains an "MacBook Air"')
def step_impl(context):
    context.execute_steps(u'''
        given user\'s shopping cart contains an "MacBook Air"
    ''')
