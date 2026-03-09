from flask import Flask, request, render_template 

app = Flask(__name__)   

# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       building = request.form.get("building")
       # getting input with name = lname in HTML form 
       room_number = request.form.get("room_number") 
       return (f"Your location is {room_number} in {building}")
    return render_template("index.html") # NOTE: what's the point of the argument here? specifying index.html or flask-test.html doesn't seem to make a difference?

if __name__=='__main__':
   app.run()