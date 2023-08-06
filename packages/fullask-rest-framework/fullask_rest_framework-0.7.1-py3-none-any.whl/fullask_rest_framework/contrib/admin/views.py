from flask import Blueprint, render_template

admin_bp = Blueprint("AdminPage", __name__, template_folder="./templates")


@admin_bp.get("/")
def admin_index():
    return render_template("index.html")
