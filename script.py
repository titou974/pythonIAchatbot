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



# PROXY = "86.236.183.61:3000"
options = webdriver.ChromeOptions()
# options.add_argument('--proxy-server=%s' % PROXY)

driver = webdriver.Chrome(options = options)

# STEP 1: Verif Adresse MAIL

driver.get("https://www.coco.gg/chat/index.html#lolach_2_23_28517_0_676678502_0_")

time.sleep(5)

profil_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'opt4')) 
)


profil_button.click()

time.sleep(2)
verif_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Récupération profil')]"))
)


verif_button.click()

time.sleep(2)

verif_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'autamailu')) 
)


verif_input.send_keys('lafermelescollegiens@gmail.com')

time.sleep(2)

validate_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@value='Valider']"))  # Use the 'value' attribute to locate the button
)


validate_button.click()

time.sleep(5)
link_text = "coco.gg"  # Replace with the actual text that appears on the link
link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{link_text}')]"))
)
link.click()

time.sleep(5)

# STEP 2: Connexion

consent_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='fc-cta-consent']"))  # This selector should be adjusted based on the actual classes used by the button
)
consent_button.click()

username_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'nicko')) 
)
username_field.send_keys('lolamym') 

# Find the password field and enter the password
gender_selection = driver.find_element(By.ID, 'femme') 
gender_selection.click()  

age_selection = driver.find_element(By.ID, 'ageu')  

age_selection.send_keys('23')

postal_code = driver.find_element(By.ID, 'zipo')

postal_code.send_keys(75002)

# Find the submit button and click it to log in
submit_button = driver.find_element(By.ID, 'entry')  # Replace with actual ID or selector
submit_button.click()
time.sleep(5)

WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

# Store the ID of the original window
original_window = driver.current_window_handle

# Switch to the new window which is the second tab
new_window = [window for window in driver.window_handles if window != original_window][0]
driver.switch_to.window(new_window)

# Wait for the automatic navigation to the chat page

#STEP 3: Chat
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, 'ongdiv0'))  # Replace with an ID unique to the chat page
)

action = ActionChains(driver)

