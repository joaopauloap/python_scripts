import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Parametros
USERNAME = ""
PASSWORD = ""
URL = "" 
COUNT = 10

# Inicia navegador com proteção contra bloqueio
driver = uc.Chrome()
driver = uc.Chrome()
wait = WebDriverWait(driver, 15)
short_wait = WebDriverWait(driver, 3)

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

# ===== LOOP DE DOWNLOAD =====
for i in range(COUNT):
    print(f"Downloading image {i + 1}...")

    # Clica no botão "Download"
    try:
        download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Baixar"]')))
        download_button.click()
    except Exception as e:
        print(f"Error: Download button not found!")
        break

    # Clica no botão de confirmação no modal
    try:
        confirm_button = short_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="full-text-confirm-download"]')))
        confirm_button.click()
    except Exception:
        pass
    
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
