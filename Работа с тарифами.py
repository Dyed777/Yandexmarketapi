from typing import Optional, Dict, List

class TariffsAPI:
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
