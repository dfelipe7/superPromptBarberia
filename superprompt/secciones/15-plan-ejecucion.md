# 15. Plan de Ejecución, Hitos y Estado de Avance por Sprints

## 15.1 Resumen Consolidado de Hitos

```
[ Sprint 1: Cimientos & Auth ] ──────────────► ✅ 100% COMPLETADO (Certificado QA)
[ Fase Multitenant Core & Personalización ] ──► ✅ 100% COMPLETADO (Desplegado en Railway)
[ Sprint 2: Citas, Horarios & OWASP ] ────────► 🟡 ~85% EN PROGRESO (Estabilización & QA)
[ Sprint 3: Pagos, Comisiones & Switcher ] ───► ⚪ PLANIFICADO (Backlog Futuro)
```

---

## 15.2 Desglose del Plan por Fases

### 🟢 Sprint 1: Arquitectura Base, Autenticación y Personal (Completado)
* **Objetivo:** Establecer los cimientos del sistema y la gestión administrativa de la barbería.
* **Métricas Alcanzadas:**
  * 48 casos de prueba QA certificados con 100% de éxito.
  * Modelo RBAC operativo con Google OAuth 2.0 y JWT criptográfico.
  * CRUD completo de barberos con cálculo de comisiones y catálogo de servicios estéticos.
  * Pipeline CI/CD en GitHub Actions y despliegue inicial en Railway.
* **Estado:** **100% Entregado y Aprobado.**

---

### 🟢 Fase Multitenant Core, Aislamiento y Personalización de Marca (Completado)
* **Objetivo:** Transformar el sistema monotienda en una plataforma SaaS Multi-Inquilino integral.
* **Métricas Alcanzadas:**
  * Modelo relacional con `Negocio` y `PerfilNegocio`, filtrado automático en ORM mediante extensiones de Prisma por `negocioId`.
  * Membresías desacopladas de la persona global: `Administrador` y `Barbero` con llaves compuestas `@@unique([negocioId, usuarioId])`.
  * Aislamiento de sesiones en Frontend por ruta (`/:slug/...`) y por pestaña (`token_barberia_<slug>`, `cliente_token_<slug>`).
  * Módulo de personalización de marca con temas dinámicos (`temaKey` en BD, `data-tenant-theme` reactivo).
  * Georreferenciación completa: asistente GPS, extractor de coordenadas y radar dark mode con OpenStreetMap y Google Maps.
  * Directorio global SaaS (`/plataforma`) con onboarding atómico de nuevas barberías y Superadmins fundadores.
* **Estado:** **100% Entregado, Migrado en BD y Desplegado en Railway.**

---

### 🟡 Sprint 2: Agendamiento, Disponibilidad, WhatsApp y OWASP 2025 (Avance Actual)
* **Objetivo:** Automatizar el agendamiento de turnos, cálculo de disponibilidad y robustecer la seguridad integral.
* **Estado Actual de Entregables:**
  * **HE-04 (Reservas de Clientes):** Flujo de agendamiento cliente/invitado operativo, tokens de gestión y confirmaciones automáticas. En proceso: pruebas de concurrencia y validaciones de borde.
  * **HE-06 (Agenda de Barbero):** Consulta de turnos y cambio de estados operativo (`COMPLETADA`, `CANCELADA`, `NO_SHOW`).
  * **HE-08 (Disponibilidad y Horarios):** Cálculo de franjas de 60 min y bloqueos de agenda listo con principio *Fail-Closed*.
  * **WhatsApp Multi-Tenant:** Sesiones independientes de Baileys por barbería en disco (`storage/sessions/<negocioId>/`).
  * **Seguridad y Auditoría OWASP Top 10: 2025:** 100% blindado en código y probado con OWASP ZAP (22.866 ataques superados) y `npm audit` (0 vulnerabilidades).
* **Métrica Consolidada:** **Avance consolidado a ~85% global**.

---

### ⚪ Sprint 3: Pasarela de Pagos, Comisiones y Métricas (Próximos Pasos)
* **Objetivo:** Monetización digital, conmutación rápida de sedes y cierre de caja automatizado.
* **Backlog Priorizado:**
  * Conmutador rápido de sedes en Header (Branch Switcher) para alternar entre barberías en 1 clic.
  * Integración con pasarela de pagos en línea (Wompi / Bold) para anticipos de citas.
  * Módulo HE-09: Cierre financiero diario y liquidación automática de comisiones ganadas por barbero.
  * Módulo HE-10: Configuración de promociones y descuentos por día de la semana.
  * Dashboard gerencial con métricas de ingresos, retención de clientes y horas pico.
