from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# --- 1. Configurar opciones de Chrome ---
options = Options()
options.headless = False  # abrir Chrome visible
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument("--user-data-dir=/tmp/temp_chrome_profile")

# --- 2. Inicializar ChromeDriver ---
driver = webdriver.Chrome(options=options)

# --- 3. Abrir la página ---
driver.get("https://www3.ugto.mx/desarrolloestudiantil/clasesdeportivas/calendarioClasesCGTO.php")

# --- 4. Espera explícita hasta que aparezcan los botones de actividades ---
wait = WebDriverWait(driver, 10)
buttons = wait.until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, "span.badge-more-schedule")
))

print(f"Se encontraron {len(buttons)} botones de actividades disponibles")

# --- 5. Hacer clic en el botón del lunes (último de los 5) ---
if len(buttons) >= 5:
    lunes = buttons[-5]
    lunes.click()
    print("Se hizo clic en el botón correspondiente al lunes")
else:
    print("No se encontraron suficientes botones para la semana")

# --- 6. Esperar que cargue el horario del gimnasio ---
time.sleep(2)

# --- 7. Hacer clic en el botón del horario usando XPath ---
try:
    horario_lunes = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="Calendar"]/div/div[2]/div/div[2]/div[8]/span[2]')
    ))
    horario_lunes.click()
    print("Se hizo clic en el botón del horario del lunes")
except:
    print("No se pudo encontrar o hacer clic en el botón del horario")

# --- 8. Seleccionar el radio button de estudiante usando JS click ---
time.sleep(2)

try:
    radio_estudiante = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="tipoUserForum1"]')
    ))
    driver.execute_script("arguments[0].click();", radio_estudiante)
    print("Se seleccionó el radio button de estudiante")
except:
    print("No se pudo seleccionar el radio button de estudiante")

# --- 9. Completar formulario ---

try:
    # Nombre
    input_nombre = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userName"]')))
    input_nombre.clear()
    input_nombre.send_keys("Dante Solorzano Ferrer")

    # NUA
    input_nua = driver.find_element(By.XPATH, '//*[@id="userNua"]')
    input_nua.clear()
    input_nua.send_keys("282940")

    # Campus
    select_campus = Select(driver.find_element(By.XPATH, '//*[@id="userCampus"]'))
    select_campus.select_by_index(2)  # opción 3, los índices empiezan en 0
    time.sleep(1)
    # División
    select_division = Select(driver.find_element(By.XPATH, '//*[@id="userDivision"]'))
    select_division.select_by_index(2)  # opción 3
    time.sleep(1)

    # Programa
    select_programa = Select(driver.find_element(By.XPATH, '//*[@id="userPrograma"]'))
    select_programa.select_by_index(7)  # opción 8

    # Correo
    input_correo = driver.find_element(By.XPATH, '//*[@id="userCorreo"]')
    input_correo.clear()
    input_correo.send_keys("d.solorzanoferrer@ugto.mx")

    # Checkbox de compromiso
    checkbox = driver.find_element(By.XPATH, '//*[@id="userCompromiso"]')
    driver.execute_script("arguments[0].click();", checkbox)  # JS click para disparar eventos JS

    # Espera 2 segundos antes de enviar
    time.sleep(2)

    # Botón enviar
    btn_enviar = driver.find_element(By.XPATH, '//*[@id="btnUserRegistrarClase"]')
    btn_enviar.click()

    print("Formulario completado y enviado correctamente")
except Exception as e:
    print("Ocurrió un error al completar el formulario:", e)

# Espera explícita hasta que el botón sea clickeable
wait = WebDriverWait(driver, 10)
try:
    btn_final = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[4]/div/div[3]/button[1]")
    ))
    btn_final.click()
    print("Se presionó el botón final correctamente")
except:
    print("No se pudo presionar el botón final")

# --- 10. Mantener la página abierta para inspección ---
print("Chrome está abierto. Presiona CTRL+C en la terminal para detener el script.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Script detenido por usuario. Cerrando Chrome...")
    driver.quit()
