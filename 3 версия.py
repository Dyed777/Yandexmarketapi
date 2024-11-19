import requests
import json
import logging
from typing import Dict, Optional

# Настройка логирования
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
def print_response(data: Optional[Dict], description: str):
    """
    Выводит данные в формате JSON с описанием, если данные не пусты.
    :param data: Ответ от API в виде словаря.
    :param description: Описание для вывода.
    """
    if data:
        print(f"{description}:", json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"Не удалось получить {description.lower()}.")
class YandexMarketAPI:
    BASE_URL = "https://api.partner.market.yandex.ru/v2"

    def __init__(self, client_id: str, api_key: str):
        self.client_id = client_id
        self.api_key = api_key
        self.headers = {
            "Api-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def _send_request(self, method: str, endpoint: str, req_params: Optional[Dict] = None,req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Отправляет запрос к API Яндекс Маркета.

        :param method: HTTP метод (GET, POST и т.д.).
        :param endpoint: Конечная точка API.
        :param req_params: Параметры URL (опционально).
        :param req_data: Данные JSON (опционально).
        :return: JSON-ответ в виде словаря или None в случае ошибки.
        """
        response = None
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, params=req_params, json=req_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response is not None:
                logging.error(f"HTTP ошибка: {http_err}")
                logging.error(f"Ответ сервера: {response.text}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Ошибка запроса: {req_err}")
        return None


    def get_campaigns(self) -> Optional[Dict]:
        """
        Получает список кампаний.
        :return: Словарь с данными о кампаниях или None в случае ошибки.
        """
        return self._send_request("GET", "campaigns")

    def get_campaign(self, camp_id: str) -> Optional[Dict]:
        """
        Получает данные конкретной кампании.
        :param camp_id: Идентификатор кампании.
        :return: Словарь с данными о кампании или None в случае ошибки.
        """
        return self._send_request("GET", f"campaigns/{camp_id}")

    def get_business_settings(self, biz_id: str, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает настройки указанного бизнеса.
        :param biz_id: Идентификатор бизнеса.
        :param req_data: Дополнительные данные запроса (опционально).
        :return: Словарь с настройками бизнеса или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/settings", req_data=req_data)

    def get_campaign_settings(self, camp_id: str) -> Optional[Dict]:
        """
        Получает настройки конкретной кампании.
        :param camp_id: Идентификатор кампании.
        :return: Словарь с настройками кампании или None в случае ошибки.
        """
        return self._send_request("GET", f"campaigns/{camp_id}/settings")

    def get_campaigns_hidden_offers(self, camp_id: str) -> Optional[Dict]:
        """
        Получает скрытые предложения для конкретной кампании.
        :param camp_id: Идентификатор кампании.
        :return: Словарь с данными о скрытых предложениях или None в случае ошибки.
        """
        return self._send_request("GET", f"campaigns/{camp_id}/hidden-offers")

    def get_business_offer_mappings(self, biz_id: str, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает маппинг предложений для бизнеса.
        :param biz_id: Идентификатор бизнеса.
        :param req_data: Данные запроса (опционально).
        :return: Словарь с данными о маппинге предложений или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/offer-mappings", req_data=req_data)

    def get_campaign_offers(self, camp_id: str, req_params: Optional[Dict] = None, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает предложения для указанной кампании.
        :param camp_id: Идентификатор кампании.
        :param req_params: Параметры запроса (опционально).
        :param req_data: Данные запроса (опционально).
        :return: Словарь с данными о предложениях или None в случае ошибки.
        """
        return self._send_request("POST", f"campaigns/{camp_id}/offers", req_params=req_params, req_data=req_data)

    def get_promos(self, biz_id: str, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает список акций для бизнеса.
        :param biz_id: Идентификатор бизнеса.
        :param req_data: Дополнительные данные запроса (опционально).
        :return: Словарь с данными об акциях или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/promos", req_data=req_data)

    def get_campaigns_orders(self, camp_id: str, limit: Optional[int] = None, page_token: Optional[str] = None) -> \
    Optional[Dict]:
        """
        Получает список заказов для кампании.
        :param camp_id: Идентификатор кампании.
        :param limit: Количество записей на одной странице (опционально).
        :param page_token: Токен для пагинации (опционально).
        :return: Словарь с данными о заказах или None в случае ошибки.
        """
        endpoint = f"campaigns/{camp_id}/orders"

        # Создаем словарь params, добавляя только непустые параметры
        params = {k: v for k, v in {"limit": limit, "page_token": page_token}.items() if v is not None}

        return self._send_request("GET", endpoint, req_params=params)

    def get_campaign_order(self, camp_id: str, ord_id: str) -> Optional[Dict]:
        """
        Получает данные конкретного заказа в кампании.
        :param camp_id: Идентификатор кампании.
        :param ord_id: Идентификатор заказа.
        :return: Словарь с данными о заказе или None в случае ошибки.
        """
        return self._send_request("GET", f"campaigns/{camp_id}/orders/{ord_id}")

    def get_returns_list(self, camp_id: str, req_params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает список возвратов для кампании.
        :param camp_id: Идентификатор кампании.
        :param req_params: Дополнительные параметры запроса (опционально).
        :return: Словарь с данными о возвратах или None в случае ошибки.
        """
        return self._send_request("GET", f"campaigns/{camp_id}/returns", req_params=req_params)

    def get_return_info(self, camp_id: int, ord_id: int, ret_id: int) -> Optional[Dict]:
        """
        Получает информацию о конкретном возврате.
        :param camp_id: Идентификатор кампании.
        :param ord_id: Идентификатор заказа.
        :param ret_id: Идентификатор возврата.
        :return: Словарь с информацией о возврате или None в случае ошибки.
        """
        return self._send_request("GET", f"campaigns/{camp_id}/orders/{ord_id}/returns/{ret_id}")

    def get_business_goods_feedback(self, biz_id: str, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает отзывы о товарах для бизнеса.
        :param biz_id: Идентификатор бизнеса.
        :param req_data: Данные запроса (опционально).
        :return: Словарь с данными об отзывах или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/goods-feedback", req_data=req_data)

    def get_business_quality_rating(self, biz_id: str, camp_ids: list[str]) -> Optional[Dict]:
        """
        Получает рейтинг качества для заданных кампаний бизнеса.
        :param biz_id: Идентификатор бизнеса.
        :param camp_ids: Список ID кампаний.
        :return: Словарь с рейтингом качества или None в случае ошибки.
        """
        data = {"campaignIds": camp_ids}
        return self._send_request("POST", f"businesses/{biz_id}/ratings/quality", req_data=data)

    def get_chats(self, biz_id: str, req_params: Optional[Dict] = None, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает чаты для указанного бизнеса.
        :param biz_id: Идентификатор бизнеса.
        :param req_params: Параметры запроса (опционально).
        :param req_data: Данные запроса (опционально).
        :return: Словарь с данными о чатах или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/chats", req_params=req_params, req_data=req_data)

    def get_warehouses(self) -> Optional[Dict]:
        """
        Получает список складов.
        :return: Словарь с данными о складах или None в случае ошибки.
        """
        return self._send_request("GET", "warehouses")

    def get_fulfillment_warehouses(self) -> Optional[Dict]:
        """
        Получает список складов с их идентификаторами.
        :return: Словарь с данными о складах с их идентификаторами или None в случае ошибки.
        """
        return self._send_request("GET", "warehouses")

    def get_regions(self, region_name: str = "") -> Optional[Dict]:
        """
        Получает информацию о регионах.
        :param region_name: Название региона для фильтрации (опционально).
        :return: Словарь с данными о регионах или None в случае ошибки.
        """
        params = {"name": region_name} if region_name else {}
        return self._send_request("GET", "regions", req_params=params)

    def get_region(self, region_id: str) -> Optional[Dict]:
        """
        Получает информацию о конкретном регионе.
        :param region_id: Идентификатор региона.
        :return: Словарь с данными о регионе или None в случае ошибки.
        """
        return self._send_request("GET", f"regions/{region_id}")

    def get_region_children(self, region_id: str) -> Optional[Dict]:
        """
        Получает информацию о подрегионах для указанного региона.
        :param region_id: Идентификатор региона.
        :return: Словарь с данными о подрегионах или None в случае ошибки.
        """
        return self._send_request("GET", f"regions/{region_id}/children")

    def get_delivery_services(self) -> Optional[Dict]:
        """
        Получает список доступных служб доставки.
        :return: Словарь с данными о службах доставки или None в случае ошибки.
        """
        return self._send_request("GET", "delivery/services")

    def get_stocks(self, camp_id: str, req_params: Optional[Dict] = None, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает информацию о запасах товаров для кампании.
        :param camp_id: Идентификатор кампании.
        :param req_params: Параметры запроса (опционально).
        :param req_data: Данные запроса (опционально).
        :return: Словарь с информацией о запасах или None в случае ошибки.
        """
        return self._send_request("POST", f"campaigns/{camp_id}/offers/stocks", req_params=req_params, req_data=req_data)

    def get_prices_by_offer_ids(self, camp_id: str, offer_ids: list[str]) -> Optional[Dict]:
        """
        Получает цены для товаров по их идентификаторам.
        :param camp_id: Идентификатор кампании.
        :param offer_ids: Список идентификаторов предложений.
        :return: Словарь с ценами или None в случае ошибки.
        """
        data = {"offerIds": offer_ids}
        return self._send_request("POST", f"campaigns/{camp_id}/offer-prices", req_data=data)

    def get_business_quarantine_offers(self, biz_id: str, req_params: Optional[Dict] = None, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает список товаров, находящихся в карантине по ценам для бизнеса.
        :param biz_id: Идентификатор бизнеса.
        :param req_params: Параметры запроса (опционально).
        :param req_data: Данные запроса (опционально).
        :return: Словарь с данными о товарах в карантине или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/price-quarantine", req_params=req_params, req_data=req_data)

    def get_campaign_quarantine_offers(self, camp_id: str, req_params: Optional[Dict] = None, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает список товаров, находящихся в карантине по ценам для кампании.
        :param camp_id: Идентификатор кампании.
        :param req_params: Параметры запроса (опционально).
        :param req_data: Данные запроса (опционально).
        :return: Словарь с данными о товарах в карантине или None в случае ошибки.
        """
        return self._send_request("POST", f"campaigns/{camp_id}/price-quarantine", req_params=req_params, req_data=req_data)

    def get_offer_cards_content_status(self, biz_id: str, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает статус контента карточек предложений.
        :param biz_id: Идентификатор бизнеса.
        :param req_data: Данные запроса (опционально).
        :return: Словарь с данными о статусе карточек или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/offer-cards", req_data=req_data)

    def get_suggested_offer_mappings(self, biz_id: str, offers: list[Dict]) -> Optional[Dict]:
        """
        Получает предложенные маппинги для товаров бизнеса.
        :param biz_id: Идентификатор бизнеса.
        :param offers: Список товаров для маппинга.
        :return: Словарь с предложениями маппинга или None в случае ошибки.
        """
        data = {"offers": offers}
        return self._send_request("POST", f"businesses/{biz_id}/offer-mappings/suggestions", req_data=data)

    def get_model_info(self, model_id: int, region_id: int, currency: str = "RUR") -> Optional[Dict]:
        """
        Получает информацию о модели товара.
        :param model_id: Идентификатор модели.
        :param region_id: Идентификатор региона.
        :param currency: Валюта (по умолчанию RUR).
        :return: Словарь с информацией о модели или None в случае ошибки.
        """
        params = {
            "regionId": region_id,
            "currency": currency
        }
        return self._send_request("GET", f"models/{model_id}", req_params=params)

    def get_models_info(self, model_ids: list[int], region_id: int, currency: str = "RUR") -> Optional[Dict]:
        """
        Получает информацию о нескольких моделях товаров.
        :param model_ids: Список идентификаторов моделей (до 100 элементов).
        :param region_id: Идентификатор региона.
        :param currency: Валюта (по умолчанию RUR).
        :return: Словарь с информацией о моделях или None в случае ошибки.
        """
        if not model_ids or len(model_ids) > 100:
            logging.error("Список model_ids должен содержать от 1 до 100 элементов.")
            return None

        params = {
            "regionId": region_id,
            "currency": currency
        }
        data = {
            "models": model_ids
        }
        return self._send_request("POST", "models", req_params=params, req_data=data)

    def get_model_offers(self, model_id: int, region_id: int, count: int = 10, currency: str = "RUR",
                         order_by_price: Optional[str] = None, page: int = 1) -> Optional[Dict]:
        """
        Получает предложения для модели товара.
        :param model_id: Идентификатор модели.
        :param region_id: Идентификатор региона.
        :param count: Количество предложений (от 1 до 100).
        :param currency: Валюта (по умолчанию RUR).
        :param order_by_price: Сортировка по цене ('ASC' или 'DESC') (опционально).
        :param page: Номер страницы.
        :return: Словарь с предложениями для модели или None в случае ошибки.
        """
        # Проверка допустимого значения для count
        if count < 1 or count > 100:
            logging.error("Параметр 'count' должен быть в диапазоне от 1 до 100.")
            return None

        # Создаем словарь params, добавляя order_by_price только если он корректен
        params = {
            "regionId": region_id,
            "count": count,
            "currency": currency,
            "page": page,
            **({"orderByPrice": order_by_price.upper()} if order_by_price and order_by_price.upper() in ["ASC","DESC"] else {})
        }
        return self._send_request("GET", f"models/{model_id}/offers", req_params=params)

    def search_models(self, query: str, region_id: int, currency: str = "RUR", page: int = 1, page_size: int = 10, ) -> Optional[Dict]:
        """
        Ищет модели товаров по заданному запросу.
        :param query: Поисковый запрос.
        :param region_id: Идентификатор региона.
        :param currency: Валюта (по умолчанию RUR).
        :param page: Номер страницы.
        :param page_size: Размер страницы (по умолчанию 10).
        :return: Словарь с данными о найденных моделях или None в случае ошибки.
        """
        if not query:
            logging.error("Параметр 'query' не должен быть пустым.")
            return None

        params = {
            "query": query,
            "regionId": region_id,
            "currency": currency,
            "page": page,
            "pageSize": page_size,

        }
        return self._send_request("GET", "models", req_params=params)

    def get_goods_feedback_comments(self, biz_id: str, feedback_id: int, page_token: Optional[str] = None) -> Optional[
        Dict]:
        """
        Получение комментариев к отзыву о товаре.
        :param biz_id: Идентификатор бизнеса.
        :param feedback_id: Идентификатор отзыва.
        :param page_token: Токен для пагинации (опционально).
        :return: Словарь с данными о комментариях или None в случае ошибки.
        """
        endpoint = f"businesses/{biz_id}/goods-feedback/comments"
        params = {}
        if page_token:
            params['page_token'] = page_token
        data = {"feedbackId": feedback_id}
        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def get_promo_offers(self, business_id: int, promo_id: str, status_type: Optional[str] = None, limit: Optional[int] = None, page_token: Optional[str] = None) -> Optional[Dict]:
        """
        Получение списка товаров, участвующих в акции.
        :param business_id: Идентификатор бизнеса.
        :param promo_id: Идентификатор акции.
        :param status_type: Фильтр по статусу участия (опционально).
        :param limit: Количество записей на одной странице (опционально).
        :param page_token: Токен для пагинации (опционально).
        :return: Словарь с данными о товарах или None в случае ошибки.
        """
        endpoint = f"businesses/{business_id}/promos/offers"

        # Создаем словарь params, добавляя только непустые параметры
        params = {k: v for k, v in {"limit": limit, "page_token": page_token}.items() if v is not None}

        # Создаем словарь data с promoId и только непустым statusType
        data = {k: v for k, v in {"promoId": promo_id, "statusType": status_type}.items() if v is not None}

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def get_bids_recommendations(self, business_id: int, skus: list[str]) -> Optional[Dict]:
        """
        Получает рекомендации по ставкам для товаров.
        :param business_id: Идентификатор бизнеса.
        :param skus: Список SKU товаров.
        :return: Словарь с рекомендациями по ставкам или None в случае ошибки.
        """
        endpoint = f"businesses/{business_id}/bids/recommendations"
        data = {"skus": skus}
        return self._send_request("POST", endpoint, req_data=data)

    def get_bids_info(self, business_id: int, skus: Optional[list[str]] = None, limit: Optional[int] = None,
                      page_token: Optional[str] = None) -> Optional[Dict]:
        """
        Получает информацию о ставках для товаров.
        :param business_id: Идентификатор бизнеса.https://github.com/Dyed777/Yandexmarketapi
        :param skus: Список SKU товаров (опционально).
        :param limit: Количество записей на одной странице (опционально).
        :param page_token: Токен для пагинации (опционально).
        :return: Словарь с данными о ставках или None в случае ошибки.
        """
        endpoint = f"businesses/{business_id}/bids/info"

        # Создаем словарь params с непустыми значениями
        params = {k: v for k, v in {"limit": limit, "page_token": page_token}.items() if v is not None}

        # Создаем словарь data с непустым значением skus
        data = {k: v for k, v in {"skus": skus}.items() if v is not None}

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def get_offer_recommendations(self, business_id: int, offer_ids: Optional[list[str]] = None, cofinance_price_filter: Optional[str] = None, recommended_cofinance_price_filter: Optional[str] = None,competitiveness_filter: Optional[str] = None, limit: Optional[int] = None,page_token: Optional[str] = None) -> Optional[Dict]:
        """
        Получает рекомендации по ценам для товаров.
        :param business_id: Идентификатор бизнеса.
        :param offer_ids: Список идентификаторов товаров (опционально).
        :param cofinance_price_filter: Фильтр по ценам для софинансирования (опционально).
        :param recommended_cofinance_price_filter: Фильтр по рекомендованным ценам для софинансирования (опционально).
        :param competitiveness_filter: Фильтр по конкурентоспособности цен (опционально).
        :param limit: Количество значений на одной странице (опционально).
        :param page_token: Токен для пагинации (опционально).
        :return: Словарь с рекомендациями или None в случае ошибки.
        """
        endpoint = f"businesses/{business_id}/offers/recommendations"

        # Создаем словари params и data, добавляя только непустые параметры
        params = {k: v for k, v in {"limit": limit, "page_token": page_token}.items() if v is not None}
        data = {k: v for k, v in {
            "offerIds": offer_ids,
            "cofinancePriceFilter": cofinance_price_filter,
            "recommendedCofinancePriceFilter": recommended_cofinance_price_filter,
            "competitivenessFilter": competitiveness_filter
        }.items() if v is not None}

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def calculate_tariffs(self, offers: list[Dict], campaign_id: Optional[int] = None,
                          selling_program: Optional[str] = None, frequency: Optional[str] = None) -> Optional[Dict]:
        """
        Рассчитывает тарифы для указанных товаров.
        :param offers: Список товаров.
        :param campaign_id: Идентификатор кампании (опционально).
        :param selling_program: Программа продаж FBY DBS FBS(опционально).
        :param frequency: Частота платежей (опционально).
        :return: Словарь с рассчитанными тарифами или None в случае ошибки.
        """
        endpoint = "tariffs/calculate"

        # Создаем словарь parameters с непустыми значениями
        parameters = {k: v for k, v in {
            "campaignId": campaign_id,
            "sellingProgram": selling_program,
            "frequency": frequency
        }.items() if v is not None}

        # Формируем данные для запроса
        data = {
            "offers": offers,
            "parameters": parameters
        }
        return self._send_request("POST", endpoint, req_data=data)

    def get_categories_tree(self, language: str = "RU") -> Optional[Dict]:
        """
        Получает дерево категорий Яндекс Маркета.
        :param language: Язык категорий (по умолчанию "RU").
        :return: Словарь с деревом категорий или None в случае ошибки.
        """
        data = {"language": language}
        return self._send_request("POST", "categories/tree", req_data=data)

    def get_categories_max_sale_quantum(self, category_ids: list[int]) -> Optional[Dict]:
        """
        Получает максимальные лимиты продажи и минимальное количество заказа для указанных категорий.
        :param category_ids: Список идентификаторов категорий.
        :return: Словарь с информацией о максимальных квотах продажи для категорий или None в случае ошибки.
        """
        if not category_ids:
            logging.error("Список 'category_ids' не должен быть пустым.")
            return None

        data = {"marketCategoryIds": category_ids}
        return self._send_request("POST", "categories/max-sale-quantum", req_data=data)

    def get_category_content_parameters(self, category_id: int) -> Optional[Dict]:
        """
        Получает список характеристик товаров с допустимыми значениями для указанной категории.

        :param category_id: Идентификатор категории на Яндекс.Маркете.
        :return: Словарь с параметрами категории или None в случае ошибки.
        """
        endpoint = f"category/{category_id}/parameters"
        return self._send_request("POST", endpoint)

    def generate_goods_feedback_report(self, business_id: int, format: str = "FILE") -> Optional[Dict]:
        """
        Инициирует генерацию отчета по отзывам о товарах.

        :param business_id: Идентификатор бизнеса.
        :param format: Формат отчета ('FILE' или 'CSV'). По умолчанию 'FILE'.
        :return: Словарь с информацией о статусе генерации отчета или None в случае ошибки.
        """
        # Проверка допустимых значений для параметра format
        if format not in ["FILE", "CSV"]:
            logging.error("Недопустимое значение параметра 'format'. Используйте 'FILE' или 'CSV'.")
            return None

        # Формирование данных для запроса
        data = {"businessId": business_id}
        params = {"format": format}

        # Отправка POST-запроса
        return self._send_request("POST", "reports/goods-feedback/generate", req_params=params, req_data=data)

    def create_chat(self, business_id: int, order_id: int) -> Optional[Dict]:
        """
        Создаёт новый чат с покупателем.

        :param business_id: Идентификатор бизнеса.
        :param order_id: Идентификатор заказа.
        :return: Словарь с данными о созданном чате или None в случае ошибки.
        """
        endpoint = f"businesses/{business_id}/chats/new"
        data = {"orderId": order_id}
        return self._send_request("POST", endpoint, req_data=data)

    def send_message_to_chat(self, business_id: int, chat_id: int, message: str) -> Optional[Dict]:
        """
        Отправляет сообщение в указанный чат.

        :param business_id: Идентификатор бизнеса.
        :param chat_id: Идентификатор чата.
        :param message: Текст сообщения.
        :return: Ответ от API или None в случае ошибки.
        """
        endpoint = f"businesses/{business_id}/chats/message"
        params = {"chatId": chat_id}
        data = {"message": message}
        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def send_file_to_chat(self, business_id: int, chat_id: int, file_path: str) -> Optional[Dict]:
        """
        Отправляет файл в указанный чат с покупателем.

        :param business_id: Идентификатор бизнеса.
        :param chat_id: Идентификатор чата.
        :param file_path: Путь к файлу для отправки.
        :return: Ответ от API или None в случае ошибки.
        """
        endpoint = f"businesses/{business_id}/chats/file/send"
        params = {"chatId": chat_id,
                  "file_path": file_path}
        return self._send_request("POST", endpoint, req_params=params)

    def get_chat_history(self, business_id: int, chat_id: int, message_id_from: Optional[int] = None,limit: Optional[int] = None, page_token: Optional[str] = None) -> Optional[Dict]:
        """
        Получает историю сообщений в чате с покупателем.

        :param business_id: Идентификатор бизнеса.
        :param chat_id: Идентификатор чата.
        :param message_id_from: Идентификатор сообщения, начиная с которого нужно получить все последующие сообщения (опционально).
        :param limit: Количество сообщений на одной странице (опционально).
        :param page_token: Токен для пагинации (опционально).
        :return: Словарь с историей сообщений или None в случае ошибки.
        """
        endpoint = f"businesses/{business_id}/chats/history"
        params = {key: value for key, value in {"chatId": chat_id, "limit": limit, "page_token": page_token}.items() if
                  value is not None}
        data = {key: value for key, value in {"messageIdFrom": message_id_from}.items() if value is not None}
        return self._send_request("POST", endpoint, req_params=params,req_data=data)

    def update_goods_feedback_comment(self, business_id: int, feedback_id: int, text: str,
                                      comment_id: Optional[int] = None) -> Optional[Dict]:
        """
        Добавляет или обновляет комментарий к отзыву о товаре.

        :param business_id: Идентификатор бизнеса.
        :param feedback_id: Идентификатор отзыва.
        :param text: Текст комментария.
        :param comment_id: Идентификатор комментария (опционально). Если указан, комментарий будет обновлен; если нет — создан новый.
        :return: Словарь с данными о комментарии или None в случае ошибки.
        """
        endpoint = f"businesses/{business_id}/goods-feedback/comments/update"
        data = {
            "feedbackId": feedback_id,
            "text": text
        }
        if comment_id is not None:
            data["commentId"] = comment_id

        return self._send_request("POST", endpoint, req_data=data)

    def skip_goods_feedbacks_reaction(self, business_id: int, feedback_ids: list[int]) -> Optional[Dict]:
        """
        Пропускает отзывы, требующие реакции, для указанного бизнеса.

        :param business_id: Идентификатор бизнеса.
        :param feedback_ids: Список идентификаторов отзывов, которые нужно пропустить.
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        endpoint = f"businesses/{business_id}/goods-feedback/skip-reaction"
        data = {"feedbackIds": feedback_ids}
        return self._send_request("POST", endpoint, req_data=data)

    def delete_goods_feedback_comment(self, business_id: int, comment_id: int) -> Optional[Dict]:
        """
        Удаляет комментарий к отзыву о товаре.

        :param business_id: Идентификатор бизнеса.
        :param comment_id: Идентификатор комментария.
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        endpoint = f"businesses/{business_id}/goods-feedback/comments/delete"
        data = {
            "id": comment_id
        }
        return self._send_request("POST", endpoint, req_data=data)

    def put_bids_for_business(self, business_id: int, bids: list[Dict[str, str | int]]) -> Optional[Dict]:
        """
        Устанавливает или обновляет ставки на товары для продвижения.

        :param business_id: Идентификатор бизнеса.
        :param bids: Список словарей с информацией о товарах и их ставках. Каждый словарь должен содержать ключи:
                     - 'sku': строка, идентификатор товара (SKU).
                     - 'bid': целое число, ставка в процентах от стоимости товара, умноженная на 100.
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        endpoint = f"businesses/{business_id}/bids"
        data = {"bids": bids}
        return self._send_request("PUT", endpoint, req_data=data)

    def update_stocks(self, business_id: int, warehouse_id: int, stocks: list[Dict]) -> Optional[Dict]:
        """
        Обновляет остатки товаров на складе.

        :param business_id: Идентификатор бизнеса.
        :param warehouse_id: Идентификатор склада.
        :param stocks: Список остатков товаров (ID товара и количество).
            Пример:
            [
                {"sku": "12345", "warehouseId": 1, "items": [{"count": 10}]},
                {"sku": "67890", "warehouseId": 1, "items": [{"count": 5}]}
            ]
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        endpoint = f"businesses/{business_id}/stocks"
        data = {
            "warehouseId": warehouse_id,
            "stocks": stocks
        }
        return self._send_request("POST", endpoint, req_data=data)

    def get_orders_stats(self, campaign_id: int, date_from: str, date_to: str, statuses: Optional[list[str]] = None,
                         has_cis: Optional[bool] = None) -> Optional[Dict]:
        """
        Получает детальную информацию по заказам.

        :param campaign_id: Идентификатор кампании.
        :param date_from: Начальная дата формирования заказа (формат 'ГГГГ-ММ-ДД').
        :param date_to: Конечная дата формирования заказа (формат 'ГГГГ-ММ-ДД').
        :param statuses: Список статусов заказов для фильтрации.
        :param has_cis: Фильтр по наличию товаров с кодом идентификации.
        :return: Словарь с информацией о заказах или None в случае ошибки.
        """
        endpoint = f"campaigns/{campaign_id}/stats/orders"
        data = {
            "dateFrom": date_from,
            "dateTo": date_to,
        }
        if statuses:
            data["statuses"] = statuses
        if has_cis is not None:
            data["hasCis"] = has_cis

        return self._send_request("POST", endpoint, req_data=data)

    def generate_shows_sales_report(self, date_from: str, date_to: str, grouping: str,
                                    business_id: Optional[int] = None, campaign_id: Optional[int] = None,
                                    report_format: str = 'FILE') -> Optional[Dict]:
        """
        Генерирует отчет «Аналитика продаж» за указанный период.

        :param date_from: Начало периода (в формате 'YYYY-MM-DD').
        :param date_to: Конец периода (в формате 'YYYY-MM-DD').
        :param grouping: Группировка данных ('CATEGORIES' или 'OFFERS').
        :param business_id: Идентификатор бизнеса (если не указан campaign_id).
        :param campaign_id: Идентификатор кампании (если не указан business_id).
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        # Проверка условий
        if not (bool(business_id) ^ bool(campaign_id)):
            logging.error("Укажите ровно один параметр: либо business_id, либо campaign_id.")
            return None

        endpoint = "reports/shows-sales/generate"
        params = {'format': report_format}
        data = {
            "dateFrom": date_from,
            "dateTo": date_to,
            "grouping": grouping,
            "businessId": business_id or None,
            "campaignId": campaign_id or None
        }

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def generate_boost_consolidated_report(self, business_id: int, date_from: str, date_to: str,
                                           report_format: str = 'FILE') -> Optional[Dict]:
        """
        Генерирует сводный отчет по бусту продаж за указанный период.

        :param business_id: Идентификатор бизнеса.
        :param date_from: Начало периода (в формате 'YYYY-MM-DD').
        :param date_to: Конец периода (в формате 'YYYY-MM-DD').
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        endpoint = "reports/boost-consolidated/generate"
        params = {'format': report_format}
        data = {
            "businessId": business_id,
            "dateFrom": date_from,
            "dateTo": date_to
        }

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def generate_goods_movement_report(self, campaign_id: int, date_from: str, date_to: str,
                                       report_format: str = 'FILE', shop_sku: Optional[str] = None) -> Optional[Dict]:
        """
        Генерирует отчет по движению товаров (FBY) за указанный период.

        :param campaign_id: Идентификатор кампании.
        :param date_from: Начало периода (в формате 'YYYY-MM-DD').
        :param date_to: Конец периода (в формате 'YYYY-MM-DD').
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :param shop_sku: SKU товара для фильтрации (опционально).
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        endpoint = "reports/goods-movement/generate"
        params = {'format': report_format}
        data = {
            "campaignId": campaign_id,
            "dateFrom": date_from,
            "dateTo": date_to
        }
        if shop_sku:
            data["shopSku"] = shop_sku

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def generate_united_orders_report(self, business_id: int, date_from: str, date_to: str, report_format: str = 'FILE',
                                      campaign_ids: Optional[list[int]] = None, promo_id: Optional[str] = None) -> \
    Optional[Dict]:
        """
        Генерирует отчет по заказам за указанный период.

        :param business_id: Идентификатор бизнеса.
        :param date_from: Начало периода (в формате 'YYYY-MM-DD').
        :param date_to: Конец периода (в формате 'YYYY-MM-DD').
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :param campaign_ids: Список идентификаторов кампаний (опционально).
        :param promo_id: Идентификатор акции (опционально).
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        endpoint = "reports/united-orders/generate"
        params = {'format': report_format}
        data = {
            "businessId": business_id,
            "dateFrom": date_from,
            "dateTo": date_to
        }
        if campaign_ids:
            data["campaignIds"] = campaign_ids
        if promo_id:
            data["promoId"] = promo_id

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def generate_competitors_position_report(self, business_id: int, category_id: int, date_from: str, date_to: str,
                                             report_format: str = 'FILE') -> Optional[Dict]:
        """
        Генерирует отчет «Конкурентная позиция» за указанный период.

        :param business_id: Идентификатор бизнеса.
        :param category_id: Идентификатор категории.
        :param date_from: Начало периода (в формате 'YYYY-MM-DD').
        :param date_to: Конец периода (в формате 'YYYY-MM-DD').
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        endpoint = "reports/competitors-position/generate"
        params = {'format': report_format}
        data = {
            "businessId": business_id,
            "categoryId": category_id,
            "dateFrom": date_from,
            "dateTo": date_to
        }

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def generate_goods_turnover_report(self, campaign_id: int, report_date: Optional[str] = None,
                                       report_format: str = 'FILE') -> Optional[Dict]:
        """
        Генерирует отчет по оборачиваемости товаров (FBY) за указанную дату.

        :param campaign_id: Идентификатор кампании.
        :param report_date: Дата отчета (в формате 'YYYY-MM-DD'). Если не указана, используется текущая дата.
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        endpoint = "reports/goods-turnover/generate"
        params = {'format': report_format}
        data = {
            "campaignId": campaign_id
        }
        if report_date:
            data["date"] = report_date

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def generate_stocks_on_warehouses_report(self, campaign_id: int, warehouse_ids: Optional[list[int]] = None,
                                             report_date: Optional[str] = None,
                                             category_ids: Optional[list[int]] = None,
                                             has_stocks: Optional[bool] = None, report_format: str = 'FILE') -> \
    Optional[Dict]:
        """
        Генерирует отчет по остаткам на складах.

        :param campaign_id: Идентификатор кампании.
        :param warehouse_ids: Список идентификаторов складов (только для модели FBY).
        :param report_date: Дата отчета (в формате 'YYYY-MM-DD') для модели FBY. В отчет попадут данные за предшествующий дате день.
        :param category_ids: Список идентификаторов категорий на Маркете (кроме модели FBY).
        :param has_stocks: Фильтр по наличию остатков (кроме модели FBY).
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        endpoint = "reports/stocks-on-warehouses/generate"
        params = {'format': report_format}
        data = {
            "campaignId": campaign_id,
            "warehouseIds": warehouse_ids,
            "reportDate": report_date,
            "categoryIds": category_ids,
            "hasStocks": has_stocks
        }
        # Удаляем ключи с значением None
        data = {k: v for k, v in data.items() if v is not None}

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def generate_united_netting_report(self, business_id: int, date_from: Optional[str] = None,
                                       date_to: Optional[str] = None,
                                       bank_order_id: Optional[int] = None, bank_order_date_time: Optional[str] = None,
                                       campaign_ids: Optional[list[int]] = None, inns: Optional[list[str]] = None,
                                       placement_programs: Optional[list[str]] = None, report_format: str = 'FILE') -> \
    Optional[Dict]:
        """
        Генерирует отчет по платежам за указанный период или по платежному поручению.

        :param business_id: Идентификатор бизнеса.
        :param date_from: Начало периода (в формате 'YYYY-MM-DD').
        :param date_to: Конец периода (в формате 'YYYY-MM-DD'). Максимальный период — 3 месяца.
        :param bank_order_id: Номер платежного поручения.
        :param bank_order_date_time: Дата платежного поручения (в формате 'YYYY-MM-DDTHH:MM:SSZ').
        :param campaign_ids: Список идентификаторов кампаний.
        :param inns: Список ИНН.
        :param placement_programs: Список моделей, по которым работает магазин ('FBS', 'FBY', 'DBS').
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        endpoint = "reports/united-netting/generate"
        params = {'format': report_format}
        data = {
            "businessId": business_id,
            "dateFrom": date_from,
            "dateTo": date_to,
            "bankOrderId": bank_order_id,
            "bankOrderDateTime": bank_order_date_time,
            "campaignIds": campaign_ids,
            "inns": inns,
            "placementPrograms": placement_programs
        }
        # Удаляем ключи с значением None
        data = {k: v for k, v in data.items() if v is not None}

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def generate_shelfs_statistics_report(self, business_id: int, date_from: str, date_to: str,
                                          attribution_type: str = 'CLICKS', report_format: str = 'FILE') -> Optional[
        Dict]:
        """
        Генерирует сводный отчет по полкам за указанный период.

        :param business_id: Идентификатор бизнеса.
        :param date_from: Начало периода (в формате 'YYYY-MM-DD').
        :param date_to: Конец периода (в формате 'YYYY-MM-DD').
        :param attribution_type: Тип атрибуции ('CLICKS' или 'SHOWS').
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        endpoint = "reports/shelf-statistics/generate"
        params = {'format': report_format}
        data = {
            "businessId": business_id,
            "dateFrom": date_from,
            "dateTo": date_to,
            "attributionType": attribution_type
        }

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def generate_goods_realization_report(self, campaign_id: int, year: int, month: int, report_format: str = 'FILE') -> \
    Optional[Dict]:
        """
        Генерирует отчет по реализации товаров за указанный месяц.

        :param campaign_id: Идентификатор кампании.
        :param year: Год отчета.
        :param month: Месяц отчета (1-12).
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        endpoint = "reports/goods-realization/generate"
        params = {'format': report_format}
        data = {
            "campaignId": campaign_id,
            "year": year,
            "month": month
        }

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def generate_united_marketplace_services_report(self, business_id: int, date_from: Optional[str] = None,
                                                    date_to: Optional[str] = None, year: Optional[int] = None,
                                                    month: Optional[int] = None, report_format: str = 'FILE',
                                                    campaign_ids: Optional[list[int]] = None,
                                                    inns: Optional[list[str]] = None) -> Optional[Dict]:
        """
        Генерирует отчет по стоимости услуг за указанный период.

        :param business_id: Идентификатор бизнеса.
        :param date_from: Начало периода (в формате 'YYYY-MM-DD') для отчета по дате начисления услуги.
        :param date_to: Конец периода (в формате 'YYYY-MM-DD') для отчета по дате начисления услуги.
        :param year: Год формирования акта для отчета по дате формирования акта.
        :param month: Месяц формирования акта (1-12) для отчета по дате формирования акта.
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :param campaign_ids: Список идентификаторов кампаний (опционально).
        :param inns: Список ИНН (опционально).
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        endpoint = "reports/united-marketplace-services/generate"
        params = {'format': report_format}

        # Формируем словарь с параметрами, исключая пустые значения
        data = {
            "businessId": business_id,
            "dateFrom": date_from,
            "dateTo": date_to,
            "year": year,
            "month": month,
            "campaignIds": campaign_ids,
            "inns": inns
        }
        # Исключаем ключи с None значениями
        data = {k: v for k, v in data.items() if v is not None}

        # Проверка на наличие необходимых параметров
        if not ({"dateFrom", "dateTo"} <= data.keys() or {"year", "month"} <= data.keys()):
            logging.error("Необходимо указать либо 'date_from' и 'date_to', либо 'year' и 'month'.")
            return None

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def get_goods_stats(self, campaign_id: int, shop_skus: list[str]) -> Optional[Dict]:
        """
        Получает подробный отчет по товарам, размещенным на Маркете.

        :param campaign_id: Идентификатор кампании.
        :param shop_skus: Список ваших идентификаторов SKU.
        :return: Словарь с информацией о товарах или None в случае ошибки.
        """
        endpoint = f"campaigns/{campaign_id}/stats/skus"
        data = {
            "shopSkus": shop_skus
        }

        return self._send_request("POST", endpoint, req_data=data)

    def generate_prices_report(self, business_id: Optional[int] = None, campaign_id: Optional[int] = None,
                               category_ids: Optional[list[int]] = None, creation_date_from: Optional[str] = None,
                               creation_date_to: Optional[str] = None, report_format: str = 'FILE') -> Optional[Dict]:
        """
        Генерирует отчет «Цены на рынке».

        :param business_id: Идентификатор бизнеса (если не указан campaign_id).
        :param campaign_id: Идентификатор кампании (если не указан business_id).
        :param category_ids: Список идентификаторов категорий для фильтрации (опционально).
        :param creation_date_from: Начальная дата появления предложения (в формате 'ДД-ММ-ГГГГ', опционально).
        :param creation_date_to: Конечная дата появления предложения (в формате 'ДД-ММ-ГГГГ', опционально).
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        # Проверка условий
        if not (bool(business_id) ^ bool(campaign_id)):
            logging.error("Укажите ровно один параметр: либо business_id, либо campaign_id.")
            return None

        endpoint = "reports/prices/generate"
        params = {'format': report_format}
        data = {
            "businessId": business_id,
            "campaignId": campaign_id,
            "categoryIds": category_ids,
            "creationDateFrom": creation_date_from,
            "creationDateTo": creation_date_to
        }
        # Исключаем ключи с None значениями
        data = {k: v for k, v in data.items() if v is not None}

        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def get_report_info(self, report_id: str) -> Optional[Dict]:
        """
        Получает статус генерации отчета и ссылку на готовый отчет.

        :param report_id: Идентификатор отчета, полученный после запуска генерации.
        :return: Словарь с информацией о статусе отчета или None в случае ошибки.
        """
        endpoint = f"reports/info/{report_id}"
        return self._send_request("GET", endpoint)

    def update_business_prices(self, business_id: int, offers: list[Dict]) -> Optional[Dict]:
        """
        Обновляет базовые цены на товары для всех магазинов, связанных с указанным бизнесом.

        :param business_id: Идентификатор бизнеса.
        :param offers: Список товаров с новыми ценами. Пример:
            [
                {
                    "offerId": "SKU123",
                    "price": {
                        "value": 1000,
                        "currencyId": "RUR",
                        "discountBase": 1200
                    }
                }
            ]
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        # Проверка входных данных
        if not offers or not isinstance(offers, list):
            logging.error("Параметр 'offers' должен быть непустым списком.")
            return None

        endpoint = f"businesses/{business_id}/offer-prices/updates"
        data = {"offers": offers}

        return self._send_request("POST", endpoint, req_data=data)

    def update_store_prices(self, campaign_id: int, offers: list[Dict]) -> Optional[Dict]:
        """
        Обновляет цены на товары в указанном магазине.

        :param campaign_id: Идентификатор кампании (магазина) в API.
        :param offers: Список товаров с новыми ценами. Пример:
            [
                {
                    "offerId": "SKU123",
                    "price": {
                        "value": 1000,
                        "currencyId": "RUR",
                        "discountBase": 1200,
                        "vat": 7
                    }
                }
            ]
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        # Проверка входных данных
        if not offers or not isinstance(offers, list):
            logging.error("Параметр 'offers' должен быть непустым списком.")
            return None

        endpoint = f"campaigns/{campaign_id}/offer-prices/updates"
        data = {"offers": offers}

        return self._send_request("POST", endpoint, req_data=data)

    def update_promo_offers(self, business_id: int, promo_id: str, offers: list[Dict]) -> Optional[Dict]:
        """
        Добавляет товары в акцию или изменяет их цены.

        :param business_id: Идентификатор бизнеса.
        :param promo_id: Идентификатор акции.
        :param offers: Список товаров с параметрами для акции. Пример:
            [
                {
                    "offerId": "SKU123",
                    "params": {
                        "discountParams": {
                            "price": 1000,
                            "promoPrice": 800
                        }
                    }
                }
            ]
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        # Проверка входных данных
        if not offers or not isinstance(offers, list):
            logging.error("Параметр 'offers' должен быть непустым списком.")
            return None

        endpoint = f"businesses/{business_id}/promos/offers/update"
        data = {
            "promoId": promo_id,
            "offers": offers
        }

        return self._send_request("POST", endpoint, req_data=data)

    def delete_promo_offers(self, business_id: int, promo_id: str, offer_ids: Optional[list[str]] = None,
                            delete_all_offers: bool = False) -> Optional[Dict]:
        """
        Удаляет товары из акции.

        :param business_id: Идентификатор бизнеса.
        :param promo_id: Идентификатор акции.
        :param offer_ids: Список SKU товаров для удаления из акции. Если None, будет использоваться параметр delete_all_offers.
        :param delete_all_offers: Если True, удаляет все товары из акции.
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        if not offer_ids and not delete_all_offers:
            logging.error("Необходимо указать либо 'offer_ids', либо установить 'delete_all_offers' в True.")
            return None

        if offer_ids and delete_all_offers:
            logging.error("Нельзя одновременно указывать 'offer_ids' и устанавливать 'delete_all_offers' в True.")
            return None

        endpoint = f"businesses/{business_id}/promos/offers/delete"
        data = {
            "promoId": promo_id,
            "deleteAllOffers": delete_all_offers,
            "offerIds": offer_ids
        }

        return self._send_request("POST", endpoint, req_data=data)

    def update_offer_mappings(self, business_id: int, offer_mappings: list[Dict],
                              only_partner_media_content: bool = False) -> Optional[Dict]:
        """
        Добавляет или обновляет информацию о товарах в каталоге.

        :param business_id: Идентификатор бизнеса в Яндекс.Маркете.
        :param offer_mappings: Список словарей с информацией о товарах.
        :param only_partner_media_content: Если True, используются только переданные изображения товаров. По умолчанию False.
        :return: Ответ API в виде словаря или None в случае ошибки.
        """
        endpoint = f"/businesses/{business_id}/offer-mappings/update"
        data = {
            "offerMappings": offer_mappings,
            "onlyPartnerMediaContent": only_partner_media_content
        }
        return self._send_request("POST", endpoint, req_data=data)

    def update_campaign_offers(self, campaign_id: int, offers: list[Dict]) -> Optional[Dict]:
        """
        Обновляет условия продажи товаров в магазине.

        :param campaign_id: Идентификатор кампании (магазина) на Яндекс.Маркете.
        :param offers: Список словарей с информацией о товарах и их условиях продажи.
        :return: Ответ API в виде словаря или None в случае ошибки.
        """
        endpoint = f"/campaigns/{campaign_id}/offers/update"
        data = {"offers": offers}
        return self._send_request("POST", endpoint, req_data=data)

    def add_hidden_offers(self, campaign_id: int, offer_ids: list[str]) -> Optional[Dict]:
        """
        Скрывает указанные товары в магазине на Яндекс.Маркете.

        :param campaign_id: Идентификатор кампании (магазина) на Яндекс.Маркете.
        :param offer_ids: Список идентификаторов товаров (offerId), которые необходимо скрыть.
        :return: Ответ API в виде словаря или None в случае ошибки.
        """
        endpoint = f"/campaigns/{campaign_id}/hidden-offers"
        data = {"hiddenOffers": [{"offerId": offer_id} for offer_id in offer_ids]}
        return self._send_request("POST", endpoint, req_data=data)

    def delete_hidden_offers(self, campaign_id: int, offer_ids: list[str]) -> Optional[Dict]:
        """
        Возобновляет показ ранее скрытых товаров в магазине на Яндекс.Маркете.

        :param campaign_id: Идентификатор кампании (магазина) на Яндекс.Маркете.
        :param offer_ids: Список идентификаторов товаров (offerId), которые необходимо снова сделать видимыми.
        :return: Ответ API в виде словаря или None в случае ошибки.
        """
        endpoint = f"/campaigns/{campaign_id}/hidden-offers/delete"
        data = {"hiddenOffers": [{"offerId": offer_id} for offer_id in offer_ids]}
        return self._send_request("POST", endpoint, req_data=data)

    def add_offers_to_archive(self, business_id: int, offer_ids: list[str]) -> Optional[Dict]:
        """
        Перемещает указанные товары в архив.

        :param business_id: Идентификатор бизнеса на Яндекс.Маркете.
        :param offer_ids: Список идентификаторов товаров (offerId), которые необходимо архивировать.
        :return: Ответ API в виде словаря или None в случае ошибки.
        """
        endpoint = f"/businesses/{business_id}/offer-mappings/archive"
        data = {"offerIds": offer_ids}
        return self._send_request("POST", endpoint, req_data=data)

    def delete_offers_from_archive(self, business_id: int, offer_ids: list[str]) -> Optional[Dict]:
        """
        Восстанавливает указанные товары из архива.

        :param business_id: Идентификатор бизнеса на Яндекс.Маркете.
        :param offer_ids: Список идентификаторов товаров (offerId), которые необходимо восстановить из архива.
        :return: Ответ API в виде словаря или None в случае ошибки.
        """
        endpoint = f"/businesses/{business_id}/offer-mappings/unarchive"
        data = {"offerIds": offer_ids}
        return self._send_request("POST", endpoint, req_data=data)

    def delete_offers(self, business_id: int, offer_ids: list[str]) -> Optional[Dict]:
        """
        Удаляет указанные товары из каталога.

        :param business_id: Идентификатор бизнеса на Яндекс.Маркете.
        :param offer_ids: Список идентификаторов товаров (offerId), которые необходимо удалить.
        :return: Ответ API в виде словаря или None в случае ошибки.
        """
        endpoint = f"/businesses/{business_id}/offer-mappings/delete"
        data = {"offerIds": offer_ids}
        return self._send_request("POST", endpoint, req_data=data)

    def delete_campaign_offers(self, campaign_id: int, offer_ids: list[str]) -> Optional[Dict]:
        """
        Удаляет указанные товары из ассортимента магазина.

        :param campaign_id: Идентификатор кампании (магазина) на Яндекс.Маркете.
        :param offer_ids: Список идентификаторов товаров (offerId), которые необходимо удалить.
        :return: Ответ API в виде словаря или None в случае ошибки.
        """
        endpoint = f"/campaigns/{campaign_id}/offers/delete"
        data = {"offerIds": offer_ids}
        return self._send_request("POST", endpoint, req_data=data)
