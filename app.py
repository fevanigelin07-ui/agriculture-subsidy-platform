from flask import Flask, request, redirect
app = Flask(__name__)
applications = []
@app.route("/")
def home():
    return """
    <h1>Agricultural Subsidy Platform</h1>
    <form action="/apply" method="post">
        Farmer Name:
        <input name="name" required>
        <br><br>
        Crop Name:
        <input name="crop" required>
        <br><br>
        Subsidy Type:
        <input name="subsidy" required>
        <br><br>
        <button type="submit">Apply for Subsidy</button>
    </form>
    <br>
    <a href="/applications">View Applications</a>
    """
@app.route("/apply", methods=["POST"])
def apply():
    app_id = len(applications) + 1

    applications.append({
        "id": app_id,
        "name": request.form["name"],
        "crop": request.form["crop"],
        "subsidy": request.form["subsidy"],
        "status": "Pending"
    })

    return redirect("/applications")
@app.route("/applications")
def view_applications():
    result = "<h1>Subsidy Applications</h1>"

    if not applications:
        result += "<p>No applications found.</p>"

    for a in applications:
        result += f"""
        <hr>
        <b>Application ID:</b> {a['id']}<br>
        <b>Farmer:</b> {a['name']}<br>
        <b>Crop:</b> {a['crop']}<br>
        <b>Subsidy:</b> {a['subsidy']}<br>
        <b>Status:</b> {a['status']}<br>
        """

    result += '<br><a href="/">New Application</a>'
    return result


@app.route("/update/<int:id>/<status>")
def update(id, status):
    for a in applications:
        if a["id"] == id:
            a["status"] = status
            break

    return redirect("/applications")


if __name__ == "__main__":
    app.run(debug=True)
