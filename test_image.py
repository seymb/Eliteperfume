from flask import Flask, render_template, request, send_file
import pyodbc
import io

app = Flask(__name__)

conn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=LAPTOP-5RV1HQQF;'
                      'DATABASE=EliteperfumeAturay;'
                      )

@app.route('/')
def index():
    return render_template('test_image.html')

@app.route('/search', methods=['POST'])
def search_by_number():
    try:
        number = request.form['number']
        cursor = conn.cursor()
        cursor.execute("SELECT ID, ProductImage FROM Product WHERE Article = ?", number)
        images = cursor.fetchall()
        
        # Преобразуйте результат в список словарей для удобной работы с шаблоном
        images_list = [{'ID': row.ID, 'ProductImage': row.ProductImage} for row in images]

        return render_template('test_image.html', images=images_list)
    except Exception as e:
        return f'Ошибка при выполнении запроса: {str(e)}'


@app.route('/image/<int:product_id>')
def get_image(product_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ProductImage FROM Product WHERE ID = ?", product_id)
        result = cursor.fetchone()

        if result and result.ProductImage:
            image_data = result.ProductImage
            return send_file(io.BytesIO(image_data), mimetype='image/jpeg')
        else:
            return 'Изображение не найдено'
    except Exception as e:
        return f'Ошибка при получении изображения: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
