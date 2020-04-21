from application import app, auth, Config, functions, CCR_Function, modals
from flask import render_template, make_response, send_from_directory, request, json, Response, stream_with_context
from werkzeug.utils import secure_filename
import os, time
import pandas as pd

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['GET','POST'])
@auth.auth_required
def dashboard():
    return render_template('dashboard.html', dashboard=True, flag=functions.file_contents(), data=functions.path_data(), regions_list=functions.regions_list())

@app.route('/static/uploads/<path:filename>')
@auth.auth_required
def download_file(filename):
    return send_from_directory(os.path.join(Config.BASE_DIR,Config.UPLOAD_FOLDER), filename=filename, as_attachment=True)

@app.route('/upload_file', methods=['POST'])
@auth.auth_required
def upload_file():
    if request.method == "POST":
        file = request.files['path_file']
        if file and functions.allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            filename = "Path_Updates.csv"
            file.save(os.path.join(Config.BASE_DIR, Config.UPLOAD_FOLDER, filename))
            return "Upload Success"
        else:
            return "Upload Error"
    else:
        return "Error"
 
@app.route('/mi_info_process', methods=['POST'])
@auth.auth_required
def process_mi_info():
    if request.method == "POST":
        try:
            query = "SELECT mi_type, otc_exp_cob, otc_sensi_cob, exp_stavros_cob, sensi_stavros_cob, prev_sensi_cob from mi_infos WHERE mi_id = ?"
            rv = modals.query_db(query, [1], one=True)
            if rv is None:
                insert_query = "INSERT INTO mi_infos (mi_id, mi_type, otc_exp_cob, otc_sensi_cob, exp_stavros_cob, sensi_stavros_cob, prev_sensi_cob) VALUES (?,?,?,?,?,?,?)"
                insert_args = (1,request.form['sel_week_mon'],request.form['otc_exp_cob'],request.form['otc_sensi_cob'],request.form['exp_stavros_cob'],request.form['sensi_stavros_cob'],request.form['prev_sensi_cob'])
                msg = modals.write_db(insert_query,insert_args,"added")
                print("MI Infos",msg)
            else:
                up_qry = "UPDATE mi_infos SET mi_type=?, otc_exp_cob=?, otc_sensi_cob=?, exp_stavros_cob=?, sensi_stavros_cob=?, prev_sensi_cob=? WHERE mi_id = ?"
                up_args = (request.form['sel_week_mon'],request.form['otc_exp_cob'],request.form['otc_sensi_cob'],request.form['exp_stavros_cob'],request.form['sensi_stavros_cob'],request.form['prev_sensi_cob'],1)
                msg = modals.write_db(up_qry, up_args,"updated")
                print("MI Infos",msg)
            return "MI Success"
        except:
            return "MI Error"
    else:
        return "Error"

@app.route('/start_process', methods=['POST'])
@auth.auth_required
def process_start():
    start = time.time()
    if request.method == "POST":
        try:
            query = "SELECT mi_type, otc_exp_cob, otc_sensi_cob, exp_stavros_cob, sensi_stavros_cob, prev_sensi_cob from mi_infos WHERE mi_id = ?"
            rv = modals.query_db(query, [1], one=True)
            if rv is not None:
                query = "SELECT sites, scenarios, risk_factors from start WHERE start_id = ?"
                rv = modals.query_db(query, [1], one=True)
                if rv is None:
                    print("start_insert")
                    insert_query = "INSERT INTO start (start_id, sites, scenarios, risk_factors) VALUES (?,?,?,?)"
                    insert_args = (1,request.form['site_select'],request.form['scenarios_select'],request.form['risk_factor_select'])
                    msg = modals.write_db(insert_query,insert_args,"added")
                    print("Start Process",msg)
                else:
                    print("update_start")
                    up_qry = "UPDATE start SET sites=?,scenarios=?,risk_factors=? WHERE start_id = ?"
                    up_args = (request.form['site_select'],request.form['scenarios_select'],request.form['risk_factor_select'],1)
                    msg = modals.write_db(up_qry, up_args,"updated")
                    print("Start Process",msg)
                
                # Import CCR Access Python Function 
                CCR_Function.Global_EUC()
                end = time.time()
                elapsed_time = round((end-start)/60,2)

                up_qry = "UPDATE script_progress SET elapsed_time = ?, status = ? WHERE script_id = ?"
                up_args = (elapsed_time,'completed',1)
                msg = modals.write_db(up_qry, up_args,"updated")
                print(msg)

                return "MI Success"
            else:
                return "MIInfo Not Set"
        except Exception as e:
            return "Start Error",e
    else:
        return "Start Error"



@app.route('/logout')
def logout():
    table_names = ['mi_infos','start','script_progress']
    for table_name in table_names:
        query = f"DELETE FROM {table_name}"
        msg = modals.truncate_db(query)
        print(table_name,msg)

    return make_response(render_template('login.html'), 401, {'WWW-Authenticate':'Basic Realm = "Login Required"'})

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_pages/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error_pages/500.html'), 500

@app.errorhandler(400)
def bad_request(error):
    return render_template('error_pages/400.html'), 400

@app.errorhandler(401)
def unauthorized(error):
    return render_template('error_pages/401.html'), 401

@app.errorhandler(403)
def forbidden(error):
    return render_template('error_pages/403.html'), 403

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('error_pages/405.html'), 405

@app.errorhandler(503)
def service_unavailable(error):
    return render_template('error_pages/503.html'), 503


@app.route('/progress')
def progress():
    def generate():
        x = 0
        data = {}
        query = "SELECT current_count, total_fn_count, status from script_progress WHERE script_id = ?"
        time.sleep(1)
        rv = modals.query_db(query, [1], one=True)
        if (rv is not None):
            while x <= rv[1]:
                query = "SELECT current_count, total_fn_count from script_progress WHERE script_id = ?"
                rv = modals.query_db(query, [1], one=True)
                print("Current {}, Total {}".format(rv[0],rv[1]))
                x = int((rv[0]/rv[1])*100)
                data['msg'] = 'Status Fine'
                data['pct'] = str(x)
                try:
                    data['elapsed_time'] = str(rv[2])
                except:
                    data['elapsed_time'] = '0'
                print(data)
                yield "data: " + json.dumps(data) + "\n\n"
        
        else:
            data = {}
            data['msg'] = 'No Data'
            data['pct'] = '0'
            data['elapsed_time'] = '0'
            print(data)
            yield "data: " + json.dumps(data) + "\n\n"
            
    return Response(stream_with_context(generate()), mimetype= 'text/event-stream')

