from flask import Flask, redirect, request, render_template
import hashlib
import csv

app = Flask(__name__)

csv_filename = "url.csv"

def generate_short_url(url):
    hash_object = hashlib.md5(url.encode())
    hash_value = hash_object.hexdigest()[:6]
    with open(csv_filename, mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        print(hash_value, url)
        csv_writer.writerow([hash_value, url])
    return hash_value
def redirect_to_url(short_url):
    with open(csv_filename, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] == short_url:
                return row[1]
    return "URL not found"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form["url"]
        custom_url = request.form["custom_url"]
        if custom_url == "":
            custom_url = "ContloUrlShortener"
        short_url = generate_short_url(original_url)
        return render_template("result.html", short_url=f"{custom_url}.com/{short_url}", original_url=original_url, click_url=short_url)

    else:
        return render_template("index.html")

@app.route("/<short_url>")

def redirect_to_url(short_url):
    with open(csv_filename, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] == short_url:
                return redirect(row[1])
    return "URL not found"

@app.route("/update", methods=["POST"])
def update_url():
    original_url = request.form["original_url"]
    new_url = request.form["new_url"]
    with open(csv_filename, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = []
        for row in csv_reader:
            if row[1] == original_url:
                row[1] = new_url
            rows.append(row)
    with open(csv_filename, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(rows)
    return redirect("/")

@app.route("/delete/<short_url>", methods=["POST"])
def delete_url(short_url):
    with open(csv_filename, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = []
        row_deleted = False
        for row in csv_reader:
            if row[0] != short_url:
                rows.append(row)
            else:
                row_deleted = True

    with open(csv_filename, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(rows)

    if row_deleted:
        return "Short URL deleted successfully"
    else:
        return "Short URL not found"



if __name__ == "__main__":
    app.run(debug=True)