from flask import Flask, request, render_template, redirect, session, jsonify

import datetime
from DBConnection import Db


app = Flask(__name__)
app.secret_key="abc"
static_path=r"C:\Users\moham\OneDrive\Documents\Chat\static\\"


@app.route('/')
def fp():
    return render_template('first_page.html')


@app.route('/login',methods=['get','post'])
def login():
    if request.method=='POST':
        c=request.form['textfield']
        d=request.form['textfield2']
        db=Db()
        q=db.selectOne("select * from login where username='"+c+"' and password='"+d+"'")
        if q is not None:
            if q['user_type']== 'admin':
                session['log'] = "lo"
                return redirect('/admin_home')
            else:
                return "<script>alert('USER NOT FOUND');window.location='/'</script>"
        else:
            return "<script>alert('USER NOT FOUND');window.location='/'</script>"
    return render_template('login.html')



@app.route('/logout')
def logout():
    session['log']=""
    return redirect('/')

@app.route('/admin_home')
def admin_home():
    if session['log'] == "lo":
        return render_template('Admin/ADMIN_INDEX.html')
    else:
        return redirect('/')




@app.route('/add_quote',methods=['get','post'])
def add_quote():
    if session['log'] == "lo":
        if request.method == "POST":
            e = request.form['select']
            q = request.form['textarea']
            db=Db()
            res=db.selectOne("select * from quote where emotion='"+e+"' and quote='"+q+"'")
            if res is not None:
                return '''<script>alert('ALREADY EXIST');window.location='/admin_home'</script>'''
            else:
                db.insert("insert into quote VALUE ('','"+e+"','"+q+"')")
                return '''<script>alert('ADDED SUCCESSFULLY');window.location='/admin_home'</script>'''
        else:
            return render_template('Admin/add_quotes.html')
    else:
        return redirect('/')



@app.route('/view_quote')
def view_quote():
    if session['log'] == "lo":
        db = Db()
        ss=db.selectOne("select * from quote")
        if ss is None:
            return '''<script>alert('NOT AVAILABLE NOW');window.location='/admin_home'</script>'''
        else:
            res=db.select("select * from quote")
            return render_template('Admin/view_quote.html',data=res)
    else:
        return redirect('/')



@app.route('/delete_quote/<q>')
def delete_quote(q):
    if session['log'] == "lo":
        db=Db()
        db.delete("delete from quote where quote_id='"+q+"'")
        return redirect('/view_quote')
    else:
        return redirect('/')



@app.route('/view_user')
def view_user():
    if session['log'] == "lo":
        db = Db()
        ss=db.selectOne("select * from user")
        if ss is None:
            return '''<script>alert('NOT AVAILABLE NOW');window.location='/admin_home'</script>'''
        else:
            res=db.select("select * from user")
            return render_template('Admin/view_user.html',data=res)
    else:
        return redirect('/')



@app.route('/view_complaint')
def view_complaint():
    if session['log'] == "lo":
        db = Db()
        ss = db.selectOne("select * from complaint,user where complaint.user_id=user.user_id")
        if ss is None:
            return '''<script>alert('NOT AVAILABLE NOW');window.location='/admin_home'</script>'''
        else:
            res = db.select("select * from complaint,user where complaint.user_id=user.user_id")
            return render_template('Admin/view_complaint.html',data=res)
    else:
        return redirect('/')



@app.route('/send_reply/<cid>',methods=['get','post'])
def send_reply(cid):
    if session['log'] == "lo":
        if request.method=="POST":
            r=request.form['textarea']
            db=Db()
            db.update("update complaint set reply='"+r+"', r_date=curdate() where complaint_id='"+cid+"'")
            return '''<script>alert('ADDED SUCCESSFULLY');window.location='/view_complaint'</script>'''
        else:
            return render_template('Admin/send_reply.html')
    else:
        return redirect('/')



@app.route('/change_password',methods=['get','post'])
def change_password():
    if session['log'] == "lo":
        if request.method=="POST":
            old_passsword=request.form['textfield']
            new_password=request.form['textfield2']
            confirm_password=request.form['textfield3']
            db=Db()
            res=db.selectOne("select * from login WHERE password='"+old_passsword+"' and user_type='admin'")
            if res is not None:
                if new_password==confirm_password:
                    db.update("update login set password='"+confirm_password+"' where user_type='admin'")
                    return '<script>alert("password changed successfully");window.location="/admin_home"</script>'
                else:
                    return '<script>alert("password mismatch");window.location="/change_password"</script>'
            else:
                return '<script>alert("password is incorrect");window.location="/change_password"</script>'
        return render_template('admin/change_password.html')
    else:
        return redirect("/")



#############################################        USER                #########################################################
#############################################        USER                #########################################################
#############################################        USER                #########################################################


@app.route('/and_login',methods=['post'])
def and_login():
    u=request.form['u']
    p=request.form['p']
    db=Db()
    ss=db.selectOne("select * from login where username='"+u+"' and password='"+p+"'")
    res={}
    if ss is not None:
        # res['type']=ss['user_type']
        # res['lid']=ss['login_id']
        # res['status']="ok"
        return jsonify(type=ss['user_type'], lid=ss['login_id'], status="ok")
    else:
        res['status']="none"
        return jsonify(status="none")



@app.route('/and_register',methods=['post'])
def and_register():
    name=request.form['na']
    plc=request.form['pla']
    pin=request.form['pin']
    dis=request.form['dis']
    em=request.form['em']
    phn=request.form['phn']
    photo=request.files['pic']
    date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    photo.save(static_path + "pic\\"+date+'.jpg')
    userimg="/static/pic/"+ date + '.jpg'
    # date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    # photo.save(r"D:\Project\aa\Chat\pic\\" + date + '.jpg')
    # userimg = "/static/pic/" + date + '.jpg'
    pswd=request.form['pswd']
    db=Db()
    res=db.insert("insert into login VALUE ('','"+em+"','"+pswd+"','user')")
    db.insert("insert into user VALUE ('"+str(res)+"','"+name+"','"+plc+"','"+dis+"','"+pin+"','"+str(userimg)+"','"+em+"','"+phn+"')")
    return jsonify(status="ok")






@app.route('/send_complaint',methods=['post'])
def send_complaint():
    c=request.form['c']
    uid=request.form['id']
    db=Db()
    db.insert("insert into complaint VALUE ('','"+uid+"',curdate(),'"+c+"','pending','pending')")
    return jsonify(status="ok")



@app.route('/and_view_complaint',methods=['post'])
def and_view_complaint():
    uid=request.form['id']
    db=Db()
    res=db.select("select * from complaint where user_id='"+uid+"'")
    if len(res)>0:
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")



@app.route('/and_view_quote',methods=['post'])
def and_view_quote():
    uid=request.form['id']
    db=Db()
    res=db.select("select * from quote")
    if len(res)>0:
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")





@app.route('/and_change_password',methods=['post'])
def and_change_password():
    o=request.form['o']
    n=request.form['n']
    c=request.form['c']
    uid=request.form['id']
    db=Db()
    ss=db.selectOne("select * from login where password='"+o+"' and login_id='"+uid+"'")
    if ss is not None:
        if n==c:
            db=Db()
            db.update("update login set password='"+n+"' where login_id='"+uid+"'")
            return jsonify(status="ok")
        else:
            return jsonify(status="a")
    else:
        return jsonify(status="b")





if __name__ == '__main__':
    app.run()
    # app.run(host="0.0.0.0")
