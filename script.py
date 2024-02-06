from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import re

conversationNumberLimit = 20
processed_usernames = set()
usernameUser = ""
conversation_states = {}
users = {}
context_message = "Tfk ?"
greeting = "Salut chou"
invitation = "Je suis sur mon mym perso, si tu veux on peut continuer à parler un peu dessus, j'échange du contenue sympa. passe à l'occasion :) : https://mym.fans/Petite_creature"
accounts = [
    {
        "username": "natashamym",
        "age": "29",
        "postal_code": 91000,
        "used": False
    },
    {
        "username": "lolamym",
        "age": "23",
        "postal_code": 13002,
        "used": False
    },
    {
        "username": "lauramym",
        "age": "21",
        "postal_code": 75015,
        "used": False
    },
    {
        "username": "luciemym",
        "age": "25",
        "postal_code": 69001,
        "used": False
    },
    {
        "username": "sophiemym",
        "age": "27",
        "postal_code": 97410,
        "used": False
    }
]

emailVerification = "lafermelescollegiens@gmail.com"

sessionIndex = 0

SESSION_TIMEOUT = 120



def init_driver():
    options = webdriver.ChromeOptions()
    # if proxy:
    #     options.add_argument(f'--proxy-server={proxy}')
    return webdriver.Chrome(options=options)

def check_for_initialization(driver, timeout=30):
    end_time = time.time() + timeout
    while True:
        try:
            time.sleep(2)
            searchy_div = driver.find_element(By.ID, 'searchy')
            fixedsy_divs = searchy_div.find_elements(By.CLASS_NAME, 'fixedsy')
            if len(fixedsy_divs) != 0:
                break
        except TimeoutException:
            pass 
        if time.time() > end_time:
            raise TimeoutException("The element did not initialize within the expected time.")
        driver.refresh()
        time.sleep(5)  

def verify_email(driver, email):
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'opt4'))).click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Récupération profil')]"))).click()
    time.sleep(2)
    email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'autamailu')))
    email_input.send_keys(email)
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Valider']"))).click()
    time.sleep(5)
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'coco.gg')]"))).click()

def login(driver, username, age, postal_code):
    driver.find_element(By.ID, 'nicko').send_keys(username)
    driver.find_element(By.ID, 'femme').click()
    driver.find_element(By.ID, 'ageu').send_keys(age)
    driver.find_element(By.ID, 'zipo').send_keys(postal_code)
    driver.find_element(By.ID, 'entry').click()
    time.sleep(5)

def validate_CTA(driver):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='fc-cta-consent']"))).click()

def switch_to_new_tab(driver):
    # Wait for the new tab to open
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

    # Store the ID of the original window
    original_window = driver.current_window_handle

    # Switch to the new window which is the second tab
    new_window = [window for window in driver.window_handles if window != original_window][0]
    driver.switch_to.window(new_window)

def check_if_connected_to_premium(driver): 
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'opt4'))).click()
    time.sleep(2)
    elements = driver.find_elements(By.CSS_SELECTOR, "div.overy b")
    for element in elements:
        if element.text == "OUI":
            print("Found a <b> with text 'OUI' inside a <div> with class 'overy'")
            return False
    else:
        print("No <b> with text 'OUI' found inside a <div> with class 'overy'")
        return True
    
def start_new_session(driver):
    global sessionIndex
    print('sessionIndex', sessionIndex)
    if sessionIndex == len(accounts):
        sessionIndex = 0
    account = accounts[sessionIndex]
    driver.get("https://www.coco.gg")
    time.sleep(5)
    validate_CTA(driver)
    login(driver, account['username'], account['age'], account['postal_code'])
    switch_to_new_tab(driver)
    check_for_initialization(driver)
    if check_if_connected_to_premium(driver) == False:
        verify_email(driver, emailVerification)
        login(driver, account['username'], account['age'], account['postal_code'])
        switch_to_new_tab(driver)
        check_for_initialization(driver)
        sessionIndex += 1
    else :
        sessionIndex += 1

def locate_chat_tab(driver):
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'ongdiv0'))  # Replace with an ID unique to the chat page
    )

def chat_with_user(user, driver, action, element):
    input_field = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "cocoa"))
    )
    if user not in conversation_states:
        input_field.send_keys(greeting)
        input_field.send_keys(Keys.ENTER)
        conversation_states[user] = {'greeting_sent': True, 'messages': [greeting], 'conversation_end': False}
        time.sleep(2)
    elif context_message not in conversation_states[user]['messages']:
        input_field.send_keys(context_message)
        input_field.send_keys(Keys.ENTER)
        conversation_states[user]['messages'].append(context_message)
        time.sleep(2)
    elif invitation not in conversation_states[user]['messages']: 
        input_field.send_keys(invitation)
        input_field.send_keys(Keys.ENTER)
        time.sleep(2)   
        conversation_states[user]['messages'].append(invitation)
        conversation_states[user]['conversation_end'] = True
        action.context_click(element).perform()
        processed_usernames.add(user)
        print(f'La conversation avec {users[user]["username"]} est terminée')
        time.sleep(2)
    else:
        processed_usernames.add(user)
        print( 'conversation déjà terminée')

def handle_new_message(name, driver):
    text_container = driver.find_element(By.ID, "textum")
    html_content = text_container.get_attribute("innerHTML")

    # Use regex to extract all content up to the <br> tag following the c5 class span
    pairs = re.findall(r'<span class="c5">(.*?)</span>(.*?)(?=<span class="c5">|<br>|$)', html_content, re.DOTALL)
    
    for username, message in pairs:
        message = message.strip()
        if name not in users:
            users[name] = {'username': name, 'messages': [message], 'newMessage': True}
        elif message not in users[name]['messages']:
            users[name]['messages'].append(message)
            users[name]['newMessage'] = True
        else:
            print('message déjà traité')
            users[name]['newMessage'] = False

def main():
    start_time = time.time()
    driver = init_driver()
    action = ActionChains(driver)
    try:
        start_new_session(driver)
        while True:
            i = 1
            while i < conversationNumberLimit:  
                element_id = f"ongdiv{i}"
                print('element_id', element_id)
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, element_id))
                    )

                    usernameUser = element.text
                    print('usernameUser', usernameUser)
                    element.click()


                    if usernameUser not in processed_usernames:
                        handle_new_message(usernameUser, driver)
                        time.sleep(5)
                        if users[usernameUser]['newMessage'] == True:
                            chat_with_user(usernameUser, driver, action, element)
                        print('conversationsIA', conversation_states)
                        print('users', users)

                    else:
                        print(f'Conversation for username {usernameUser} already processed or ended.')
                        action.context_click(element).perform()
                    i += 1

                except TimeoutException:
                    print("No new chat tab found")
                    time.sleep(1)
                    i = 1  
                    if time.time() - start_time > SESSION_TIMEOUT:
                        print("Session timeout exceeded. Starting a new session...")
                        driver.quit()  
                        return main() 
                except NoSuchElementException:
                    print(f"No such element {element_id}, might be fewer chat tabs than expected.")
                    break 
                except Exception as e:
                        print(f"An error occurred: {e}")
                        i += 1

            time.sleep(5) 
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

# PROXY = "86.236.183.61:3000"
# options = webdriver.ChromeOptions()
# # options.add_argument('--proxy-server=%s' % PROXY)

# driver = webdriver.Chrome(options = options)
