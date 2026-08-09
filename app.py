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
if __name__ == "__main__":
    app.run(debug=True)
