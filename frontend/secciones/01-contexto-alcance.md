# 01. Contexto Organizacional y Definición del Problema

## 1.1 Contexto de Negocio y Generalización a Plataforma SaaS Multitenant
El proyecto tuvo su génesis en un caso de estudio real: la barbería **Kyrios Studio** (Popayán, Colombia), la cual requería modernizar su operativa de agendamiento y control de comisiones. Sin embargo, para responder a los estándares modernos de ingeniería de software y escalabilidad comercial, **la arquitectura fue completamente refactorizada y generalizada como una Plataforma SaaS Multitenant para la Industria de Barberías**.

Bajo este paradigma, el sistema **no está atado a ninguna barbería en particular**:
* **Kyrios Barber** funge exclusivamente como el **inquilino piloto y caso de validación inicial** del sistema.
* **Cualquier barbería, salón masculino, franquicia o sede independiente** puede darse de alta en la plataforma (mediante el hub global `/plataforma` o `POST /plataforma/negocios`).
* Cada negocio opera como un **Tenant 100% autónomo**: dispone de su propia URL pública (`/:slug`), su propio logotipo, su propio lema, sus coordenadas geográficas, su propia paleta de colores y tema visual dinámico (`temaKey`), su catálogo de servicios independientes, su equipo de barberos con comisiones pactadas y su aislamiento criptográfico de sesiones y citas.

## 1.2 Definición del Problema Central
Históricamente, la operación diaria de las barberías se ha gestionado de forma manual y fragmentada mediante cuadernos de apuntes físicos y conversaciones dispersas en aplicaciones de mensajería (WhatsApp personal de cada barbero). Este modelo genera fallas operativas críticas:

1. **Colisión de Citas y Agendamiento Solapado:**  
   Falta de sincronización en tiempo real entre los turnos solicitados por los clientes y la disponibilidad real de cada barbero, provocando sobreventa de horarios o clientes esperando más de 45 minutos.
2. **Elevada Tasa de Inasistencia Sin Aviso (*No-Show*):**  
   Al no contar con un sistema automatizado de recordatorios y confirmación previa de citas, entre un 20% y 30% de los turnos agendados terminaban en inasistencia, causando horas muertas y pérdidas económicas directas para los barberos.
3. **Opacidad en la Liquidación de Comisiones:**  
   Incertidumbre y fricción entre la administración y el personal técnico al final de la jornada por falta de un registro centralizado y trazable de qué servicios fueron efectivamente prestados por cada barbero en cada sede.
4. **Vulnerabilidad y Mezcla de Información en Sedes Múltiples:**  
   Riesgo de fuga o contaminación cruzada de datos de clientes, ingresos y configuraciones entre diferentes sucursales o franquicias al no contar con un aislamiento estricto por inquilino.

## 1.3 Solución Planteada
Diseñar, construir e implementar una plataforma web SaaS generalizada para barberías (*Barber SaaS Platform*) con arquitectura cliente-servidor desacoplada y soporte nativo Multi-Tenant que automatice:
* El agendamiento autónomo de citas en línea por parte de los clientes (registrados o invitados) bajo la URL propia de cada barbería (`/:slug/reservar`).
* El control milimétrico de la disponibilidad, descansos y bloqueos de agenda de cada barbero por sede.
* El despacho automatizado de confirmaciones y recordatorios a través de WhatsApp (Baileys) con sesiones aisladas por negocio y correo electrónico.
* La administración multisede segura bajo el estándar internacional de ciberseguridad **OWASP Top 10: 2025**, permitiendo a dueños y administradores gestionar múltiples barberías con una única cuenta global sin colisión de sesiones.


---

# 02. Alcance del Proyecto y Hoja de Ruta de Sprints

## 2.1 Delimitación del Alcance Global
El proyecto abarca el desarrollo de una plataforma SaaS multitenant para la gestión integral de barberías, contemplando una API REST en NestJS conectada a base de datos relacional MariaDB/MySQL con aislamiento por inquilino, y un cliente web responsivo en React 19 con soporte para prefijos de ruta por sede (`/:slug`).

Todo el ciclo de ingeniería y entrega se encuentra normado bajo el enfoque **Human-in-the-Loop (HITL)**: la Inteligencia Artificial asiste proponiendo código, optimizaciones y pruebas en un bucle continuo de retroalimentación, mientras que el desarrollador humano valida cada cambio y ejerce la toma de decisiones finales en momentos críticos (migraciones de esquemas Prisma, seguridad, autorizaciones y despliegue a producción).

