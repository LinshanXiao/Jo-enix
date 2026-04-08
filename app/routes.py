from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
COMPANY_EMAIL = os.environ.get("COMPANY_EMAIL")
COMPANY_EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")

def init_app(app):
    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/ecommerce")
    def ecommerce():
        return render_template("ecommerce.html")

    @app.route("/entertainment")
    def entertainment():
        return render_template("entertainment.html")

    @app.route("/ip")
    def ip():
        return render_template("ip.html")

    @app.route("/cases")
    def cases():
        return render_template("cases.html")

    @app.route("/team")
    def team():
        return render_template("team.html")

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip()
            message = request.form.get("message", "").strip()

            if not name or not email or not phone or not message:
                flash("Please fill in all fields.", "error")
                return redirect(url_for("contact"))

            try:
                subject = f"New Contact Enquiry from {name}"

                body = f"""
    You received a new enquiry from your website.

    Name: {name}
    Email: {email}
    Contact Number: {phone}

    Message:
    {message}
    """

                msg = MIMEMultipart()
                msg["From"] = COMPANY_EMAIL
                msg["To"] = RECEIVER_EMAIL
                msg["Subject"] = subject
                msg["Reply-To"] = email
                msg.attach(MIMEText(body, "plain"))

                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                server.login(COMPANY_EMAIL, COMPANY_EMAIL_PASSWORD)
                server.send_message(msg)
                server.quit()

                flash("Your enquiry has been sent successfully.", "success")
                return redirect(url_for("contact"))

            except Exception as e:
                print("Email send error:", e)
                flash("Something went wrong. Please try again later.", "error")
                return redirect(url_for("contact"))

        return render_template("contact.html")

