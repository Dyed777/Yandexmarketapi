from typing import Optional, Dict, List,Any

class CategoriesAPI:
    def get_categories_tree(self, language: str = "RU") -> Optional[Dict]:
        """
        Получает дерево категорий Яндекс.Маркета.
        :param language: Язык категорий (по умолчанию "RU").
        :return: Словарь с деревом категорий или None в случае ошибки.
        """
        data = {"language": language}
        return self._send_request("POST", "categories/tree", req_data=data)

    def get_categories_max_sale_quantum(self, category_ids: List[int]) -> Optional[Dict]:
        """
        Получает максимальные лимиты продажи и минимальное количество заказа для указанных категорий.
        :param category_ids: Список идентификаторов категорий.
        :return: Словарь с информацией о максимальных квотах продажи для категорий или None в случае ошибки.
        """
        if not category_ids:
            raise ValueError("Список 'category_ids' не должен быть пустым.")
        data = {"marketCategoryIds": category_ids}
        return self._send_request("POST", "categories/max-sale-quantum", req_data=data)

    def get_category_content_parameters(self, category_id: int) -> Optional[Dict]:
        """
        Получает список характеристик товаров с допустимыми значениями для указанной категории.
        :param category_id: Идентификатор категории на Яндекс.Маркете.
        :return: Словарь с параметрами категории или None в случае ошибки.
        """
        return self._send_request("POST", f"category/{category_id}/parameters")

    def update_offer_content(self, business_id: int, offers_content: List[Dict[str, Any]]) -> Optional[Dict]:
        """
        Редактирует категорийные характеристики товаров.
        :param business_id: Идентификатор кабинета.
        :param offers_content: Список товаров с их характеристиками.
        :return: Ответ API или None в случае ошибки.
        """
        if not offers_content:
            raise ValueError("Список 'offers_content' не должен быть пустым.")

        endpoint = f"businesses/{business_id}/offer-cards/update"
        data = {"offersContent": offers_content}
        return self._send_request("POST", endpoint, req_data=data)