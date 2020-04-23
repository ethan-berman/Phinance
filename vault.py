from flask import ( Blueprint, flash, g, redirect, render_template,request,session,url_for)
from db import get_db
import auth
from auth import login_required

bp = Blueprint('vault', __name__)
@bp.route('/')
@login_required
def index():
    db = get_db()
    budgets = db.execute(
        'SELECT p.id, title, Cost, created, author_id, username'
        ' FROM expense p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )
    return render_template('vault/index.html.j2', budgets=budgets)

@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        #category in integer form, client side has deciphering switch statements
        category = request.form['category']
        title = request.form['title']
        body = request.form['body']
        cost = request.form['cost']
        reimbursement = 0
        if request.form['reimbursement'] is "yes":
            reimbursement = 1
        imgurl = 'http://google.com'
        #this imgurl line is gonna have to change lol
        #tru lol it did
        #imgurl = request.form['imgurl']
        error = None
        if not title:
            error = 'title error'
        if not body:
            error = 'body error'
        if not cost:
            error = 'cost error'
        if not reimbursement:
            reimbursement = 'reimbursement error'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO expense (category, title, body, cost, reimbursement, imgurl, author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                (category, title, body, cost, reimbursement, imgurl, g.user['id'])
            )
            db.commit()

            return redirect(url_for('vault.index'))
    budgets = ['Commissary ', 'Phikiea Educator ', 'Treasurer ', 'Rush ', 'House Manager ', 'Wet-Social ', 'Dry-Social ', 'Internal-Social ', 'Historian ']
    return render_template('vault/create.html.j2', budgets=budgets)
@bp.route('/parlor', methods=('GET', 'POST'))
@login_required
def parlor():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        cost = request.form['cost']
        error = None
        if not title:
            error = 'title error'
        if not body:
            error = 'body error'
        if not cost:
            error = 'cost error'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO parlor (title, body, cost, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, cost, g.user['id'])
            )
            db.commit()
            return redirect(url_for('vault.index'))
    return render_template('vault/parlor.html.j2')
