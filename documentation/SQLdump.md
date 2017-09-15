## Command line interface:
Creating a SQL dump file of the price_sleuth database and ingesting dump file into empty database named 'bree'
```
$ ssh -i id_rsa_xxxxx bree@xx.xxx.xxx.xx
```
Welcome to Ubuntu 16.04.1 LTS (GNU/Linux 4.4.0-47-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

104 packages can be updated.
0 updates are security updates.

```
~$ mysqldump -u root -p price_sleuth > bree.sql
Enter password: 
~$ ls
bree.sql
~$ mysql -u root -p bree < bree.sql
Enter password: 
~$ exit
```
