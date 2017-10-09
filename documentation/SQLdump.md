## Command line interface:
Creating a SQL dump file of the price_sleuth database and ingesting dump file into empty database named 'flourishdump'
```
$ ssh -i 'name of rsa key' username@xx.xxx.xxx.xx
```
Welcome to Ubuntu 16.04.1 LTS (GNU/Linux 4.4.0-47-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

```
~$ mysqldump -u root -p DBname > flourishdump.sql
Enter password: 
~$ ls
flourishdump.sql
~$ mysql -u root -p username < flourishdump.sql
Enter password: 
~$ exit
```
