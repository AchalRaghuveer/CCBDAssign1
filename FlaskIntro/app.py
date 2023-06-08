from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

connection = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:ccbdserver2.database.windows.net,1433;Database=CCBD;Uid=abr2435;Pwd=UTApass3;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')

cursor = connection.cursor()

@app.route("/")
def index():
    cursor = connection.cursor()
    cursor.execute("select * from dbo.[people]")
    data = cursor.fetchall()
    print("length = ", len(data))
    return render_template('index.html')

@app.route("/search", methods=['GET', 'POST'])
def searchName():
    search_query = request.form.get('searchName')
    print('search', search_query)
    cursor = connection.cursor()
    # cursor.execute("select * from dbo.[people]")
    cursor.execute("select picture from dbo.[people] where name = '{}'".format(search_query))
    data = cursor.fetchone()
    print("result = ", data)
    link="https://abr2435assign1.blob.core.windows.net/abr2435container/" + str(data[0])
    print('link----->', link)
    print('link2--->https://abr2435assign1.blob.core.windows.net/abr2435container/chuck.jpg')
    return render_template('index.html', imgLink=link)

@app.route("/money", methods=['GET', 'POST'])
def moneyRange():
    number1 = request.form.get('number1')
    number2 = request.form.get('number2')
    cursor = connection.cursor()
    cursor.execute("select picture from dbo.[people] where salary between ? and ? ",(number1, number2))
    data = cursor.fetchall()
    linkVals = []
    if data:
        print("result = ", data)
        image_paths = [row[0] for row in data if row[0].strip() != '']
        print('after sorting', image_paths)
        for i in range(len(image_paths)):
            print('img val', image_paths[i])
            if len(image_paths[i]) > 0:
                linkVals.append("https://abr2435assign1.blob.core.windows.net/abr2435container/" + str(image_paths[i]))
                print('vals =====> https://abr2435assign1.blob.core.windows.net/abr2435container/', str(image_paths[i]))

    return render_template('index.html', linkVals=linkVals)

if __name__ == "__main__":
    app.run(debug = True)
