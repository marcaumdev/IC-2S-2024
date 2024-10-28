import json
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask('Clima Saúde')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/BD_Clima_Saude'

mybd = SQLAlchemy(app)

#------------- TABELAS -------------

# Pais
class Pais(mybd.Model):
    __tablename__ = "pais"
    id = mybd.Column(mybd.Integer, primary_key=True, autoincrement=True, unique=True)
    nome = mybd.Column(mybd.String(100))
    sigla = mybd.Column(mybd.String(5))
    densidade = mybd.Column(mybd.Integer)
    area = mybd.Column(mybd.Float)

    def to_json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "sigla": self.sigla,
            "densidade": self.densidade,
            "area": self.area
        }
    
# Mortes
class Mortes(mybd.Model):
    __tablename__ = "mortes"
    id = mybd.Column(mybd.Integer, primary_key=True, autoincrement=True, unique=True)
    id_pais = mybd.Column(mybd.Integer, mybd.ForeignKey('pais.id'))
    ano = mybd.Column(mybd.Integer)
    quantidade = mybd.Column(mybd.Integer)

    pais = mybd.relationship('Pais')

    def to_json(self):
        return {
            "id": self.id,
            "id_pais": self.id_pais,
            "ano": self.ano,
            "quantidade": self.quantidade
        }

# Emissão
class Emissao(mybd.Model):
    __tablename__ = 'emissao'

    id = mybd.Column(mybd.Integer, primary_key=True, autoincrement=True, unique=True)
    id_pais = mybd.Column(mybd.Integer, mybd.ForeignKey('pais.id'))
    ano = mybd.Column(mybd.Integer)
    total = mybd.Column(mybd.Float)
    carvao = mybd.Column(mybd.Float)
    petroleo = mybd.Column(mybd.Float)
    gas = mybd.Column(mybd.Float)
    cimento = mybd.Column(mybd.Float)
    queima = mybd.Column(mybd.Float)
    outros = mybd.Column(mybd.Float)

    pais = mybd.relationship('Pais')

    def to_json(self):
        return {
            "id": self.id,
            "id_pais": self.id_pais,
            "ano": self.ano,
            "total": self.total,
            "carvao": self.carvao,
            "petroleo": self.petroleo,
            "gas": self.gas,
            "cimento": self.cimento,
            "queima": self.queima,
            "outros": self.outros
        }

# Temperatura
class Temperatura(mybd.Model):
    __tablename__ = 'temperatura'

    id = mybd.Column(mybd.Integer, primary_key=True, autoincrement=True, unique=True)
    id_pais = mybd.Column(mybd.Integer, mybd.ForeignKey('pais.id'))
    ano = mybd.Column(mybd.Integer)
    indice = mybd.Column(mybd.Float)

    pais = mybd.relationship('Pais')

    def to_json(self):
        return {
            "id": self.id,
            "id_pais": self.id_pais,
            "ano": self.ano,
            "indice": self.indice
        }

#------------- GETS BY ID -------------

# Pais
@app.route("/paises/<id>", methods=["GET"])
def seleciona_pais_id(id):
    pais_objetos = Pais.query.filter_by(id=id).first()

    if(pais_objetos == None):
        return gera_response(404, "pais", {}, "Pais não encontrado!")

    pais_json = pais_objetos.to_json()

    return gera_response(200, "pais", pais_json)

# Mortes
@app.route("/mortes/<id>", methods=["GET"])
def seleciona_mortes_id(id):
    mortes_objetos = Mortes.query.filter_by(id=id).first()

    if(mortes_objetos == None):
        return gera_response(404, "mortes", {}, "Mortes não encontradas!")

    mortes_json = mortes_objetos.to_json()

    return gera_response(200, "mortes", mortes_json)

# Emissao
@app.route("/emissao/<id>", methods=["GET"])
def seleciona_emissao_id(id):
    emissao_objetos = Emissao.query.filter_by(id=id).first()

    if(emissao_objetos == None):
        return gera_response(404, "emissao", {}, "Emissão não encontrada!")

    emissao_json = emissao_objetos.to_json()

    return gera_response(200, "emissao", emissao_json)

# Temperatura
@app.route("/temperatura/<id>", methods=["GET"])
def seleciona_temperatura_id(id):
    temperatura_objetos = Temperatura.query.filter_by(id=id).first()

    if(temperatura_objetos == None):
        return gera_response(404, "temperatura", {}, "Temperatura não encontrada!")

    temperatura_json = temperatura_objetos.to_json()

    return gera_response(200, "temperatura", temperatura_json)

#------------- GETS ALL -------------

