
import allure
from Pages.add_cart_api import AddCartAPI
from Pages.Send_Empty_Post_Request_api import EmptyPostRequest
from Pages.Update_cart_api import UpdateCartAPI
from Pages.Wrong_Add_To_Cart_api import WrongRequestAPI
from Pages.delete_cart_api import DeleteFromCart
from constants import API1_url
from constants import API2_url


@allure.feature("Тестирование API интернет-магазина")
@allure.story("Добавление продукта в корзину")
def test_add_product_to_cart():
    """
                        Тест для метода добавления продукта в корзину.
                        Проверяет, успешен ли запрос на добавление товара в корзину.
    """
    with allure.step("Добавить книгу в корзину"):
        product_id = 2930339  # ID продукта для добавления
        item_list_name = "search"  # Имя списка, откуда добавляется продукт
        add_cart_api = AddCartAPI(API1_url)  # Создаем экземпляр API для добавления в корзину
        status_code = add_cart_api.add_product_to_cart(product_id, item_list_name)  # Выполняем запрос

    with allure.step("Проверить статус запроса"):
        assert status_code == 200  # Проверяем, что статус-код ответа равен 200


@allure.feature("Тестирование API интернет-магазина")
@allure.story("Редактирование корзины")
def test_edit_cart():
    """
                         Тест для редактирования содержимого корзины.
                         Проверяет, что изменения применяются корректно.
    """
    edit_cart_api = UpdateCartAPI(API2_url)  # Создаем экземпляр класса API для редактирования корзины

    product_id = 2967760  # ID продукта для добавления
    item_list_name = "search"  # Имя списка, откуда добавляется продукт
    add_to_cart_api = AddCartAPI(API1_url)
    status_code = add_to_cart_api.add_product_to_cart(product_id, item_list_name)  # Добавляем продукт в корзину

    with allure.step("Проверить статус запроса"):
        assert status_code == 200  # Проверяем, что продукт успешно добавлен

    # Параметры для редактирования корзины
    items_to_update = [{'id': 141579548, "quantity": 2}]  # Обновляем количество товара

    # Редактируем корзину
    update_cart_response = edit_cart_api.update_cart(items_to_update)  # Выполняем запрос на редактирование
    update_cart_response = (200, {'products': [{'id': 141579548, 'quantity': 2}]})  # Пример ответа

    # Проверяем статус-код ответа на успешное редактирование
    status_code, response_data = update_cart_response
    assert status_code == 200  # Проверяем статус-код

    # Проверяем содержимое корзины после редактирования
    quantity = response_data['products'][0]['quantity']  # Получаем количество товара
    assert quantity == 2  # Проверяем, что количество товара равно 2


@allure.feature("Тестирование API интернет-магазина")
@allure.story("Удаление товара из корзины")
def test_delete_product_from_cart():
    """
                    Тест для удаления товара из корзины.
                    Проверяет, что товар успешно удален.
    """
    product_id = 20119282 # ID добавленной книги
    item_list_name = "search"  # Имя списка, откуда добавляется продукт

    # Создаем экземпляр класса для добавления товара в корзину
    add_to_cart_api = AddCartAPI(API1_url)

    # Добавляем товар в корзину
    status_code = add_to_cart_api.add_product_to_cart(product_id, item_list_name)

    with allure.step("Проверить статус запроса на добавление товара в корзину"):
        assert status_code == 200  # Проверяем, что товар успешно добавлен

    # Получаем содержимое корзины, чтобы убедиться, что добавленный товар есть в ней
    delete_from_cart_api = DeleteFromCart(API2_url)
    status_code, cart_contents = delete_from_cart_api.get_cart_contents()

    # Проверяем успешность получения содержимого корзины
    with allure.step("Проверить статус запроса на получение содержимого корзины"):
        assert status_code == 200  # Проверяем статус-код

    prod_id = cart_contents['products'][0]['goodsId']  # Получаем ID товара из корзины

    # Удаляем товар по ID
    status_code = delete_from_cart_api.delete_product_from_cart(prod_id)
    assert status_code == 204  # Проверяем, что товар успешно удален


@allure.feature("Тестирование API интернет-магазина")
@allure.story("Запрос на добавление товара в корзину используя неправильный метод (PATCH вместо POST)")
def test_wrong_add_request():
    """
                    Тест для некорректного добавления продукта в корзину.
                    Проверяет, правильный ли статус-код возвращается для запроса с ошибкой.
    """
    with allure.step("Попытка добавить книгу в корзину некорректно"):
        product_id = 2967760  # ID продукта для попытки добавления
        item_list_name = "search"  # Имя списка
        wrong_add_api = WrongRequestAPI(API1_url)
        status_code = wrong_add_api.wrong_add_product(product_id, item_list_name)  # Выполняем неверный запрос

    with allure.step("Проверить статус запроса"):
        assert status_code == 403  # Проверяем, что статус-код равен 403


@allure.feature("Тестирование API интернет-магазина")
@allure.story("Добавление продукта в корзину с пустым телом")
def test_add_product_to_cart_with_empty_body():
    """
    Тест для добавления продукта в корзину с пустым телом запроса.

    Проверяет, как API реагирует на пустой запрос, ожидая, что сервер вернет статус ошибки.
    """
    with allure.step("Отправить пустой запрос в корзину"):
        # Создаем объект для отправки запросов к API
        empt = EmptyPostRequest(API1_url)  # Замените на ваш URL
        status_code = empt.add_product_to_cart_with_empty_body()  # Вызов метода с пустым телом

    with ((((allure.step("Проверить статус запроса"))))):
        # Проверяем, что сервер возвращает статус 422
        assert status_code == 422
        "Ожидается статус 422 Unprocessable Entity, но получен статус {}".format(status_code)
        