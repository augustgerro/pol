# RSS feed generator website with user friendly interface

This is source code of RSS feed generator website with user friendly interface.


## Configure 

Just create and fill `.env` file. Ex:

```ini
cat << EOF > .env

DB_NAME=politepol
DB_USER=rooooooooooot
DB_PASSWORD=toooooooooooor
MYSQL_ROOT_PASSWORD=rootpass

EOF
```

## Run application and DB


```bash
docker-compose build
docker-compose up -d
```

## Now lets test in browser 

Use your Local or public IP address. Ex:
http://127.0.0.1:8088



---

#### License

MIT