# Pais
@app.route("/paises", methods=["GET"])
def selecionar_paises():
    paises_objetos = Pais.query.all()

    paises_json = [pais.to_json() for pais in paises_objetos]

    return gera_response(200, "pais", paises_json)

# Mortes
@app.route("/mortes", methods=["GET"])
def selecionar_mortes():
    mortes_objetos = Mortes.query.all()

    mortes_json = [mortes.to_json() for mortes in mortes_objetos]

    return gera_response(200, "mortes", mortes_json)

# Emissao
@app.route("/emissao", methods=["GET"])
def selecionar_emissao():
    emissao_objetos = Emissao.query.all()

    emissao_json = [emissao.to_json() for emissao in emissao_objetos]

    return gera_response(200, "emissao", emissao_json)

# Temperatura
@app.route("/temperatura", methods=["GET"])
def selecionar_temperatura():
    temperatura_objetos = Temperatura.query.all()

    temperatura_json = [temperatura.to_json() for temperatura in temperatura_objetos]

    return gera_response(200, "temperatura", temperatura_json)

# ------------- POSTS -------------

# Pais
@app.route("/paises", methods=["POST"])
def criar_pais():
    body = request.get_json()
    try:
        pais = Pais(
            nome = body["nome"],
            sigla = body["sigla"],
            densidade = body["densidade"],
            area = body["area"]
        )

        mybd.session.add(pais)
        mybd.session.commit()

        return gera_response(201, "pais", pais.to_json(), "Criado com Sucesso!!!")
    
    except Exception as e:
        print('Erro', e)

        return gera_response(400, "pais", {}, "Erro ao cadastrar!!!")
    
# Mortes
@app.route("/mortes", methods=["POST"])
def criar_mortes():
    body = request.get_json()
    try:
        mortes = Mortes(
            id_pais = body["id_pais"],
            ano = body["ano"],
            quantidade = body["quantidade"]
        )

        mybd.session.add(mortes)
        mybd.session.commit()

        return gera_response(201, "mortes", mortes.to_json(), "Criada com Sucesso!!!")
    
    except Exception as e:
        print('Erro', e)

        return gera_response(400, "mortes", {}, "Erro ao cadastrar!!!")

# Emissao
@app.route("/emissao", methods=["POST"])
def criar_emissao():
    body = request.get_json()
    try:
        emissao = Emissao(
            id_pais = body["id_pais"],
            ano = body["ano"],
            total = body["total"],
            carvao = body["carvao"],
            petroleo = body["petroleo"],
            gas = body["gas"],
            cimento = body["cimento"],
            queima = body["queima"],
            outros = body["outros"],
        )

        mybd.session.add(emissao)
        mybd.session.commit()

        return gera_response(201, "emissao", emissao.to_json(), "Criada com Sucesso!!!")
    
    except Exception as e:
        print('Erro', e)

        return gera_response(400, "emissao", {}, "Erro ao cadastrar!!!")

# Temperatura
@app.route("/temperatura", methods=["POST"])
def criar_temperatura():
    body = request.get_json()
    try:
        temperatura = Temperatura(
            id_pais = body["id_pais"],
            ano = body["ano"],
            indice = body["indice"]
        )

        mybd.session.add(temperatura)
        mybd.session.commit()

        return gera_response(201, "temperatura", temperatura.to_json(), "Criada com Sucesso!!!")
    
    except Exception as e:
        print('Erro', e)

        return gera_response(400, "temperatura", {}, "Erro ao cadastrar!!!")

#------------- PUTS -------------

