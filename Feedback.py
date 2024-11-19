from typing import Optional, Dict, List

class FeedbackAPI:

    def get_business_goods_feedback(self, biz_id: str, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает отзывы о товарах для указанного бизнеса.
        :param biz_id: Идентификатор бизнеса.
        :param req_data: Дополнительные данные запроса (опционально).
        :return: Словарь с отзывами о товарах или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{biz_id}/goods-feedback", req_data=req_data)

    def get_goods_feedback_comments(self, biz_id: str, feedback_id: int, page_token: Optional[str] = None) -> Optional[Dict]:
        """
        Получение комментариев к отзыву о товаре.
        :param biz_id: Идентификатор бизнеса.
        :param feedback_id: Идентификатор отзыва.
        :param page_token: Токен для пагинации (опционально).
        :return: Словарь с данными о комментариях или None в случае ошибки.
        """
        params = {"page_token": page_token} if page_token else {}
        return self._send_request("POST", f"businesses/{biz_id}/goods-feedback/comments", req_params=params, req_data={"feedbackId": feedback_id})

    def update_goods_feedback_comment(self, business_id: int, feedback_id: int, text: str, comment_id: Optional[int] = None) -> Optional[Dict]:
        """
        Добавляет или обновляет комментарий к отзыву о товаре.
        :param business_id: Идентификатор бизнеса.
        :param feedback_id: Идентификатор отзыва.
        :param text: Текст комментария.
        :param comment_id: Идентификатор комментария (опционально). Если указан, комментарий будет обновлен.
        :return: Словарь с данными о комментарии или None в случае ошибки.
        """
        data = {
            "feedbackId": feedback_id,
            "text": text
        }
        if comment_id is not None:
            data["commentId"] = comment_id
        return self._send_request("POST", f"businesses/{business_id}/goods-feedback/comments/update", req_data=data)

    def delete_goods_feedback_comment(self, business_id: int, comment_id: int) -> Optional[Dict]:
        """
        Удаляет комментарий к отзыву о товаре.
        :param business_id: Идентификатор бизнеса.
        :param comment_id: Идентификатор комментария.
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{business_id}/goods-feedback/comments/delete", req_data={"id": comment_id})

    def skip_goods_feedbacks_reaction(self, business_id: int, feedback_ids: List[int]) -> Optional[Dict]:
        """
        Пропускает отзывы, требующие реакции, для указанного бизнеса.
        :param business_id: Идентификатор бизнеса.
        :param feedback_ids: Список идентификаторов отзывов, которые нужно пропустить.
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        return self._send_request("POST", f"businesses/{business_id}/goods-feedback/skip-reaction", req_data={"feedbackIds": feedback_ids})

    def generate_goods_feedback_report(self, business_id: int, format: str = "FILE") -> Optional[Dict]:
        """
        Инициирует генерацию отчета по отзывам о товарах.
        :param business_id: Идентификатор бизнеса.
        :param format: Формат отчета ('FILE' или 'CSV'). По умолчанию 'FILE'.
        :return: Словарь с информацией о статусе генерации отчета или None в случае ошибки.
        """
        if format not in ["FILE", "CSV"]:
            raise ValueError("Недопустимое значение параметра 'format'. Используйте 'FILE' или 'CSV'.")
        return self._send_request("POST", f"reports/goods-feedback/generate", req_params={"format": format}, req_data={"businessId": business_id})
