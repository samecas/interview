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
--- fstab.2022-04-23	2022-04-23 16:19:57.042359130 +0300
+++ fstab	2022-04-23 16:29:29.104831600 +0300
@@ -6,6 +6,6 @@
 /dev/vg/opt                                 /opt        ext4    data=ordered                0 2
 /dev/vg/home                                /home       xfs     noatime                     0 0
 UUID=3c00c10f-ce64-430c-9a1a-db1abc0bba82   /boot       ext4    data=ordered                0 2
-abc123.example.com:/shareabc                /mnt/abc    nfs     _netdev,bg,tcp,hard,intr    0 0
+xyz123.example.com:/shareabc                /mnt/abc    nfs     _netdev,bg,tcp,hard,intr    0 0
 123abc.example.com:/share1                  /mnt/1      nfs     _netdev,bg,tcp,hard,intr    0 0
-ABC123.example.com:/share2                  /mnt/2      nfs     _netdev,bg,tcp,hard,intr    0 0
+xyz123.example.com:/share2                  /mnt/2      nfs     _netdev,bg,tcp,hard,intr    0 0
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
- **s/^abc/xyz/I'** - here we are searching case-insensitively (option I) for lines which starts with "abc" (regex ^) and replacing them with xyz
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

# API Challenge

Sample API call script which is running on container

## Requirements

Create a container-based script in the language of your choosing which will query the GitHub API once every 10 minutes for commits made by Linus Torvalds and send an alert email to: ??? when a new commit is detected. The script should not send more than one email in a 24 hour period

## Solution

The following files are provided to complete the task: **main.py, Dockerfile, docker-compose.yaml, commits-check-deployment.yaml**

## How to use

**Configuring environment variables**

Open **Dockerfile** and configure GitHub token as well as mail credentials and smtp server

```
....
ENV GITHUB_TOKEN=ghp_xxxxxx
ENV MAIL_USER=sender
ENV MAIL_PASS=Test21123
ENV MAIL_HOST=mail.example.com
ENV MAIL_FROM=sender@example.com
ENV MAIL_TO=recipient@example.com
...
```

Then build the image:
```
# docker build -t gh-app .
Sending build context to Docker daemon  15.87kB
...
 ---> 30e245f9d8ed
Successfully built 30e245f9d8ed
Successfully tagged gh-app:latest
```

Next you may want to run actual docker container:

```
# docker run --name commits -d gh-app
ce65cb56ce4f09562d7a246a7308732193c41c1494537a1dad78d04a27bf8753
```

Or alternatively you can use docker compose:

```
# docker-compose up -d
Creating commits ... done
```

check container status

```
# docker ps | grep  commits
ce65cb56ce4f   gh-app                 "python -u ./main.py"    31 seconds ago   Up 30 seconds             commits
```

Additionally you create pod on k8s environment. In this case minikube was used.

```
# kubectl apply -f commits-check-deployment.yaml
deployment.apps/commits-check configured
# kubectl get pods
NAME                             READY   STATUS             RESTARTS        AGE
commits-check-7d76666866-lfm5q   1/1     Running            0               14s
```
