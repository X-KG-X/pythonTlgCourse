#!/usr/bin/env python3
from ldap3 import Server, Connection, ALL

server = Server('ipa.demo1.freeipa.org', get_info=ALL)
conn = Connection(server, 'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', 'Secret123', auto_bind=True)
conn.search('dc=demo1,dc=freeipa,dc=org','(objectclass=person)', attributes=['sn', 'krbLastPwdChange', 'objectclass'])

print("*********************************************")


searchParameters = { 'search_base': 'dc=demo1,dc=freeipa,dc=org','search_filter': '(objectClass=Person)','attributes': ['cn', 'givenName'],'paged_size': 5 }

while True:
    conn.search(**searchParameters)
    for entry in conn.entries:
        print(entry)
    cookie = conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
    if cookie:
        searchParameters['paged_cookie'] = cookie
    else:
        break