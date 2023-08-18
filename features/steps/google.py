# fetch_company_details.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
from behave import *

# Set up the Selenium WebDriver (assuming you have installed the appropriate driver for your browser)


company_details = []
store_dict = {}

# BDD Steps

@given("the user is on the Google search page")
def step_user_on_google_search_page(context):
    context.driver = webdriver.Chrome()

    # Navigate to Google search page
    context.driver.get("https://www.google.com")

@when('the user searches for "{search_term}"')
def step_user_searches_for(context, search_term):
    # Enter the search term and perform the search
    company = context.driver.find_element(By.XPATH, '//textarea[@id="APjFqb"]')
    company.send_keys(search_term)
    company.send_keys(Keys.RETURN)
    time.sleep(2)

@then("the user extracts the company details")
def step_user_extracts_company_details(context):
    # Extract company details and store them in company_details list
    try:
        company_name =context.driver.find_element(By.XPATH, "//div[@class='SPZz6b']/h2/span")
        store_dict["company"] = company_name.text
        company_add =context.driver.find_element(By.XPATH, '//span[@class="LrzXr"]')
        store_dict["address"] = company_add.text
        reviews =context.driver.find_element(By.XPATH, '//div[@class="CJQ04"]/div/span[@class="hqzQac"]/span/a')
        store_dict["reviews"] = reviews.text
        ratings =context.driver.find_element(By.XPATH, '//div[@class="CJQ04"]/div/span[@class="Aq14fc"]')
        store_dict["ratings"] = ratings.text

    except:
        store_dict["address"] = None
        store_dict["reviews"] = None
        store_dict["ratings"] = None
    else:
        new =context.driver.find_element(By.XPATH, '//div[@class="a4bIc"]/textarea')
        new.send_keys(" lat and long")
        new.send_keys(Keys.RETURN)
        elem =context.driver.find_element(By.XPATH, '//div[@class="Z0LcW t2b5Cf"]').text
        L = elem.split(",")
        store_dict["latitude"] = L[0]
        store_dict["longitude"] = L[1]
        time.sleep(3)
    company_details.append(store_dict)

@then("the user saves the company details to a CSV file")
def step_user_saves_company_details_to_csv(context):
    # Specify the CSV file path
    csv_file_path = 'company_details.csv'

    # Extract the keys from the first dictionary in the list (assuming all dictionaries have the same keys)
    field_names =company_details[0].keys()

    # Write data to CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(company_details)

    print(f"Data has vbeen successfully written to {csv_file_path}")

# Clean up after all the tests have run
def after_all(context):
    # Close the WebDriver
    context.driver.quit()


