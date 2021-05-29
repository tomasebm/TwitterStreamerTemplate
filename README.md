# TwitterStreamerTemplate
Scripts para montar un streamer de tweets en AWS Lightsail.

> Nota: Crear la instancia seleccionando la imagen Ubuntu 18.04.

## 1 - Instalación de paquetes y dependencias

Al conectarnos a nuestra instancia, clonamos el presente repositorio utilizando:

```sh
sudo git clone https://github.com/tomasebm/TwitterStreamerTemplate
```

Posteriormente, corremos el script 'install.sh' en el directorio raíz

> Nota: Seleccionar las opciones por default de todos los mensajes que aparezcan. En otras palabras, dale enter a todo.

```sh
sh /home/ubuntu/TwitterStreamerTemplate/install.sh
```


## 2 - Configuramos Postfix

> Nota: Configuramos un agente que envía un mensaje cuando nos estamos por quedar sin espacio en disco.

Abrimos el main.cf

```sh
sudo nano /etc/postfix/main.cf
```

Agregamos/modificamos las siguientes lineas:

```sh
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_tls_security_level=encrypt
mydestination =
```

> Nota: Asegurate que la variable 'mydestination' está asignada pero vacía.

### 2.1 - Configuramos las credenciales

```sh
sudo nano /etc/postfix/sasl_passwd
```

En el archivo insertamos la siguiente información:

```sh
[smtp.gmail.com]:587 userid@gmail.com:password
```
Reemplazá userid@gmail y el password con tus credenciales de gmail.

Luego, aplicá los siguientes permisos a los archivos, por seguridad:

```sh
sudo chown root:root /etc/postfix/sasl_passwd
sudo chmod 600 /etc/postfix/sasl_passwd
```

Por último, convertimos el archivo 'sasl_passwd' a una base de datos:

```sh
sudo postmap /etc/postfix/sasl_passwd
```
### 2.2 - Reiniciamos y probamos el funcionamiento

Reiniciamos el sevicio postfix para que tome los cambios:

```sh
sudo systemctl restart postfix
```
Probamos que funcione, deberías recibir un correo electrónico a la dirección que reemplaces en 'userid@gmail.com'

```sh
echo "Test Postfix Gmail SMTP Relay" | mail -s "Postfix Gmail SMTP Relay" userid@gmail.com
```

Si no funciona, podés debuggear con:

```sh
sudo tail /var/log/mail.log
```

## 3 - Configuramos Cron para mantener el scraper siempre corriendo


