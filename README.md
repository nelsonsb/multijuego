# Arquitectura para un Juego Multijugador en Línea en Tiempo Real




## Stack Tecnologico

### Infraestructura
* Podemos alojar nuestra aplicación en contenedores. Para esto usamos ECS o Kubernets, de esta forma podemos crear escalabilidad de los contenedores.
* También se puede usar CloudFront para distribuir contenido estático en diferentes regiones de acuerdo a la ubicación de los jugadores

### Gestión de Datos (Almacenamiento)
* Redis, para la memoria caché que se usa cuando tenemos datos frecuentemente consultados
* DynamoDB : tiene baja latencia y ofrece alta escalabilidad. Se puede basar en la región más cercana al jugador. Para información volátil se puede usar TTL en Dynamo
* RDBS : Almacenamiento de información que no necesita baja latencia. Información perdurable en el largo plazo.

### Escalabilidad
* Podemos usar AWS ECS o Kubernetes. ESto nos permite escalar servicios muy fácilmente
* CloudFront. Nos permite distribuir contenidos estáticos de manera Global
* Usando Load Balancer se pueden balancear la carga en los servidores basados en el tráfico y su procedencia.

### Tolerancia a Fallos
* Podemos usar redundancia en Dynamo a nivel regional y replicación de datos.
* Podemos implementar Helth checks de manera automática para reiniciar servidores que han sufrido fallas.
* Las bases de datos pueden tener sistema de Backups continuos.
* Uso de serivios como DLQ para retener los mensajes hasta que sean procesados de manera correcta.

### Seguridad
* POdemos usar cognito para la autenticación de los usuarios.
* Definir roles de manera precisa para asignar los permisos necesarios a los servicios.
* Servicios como KMS nos permiten almacenar de manera segura información sensible.
* Utilizar un Firewall y servicios como WAF para prevención de ataques maliciosos.
* AWS Shield nos permite protegernos de ataques DDoS
* Manejo de JWT para las autenticaciones.

### Diagrama
![Diagrama Arquitectura - Multijuego en línea](https://github.com/nelsonsb/multijuego/multijuego.png)



