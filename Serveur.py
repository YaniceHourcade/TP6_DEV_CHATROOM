import socket

host = '10.10.10.11' 
port = 13337 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))  
    s.listen(1)
    print(f"Le serveur est prêt. En attente d'un client...")

    conn, addr = s.accept() 
    print(f"Un client vient de se connecter et son IP c'est {addr[0]}")

    while True:
        try:
            data = conn.recv(1024)  

            if not data: 
                break 

            message = data.decode('utf-8')  
            print(f"Données reçues du client : {message}")

            if "meo" in message:
                response = b"Meo a toi confrere."
            elif "waf" in message:
                response = b"ptdr t ki."
            elif "meo" not in message and "waf" not in message: 
                response = b"Mes respects humble humain."

            conn.sendall(response)

        except socket.error:
            print("Une erreur s'est produite.")
            break

except Exception as e:
    print(f"Erreur lors de la connexion : {e}")

finally:
    conn.close()
    s.close()