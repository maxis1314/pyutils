from flask import Flask,render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/home")
def home():
    return render_template('index.html')
@app.route("/gaga2")
def hello23():
    return "gaga2 World!"    
if __name__ == "__main__":
    app.run(debug=True)
