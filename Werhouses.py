from typing import Optional, Dict

class WarehousesAPI:
    def get_stocks(self, camp_id: str, req_params: Optional[Dict] = None, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает информацию о запасах товаров для кампании.
        :param camp_id: Идентификатор кампании.
        :param req_params: Параметры запроса (опционально).
        :param req_data: Данные запроса (опционально).
        :return: Словарь с информацией о запасах или None в случае ошибки.
        """
        return self._send_request("POST", f"campaigns/{camp_id}/offers/stocks", req_params=req_params, req_data=req_data)

    def update_stocks(self, business_id: int, warehouse_id: int, stocks: list[Dict]) -> Optional[Dict]:
        """
        Обновляет остатки на складе для указанного бизнеса.
        :param business_id: Идентификатор бизнеса.
        :param warehouse_id: Идентификатор склада.
        :param stocks: Список остатков товаров.
        :return: Словарь с результатами обновления остатков или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{business_id}/stocks", req_data={"warehouseId": warehouse_id, "stocks": stocks})

    def get_fulfillment_warehouses(self) -> Optional[Dict]:
        """
        Получает список складов с их идентификаторами.
        :return: Словарь с данными о складах или None в случае ошибки.
        """
        return self._send_request("GET", "warehouses")

    def get_delivery_services(self) -> Optional[Dict]:
        """
        Получает список доступных служб доставки.
        :return: Словарь с данными о службах доставки или None в случае ошибки.
        """
        return self._send_request("GET", "delivery/services")

    def get_warehouses(self) -> Optional[Dict]:
        """
        Получает список складов.
        :return: Словарь с данными о складах или None в случае ошибки.
        """
        return self._send_request("GET", "warehouses")

