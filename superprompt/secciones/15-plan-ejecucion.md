# 15. Plan de Ejecución, Hitos y Estado de Avance por Sprints

## 15.1 Resumen Consolidado de Hitos

```
[ Sprint 1: Cimientos & Auth ] ───────► ✅ 100% COMPLETADO (Certificado QA)
[ Sprint 2: Citas, Horarios & OWASP ] ─► 🟡 ~68% EN PROGRESO (Estabilización & QA)
[ Sprint 3: Pagos & Analítica ] ───────► ⚪ PLANIFICADO (Backlog Futuro)
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

### 🟡 Sprint 2: Agendamiento, Disponibilidad, WhatsApp y OWASP 2025 (Avance Actual)
* **Objetivo:** Automatizar el agendamiento de turnos, cálculo de disponibilidad y robustecer la seguridad integral.
* **Estado Actual de Entregables:**
  * **HE-04 (Reservas de Clientes):** 75% Backend / 65% Frontend ➔ Flujo de agendamiento cliente/invitado operativo, tokens de gestión y confirmaciones automáticas. En proceso: pruebas de concurrencia y validaciones de borde.
  * **HE-06 (Agenda de Barbero):** 70% Backend / 60% Frontend ➔ Consulta de turnos y cambio de estados operativo. En proceso: optimización responsive de la vista móvil del barbero.
  * **HE-08 (Disponibilidad y Horarios):** 75% Backend / 65% Frontend ➔ Cálculo de franjas de 60 min y bloqueos de agenda listo con principio *Fail-Closed*. En proceso: interfaz visual para descansos múltiples.
  * **Seguridad y Auditoría OWASP Top 10: 2025:** 100% blindado en código y probado con OWASP ZAP (22.866 ataques superados) y `npm audit` (0 vulnerabilidades).
* **Métrica Consolidada:** **15 de 23 Historias de Usuario con avance significativo (~68% global)**, concentrando el esfuerzo en pruebas de integración y refinamiento UI/UX.

---

### ⚪ Sprint 3: Pasarela de Pagos, Comisiones y Métricas (Próximos Pasos)
* **Objetivo:** Monetización digital y cierre de caja automatizado.
* **Backlog Priorizado:**
  * Integración con pasarela de pagos en línea (Wompi / Bold) para anticipos de citas.
  * Módulo HE-09: Cierre financiero diario y liquidación automática de comisiones ganadas por barbero.
  * Módulo HE-10: Configuración de promociones y descuentos por día de la semana.
  * Dashboard gerencial con métricas de ingresos, retención de clientes y horas pico.