conversationNumberLimit = 20
processed_usernames = set()
usernameUser = "bichou"
conversation_states = {}
users = {}
context_message = "Tfk ?"
greeting = "Salut chou"
invitation = "Je suis sur mon mym perso, si tu veux on peut continuer à parler un peu dessus, j'échange du contenue sympa. passe à l'occasion :) : https://mym.fans/Petite_creature"

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
                input_field = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "cocoa"))
                )

                text_container = driver.find_element(By.ID, "textum")
                html_content = text_container.get_attribute("innerHTML")

                # Use regex to extract all content up to the <br> tag following the c5 class span
                pairs = re.findall(r'<span class="c5">(.*?)</span>(.*?)(?=<span class="c5">|<br>|$)', html_content, re.DOTALL)
                
                for username, message in pairs:
                    message = message.strip()
                    if usernameUser not in users:
                        users[usernameUser] = {'username': usernameUser, 'messages': [message]}
                    elif message not in users[usernameUser]['messages']:
                        users[usernameUser]['messages'].append(message)
                    else:
                        print('message déjà traité')
                print('utilisateurs', users)
                time.sleep(5)
                if usernameUser not in conversation_states:
                    input_field.send_keys(greeting)
                    input_field.send_keys(Keys.ENTER)
                    conversation_states[usernameUser] = {'greeting_sent': True, 'messages': [greeting], 'conversation_end': False}
                    time.sleep(2)
                elif context_message not in conversation_states[usernameUser]['messages']:
                    input_field.send_keys(context_message)
                    input_field.send_keys(Keys.ENTER)
                    conversation_states[usernameUser]['messages'].append(context_message)
                    time.sleep(2)
                elif invitation not in conversation_states[usernameUser]['messages']: 
                    input_field.send_keys(invitation)
                    input_field.send_keys(Keys.ENTER)
                    time.sleep(2)   
                    conversation_states[usernameUser]['messages'].append(invitation)
                    conversation_states[usernameUser]['conversation_end'] = True
                    action.context_click(element).perform()
                    processed_usernames.add(usernameUser)
                    print(f'La conversation avec {users[usernameUser]["username"]} est terminée')
                    time.sleep(2)
                else:
                    processed_usernames.add(usernameUser)
                    print( 'conversation déjà terminée')

            else:
                print(f'Conversation for username {usernameUser} already processed or ended.')
                action.context_click(element).perform()
            print('conversationsIA', conversation_states)
            i += 1

        except TimeoutException:
            # No new element within 2 seconds, handle the timeout case
            print("No new chat tab found")
            # if usernameUser not in processed_usernames:
            #     input_field = WebDriverWait(driver, 5).until(
            #         EC.element_to_be_clickable((By.ID, "cocoa"))
            #     )

            #     text_container = driver.find_element(By.ID, "textum")
            #     html_content = text_container.get_attribute("innerHTML")

            #     # Use regex to extract all content up to the <br> tag following the c5 class span
            #     pairs = re.findall(r'<span class="c5">(.*?)</span>(.*?)(?=<span class="c5">|<br>|$)', html_content, re.DOTALL)
                
            #     for username, message in pairs:
            #         message = message.strip()
            #         if usernameUser not in users:
            #             users[usernameUser] = {'username': usernameUser, 'messages': [message]}
            #         elif message not in users[usernameUser]['messages']:
            #             users[usernameUser]['messages'].append(message)
            #         else:
            #             print('message déjà traité')
            #     print('utilisateurs', users)
            #     time.sleep(5)
            #     if usernameUser not in conversation_states:
            #         input_field.send_keys(greeting)
            #         input_field.send_keys(Keys.ENTER)
            #         conversation_states[usernameUser] = {'greeting_sent': True, 'messages': [greeting], 'conversation_end': False}
            #         time.sleep(2)
            #     elif context_message not in conversation_states[usernameUser]['messages']:
            #         input_field.send_keys(context_message)
            #         input_field.send_keys(Keys.ENTER)
            #         conversation_states[usernameUser]['messages'].append(context_message)
            #         time.sleep(2)
            #     elif invitation not in conversation_states[usernameUser]['messages']: 
            #         input_field.send_keys(invitation)
            #         input_field.send_keys(Keys.ENTER)   
            #         conversation_states[usernameUser]['messages'].append(invitation)
            #         conversation_states[usernameUser]['conversation_end'] = True
            #         action.context_click(element).perform()
            #         processed_usernames.add(usernameUser)
            #         print(f'La conversation avec {users[usernameUser]["username"]} est terminée')
            #         time.sleep(2)
            #     else:
            #         processed_usernames.add(usernameUser)
            #         print( 'conversation déjà terminée')

            time.sleep(1)
            i = 1  # Reset the counter to restart the loop
        except NoSuchElementException:
            print(f"No such element {element_id}, might be fewer chat tabs than expected.")
            break  # Break out of the while loop if an expected element doesn't exist
        except Exception as e:
                print(f"An error occurred: {e}")
                if usernameUser not in processed_usernames:
                    input_field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "cocoa"))
                    )

                    text_container = driver.find_element(By.ID, "textum")
                    html_content = text_container.get_attribute("innerHTML")

                    # Use regex to extract all content up to the <br> tag following the c5 class span
                    pairs = re.findall(r'<span class="c5">(.*?)</span>(.*?)(?=<span class="c5">|<br>|$)', html_content, re.DOTALL)
                    
                    for username, message in pairs:
                        message = message.strip()
                        if usernameUser not in users:
                            users[usernameUser] = {'username': usernameUser, 'messages': [message]}
                        elif message not in users[usernameUser]['messages']:
                            users[usernameUser]['messages'].append(message)
                        else:
                            print('message déjà traité')
                    print('utilisateurs', users)
                    time.sleep(5)
                    if usernameUser not in conversation_states:
                        input_field.send_keys(greeting)
                        input_field.send_keys(Keys.ENTER)
                        conversation_states[usernameUser] = {'greeting_sent': True, 'messages': [greeting], 'conversation_end': False}
                        time.sleep(2)
                    elif context_message not in conversation_states[usernameUser]['messages']:
                        input_field.send_keys(context_message)
                        input_field.send_keys(Keys.ENTER)
                        conversation_states[usernameUser]['messages'].append(context_message)
                        time.sleep(2)
                    elif invitation not in conversation_states[usernameUser]['messages']: 
                        input_field.send_keys(invitation)
                        input_field.send_keys(Keys.ENTER)
                        time.sleep(2)   
                        conversation_states[usernameUser]['messages'].append(invitation)
                        conversation_states[usernameUser]['conversation_end'] = True
                        action.context_click(element).perform()
                        processed_usernames.add(usernameUser)
                        print(f'La conversation avec {users[usernameUser]["username"]} est terminée')
                        time.sleep(2)
                    else:
                        processed_usernames.add(usernameUser)
                        print( 'conversation déjà terminée')

                else:
                    print(f'Conversation for username {usernameUser} already processed or ended.')
                    action.context_click(element).perform()
                print('conversationsIA', conversation_states)
                i += 1

    time.sleep(5) 