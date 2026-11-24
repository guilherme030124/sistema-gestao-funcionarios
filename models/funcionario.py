from database import conectar
from datetime import datetime



def validar_cpf(cpf):
    if cpf == '':
        print('cpf obrigatorio!')
        return False

    if not cpf.isdigit():
        print('CPF deve conter apenas números!')
        return False

    if len(cpf) != 11:
        print('CPF deve conter exatamente 11 digitos!')
        return False

    if cpf == cpf[0] * 11:
        print('CPF inválido! Não pode conter todos os números iguais.')
        return False

    numeros = cpf[:9]
    pesos = range(10, 1, -1)

    soma = 0

    for numero, peso in zip(numeros,pesos):
        soma += int(numero) * peso
    resto = soma % 11
    if resto < 2:
        digito = 0
    else:
        digito = 11 - resto

    if digito != int(cpf[9]):
        print('CPF inválido! Dígito verificador incorreto.')
        return False


    numeros = cpf[:10]
    pesos = range(11, 1, -1)
    soma = 0

    for numero, peso in zip(numeros, pesos):
        soma += int(numero) * peso

    resto = soma % 11
    if resto < 2:
        digito = 0
    else:
        digito = 11 - resto
    if digito != int(cpf[10]):
        print('CPF inválido! Dígito verificador incorreto.')
        return False

    return True




class Funcionario:
    def __init__(self,nome,cpf,funcao,funcao_id):
        self.id=None
        self.nome = nome
        self.cpf = cpf
        self.funcao = funcao
        self.funcao_id = funcao_id
        self.status = "ativo"


class SistemaFuncionarios:
    def __init__(self):
        pass

    def validar_nome(self, nome):
        if any(char.isdigit() for char in nome):
            print('o nome nao pode conter numeros!')
            return False

        if nome == '':
            print('nome obrigatorio! ')
            return False
        return True


    def cadastrar_funcionario(self):

        conexao = None
        cursor=None
