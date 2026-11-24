from database import conectar

class Obra:
    def __init__(self,nome_obra):
        self.id = None
        self.nome_obra = nome_obra

class SistemaObras:
    def cadastrar_obra(self):
        conexao = None
        cursor = None
        try:
            conexao = conectar()
            cursor = conexao.cursor()

            nome_obra = (input('nome da obra: ')).strip()

            if nome_obra == '':
                print('o nome da obra é obrigatorio! ')
                return False

            sql1 = """
                           select * from obras
                           where LOWER(nome) = LOWER(%s)
                       """
            nome_obra = nome_obra.title()
            cursor.execute(sql1, (nome_obra,))

            resultado1 = cursor.fetchone()
            if resultado1:
                print('obra ja cadastrada!')
                return False

            sql = """insert into obras (nome )
                           values (%s)            
                       """

            cursor.execute(sql, (nome_obra,))
            id_obra = cursor.lastrowid
            conexao.commit()

            obra = Obra(nome_obra)
            obra.id = id_obra

            print(f'obra criada: id={obra.id} / nome={obra.nome_obra}')

            return True
        except Exception as erro:
            try:
                if conexao:
                    conexao.rollback()
            except Exception as erro_rollback:
                print(f'a conexao falhou {erro_rollback} ')
            print(f'erro {erro}')
            return False



        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()


    def listar_obras(self):
        conexao =None
        cursor=None
        try:
            conexao=conectar()
            cursor=conexao.cursor(dictionary = True)

            sql = 'select id,nome,status from obras '

            cursor.execute(sql)
            resultado = cursor.fetchall()

            if not resultado:
                print('nenhuma obra cadastrada! ')
                return False

            for obras in resultado:
                print(f"obra = {obras['nome']}")
                print(f"id = {obras['id']}")
                print(f"status = {obras['status']}")
                print('='*30)
            return True
        except Exception as erro:
            print(f'erro = {erro}')
            return False

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def consultar_obra(self):
        conexao=None
        cursor=None
        try:
            conexao=conectar()
            cursor=conexao.cursor(dictionary=True)

            obra_consulta = input('obra que deseja consultar: ').strip()

            if obra_consulta == '':
                print('é obrigatorio colocar o nome da obra para consultar')
                return False

            obra_consulta = obra_consulta.title()

            sql = """
                select id,nome,status from obras
                where LOWER(nome) = LOWER(%s)   
            """

            cursor.execute(sql,(obra_consulta,))

            resultado_obra = cursor.fetchone()

            if not resultado_obra:
                print('obra nao localizada! ')
                return False

            print(f"id = {resultado_obra['id']}")
            print(f"nome = {resultado_obra['nome']}")
            print(f"status = {resultado_obra['status']}")
            return True

        except Exception as erro:
            print(f'erro {erro}')
            return False

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def editar_obra(self):
        conexao=None
        cursor=None
        try:
            conexao=conectar()
            cursor=conexao.cursor(dictionary=True)
        #listar obra
            sql='select id, nome,status from obras'

            cursor.execute(sql)

            resultado_obra=cursor.fetchall()
            if not resultado_obra:
                print('nenhuma obra encontrada!')
                return False

            for obras in resultado_obra:
                print('=====================')
                print(f"id = {obras['id']}")
                print(f"nome = {obras['nome']}")
                print(f"status = {obras['status']}")
                print('=====================')

            try:
                escolha_id = int(input('escolha o ID da obra: '))

                sql3="""
                    select id,nome
                    from obras
                    where id = %s
                """

                cursor.execute(sql3,(escolha_id,))
                resultado=cursor.fetchone()

                if not resultado:
                    print('obra nao existe!')
                    return False


                novo_nome=input('novo nome: ').strip()

                if novo_nome == '':
                    print('é obrigatorio colocar o nome da obra!')
                    return False

                novo_nome = novo_nome.title()

                if novo_nome == resultado['nome']:
                    print('O nome informado é igual ao nome atual da obra.')
                    return False

                sql2="""
                     select id 
                     from obras
                     where LOWER(nome) = LOWER(%s)
                     and id != %s   
                """

                cursor.execute(sql2,(novo_nome,escolha_id))
                resultado_comp = cursor.fetchone()

                if resultado_comp:
                    print('foi localizada outra obra com esse nome!')
                    return False


                sql1="""
                    update obras
                    set nome = %s
                    where id= %s
                """


                cursor.execute(sql1,(novo_nome,escolha_id))
                if cursor.rowcount == 0:
                    print('nenhuma obra foi alterada!')
                    return False
                conexao.commit()

                print('nome da obra alterado com sucesso!')

                return True
            except ValueError:
                print(f'ID invalido!')
                return False


        except Exception as erro:
            if conexao:
                try:
                    conexao.rollback()
                except Exception as Erro_rollback:
                    print(f'conexao falhou! {Erro_rollback}')
            print(f'erro {erro}')
            return False

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def excluir_obra(self):
        conexao=None
        cursor=None
        try:
            conexao=conectar()
            cursor=conexao.cursor(dictionary = True)

            sql="select id, nome from obras "

            cursor.execute(sql)
            resultado1=cursor.fetchall()

            if resultado1:
                for lista in resultado1:
                    print(f"id = {lista['id']} / nome = {lista['nome']}")

            else:
                print('Nenhuma obra encontrada!')
                return False
            try:
                escolha_id = int(input('escolha ID:'))

                sql2="""select id,nome
                        from obras
                        where id = %s and status = 'ativa'
                        """
                cursor.execute(sql2,(escolha_id,))

                resultado2= cursor.fetchone()

                if not resultado2:
                    print('ID não localizado!')
                    return False

                confirmar_exclusao = str(input(f"Tem certeza de que deseja excluir esta obra '{resultado2['nome']}'? (S/Sim):")).strip().upper()

                if confirmar_exclusao in ('S','SIM'):

                    sql="""
                        SELECT id
                        FROM historico_obras
                        WHERE obra_id = %s
                        LIMIT 1;
                    """

                    cursor.execute(sql,(escolha_id,))
                    resultado=cursor.fetchone()

                    if resultado:
                        print('existe registros nessa obra, nao pode ser excluida!')
                        return False


                    sql3 = """
                            delete from obras
                            where id = %s and status = 'ativa'
                    """

                    cursor.execute(sql3,(escolha_id,))

                    if cursor.rowcount == 0:
                        print('A obra não foi excluída ')
                        return False

                    conexao.commit()

                    print('Obra excluída com sucesso! ')
                    return True
                else:
                    print('exclusao cancelada!')
                    return False
            except ValueError:
                print('	ID inválido!')
                return False

        except Exception as Erro:
            try:
                if conexao:
                    conexao.rollback()
            except Exception as Erro_rollback:
                print(f'conexao falhou! {Erro_rollback}')
            print(f'erro {Erro}')
            return False

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()
    def encerrar_obra(self):
        conexao=None
        cursor=None
        try:
            conexao=conectar()
            cursor=conexao.cursor(dictionary = True)

            sql1 = """
                select id,nome
                from obras
                where status = 'ativa'; 
            """

            cursor.execute(sql1)
            resultado1 = cursor.fetchall()

            if not resultado1:
                print('Nao existem obras ativas!')
                return False

            for obras in resultado1:
                print(f"id = {obras['id']}")
                print(f"nome = {obras['nome']}")


            try:

                escolha_id=int(input('escolha ID: '))

                confirmar_escolha=str(input('tem certeza que deseja encerrar essa obra [Sim/nao]')).upper().strip()
                if confirmar_escolha not in ('S','SIM'):
                    print('Operação cancelada!')
                    return False

                if not any(obra['id'] == escolha_id for obra in resultado1):
                    print('ID inválido!')
                    return False

                sql2= """
                    select funcionario_id
                    from historico_obras
                    where obra_id = %s
                    and data_fim IS NULL;
                """

                cursor.execute(sql2,(escolha_id,))

                resultado2=cursor.fetchone()

                if resultado2:
                    print('tem funcionarios ativos na obra! ')
                    return False

                sql3 = """
                    update obras
                    set status = %s
                    where id = %s AND status = 'ativa'

                """

                cursor.execute(sql3,('encerrada',escolha_id,))

                if cursor.rowcount > 0:
                    conexao.commit()
                    print('obra encerrada com sucesso!')

                else:
                    print('Nao foi possivel encerrar a obra!')
                    return False

            except ValueError:
                print('digite apenas numeros inteiros!')

        except Exception as Erro:
                if conexao:
                    try:
                        conexao.rollback()
                    except Exception as erro_rollback:
                        print(f'Erro no rollback: {erro_rollback}')

                print(f'erro ao encerrar a obra: {Erro}')
                return False

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()
































