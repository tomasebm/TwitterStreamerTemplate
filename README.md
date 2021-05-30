# TwitterStreamerTemplate
Scripts para montar un streamer de Twitter usando tweepy en AWS Lightsail.

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
Reemplazá 'userid@gmail' y el password con tus credenciales de gmail. Te recomiendo consultar como sacar las credenciales en [este link.](https://www.linode.com/docs/guides/configure-postfix-to-send-mail-using-gmail-and-google-apps-on-debian-or-ubuntu/) Siempre activá la autenticación de 2 pasos, y configurá una app key. Es muy riesgoso configurar este archivo con tu clave en un archivo de texto plano, por más que le apliquemos permisos de usuario.

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

## 3 - Configuramos Cron para mantener el scraper siempre corriendo y activar el monitor de espacio en disco

Abrimos el archivo para configurar scripts en cron

```sh
sudo crontab -e
```

Y agregamos los dos scripts del presente repositorio:

```sh
*/5 * * * * sh /home/ubuntu/TwitterStreamerTemplate/scripts/keepalive.sh >> /home/ubuntu/TwitterStreamerTemplate/scripts/crontablog.log 2>&1
0 * * * * sh /home/ubuntu/TwitterStreamerTemplate/scripts/diskusagewarning.sh >> /home/ubuntu/TwitterStreamerTemplate/scripts/crontablog2.log 2>&1
```

Reiniciamos cron:

```sh
sudo service cron reload
```
## 4 - Customizamos el scraper con nuestras credenciales y términos de búsqueda

### 4.1 - Configuramos credenciales

En el archivo 'general_settings.py' debemos configurar nuestras consumer y api keys, así como las access tokens.

### 4.2 - Configuramos nuestros términos de búsqueda

En el archivo 'scrap_tweets.py' verás una variable que se llama 'search_terms', la variable contiene una lista con términos random para que la uses de ejemplo. Ingresá los términos que quieras trackear y listo.

### 4.3 - Modificamos el script de monitor de espacio en disco

En la carpeta de scripts está el script "diskusagewarning.sh", modificá el archivo con la dirección de mail a la que querés advertir la falta de espacio en disco.

------------------------------------------------------------------------------------------------------------------------------------------------------

Y listo, ya está todo configurado. Utilizando el programa 'htop' (ya instalado por el script) podemos ver los procesos que corren, debemos verificar que 'scrap_tweets.py' esté corriendo. De todas maneras cron cada unos minutos va a verificar que esté corriendo el script, y si no lo encuentra lo levanta.
