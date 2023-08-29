from flask import Flask,render_template, url_for,redirect, request
from forms import NameForm
import json
import mariadb

app=Flask(__name__)

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'sprintvisitor'
}

#app.config['MYSQL_HOST'] = '127.0.0.1'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'sprintvisitor'


app.config['SECRET_KEY'] = '2efff2e8723c48ea1b54e11f00b8d3c3'


# connection for MariaDB
#conn = mariadb.connect(**config)
# create a connection cursor
#cur = conn.cursor()
# execute a SQL statement
#cur.execute("select * from visitor")

   # serialize results into JSON
   #json_data=[]
   #for result in rv:
    #   json_data.append(dict(zip(row_headers,result)))

   # return the results!
   #return json.dumps(json_data)

@app.route('/', methods=['POST','GET'])
@app.route('/home', methods=['POST','GET'])
def home():
    form = NameForm()
    return render_template('home.html', form = form)

@app.route('/add', methods = ['POST', 'GET'])
def add():
    if request.method == 'POST':
        visName = request.form['name']
        #print(visName)
        conn = mariadb.connect(**config)
        print(f"WE ARE CONNECTED ORAYT")
        # create a connection cursor
        cur = conn.cursor()
        # execute a SQL statement
        try:
            #sql = " INSERT INTO visitor (Visitor_ID, Visitor_Name)  VALUES( NULL, '{}')".format(Visitor_ID, Visitor_Name)
            cur.execute("INSERT INTO visitor (Visitor_ID, Visitor_Name) VALUES ('{}','{}')".format(cur.lastrowid,visName))
        except mariadb.Error as e:
            print(f"Error tayo: {e}")
        
        conn.commit()
        print(f"Last Inserted ID iss: {cur.lastrowid}")
        
        conn.close()
        return redirect(url_for('main'))

@app.route('/main')
def main():
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM visitor ORDER BY Visitor_ID DESC LIMIT 1")
        visitorname = cur.fetchall()
        cur.close()
        print(visitorname[0][1])
        return render_template('main.html', vis_name = visitorname )
    except:
        print(f"WE GOT SOME ERROR BOI")

    

if __name__ == '__main__':
    app.run(debug=True)