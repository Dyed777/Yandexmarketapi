from typing import Optional, Dict, List

class ReportsAPI:

    def generate_report(self, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None, report_format: str = "FILE") -> Optional[Dict]:
        """
        Генерирует отчет с заданным конечным путем и параметрами.
        :param endpoint: Конечный путь API для генерации отчета.
        :param params: Дополнительные параметры запроса (опционально).
        :param data: Данные запроса (опционально).
        :param report_format: Формат отчета ('FILE' или 'CSV'). По умолчанию 'FILE'.
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        params = params or {}
        params["format"] = report_format
        return self._send_request("POST", endpoint, req_params=params, req_data=data)

    def get_goods_feedback_comments(self, biz_id: str, feedback_id: int, page_token: Optional[str] = None) -> Optional[
        Dict]:
        """
        Получение комментариев к отзыву о товаре.
        :param biz_id: Идентификатор бизнеса.
        :param feedback_id: Идентификатор отзыва.
        :param page_token: Токен для пагинации (опционально).
        :return: Словарь с данными о комментариях или None в случае ошибки.
        """
        params = {"page_token": page_token} if page_token else {}
        return self._send_request("POST", f"businesses/{biz_id}/goods-feedback/comments", req_params=params,
                                  req_data={"feedbackId": feedback_id})

    def generate_shows_sales_report(self, date_from: str, date_to: str, grouping: str, business_id: Optional[int] = None, campaign_id: Optional[int] = None, report_format: str = 'FILE') -> Optional[Dict]:
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
        if not (bool(business_id) ^ bool(campaign_id)):
            raise ValueError("Укажите ровно один параметр: либо business_id, либо campaign_id.")
        data = {
            "dateFrom": date_from,
            "dateTo": date_to,
            "grouping": grouping,
            "businessId": business_id,
            "campaignId": campaign_id
        }
        return self.generate_report("reports/shows-sales/generate", data=data, report_format=report_format)

    def generate_boost_consolidated_report(self, business_id: int, date_from: str, date_to: str, report_format: str = 'FILE') -> Optional[Dict]:
        """
        Генерирует сводный отчет по бусту продаж за указанный период.
        :param business_id: Идентификатор бизнеса.
        :param date_from: Начало периода (в формате 'YYYY-MM-DD').
        :param date_to: Конец периода (в формате 'YYYY-MM-DD').
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        data = {"businessId": business_id, "dateFrom": date_from, "dateTo": date_to}
        return self.generate_report("reports/boost-consolidated/generate", data=data, report_format=report_format)

    def generate_goods_movement_report(self, campaign_id: int, date_from: str, date_to: str, report_format: str = 'FILE', shop_sku: Optional[str] = None) -> Optional[Dict]:
        """
        Генерирует отчет по движению товаров (FBY) за указанный период.
        :param campaign_id: Идентификатор кампании.
        :param date_from: Начало периода (в формате 'YYYY-MM-DD').
        :param date_to: Конец периода (в формате 'YYYY-MM-DD').
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :param shop_sku: SKU товара для фильтрации (опционально).
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        data = {"campaignId": campaign_id, "dateFrom": date_from, "dateTo": date_to, "shopSku": shop_sku}
        return self.generate_report("reports/goods-movement/generate", data=data, report_format=report_format)

    def generate_united_orders_report(self, business_id: int, date_from: str, date_to: str, report_format: str = 'FILE', campaign_ids: Optional[List[int]] = None, promo_id: Optional[str] = None) -> Optional[Dict]:
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
        data = {"businessId": business_id, "dateFrom": date_from, "dateTo": date_to, "campaignIds": campaign_ids, "promoId": promo_id}
        return self.generate_report("reports/united-orders/generate", data=data, report_format=report_format)

    def generate_competitors_position_report(self, business_id: int, category_id: int, date_from: str, date_to: str, report_format: str = 'FILE') -> Optional[Dict]:
        """
        Генерирует отчет «Конкурентная позиция» за указанный период.
        :param business_id: Идентификатор бизнеса.
        :param category_id: Идентификатор категории.
        :param date_from: Начало периода (в формате 'YYYY-MM-DD').
        :param date_to: Конец периода (в формате 'YYYY-MM-DD').
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        data = {"businessId": business_id, "categoryId": category_id, "dateFrom": date_from, "dateTo": date_to}
        return self.generate_report("reports/competitors-position/generate", data=data, report_format=report_format)

    def generate_goods_turnover_report(self, campaign_id: int, report_date: Optional[str] = None, report_format: str = 'FILE') -> Optional[Dict]:
        """
        Генерирует отчет по оборачиваемости товаров (FBY) за указанную дату.
        :param campaign_id: Идентификатор кампании.
        :param report_date: Дата отчета (в формате 'YYYY-MM-DD').
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        data = {"campaignId": campaign_id, "date": report_date}
        return self.generate_report("reports/goods-turnover/generate", data=data, report_format=report_format)

    def generate_stocks_on_warehouses_report(self, campaign_id: int, warehouse_ids: Optional[List[int]] = None, report_date: Optional[str] = None, category_ids: Optional[List[int]] = None, has_stocks: Optional[bool] = None, report_format: str = 'FILE') -> Optional[Dict]:
        """
        Генерирует отчет по остаткам на складах.
        :param campaign_id: Идентификатор кампании.
        :param warehouse_ids: Список идентификаторов складов.
        :param report_date: Дата отчета (в формате 'YYYY-MM-DD').
        :param category_ids: Список идентификаторов категорий.
        :param has_stocks: Фильтр по наличию остатков.
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        data = {"campaignId": campaign_id, "warehouseIds": warehouse_ids, "reportDate": report_date, "categoryIds": category_ids, "hasStocks": has_stocks}
        return self.generate_report("reports/stocks-on-warehouses/generate", data=data, report_format=report_format)

    def generate_united_netting_report(self, business_id: int, date_from: Optional[str] = None, date_to: Optional[str] = None, bank_order_id: Optional[int] = None, bank_order_date_time: Optional[str] = None, campaign_ids: Optional[List[int]] = None, inns: Optional[List[str]] = None, placement_programs: Optional[List[str]] = None, report_format: str = 'FILE') -> Optional[Dict]:
        """
        Генерирует отчет по платежам за указанный период или по платежному поручению.
        :param business_id: Идентификатор бизнеса.
        :param date_from: Начало периода (в формате 'YYYY-MM-DD').
        :param date_to: Конец периода (в формате 'YYYY-MM-DD').
        :param bank_order_id: Номер платежного поручения.
        :param bank_order_date_time: Дата платежного поручения (в формате 'YYYY-MM-DDTHH:MM:SSZ').
        :param campaign_ids: Список идентификаторов кампаний.
        :param inns: Список ИНН.
        :param placement_programs: Список моделей работы.
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        data = {"businessId": business_id, "dateFrom": date_from, "dateTo": date_to, "bankOrderId": bank_order_id, "bankOrderDateTime": bank_order_date_time, "campaignIds": campaign_ids, "inns": inns, "placementPrograms": placement_programs}
        return self.generate_report("reports/united-netting/generate", data=data, report_format=report_format)

    def generate_shelfs_statistics_report(self, business_id: int, date_from: str, date_to: str, attribution_type: str = 'CLICKS', report_format: str = 'FILE') -> Optional[Dict]:
        """
        Генерирует сводный отчет по полкам за указанный период.
        :param business_id: Идентификатор бизнеса.
        :param date_from: Начало периода (в формате 'YYYY-MM-DD').
        :param date_to: Конец периода (в формате 'YYYY-MM-DD').
        :param attribution_type: Тип атрибуции ('CLICKS' или 'SHOWS').
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        data = {"businessId": business_id, "dateFrom": date_from, "dateTo": date_to, "attributionType": attribution_type}
        return self.generate_report("reports/shelf-statistics/generate", data=data, report_format=report_format)

    def generate_goods_realization_report(self, campaign_id: int, year: int, month: int, report_format: str = 'FILE') -> Optional[Dict]:
        """
        Генерирует отчет по реализации товаров за указанный месяц.
        :param campaign_id: Идентификатор кампании.
        :param year: Год отчета.
        :param month: Месяц отчета (1-12).
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        data = {"campaignId": campaign_id, "year": year, "month": month}
        return self.generate_report("reports/goods-realization/generate", data=data, report_format=report_format)

    def generate_united_marketplace_services_report(self, business_id: int, date_from: Optional[str] = None, date_to: Optional[str] = None, year: Optional[int] = None, month: Optional[int] = None, report_format: str = 'FILE', campaign_ids: Optional[List[int]] = None, inns: Optional[List[str]] = None) -> Optional[Dict]:
        """
        Генерирует отчет по стоимости услуг за указанный период.
        :param business_id: Идентификатор бизнеса.
        :param date_from: Начало периода (в формате 'YYYY-MM-DD').
        :param date_to: Конец периода (в формате 'YYYY-MM-DD').
        :param year: Год формирования акта для отчета по дате формирования акта.
        :param month: Месяц формирования акта (1-12).
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :param campaign_ids: Список идентификаторов кампаний.
        :param inns: Список ИНН.
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        if not ((date_from and date_to) or (year and month)):
            raise ValueError("Необходимо указать либо 'date_from' и 'date_to', либо 'year' и 'month'.")
        data = {"businessId": business_id, "dateFrom": date_from, "dateTo": date_to, "year": year, "month": month, "campaignIds": campaign_ids, "inns": inns}
        return self.generate_report("reports/united-marketplace-services/generate", data=data, report_format=report_format)

    def generate_prices_report(self, business_id: Optional[int] = None, campaign_id: Optional[int] = None, category_ids: Optional[List[int]] = None, creation_date_from: Optional[str] = None, creation_date_to: Optional[str] = None, report_format: str = 'FILE') -> Optional[Dict]:
        """
        Генерирует отчет «Цены на рынке».
        :param business_id: Идентификатор бизнеса.
        :param campaign_id: Идентификатор кампании.
        :param category_ids: Список идентификаторов категорий.
        :param creation_date_from: Начальная дата появления предложения.
        :param creation_date_to: Конечная дата появления предложения.
        :param report_format: Формат отчета ('FILE' или 'CSV').
        :return: Словарь с информацией об отчете или None в случае ошибки.
        """
        if not (business_id or campaign_id):
            raise ValueError("Укажите либо 'business_id', либо 'campaign_id'.")
        data = {"businessId": business_id, "campaignId": campaign_id, "categoryIds": category_ids, "creationDateFrom": creation_date_from, "creationDateTo": creation_date_to}
        return self.generate_report("reports/prices/generate", data=data, report_format=report_format)

    def get_report_info(self, report_id: str) -> Optional[Dict]:
        """
        Получает статус генерации отчета и ссылку на готовый отчет.
        :param report_id: Идентификатор отчета, полученный после запуска генерации.
        :return: Словарь с информацией о статусе отчета или None в случае ошибки.
        """
        return self._send_request("GET", f"reports/info/{report_id}")
