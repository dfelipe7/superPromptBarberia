# 10. Integraciones Externas y Servicios de Terceros

## 10.1 Proveedor de Identidad: Google Identity Services (OAuth 2.0)
* **Objetivo:** Delegar la autenticación de personal y clientes en la infraestructura de seguridad de Google.
* **Flujo Multitenant:**
  1. El cliente o miembro del personal inicia sesión en el frontend usando `@react-oauth/google` y obtiene un `idToken`.
  2. El frontend envía el `idToken` al endpoint correspondiente (`/auth/google` para staff o `/auth/clientes/google` para clientes) adjuntando la cabecera `X-Negocio-Slug`.
  3. El backend verifica la firma con `OAuth2Client` de Google usando `GOOGLE_CLIENT_ID`.
  4. Resuelve la identidad global en `Usuario` y busca la membresía en la sede activa (`Administrador`, `Barbero` o `Cliente`).
  5. Emite un JWT con los reclamos acotados a ese tenant.

---

## 10.2 Proveedor de Mensajería: WhatsApp Web Multi-Tenant (@whiskeysockets/baileys)
* **Objetivo:** Notificaciones automáticas de confirmación y recordatorio de citas personalizadas por barbería.
* **Aislamiento por Sede (Multi-Sesión):**
  * Cada barbería tiene su propia sesión independiente de WhatsApp gestionada a través de un pool en memoria `Map<number, SesionWhatsAppNegocio>` en `WhatsAppService`.
  * Las credenciales de conexión se guardan de forma aislada en disco bajo la ruta:
    `~/.barberia_whatsapp_sessions/negocio_<negocioId>/` (o la variable `WHATSAPP_SESSION_PATH`).
  * Migración automática transparente para la sede fundadora (`negocio 1`) desde `~/.kyrios_whatsapp_session`.
  * La vinculación se realiza mediante código QR desde el panel de administración de la sede, con temporizador de desconexión preventiva por inactividad.
  * Colas de mensajes en memoria independientes por tenant con políticas de caducidad automática para citas vencidas (`horaInicioCitaMs`).
  * Plantillas de mensajes dinámicas configurables por tenant en `WhatsAppPlantilla` con variables enriquecidas (`{negocio}`, `{cliente}`, `{fecha}`, `{hora}`, `{servicio}`, `{barbero}`, `{ubicacion}`, `{precio}`, `{enlaceGestion}`).

---

## 10.3 Georreferenciación y Mapas: OpenStreetMap + Google Maps
* **Objetivo:** Brindar a los clientes una experiencia visual moderna de ubicación de la sede con navegación en 1 clic.
* **Arquitectura de Mapas:**
  * **OpenStreetMap Embed:** Embebido en la portada pública con coordenadas canónicas (`latitud`, `longitud`) y estilizado con filtro CSS Dark Mode. Libre de bloqueos de `X-Frame-Options` y sin exigir cookies de terceros ni API keys.
  * **Google Maps Deep Linking:** Botones "Cómo llegar" y "Abrir mapa" dirigen al enlace oficial canónico de Google Maps (`https://www.google.com/maps/search/?api=1&query=lat,lng`) abriendo la aplicación nativa de mapas en el móvil del cliente.

---

## 10.4 Proveedor de Correo: Google SMTP (Nodemailer)
* **Objetivo:** Despacho de alertas inmediatas de ciberseguridad ante anomalías.
* **Configuración:**
  * Host: `smtp.gmail.com` en puerto seguro TLS (587) con autenticación mediante Contraseña de Aplicación (`SMTP_PASS`).
  * Alertas automáticas enviadas al Superadmin de la plataforma cuando el filtro global de excepciones intercepta errores `403` o `>= 500`.

---

## 10.5 Infraestructura Cloud y Contenedores
* **Railway PaaS:** Despliegue continuo de contenedores Docker con Nginx para Frontend y Node.js para Backend.
* **Base de Datos Gestionada:** MySQL 8 / MariaDB relacional con soporte transaccional y claves foráneas compuestas.
