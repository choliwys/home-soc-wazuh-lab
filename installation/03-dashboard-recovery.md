# 03 — Recuperación de red y Wazuh Dashboard

## Objetivo

Recuperar la conectividad del nodo central tras el reinicio, finalizar el estado pendiente de `dpkg` y validar `wazuh-dashboard` sin reinstalar los componentes ya validados.

## Alcance y seguridad

- Ejecutar desde la consola local de la laptop secundaria o una sesión SSH ya recuperada.
- Este procedimiento modifica paquetes y servicios del nodo; revisar cada comando antes de ejecutarlo.
- No pegar la contraseña de Wi-Fi, credenciales de dashboard, certificados ni direcciones reales en el repositorio o en un chat.
- Si la red no se recupera con las comprobaciones indicadas, detenerse y registrar la salida sanitizada antes de cambiar la configuración de NetworkManager.

## 1. Confirmar la red

Ejecutar:

```bash
nmcli device status
ip -brief address
ip route
getent ahosts packages.wazuh.com | head
```

Resultado esperado: la interfaz Wi-Fi está conectada, existe una ruta predeterminada y DNS resuelve el repositorio de Wazuh. Si no hay conexión, restaurarla desde la consola con las credenciales privadas correspondientes; no documentar ni automatizar esas credenciales aquí.

## 2. Recuperar el estado de paquetes

Con la red activa, ejecutar en este orden:

```bash
sudo dpkg --configure -a
sudo apt-get -f install
sudo apt-get install wazuh-dashboard
```

El primer comando termina configuraciones pendientes; el segundo resuelve dependencias rotas; el tercero instala o termina de instalar el dashboard. Si uno falla, no repetirlo a ciegas: guardar la salida sanitizada, revisar el espacio disponible con `df -h /` y el estado de red antes de continuar.

## 3. Validar servicios

```bash
sudo systemctl --no-pager --full status wazuh-manager wazuh-indexer wazuh-dashboard
sudo ss -ltnp | grep -E ':(443|1514|1515|55000|9200)\b'
curl -kI --max-time 10 https://localhost
dpkg-query -W wazuh-manager wazuh-indexer wazuh-dashboard filebeat
```

Resultado esperado: los tres servicios están activos, el dashboard escucha en 443 y responde localmente. La consulta de paquetes registra las versiones reales que luego se documentarán sin secretos.

## 4. Validar desde la LAN y cerrar el hito

Desde la estación de trabajo, abrir `https://<WAZUH_LAB_LAN_IP>`. Tras verificar la advertencia esperada del certificado local, iniciar sesión con la credencial almacenada fuera del repositorio. Una vez comprobado el acceso:

1. Rotar las credenciales por defecto con el método oficial aplicable a la versión instalada.
2. Confirmar las reglas de firewall mínimas para la LAN.
3. Actualizar `docs/status.md`, `installation/02-wazuh-single-node-installation.md` y, si corresponde, `docs/decisions.md`.

## Evidencia mínima

- Fecha, versiones de paquetes y estado de los servicios.
- Resultado sanitizado de conectividad y acceso al dashboard.
- Confirmación de rotación de credenciales, sin revelar valores.
- Captura sanitizada solo si aporta evidencia útil.

## Resultado registrado — 2026-09-01

- La recuperación de red devolvió el acceso SSH al nodo central.
- El indexer no iniciaba porque `network.host` conservaba una dirección LAN anterior. Las referencias de red de Indexer, Manager, Filebeat y Dashboard se actualizaron para la dirección LAN actual.
- Como el certificado del indexer incluía la dirección anterior, se regeneró el conjunto de certificados interno y se desplegó fuera de Git con permisos restringidos.
- `wazuh-indexer`, `wazuh-manager`, `filebeat` y `wazuh-dashboard` quedaron activos. El indexer respondió por HTTPS y el dashboard respondió desde la estación de trabajo de la LAN.
- Se confirmó el inicio de sesión real en Wazuh Dashboard desde la LAN con la cuenta administrativa inicial; no se registraron credenciales en el repositorio.
- Se rotaron las credenciales administrativas iniciales. Las comprobaciones posteriores confirmaron comunicación correcta entre Dashboard, Manager, Filebeat e Indexer; los valores no se registraron.
- Versiones validadas: Wazuh Manager, Indexer y Dashboard `4.14.7-1`; Filebeat `7.10.2-2`.
- Se detectó un fallo de `systemd-networkd-wait-online.service` durante el arranque. No bloquea la red ni Wazuh, pero debe revisarse antes del siguiente reinicio planificado.