## 2.2 Estado de Cumplimiento por Fases

### 🟢 Sprint 1: Fundaciones, Identidad y Gestión Operativa Base (100% Completado)
Fase inicial centrada en la arquitectura base, seguridad perimetral y administración del personal:
* **Autenticación e Identidad:** Inicio de sesión único con Google OAuth 2.0 (SSO) y emisión de JWT firmados criptográficamente.
* **Modelo RBAC y Membresías:** Desacoplamiento entre la persona global (`Usuario`) y sus roles por sede (`Administrador` y `Barbero`) mediante llaves compuestas `@@unique([negocioId, usuarioId])`.
* **Módulo de Usuarios y Barberos (HE-05, HE-07):** CRUD de personal, asignación de porcentajes de comisión por sede y carga segura de fotos de perfil.
* **Módulo de Servicios (HE-02):** Catálogo de servicios estéticos, duraciones, precios base y vinculación barbero-servicio acotada por tenant.
* **Infraestructura Cloud:** Pipeline CI/CD automatizado en GitHub Actions y despliegue en la nube en Railway.

### 🟢 Fase Multitenant Core & Personalización de Marca (100% Completada)
Evolución de la arquitectura a SaaS Multitenant integral:
* **Aislamiento de Inquilinos:** Middleware de contexto de negocio (`X-Negocio-Slug` / subdominios) y extensión de Prisma para filtrado automático por `negocioId`.
* **Aislamiento de Sesiones por Pestaña en Frontend:** Soporte para rutas prefijadas (`/:slug/...`), tokens independientes (`token_barberia_<slug>`, `cliente_token_<slug>`) y prevención de colisión de sesiones al abrir múltiples sedes en pestañas simultáneas.
* **Directorio Global y Onboarding (/plataforma):** Hub centralizado para explorar sedes registradas, registrar nuevas barberías (`POST /plataforma/negocios`) con asignación atómica de Superadmin fundador, y activación/suspensión de tenants.
* **Identidad de Marca y Temas Dinámicos:** Módulo `PerfilNegocio` con soporte en base de datos para temas visuales (`temaKey`), coordenadas geográficas (`latitud`, `longitud`), geolocalización GPS, radar dark mode con OpenStreetMap/Google Maps y personalización completa de marca en tiempo real (`TenantBrandContext`).

### 🟡 Sprint 2: Motor de Agendamiento, Horarios, Mensajería y Blindaje OWASP 2025 (~85% Avance Consolidado)
Fase orientada a la experiencia de reserva y estabilidad del negocio:
* **Módulo de Reservas (HE-04):** Flujo de agendamiento para clientes registrados e invitados, cálculo dinámico de precios, cancelación controlada por tiempo, tokens criptográficos cifrados (`gestionTokenCifrado`) y soporte para reservas administrativas.
* **Módulo de Agenda del Barbero (HE-06):** Panel interactivo de turnos asignados y máquina de estados de citas (`PENDIENTE`, `CONFIRMADA`, `COMPLETADA`, `CANCELADA`, `NO_SHOW`).
* **Motor de Disponibilidad y Horarios (HE-08):** Horarios semanales por barbero, bloqueos de franjas por descanso y cálculo de slots libres de 60 minutos con principio *Fail-Closed*.
* **WhatsApp Multi-Tenant:** Sesiones independientes de Baileys por barbería almacenadas de forma aislada en disco (`storage/sessions/<negocioId>/`) y plantillas personalizadas por tenant.
* **Seguridad y Auditoría OWASP Top 10: 2025:** Blindaje del A01 al A10, registro estructurado en 3 archivos Winston (`audit.log`, `security.log`, `error.log`), despacho de correos SMTP de alerta inmediata y certificación DAST mediante OWASP ZAP (22.866 vectores superados).

### ⚪ Sprint 3: Monetización, Liquidación y Métricas de Negocio (Backlog Futuro)
* **Pasarela de Pagos Digitales:** Integración de cobros de anticipos en línea (Wompi / Bold).
* **Módulo Financiero y Comisiones (HE-09):** Cierre de caja diario y liquidación automática de comisiones ganadas por barbero.
* **Conmutador Rápido de Sedes (Branch Switcher):** Selector en Header para saltar entre barberías a cargo de un mismo Superadmin en 1 clic.
* **Dashboard Analítico Avanzado:** Reportes gráficos de clientes frecuentes, servicios más vendidos y horas de mayor afluencia.
