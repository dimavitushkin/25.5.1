import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:\PyCharm\chromedriver.exe')
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()


def test_petfriends():

    # pytest.driver.find_element(By.XPATH, "//button[@onclick='document.location='/new_user';\"]").click()
    # pytest.driver.find_element(By.XPATH, "//a[@href='/login']").click()
    pytest.driver.find_element(By.ID, "email").send_keys("assasinfable@yandex.ru")
    pytest.driver.find_element(By.ID, "pass").send_keys("12345")
    pytest.driver.find_element(By.XPATH, "//button[@type='submit']").click()
    # pytest.driver.find_element(By.XPATH, "//a[@href='/my_pets']").click()

    pytest.driver.implicitly_wait(10)

    cards = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck.card')

    for i in range(len(cards)):
        pytest.driver.implicitly_wait(10)
        image = cards[i].find_element(By.XPATH, '//img[@class="card-img-top"]').get_attribute('src')
        pytest.driver.implicitly_wait(10)
        name = cards[i].find_element(By.XPATH, '//h5[@class="card-title"]').text
        pytest.driver.implicitly_wait(10)
        description = cards[i].find_element(By.XPATH, '//p[@class="card-text"]').text

        assert image != ''
        assert name != ''
        assert description != ''
        assert ', ' in description
        parts = description.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
