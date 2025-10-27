from database import db

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    layout_data = db.Column(db.Text)
    sold = db.Column(db.Boolean, default=False)  # New field for sold status