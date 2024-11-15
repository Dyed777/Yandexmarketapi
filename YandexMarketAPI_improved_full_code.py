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

    def _send_request(self, method: str, endpoint: str, req_params: Optional[Dict] = None,
                      req_data: Optional[Dict] = None) -> Optional[Dict]:
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

    def get_goods_feedback_comments(self, biz_id: str, feedback_id: int, page_token: Optional[str] = None) -> Optional[Dict]:
        """
        Получение комментариев к отзыву о товаре.
        :param biz_id: Идентификатор бизнеса.
        :param feedback_id: Идентификатор отзыва.
        :param page_token: Токен для пагинации (опционально).
        :return: Словарь с данными о комментариях или None в случае ошибки.
        """
        endpoint = f"businesses/{biz_id}/goods-feedback/{feedback_id}/comments"
        params = {}
        if page_token:
            params['page_token'] = page_token
        return self._send_request("POST", endpoint, req_params=params)

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
        :param business_id: Идентификатор бизнеса.
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
        :param selling_program: Программа продаж (опционально).
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


# -------------------------------
# Пример использования класса
# -------------------------------
if __name__ == "__main__":
    client_id = "914570202"
    api_key = "ACMA:EiUUExLd1nFnCRqsg56RzJuVJ2b0r1FsfHy3Owoi:5dc195fa"
    api = YandexMarketAPI(client_id, api_key)

    #campaigns = api.get_campaigns()
    #print_response(campaigns, "Список кампаний")

    #campaign_id = "21962613"
    #campaign_info = api.get_campaign(campaign_id)
    #print_response(campaign_info, "Информация о кампании")

    #business_id = "954323"
    #business_settings = api.get_business_settings(business_id)
    #print_response(business_settings, "Информация о настройках кабинета")

    #campaign_settings = api.get_campaign_settings(campaign_id)
    #print_response(campaign_settings, "Информация о настройках магазина")

    #hidden_offers = api.get_campaigns_hidden_offers(campaign_id)
    #print_response(hidden_offers, "Список скрытых товаров")

    #offer_mappings = api.get_business_offer_mappings(business_id)
    #print_response(offer_mappings, "Список товаров в каталоге бизнеса")

    #offers = api.get_campaign_offers(campaign_id, req_data={})
    #print_response(offers, "Список товаров в магазине")

    #promos = api.get_promos(business_id)
    #print_response(promos, "Информация об акциях Маркета")

    #orders = api.get_campaigns_orders(campaign_id, limit=5)
    #print_response(orders, "Список заказов")

    #order_id = "585090288"
    #order_info = api.get_campaign_order(campaign_id, order_id)
    #print_response(order_info, "Информация о заказе")

    #returns_list = api.get_returns_list(campaign_id)
    #print_response(returns_list, "Список возвратов и невыкупов")

    #order_id = 579218013
    #return_id = 53738350
    #return_info = api.get_return_info(int(campaign_id), int(order_id), return_id)
    #print_response(return_info, "Информация о возврате")

    #feedback_info = api.get_business_goods_feedback(business_id)
    #print_response(feedback_info, "Информация об отзывах о товарах")

    #quality_rating_info = api.get_business_quality_rating(business_id, [campaign_id])
    #print_response(quality_rating_info, "Информация об индексе качества магазинов")

    #warehouses = api.get_warehouses()
    #print_response(warehouses, "Список складов")

    #delivery_services = api.get_delivery_services()
    #print_response(delivery_services, "Справочник служб доставки")

    #regions = api.get_regions(region_name="Москва")
    #print_response(regions, "Регионы, соответствующие названию 'Москва'")

    #search_results = api.search_models("Термопаста", region_id=213, page=1, page_size=5)
    #print_response(search_results, "Результаты поиска моделей")

    #region_id = "213"
    #region_info = api.get_region(region_id)
    #print_response(region_info, f"Информация о регионе с ID {region_id}")
    #children_regions = api.get_region_children(region_id)
    #print_response(children_regions, f"Дочерние регионы для региона с ID {region_id}")

    #stocks_info = api.get_stocks(campaign_id, req_params={"limit": 10}, req_data={"withTurnover": True, "archived": False})
    #print_response(stocks_info, "Информация об остатках и оборачиваемости товаров")

    #offer_ids = ["8208310359"]
    #prices_info = api.get_prices_by_offer_ids(campaign_id, offer_ids)
    #print_response(prices_info, "Информация о ценах для указанных товаров")

    #quarantine_offers_business = api.get_business_quarantine_offers(business_id, req_data={})
    #print_response(quarantine_offers_business, "Список товаров в карантине по цене для бизнеса")

    #quarantine_offers_campaign = api.get_campaign_quarantine_offers(campaign_id, req_data={})
    #print_response(quarantine_offers_campaign, "Список товаров в карантине по цене для кампании")

    #offer_cards_status = api.get_offer_cards_content_status(business_id, req_data={"offerIds": ["1019411458"]})
    #print_response(offer_cards_status, "Информация о заполненности карточек товаров")

    #offers = [
    #    {
     #       "offerId": "1026281557",
      #      "name": "Термоклей двухкомпонентный STEEL STG-1v2",
       #     "category": "Компьютерная техника/Комплектующие/Термопаста",
        #    "vendor": "STEEL",
         #   "barcodes": ["4610019100644"],
          #  "description": "Теплопроводный клей предназначен для радиаторов.",
           # "vendorCode": "STG-1v2-1",
            #"basicPrice": {"value": "220.0", "currencyId": "RUR"}
        #}
    #]
    #suggested_mappings = api.get_suggested_offer_mappings(business_id, offers)
    #print_response(suggested_mappings, "Список соответствующих карточек на Маркете")

    #model_id = 822120412
    #region_id = 213
    #model_info = api.get_model_info(model_id, region_id)
    #print_response(model_info, "Информация о модели")

    #model_ids = [952757555, 822120412]
    #models_info = api.get_models_info(model_ids, region_id)
    #print_response(models_info, "Информация о моделях")

    #offers_info = api.get_model_offers(model_id, region_id, count=5, order_by_price="ASC")
    #print_response(offers_info, "Список предложений для модели")

    #search_query = "Термопаста"
    #search_results = api.search_models(search_query, region_id, page=1, page_size=5)
    #print_response(search_results, "Результаты поиска моделей")

    #feedback_id = 35212560
    #comments = api.get_goods_feedback_comments(business_id, feedback_id)
    #print_response(comments, "Комментарии о товаре")

    #business_id = 954323
    #promo_id = "cf_121198"
    #promo_offers = api.get_promo_offers(business_id, promo_id, limit=5)
    #print_response(promo_offers, "Список товаров в акции")

    #skus = ["102089688224", "103611356459", "100813589980"]
    #recommendations = api.get_bids_recommendations(business_id, skus)
    #print_response(recommendations, "Рекомендованные ставки")

    #bids_info = api.get_bids_info(business_id, skus=skus, limit=50)
    #print_response(bids_info, "Информация об установленных ставках")

    #recommendations = api.get_offer_recommendations(business_id=business_id, offer_ids=['862547698', '862536189'])
    #print_response(recommendations, "Рекомендации по ценам")

    #offers = [{"categoryId": 90535, "price": 300, "length": 14, "width": 3.5, "height": 3, "weight": 0.051, "quantity": 1}]
    #tariffs = api.calculate_tariffs(offers, campaign_id=21962613, frequency='DAILY')
    #print_response(tariffs, "Рассчитанные тарифы")

    #categories_tree = api.get_categories_tree()
    #print_response(categories_tree, "Дерево категорий")

    #chats = api.get_chats(business_id,req_data={})
    #print_response(chats, "Список чатов")

    #category_ids = [7969496, 6374360]  # Замените на реальные идентификаторы категорий
    #categories_quantum = api.get_categories_max_sale_quantum(category_ids)
    #print_response(categories_quantum, "Информация о максимальных квотах продажи для категорий")


    #category_params= api.get_category_content_parameters(category_id=7969496)
    #print_response(category_params,"Список характеристик для категорий товара")

    #report_respone=api.generate_goods_feedback_report(business_id=954323,format="CSV")
    #print_response(report_respone,"Статус генераций отчёта об отзывах")

    #chat_respone=api.create_chat(business_id=954323,order_id=585090288)
    #print_response(chat_respone,"Созданный чат")

    #send_message=api.send_message_to_chat(business_id=954323,chat_id=585090288,message="Проверка")
    #print_response(send_message,"Отправка сообщения в чат")

    #warehouses_FBY=api.get_fulfillment_warehouses()
    #print_response(warehouses_FBY,"Список складов с идентификаторами")