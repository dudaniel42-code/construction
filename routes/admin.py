from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

def create_admin_blueprint():
    admin = Blueprint('admin', __name__)

    from app import app  # Inside function
    from database import db
    from models.plan import Plan

    @admin.route('/')
    def admin_panel():
        plans = Plan.query.all()
        plan_count = len(plans)
        return render_template('admin.html', plans=plans, plan_count=plan_count)

    @admin.route('/upload', methods=['GET', 'POST'])
    def upload_plan():
        from utils.process_plan import process_floor_plan
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            file = request.files['image']
            sold = 'sold' in request.form
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                layout_data = process_floor_plan(file_path)
                plan = Plan(title=title, description=description, image_path=filename, layout_data=layout_data, sold=sold)
                db.session.add(plan)
                db.session.commit()
                return redirect(url_for('admin.admin_panel'))
        return render_template('admin.html')

    @admin.route('/delete/<int:id>', methods=['POST'])
    def delete(id):
        plan = Plan.query.get_or_404(id)
        db.session.delete(plan)
        db.session.commit()
        return redirect(url_for('admin.admin_panel'))

    @admin.route('/edit/<int:id>', methods=['POST'])
    def edit(id):
        plan = Plan.query.get_or_404(id)
        plan.title = request.form['title']
        plan.description = request.form['description']
        plan.sold = 'sold' in request.form
        db.session.commit()
        return redirect(url_for('admin.admin_panel'))

    return admin