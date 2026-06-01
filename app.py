from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# 🔐 Load credentials from environment variables (secure practice)
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "admin123")

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

        # ✅ Secure comparison using env variables
        if username == ADMIN_USER and password == ADMIN_PASS:
            message = "Login Successful"
        else:
            message = "Invalid Credentials"

    return render_template_string(LOGIN_HTML, message=message)

if __name__ == "__main__":
    # ❌ never use debug=True in security projects
    app.run(debug=False, host="127.0.0.1")
