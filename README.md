```sh
echo -n | openssl aes-256-ctr -a -pbkdf2 -nosalt
echo | openssl aes-256-ctr -d -a -pbkdf2 -nosalt
```
