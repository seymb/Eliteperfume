from flask import Flask, render_template, send_file, request
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
    return render_template('main.html')

@app.route('/admin_page')
def admin_page():
    return render_template('admin.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        # Получаем данные из формы
        article = request.form['article']
        category = request.form['category']
        productname = request.form['productname']
        volume = request.form['volume']
        price = request.form['price']
        price10 = request.form['price10']
        price30 = request.form['price30']
        price50 = request.form['price50']
        price100 = request.form['price100']
        production = request.form['production']
        tradinghouse = request.form['tradinghouse']
        creation = request.form['creation']
        purpose = request.form['purpose']
        productType = request.form['productType']
        aromanotes = request.form['aromanotes']
        purchases = request.form['purchases']
        overview = request.form['overview']
        image = request.files['fileInput']
        image_data = image.read()

        # Вставка данных в таблицу Product и получаем ID новой записи
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Product 
            (Article, Category, ProductName, Volume, Price, Price10, Price30, Price50, Price100, Production, TradingHouse, DateofCreation, Assignment, ProductType, FlavorNotes, NumberofPurchases, Descript, ProductImage) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, article, category, productname, volume, price, price10, price30, price50, price100, production, tradinghouse, creation, purpose, productType, aromanotes, purchases, overview, pyodbc.Binary(image_data))
        
        conn.commit()
        cursor.close()

        return 'Данные успешно сохранены в базе данных!'
    except Exception as e:
        return f'Ошибка при выполнении запроса: {str(e)}'

@app.route('/women_perf')
def women_perf():
    try:
        with create_connection().cursor() as cursor:
            cursor.execute("SELECT ID, ProductImage, ProductName, Volume, Price FROM Product WHERE Category = 'Мужская'")
            products = cursor.fetchall()

            # Преобразуйте результат в список словарей для удобной работы с шаблоном
            products_list = [{'ID': row.ID, 'ProductImage': row.ProductImage, 'ProductName': row.ProductName, 
                              'Volume': row.Volume, 'Price': row.Price} for row in products]

        return render_template('women_perf.html', products=products_list)
    except Exception as e:
        return f'Ошибка при выполнении запроса: {str(e)}'

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