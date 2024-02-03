from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import TimeoutException
import time
import re



# PROXY = "86.236.183.61:3000"
options = webdriver.ChromeOptions()
# options.add_argument('--proxy-server=%s' % PROXY)

driver = webdriver.Chrome(options = options)

driver.get("https://www.coco.gg/chat/index.html#mimiMym_2_21_04428_0_514363797_0_")


processed_elements = set()
usernameUser = "bichou"
conversation_states = {}
users = {}

while True:
    for i in range(100):  # Adjust the range as necessary
        element_id = f"ongdiv{i}"
        if element_id not in processed_elements:
            try:
                element = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.ID, element_id))
                )
                # Click the new chat tab
                element.click()

                input_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "cocoa"))
                )

                text_container = driver.find_element(By.ID, "textum")
                html_content = text_container.get_attribute("innerHTML")

                # Use regex to extract all content up to the <br> tag following the c5 class span
                pairs = re.findall(r'<span class="c5">(.*?)</span>(.*?)(?=<span class="c5">|<br>|$)', html_content, re.DOTALL)
                
                for username, message in pairs:
                    usernameUser = username.strip().replace(":", "")
                    message = message.strip()
                    print(f"User: {username}, Message: {message}")
                    if element_id not in users:
                        users[element_id] = {'username': usernameUser, 'message': message}
                    else:
                        users[element_id]['message'] = users[element_id]['message'] + '. ' + message
                print('utilisateurs', users)
                time.sleep(2)
                if element_id not in conversation_states:
                    # If it's a new conversation, send the initial greeting
                    greeting = "Salut chou"
                    input_field.send_keys(greeting)
                    input_field.send_keys(Keys.ENTER)
                    conversation_states[element_id] = {'greeting_sent': True, 'messages': [greeting]}
                    time.sleep(2)
                else:
                    # If we've been here before, send a contextually relevant message
                    context_message = "Tfk ?"
                    input_field.send_keys(context_message)
                    input_field.send_keys(Keys.ENTER)
                    conversation_states[element_id]['messages'].append(context_message)
                    time.sleep(2)

                print('conversationsIA', conversation_states)

            except TimeoutException:
                # No new element within 2 seconds, handle the timeout case
                print("No new chat tab found")
                processed_elements.clear()
                break  # Break out of the for loop and start over
            except Exception as e:
                print(f"An error occurred: {e}")
                # Handle any other exceptions
    time.sleep(5) 