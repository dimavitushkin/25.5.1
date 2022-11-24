import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:\PyCharm\chromedriver.exe')
   pytest.driver.get('https://petfriends.skillfactory.ru/')

   yield

   pytest.driver.quit()


class Pet:
    def __init__(self, photo, name, animalType, age):
        self.photo = photo
        self.name = name
        self.animalType = animalType
        self.age = age


def test_petfriends():
    wait = WebDriverWait(pytest.driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Зарегистрироваться')]"))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/login']"))).click()
    wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys("assasinfable@yandex.ru")
    wait.until(EC.presence_of_element_located((By.ID, "pass"))).send_keys("12345")
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='navbar-toggler-icon']"))).click()
    # time.sleep(1)
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/my_pets']"))).click()
    # time.sleep(1)

    wait.until(EC.title_is('PetFriends: My Pets'))
    # time.sleep(1)

    stringCountOfPets = wait.until(EC.presence_of_element_located((By.XPATH, "//body/div[1]/div[1]/div[1]"))).text
    countOfPets = stringCountOfPets.split('\n')[1].split(':')[1].strip()

    listOfRows = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr')))
    assert int(countOfPets) == len(listOfRows)

    petList = []
    listOfPetsName = []

    for i in range(len(listOfRows)):
        petItem = ''
        rowElements = wait.until(EC.presence_of_all_elements_located((By.XPATH, f'//tbody/tr[{i + 1}]/td')))

        itemPhoto = wait.until(EC.presence_of_element_located((By.XPATH, f'//tbody/tr[{i + 1}]/th[@scope="row"]/img'))).get_attribute('src')

        itemName = rowElements[0].text.strip()
        itemAnimalType = rowElements[1].text.strip()
        itemAge = rowElements[2].text.strip()

        petItem = Pet(itemPhoto, itemName, itemAnimalType, itemAge)
        petList.append(petItem)

        assert itemName != ''
        assert itemAnimalType != ''
        assert itemAge != ''

        listOfPetsName.append(itemName)

        emptyPhotoCount = 0
        for pet in petList:
            if pet.photo == '':
                emptyPhotoCount += 1

        assert emptyPhotoCount <= (len(petList) / 2)

        uniquePetsName = list(dict.fromkeys(listOfPetsName))
        assert len(listOfPetsName) == len(uniquePetsName)

        uniquePets = list(dict.fromkeys(petList))
        assert len(petList) == len(uniquePets)
