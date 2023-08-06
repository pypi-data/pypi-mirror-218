import requests
from bs4 import BeautifulSoup
import random

class nick():
    class NationType(): # Нации
        RUSSIAN = 'russian'
        JAPANESE = 'japanese'
        ITALIAN = 'italian'
        LATINOS = 'latinos'
        FRENCH = 'french'
        SWEDISH = 'swedish'
        GERMAN = 'german'
        DANISH = 'danish'
        ROMANIAN = 'romanian'
        AMERICAN = 'american'

        def random(): # Выбор рандомной нации
            return random.choice(['russian', 'japanese', 'italian', 'latinos', 'french', 'swedish', 'german', 'danish', 'romanian', 'american'])
    class GenderType(): # Гендеры
        MALE = 'male'
        FEMALE = 'female'

        def random(): # Выбор рандомного гендера
            return random.choice(['male', 'female'])
    def GenerateNick(gender = GenderType.random() or str, nation = NationType.random() or str, name = '', surname = ''):
        page = requests.get(f'http://rp-nicks.aa-roleplay.ru/index.php?gender={gender}&nation={nation}&name={name}&surname={surname}')
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'lxml')
            nick = soup.find('textarea')
            return nick.text