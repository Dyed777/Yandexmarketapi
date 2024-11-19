from typing import Optional, Dict, List
class CampaignsAPI:

    def get_campaigns(self) -> Optional[Dict]:
        """
        Получает список кампаний.
        :return: Словарь с данными о кампаниях или None в случае ошибки.
        """
        return self._send_request("GET", "campaigns")

    def get_campaign(self, camp_id: int) -> Optional[Dict]:
        """
        Получает данные конкретной кампании.
        :param camp_id: Идентификатор кампании.
        :return: Словарь с данными о кампании или None в случае ошибки.
        """
        return self._send_request("GET", f"campaigns/{camp_id}")

    def get_campaign_settings(self, camp_id: int) -> Optional[Dict]:
        """
        Получает настройки конкретной кампании.
        :param camp_id: Идентификатор кампании.
        :return: Словарь с настройками кампании или None в случае ошибки.
        """
        return self._send_request("GET", f"campaigns/{camp_id}/settings")

    def get_campaigns_orders(self, camp_id: int, limit: Optional[int] = None, page_token: Optional[str] = None) -> Optional[Dict]:
        """
        Получает список заказов для кампании.
        :param camp_id: Идентификатор кампании.
        :param limit: Количество записей на одной странице (опционально).
        :param page_token: Токен для пагинации (опционально).
        :return: Словарь с данными о заказах или None в случае ошибки.
        """
        params = {k: v for k, v in {"limit": limit, "page_token": page_token}.items() if v is not None}
        return self._send_request("GET", f"campaigns/{camp_id}/orders", req_params=params)

    def get_campaign_order(self, camp_id: int, ord_id: int) -> Optional[Dict]:
        """
        Получает данные конкретного заказа в кампании.
        :param camp_id: Идентификатор кампании.
        :param ord_id: Идентификатор заказа.
        :return: Словарь с данными о заказе или None в случае ошибки.
        """
        return self._send_request("GET", f"campaigns/{camp_id}/orders/{ord_id}")

    def get_campaigns_hidden_offers(self, camp_id: int) -> Optional[Dict]:
        """
        Получает скрытые предложения для конкретной кампании.
        :param camp_id: Идентификатор кампании.
        :return: Словарь с данными о скрытых предложениях или None в случае ошибки.
        """
        return self._send_request("GET", f"campaigns/{camp_id}/hidden-offers")

    def get_campaign_offers(self, camp_id: int, req_params: Optional[Dict] = None, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает предложения для указанной кампании.
        :param camp_id: Идентификатор кампании.
        :param req_params: Параметры запроса (опционально).
        :param req_data: Данные запроса (опционально).
        :return: Словарь с данными о предложениях или None в случае ошибки.
        """
        return self._send_request("POST", f"campaigns/{camp_id}/offers", req_params=req_params, req_data=req_data)

    def get_campaign_quarantine_offers(self, camp_id: int, req_params: Optional[Dict] = None, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает список товаров, находящихся в карантине по ценам для кампании.
        :param camp_id: Идентификатор кампании.
        :param req_params: Параметры запроса (опционально).
        :param req_data: Данные запроса (опционально).
        :return: Словарь с данными о товарах в карантине или None в случае ошибки.
        """
        return self._send_request("POST", f"campaigns/{camp_id}/price-quarantine", req_params=req_params, req_data=req_data)

    def update_campaign_offers(self, campaign_id: int, offers: List[Dict]) -> Optional[Dict]:
        """
        Обновляет условия продажи товаров в магазине.
        :param campaign_id: Идентификатор кампании (магазина) на Яндекс.Маркете.
        :param offers: Список словарей с информацией о товарах и их условиях продажи.
        :return: Ответ API в виде словаря или None в случае ошибки.
        """
        return self._send_request("POST", f"campaigns/{campaign_id}/offers/update", req_data={"offers": offers})

    def delete_campaign_offers(self, campaign_id: int, offer_ids: List[str]) -> Optional[Dict]:
        """
        Удаляет указанные товары из ассортимента магазина.
        :param campaign_id: Идентификатор кампании (магазина) на Яндекс.Маркете.
        :param offer_ids: Список идентификаторов товаров (offerId), которые необходимо удалить.
        :return: Ответ API в виде словаря или None в случае ошибки.
        """
        return self._send_request("POST", f"campaigns/{campaign_id}/offers/delete", req_data={"offerIds": offer_ids})
