from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configure the SQLAlchemy part
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weights.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Weight model
class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(50), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    # Fetch all weight entries
    weights = Weight.query.all()
    return render_template("index.html", title="Weight Tracker", weights=weights)

@app.route("/add", methods=["POST"])
def add_weight():
    # Get the weight value and date from the form
    weight_value = request.form.get("weight")
    weight_date = request.form.get("date")
    if weight_value and weight_date:
        new_weight = Weight(value=weight_value, date=weight_date)
        db.session.add(new_weight)
        db.session.commit()
    return redirect(url_for('hello_world'))

