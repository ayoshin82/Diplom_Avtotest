
import requests
import json
import allure
from constants import API1_url, bearer_token


@allure.description("Тестирование добавления товара в корзину на сайте Читай-город.")
class AddCartAPI:
    """Класс для работы с API добавления товара в корзину."""

    url = API1_url  # URL для добавления товара в корзину

    # Инициализация класса
    def __init__(self, url):
        """
                    Создает новый объект для работы с API.
        """
        self.url = url
        self.headers = {
            'Content-Type': 'application/json',  # Установка типа контента
            'Authorization': bearer_token  # Установка токена для авторизации
        }

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': bearer_token,
            'User-Agent': 'Mozilla/5.0',  # Добавить User-Agent
            'Accept': 'application/json'  # Добавить Accept
        }

    def add_product_to_cart(self, product_id: int, item_list_name: str) -> int:
        """             Добавляет товар в корзину и возвращает статус-код ответа.

                        Args:
                            product_id (int): ID товара для добавления.
                            item_list_name (str): Имя списка, к которому принадлежит товар.

                        Returns:
                            int: Статус-код ответа от сервера (например, 200 для успешного добавления).
        """
        # Данные для добавления товара
        payload = {
            "id": product_id,  # ID товара
            "adData": {
                "item_list_name": item_list_name,  # Имя списка товаров
            }
        }

        # Отправляем POST-запрос
        resp = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
        return resp.status_code  # Возвращаем статус-код ответа
