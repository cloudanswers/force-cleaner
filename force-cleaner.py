import os
from time import sleep
from selenium import webdriver


def login(driver, username, password):
    driver.get('https://test.salesforce.com')
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('Login').click()


def open_installed_packages(driver):
    setup_url = driver.current_url.split('force.com/')[0] + 'force.com/0A3'
    driver.get(setup_url)


def fix_button_or_link(driver):
    # this page has slow js
    sleep(1)

    # save the field name for later
    name = None
    for row in driver.find_elements_by_css_selector('div.pbBody tr'):
        if row.text.startswith('Name'):
            name = row.find_element_by_css_selector('td.col02').text
    assert name

    # there are 2 in this page, one at top and one on bottom
    # button "Where is this used?"
    driver.find_elements_by_name('impactAnalysis')[0].click()

    row = driver.find_elements_by_css_selector("tr .dataRow")[0]
    if row.text.startswith('Page Layout'):
        row.find_elements_by_tag_name('a')[0].click()


    exit()


def fix_top_uninstall_problem(driver):
    row = driver.find_elements_by_css_selector("tr .dataRow")[0]

    if row.text.startswith('Button or Link'):
        action = fix_button_or_link
    else:
        raise Exception('unknown metadata type')

    # follow the first error
    row.find_elements_by_tag_name('a')[0].click()

    action(driver)


def uninstall_top_package(driver):
    driver.find_elements_by_link_text('Uninstall')[0].click()
    # js on this page can be slow
    sleep(1)
    driver.find_element_by_name('p5').click()
    driver.find_element_by_id('Uninstall').click()

    if 'Problems' in driver.page_source:
        fix_top_uninstall_problem(driver)
        open_installed_packages(driver)
        uninstall_top_package(driver)
        # TODO make sure we don't end up in a loop


if __name__ == '__main__':

    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    if not username or not password:
        raise Exception('USERNAME and PASSWORD env not set')

    driver = webdriver.Firefox()
    login(driver, username, password)

    open_installed_packages(driver)

    uninstall_top_package(driver)