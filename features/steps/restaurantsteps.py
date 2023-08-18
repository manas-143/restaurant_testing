import csv
import time
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By

output_file_name = "google_map_restaurants_data.csv"
unique_check = []
number = 30

def save_data(data):
    header = ['id', 'company_name', 'rating', 'reviews_count', 'address']
    with open(output_file_name, 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if data[0] == 1:
            writer.writerow(header)
        writer.writerow(data)

def rating_and_review_count(restaurant):
    try:
        reviews_block = restaurant.find_element(By.CLASS_NAME, 'AJB7ye').text.split("(")
        rating = reviews_block[0].strip()
        reviews_count = reviews_block[1].split(")")[0].strip()
    except:
        rating = "no ratings"
        reviews_count = "no reviews"

    return rating, reviews_count

def address_and_category(restaurant):
    try:
        address_block =restaurant.find_elements(By.CLASS_NAME, "W4Efsd")[2].text.split("·")
        if len(address_block) >= 2:
            address = address_block[1].strip()
        elif len(address_block) == 1:
            address = "address not available"
    except:
        address = "address not available"

    return address

@given("the user is on the Google Maps restaurants page")
def step_impl_given(context):
    context.driver = webdriver.Chrome()
    url = "https://www.google.com/maps/search/restaurants+near+me/"
    context.driver.get(url)
    time.sleep(5)

@when("the user scrolls down and loads more restaurants")
def step_impl_when(context):
    global unique_check, number

    def get_restaurant_info():
        global unique_check, number

        time.sleep(2)
        for business in context.driver.find_elements(By.CLASS_NAME, 'THOPZb'):
            name = business.find_element(By.CLASS_NAME, 'fontHeadlineSmall').text
            rating, reviews_count = rating_and_review_count(business)
            address = address_and_category(business)

            unique_id = "".join([name, rating, reviews_count, address])
            if unique_id not in unique_check and len(unique_check) != number:
                data = [name, rating, reviews_count, address]
                save_data(data)
                unique_check.append(unique_id)

    panel_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]'
    scrollable_div =context.driver.find_element(By.XPATH, panel_xpath)

    flag = True
    i = 0
    while flag:
        print(f"Scrolling to page {i + 2}")
        context.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        time.sleep(2)

        if "You've reached the end of the list." in context.driver.page_source:
            flag = False

        get_restaurant_info()
        i += 1

@then("the user should scrape and save information for {number:d} restaurants")
def step_impl_then(context, number):
    assert len(unique_check) == number

@then("the user should not have duplicate restaurant information")
def step_impl_then(context):
    unique_set = set(unique_check)
    assert len(unique_set) == len(unique_check)
