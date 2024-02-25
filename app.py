from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/aboutus.html')
def aboutus():
    return render_template("aboutus.html")

@app.route('/contact.html')
def contact():
    return render_template("contact.html")

@app.route('/bolg.html')
def blog():
    return render_template("bolg.html")

@app.route('/wannatry.html')
def wannatry():
    return render_template("wannatry.html")

if __name__ == "__main__":
    app.run(debug=True)