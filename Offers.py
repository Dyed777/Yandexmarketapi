from typing import Optional, Dict, List, Union

class OffersAPI:

    def get_prices_by_offer_ids(self, camp_id: str, offer_ids: List[str]) -> Optional[Dict]:
        """
        Получает цены для товаров по их идентификаторам.
        :param camp_id: Идентификатор кампании.
        :param offer_ids: Список идентификаторов предложений.
        :return: Словарь с ценами или None в случае ошибки.
        """
        return self._send_request("POST", f"campaigns/{camp_id}/offer-prices", req_data={"offerIds": offer_ids})

    def get_offer_cards_content_status(self, biz_id: str, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает статус контента карточек предложений.
        :param biz_id: Идентификатор бизнеса.
        :param req_data: Данные запроса (опционально).
        :return: Словарь с данными о статусе карточек или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/offer-cards", req_data=req_data)

    def get_suggested_offer_mappings(self, biz_id: str, offers: List[Dict]) -> Optional[Dict]:
        """
        Получает предложенные карточки для товаров бизнеса.
        :param biz_id: Идентификатор бизнеса.
        :param offers: Список товаров для маппинга.
        :return: Словарь с предложениями маппинга или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/offer-mappings/suggestions", req_data={"offers": offers})

    def get_models_info(self, model_ids: List[int], region_id: int, currency: str = "RUR") -> Optional[Dict]:
        """
        Получает информацию о нескольких моделях товаров.
        :param model_ids: Список идентификаторов моделей (до 100 элементов).
        :param region_id: Идентификатор региона.
        :param currency: Валюта (по умолчанию RUR).
        :return: Словарь с информацией о моделях или None в случае ошибки.
        """
        if not model_ids or len(model_ids) > 100:
            raise ValueError("Список model_ids должен содержать от 1 до 100 элементов.")
        return self._send_request("POST", "models", req_params={"regionId": region_id, "currency": currency}, req_data={"models": model_ids})

    def get_model_info(self, model_id: int, region_id: int, currency: str = "RUR") -> Optional[Dict]:
        """
        Получает информацию о модели товара.
        :param model_id: Идентификатор модели.
        :param region_id: Идентификатор региона.
        :param currency: Валюта (по умолчанию RUR).
        :return: Словарь с информацией о модели или None в случае ошибки.
        """
        return self._send_request("GET", f"models/{model_id}", req_params={"regionId": region_id, "currency": currency})

    def get_model_offers(self, model_id: int, region_id: int, count: int = 10, currency: str = "RUR", order_by_price: Optional[str] = None, page: int = 1) -> Optional[Dict]:
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
        if count < 1 or count > 100:
            raise ValueError("Параметр 'count' должен быть в диапазоне от 1 до 100.")
        params = {
            "regionId": region_id,
            "count": count,
            "currency": currency,
            "page": page,
            **({"orderByPrice": order_by_price.upper()} if order_by_price and order_by_price.upper() in ["ASC", "DESC"] else {})
        }
        return self._send_request("GET", f"models/{model_id}/offers", req_params=params)

    def search_models(self, query: str, region_id: int, currency: str = "RUR", page: int = 1, page_size: int = 10) -> Optional[Dict]:
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
            raise ValueError("Параметр 'query' не должен быть пустым.")
        params = {
            "query": query,
            "regionId": region_id,
            "currency": currency,
            "page": page,
            "pageSize": page_size
        }
        return self._send_request("GET", "models", req_params=params)

    def update_offer_mappings(self, business_id: int, offer_mappings: List[Dict], only_partner_media_content: bool = False) -> Optional[Dict]:
        """
        Добавляет или обновляет информацию о товарах в каталоге.
        :param business_id: Идентификатор бизнеса.
        :param offer_mappings: Список словарей с информацией о товарах.
        :param only_partner_media_content: Если True, используются только переданные изображения товаров.
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{business_id}/offer-mappings/update", req_data={
            "offerMappings": offer_mappings,
            "onlyPartnerMediaContent": only_partner_media_content
        })

    def add_hidden_offers(self, campaign_id: int, offer_ids: List[str]) -> Optional[Dict]:
        """
        Скрывает указанные товары в магазине на Яндекс.Маркете.
        :param campaign_id: Идентификатор кампании (магазина) на Яндекс.Маркете.
        :param offer_ids: Список идентификаторов товаров (offerId), которые необходимо скрыть.
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        data = {"hiddenOffers": [{"offerId": offer_id} for offer_id in offer_ids]}
        return self._send_request("POST", f"/campaigns/{campaign_id}/hidden-offers", req_data=data)

    def delete_hidden_offers(self, campaign_id: int, offer_ids: List[str]) -> Optional[Dict]:
        """
        Возобновляет показ ранее скрытых товаров в магазине на Яндекс.Маркете.
        :param campaign_id: Идентификатор кампании (магазина) на Яндекс.Маркете.
        :param offer_ids: Список идентификаторов товаров (offerId), которые необходимо снова сделать видимыми.
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        data = {"hiddenOffers": [{"offerId": offer_id} for offer_id in offer_ids]}
        return self._send_request("POST", f"/campaigns/{campaign_id}/hidden-offers/delete", req_data=data)

    def calculate_tariffs(self, offers: List[Dict], campaign_id: Optional[int] = None, selling_program: Optional[str] = None, frequency: Optional[str] = None) -> Optional[Dict]:
        """
        Рассчитывает тарифы для указанных товаров.
        :param offers: Список товаров.
        :param campaign_id: Идентификатор кампании (опционально).
        :param selling_program: Программа продаж (например, 'FBY', 'DBS', 'FBS') (опционально).
        :param frequency: Частота платежей (например, 'ONCE' или 'MONTHLY') (опционально).
        :return: Словарь с рассчитанными тарифами или None в случае ошибки.
        """
        endpoint = "tariffs/calculate"

        # Формируем данные для запроса
        parameters = {k: v for k, v in {
            "campaignId": campaign_id,
            "sellingProgram": selling_program,
            "frequency": frequency
        }.items() if v is not None}

        data = {
            "offers": offers,
            "parameters": parameters
        }

        return self._send_request("POST", endpoint, req_data=data)
