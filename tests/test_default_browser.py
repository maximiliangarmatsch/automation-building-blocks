from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import time
# Configure ChromeOptions to use the remote debugging port
options = uc.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
driver = uc.Chrome(driver_executable_path=ChromeDriverManager(driver_version = "127.0.6533.72").install(), 
                   options=options, 
                   desired_capabilities=DesiredCapabilities.CHROME)
driver.get("https://www.google.com")
time.sleep(30)
