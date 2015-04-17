from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import time
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import re

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

import settings
from models import Vendor, MenuCategory, MenuItem, Review, Base

engine = sqlalchemy.create_engine('sqlite:///:columbia.db:')
Base.metadata.create_all(engine)

def load_seamless_local_vendors():
    # Initialize Firefox and navigate to the local restaurants page
    login = driver.find_element_by_id("memberLogin")
    login.click()
    time.sleep(5)   # Wait till login field appears
    username_field = driver.find_element_by_id("username")
    password_field = driver.find_element_by_id("password")
    username_field.send_keys(settings.username)
    password_field.send_keys(settings.password)
    driver.find_element_by_id("submitLogin").click()
    time.sleep(5)
    driver.find_element_by_id("FindFood").click()
    time.sleep(5)
    load_all_restaurants()
    time.sleep(5)

def load_all_restaurants():
    # Continuously scrolldown, allowing new restaurants to load, until they are all loaded.
    try:
        load_message = driver.find_element_by_id("LoadMessage").get_attribute("innerHTML")
    except:
        load_message = "display: none"
    for x in range(60):
        if "display: none" not in load_message:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.2)
            try:
                load_message = driver.find_element_by_id("LoadMessage").get_attribute("innerHTML")
            except:
                load_message = "display: none"
        else:
            break
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(.2)

def restaurants():
    # Returns all restaurant links on the restaurant page
    return driver.find_elements_by_xpath("//div[@class='restaurant-name']/a[@class='tooltip']")

def clean(string):
    print string
    reg = re.compile('\s')
    str1 = reg.subn(' ', str(string))[0]
    return str(str1.strip())



def get_soup(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.text)

def iterate_vendors():
    # vendors_soup = BeautifulSoup(driver.page_source)
    # vendors = vendors_soup.find_all('a', )
    vendors = restaurants()
    for vendor in vendors:
        url = vendor.get_attribute("href")
        parse_vendor(session, url)

def parse_vendor(session, url):
    try:
        soup = get_soup(url)
        vendor_id = str(url.rsplit("/", 1)[1])
        name = str(soup.find('span', {'id':'VendorName'}).getText().strip())
        details = soup.find('div', {'id':'RestaurantDetails'})
        delivery_estimate = details.find_all('strong')[0].getText().strip()
        delivery_minimum = details.find_all('strong')[1].getText()
        delivery_minimum = clean(delivery_minimum.split("  ")[0])
        add_vendor(session, vendor_id, name, delivery_estimate, delivery_minimum)
        for li in soup.find_all('li', {"class":"menuItem"}):
            try:
                parse_menu_item(session, li, vendor_id)
            except:
                print "error while parsing menu_item"
                traceback.print_exc(file=sys.stderr)
                print ""
    except:
        print >> sys.stderr, "Error while parsing vendor"
        traceback.print_exc(file=sys.stderr)
        print >> sys.stderr, " "

def parse_menu_item(session, element, vendor_id):
    tooltip = element.find('a', {"class":"customTooltip"})
    name = tooltip['title']
    name = name.split(" - ", 1)[0]
    try:
        likes = int(tooltip['data'].split(" ", 1)[0])
    except:
        likes = 0
    price = element.find('span', {"class":"price"}).getText()
    price = float(price.split("$")[1].split("+")[0])
    menu_item = add_menu_item(session, name, price, likes, vendor_id)



def add_vendor(session, id, name, delivery_estimate, delivery_minimum):
    #, address, phone
    # try:     
    vendor = session.query(Vendor).filter_by(id=id).first()
    if vendor == None:
        vendor = Vendor(
            id=str(id), 
            name=str(name), 
            delivery_estimate=str(delivery_estimate),
            delivery_minimum=str(delivery_minimum)
            # address=address, 
            # phone=phone
            )
        session.add(vendor)
        output = "New Vendor"
    else:
        output = "Vendor Already Exists"
    session.commit()
    print output
    # except:
    #     print >> sys.stderr, "Error while adding vendor"
    #     traceback.print_exc(file=sys.stderr)
    #     print >> sys.stderr, " "

def add_menu_item(session, name, price, likes, vendor_id):
    # Creates a new menu item
    # Will add "description" later
    try:     
        menu_item = session.query(MenuItem).filter_by(name=name).filter_by(vendor_id=vendor_id).first()
        if menu_item == None:
            menu_item = MenuItem(
                name=name,
                price=price,
                likes=likes,
                vendor_id=vendor_id
                # description = description
                )
            session.add(menu_item)
            output = "New MenuItem"
        else:
            output = "MenuItem Already Exists"
        session.commit()
        print output, menu_item
    except:
        print >> sys.stderr, "Error while adding menu item", name
        traceback.print_exc(file=sys.stderr)
        print >> sys.stderr, " "

def display_database():
    # Display all the rows currently in the database
    print "Total Vendors:", session.query(Vendor).count()
    print "Total MenuItems:", session.query(MenuItem).count()
    for vendor in session.query(Vendor).all():
        print vendor
        for menu_item in session.query(MenuItem).filter_by(vendor_id=vendor.id).all():
            print "    ", menu_item

driver = webdriver.Firefox()
driver.get("http://www.seamless.com")
load_seamless_local_vendors()

Session = sessionmaker(bind=engine)
session = Session()


# display_database()
print ""