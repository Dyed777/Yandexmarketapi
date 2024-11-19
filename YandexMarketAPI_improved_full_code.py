import requests
import json
import logging
from typing import Dict, Optional
from Business import BusinessesAPI
from Campaigns  import CampaignsAPI
from Categories import CategoriesAPI
from Chats import ChatsAPI
from Feedback import  FeedbackAPI
from Offers import  OffersAPI
from Promos import PromosAPI
from Regions import  RegionsAPI
from Reports import ReportsAPI
from Werhouses import  WarehousesAPI

# Настройка логирования
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def print_response(data: Optional[Dict], description: str):
    if data:
        print(f"{description}:", json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"Не удалось получить {description.lower()}.")

class YandexMarketAPI(BusinessesAPI):  # Наследуем CampaignsAPI
    BASE_URL = "https://api.partner.market.yandex.ru/v2"

    def __init__(self, client_id: str, api_key: str):
        self.client_id = client_id
        self.api_key = api_key
        self.headers = {
            "Api-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def _send_request(self, method: str, endpoint: str, req_params: Optional[Dict] = None, req_data: Optional[Dict] = None) -> Optional[Dict]:
        response = None
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, params=req_params, json=req_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response is not None:
                logging.error(f"HTTP ошибка: {http_err}")
                logging.error(f"Ответ сервера: {response.text}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Ошибка запроса: {req_err}")
        return None

if __name__ == "__main__":
    client_id = "914570202"
    api_key = "ACMA:EiUUExLd1nFnCRqsg56RzJuVJ2b0r1FsfHy3Owoi:5dc195fa"
    api = YandexMarketAPI(client_id, api_key)

    a=api.get_bids_recommendations
    print_response(a,"Отзывы о товаре")