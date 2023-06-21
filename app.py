from flask import Flask, render_template, request
import pyodbc
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)


connection = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:ccbdserver1.database.windows.net,1433;Database=CCBD;Uid=abr2435;Pwd=UTApass3;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')

cursor = connection.cursor()


@app.route("/")
def index():
    cursor = connection.cursor()
    cursor.execute("select * from dbo.[city]")
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
    link = "https://abr2435assign1.blob.core.windows.net/abr2435container/" + str(data[0])
    print('link----->', link)
    print('link2--->https://abr2435assign1.blob.core.windows.net/abr2435container/chuck.jpg')
    return render_template('index.html', imgLink=link)


@app.route("/money", methods=['GET', 'POST'])
def moneyRange():
    number1 = request.form.get('number1')
    number2 = request.form.get('number2')
    cursor = connection.cursor()
    cursor.execute("select picture from dbo.[people] where salary between ? and ? ", (number1, number2))
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


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    # img = request.form.get('img')
    img = request.files['img']
    name = request.form.get('name')
    cursor = connection.cursor()
    msg = upload(img)
    cursor.execute("update dbo.[people] set Picture=? where Name=?", (img.filename, name))

    return render_template('index.html', msg=msg)


def upload(file):
    account_url = "DefaultEndpointsProtocol=https;AccountName=abr2435assign1;AccountKey=vD9scxZxq94P15DKDccDeGj1I10NJJux8Y8Qh6tTdM9ubazSBLqs7QyxVYvIR/ehAhUgmNKgSS3I+AStWiOwEg==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(account_url)
    container_client = blob_service_client.get_container_client("abr2435container")
    print("File", file)
    blob_client = container_client.upload_blob(name=file.filename, data=file.stream, overwrite=True)
    return "success"


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    name = request.form.get('nameDelete')
    print("name ===> ", name)
    cursor.execute("delete from dbo.[people] where Name=?", (name,))
    connection.commit()
    return render_template('index.html', msg3="Deleted")


@app.route("/change", methods=['GET', 'POST'])
def change():
    name = request.form.get('nameChange')
    descript = request.form.get('descript')
    print("name ===> ", name)
    cursor.execute("update dbo.[people] set Keywords=? where Name=?", (descript, name))
    connection.commit()
    return render_template('index.html', msg4="Changed")

@app.route("/salary", methods=['GET', 'POST'])
def salary():
    name = request.form.get('nameSal')
    salary = request.form.get('salary')
    print("name ===> ", name)
    cursor.execute("update dbo.[people] set Salary=? where Name=?", (salary, name))
    connection.commit()
    return render_template('index.html', msg5="Changed")


if __name__ == "__main__":
    app.run(debug=True)
