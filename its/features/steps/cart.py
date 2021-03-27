from behave import *

@given('web browser is at "Laptops & Notebooks" products page')
def step_impl(context):
    context.browser.get("http://pat.fit.vutbr.cz:8066/index.php?route=product/category&path=18")

@when('user clicks on "ADD TO CART" button of "MacBook Air"')
def step_impl(context):
    button = context.browser.find_element_by_xpath("//div[@id='content']/div[4]/div[3]/div/div[2]/div[2]/button/span")
    button.click()

@then('"MacBook Air" is added to the shopping cart')
def step_impl(context):
    context.browser.get("http://pat.fit.vutbr.cz:8066/index.php?route=checkout/cart")
    context.browser.find_element_by_xpath("//*[contains(text(), 'MacBook Air')]")

@given('user\'s shopping cart contains an "MacBook Air"')
def step_impl(context):
    context.browser.get("http://pat.fit.vutbr.cz:8066/index.php?route=product/category&path=18")
    context.browser.find_element_by_xpath("//div[@id='content']/div[4]/div[3]/div/div[2]/div[2]/button/span").click()

@given('web browser is at "Shopping cart" page')
def step_impl(context):
    context.browser.get("http://pat.fit.vutbr.cz:8066/index.php?route=checkout/cart")

@when('user clicks red button representing removal')
def step_impl(context):
    context.browser.find_element_by_xpath("//div[@id='content']/form/div/table/tbody/tr/td[4]/div/span/button[2]").click()

@then('"MacBook Air" is removed from cart')
def step_impl(context):
    context.browser.get("http://pat.fit.vutbr.cz:8066/index.php?route=checkout/cart")
    context.browser.find_element_by_xpath("//*[contains(text(), 'Your shopping cart is empty!')]")

@when('user change quantity number to "20" and clicks "Update"')
def step_impl(context):
    context.browser.find_element_by_xpath("//div[@id='content']/form/div/table/tbody/tr/td[4]/div/input").clear()
    context.browser.find_element_by_xpath("//div[@id='content']/form/div/table/tbody/tr/td[4]/div/input").send_keys("20")
    context.browser.find_element_by_xpath("//div[@id='content']/form/div/table/tbody/tr/td[4]/div/span/button").click()

@then('user\'s shopping cart contains "20" items of "MacBook Air"')
def step_impl(context):
    quantity = context.browser.find_element_by_xpath("//input[starts-with(@name, 'quantity')]").get_attribute("value")
    assert(u"20" == quantity)
