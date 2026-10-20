# 10. Integraciones Externas y Servicios de Terceros

## 10.1 Proveedor de Identidad: Google Identity Services (OAuth 2.0)
* **Objetivo:** Delegar la autenticación de usuarios y clientes en la infraestructura de seguridad de Google.
* **Flujo de Integración:**
  1. El cliente inicia sesión en el frontend usando `@react-oauth/google` y obtiene un `idToken` firmado por Google.
  2. El frontend envía el `idToken` al endpoint `/auth/google`.
  3. El backend verifica criptográficamente la firma con `OAuth2Client` de Google usando `GOOGLE_CLIENT_ID`.
  4. Se extraen los datos estables (`sub`, `email`, `name`, `picture`).
  5. Se busca al usuario en la base de datos interna; si no existe, se rechaza con 401 (sistema cerrado para personal) o se crea el registro en clientes.

---

## 10.2 Proveedor de Mensajería: WhatsApp Web Protocol (@whiskeysockets/baileys)
* **Objetivo:** Notificar de forma inmediata a los clientes la confirmación y recordatorios de sus citas.
* **Características Técnicas:**
  * Conexión por WebSockets directos emulando una sesión de WhatsApp Web mediante la librería open-source Baileys.
  * La autenticación inicial se realiza escaneando un código QR dinámico desde el panel de administración (`/whatsapp`).
  * Las credenciales de sesión se persisten localmente en una carpeta aislada (`~/.kyrios_whatsapp_session`).
  * **Optimización en Memoria:** Si no hay actividad de escaneo tras 60 segundos, el socket entra en reposo automático para no consumir recursos del servidor.

---

## 10.3 Proveedor de Correo: Google SMTP (Nodemailer)
* **Objetivo:** Despacho de alertas de ciberseguridad al Superadministrador y confirmaciones de respaldo a los clientes.
* **Configuración:**
  * Host: `smtp.gmail.com` en puerto seguro TLS (587).
  * Autenticación mediante Contraseña de Aplicación segura de Google (`SMTP_PASS`).
  * Alertas críticas automáticas: disparadas cuando el filtro global de excepciones intercepta un error con código `403` o `status >= 500`.

---

## 10.4 Proveedor de Base de Datos y Alojamiento Cloud
* **Railway PaaS:** Despliegue continuo de contenedores Docker para Backend y Frontend.
* **MariaDB Cloud:** Instancia relacional gestionada con copias de seguridad automáticas y SSL activo.
