from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages
from database_connection import connection_pool 
from datetime import datetime, timedelta
from flask import make_response
import requests
import json
import os

app = Flask(__name__)


app.secret_key = os.urandom(24)


# Flask set application context
app.app_context().push()

@app.route('/')
def list_record():
    
    controller()
    
    
    conn = connection_pool.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT reservation.panel_panel_id, reservation.rStatus, reservation.user_name, reservation.rTime FROM reservation INNER JOIN users ON reservation.users_user_id = users.user_id")  # SQL sorgunuzu ayarlayın
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('index.html', data=rows )


def controller():
    conn = connection_pool.get_connection()
    cursor = conn.cursor()
    query = "SELECT panel_panel_id, rTime FROM reservation"
    cursor.execute(query)
    data = cursor.fetchall()

    now = datetime.now()

    for p_id, datetime_str in data:
       
        
        if datetime_str is not None and '-' in datetime_str:
             
            try:
                
                time_str, date_str = datetime_str.split('-')
                
                # date and time objects
                result_date = datetime.strptime(date_str, "%d.%m.%Y")
                result_time = datetime.strptime(time_str, "%H:%M")
                
                
                
                now_time = datetime.strftime(now, "%H:%M")
            
                

                if now.date() > result_date.date() or (now.date() == result_date.date() and now_time > result_time.strftime("%H:%M")):

                    cursor.execute("SELECT * FROM panel WHERE panel_id = %s FOR UPDATE", (p_id,))
                    result = cursor.fetchone()
                    
                    query2 = "DELETE FROM reservation WHERE reservation.panel_panel_id = (%s)"                
                    cursor.execute(query2,(p_id,))

                    panel_update = "UPDATE panel SET rStatus = 'available' WHERE  panel.panel_id =  (%s)"
                    cursor.execute(panel_update,( p_id,))  
                    
                    conn.commit()
                    
          
            except Exception as e:
                        print("Error:", e)
                        conn.rollback()
        elif datetime_str is not None and '.' in datetime_str:
            try:
                result_date = datetime.strptime(datetime_str,"%d.%m.%Y")
                

                if result_date.date() < now.date():

                    cursor.execute("SELECT * FROM panel WHERE panel_id = %s FOR UPDATE", (p_id,))
                    result = cursor.fetchone()
                
                    query3 = "DELETE FROM reservation WHERE reservation.panel_panel_id = (%s)"                
                    cursor.execute(query3,(p_id,))

                    panel_update = "UPDATE panel SET rStatus = 'available' WHERE  panel.panel_id = (%s)"
                    cursor.execute(panel_update,( p_id,))
                    conn.commit()
                    
                    
              

            except Exception as e:
                    print("Error:", e)
                    conn.rollback()
    cursor.close()
    conn.close()



@app.route('/add_reservation', methods=['POST'])
def add_reservation():

    if request.method == 'POST':
        # data from the form
        name = request.form['name']
        panel = request.form['panel']
        
        conn = connection_pool.get_connection()
        global message
    

        if conn.is_connected:
            print("Database is connected.")
            
            cursor = conn.cursor()
            control = "SELECT panel.rStatus FROM panel WHERE panel.panel_id = (%s)"
            cursor.execute(control,(panel,))
            result = cursor.fetchone()
            
                


            if result is not None:
                
                

                if "available" == result[0]:

                    try:
                        
                    
                        if end_time() is not None :

                            cursor.execute("SELECT * FROM panel WHERE panel_id = %s FOR UPDATE", (panel,))
                            result_ = cursor.fetchone()
                
                            add_user = "INSERT INTO users (name) VALUES (%s)"
                            cursor.execute(add_user,(name,))
                        
                            add_panel = "UPDATE panel SET rStatus = 'not available' WHERE  panel.panel_id =  (%s)"
                            cursor.execute(add_panel,(panel,))

                            # get the user who made the reservation
                            cursor.execute("SELECT LAST_INSERT_ID()")
                            last_inserted_id = cursor.fetchone()[0]
                    
                            # get the name of the user who made the reservation
                            get_user_name_query = "SELECT name FROM users WHERE user_id = %s"
                            cursor.execute(get_user_name_query, (last_inserted_id,))
                            last_inserted_user_name = cursor.fetchone()[0]

                        
                            add_reservations = "INSERT INTO reservation(users_user_id,panel_panel_id,rTime,rStatus,user_name) VALUES (%s,%s,%s,%s,%s)"
                            cursor.execute(add_reservations,(last_inserted_id,panel,end_time(),"not available",last_inserted_user_name,))

                            conn.commit()                                 
                            
                            
                            webhook(name, panel, end_time())
                            
                            flash("Reservation successfull!", 'success')
                            return redirect(request.referrer)
                        else:
                            
                            flash("Timestamp format is incorrect or outdated", 'error')
                            return redirect(request.referrer)

                        

                    except Exception as e:
                        print("Error:", e)
                        conn.rollback()
                          
                        
                        flash("Reservation not successfull", 'error')
                        return redirect(request.referrer)
                    
                        
                    finally:
                    
                        cursor.close()
                        conn.close()
                               
                else:
                
                   
                    
                    cursor.close()
                    conn.close()
                    
                    
                    flash("Unavailable panel!", 'error')
                    return redirect(request.referrer)
                    
                

            else:
                
                
                cursor.close()
                conn.close()
                
                
                
                flash("Invalid panel_id!", 'error')
                return redirect(request.referrer)

        else:
            
            print("Could not connect to database")
            
            conn.close()
            
              
            
            flash("Error:  Could not connect to database.", 'error')
            return redirect(request.referrer)


