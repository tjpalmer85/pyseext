# This is just an entrypoint I can use to exercise the pyseext package

# Imports

# Third-party
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import time

# Ours
from pyseext.Ext import Ext
from pyseext.ComponentQuery import ComponentQuery
from Altus.AMS.Authentication import Authentication

# Initialise web driver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Load site
driver.get('http://localhost/atgws/build/Production/AltusProductsTransferGateway/')

# Wait for DOM
Ext(driver).wait_for_dom_ready()

# Create CQ instance
cq = ComponentQuery(driver)

# Wait for viewport (first load can take a while)
cq.wait_for_query('viewport', timeout=30)

# Login to the application
Authentication(driver).login(110002, 'altus.support', 'Password01!')

time.sleep(2)
driver.quit()
