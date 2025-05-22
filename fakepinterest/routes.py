#render_template ==> traz da pasta templates os arquivos
#url_for ==> permite usar o nome da função de uma rota para um href
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename

@app.route('/', methods=["GET", "POST"])#rota da homepage
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', usuario=usuario.username))
    return render_template('homepage.html', form=formlogin)

@app.route("/criarconta", methods=["GET", "POST"])#rota criar conta
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data, senha=senha, email=formcriarconta.email.data)

        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template('criarconta.html', form=formcriarconta)


@app.route('/perfil/<id_usuario>', methods=["GET", "POST"])#rota do perfil #<usuario> é uma variável
@login_required
def perfil(id_usuario):#função do perfil
    if int(id_usuario) == int(current_user.id):#perfil do usuario logado
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = 
            arquivo.save(caminho)
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template('perfil.html', usuario=current_user.id, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario.id, form=None)

@app.route('/logout')#rota de logout
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))