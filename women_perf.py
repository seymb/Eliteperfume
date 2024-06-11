from flask import Flask, render_template, send_file
import pyodbc
from PIL import Image
import io

app = Flask(__name__)

def create_connection():
    return pyodbc.connect('DRIVER={SQL Server};'
                          'SERVER=LAPTOP-5RV1HQQF;'
                          'DATABASE=EliteperfumeAturay;'
                          )

@app.route('/')
def index():
    try:
        with create_connection().cursor() as cursor:
            cursor.execute("SELECT ID, ProductImage, ProductName, Volume, Price FROM Product")
            products = cursor.fetchall()

            # Преобразуйте результат в список словарей для удобной работы с шаблоном
            products_list = [{'ID': row.ID, 'ProductImage': row.ProductImage, 'ProductName': row.ProductName, 
                              'Volume': row.Volume, 'Price': row.Price} for row in products]

        return render_template('women_perf.html', products=products_list)
    except Exception as e:
        return f'Ошибка при выполнении запроса: {str(e)}'

@app.route('/admin_page')
def admin_page():
    return render_template('admin.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Логика обработки данных после отправки формы
    return 'Form submitted successfully!'

@app.route('/image/<int:product_id>')
def get_image(product_id):
    try:
        with create_connection().cursor() as cursor:
            cursor.execute("SELECT ProductImage FROM Product WHERE ID = ?", product_id)
            result = cursor.fetchone()

            if result and result.ProductImage:
                image_data = result.ProductImage

                try:
                    # Используйте PIL для определения типа изображения
                    image = Image.open(io.BytesIO(image_data))
                    image_type = image.format.lower()

                    # Отправка изображения с правильным mimetype
                    return send_file(io.BytesIO(image_data), mimetype=f'image/{image_type}')
                except Exception as e:
                    print(f'Ошибка при открытии изображения: {str(e)}')
                    return 'Ошибка при открытии изображения'
            else:
                return 'Изображение не найдено'
    except Exception as e:
        print(f'Ошибка при получении изображения: {str(e)}')
        return 'Ошибка при получении изображения'

@app.route('/product_details/<int:product_id>')
def product_details(product_id):
    try:
        with create_connection().cursor() as cursor:
            cursor.execute("SELECT * FROM Product WHERE ID = ?", product_id)
            product = cursor.fetchone()

            if product:
                return render_template('product_page.html', product=product)
            else:
                return 'Товар не найден'
    except Exception as e:
        return f'Ошибка при выполнении запроса: {str(e)}'



if __name__ == '__main__':
    app.run(debug=True)
