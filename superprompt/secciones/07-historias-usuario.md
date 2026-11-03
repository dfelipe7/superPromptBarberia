# 07. Épicas, Historias de Usuario (HUs) y Criterios de Aceptación Gherkin

## 7.1 Catálogo Oficial de Épicas del Sistema

* **Épicas Fundacionales del Sprint 1 (100% Certificadas):**
  * **HE-01:** Acceso y Autenticación de Usuarios (Google SSO / JWT).
  * **HE-02:** Gestión del Catálogo de Servicios y Asignación.
  * **HE-05:** Gestión de Barberos, Porcentaje de Comisión y Fotos de Perfil.
  * **HE-07:** Gestión de Usuarios, Roles Administrativos y Permisos (RBAC).

* **Épicas de Plataforma y Aislamiento Multitenant (100% Certificadas):**
  * **HE-11:** Directorio Global de Barberías y Onboarding de Nuevos Tenants.
  * **HE-12:** Identidad de Marca, Georreferenciación y Temas Visuales Dinámicos.

* **Épicas Centrales del Sprint 2 (~85% Avance Consolidado):**
  * **HE-04:** Gestión de Reservas (Clientes Registrados, Invitados y Reservas Admin).
  * **HE-06:** Agenda, Turnos y Cambio de Estado de Reservas del Barbero.
  * **HE-08:** Gestión de Disponibilidad, Horario Semanal y Bloqueos de Agenda.

---

## 7.2 Historias de Usuario y Criterios de Aceptación (Gherkin BDD)

### 📌 HE-04-HU-01: Agendamiento de Cita por Cliente (Online en Sede)
> **Como** cliente de una barbería en la plataforma,  
> **Quiero** seleccionar un servicio, un barbero y una hora disponible en la web de esa sede (`/:slug/reservar`),  
> **Para** asegurar mi cita estética con anticipación sin tener que llamar por teléfono.

* **Criterio de Aceptación 1 (Flujo Exitoso con Disponibilidad):**
  * **Dado que** el cliente se encuentra en `/:slug/reservar` y selecciona el servicio "Corte Degradado" (duración 60 min) con el barbero "Carlos",
  * **Cuando** selecciona la fecha deseada y proporciona sus datos de contacto válidos,
  * **Entonces** el sistema valida que no existan bloqueos ni reservas previas en esa franja dentro del `negocioId`, registra la reserva con estado `PENDIENTE`, genera el token de gestión cifrado y despacha la confirmación por WhatsApp y correo.

* **Criterio de Aceptación 2 (Rechazo por Solapamiento de Horario):**
  * **Dado que** la franja seleccionada ya fue reservada por otro cliente de forma concurrente,
  * **Cuando** el cliente intenta confirmar la cita en ese mismo horario,
  * **Entonces** el backend responde con HTTP 409 (Conflicto) y refresca la vista de disponibilidad de esa sede.

---

### 📌 HE-11-HU-01: Onboarding de Nueva Barbería en la Plataforma
> **Como** emprendedor o dueño de barbería,  
> **Quiero** registrar una nueva sucursal en `/plataforma` con su nombre, slug y correo del fundador,  
> **Para** habilitar un nuevo tenant autónomo con su propia URL y panel de administración.

* **Criterio de Aceptación 1 (Creación Exitosa de Tenant):**
  * **Dado que** se envía una petición con un slug no existente (ej. `barberia-norte`) y un correo de administrador,
  * **Cuando** el endpoint `POST /plataforma/negocios` procesa la solicitud,
  * **Entonces** se crea atómicamente el registro en `Negocio`, se inicializa su `PerfilNegocio` y se vincula al usuario como `Superadmin` de esa sede (`Administrador` con `superadmin: true`).

---

### 📌 HE-12-HU-01: Personalización de Marca y Tema Visual por Sede
> **Como** Superadministrador de una barbería,  
> **Quiero** seleccionar el tema visual oficial y registrar la ubicación geográfica del local,  
> **Para** que los clientes vean la paleta corporativa y el mapa con radar dark mode de mi sede.

* **Criterio de Aceptación 1 (Persistencia de Tema y Radar GPS):**
  * **Dado que** el Superadmin ingresa a `/:slug/configuracion`, selecciona el tema `cyber-lime` y usa el botón GPS,
  * **Cuando** guarda los cambios (`PUT /negocios/perfil`),
  * **Entonces** se persiste `temaKey: 'cyber-lime'` y las coordenadas en la base de datos, y la web pública adopta automáticamente las variables cromáticas y el mapa de calles centrado.

---

### 📌 HE-08-HU-01: Definición de Horario Semanal del Barbero
> **Como** barbero de la barbería,  
> **Quiero** configurar mis días y horas de atención habituales en la semana,  
> **Para** que el sistema solo ofrezca citas en los momentos en que estoy en el local.

* **Criterio de Aceptación (Registro de Turnos en Franjas de 60 Minutos):**
  * **Dado que** el barbero inicia sesión en su sede y accede a su módulo de horario semanal,
  * **Cuando** define que los lunes atiende de "09:00" a "18:00",
  * **Entonces** el sistema persiste los intervalos horarios acotados al `negocioId` y genera las franjas de 60 minutos elegibles para los clientes.

---

### 📌 HE-06-HU-02: Actualización de Estado de Cita por el Barbero
> **Como** barbero asignado a una cita,  
> **Quiero** marcar una reserva como `COMPLETADA` o registrar un `NO_SHOW`,  
> **Para** mantener actualizada mi agenda y validar el cumplimiento del servicio.

* **Criterio de Aceptación 1 (Finalización Exitosa del Servicio):**
  * **Dado que** el barbero tiene una cita en estado `CONFIRMADA` en la fecha actual,
  * **Cuando** presiona el botón "Completar Servicio",
  * **Entonces** el estado de la reserva cambia a `COMPLETADA` en la base de datos y se registra el evento en el log de auditoría.

* **Criterio de Aceptación 2 (Seguridad contra Modificación Cruzada - BOLA / Tenant):**
  * **Dado que** un usuario intenta cambiar el estado de una cita que pertenece a otro barbero o a otra barbería,
  * **Cuando** envía la petición PATCH al endpoint `/reservas/:id/completar`,
  * **Entonces** el servicio de autorización rechaza la solicitud con HTTP 403 Forbidden y notifica al Superadministrador por correo electrónico.
