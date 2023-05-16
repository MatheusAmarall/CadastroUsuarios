from PySide6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox,\
    QSizePolicy, QComboBox, QTableWidget, QAbstractItemView, QTableWidgetItem
import requests
from infra.entities.cliente import Cliente
from infra.repository.cliente_repository import ClienteRepository
from infra.configs.connection import DBConnectionHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        conn = DBConnectionHandler()

        self.setWindowTitle('Cadastro de clientes')
        self.setMinimumSize(500, 900)

        self.lbl_cpf = QLabel('CPF', self)
        self.txt_cpf = QLineEdit(self)
        self.txt_cpf.setInputMask('000.000.000-00')
        self.lbl_nome = QLabel('Nome', self)
        self.txt_nome = QLineEdit(self)
        self.lbl_telefone_fixo = QLabel('Telefone Fixo', self)
        self.txt_telefone_fixo = QLineEdit(self)
        self.txt_telefone_fixo.setInputMask('(00)0000-0000')
        self.lbl_telefone_celular = QLabel('Telefone Celular', self)
        self.txt_telefone_celular = QLineEdit(self)
        self.txt_telefone_celular.setInputMask('(00)00000-0000')
        self.lbl_sexo = QLabel('Sexo', self)
        self.cb_sexo = QComboBox()
        self.cb_sexo.addItems(['Não informado', 'Masculino', 'Feminino'])
        self.lbl_cep = QLabel('CEP', self)
        self.txt_cep = QLineEdit(self)
        self.txt_cep.setInputMask('00.000-000')
        self.lbl_logradouro = QLabel('Rua', self)
        self.txt_logradouro = QLineEdit(self)
        self.lbl_numero = QLabel('Número', self)
        self.txt_numero = QLineEdit(self)
        self.lbl_complemento = QLabel('Complemento', self)
        self.txt_complemento = QLineEdit(self)
        self.lbl_bairro = QLabel('Bairro', self)
        self.txt_bairro = QLineEdit(self)
        self.lbl_municipio = QLabel('Município', self)
        self.txt_municipio = QLineEdit(self)
        self.lbl_estado = QLabel('Estado', self)
        self.txt_estado = QLineEdit(self)
        self.btn_salvar = QPushButton('Salvar')
        self.btn_limpar = QPushButton('Limpar')
        self.btn_remover = QPushButton('Remover')
        self.tabela_clientes = QTableWidget()

        self.tabela_clientes.setColumnCount(12)
        self.tabela_clientes.setHorizontalHeaderLabels(['CPF', 'Nome', 'Telefone Fixo', 'Telefone Celular', 'Sexo',
                                                        'Cep', 'Logradouro', 'Número', 'Complemento', 'Bairro',
                                                        'Município', 'Estado'])

        self.tabela_clientes.setSelectionMode(QAbstractItemView.NoSelection)
        self.tabela_clientes.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_cpf)
        layout.addWidget(self.txt_cpf)
        layout.addWidget(self.lbl_nome)
        layout.addWidget(self.txt_nome)
        layout.addWidget(self.lbl_telefone_fixo)
        layout.addWidget(self.txt_telefone_fixo)
        layout.addWidget(self.lbl_telefone_celular)
        layout.addWidget(self.txt_telefone_celular)
        layout.addWidget(self.lbl_sexo)
        layout.addWidget(self.cb_sexo)
        layout.addWidget(self.lbl_cep)
        layout.addWidget(self.txt_cep)
        layout.addWidget(self.lbl_logradouro)
        layout.addWidget(self.txt_logradouro)
        layout.addWidget(self.lbl_numero)
        layout.addWidget(self.txt_numero)
        layout.addWidget(self.lbl_complemento)
        layout.addWidget(self.txt_complemento)
        layout.addWidget(self.lbl_bairro)
        layout.addWidget(self.txt_bairro)
        layout.addWidget(self.lbl_municipio)
        layout.addWidget(self.txt_municipio)
        layout.addWidget(self.lbl_estado)
        layout.addWidget(self.txt_estado)
        layout.addWidget(self.tabela_clientes)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_limpar)
        layout.addWidget(self.btn_remover)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.btn_remover.setVisible(False)
        self.btn_remover.clicked.connect(self.deletar_cliente)
        self.btn_salvar.clicked.connect(self.salvar_cliente)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.txt_cpf.editingFinished.connect(self.consulta_cliente)
        self.txt_cep.editingFinished.connect(self.consulta_endereco)

        self.tabela_clientes.cellDoubleClicked.connect(self.carrega_dados)
        self.popula_tabela_clientes()


    def salvar_cliente(self):
        db = ClienteRepository()

        cliente = Cliente(
            cpf=self.txt_cpf.text().replace("-", "").replace(".", ""),
            nome=self.txt_nome.text(),
            telefone_fixo=self.txt_telefone_fixo.text(),
            telefone_celular=self.txt_telefone_celular.text(),
            sexo=self.cb_sexo.currentText(),
            cep=self.txt_cep.text(),
            logradouro=self.txt_logradouro.text(),
            numero=self.txt_numero.text(),
            complemento=self.txt_complemento.text(),
            bairro=self.txt_bairro.text(),
            municipio=self.txt_municipio.text(),
            estado=self.txt_estado.text()
        )

        if self.btn_salvar.text() == 'Salvar':
            retorno = db.insert(cliente)
            if retorno == 'OK':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Cadastro realizado')
                msg.setText('Cadastro realizado com sucesso')
                msg.exec()

                self.limpar_campos()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao cadastrar')
                msg.setText(f'Erro ao cadastrar o cliente, verifique os dados')
                msg.exec()
        elif self.btn_salvar.text() == 'Atualizar':
            retorno = db.update(cliente)

            if retorno == 'OK':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Atualizar')
                msg.setText('Usuario editado com sucesso')
                msg.exec()

                self.limpar_campos()

        self.popula_tabela_clientes()

    def consulta_cliente(self):
        if self.txt_cpf.text().replace('.', '').replace('-', '') != '':
            db = ClienteRepository()
            retorno = db.select(str(self.txt_cpf.text()).replace('.', '').replace('-', ''))

            if retorno is not None:
                self.btn_salvar.setText('Atualizar')
                msg = QMessageBox()
                msg.setWindowTitle('Cliente já cadastrado')
                msg.setText(f'O CPF {self.txt_cpf.text()} já está cadastrado')
                msg.exec()
                self.txt_nome.setText(retorno.nome)
                self.txt_telefone_fixo.setText(retorno.telefone_fixo)
                self.txt_telefone_celular.setText(retorno.telefone_celular)
                sexo_map = {'Não informado': 0, 'Masculino': 1, 'Feminino': 2}
                self.cb_sexo.setCurrentIndex(sexo_map.get(retorno.sexo, 0))
                self.txt_cep.setText(retorno.cep)
                self.txt_logradouro.setText(retorno.logradouro)
                self.txt_numero.setText(retorno.numero)
                self.txt_complemento.setText(retorno.complemento)
                self.txt_bairro.setText(retorno.bairro)
                self.txt_municipio.setText(retorno.municipio)
                self.txt_estado.setText(retorno.estado)
                self.btn_remover.setVisible(True)

    def deletar_cliente(self):
        db = ClienteRepository()
        retorno = db.delete(self.txt_cpf.text().replace('.', '').replace('-', ''))

        if retorno == 'OK':
            msg = QMessageBox()
            msg.setWindowTitle('Remover cliente')
            msg.setText(f'O CPF {self.txt_cpf.text()} foi deletado')
            msg.exec()

            self.limpar_campos()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Remover cliente')
            msg.setText('Erro ao remover cliente')
            msg.exec()

        self.txt_cpf.setReadOnly(False)
        self.popula_tabela_clientes()

    def limpar_campos(self):
        for widget in self.container.children():
            if isinstance(widget, QLineEdit):
                widget.setText("")
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)

        self.btn_salvar.setText('Salvar')
        self.btn_remover.setVisible(False)
        self.txt_cpf.setReadOnly(False)

    def consulta_endereco(self):
        url = f"https://viacep.com.br/ws/{str(self.txt_cep.text()).replace('.', '').replace('-', '')}/json/"

        response = requests.get(url)
        if response.status_code == 200:
            endereco = response.json()
            self.txt_logradouro.setText(f"{endereco['logradouro']}")
            self.txt_bairro.setText(f"{endereco['bairro']}")
            self.txt_municipio.setText(f"{endereco['localidade']}")
            self.txt_estado.setText(f"{endereco['uf']}")
        else:
            msg = QMessageBox()
            msg.setInformativeText('Cep inválido ou não encontrado')
            msg.exec()

    def popula_tabela_clientes(self):
        self.tabela_clientes.setRowCount(0)
        db = ClienteRepository()
        lista_clientes = db.select_all()
        self.tabela_clientes.setRowCount(len(lista_clientes))

        for linha, cliente in enumerate(lista_clientes):
            valores_cliente = [cliente.cpf, cliente.nome, cliente.telefone_fixo, cliente.telefone_celular, cliente.sexo, cliente.cep, cliente.logradouro, cliente.numero, cliente.complemento, cliente.bairro, cliente.municipio, cliente.estado]
            for coluna, valor in enumerate(valores_cliente):
                self.tabela_clientes.setItem(linha, coluna, QTableWidgetItem(str(valor)))

    def carrega_dados(self, row, column):
        self.txt_cpf.setText(self.tabela_clientes.item(row, 0).text())
        self.txt_nome.setText(self.tabela_clientes.item(row, 1).text())
        self.txt_telefone_fixo.setText(self.tabela_clientes.item(row, 2).text())
        self.txt_telefone_celular.setText(self.tabela_clientes.item(row, 3).text())
        sexo_map = {'Não informado': 0, 'Masculino': 1, 'Feminino': 2}
        self.cb_sexo.setCurrentIndex(sexo_map.get(self.tabela_clientes.item(row, 4).text(), 0))
        self.txt_cep.setText(self.tabela_clientes.item(row, 5).text())
        self.txt_logradouro.setText(self.tabela_clientes.item(row, 6).text())
        self.txt_numero.setText(self.tabela_clientes.item(row, 7).text())
        self.txt_complemento.setText(self.tabela_clientes.item(row, 8).text())
        self.txt_bairro.setText(self.tabela_clientes.item(row, 9).text())
        self.txt_municipio.setText(self.tabela_clientes.item(row, 10).text())
        self.txt_estado.setText(self.tabela_clientes.item(row, 11).text())
        self.btn_salvar.setText('Atualizar')
        self.txt_cpf.setReadOnly(True)
        self.btn_remover.setVisible(True)


