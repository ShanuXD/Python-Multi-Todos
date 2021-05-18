from flask import Blueprint, render_template, jsonify
from flask.globals import request
from flask.helpers import flash
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from .models import Note
from . import db
import json

# "views" anme of the blueprint
views = Blueprint("views", __name__)


@views.route("/", methods=["POST", "GET"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")

        if len(note)<3:
            flash("Note is to short!", category="error")
        else:
            new_note = Note(text=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note Added!", category="success")

    return render_template("index.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return ""