from models.funcionario import SistemaFuncionarios
from Obras import SistemaObras
from historico_obras import HistoricoObras
from database import conectar

from menus.menus import (
    menu_principal,
    menu_funcionario,
    menu_obra,
    menu_historico_obras
)

sistema = SistemaFuncionarios()
sistema_obras = SistemaObras()
sistema_historico_obras = HistoricoObras()


while True:
    menu_principal()
    try:
        opcao_principal=int(input('escolha: '))

        if opcao_principal == 1:

            while True:
                menu_funcionario()
                try:
                    opcao_funcionario=int(input('escolha: '))
                except ValueError:
                    print('digite apenas numeros inteiros!')
                    continue

                if opcao_funcionario == 1:
                    if sistema.cadastrar_funcionario():
                        print('funcionario cadastrado com sucesso! ')
                elif opcao_funcionario == 2:

                    sistema.listar_funcionarios()

                elif opcao_funcionario == 3:

                    sistema.consultar_funcionario()

                elif opcao_funcionario == 4:

                    sistema.editar_funcionario()

                elif opcao_funcionario == 5:

                    sistema.desativar_funcionario()

                elif opcao_funcionario == 0:
                    print('encerrando o menu de funcionarios...')
                    break

                else:
                    print('opção invalida! ')


        elif opcao_principal == 2:


            while True:
                menu_obra()
                try:
                    opcao_obra = int(input('Escolha: '))
                except ValueError:
                    print('digite apenas numeros inteiros!')
                    continue

                if opcao_obra == 1:
                    sistema_obras.cadastrar_obra()

                elif opcao_obra == 2:
                    sistema_obras.listar_obras()

                elif opcao_obra == 3:
                    sistema_obras.consultar_obra()

                elif opcao_obra == 4:
                    sistema_obras.editar_obra()

                elif opcao_obra == 5:
                    sistema_obras.excluir_obra()

                elif opcao_obra == 6:
                    sistema_obras.encerrar_obra()

                elif opcao_obra == 0:
                    break

                else:
                    print('Opção inválida!')
        elif opcao_principal == 3:


            while True:
                menu_historico_obras()
                try:
                    opcao_historico = int(input('escolha: '))
                except ValueError:
                    print('digite apenas numeros inteiros!')
                    continue


                if opcao_historico == 1:
                    funcionario_id = sistema_historico_obras.selecionar_funcionarios()

                    if funcionario_id is not None:
                        sistema_historico_obras.vincular_funcionario_obra(funcionario_id)


                elif opcao_historico == 2:

                        sistema_historico_obras.consultar_historico_obras()



                elif opcao_historico == 3:
                    funcionario_id = sistema_historico_obras.selecionar_funcionarios()

                    if funcionario_id is not None:
                        sistema_historico_obras.alterar_obra_funcionario(funcionario_id)


                elif opcao_historico == 4:
                    funcionario_id = sistema_historico_obras.selecionar_funcionarios()

                    if funcionario_id is not None:
                        sistema_historico_obras.desvincular_funcionario_obra(funcionario_id)





                elif opcao_historico == 0:
                    print('voltando...')
                    break
                else:
                    print('opção invalida!')






        elif opcao_principal == 0:
            print('encerrando o sistema...')
            break

        else:
            print('opção invalida!')

    except ValueError as error:
       print(f'digite apenas numeros inteiros! {error}')
