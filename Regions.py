from typing import Optional, Dict

class RegionsAPI:

    def get_region_by_name(self, region_name: str = "") -> Optional[Dict]:
        """
        Получает информацию о регионах по его названию.
        :param region_name: Название региона для фильтрации (опционально).
        :return: Словарь с данными о регионах или None в случае ошибки.
        """
        params = {"name": region_name} if region_name else {}
        return self._send_request("GET", "regions", req_params=params)

    def get_region(self, region_id: int) -> Optional[Dict]:
        """
        Получает информацию о конкретном регионе по его ID.
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
