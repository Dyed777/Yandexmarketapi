import logging
from typing import Optional, Dict, List, Union
class BusinessesAPI:

    def get_business_settings(self, biz_id: int, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Возвращает настройки бизнеса по его идентификатору.
        :param biz_id: Идентификатор бизнеса.
        :param req_data: Дополнительные данные запроса (опционально).
        :return: Словарь с настройками бизнеса или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/settings", req_data=req_data)

    def get_business_offer_mappings(self, biz_id: int, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Возвращает соответствия предложений для указанного бизнеса.
        :param biz_id: Идентификатор бизнеса.
        :param req_data: Дополнительные данные запроса (опционально).
        :return: Словарь с маппингом предложений или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/offer-mappings", req_data=req_data)

    def get_business_quarantine_offers(self, biz_id: int, req_params: Optional[Dict] = None, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Возвращает предложения бизнеса, находящиеся в "карантине".
        :param biz_id: Идентификатор бизнеса.
        :param req_params: Параметры запроса (опционально).
        :param req_data: Данные запроса (опционально).
        :return: Словарь с данными о предложениях в карантине или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/price-quarantine", req_params=req_params, req_data=req_data)

    def get_business_goods_feedback(self, biz_id: int, limit: Optional[int]=None, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает отзывы о товарах для указанного бизнеса.
        :param biz_id: Идентификатор бизнеса.
        :param req_data: Дополнительные данные запроса (опционально).
        :return: Словарь с отзывами о товарах или None в случае ошибки.
        """
        req_params = {"limit": limit} if limit else None
        return self._send_request("POST", f"businesses/{biz_id}/goods-feedback",  req_data=req_data, req_params=req_params )

    def get_business_quality_rating(self, biz_id: int, camp_ids: List[str]) -> Optional[Dict]:
        """
        Возвращает рейтинг качества для указанного бизнеса и кампаний.
        :param biz_id: Идентификатор бизнеса.
        :param camp_ids: Список идентификаторов кампаний.
        :return: Словарь с рейтингом качества или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/ratings/quality", req_data={"campaignIds": camp_ids})

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

    def put_bids_for_business(self, business_id: int, bids: List[Dict[str, Union[str, int]]]) -> Optional[Dict]:
        """
        Устанавливает ставки для указанного бизнеса.
        :param business_id: Идентификатор бизнеса.
        :param bids: Список словарей с информацией о ставках.
        :return: Словарь с результатами установки ставок или None в случае ошибки.
        """
        return self._send_request("PUT", f"businesses/{business_id}/bids", req_data={"bids": bids})

    def add_offers_to_archive(self, business_id: int, offer_ids: List[str]) -> Optional[Dict]:
        """
        Добавляет предложения в архив для указанного бизнеса.
        :param business_id: Идентификатор бизнеса.
        :param offer_ids: Список идентификаторов предложений.
        :return: Словарь с результатами операции или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{business_id}/offer-mappings/archive", req_data={"offerIds": offer_ids})

    def delete_offers_from_archive(self, business_id: int, offer_ids: List[str]) -> Optional[Dict]:
        """
        Удаляет предложения из архива для указанного бизнеса.
        :param business_id: Идентификатор бизнеса.
        :param offer_ids: Список идентификаторов предложений.
        :return: Словарь с результатами операции или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{business_id}/offer-mappings/unarchive", req_data={"offerIds": offer_ids})

    def delete_offers(self, business_id: int, offer_ids: List[str]) -> Optional[Dict]:
        """
        Удаляет предложения для указанного бизнеса.
        :param business_id: Идентификатор бизнеса.
        :param offer_ids: Список идентификаторов предложений.
        :return: Словарь с результатами удаления или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{business_id}/offer-mappings/delete", req_data={"offerIds": offer_ids})

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