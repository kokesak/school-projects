from behave import *

@given('web browser is at index page')
def step_impl(context):
    context.browser.get("http://pat.fit.vutbr.cz:8066/")

@when('user change currency to {currency}')
def step_impl(context, currency):
    context.browser.find_element_by_xpath("//span[contains(.,'Currency')]").click()
    context.browser.find_element_by_xpath("//button[@name=\'" + currency + "\']").click()

@then('prices on website are changed to {currency}')
def step_impl(context, currency):
    if (currency == "EUR"):
        context.browser.find_element_by_xpath("//*[contains(text(), '556.79€')]")
    elif (currency == "GBP"):
        context.browser.find_element_by_xpath("//*[contains(text(), '£481.96')]")
    elif (currency == "USD"):
        context.browser.find_element_by_xpath("//*[contains(text(), '$602.00')]")

@given('"Sort By:" box is set to "Default"')
def step_impl(context):
    context.browser.find_element_by_xpath("//select[@id='input-sort']").click()
    context.browser.find_element_by_xpath("//option[normalize-space(.)='Default']").click()

@when('user changes "Sort By:" box to "Price (Low > High)"')
def step_impl(context):
    context.browser.find_element_by_xpath("//select[@id='input-sort']").click()
    context.browser.find_element_by_xpath("//option[normalize-space(.)='Price (Low > High)']").click()

@then('prices of items are sorted by price from low to high')
def step_impl(context):
    context.execute_steps(u'''
         when user change currency to USD
    ''')
    context.browser.find_element_by_xpath("//div[@id='content']/div[4]/div[1]/div/div[2]/div/p[2][contains(text(), '$122.00')]")
    context.browser.find_element_by_xpath("//div[@id='content']/div[4]/div[2]/div/div[2]/div/p[2][contains(text(), '$602.00')]")
    context.browser.find_element_by_xpath("//div[@id='content']/div[4]/div[3]/div/div[2]/div/p[2][contains(text(), '$1,202.00')]")
    context.browser.find_element_by_xpath("//div[@id='content']/div[4]/div[4]/div/div[2]/div/p[2][contains(text(), '$1,202.00')]")
    context.browser.find_element_by_xpath("//div[@id='content']/div[4]/div[5]/div/div[2]/div/p[2][contains(text(), '$2,000.00')]")

@then('user shopping cart is empty')
def step_impl(context):
    context.execute_steps(u'''
        then "MacBook Air" is removed from cart
    ''')
