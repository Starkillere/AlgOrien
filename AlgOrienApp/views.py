# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session, flash
from . import KnnOrien
from datetime import timedelta
import os

app = Flask(__name__)

app.config.from_object("config")
app.secret_key = app.config["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(days=5)

@app.route('/')
def acceuil():
    return render_template("accueil.html")

@app.route("/questionnaire", methods=["GET", "POST"])
def questionnaire():
    if request.method == "POST":
        return render_template("resulta.html")
    else:
        return render_template("questionnaire.html")