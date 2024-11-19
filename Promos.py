from typing import Optional, Dict, List

class PromosAPI:

    def get_promos(self, biz_id: str, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает список акций для указанного бизнеса.
        :param biz_id: Идентификатор бизнеса.
        :param req_data: Дополнительные данные запроса (опционально).
        :return: Словарь с данными об акциях или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/promos", req_data=req_data)

    def get_promo_offers(self, business_id: int, promo_id: str, status_type: Optional[str] = None, limit: Optional[int] = None, page_token: Optional[str] = None) -> Optional[Dict]:
        """
        Получает список товаров, участвующих в акции.
        :param business_id: Идентификатор бизнеса.
        :param promo_id: Идентификатор акции.
        :param status_type: Фильтр по статусу участия (опционально).
        :param limit: Количество записей на одной странице (опционально).
        :param page_token: Токен для пагинации (опционально).
        :return: Словарь с данными о товарах или None в случае ошибки.
        """
        params = {k: v for k, v in {"limit": limit, "page_token": page_token}.items() if v is not None}
        data = {k: v for k, v in {"promoId": promo_id, "statusType": status_type}.items() if v is not None}
        return self._send_request("POST", f"businesses/{business_id}/promos/offers", req_params=params, req_data=data)

    def update_promo_offers(self, business_id: int, promo_id: str, offers: List[Dict]) -> Optional[Dict]:
        """
        Добавляет товары в акцию или изменяет их цены.
        :param business_id: Идентификатор бизнеса.
        :param promo_id: Идентификатор акции.
        :param offers: Список товаров с параметрами для акции.
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        if not offers or not isinstance(offers, list):
            raise ValueError("Параметр 'offers' должен быть непустым списком.")
        data = {"promoId": promo_id, "offers": offers}
        return self._send_request("POST", f"businesses/{business_id}/promos/offers/update", req_data=data)

    def delete_promo_offers(self, business_id: int, promo_id: str, offer_ids: Optional[List[str]] = None, delete_all_offers: bool = False) -> Optional[Dict]:
        """
        Удаляет товары из акции.
        :param business_id: Идентификатор бизнеса.
        :param promo_id: Идентификатор акции.
        :param offer_ids: Список SKU товаров для удаления из акции. Если None, будет использоваться параметр delete_all_offers.
        :param delete_all_offers: Если True, удаляет все товары из акции.
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        if not offer_ids and not delete_all_offers:
            raise ValueError("Необходимо указать либо 'offer_ids', либо установить 'delete_all_offers' в True.")
        if offer_ids and delete_all_offers:
            raise ValueError("Нельзя одновременно указывать 'offer_ids' и устанавливать 'delete_all_offers' в True.")
        data = {"promoId": promo_id, "offerIds": offer_ids, "deleteAllOffers": delete_all_offers}
        return self._send_request("POST", f"businesses/{business_id}/promos/offers/delete", req_data=data)
