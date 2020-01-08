from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import sys
import time

def contains_elem(web, css_selector):
	try:
		elem = web.find_element(By.CSS_SELECTOR, css_selector)

		if elem:
			return True
		else:
			return False

	except Exception as e:
		return False

def find_elem(web, css_selector):
	elem = web.find_element(By.CSS_SELECTOR, css_selector)

	if elem:
		return elem
	else:
		raise Exception('Element with CSS Selector ' + css_selector + ' not found')

def find_elems(web, css_selector):
	try:
		elems = web.find_elements(By.CSS_SELECTOR, css_selector)

		if elems:
			return elems
		else:
			[]

	except Exception as e:
		return []

def visible_elem(web, css_selector):
	try:
		elem = web.find_element(By.CSS_SELECTOR, css_selector)

		if elem:
			return elem.is_displayed()
		else:
			return False

	except Exception as e:
		return False

def wait_until_invisible(web, css_selector, message):
	# We are required to solve the captcha
	if contains_elem(web, css_selector) and message != '':
		print()
		print("INFO: Es necesario " + message + " que aparece en pantalla!")

	try:
		element = WebDriverWait(web, 3600).until_not(
			EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
		)

	except (TimeoutException, NoSuchElementException):
		pass

def click_element(web, css_selector):
	find_elem(web, css_selector).click()

def priced_course(web):
	element = find_elem(web, 'div.course-price-text > span:nth-child(2)')
	price = element.get_attribute('innerText')
	price = price.strip().lower()
	return not("gratuito" in price or "gratis" in price or "free" in price)

def wait_until_loaded(web):
	try:
		elem = WebDriverWait(web, 2).until(EC.presence_of_element_located((By.NAME, 'html')))
		return
	except TimeoutException:
		return

if len(sys.argv) != 2:
	print("ERROR: Falta como parametro el link de Chollometro")
	quit(-1)

try:
	result = urlparse(sys.argv[1])

	if not "chollometro" in result.hostname:
		print("ERROR: El link introducido no es de Chollometro")
		quit(-1)

	print("Es necesario que inicies sesión en Udemy para continuar")

	web = webdriver.Chrome(executable_path="C:/Users/Robert/Downloads/chromedriver_win32/chromedriver.exe", service_log_path='NUL')
	web.get('http://udemy.com')
	wait_until_invisible(web, 'div.g-recaptcha', 'resolver el captcha')
	time.sleep(5)
	if visible_elem(web, 'div.ud-component--footer--eu-cookie-message'):
		click_element(web, 'button.eu-cookie-message--eu-cookie-message__cta--n9_pl')
	click_element(web, 'button[data-purpose="header-login"]')
	wait_until_invisible(web, 'div.g-recaptcha', 'resolver el captcha')

	wait_until_invisible(web, 'button[data-purpose="header-login"]', '')

	print("Accediendo a link de Chollometro...")

	web.get(sys.argv[1])

	print("Procesando cursos...")

	links = []

	# Search for Udemy links in the window
	for link in find_elems(web, 'div.userHtml > div.cept-description-container a[title*="udemy.com"]'):
		links.append(link.get_attribute('title'))

	# No Udemy links found
	if not links:
		print()
		print("No se han detectado cursos.")
		quit(0)

	print()
	print(str(len(links)) + " cursos detectados, inscribiendo...")

	for i in range(len(links)):
		print()
		print("Inscribiendo en curso #" + str(i + 1))

		web.get(links[i])

		wait_until_loaded(web)

		# We wait the user to solve the captcha if needed
		wait_until_invisible(web, 'div.g-recaptcha', 'resolver el captcha')

		if contains_elem(web, 'div.purchase-text'):
			print()
			print("INFO: Ya estas inscrito en el curso #" + str(i + 1))
			continue

		if priced_course(web):
			print()
			print("WARNING: El curso #" + str(i + 1) + " es de pago, saltando...")
			continue

		# TODO: things to consider when subscribing to course:
		# - Max. number of requests error in course page
		# - Max. number of requests error in checkout page
		# - Captcha may occur at any point (before or after clicking subscribe button)
		# - Checkout page may appear (not a direct subscription)

		# Click subscribe to course button
		click_element(web, 'button[data-purpose="buy-this-course-button"]')

		# We wait the user to solve the captcha if needed
		wait_until_invisible(web, 'div.g-recaptcha', 'resolver el captcha')

		# Wait before checking if course was bought
		wait_until_loaded(web)

		# Successfully bought the free course
		if contains_elem(web, 'div.styles--success-alert__text--1kk07'):
			print()
			print("Inscrito en curso #" + str(i + 1))
			continue

		wait_until_loaded(web)

		# TODO: Check if max. number of requests occurs after buying the course without being redirected to checkout page (cooldown)

		# We have been redirected to checkout page
		if contains_elem(web, 'div[data-purpose="cart-list"]'):
			if priced_course(web):
				print()
				print("WARNING: El curso #" + str(i + 1) + " es de pago, saltando...")
				continue

			# TODO: Check if max. number of requests error is considered

			# Click purchase button
			click_element(web, 'div.checkout--sc-card-footer--14lRj button[type=submit]')

			# Course purchased successfully
			if contains_elem(web, 'div.styles--success-alert__guarantee--3wtEG'):
				print()
				print("Inscrito en curso #" + str(i + 1))
				continue

			# Course could not be purchased (too many requests error), so we need to wait to cool it down
			while not contains_elem(web, 'div.styles--success-alert__guarantee--3wtEG'):
				time.sleep(30) # 30 second cooldown
				web.click(css_selector='div.checkout--sc-card-footer--14lRj button[type=submit]')

			# Course purchased successfully
			if not contains_elem(web, 'div.styles--success-alert__guarantcontains_elem-3wtEG'):
				print()
				print("ERROR: Ha fallado la inscripcion del curso #" + str(i + 1))
				continue

except ValueError:
	print("ERROR: El parametro no contiene una URL valida")
	quit()