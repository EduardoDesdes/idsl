#!/bin/bash

#Configuracion de servicio

cp /root/idsl/daemon /etc/init.d/idsl

chmod 755 /etc/init.d/idsl

for i in `seq 1 6`;do
	ln -s /etc/init.d/idsl /etc/rc$i.d/S01idsl
done

#Levantando servidor

systemctl daemon-reload

service idsl restart
service idsl status
