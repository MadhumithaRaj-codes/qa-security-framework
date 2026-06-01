from flask import Flask, request, render_template_string

app = Flask(__name__)

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>QA Security Framework</title>
</head>
<body>

<h2>Login Page</h2>

<form method="POST">
    <input type="text" name="username" placeholder="Username">
    <br><br>

    <input type="password" name="password" placeholder="Password">
    <br><br>

    <button type="submit">Login</button>
</form>

{% if message %}
<p>{{ message }}</p>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "password123":
            message = "Login Successful"
        else:
            message = "Invalid Credentials"

    return render_template_string(LOGIN_HTML, message=message)

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1")