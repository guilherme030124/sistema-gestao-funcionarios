from database import conectar
from mysql.connector import IntegrityError

class HistoricoObras:
    def selecionar_funcionarios(self):
        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)

            sql = """
                SELECT id, nome, cpf
                FROM funcionarios;
            """

            cursor.execute(sql)
            resultado = cursor.fetchall()

            if not resultado:
                print('Nenhum funcionário encontrado!')
                return None

            for funcionario in resultado:
                print(f"ID = {funcionario['id']}")
                print(f"Nome = {funcionario['nome']}")
                print(f"CPF = {funcionario['cpf']}")
                print('=' * 30)

            try:
                funcionario_id = int(input('Digite o ID do funcionário: '))

                if not any(dados['id'] == funcionario_id for dados in resultado):
                    print('ID inválido!')
                    return None

                return funcionario_id

            except ValueError:
                print('Digite apenas números inteiros!')
                return None

        except Exception as erro:
            print(f'Erro = {erro}')
            return None

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def vincular_funcionario_obra(self,funcionario_id):
        conexao = None
        cursor=None
        try:
            conexao=conectar()
            cursor=conexao.cursor(dictionary = True)

            sql1 = """
                    SELECT id
                    FROM funcionarios
                    WHERE id = %s;
                 """

            cursor.execute(sql1,(funcionario_id,))
            resultado2 = cursor.fetchone()

            if not resultado2:
                print('Funcionário não encontrado!')
                return False

            sql2="""SELECT
            id, obra_id
            FROM historico_obras
            WHERE funcionario_id = %s
            AND data_fim IS NULL;
            """

            cursor.execute(sql2,(funcionario_id,))
            resultado=cursor.fetchone()

            if resultado:
                print('Funcionário já está vinculado a uma obra')
                return False
            else:
                print('Funcionário disponível para vinculação!')


            sql3="""
                    select id,nome
                    from obras
                    where status = 'ativa'
                    order by nome;
            """

            cursor.execute(sql3)
            resultado3=cursor.fetchall()

            if resultado3:
                for obra in resultado3:
                    print(f"id = {obra['id']} / nome = {obra['nome']}")

            else:
                print('Nenhuma obra localizada!')
                return False
            try:
                escolha_id=int(input('Digite o ID da obra: '))

                if escolha_id <=0:
                    print('digite apenas numeros positivos')
                    return False

                sql4="""
                    select id
                    from obras
                    where id = %s and status = 'ativa'
                """
                cursor.execute(sql4,(escolha_id,))

                resultado4=cursor.fetchone()

                if resultado4:
                    print('Obra localizada!')
                else:
                    print('Obra não encontrada!')
                    return False

                sql5="""INSERT INTO historico_obras
                (funcionario_id, obra_id, data_inicio)
                VALUES( %s, %s, CURDATE());
                """

                cursor.execute(sql5,(funcionario_id,escolha_id))
                conexao.commit()
                print('funcionario vinculado a obra com sucesso!')
                return True

            except ValueError:
                print('Digite apenas números inteiros!')
                return False
        except IntegrityError as Erro:
            if conexao:
                conexao.rollback()

            if Erro.errno == 1062:
                print('Funcionário já possui vínculo ativo!')
            else:
                print(f'Erro de integridade: {Erro}')
            return False

        except Exception as erro:
            if conexao:
                conexao.rollback()

            print(f'Erro: {erro}')
            return False

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def consultar_historico_obras(self):
        conexao = None
        cursor = None
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary = True)


            consulta=input('Digite o cpf do colaborador: ').strip()


            if consulta == '':
                print('obrigatorio inserir o cpf!')
                return False
            if not consulta.isdigit():
                print('digite apenas numeros inteiros!')
                return False

            if len(consulta) != 11:
                print('CPF deve conter exatamente 11 digitos!')
                return False



            sql1="""
                select 
                    f.nome AS nome_funcionario,
                    f.cpf,
                    o.nome AS nome_obra,
                    ho.data_inicio,
                    ho.data_fim, 
                    CASE
                        WHEN ho.data_fim IS NULL THEN 'em andamento'
                        ELSE 'Encerrado'
                    END AS situacao
                from historico_obras ho
                inner join funcionarios f
                    on ho.funcionario_id = f.id
                inner join obras o
                    on ho.obra_id = o.id
                where f.cpf = %s
            """

            cursor.execute(sql1,(consulta,))

            resultado1=cursor.fetchall()

            if resultado1:
                for lista in resultado1:
                    print('LISTANDO...')
                    print(f"Nome = {lista['nome_funcionario']}")
                    print(f"Obra = {lista['nome_obra']}")
                    print(f"Data inicio = {lista['data_inicio']}")
                    print(f"Data fim = {lista['data_fim']}")
                    print(f"Situação = {lista['situacao']}")
                    print('='*30)
                return True
            else:
                print('Nenhum resultado encontrado!')
            return False

        except Exception as erro:
            print(f'erro ao consultar historico: {erro}')
            return False


        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def alterar_obra_funcionario(self,funcionario_id):
        conexao=None
        cursor=None
        try:
            conexao=conectar()
            cursor=conexao.cursor(dictionary = True)

            sql="""
                select id,nome
                from funcionarios
                where id = %s;
            """

            cursor.execute(sql,(funcionario_id,))
            resultado1=cursor.fetchone()

            if not resultado1:
                print('resultado nao encontrado!')
                return False

            sql2="""SELECT
                       ho.id,
                       o.nome AS nome_obra,
                       o.id AS obras_id
                   from historico_obras ho
                   inner join obras o 
                       on ho.obra_id = o.id
                   where ho.funcionario_id = %s
                   and ho.data_fim is NULL;
                  
                    """

            cursor.execute(sql2,(funcionario_id,))
            resultado2=cursor.fetchall()

            if len(resultado2) == 0:
                print('Funcionário sem vínculo ativo!')
                return False

            if len(resultado2) > 1:
                print('Erro: funcionário possui múltiplos vínculos ativos!')
                return False

            print(f"O funcionario = {resultado1['nome']} está vinculado a obra = {resultado2[0]['nome_obra']} ")



            alterar_obra=input('tem certeza que deseja alterar o colaborador de obra: [sim/S]').strip().upper()
            if alterar_obra not in ( 'SIM', 'S'):
                print('operação cancelada!')
                return False
            sqlo = """
                      select id,nome
                      from obras
                      where status = 'ativa' ;
                  """
            cursor.execute(sqlo)

            resultado_obras = cursor.fetchall()

            if not resultado_obras:
                print('lista vazia!')
                return False
            for obras in resultado_obras:
                print(f"id {obras['id']} // nome {obras['nome']} ")
            try:
                escolha_id_obra = int(input('escolha o ID: '))

                if escolha_id_obra <=0:
                    print('digite apenas numeros positivos')
                    return False

            except ValueError:
                print('Digite apenas numeros inteiros!')
                return False

            sqlid = """
                     select id 
                     from obras
                     where id = %s and status = 'ativa';
                       """
            cursor.execute(sqlid, (escolha_id_obra,))
            resultadoid = cursor.fetchone()

            if not resultadoid:
                print('Obra nao encontrada ou encerrada!')
                return False

            if resultado2[0]['obras_id'] == escolha_id_obra:
                print('alteração nao permitida, obra selecionada igual a anterior!')
                return False

            sqlu = """
                        update historico_obras
                        set data_fim = CURDATE()
                        where id =%s
                        and data_fim IS NULL
                      """
            cursor.execute(sqlu, (resultado2[0]['id'],))

            if cursor.rowcount != 1:
                raise Exception ('nao foi possivel encerrar o vinculo anterior!')

            sqli = """
                           insert into historico_obras
                           (funcionario_id,obra_id,data_inicio)
                           values(%s,%s,curdate());
                       """

            cursor.execute(sqli, (funcionario_id, escolha_id_obra,))


            conexao.commit()

            print('obra do funcionario alterada com sucesso!')

            return True
        except IntegrityError as Erro:
            if conexao:
                conexao.rollback()

            if Erro.errno == 1062:
                print('Funcionário já possui vínculo ativo!')
            else:
                print(f'Erro de integridade: {Erro}')
            return False


        except Exception as Erro:
                if conexao:
                    conexao.rollback()

                print(f'erro ao alterar obra: {Erro}')
                return False


        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()


    def desvincular_funcionario_obra(self,funcionario_id):
        conexao=None
        cursor=None
        try:
            conexao=conectar()
            cursor=conexao.cursor(dictionary = True)

            sql="""
                select id 
                from funcionarios
                where id = %s;
            """
            cursor.execute(sql,(funcionario_id,))
            resultado_existe=cursor.fetchone()

            if not resultado_existe:
                print('ID nao localizado!')
                return False

            sql1="""
                select 
                    ho.id,  
                    o.nome as nome_obra
                from historico_obras ho
                join obras o
                    on ho.obra_id = o.id
                where ho.funcionario_id = %s
                and ho.data_fim IS NULL;
            """

            cursor.execute(sql1,(funcionario_id,))
            resultado1=cursor.fetchone()

            if not resultado1:
                print('Nenhum vínculo ativo encontrado para este funcionário!')
                return False

            print(f"nome = {resultado1['nome_obra']}")

            confirmar=input('tem certeza que deseja disvicular? [S/SIM]').strip().upper()

            if confirmar not in ('S', 'SIM'):
                print('Operação cancelada!')
                return False

            sql2="""
                update historico_obras
                set data_fim = CURDATE()
                where id = %s
                and data_fim IS NULL
                
            """

            cursor.execute(sql2,(resultado1['id'],))
            if cursor.rowcount != 1:
                raise Exception('erro ao atualizar vinculo!')

            conexao.commit()

            print('Funcionário desvinculado com sucesso!')

            return True

        except Exception as Erro:
            if conexao:
                conexao.rollback()
            print(f'erro {Erro}')
            return False

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()
