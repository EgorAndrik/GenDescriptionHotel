from flask import Flask, request, render_template, jsonify
from model import DescriptionGener
from typing import Any, Dict


# Инициализация Flask-приложения и модели генерации описаний
app: Flask = Flask(__name__, static_folder='static', static_url_path='/static')
llm: DescriptionGener = DescriptionGener()


@app.route('/')
def main() -> str:
    """Главная страница приложения."""
    return render_template('welcome.html')


@app.route('/generate')
def generate() -> str:
    """Страница для ввода данных для генерации описания отеля."""
    return render_template('index.html')


@app.route('/get_data', methods=['POST'])
def get_data() -> Any:
    """
    Обработка данных, полученных от клиента для генерации описания отеля.
    Ожидается JSON с информацией об отеле.
    
    Возвращает:
        JSON-ответ с описанием отеля или ошибкой, если данные некорректны.
    """
    data: Dict[str, Any] = request.get_json()  # Получение JSON-данных от клиента
    
    # Извлечение данных об отеле из запроса
    hotel_name: str = data.get('hotelName', '')
    hotel_address: str = data.get('hotelAddress', '')
    price_per_night: str = data.get('pricePerNight', '')
    category: str = data.get('category', '')
    services: str = data.get('services', '')
    features: str = data.get('features', '')

    print("Received data:", data)  # Логирование полученных данных

    # Генерация описания отеля с использованием модели
    response_text: str = llm.genDescription(
        hotel_name=hotel_name,
        hotel_address=hotel_address,
        average_price=price_per_night,
        target_category=category,
        services_description=services,
        hotel_features=features
    )

    print("Generated description:", response_text)  # Логирование результата генерации

    # Возврат JSON-ответа с сгенерированным описанием
    return jsonify({"description": response_text})


# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
