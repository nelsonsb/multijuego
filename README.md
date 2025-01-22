# Arquitectura para un Juego Multijugador en Línea

## Stack Tecnológico

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

No es un diagrama totalmente exacto de la solución, pero muestra algunos servicios que se pueden implementar para la aplicación.

Adicionalmente se pueden definir diferentes 'Availability Zones' para la redundancia. Se pueden usar diferentes regiones y la escalabilidad también es puede manejar en diferentes regiones y zonas.

Obviamente también falta incluir algunos otros servicios proporcionados por AWS y que se mencionan en el listado.

![Diagrama Arquitectura - Multijuego en línea](https://github.com/nelsonsb/multijuego/blob/main/multijuego.png)


## Listado de Flujos de Datos

Solo se mencionarán algunos de manera muy general

- Autenticación del jugador:
    - El cliente envía las credenciales al API Gateway.
    - El API Gateway redirige la solicitud al Servicio de Autenticación.
    - Si es válido, se genera un token JWT y se envía al cliente.
    - En este caso usamos Cognito.
    - Se visualiza en la parte inferior del gráfico
- Inicio de una partida:
    - El cliente solicita una nueva partida al API Gateway.
    - La solicitud se enruta al Servidor de Juegos correspondiente.
    - El Servidor de Juegos registra la partida en el Servicio de Persistencia.
    - Se observa en la parte superior del gráfico
    - Podemos usar contenedores o usar el servicio EC2 para máquinas virtuales.
- Actualización en tiempo real durante el juego:
    - El Servidor de Juegos actualiza el estado del juego y utiliza Redis para almacenar datos temporales.
    - Si es necesario, los eventos clave se envían al Servicio de Persistencia a través de la Cola de Mensajes.
- Finalización de una partida:
    - El Servidor de Juegos guarda el resultado en el Servicio de Persistencia.
    - El Servicio de Persistencia actualiza la Base de Datos Distribuida.
    - En la gráfica se muestra la base de datos usando RDS
- Protección de datos:
    - Todo el tráfico entre componentes está cifrado con TLS.
    - Los datos sensibles se cifran antes de ser almacenados.



## Sistema de caché distribuido en Python usando Redis

Se debe instalar Redis y la biblioteca de cliente para Python

```
pip install redis
```

Revisar el archivo [punto2.py](https://github.com/nelsonsb/multijuego/blob/main/punto2.py).

### Explicación:

Almacenar y recuperar datos: Utilizamos el método set para almacenar datos con una clave y opcionalmente un tiempo de vida (TTL). 

El método get se usa para recuperar datos por clave.

Manejo de consistencia distribuida: Redis maneja automáticamente la consistencia distribuida.

Invalidación y caducidad: Los métodos invalidate y expire permiten eliminar entradas de la caché o establecer un tiempo de expiración para los datos.