def panels():
    
    for i in range(100,201):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM panel WHERE panel_id = %s"
        cursor.execute(query,(i,))
        row_count = cursor.fetchone()[0]

        try:
            if row_count == 0:
                query1 = "INSERT INTO panel (panel_id,rStatus) VALUES (%s,%s)"
                cursor.execute(query1,(i,"available",))
                conn.commit() 
        except Exception as e:
                print("Error:", e)
                conn.rollback()
                    
        finally:
            cursor.close()
            conn.close()

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        search = request.form['search_term']
        
        
        if search != "":
            conn = connection_pool.get_connection()
            cursor = conn.cursor()
            query = "SELECT reservation.panel_panel_id, reservation.rStatus, reservation.user_name, reservation.rTime FROM reservation WHERE reservation.panel_panel_id = (%s)"
            cursor.execute(query,(search,))
            

            
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return render_template('index.html', data=rows)       
            
        else:
            
            return redirect(url_for('list_record'))

def end_time():

    try:        
        reservation_time_str = request.form['hours']
        if reservation_time_str.isdigit():
            reservation_time = int(reservation_time_str)

            now = datetime.now()
            temp = now + timedelta(hours=reservation_time)

            end_time_ = temp.strftime("%H:%M-%d.%m.%Y")

            return end_time_
        elif not reservation_time_str:
            day = datetime.today()
            today = datetime.strftime(day,"%d.%m.%Y")
            return today
        else:
            result_date = datetime.strptime(reservation_time_str,"%d.%m.%Y")
            reservation_time_ = result_date.strftime("%d.%m.%Y")
            now = datetime.now()
            if result_date.date() < now.date():
                reservation_time_ = None
            else:
                return reservation_time_

    except Exception as e:
        print("Error:", e)
    

 
@app.route('/remove', methods=['POST'])
def remove_reservation():
    if request.method == 'POST':
        # get form data from user
        confirmation = request.form.get('confirmation')
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        global message

        if confirmation == 'yes':
      
                
            try:
                item_id = request.form.get('panel_id')

                cursor.execute("SELECT * FROM panel WHERE panel_id = %s FOR UPDATE", (item_id,))
                result_ = cursor.fetchone()

                temp_query = "SELECT reservation.users_user_id FROM reservation WHERE reservation.panel_panel_id = (%s)"
                cursor.execute(temp_query,(item_id,))
                result = cursor.fetchone()[0]

                query = "DELETE FROM reservation WHERE reservation.panel_panel_id = (%s)"                
                cursor.execute(query,(item_id,))

                add_panel = "UPDATE panel SET rStatus = 'available' WHERE  panel.panel_id =  (%s)"
                cursor.execute(add_panel,(item_id,))

                remove_user = "DELETE FROM users WHERE users.user_id =(%s)"
                cursor.execute(remove_user,(result,))

                conn.commit()
               
                flash("Reservation removed.", 'success')
                return redirect(request.referrer)
            except Exception as e:
                
                conn.rollback()
                flash("Reservation not removed.", 'error')
                return redirect(request.referrer)
                

            finally:
                
                    cursor.close()
                    conn.close()
                    
                    print("Database connection closed.(Remove)")      
        
        return redirect(url_for('list_record'))

def webhook(name,panel,time):
    url ='https://example.com/webhook-endpoint'
    payload = {
        "title": panel,
        "text" : name + ", " + panel + " panelini " + time + " sonuna kadar rezerve etti."
        #"text" : name + " reserved panel " + panel + " until date " + time
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.text.encode('utf8'))




panels()
#list_record()

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=8000)
    '''from gunicorn.app.wsgiapp import WSGIApplication
    app = WSGIApplication()
    app.run()'''
