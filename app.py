from flask import Flask, render_template, request, send_file
from utils.pdf_generator import generate_pdf
import os

app = Flask(__name__)




@app.route("/", methods=["GET", "POST"])
def quotation():
    if request.method == "POST":

        items = request.form.getlist("item[]")
        qtys = request.form.getlist("qty[]")
        rates = request.form.getlist("rate[]")

        data = {
            "client": request.form["client"],
            "date": request.form["date"],
            "place": request.form["place"],
            "items": list(zip(items, qtys, rates))
        }

        
        pdf_path = generate_pdf(data)

        return send_file(pdf_path, as_attachment=True)

    return render_template("quotation_form.html")

if __name__ == "__main__":
    app.run()
