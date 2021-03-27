from behave import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

@when('user clicks on "Checkout" button')
def step_impl(context):
    context.browser.find_element_by_xpath("//a[normalize-space(.)='Checkout']").click()

@then('checkout phase is on step {step}')
def step_impl(context, step):
    if (step == 2):
        attribute = context.browser.find_element_by_xpath("//div[@id='collapse-payment-address']").get_attribute("class")
        assert(u"panel-collapse collapse in" == attribute)
    elif (step == 1):
        attribute = context.browser.find_element_by_xpath("//div[@id='collapse-payment-option']").get_attribute("class")
        assert(u"panel-collapse collapse in" == attribute)

@given('web browser is at "Checkout" page on step: "Billing Details"')
def step_impl(context):
    context.browser.get("http://pat.fit.vutbr.cz:8066/index.php?route=checkout/checkout")
    context.execute_steps(u'''
        then checkout phase is on step 2
    ''')


@when('user continues correctly to make an order')
def step_impl(context):
#    time.sleep(5)
#    context.browser.find_element_by_xpath("//input[@id='button-payment-address']").click()

    WebDriverWait(context.browser, 15).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='button-payment-address']"))).click()
    time.sleep(1)
    attribute = context.browser.find_element_by_xpath("//div[@id='collapse-shipping-address']").get_attribute("class")
    assert(u"panel-collapse collapse in" == attribute)

    WebDriverWait(context.browser, 15).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='button-shipping-address']"))).click()
    time.sleep(1)
    attribute = context.browser.find_element_by_xpath("//div[@id='collapse-shipping-method']").get_attribute("class")
    assert(u"panel-collapse collapse in" == attribute)

    WebDriverWait(context.browser, 15).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='button-shipping-method']"))).click()
    time.sleep(1)
    attribute = context.browser.find_element_by_xpath("//div[@id='collapse-payment-method']").get_attribute("class")
    assert(u"panel-collapse collapse in" == attribute)

    WebDriverWait(context.browser, 15).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and @name='agree']"))).click()
    context.browser.find_element_by_xpath("//input[@id='button-payment-method']").click()
    time.sleep(1)
    attribute = context.browser.find_element_by_xpath("//div[@id='collapse-checkout-confirm']").get_attribute("class")
    assert(u"panel-collapse collapse in" == attribute)

    WebDriverWait(context.browser, 15).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='button-confirm' and @value='Confirm Order']"))).click()

@then('order is successfully created')
def step_impl(context):
    context.browser.find_element_by_xpath("//*[contains(text(), 'Your order has been successfully processed!')]")
