import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json

# Parametros
USERNAME = ""
PASSWORD = ""
URL = "" 
COUNT = 0
EXTENSION_URL = "https://chromewebstore.google.com/detail/familysearch-center-premi/kpmeinlohefglphoflpoblpphppnokap"

# Função para instalar a extensão
def install_extension(driver, wait):
    driver.get(EXTENSION_URL)
    try:
        # Espera o botão "Usar no Chrome" e clica nele
        use_in_chrome_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Usar no Chrome']")))
        use_in_chrome_button.click()
        
        # Confirma a instalação no modal
        add_extension_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Adicionar extensão']")))
        add_extension_button.click()
        print("Extensão instalada com sucesso!")
    except Exception as e:
        print(f"Erro ao instalar a extensão: {e}")

# Criando opções do Chrome
options = uc.ChromeOptions()

# Criando o driver
driver = uc.Chrome(options=options, use_subprocess=True, version_main=144)  # Specify the main version of your Chrome browser
wait = WebDriverWait(driver, 15)
short_wait = WebDriverWait(driver, 3)

# Instala a extensão
install_extension(driver, wait)

# Acessa a URL desejada
driver.get(URL)
time.sleep(5)

# Espera campos de login
field_username = wait.until(EC.presence_of_element_located((By.ID, "userName")))
field_password = wait.until(EC.presence_of_element_located((By.ID, "password")))
button_login = wait.until(EC.element_to_be_clickable((By.ID, "login")))

# Preenche login
field_username.send_keys(USERNAME)
field_password.send_keys(PASSWORD)
button_login.click()

# Botão aceitar cookies
try:
    button_cookies = wait.until(EC.element_to_be_clickable((By.ID, "truste-consent-button")))
    button_cookies.click()
except Exception as e:
    print(f"Error: accept cookies button not found!")
    
# Aguarda para redirecionamento
time.sleep(5)

try:
    button_ok = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Muito bem']")))
    button_ok.click()
    time.sleep(1)
except Exception:
        pass

# ===== LOOP DE DOWNLOAD =====
for i in range(COUNT):
    print(f"Downloading image {i + 1}...")

    try:
        # Locate the "Download" button
        download_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Baixar"]')))
        
        # Check if the button is disabled
        is_disabled = download_button.get_attribute("disabled") is not None

        if not is_disabled:
            # If the button is enabled, click it
            download_button.click()

            # Clica no botão de confirmação no modal
            try:
                radio = short_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='radio'][value='JPG Only']")))
                radio.click()
                time.sleep(1)
                confirm_button = short_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="full-text-confirm-download"]')))
                confirm_button.click()
            except Exception:
                pass
        else:
            # Logic for protected images
            try:
                # Access browser logs to find the request URL
                logs = driver.get_log('performance')
                for entry in logs:
                    log = json.loads(entry['message'])['message']
                    if log['method'] == 'Network.responseReceived' and '/image_files/9/0_0.jpg' in log['params']['response']['url']:
                        original_url = log['params']['response']['url']
                        modified_url = original_url.replace('/image_files/9/0_0.jpg', '/$dist')
                        driver.get(modified_url)
                        time.sleep(5)  # Wait for the image to load

                        # Save the image
                        with open(f'image_{i + 1}.jpg', 'wb') as file:
                            file.write(driver.find_element(By.TAG_NAME, 'img').screenshot_as_png)
                        print(f"Image {i + 1} downloaded successfully.")
                        break
            except Exception as e:
                print(f"Error: Unable to download protected image. {e}")
                break
    except Exception as e:
        print(f"Error: Download button not found! {e}")
        break

    # Clica no botão Próxima imagem
    try:
        time.sleep(5)
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Próxima Imagem"]')))
        next_button.click()
    except Exception:
        print("Error: Next button not found!")
        break

driver.quit()
print("Done.")
