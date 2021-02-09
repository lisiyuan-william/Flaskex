# -*- coding: utf-8 -*-

import json
import os

from flask import Flask, redirect, url_for, request, session, render_template

from scripts.functions import get_sql_table as gst
from scripts.functions import quote_str_list as qs

app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only


# Heroku
# from flask_heroku import Heroku
# heroku = Heroku(app)

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('sql_tables.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


@app.route('/do-get-tables', methods=['POST'])
def do_get_tables():
    sql = request.form['data']
    tables = gst.extract_table_name_from_sql(sql)
    return json.dumps('\n'.join(tables))


@app.route('/do-quote-strs', methods=['POST'])
def do_quote_str():
    data = json.loads(request.get_data(as_text=True))
    pre = '"' if data['pre'] is None else data['pre']
    after = data['after'] if data['after'] is None else '"'
    ls = qs.quote(data['txt'], data['df'], pre, after)
    return json.dumps('\n'.join(ls))


# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0")
