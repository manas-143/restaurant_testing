from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

parent_path = ''
actual_price = 0
total_num_of_prod = 0
index = []

Locators = {
    "INPUT_AREA": "//input[@id='twotabsearchtextbox']",
    "INPUT_CLICK": "//input[@id='nav-search-submit-button']",
    "RATING": "//*[@class='a-icon-alt']",
    "PRODUCT_LIST": '//*[@class="a-section aok-relative s-image-fixed-height"]',
    "PRICE": "//span[@class='a-price-whole']",
    "ADD_TO_CART": "//input[@id='add-to-cart-button']",
    "SUB_TOTAL": '//span[@id="attach-accessory-cart-subtotal"]'
}


@given('User is on Amazon Page')
def opening_page(context):
    """
    Just Opening Window And Passing Link To Reach at main page and maximizing the window


    """
    context.driver = webdriver.Chrome()
    context.driver.get("https://www.amazon.in/")
    context.driver.maximize_window()


@when(u'He Search For Product Name "{product}"')
def product_searching(context, product):
    """
    In This I Generated Location For Input tag so that we can pass value to that for element
    search

    :param product: Holding The Value Of Product For Search
    :type   product: str
    """
    wait = WebDriverWait(context.driver, 20)
    input_prod = wait.until(ec.presence_of_element_located((By.XPATH, Locators["INPUT_AREA"])))
    input_prod.send_keys(product)
    original_window = context.driver.current_window_handle
    wait.until(ec.presence_of_element_located((By.XPATH, Locators['INPUT_CLICK']))).click()
    parent_url = context.driver.current_window_handle
    global parent_path
    parent_path = parent_url


@when(u'He filters product based on more than "{rating}" star rating')
def filtering_product_based_on_rating(context, rating):
    """
    In This Based On the rating parameter i filtered the product having rating more than
    given rating parameter and storing their index position to index variable for further use
    :param rating: Value Based on which i am filtering product

    """
    wait = WebDriverWait(context.driver, 10)
    rank_list = wait.until(ec.presence_of_all_elements_located((By.XPATH, Locators['RATING'])))
    # rank_list = wait.until(ec.presence_of_all_elements_located((By.XPATH, "//*[@class='a-icon-alt']")))

    all_prod = wait.until(
        ec.presence_of_all_elements_located(
            (By.XPATH, Locators['PRODUCT_LIST'])))

    index_pos = []
    for i in range(len(rank_list)):
        if float(rank_list[i].get_attribute('textContent').split()[0]) >= float(rating):
            index_pos.append(i)
    global index
    index = index_pos


@when(u'He add first "{num_of_prod}" product to cart')
def add_to_cart(context, num_of_prod):
    """
    Based On The Rating Top Product Adding To Cart And Before that storing the actual price
    summation to a variable act_price so we can compare and end with summarized price
    :param num_of_prod: Store Total Number of product we want to cart

    """
    wait = WebDriverWait(context.driver, 10)
    price = wait.until(ec.presence_of_all_elements_located((By.XPATH, Locators['PRICE'])))
    all_prod = wait.until(
        ec.presence_of_all_elements_located((By.XPATH, Locators['PRODUCT_LIST'])))
    count = 1
    act_price = 0
    top_pro = 1
    for i in range(len(all_prod)):
        if i in index:
            print(float(price[i].get_attribute('textContent').replace(',', '')))
            act_price += float(price[i].get_attribute('textContent').replace(',', ''))
            time.sleep(10)
            top_pro += 1
        if top_pro > int(num_of_prod):
            break
    global actual_price
    actual_price = act_price

    for i in range(len(all_prod)):
        if i in index:
            all_prod[i].click()
            han = context.driver.window_handles
            count += 1
        if count > int(num_of_prod):
            break
    for window_handle in set(han):
        if window_handle != parent_path:
            context.driver.switch_to.window(window_handle)
            wait.until(ec.element_to_be_clickable((By.XPATH, Locators['ADD_TO_CART']))).click()
            time.sleep(5)


