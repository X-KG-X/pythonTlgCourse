#!/usr/bin/env python3
from ldap3 import Server, Connection, ALL, NTLM

# server=Server('ipa.demo1.freeipa.org', get_info=ALL)
#conn = Connection( server, auto_bind=True)
#conn = Connection(server, user="Domain\\User", password="password", authentication=NTLM)
server = Server('ipa.demo1.freeipa.org', use_ssl=True, get_info=ALL)
conn = Connection(server, 'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', 'Secret123', auto_bind=True)
conn.extend.standard.who_am_i()
conn.start_tls()

print(conn)
print("------------")
print(server)
print("------------")
print(server.info)