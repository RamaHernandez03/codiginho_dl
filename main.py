from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# CONSTANTES

USERNAME = "user@gmail.com"
PASSWORD = "password"
LOGIN_URL = "https://registration.codinggiants.es/app/Login"
RESERVATION_URL = "https://registration.codinggiants.es/app/RezerwacjaTerminow"

def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=Service(), options=options)

def login(driver):
    driver.get(LOGIN_URL)
    time.sleep(3)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "mat-input-0"))).send_keys(USERNAME)
    driver.find_element(By.ID, "mat-input-1").send_keys(PASSWORD + Keys.RETURN)

def seleccionar_dia_visible(driver, dia_str):
    wait = WebDriverWait(driver, 10)

    try:
        calendario_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'calendar')]")))
        calendario_btn.click()
        print("🖱️ Clic en botón de calendario")
    except Exception as e:
        raise Exception("No se encontro el calendario:", e)
    time.sleep(1)
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//mat-calendar")))
        print("✅ Calendario visible")
    except Exception as e:
        raise Exception("El calendario no esta visible:", e)
    # Arma el Fstring de la fecha del xPATH.
    aria_label = f"{dia_str} de julio de 2025"
    xpath_dia = f"//button[@aria-label='{aria_label}']"

    try:
        boton_dia = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_dia)))
        boton_dia.click()
        print(f"📆 Día {dia_str} seleccionado correctamente.")
    except Exception as e:
        raise Exception(f"No se pudo hacer clic en el día {dia_str}: {e}")


''' Una vez que entra al reservation a continuacion elije siempre, Summer 2025, DL y fecha. '''
def aplicar_filtros(driver):
    driver.get(RESERVATION_URL)
    time.sleep(2)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-label[text()='Choose semester']/ancestor::mat-form-field"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-option//span[contains(text(),'Summer 2025')]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-label[text()='Course type']/ancestor::mat-form-field"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-option//span[contains(text(),'DemonstrationLesson1On1Online')]"))).click()
    dia = input("¿Dia del mes a seleccionar (Numero del dia solamente)? (por ejemplo, 18): ").strip()
    seleccionar_dia_visible(driver, dia)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Get available groups')]"))).click()

def reservar_clases(driver):
    wait = WebDriverWait(driver, 10)
    while True:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr")))
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        for row in rows:
            try:
                # Si ya esta reservada, saltea
                clase_reservada = "background-color: yellow" in row.get_attribute("outerHTML")
                if clase_reservada:
                    print("⚠️ Clase ya reservada, salteada.")
                    continue
                # Si la DL es de un sabado o domingo se saltea
                dia_texto = row.find_element(By.XPATH, ".//td[contains(@class, 'cdk-column-dayOfWeek')]").text.strip().lower()
                if "sábado" in dia_texto or "sabado" in dia_texto or "domingo" in dia_texto:
                    print(f"⛔ Clase en fin de semana ({dia_texto}), salteada.")
                    continue
                # Click en  el boton de reserva
                boton_mas = row.find_element(By.XPATH, ".//button[.//i[contains(@class, 'fa-plus-circle')]]")
                driver.execute_script("arguments[0].click();", boton_mas)
                print(f"✅ Clase reservada para: {dia_texto.capitalize()}")
                time.sleep(0.5)
            except Exception as e:
                print("Error en la fila de la DL:", e)
        # Siguiente pagina de DL's
        try:
            siguiente = driver.find_element(By.XPATH, "//button[@aria-label='Next page' and not(@disabled)]")
            siguiente.click()
            print("👉 Pasando a la siguiente pagina...")
            time.sleep(2)
        except:
            print("✅ No hay más paginas. Finalizando.")
            break

def main():
    driver = iniciar_driver()
    try:
        login(driver)
        aplicar_filtros(driver)
        reservar_clases(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
