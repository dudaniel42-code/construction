from flask import Blueprint, render_template, request, redirect, url_for
from database import db
from models.plan import Plan

def create_main_blueprint():
    # Create the blueprint
    main = Blueprint('main', __name__)

    @main.route('/')
    def index():
        return render_template('index.html')

    @main.route('/plans')
    def plans():
        plans = Plan.query.all()
        return render_template('plans.html', plans=plans)

    @main.route('/plan/<int:id>')
    def plan_detail(id):
        plan = Plan.query.get_or_404(id)
        return render_template('plan_detail.html', plan=plan)

    @main.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            # Handle contact form (e.g., save to DB or send email)
            return redirect(url_for('main.index'))
        return render_template('contact.html')

    @main.route('/why_choose_us')
    def why_choose_us():
        return render_template('why_choose_us.html')

    @main.route('/about')
    def about():
        return render_template('about.html')

    return main