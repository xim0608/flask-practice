from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def calculate():
    if request.method == 'POST':
        height = request.form['height']
        weight = request.form['weight']
        bmi = float(weight) / float(height) ** 2
    else:
        bmi = ""
    return render_template('calculate.html', bmi=bmi)

if __name__ == "__main__":
    app.run(debug=True)
