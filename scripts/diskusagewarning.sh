
#!/bin/bash
# www.fduran.com
# script that will send an email to EMAIL when disk use in partition PART is bigger than %MAX
# adapt these 3 parameters to your case
MAX=90
EMAIL=laiadomenechburin@gmail.com
PART=xvda1

USE=`df -h |grep $PART | awk '{ print $5 }' | cut -d'%' -f1`
if [ $USE -gt $MAX ]; then
  echo "Porcentaje en uso: $USE" | mail -s "Scraper de Twitter (Mercado cambiario/Ariel Wilkis) con poco espacio restante." $EMAIL
fi