#VALIDAR CPF
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)

            cpf = str(input('cpf: ')).strip()
            if not validar_cpf(cpf):
                return False



            sql_consulta="select cpf from funcionarios where cpf = %s"

            cursor.execute(sql_consulta,(cpf,))

            resultado=cursor.fetchone()

            if resultado:
                print('cpf ja registrado!')
                return False



            nome = str(input('nome: ')).strip()

            if not self.validar_nome(nome):
                return False




            hoje = datetime.today().date()
            data_admissao = input('Data de admissão (DD/MM/AAAA): ').strip()


            if data_admissao == '':
                raise ValueError('Data de admissão obrigatória!')

            data_formatada = datetime.strptime(data_admissao, "%d/%m/%Y").date()

            if data_formatada >hoje:
                print('Data de admissão não pode ser futura!')
                return False

            funcao = str(input('função: ')).strip()

            if funcao == '':
                print('é obrigatorio informar uma função! ')
                return False

            sql="""
                select id,nome
                from funcoes
                where nome = %s
            """

            cursor.execute(sql,(funcao,))

            resultado_funcao=cursor.fetchone()


            if not resultado_funcao:
                print('funcao nao encontrada! ')
                return False

            funcionario = Funcionario(nome,cpf,resultado_funcao['nome'],resultado_funcao['id'])




            sql="""insert into funcionarios(nome, cpf, data_admissao)
            values(%s,%s,%s)"""

            cursor.execute(sql, (funcionario.nome, funcionario.cpf, data_formatada))
            id_funcionario = cursor.lastrowid

            funcionario.id = id_funcionario
            print(f"Funcionário criado: {funcionario.nome} | ID: {funcionario.id} | Função: {funcionario.funcao}")

            sql = """   
                        insert into historico_funcoes(funcao_id,funcionario_id,data_inicio,data_fim)
                        values(%s,%s,%s,NULL)
                    """

            cursor.execute(sql, (funcionario.funcao_id, funcionario.id,data_formatada))

            conexao.commit()
        except ValueError as erro:
            print(f'erro: {erro} ')
            return False
        except Exception as erro:
            if conexao:
                try:
                    conexao.rollback()

                except Exception as Erro_rollback:
                    print(f'conexao falhou! {Erro_rollback}')
            print(f'erro ao cadastrar funcionario: {erro}')
            return False
        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()
        return True


    def listar_funcionarios(self):
        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)

            sql=""" select
                    func.id,
                    func.nome,
                    func.cpf,
                    func.status,
                    f.nome AS funcao_atual
                    from funcionarios func
                    join historico_funcoes hf on func.id = hf.funcionario_id
                    join funcoes f on hf.funcao_id = f.id
                    where func.status = 'ativo'
                    and hf.data_fim is null
            """

            cursor.execute(sql)
            resultado = cursor.fetchall()

            if not resultado:
                print('nenhum funcionario ativo registrado! ')
                return

            for funcionario in resultado:
                print('='.center(40, '-'))
                print(f"nome: {funcionario['nome']}")
                print(f"cpf: {funcionario['cpf']}")
                print(f"status: {funcionario['status']}")
                print(f"funcao: {funcionario['funcao_atual']}")

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()


    def consultar_funcionario(self):
        conexao = None
        cursor = None
        try:
            conexao=conectar()
            cursor=conexao.cursor(dictionary = True)
            consultar_cpf = (input('cpf que deseja consultar: ').strip())

            if not validar_cpf(consultar_cpf):
                return

            sql = """
                select
                    func.cpf,
                    func.status,
                    func.nome,
                    f.nome AS funcao_atual
                from funcionarios func
                left join historico_funcoes hf
                    on hf.funcionario_id = func.id
                    and hf.data_fim IS NULL
                left join funcoes f 
                    on f.id = hf.funcao_id
                where func.cpf = %s 
                """

            cursor.execute(sql,(consultar_cpf,))

            resultado=cursor.fetchone()

            if resultado:

                print("=".center(40, '='))
                print(f"nome = {resultado['nome']}")
                print(f"cpf = {resultado['cpf']}")
                print(f"status = {resultado['status']}")
                print(f"função = {resultado['funcao_atual']}")

            else:
                print('cpf nao encontrado! ')

        except Exception as erro:
            print(f"Erro ao consultar funcionário: {erro}")

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()


    def editar_funcionario(self):
        conexao = None
        cursor = None
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            editar_cpf = input('cpf do funcionario que deseja editar: ').strip()

            if not validar_cpf(editar_cpf):
                return



            sql =""" select id, cpf, status,nome
                  from funcionarios
                  where cpf = %s and status = 'ativo' """

            cursor.execute(sql,(editar_cpf,))

            resultado = cursor.fetchone()

            if not resultado:
                print('cpf nao localizado! ')
                return




            sql="""
                select 
                    f.nome AS funcao_atual,
                    h.data_inicio
                from historico_funcoes h
                join funcoes f on f.id = h.funcao_id
                WHERE h.funcionario_id = %s
                AND h.data_fim IS NULL
            """

            cursor.execute(sql,(resultado['id'],))

            funcao_atual=cursor.fetchone()



            print(f"nome: {resultado['nome']}")
            print(f"cpf = {resultado['cpf']}")
            print(f"status = {resultado['status']}")


            if funcao_atual:
                print(f"função = {funcao_atual['funcao_atual']}")
                print('=' * 30)
            else:
                print('nenhuma funcao atual registrada!')



            print('menu edição:\n'
                  '1-editar nome:\n'
                  '2-editar funcao\n'
                  '0-sair\n'
                  + '=' * 30)


            try:
                escolha_edicao = int(input('escolha: '))


                if escolha_edicao == 1:
                    novo_nome = input('nome: ').strip()

                    if novo_nome == '':
                        print('nome obrigatorio!')
                        return

                    elif any(char.isdigit() for char in novo_nome):
                        print('o nome nao pode conter numeros!')
                        return

                    elif novo_nome == resultado['nome']:
                        print('o funcionario ja possui esse nome!')
                        return

                    else:

                        sql="""update funcionarios
                                set nome = %s
                                where cpf = %s
                            """


                        cursor.execute(sql,(novo_nome,editar_cpf,))


                        if cursor.rowcount:
                            conexao.commit()
                            print('nome alterado com sucesso! ')
                            resultado['nome'] = novo_nome

                        else:
                            print('dados nao alterados! ')








                elif escolha_edicao == 2:

                    # 1. Consultar a função atual do funcionário

                    sql = """
    
                        SELECT
                            f.nome AS funcao_atual,
                            h.data_inicio
                        FROM historico_funcoes h
                        JOIN funcoes f ON f.id = h.funcao_id
                        WHERE h.funcionario_id = %s
                          AND h.data_fim IS NULL
                    """

                    cursor.execute(sql, (resultado['id'],))

                    funcao_atual = cursor.fetchone()

                    if funcao_atual:

                        print(f"\nFunção atual: {funcao_atual['funcao_atual']}")

                        print(f"Desde: {funcao_atual['data_inicio']}")

                    else:

                        print("Funcionário não possui função atual registrada.")

                    # 2. Listar as funções disponíveis

                    sql = """
    
                        SELECT id, nome
    
                        FROM funcoes
    
                        ORDER BY id
    
                    """

                    cursor.execute(sql)

                    funcoes = cursor.fetchall()

                    print("\n--- FUNÇÕES DISPONÍVEIS ---")

                    for funcao in funcoes:
                        print(f"{funcao['id']} - {funcao['nome']}")

                    # 3. Solicitar a nova função

                    try:

                        escolha_id = int(input("\nDigite o ID da nova função: "))

                    except ValueError:

                        print("Digite um ID numérico válido.")

                    else:

                        ids_funcoes = [funcao['id'] for funcao in funcoes]

                        if escolha_id not in ids_funcoes:

                            print("ID de função inválido.")


                        elif (

                                funcao_atual

                                and next(

                            f['nome'] for f in funcoes

                            if f['id'] == escolha_id

                        ) == funcao_atual['funcao_atual']

                        ):

                            print("O funcionário já exerce essa função.")


                        else:

                            try:

                                # 4. Encerrar o histórico da função anterior

                                if funcao_atual:
                                    sql = """
    
                                        UPDATE historico_funcoes
    
                                        SET data_fim = CURDATE()
    
                                        WHERE funcionario_id = %s
    
                                          AND data_fim IS NULL
    
                                    """

                                    cursor.execute(sql, (resultado['id'],))

                                # 5. Registrar a nova função no histórico

                                sql = """
    
                                    INSERT INTO historico_funcoes
    
                                        (funcionario_id, funcao_id, data_inicio, data_fim)
    
                                    VALUES (%s, %s, CURDATE(), NULL)
    
                                """

                                cursor.execute(

                                    sql,

                                    (resultado['id'], escolha_id)

                                )

                                conexao.commit()

                                print("Função do funcionário atualizada com sucesso!")


                            except Exception as erro:
                                if conexao:
                                    conexao.rollback()

                                print(f"Erro ao atualizar a função: {erro}")

                elif escolha_edicao == 0:

                    print('voltando ao menu principal...')
                    return

                else:
                    print('opção invalida! ')

            except ValueError:
                print('Digite apenas numeros inteiros! ')

            except Exception as erro:
                if conexao:
                    conexao.rollback()
                print(f'erro ao editar funcionarios {erro}')



        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()




    def desativar_funcionario(self):
        conexao=None
        cursor=None
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)

            desativar_cpf = input('digite o cpf: ').strip()

            if not validar_cpf(desativar_cpf):
                return

            sql = ' select * from funcionarios where cpf = %s '

            cursor.execute(sql,(desativar_cpf,))

            resultado = cursor.fetchone()


            if resultado:
                if resultado['status'] == 'inativo':
                    print('colaborador inativo!')
                    return

                sql2 = """
                            select
                                f.nome AS funcao_atual,
                                h.data_inicio
                            from historico_funcoes h
                            join funcoes f on f.id = h.funcao_id
                            where h.funcionario_id = %s 
                            and h.data_fim is null;
    
                            """
                cursor.execute(sql2, (resultado['id'],))

                funcao = cursor.fetchone()


                print(f"nome: {resultado['nome']}")
                print(f"cpf: {resultado['cpf']}")
                print(f"status: {resultado['status']}")
                if funcao:
                    print(f"funcao: {funcao['funcao_atual']}")
                else:
                    print("Nenhuma função ativa encontrada.")



                confirmar = input('tem certeza que deseja desligar esse colaborador? [S/SIM]').strip().upper()

                if confirmar in ('S', 'SIM'):

                    sql = """
                        update funcionarios
                        set status = 'inativo'
                        where cpf = %s
                    """

                    cursor.execute(sql,(desativar_cpf,))

                    if cursor.rowcount == 0:
                        print('funcionario nao foi atualizado! ')
                        return

                    print(f'colaborador {resultado["nome"]} inativado com sucesso! ')

                    sql1="""
                        update historico_funcoes
                        set data_fim = CURDATE()
                        where funcionario_id = %s
                        and data_fim is null
                    
                    """

                    cursor.execute(sql1,(resultado['id'],))
                    conexao.commit()

                else:
                    print('atualização cancelado com sucesso! ')
            else:
                print('cpf nao localizado! ')

        except Exception as erro:
            if conexao:
                conexao.rollback()
            print(f"Erro ao desligar funcionário: {erro}")
        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()