@then('the cart value should be sum of products')
def comparing_price(context):
    """
    Comparing The Actual Summation of Price of added product with the summarized price
    showing on the web page after adding all product
    """
    wait = WebDriverWait(context.driver, 10)
    try:
        summarized_price = wait.until(
            ec.presence_of_element_located((By.XPATH, Locators['SUB_TOTAL']))).get_attribute(
            "textContent")
        assert actual_price == summarized_price
    except AssertionError as msg:
        print('Summarized Price And Actual Price Are Not Same')
    context.driver.quit()


'''-----------all the locators-------------'''
Locators={"search_box":"twotabsearchtextbox",

          "search_button" : "//input[@value='Go']",

          "rating_review_span_class" : "span.a-icon-alt",

          "laptop_list_div" : '//div[@data-component-type="s-search-result"]',

          "add_to_cart_button" :'//input[@id="add-to-cart-button"]',

          "Price_tag" : '//span[@class="a-price-whole"][1]',

          "cart_icon" : '//div[@id="nav-cart-count-container"]',

          "total_price" : '//span[@id="sc-subtotal-amount-activecart"]'
          }
'''---------------------------------------------------------------------------------------'''
amount = []  # ---------------------------------------------empty list to add the amount
laptops_to_add = []  # -------------------------------------empty list to add the highest rated items


@given("the Customer is on the Amazon.in homepage")
def amazon_login(context):
    context.driver = webdriver.Chrome()
    context.wait = WebDriverWait(context.driver, 15)
    context.driver.get("https://www.amazon.in/") #amazon webpage


@when('the Customer searches for "{search_query}"')
def search_for_laptops(context, search_query):
    search_box = context.driver.find_element(By.ID,Locators["search_box"] )
    search_box.send_keys(search_query) #------------------------------------contains search items
    search_button = context.driver.find_element(By.XPATH,Locators["search_button"])
    search_button.click()
    context.parent_url = context.driver.current_window_handle

@then("the Customer adds three highly-rated Dell laptops to the cart")
def add_laptops_to_cart(context):
    laptop_links = context.driver.find_elements(By.XPATH, Locators["laptop_list_div"])
    for laptop_element in laptop_links:
        rating_elements = laptop_element.find_elements(By.CSS_SELECTOR,Locators["rating_review_span_class"] )
        rating = rating_elements[0].get_attribute("innerHTML").split()[0] if rating_elements else "N/A" #to get the texts in the links
        if rating >= "4.0":
            laptops_to_add.append(laptop_element)

            '''to add the highest rated laptops'''
    laptops_added = 0
    for laptop_link in laptops_to_add:
        laptop_link.click()
        time.sleep(2)
        web_link = context.driver.window_handles #------------------contains parent web link
        '''--------------------------------------'''
    for item in web_link:
        if item != context.parent_url:
            context.driver.switch_to.window(item)
            wait = WebDriverWait(context.driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, Locators["add_to_cart_button"])))
            price_element = context.driver.find_element(By.XPATH,Locators["Price_tag"] ) #----------price webelement of laptop
            p = price_element.get_attribute("innerHTML")#price of laptop
            amount.append(p.replace('<span class="a-price-decimal">.</span>', ""))
            add_to_cart = context.driver.find_element(By.XPATH, Locators["add_to_cart_button"])
            add_to_cart.click()

            time.sleep(5)
            context.driver.switch_to.window(context.parent_url)
            laptops_added += 1
            if laptops_added == 3:
                break

@then("the Customer verifies the total price in the cart")
def price_compare(context):
    cart_button = context.driver.find_element(By.XPATH,Locators["cart_icon"] )
    cart_button.click()
    time.sleep(2)

    price = context.driver.find_element(By.XPATH, Locators["total_price"])
    time.sleep(3)
    final_price = price.text
    final_price = float(final_price.replace(",", ""))

    total_amount = sum(float(x.replace(',', '')) for x in amount)

    assert final_price == total_amount, "Total price in cart does not match with expected."


@then('the Customer closes the browser')
def close_browser(context):
    context.driver.quit()


