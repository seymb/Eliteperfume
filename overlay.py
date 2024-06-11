from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

def create_connection():
    return pyodbc.connect('DRIVER={SQL Server};'
                          'SERVER=LAPTOP-5RV1HQQF;'
                          'DATABASE=EliteperfumeAturay;'
                          )


@app.route('/')
def index():
    return render_template('overlay.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        # Получаем данные из формы
        article = request.form['article']
        productname = request.form['productname']
        volume = request.form['volume']
        purchases = request.form['purchases']

        # Вставка данных в таблицу Product и получаем ID новой записи
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Product 
            SET ProductName = ?, Volume = ?, NumberofPurchases = ?
            WHERE Article = ?
            """, (productname, volume, purchases, article))
        
        conn.commit()
        cursor.close()
        conn.close()

        return 'Данные успешно изменены в базе данных!'
    except Exception as e:
        return f'Ошибка при выполнении запроса: {str(e)}'

@app.route('/nesubmit_form', methods=['POST'])
def nesubmit_form():
    try:
        # Получаем данные из формы
        article = request.form['article']
        productname = request.form['productname']

        # Вставка данных в таблицу Product и получаем ID новой записи
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM Product 
            WHERE Article = ? AND ProductName = ?
            """, (article, productname))
        
        conn.commit()
        cursor.close()
        conn.close()


        return 'Данные успешно удалены из базы данных!'
    except Exception as e:
        return f'Ошибка при выполнении запроса: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)