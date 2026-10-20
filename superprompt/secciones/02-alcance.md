# 02. Alcance del Proyecto y Hoja de Ruta de Sprints

## 2.1 Delimitación del Alcance Global
El proyecto abarca el desarrollo del software integral para la barbería Kyrios Studio, contemplando una API REST en NestJS conectada a base de datos relacional MariaDB y un cliente web responsivo en React 19.

## 2.2 Estado de Cumplimiento por Fases

### 🟢 Sprint 1: Fundaciones, Identidad y Gestión Operativa Base (100% Completado)
Fase inicial centrada en la arquitectura base, seguridad perimetral y administración del personal:
* **Autenticación e Identidad:** Inicio de sesión único con Google OAuth 2.0 (SSO) y emisión de JWT firmados criptográficamente.
* **Modelo RBAC:** Definición de roles (`SUPERADMIN`, `ADMINISTRADOR`, `BARBERO`, `CLIENTE`) con `RolesGuard` y `ProtectedRoute`.
* **Módulo de Usuarios y Barberos (HE-05, HE-07):** CRUD de personal, asignación de porcentajes de comisión, carga segura de fotos de perfil mediante Multer (validación MIME real y renombramiento UUID).
* **Módulo de Servicios (HE-02):** Catálogo de servicios estéticos, duraciones, precios base y vinculación barbero-servicio.
* **Infraestructura Cloud:** Pipeline CI/CD automatizado en GitHub Actions y despliegue en la nube en Railway.

### 🟡 Sprint 2: Motor de Agendamiento, Horarios, Mensajería y Blindaje OWASP 2025 (~68% Avance Consolidado)
Fase actual orientada a la experiencia de reserva y estabilidad del negocio. El núcleo operativo está construido y actualmente en ciclo de pruebas de integración, seguridad y refinamiento UI/UX:
* **Módulo de Reservas (HE-04):** Flujo de agendamiento de citas para clientes registrados e invitados, cálculo dinámico de precios, cancelación controlada por tiempo y generación de tokens criptográficos de gestión (`X-Reservation-Management-Token`).
* **Módulo de Agenda del Barbero (HE-06):** Panel interactivo de turnos asignados y máquina de estados de citas (`PENDIENTE`, `COMPLETADA`, `CANCELADA`, `NO_SHOW`).
* **Motor de Disponibilidad y Horarios (HE-08):** Configuración de horarios semanales por barbero, bloqueos de franjas por almuerzo/descansos y algoritmo de cálculo de slots libres de 60 minutos con principio *Fail-Closed*.
* **Notificaciones Automatizadas:** Despacho de mensajes de confirmación de reserva vía WhatsApp Web (Baileys) y cron de recordatorios 2 horas antes de la cita.
* **Seguridad y Auditoría OWASP Top 10: 2025:** Blindaje del A01 al A10, registro estructurado en 3 archivos Winston (`audit.log`, `security.log`, `error.log`), despacho de correos SMTP de alerta inmediata ante errores 500 o 403, y certificación DAST mediante OWASP ZAP (22.866 vectores de ataque superados sin brechas).
* **Estado Actual:** ~68% completado, enfocando el esfuerzo restante en pruebas de concurrencia, pulido de la vista responsive móvil y refinamientos finales de QA.

### ⚪ Sprint 3: Monetización, Liquidación y Métricas de Negocio (Backlog Futuro / Próximos Pasos)
Alcance venidero no implementado en la versión actual:
* **Pasarela de Pagos Digitales:** Integración de cobros de anticipos en línea (Wompi / Bold).
* **Módulo Financiero y Comisiones (HE-09):** Cierre de caja diario, balance de ingresos y liquidación automática de comisiones ganadas por barbero.
* **Módulo de Descuentos y Promociones (HE-10):** Beneficios comerciales configurables por día de la semana.
* **Dashboard Analítico:** Reportes gráficos de clientes frecuentes, servicios más vendidos y horas de mayor afluencia.
