import socket
import sqlite3

HOST = "127.0.0.1"
PORT = 50000

# ===== BANCO DE DADOS =====
def criar_banco():
    conn = sqlite3.connect("neopets.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS neopets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        especie TEXT NOT NULL,
        cor TEXT NOT NULL,
        nivel INTEGER NOT NULL,
        forca INTEGER NOT NULL,
        idade INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# CREATE
def create_neopet(nome, especie, cor, nivel, forca, idade):
    conn = sqlite3.connect("neopets.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO neopets (nome, especie, cor, nivel, forca, idade) VALUES (?, ?, ?, ?, ?, ?)",
                   (nome, especie, cor, int(nivel), int(forca), int(idade)))
    conn.commit()
    conn.close()
    return "Neopet cadastrado com sucesso!"

# READ
def read_neopet(id_pet):
    conn = sqlite3.connect("neopets.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM neopets WHERE id=?", (id_pet,))
    pet = cursor.fetchone()
    conn.close()
    if pet:
        return f"ID: {pet[0]} | Nome: {pet[1]} | Espécie: {pet[2]} | Cor: {pet[3]} | Nível: {pet[4]} | Força: {pet[5]} | Idade: {pet[6]}"
    else:
        return "Neopet não encontrado."

# UPDATE
def update_neopet(id_pet, nome, especie, cor, nivel, forca, idade):
    conn = sqlite3.connect("neopets.db")
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE neopets
    SET nome=?, especie=?, cor=?, nivel=?, forca=?, idade=?
    WHERE id=?
    """, (nome, especie, cor, int(nivel), int(forca), int(idade), id_pet))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return "Neopet atualizado com sucesso!" if updated else "Neopet não encontrado."

# DELETE
def delete_neopet(id_pet):
    conn = sqlite3.connect("neopets.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM neopets WHERE id=?", (id_pet,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return "Neopet removido com sucesso!" if deleted else "Neopet não encontrado."

# ===== SERVIDOR SOCKET =====
def main():
    criar_banco()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Servidor rodando em {HOST}:{PORT}...")

    conn, addr = server_socket.accept()
    print("Cliente conectado:", addr)

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        if data == "EXIT":
            print("Cliente encerrou a conexão.")
            break

        partes = data.split("|")
        comando = partes[0].upper()

        if comando == "CREATE":
            resposta = create_neopet(*partes[1:])
        elif comando == "READ":
            resposta = read_neopet(partes[1])
        elif comando == "UPDATE":
            resposta = update_neopet(*partes[1:])
        elif comando == "DELETE":
            resposta = delete_neopet(partes[1])
        else:
            resposta = "Comando inválido."

        conn.sendall(resposta.encode())

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    main()
