#!/usr/bin/env python3
from ldap3 import Server, Connection, ALL

server = Server('ipa.demo1.freeipa.org', get_info=ALL)
conn = Connection(server, 'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', 'Secret123', auto_bind=True)
conn.search('dc=demo1,dc=freeipa,dc=org','(objectclass=person)', attributes=['sn', 'krbLastPwdChange', 'objectclass'])

print("*********************************************")
print(conn.entries)
print("------------")
print(server)
print("------------")
print(server.info)