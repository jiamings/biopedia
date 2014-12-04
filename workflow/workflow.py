from vector9 import Vector9
from werkzeug.utils import secure_filename
import sys
sys.path.append('../')
from flask import Blueprint, make_response, render_template, request, url_for, redirect
workflow_bp = Blueprint('workflow', __name__, template_folder='templates')

@workflow_bp.route('/workflow', methods=['GET'])
def workflow():
    return render_template('workflow.html')

@workflow_bp.route('/handleworkflow', methods=['POST'])
def handleworkflow():
    num = request.form['number']  #total number of block dragged
    a = []   # this list shows what function we should run and what is the order
    print 'here'
    has1 = '0'
    for i in range(1, int(num)+1):
        if request.form[str(i)] == '1':
            has1 = '1'
        if has1 == '1' and request.form[str(i)] == '2':   #judge if 1 is before 2
            return redirect(url_for('workflow'))
        a.append(int(request.form[str(i)]))
        #print request.form[str(i)]

    try:
        file = request.files['importdata']
        file_secure_name = secure_filename(file.filename)

        fvalue = file.read()
        fsvalue = fvalue.split()

        ffvalue = []                        #file float list value
        for i in fsvalue:
            ffvalue.append(float(i))
        ftvalue = tuple(ffvalue)            #file tuple value

        for i in range(1, len(a)):
            if a[i-1] == 1 and a[i] == 2:
                raise Exception

        obj1 = Vector9(ftvalue)
        for i in range(0, len(a)):
            print 'opt', a[i]
            obj1 = obj1.operator(a[i])

        print 'execute sequence is ', a

        output = ""
        for i in obj1.x:
            output = output + str(i) + " "

        print "output is", output

        response = make_response(output)
        response.headers["Content-Disposition"] = "attachment; filename=output.txt"
        return response
    except:
        return redirect(url_for('workflow_bp.workflow'))

