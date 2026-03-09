from flask import Flask, request, render_template 

app = Flask(__name__)   

# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       first_name = request.form.get("fname")
       # getting input with name = lname in HTML form 
       last_name = request.form.get("lname") 
       return (f"Your name is {first_name} {last_name}")
    return render_template("index.html") # NOTE: what's the argument here? specifying index.html or flask-test.html doesn't seem to make a difference?

if __name__=='__main__':
   app.run()