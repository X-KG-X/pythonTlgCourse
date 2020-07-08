#!/usr/bin/env python3
from ldap3 import Server, Connection, ALL, MODIFY_ADD, MODIFY_REPLACE, MODIFY_DELETE
from ldap3.utils.dn import safe_rdn

server = Server('ipa.demo1.freeipa.org', get_info=ALL)
conn = Connection(server, 'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', 'Secret123', auto_bind=True)
conn.search('dc=demo1,dc=freeipa,dc=org','(objectclass=person)', attributes=['sn', 'krbLastPwdChange', 'objectclass'])


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

conn.add('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'organizationalUnit')
conn.add('cn=b.young,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'inetOrgPerson', {'givenName': 'Beatrix', 'sn': 'Young', 'departmentNumber': 'DEV', 'telephoneNumber': 1111})

# print("*********************************************")
# print(server.schema.object_classes['inetOrgPerson'])
# print("*********************************************")
# print(server.schema.object_classes['organizationalPerson'])
# print("*********************************************")
# print(server.schema.object_classes['person'])
# print("*********************************************")
# print(server.schema.object_classes['top'])

conn.search('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', '(cn=*)', attributes=['objectClass'])
print(conn.entries[0])

conn.modify_dn('cn=b.young,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'cn=b.smith')

conn.search('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', '(cn=b.smith)', attributes=['objectclass', 'sn', 'cn', 'givenname'])
print(conn.entries[0])

# conn.add('ou=moved, ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'organizationalUnit')
# conn.modify_dn('cn=b.smith,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'cn=b.smith', new_superior='ou=moved, ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org')

# print(safe_rdn('cn=b.smith,ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org'))
# print(safe_rdn('cn=b.smith+sn=young,ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org'))

conn.modify('cn=b.smith,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', {'sn': [(MODIFY_ADD, ['Young'])]})
conn.search('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', '(cn=b.smith)', attributes=['sn', 'cn'])
print(conn.entries[0])
conn.modify('cn=b.smith,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', {'sn': [(MODIFY_DELETE, ['Young'])]})
conn.search('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', '(cn=b.smith)', attributes=['sn', 'cn'])
print(conn.entries[0])
conn.modify('cn=b.smith,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', {'sn': [(MODIFY_REPLACE, ['Smith'])]})
conn.search('ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', '(cn=b.smith)', attributes=['sn', 'cn'])
print(conn.entries[0])

print(conn.compare('cn=b.smith,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'departmentNumber', 'DEV'))
print(conn.compare('cn=b.smith,ou=moved,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'departmentNumber', 'QA'))


conn.modify('cn=b.smith,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', {'sn': [(MODIFY_DELETE, ['Johnson'])], 'givenname': [(MODIFY_REPLACE, ['Beatrix'])]})
conn.modify_dn('cn=b.smith,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'cn=b.young')
print(conn.add('cn=m.johnson,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'inetOrgPerson', {'givenName': 'Mary Ann', 'sn': 'Johnson', 'departmentNumber': 'DEV', 'telephoneNumber': 2222}))
print(conn.add('cn=q.gray,ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'inetOrgPerson', {'givenName': 'Quentin', 'sn': 'Gray', 'departmentNumber': 'QA', 'telephoneNumber': 3333}))