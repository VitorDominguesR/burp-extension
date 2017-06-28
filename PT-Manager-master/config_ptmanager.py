# coding:utf8

import os

#cria pasta do repositorio
try:
    os.system("apt-get install cifs-utils")
    print "\n\n"
    repository_mount_path = raw_input("Informe o caminho onde será criada a pasta de montagem\n"
                                      "do repositório de vulnerabilidades(Ex.: /root/ptmanager_repo): ")
    os.mkdir(repository_mount_path)
    print "Pasta criada com sucesso\n"


#Cria arquivo de credenciais do SMB
    credentialssmb_mount_path = raw_input("\nInforme o caminho onde será criado o arquivo de credenciais do smb "
                                      "(Ex.: /root/): ")

    credentialssmb_mount_path+='/.smbcredentials'

    credetialssmb_file = open(credentialssmb_mount_path,'w')
    dict_fields_credfile = {'username':'', 'password':'',  'domain':'WORKGROUP'}
    for key, value in dict_fields_credfile.items():
        if key != 'domain':
            dict_fields_credfile[key] = raw_input('Insira '+key+':')
        credetialssmb_file.write(key+'='+dict_fields_credfile[key]+'\n')
    credetialssmb_file.close()

    print "Arquivo de credeciais criado com sucesso\n"

#escreve no arquivo fstab
    fstab_file = open('/etc/fstab','ab+')

    fstab_file.write('//vim.home/vulns_repo   {0} cifs    '
                    'rw,noauto,credentials={1},iocharset=utf8    0       0'.format(repository_mount_path,
                                                                                   credentialssmb_mount_path))

    fstab_file.seek(0, os.SEEK_SET)
    #print fstab_file.readlines()
    fstab_file.close()

    print "Caminho escrito no fstab\n"

#cria arquivo de montagem dentro do profile.d
    mount_smb_file = open('/etc/profile.d/mount_smb.sh','w')
    mount_smb_file.write('#!/bin/bash\n')
    mount_smb_file.write('mount '+repository_mount_path)
    mount_smb_file.close()
#monta o repositorio
    os.system('mount '+repository_mount_path)
    print "Done!"
except Exception as e:
    print e