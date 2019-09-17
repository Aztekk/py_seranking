import requests
import pandas as pd
import datetime
from pandas.io.json import json_normalize


class SERanking(object):
    """
    Класс для работы с SERanking
    """
    MANAGEMENT_URL = "https://api4.seranking.com/"
    token = None
    now = str(datetime.datetime.now().date())

    def __init__(self, token):
        """
        Инициализация объекта класса
        :param token: токен от API SERanking
        """
        self.token = token

    @property
    def get_header(self):
        """
        :return: заголовок с данными авторизации.
        """
        return {
            'Authorization': 'Bearer {}'.format(self.token)
        }

    def get_sites(self):
        """
        :return: все существующие сайты
        """
        url = [self.MANAGEMENT_URL, 'sites']
        url = ''.join(url)
        headers = self.get_header
        response = requests.get(url, headers=headers)
        result = pd.DataFrame(response.json())
        return result

    def search_engines(self):
        """
        :return: все существующие поисковые системы, доступные в SEranking
        """
        url = [self.MANAGEMENT_URL, '/system/search-engines']
        url = ''.join(url)
        headers = self.get_header
        response = requests.get(url, headers=headers)
        result = pd.DataFrame(response.json())
        return result

    def site_search_engines(self, site_id):
        """
        :param site_id: ID проекта
        :return: json со списком поисковых систем проекта
        """

        url = [self.MANAGEMENT_URL, 'sites/', str(site_id), '/search-engines']
        url = ''.join(url)
        headers = self.get_header
        response = requests.get(url, headers=headers)
        result = pd.DataFrame(response.json())
        return result

    def site_keywords(self, site_id):
        """
        :param site_id: ID проекта
        :return: json со списком ключевых слов проекта
        """

        url = [self.MANAGEMENT_URL, 'sites/', str(site_id), '/keywords']
        url = ''.join(url)
        headers = self.get_header
        response = requests.get(url, headers=headers)
        result = pd.DataFrame(response.json())
        return result

    def keywords_statistics(self, site_id, date_from, date_to=now):
        """
        Возвращает статистику по ключевым словам
        :param site_id: идентификатор сайта
        :param date_from: дата начала сбора статистики
        :param date_to: дата конца сбора статистики
        :return: DataFrame со статистикой по ключевым словам
        """
        keywords_statistics_data = self.keywords_statistics_json(site_id, date_from, date_to)

        result = pd.DataFrame()
        norm = json_normalize(keywords_statistics_data, 'keywords', ['site_engine_id'])
        for i in range(len(norm)):
            cont = pd.DataFrame(norm.iloc[i]['positions'])
            cont['name'] = norm.iloc[i]['name']
            cont['competition'] = norm.iloc[i]['competition']
            cont['id'] = norm.iloc[i]['id']
            cont['kei'] = norm.iloc[i]['kei']
            cont['results'] = norm.iloc[i]['results']
            cont['volume'] = norm.iloc[i]['volume']
            cont['site_engine_id'] = norm.iloc[i]['site_engine_id']
            result = result.append(cont)
        return result

    def site_search_engines(self, site_id):
        """
        :param site_id: идентификатор сайта
        :return: DataFrame с поисковыми системами сайта
        """
        site_engines = self.site_search_engines(site_id)
        site_engines = pd.DataFrame(site_engines)
        search_engines = self.search_engines
        search_engines = pd.DataFrame(search_engines)[['id', 'name']]
        search_engines.id = search_engines.id.astype('int')
        site_engines.search_engine_id = site_engines.search_engine_id.astype('int')
        result = site_engines.merge(search_engines, left_on='search_engine_id', right_on='id', how='inner')
        return result
