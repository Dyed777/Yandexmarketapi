from typing import Optional, Dict

class ChatsAPI:

    def get_chats(self, biz_id: int, req_params: Optional[Dict] = None, req_data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Получает список чатов для указанного бизнеса.
        :param biz_id: Идентификатор бизнеса.
        :param req_params: Параметры запроса (опционально).
        :param req_data: Данные запроса (опционально).
        :return: Словарь с данными о чатах или None в случае ошибки.
        """
        params = {k: v for k, v in {"req_params": req_params, "req_data": req_data}.items() if v is not None}

        return self._send_request("POST", f"businesses/{biz_id}/chats", req_params=req_params, req_data={})

    def create_chat(self, business_id: int, order_id: int) -> Optional[Dict]:
        """
        Создает новый чат с покупателем.
        :param business_id: Идентификатор бизнеса.
        :param order_id: Идентификатор заказа.
        :return: Словарь с данными о созданном чате или None в случае ошибки.
        """
        data = {"orderId": order_id}
        return self._send_request("POST", f"businesses/{business_id}/chats/new", req_data=data)

    def send_message_to_chat(self, business_id: int, chat_id: int, message: str) -> Optional[Dict]:
        """
        Отправляет сообщение в указанный чат.
        :param business_id: Идентификатор бизнеса.
        :param chat_id: Идентификатор чата.
        :param message: Текст сообщения.
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        data = {"message": message}
        params = {"chatId": chat_id}
        return self._send_request("POST", f"businesses/{business_id}/chats/message", req_params=params, req_data=data)

    def send_file_to_chat(self, business_id: int, chat_id: int, file_path: str) -> Optional[Dict]:
        """
        Отправляет файл в указанный чат с покупателем.
        :param business_id: Идентификатор бизнеса.
        :param chat_id: Идентификатор чата.
        :param file_path: Путь к файлу для отправки.
        :return: Словарь с результатом операции или None в случае ошибки.
        """
        params = {"chatId": chat_id, "filePath": file_path}
        return self._send_request("POST", f"businesses/{business_id}/chats/file/send", req_params=params)

    def get_chat_history(self, business_id: int, chat_id: int, message_id_from: Optional[int] = None, limit: Optional[int] = None, page_token: Optional[str] = None) -> Optional[Dict]:
        """
        Получает историю сообщений в чате с покупателем.
        :param business_id: Идентификатор бизнеса.
        :param chat_id: Идентификатор чата.
        :param message_id_from: Идентификатор сообщения, начиная с которого нужно получить последующие (опционально).
        :param limit: Количество сообщений на одной странице (опционально).
        :param page_token: Токен для пагинации (опционально).
        :return: Словарь с историей сообщений или None в случае ошибки.
        """
        params = {"chatId": chat_id, "limit": limit, "page_token": page_token}
        data = {"messageIdFrom": message_id_from}
        params = {key: value for key, value in params.items() if value is not None}
        data = {key: value for key, value in data.items() if value is not None}
        return self._send_request("POST", f"businesses/{business_id}/chats/history", req_params=params, req_data=data)
