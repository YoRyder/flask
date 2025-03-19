
from flask import Flask , render_template , request
from sqlalchemy import create_engine, text

app = Flask(__name__)
conn_str = "mysql://root:cset155@localhost/boatdb"
engine = create_engine(conn_str, echo = True)
conn = engine.connect()


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/hello/<name>')
def greeting(name):
    return render_template('User.html',name = name)


@app.route('/boats')
def boats():
   boats = conn.execute(text('select * from boats')).all()
   return render_template('boats.html', boats = boats[:10])
 

@app.route('/boatCreate', methods = ['GET'])
def getBoat():
   return render_template('boat_create.html')


@app.route('/boatCreate', methods = ['POST'])
def createBoat():
    try:
         conn.execute(text('insert into boats values(:id, :name, :type, :owner_id, :rental_price)') , request.form)
         return render_template('boat_create.html', error = None, success ="successful")
    except:
        return render_template('boat_create.html',error = "Failed", success = None)


@app.route('/search', methods=['GET', 'POST'])
def search():
    search_results = None
    search_query = ""  
    if request.method == 'POST':
        search_query = request.form.get('search_query', '')
        search_results = conn.execute(text("Select * from boats where id = :query"),
            {"query": search_query}).all()
    return render_template('search.html', results=search_results, query=search_query)



@app.route('/delete', methods=['GET', 'POST'])
def delete():
    message = None
    if request.method == 'POST':
        boat_id = request.form.get('boat_id')
        result = conn.execute(text("Delete from boats where id = :id"), {"id": boat_id})
        conn.commit()

        if result.rowcount > 0:  
            message = f"Boat with ID {boat_id} has been deleted."
        else:
            message = f"No boat found with ID {boat_id}."
    return render_template('delete.html', message=message)


@app.route('/update', methods=['GET'])
def update_form():
    return render_template('update.html') 

@app.route('/update', methods=['POST'])
def update():
    boat_id = request.form.get('boat_id')
    name = request.form.get('name')
    boat_type = request.form.get('type')
    owner_id = request.form.get('owner_id')
    rental_price = request.form.get('rental_price')
    conn.execute(text("UPDATE boats SET name=:name, type=:type, owner_id=:owner_id, rental_price=:rental_price WHERE id=:id"), {
        "name": name, 
        "type": boat_type, 
        "owner_id": owner_id, 
        "rental_price": rental_price, 
        "id": boat_id
    })
    conn.commit()
    return "Boat updated!"


if __name__ == '__main__':
    app.run(debug=True)





#
# Put into terminal to get flask

#  pip install flask
# pip install flask-sqlalchemy
# pip install mysqlclient
# render_template