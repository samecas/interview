# Sed Challenge

Given fstab need to be changed as per requirements.

## Requirements

- take a backup of the existing file with the current date as it's extension .YYYY-MM-DD 
- case-insensitively replace all occurrences of abc at the beginning of a line only with xyz for NFS mounts only

## Solution

Executing the following sed commnad :

```bash
sed -i.`date +"%Y-%m-%d"` '/nfs/ s/^abc/xyz/I' fstab
```
Gives us result: 

```bash
--- fstab	2022-04-23 15:42:14.196522167 +0300
+++ fstab.2022-04-23	2022-04-23 15:41:43.943551574 +0300
@@ -6,6 +6,6 @@
 /dev/vg/opt                                 /opt        ext4    data=ordered                0 2
 /dev/vg/home                                /home       xfs     noatime                     0 0
 UUID=3c00c10f-ce64-430c-9a1a-db1abc0bba82   /boot       ext4    data=ordered                0 2
-xyz123.example.com:/shareabc                /mnt/abc    nfs     _netdev,bg,tcp,hard,intr    0 0
+abc123.example.com:/shareabc                /mnt/abc    nfs     _netdev,bg,tcp,hard,intr    0 0
 123abc.example.com:/share1                  /mnt/1      nfs     _netdev,bg,tcp,hard,intr    0 0
-xyz123.example.com:/share2                  /mnt/2      nfs     _netdev,bg,tcp,hard,intr    0 0
+ABC123.example.com:/share2                  /mnt/2      nfs     _netdev,bg,tcp,hard,intr    0 0
```

make sure backup is ok :
```
diff -u /tmp/fstab.orig /tmp/fstab.2022-04-23  | wc -l
0
```
## Deconstruction sed by piece 

- **sed** binary itself 
- **-i.\`date +"%Y-%m-%d"`** - option for edititing file in combination with "date" command for naming backup file with current date stamp
- **'/nfs/** - search patern. We want to proceed lines which contains "nfs" patern
- **s/^abc/xyz/I'** - here we are searching for lines which start with "abc" (regex ^) and replacing them with xyz 
- **fstab** - actual filename we are changing

## Files included on this repo

- **fstab.orig** - original file for reverence only
- **fstab** - file after executing sed commad
- **fstab.2022-04-23** - backup version of file 

## References
- [regular expression cheat sheet](https://web.mit.edu/hackl/www/lab/turkshop/slides/regex-cheatsheet.pdf)
- [sed manual page](https://man.cx/sed)
- [basic usage of sed command](https://www.geeksforgeeks.org/sed-command-in-linux-unix-with-examples/)
- [advanced usage of the sed command](https://www.linuxtopia.org/online_books/advanced_bash_scripting_guide/x17375.html)

