from Crypto.Random.random import randrange
from pwn import *

# Connexion au serveur
conn = remote('challenges.france-cybersecurity-challenge.fr', 2151)

# Récupération des paramètres publics
print(conn.recvuntil(b'Public key:').decode())
print(conn.recvuntil(b'p = ').decode())
p = int(conn.recvline().strip().decode())
print(conn.recvuntil(b'g = ').decode())
g = int(conn.recvline().strip().decode())
print(conn.recvuntil(b'y = ').decode()) 
y = int(conn.recvline().strip().decode())

print(f"Paramètres publics reçus: p={p}, g={g}, y={y}")

# Forge de la signature 
a = randrange(p)
r = pow(g, a, p)
s = (-r) % (p-1)  
m_forge = (pow(y,a,p) * pow(r,s,p)) % p

print(f"Signature forgée calculée: a={a}, r={r}, s={s}, m_forge={m_forge}")

# Envoi des valeurs forgées au serveur
print(conn.recvuntil(b'Input a message.').decode())
print(f"Envoi de m_forge: {m_forge}")
conn.sendline(str(m_forge).encode())

print(conn.recvuntil(b'Input a signature. First, input r.').decode())  
print(f"Envoi de r: {r}")
conn.sendline(str(r).encode())

print(conn.recvuntil(b'Now, input s.').decode())
print(f"Envoi de s: {s}")
conn.sendline(str(s).encode())

# Affichage de la réponse du serveur
server_response = conn.recvall().decode()
print(f"Réponse du serveur: {server_response}")

conn.close()
