# 07. Épicas, Historias de Usuario (HUs) y Criterios de Aceptación Gherkin

## 7.1 Catálogo Oficial de Épicas del Sistema

* **Épicas Fundacionales del Sprint 1 (100% Certificadas):**
  * **HE-01:** Acceso y Autenticación de Usuarios (Google SSO / JWT).
  * **HE-02:** Gestión del Catálogo de Servicios y Asignación.
  * **HE-05:** Gestión de Barberos, Porcentaje de Comisión y Fotos de Perfil.
  * **HE-07:** Gestión de Usuarios, Roles Administrativos y Permisos (RBAC).

* **Épicas Centrales del Sprint 2 (~68% Avance Consolidado):**
  * **HE-04:** Gestión de Reservas (Clientes Registrados e Invitados).
  * **HE-06:** Agenda, Turnos y Cambio de Estado de Reservas del Barbero.
  * **HE-08:** Gestión de Disponibilidad, Horario Semanal y Bloqueos de Agenda.

---

## 7.2 Historias de Usuario y Criterios de Aceptación (Gherkin BDD)

### 📌 HE-04-HU-01: Agendamiento de Cita por Cliente (Online)
> **Como** cliente de Kyrios Studio,  
> **Quiero** seleccionar un servicio, un barbero y una hora disponible en la plataforma web,  
> **Para** asegurar mi cita estética con anticipación sin tener que llamar por teléfono.

* **Criterio de Aceptación 1 (Flujo Exitoso con Disponibilidad):**
  * **Dado que** el cliente se encuentra en la pantalla de agendamiento y selecciona el servicio "Corte Degradado" (duración 60 min) con el barbero "Carlos",
  * **Cuando** selecciona la fecha "2026-10-25" a las "15:00" y proporciona sus datos de contacto válidos,
  * **Entonces** el sistema valida que no existan bloqueos ni reservas previas en esa franja, registra la reserva con estado `PENDIENTE`, genera el token de gestión y despacha la confirmación por WhatsApp y correo electrónico.

* **Criterio de Aceptación 2 (Rechazo por Solapamiento de Horario):**
  * **Dado que** la franja de las "15:00" ya fue reservada por otro cliente de forma concurrente,
  * **Cuando** el cliente intenta confirmar la cita en ese mismo horario,
  * **Entonces** el backend responde con un error HTTP 409 (Conflicto de dominio) informando que la franja horaria fue ocupada y refresca la vista de disponibilidad.

---

### 📌 HE-08-HU-01: Definición de Horario Semanal del Barbero
> **Como** barbero de la barbería,  
> **Quiero** configurar mis días y horas de atención habituales en la semana,  
> **Para** que el sistema solo ofrezca citas en los momentos en que estoy en el local.

* **Criterio de Aceptación (Registro de Turnos en Franjas de 60 Minutos):**
  * **Dado que** el barbero inicia sesión y accede a su módulo de horario semanal,
  * **Cuando** define que los lunes atiende de "09:00" a "18:00",
  * **Entonces** el sistema persiste los intervalos horarios y el motor de disponibilidad genera exactamente 9 franjas de 60 minutos elegibles para los clientes.

---

### 📌 HE-06-HU-02: Actualización de Estado de Cita por el Barbero
> **Como** barbero asignado a una cita,  
> **Quiero** marcar una reserva como `COMPLETADA` o registrar un `NO_SHOW`,  
> **Para** mantener actualizada mi agenda y validar el cumplimiento del servicio.

* **Criterio de Aceptación 1 (Finalización Exitosa del Servicio):**
  * **Dado que** el barbero tiene una cita en estado `CONFIRMADA` en la fecha actual,
  * **Cuando** presiona el botón "Completar Servicio",
  * **Entonces** el estado de la reserva cambia a `COMPLETADA` en la base de datos y se registra el evento en el log de auditoría.

* **Criterio de Aceptación 2 (Seguridad contra Modificación Cruzada - BOLA):**
  * **Dado que** un barbero con `id: 5` intenta cambiar el estado de una cita que pertenece al barbero `id: 9`,
  * **Cuando** envía la petición PATCH al endpoint `/reservas/:id/completar`,
  * **Entonces** el servicio de autorización rechaza la solicitud con HTTP 403 Forbidden y notifica al Superadministrador por correo electrónico.
