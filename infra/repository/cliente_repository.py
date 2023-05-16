from infra.configs.connection import DBConnectionHandler
from infra.entities.cliente import Cliente

class ClienteRepository:
    def select_all(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Cliente).all()
            return data

    def select(self, cpf):
        with DBConnectionHandler() as db:
            data = db.session.query(Cliente).filter(Cliente.cpf == cpf).first()
            return data

    def insert(self, cliente):
        with DBConnectionHandler() as db:
            try:
                db.session.add(cliente)
                db.session.commit()
                return "OK"
            except Exception as e:
                db.session.rollback()
                return e

    def delete(self, cpf):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Cliente).filter(Cliente.cpf == cpf).delete()
                db.session.commit()
                return "OK"
            except Exception as e:
                db.session.rollback()
                return e

    def update(self, cliente=Cliente):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Cliente).filter(Cliente.cpf == cliente.cpf).update({'nome' : cliente.nome, 'telefone_fixo' : cliente.telefone_fixo, 'telefone_celular' : cliente.telefone_celular,
                                                                           'sexo' : cliente.sexo, 'cep' : cliente.cep, 'logradouro' : cliente.logradouro, 'numero' : cliente.numero,
                                                                           'complemento' : cliente.complemento, 'bairro' : cliente.bairro, 'municipio' : cliente.municipio,
                                                                           'estado' : cliente.estado})
                db.session.commit()
                return "OK"
            except Exception as e:
                db.session.rollback()
                return e