# Pais
@app.route("/paises/<id>", methods=["PUT"])
def atualizar_pais(id):
    pais_objeto = Pais.query.filter_by(id=id).first()

    if(pais_objeto == None):
        return gera_response(404, "pais", {}, "País não encontrado!")

    body = request.get_json()

    try:
        if('nome' in body):
            pais_objeto.nome = body["nome"]
        if('sigla' in body):
            pais_objeto.sigla = body["sigla"]
        if('densidade' in body):
            pais_objeto.densidade = body["densidade"]
        if('area' in body):
            pais_objeto.area = body["area"]
        
        mybd.session.add(pais_objeto)
        mybd.session.commit()

        return gera_response(200, "pais", pais_objeto.to_json(), "Atualizado com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "pais", {}, "Erro ao atualizar")

# Mortes
@app.route("/mortes/<id>", methods=["PUT"])
def atualizar_mortes(id):
    mortes_objeto = Mortes.query.filter_by(id=id).first()

    if(mortes_objeto == None):
        return gera_response(404, "mortes", {}, "Mortes não encontrada!")

    body = request.get_json()

    try:
        if('id_pais' in body):
            mortes_objeto.id_pais = body["id_pais"]
        if('ano' in body):
            mortes_objeto.ano = body["ano"]
        if('quantidade' in body):
            mortes_objeto.quantidade = body["quantidade"]
        
        mybd.session.add(mortes_objeto)
        mybd.session.commit()

        return gera_response(200, "mortes", mortes_objeto.to_json(), "Atualizada com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "mortes", {}, "Erro ao atualizar")

# Emissão
@app.route("/emissao/<id>", methods=["PUT"])
def atualizar_emissao(id):
    emissao_objeto = Emissao.query.filter_by(id=id).first()

    if(emissao_objeto == None):
        return gera_response(404, "emissao", {}, "Emissão não encontrada!")

    body = request.get_json()

    try:
        if('id_pais' in body):
            emissao_objeto.id_pais = body["id_pais"]
        if('ano' in body):
            emissao_objeto.ano = body["ano"]
        if('total' in body):
            emissao_objeto.total = body["total"]
        if('carvao' in body):
            emissao_objeto.carvao = body["carvao"]
        if('petroleo' in body):
            emissao_objeto.petroleo = body["petroleo"]
        if('gas' in body):
            emissao_objeto.gas = body["gas"]
        if('cimento' in body):
            emissao_objeto.cimento = body["cimento"]
        if('queima' in body):
            emissao_objeto.queima = body["queima"]
        if('outros' in body):
            emissao_objeto.outros = body["outros"]
        
        mybd.session.add(emissao_objeto)
        mybd.session.commit()

        return gera_response(200, "emissao", emissao_objeto.to_json(), "Atualizada com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "emissao", {}, "Erro ao atualizar")

# Temperatura
@app.route("/temperatura/<id>", methods=["PUT"])
def atualizar_temperatura(id):
    temperatura_objeto = Temperatura.query.filter_by(id=id).first()

    if(temperatura_objeto == None):
        return gera_response(404, "temperatura", {}, "Emissão não encontrada!")

    body = request.get_json()

    try:
        if('id_pais' in body):
            temperatura_objeto.id_pais = body["id_pais"]
        if('ano' in body):
            temperatura_objeto.ano = body["ano"]
        if('indice' in body):
            temperatura_objeto.indice = body["indice"]
        
        mybd.session.add(temperatura_objeto)
        mybd.session.commit()

        return gera_response(200, "temperatura", temperatura_objeto.to_json(), "Atualizada com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "temperatura", {}, "Erro ao atualizar")
    
#------------- DELETES -------------

# Pais
@app.route("/paises/<id>", methods=["DELETE"])
def deletar_pais(id):
    pais_objeto = Pais.query.filter_by(id=id).first()

    if(pais_objeto == None):
        return gera_response(404, "pais", {}, "Pais não encontrado!")

    try:
        mybd.session.delete(pais_objeto)
        mybd.session.commit()

        return gera_response(200, "pais", {}, "Deletado com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "pais", {}, "Erro ao deletar")
    
# Mortes
@app.route("/mortes/<id>", methods=["DELETE"])
def deletar_mortes(id):
    mortes_objeto = Mortes.query.filter_by(id=id).first()

    if(mortes_objeto == None):
        return gera_response(404, "mortes", {}, "Mortes não encontradas!")

    try:
        mybd.session.delete(mortes_objeto)
        mybd.session.commit()

        return gera_response(200, "mortes", {}, "Deletada com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "mortes", {}, "Erro ao deletar")

# Emissão
@app.route("/emissao/<id>", methods=["DELETE"])
def deletar_emissao(id):
    emissao_objeto = Emissao.query.filter_by(id=id).first()

    if(emissao_objeto == None):
        return gera_response(404, "emissao", {}, "Emissão não encontrado!")

    try:
        mybd.session.delete(emissao_objeto)
        mybd.session.commit()

        return gera_response(200, "emissao", {}, "Deletada com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "emissao", {}, "Erro ao deletar")

# Temperatura
@app.route("/temperatura/<id>", methods=["DELETE"])
def deletar_temperatura(id):
    temperatura_objeto = Temperatura.query.filter_by(id=id).first()

    if(temperatura_objeto == None):
        return gera_response(404, "temperatura", {}, "Temperatura não encontrado!")

    try:
        mybd.session.delete(temperatura_objeto)
        mybd.session.commit()

        return gera_response(200, "temperatura", {}, "Deletada com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "temperatura", {}, "Erro ao deletar")

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

app.run(port=5500, host='localhost', debug=True)