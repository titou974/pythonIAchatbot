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
newMessage = False

def init_driver():
    options = webdriver.ChromeOptions()
    # if proxy:
    #     options.add_argument(f'--proxy-server={proxy}')
    return webdriver.Chrome(options=options)

def check_for_initialization(driver, timeout=30):
    driver.get("https://www.coco.gg/chat/index.html#natasha92_2_29_36213_0_290649056_0_")
    end_time = time.time() + timeout
    while True:
        try:
            time.sleep(2)
            searchy_div = driver.find_element(By.ID, 'searchy')
            # Look for any child divs with class "fixedsy" inside "searchy" div
            fixedsy_divs = searchy_div.find_elements(By.CLASS_NAME, 'fixedsy')
            # If any "fixedsy" divs are found, return False
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
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'coco.gg')]"))).click()

def login(driver, username, age, postal_code):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='fc-cta-consent']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'nicko'))).send_keys(username)
    driver.find_element(By.ID, 'femme').click()
    driver.find_element(By.ID, 'ageu').send_keys(age)
    driver.find_element(By.ID, 'zipo').send_keys(postal_code)
    driver.find_element(By.ID, 'entry').click()
    time.sleep(5)

def switch_to_new_tab(driver):
    # Wait for the new tab to open
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

    # Store the ID of the original window
    original_window = driver.current_window_handle

    # Switch to the new window which is the second tab
    new_window = [window for window in driver.window_handles if window != original_window][0]
    driver.switch_to.window(new_window)

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
    driver = init_driver()
    action = ActionChains(driver)
    try:
        check_for_initialization(driver)
        verify_email(driver, 'lafermelescollegiens@gmail.com')
        login(driver, 'natasha92', '29', 91000)
        switch_to_new_tab(driver)
        check_for_initialization(driver)
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

# # STEP 1: Verif Adresse MAIL

# driver.get("https://www.coco.gg/chat/index.html#lolach_2_23_28517_0_676678502_0_")
