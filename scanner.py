import socket, threading, sys

if len(sys.argv) > 1:
    alvo = sys.argv[1]
else:
    alvo = input("Qual alvo? (ex: scanme.nmap.org): ")

print(f"\n[+] Escaneando {alvo} - V5 BANNER GRABBER\n")

def scan(porta):
    s = socket.socket()
    s.settimeout(1.5)
    try:
        s.connect((alvo, porta))
        try:
            serv = socket.getservbyport(porta)
        except:
            serv = "desconhecido"
        
        # Tenta pegar a versão (banner)
        banner = ""
        try:
            if porta == 80 or porta == 8080:
                s.send(b"GET / HTTP/1.0\r\n\r\n")
            banner_data = s.recv(1024).decode(errors='ignore').strip()
            if banner_data:
                banner = banner_data.split('\n')[0][:80] # pega só a 1ª linha
        except:
            pass
        
        if banner:
            print(f"\033[92m[ABERTA] {porta:5} -> {serv:12} | {banner}\033[0m")
        else:
            print(f"\033[92m[ABERTA] {porta:5} -> {serv}\033[0m")
        s.close()
    except:
        pass

portas = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,1723,3306,3389,5432,5900,8080,8443]

threads = []
for p in portas:
    t = threading.Thread(target=scan, args=(p,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("\n[✓] V5 finalizada!")
