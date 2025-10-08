from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/resume")
def resume():
	return render_template("resume.html")

@app.route("/projects")
def projects():
	return render_template("projects.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
	if request.method == "POST":
		first = request.form.get("first_name", "").strip()
		last = request.form.get("last_name", "").strip()
		email = request.form.get("email", "").strip()
		password = request.form.get("password", "")
		confirm = request.form.get("confirm_password", "")

		# Basic server-side checks; client validation is enforced via HTML attributes
		errors = []
		if not first:
			errors.append("First name is required.")
		if not last:
			errors.append("Last name is required.")
		if not email:
			errors.append("Email is required.")
		if len(password) < 8:
			errors.append("Password must be at least 8 characters.")
		if password != confirm:
			errors.append("Passwords do not match.")

		if errors:
			for msg in errors:
				flash(msg, "error")
			return render_template("contact.html"), 400

		return redirect(url_for("thankyou"))
	return render_template("contact.html")

@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


if __name__ == "__main__":
	# needed for flash messages
	app.secret_key = "dev-secret"
	app.run(debug=True)


