from flask import Flask, render_template, request
import pyodbc
import logging

app = Flask(__name__)

# Подключение к базе данных
conn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=LAPTOP-5RV1HQQF;'
                      'DATABASE=EliteperfumeAturay;'
                      )

@app.route('/')
def index():
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
        logging.error('Ошибка при выполнении запроса: %s', str(e))
        return f'Ошибка при выполнении запроса: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
