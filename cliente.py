import socket

HOST = "127.0.0.1"  # endereço do servidor (localhost por enquanto)
PORT = 50000         # mesma porta que o servidor vai usar

def menu():
    print("\n=== CADASTRO DE NEOPETS ===")
    print("1 - Cadastrar Neopet (CREATE)")
    print("2 - Consultar Neopet (READ)")
    print("3 - Atualizar Neopet (UPDATE)")
    print("4 - Remover Neopet (DELETE)")
    print("5 - Sair")
    return input("Escolha uma opção: ")

def main():
    # cria o socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print("Conectado ao servidor.")

    while True:
        opcao = menu()

        if opcao == "1":
            nome = input("Nome: ")
            especie = input("Espécie: ")
            cor = input("Cor: ")
            nivel = input("Nível: ")
            forca = input("Força: ")
            idade = input("Idade: ")
            mensagem = f"CREATE|{nome}|{especie}|{cor}|{nivel}|{forca}|{idade}"

        elif opcao == "2":
            id_pet = input("ID do Neopet: ")
            mensagem = f"READ|{id_pet}"

        elif opcao == "3":
            id_pet = input("ID do Neopet a atualizar: ")
            nome = input("Nome: ")
            especie = input("Espécie: ")
            cor = input("Cor: ")
            nivel = input("Nível: ")
            forca = input("Força: ")
            idade = input("Idade: ")
            mensagem = f"UPDATE|{id_pet}|{nome}|{especie}|{cor}|{nivel}|{forca}|{idade}"

        elif opcao == "4":
            id_pet = input("ID do Neopet a remover: ")
            mensagem = f"DELETE|{id_pet}"

        elif opcao == "5":
            print("Encerrando conexão...")
            client_socket.sendall("EXIT".encode())
            break

        else:
            print("Opção inválida!")
            continue

        # envia mensagem para o servidor
        client_socket.sendall(mensagem.encode())

        # espera resposta do servidor
        resposta = client_socket.recv(1024).decode()
        print("\nResposta do servidor:", resposta)

    client_socket.close()

if __name__ == "__main__":
    main()
