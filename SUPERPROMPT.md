# SUPERPROMPT MAESTRO GLOBAL - PLATAFORMA SAAS PARA BARBERIAS

> **Especificación maestra unificada Full-Stack compilada automáticamente a partir de los módulos independientes de `backend/` y `frontend/`.**

> **ESTADO DE LA ESPECIFICACIÓN: ESPECIFICACIÓN VIVA (LIVING SPECIFICATION)**
> Este documento representa con fidelidad milimétrica el estado del sistema hasta la fase actual y continúa evolucionando activamente a medida que se completan los hitos del roadmap y las siguientes fases de desarrollo.

> - **🟢 Sprint 1 (Cimientos & Auth):** 100% Completado y Certificado.
> - **🟢 Fase Multitenant Core & Temas:** 100% Completado, Migrado y Desplegado.
> - **🟡 Sprint 2 (Citas, Horarios & OWASP):** ~85% Consolidado (En curso).
> - **⚪ Sprint 3 (Pagos, Comisiones & Switcher):** Planificado / Backlog futuro incremental.

## Estructura Maestra del Sistema

- [PARTE I: ESPECIFICACIÓN Y ARQUITECTURA DE BACKEND (NestJS 11 + Prisma ORM 7 + MySQL 8)](#parte-i-backend)
- [PARTE II: ESPECIFICACIÓN Y EXPERIENCIA DE FRONTEND (React 19 + Vite 6 + React Router v7)](#parte-ii-frontend)

---

<a id="parte-i-backend"></a>

# =========================================================================
# PARTE I: ESPECIFICACIÓN DE BACKEND (API REST, PRISMA & PERSISTENCIA)
# =========================================================================

# SUPERPROMPT BACKEND - PLATAFORMA SAAS PARA BARBERIAS

> **Especificación especializada para Backend (NestJS 11 + Prisma ORM 7 + MySQL 8 + Seguridad OWASP).**

> **ESTADO DE LA ESPECIFICACIÓN: ESPECIFICACIÓN VIVA (LIVING SPECIFICATION)**
> Este documento representa con fidelidad milimétrica el estado del sistema hasta la fase actual y continúa evolucionando activamente a medida que se completan los hitos del roadmap y las siguientes fases de desarrollo.

> - **🟢 Sprint 1 (Cimientos & Auth):** 100% Completado y Certificado.
> - **🟢 Fase Multitenant Core & Temas:** 100% Completado, Migrado y Desplegado.
> - **🟡 Sprint 2 (Citas, Horarios & OWASP):** ~85% Consolidado (En curso).
> - **⚪ Sprint 3 (Pagos, Comisiones & Switcher):** Planificado / Backlog futuro incremental.

## Índice de Contenidos

- [00. Instrucciones Ia](#00-instrucciones-ia)
- [01. Contexto Alcance](#01-contexto-alcance)
- [02. Roles Permisos Rbac](#02-roles-permisos-rbac)
- [03. Stack Tecnologico](#03-stack-tecnologico)
- [04. Arquitectura Patrones](#04-arquitectura-patrones)
- [05. Modelo Datos](#05-modelo-datos)
- [06. Seguridad Owasp Logs](#06-seguridad-owasp-logs)
- [07. Contratos Api Dtos](#07-contratos-api-dtos)
- [08. Integraciones](#08-integraciones)
- [09. Pruebas](#09-pruebas)
- [10. Ia Responsable Hitl](#10-ia-responsable-hitl)
- [11. Plan Ejecucion Bootstrap](#11-plan-ejecucion-bootstrap)

---

<a id="00-instrucciones-ia"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 00-instrucciones-ia.md -->
<!-- ========================================================================= -->

# 00. Instrucciones de Ejecución, Directivas de IA y Protocolo HITL

## 0.1 Objetivo General
Este documento establece las directrices normativas y técnicas para el desarrollo, auditoría y mantenimiento del sistema **Plataforma SaaS Multitenant para Barberías (Barber SaaS Platform)**, concebida como una solución agnóstica y multi-inquilino donde cualquier establecimiento de barbería puede operar de manera autónoma (utilizando a *Kyrios Barber* como caso de estudio e inquilino piloto inicial). Cualquier agente de Inteligencia Artificial (IA) o desarrollador de software que interactúe con este repositorio **DEBE** acatar estrictamente las reglas aquí descritas para garantizar la coherencia arquitectónica, la integridad de datos, el aislamiento multi-inquilino (*tenant isolation*) y el blindaje de seguridad.

## 0.2 Terminología Normativa (RFC 2119)
* **DEBE / OBLIGATORIO (SHALL / MUST):** Indica una exigencia absoluta del sistema de ingeniería.
* **NO DEBE (MUST NOT):** Indica una prohibición absoluta por motivos de seguridad o integridad arquitectónica.
* **DEBERÍA / RECOMENDADO (SHOULD):** Indica una práctica aconsejable que solo puede omitirse con justificación técnica explícita.
* **PUEDE / OPCIONAL (MAY):** Indica una característica potestativa según los requerimientos de la fase.

## 0.3 Directivas Estrictas de Codificación
1. **TypeScript Estricto:**
   * Tanto en Backend (NestJS 11) como en Frontend (React 19), el código **DEBE** tener tipado estricto.
   * **PROHIBICIÓN:** **NO DEBE** utilizarse el tipo `any` bajo ninguna circunstancia. Toda estructura de datos debe contar con su correspondiente `interface`, `type` o `DTO`.
2. **Arquitectura y Aislamiento Multi-Tenant en NestJS:**
   * Cada módulo **DEBE** encapsular sus controladores, servicios y repositorios.
   * Toda consulta a modelos de ámbito de inquilino (*tenant-scoped*) **DEBE** estar acotada obligatoriamente por el `negocioId` del contexto de la petición (`X-Negocio-Slug` o subdominio), garantizado por el middleware de aislamiento y extensiones de Prisma.
   * La validación de entrada **DEBE** ejecutarse a través de `ValidationPipe` global con `{ whitelist: true, forbidNonWhitelisted: true, transform: true }`.
3. **Persistencia y Esquema Prisma:**
   * Ningún cambio en la base de datos **DEBE** realizarse manualmente o mediante consultas arbitrarias.
   * Todo ajuste estructural de base de datos **DEBE** ejecutarse mediante migraciones versionadas de Prisma (`npx prisma migrate dev` / `prisma migrate deploy`). Se prohíbe el uso de comandos destructivos como `db push` en producción.
4. **Seguridad Defensiva y Principio Fail-Closed:**
   * En caso de duda, falta de contexto de negocio, o inconsistencia en la verificación de reservas o disponibilidad horaria, el sistema **DEBE** "fallar cerrado" (`fail-closed`), rechazando la operación con el código HTTP correspondiente (403, 404, 409 o 503).
5. **Preservación de Pruebas y Evidencias:**
   * Todo cambio en la lógica de negocio **DEBE** respaldarse con pruebas unitarias (`*.spec.ts`) ejecutadas satisfactoriamente mediante `npm run test`.

---

## 0.4 Protocolo Operativo Human-in-the-Loop (HITL)

### 0.4.1 Marco Conceptual y Fundamento Teórico
La técnica **Human-in-the-Loop (HITL)** o *humano en el bucle* es un enfoque de inteligencia artificial (IA) que combina el aprendizaje automático y los modelos de lenguaje con la **supervisión o intervención humana directa**. 

Su objetivo primordial es crear un **bucle de retroalimentación continuo (*continuous feedback loop*)**:
1. **Automatización y Propuesta (Modelo de IA):** El agente de IA realiza predicciones, genera código TypeScript, formula DTOs, propone esquemas de base de datos o automatiza procesos técnicos repetitivos.
2. **Supervisión y Refinamiento (Humano en el Bucle):** El desarrollador humano inspecciona, valida, corrige, refina y retroalimenta al modelo con ajustes sucesivos.
3. **Decisiones Finales en Momentos Críticos:** En aquellos puntos donde un error genera impacto irreversible (migraciones de base de datos, persistencia, seguridad, autenticación y despliegue a producción), la decisión final reside **exclusivamente en la persona humana**.

```
  ┌────────────────────────────────────────────────────────┐
  │         BUCLE DE RETROALIMENTACIÓN CONTINUO (HITL)     │
  └────────────────────────────────────────────────────────┘
              │                               ▲
  1. Propuesta de Código                      │ 2. Retroalimentación,
     y Automatización                         │    Pruebas y Corrección
              ▼                               │
  ┌──────────────────────┐        ┌──────────────────────┐
  │     AGENTE DE IA     │        │ DESARROLLADOR HUMANO │
  │   (Genera / Predice) │        │ (Supervisa / Refina) │
  └──────────────────────┘        └──────────────────────┘
              │
              ▼ [Llegada a un Momento Crítico]
  ┌──────────────────────────────────────────────────────┐
  │            COMPUERTAS DE APROBACIÓN HUMANA           │
  │  • Compuerta 1: Aprobación de Plan y Arquitectura    │
  │  • Compuerta 2: Auditoría de SQL de Migraciones      │
  │  • Compuerta 3: Verificación de Tests y Calidad      │
  │  • Compuerta 4: Aprobación de Push / Despliegue      │
  └──────────────────────────────────────────────────────┘
              │ [Solo si el Humano Autoriza]
              ▼
    [ Persistencia en BD / Despliegue a Producción ]
```

### 0.4.2 Las 5 Compuertas Mandatorias de Validación Humana
1. **Compuerta 1 (Plan & Arquitectura):** La IA **DEBE** plantear el diagnóstico y el plan de modificación antes de alterar código sustancial. El desarrollador valida el alcance.
2. **Compuerta 2 (Revisión de Código / Diff):** El humano audita línea por línea los cambios propuestos (`git diff`) para descartar regresiones o violaciones al aislamiento multi-inquilino.
3. **Compuerta 3 (Calidad & Tests):** Ningún cambio se considera terminado hasta que el humano ejecute y verifique las suites unitarias (`npm test`) y de compilación (`npm run build`).
4. **Compuerta 4 (Control de Migraciones SQL):** Ninguna migración de base de datos (`prisma migrate dev` o `prisma migrate deploy`) se ejecuta sin que el humano haya revisado y aprobado el archivo SQL generado (`migration.sql`). Se prohíbe `db push` destructivo.
5. **Compuerta 5 (Control de Red y Despliegue):** La IA **NO DEBE** ejecutar `git push`, interactuar con redes externas sin permiso, ni desplegar directamente a Railway/producción. Toda acción de publicación requiere autorización explícita del humano en la terminal.

---

<a id="01-contexto-alcance"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 01-contexto-alcance.md -->
<!-- ========================================================================= -->

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

---

<a id="02-roles-permisos-rbac"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 02-roles-permisos-rbac.md -->
<!-- ========================================================================= -->

# 03. Matriz de Roles, Permisos y Control de Acceso Multitenant (RBAC)

## 3.1 Desacoplamiento: Persona Global vs. Membresías por Sede
El sistema implementa un modelo de Control de Acceso Basado en Roles (RBAC) desacoplado, donde la identidad humana es global pero los permisos se ejercen exclusivamente dentro de la barbería en curso:

```
                      ┌────────────────────────────┐
                      │    Usuario (Global)        │
                      │  id, email, googleId, ...  │
                      └──────────────┬─────────────┘
                                     │
           ┌─────────────────────────┼─────────────────────────┐
           ▼                         ▼                         ▼
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│    Administrador     │  │       Barbero        │  │       Cliente        │
│ negocioId, usuarioId │  │ negocioId, usuarioId │  │ negocioId, usuarioId │
│ superadmin: boolean  │  │ comision, fotoUrl... │  │ citas, historial...  │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

1. **`SUPERADMIN` (Por Sede / Membresía):**
   * Es un administrador con el atributo `superadmin: true` en la tabla `Administrador` para un `negocioId` determinado.
   * Responsable de la creación y gestión de otros administradores en esa sede, configuración de identidad de marca, horarios del local y auditoría.
   * **Alcance:** Un usuario puede ser Superadmin en la Barbería A y no tener acceso o ser simplemente un barbero en la Barbería B.
2. **`ADMINISTRADOR` (Por Sede):**
   * Gestiona el día a día de esa barbería específica.
   * Gestiona servicios, da de alta o suspende barberos, consulta reservas globales de la sede, registra citas presenciales y vincula el dispositivo WhatsApp del local.
   * **Restricción:** No puede crear otros administradores ni alterar la cuenta de un Superadmin de la sede.
3. **`BARBERO` (Por Sede):**
   * Personal técnico vinculado a una barbería mediante `Barbero` `@@unique([negocioId, usuarioId])`.
   * Consulta su agenda de citas asignadas, actualiza el estado de sus turnos (`COMPLETADA`, `CANCELADA`, `NO_SHOW`), define su horario semanal y bloqueos de descanso.
   * **Restricción (BOLA/IDOR):** No tiene autorización para consultar citas, comisiones ni datos de otros barberos ni de otras barberías.
4. **`CLIENTE` (Registrado o Invitado):**
   * **Modalidad Autenticado:** Inicia sesión con Google OAuth o credenciales de cliente; sus reservas se asocian a su ficha de cliente en esa sede (`@@unique([negocioId, usuarioId])` o `@@unique([negocioId, googleId])`).
   * **Modalidad Invitado:** Agenda únicamente con nombre, teléfono y correo; recibe un token de gestión cifrado (`gestionTokenCifrado`) que le permite consultar o cancelar su reserva sin contraseña.

---

## 3.2 Matriz RACI de Permisos por Módulo (Aislada por Tenant)

| Módulo / Funcionalidad | SUPERADMIN (Sede) | ADMINISTRADOR (Sede) | BARBERO (Sede) | CLIENTE (Sede) |
|---|:---:|:---:|:---:|:---:|
| **Crear / Desactivar Administradores de la Sede** | **R / A** | ❌ | ❌ | ❌ |
| **Configurar Perfil, Marca y Tema Visual** | **R / A** | **R** | ❌ | ❌ |
| **Gestionar Barberos y Comisiones** | **A** | **R** | ❌ | ❌ |
| **Gestionar Catálogo de Servicios del Negocio** | **A** | **R** | **C** | **I** |
| **Configurar Horario y Bloqueos Propios** | **A** | **A** | **R** (Solo propios) | ❌ |
| **Consultar Agenda de Citas de la Sede** | **I** (Global sede) | **R** (Global sede) | **R** (Solo propias) | **I** (Solo suyas) |
| **Cambiar Estado de Cita** | **A** | **A** | **R** (Sus turnos) | ❌ |
| **Agendar Cita** | **A** | **R** (Presencial) | ❌ | **R** (Online) |
| **Cancelar Cita** | **A** | **R** | **R** | **R** (Con token/dueño) |
| **Revisar Logs de Auditoría del Negocio** | **R / A** | ❌ | ❌ | ❌ |
| **Configurar WhatsApp del Local** | **A** | **R** | ❌ | ❌ |

*(Convención RACI: **R** = Responsable de ejecutar, **A** = Aprobador final, **C** = Consultado, **I** = Informado / Lectura).*

---

## 3.3 Mecanismo de Aplicación en el Código
* **Frontend:** Rutas protegidas mediante componentes `ProtectedRoute` que verifican tanto la validez del token de la sede activa (`token_barberia_<slug>`) como el rol de membresía en esa sede antes de renderizar la vista.
* **Backend:**
  * **Verificación de Inquilino:** `NegocioContextoService` extrae el `negocioId` a partir del slug recibido en la cabecera `X-Negocio-Slug` o subdominio.
  * **Verificación de Identidad:** `JwtAuthGuard` valida el JWT del personal o del cliente.
  * **Verificación de Roles:** `RolesGuard` inspecciona los roles de membresía asociados al `negocioId` activo.

---

<a id="03-stack-tecnologico"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 03-stack-tecnologico.md -->
<!-- ========================================================================= -->

# 04. Stack Tecnológico y Convenciones de Ingeniería

## 4.1 Tecnologías del Backend (API REST Multitenant)
* **Lenguaje:** TypeScript 5.7+ con compilación estricta (`strict: true`, `noImplicitAny: true`).
* **Framework:** NestJS 11.0 (Arquitectura orientada a módulos, controladores e inyección de dependencias).
* **ORM:** Prisma ORM 7.0 con extensiones de cliente personalizadas (`$extends`) para inyección automática de filtros de aislamiento por `negocioId`.
* **Motor de Base de Datos:** MariaDB 11.4 / MySQL 8.0 (Almacenamiento relacional compatible con transacciones ACID y claves compuestas foráneas).
* **Seguridad Perimetral:**
  * `helmet` v8.0.0 (Inyección de cabeceras de seguridad HTTP, CSP adaptado para iframes de mapas).
  * `@nestjs/throttler` v6.4.0 (Rate Limiting defensivo anti fuerza bruta).
  * `argon2` y `bcrypt` (Hashing criptográfico irreversible con salt para credenciales y tokens de gestión).
  * `@nestjs/jwt` (Generación y verificación de tokens de sesión HMAC-SHA256 con separación de roles de personal y clientes).
* **Observabilidad y Alertas:**
  * `nest-winston` + `winston-daily-rotate-file` (Registro rotativo en `audit.log`, `security.log` y `error.log`).
  * `@nestjs-modules/mailer` + `nodemailer` (Despacho de alertas SMTP a Google Gmail ante fallos 403 y 500).
* **Integraciones:**
  * `@whiskeysockets/baileys` (Integración con protocolo oficial WhatsApp Web con sesiones multi-tenant en disco).
  * `google-auth-library` (Validación criptográfica de tokens emitidos por Google Identity Services).

## 4.2 Tecnologías del Frontend (Cliente Web Multitenant)
* **Librería Core:** React 19.0 con TypeScript 5.8+.
* **Empaquetador y Servidor:** Vite 6.2 (Compilación modular basada en ESM y recarga rápida HMR) + Nginx en contenedor de producción.
* **Enrutamiento:** React Router DOM v7 (Manejo de rutas dinámicas prefijadas por sede `/:slug/...` y rutas globales `/plataforma`).
* **Manejo de Estado del Servidor:** TanStack Query v5 (Caché reactiva, invalidación automática tras mutaciones).
* **Clientes HTTP:**
  * `apiClient` (Axios 1.7): Interceptor con `Authorization: Bearer <token_barberia_slug>` y cabecera `X-Negocio-Slug: <slug>` para administración y catálogo.
  * `reservasApiClient` (Axios 1.7): Interceptor con `Authorization: Bearer <cliente_token_slug>` para el portal de clientes autenticados.
* **Estilos y Theming Dinámico:**
  * CSS Variables reactivas inyectadas por `TenantBrandContext` (`data-tenant-theme="clasico-azul" | "cyber-lime" | "oro-vip" | ...`).
  * Mapas embebidos con OpenStreetMap (filtro CSS Dark Mode) e integración a Google Maps.
* **Iconografía:** Lucide React.

## 4.3 Convenciones de Código y Estructura
1. **Nomenclatura de Archivos:** `kebab-case.tipo.ts` (Ej: `reservas.controller.ts`, `reservas.service.ts`, `reservas.repository.ts`).
2. **DTOs Obligatorios:** Toda petición POST, PUT o PATCH **DEBE** contar con su DTO de entrada tipado con decoradores de `class-validator` (`@IsString()`, `@IsInt()`, `@Min()`, `@IsEmail()`, etc.).
3. **Manejo de Respuestas:** El backend **DEBE** estructurar sus respuestas exitosas bajo un esquema JSON claro, y en caso de error **DEBE** responder con el formato estándar `{ statusCode, timestamp, path, message }` garantizado por el filtro global de excepciones.

---

<a id="04-arquitectura-patrones"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 04-arquitectura-patrones.md -->
<!-- ========================================================================= -->

# 05. Arquitectura del Sistema y Patrones de Diseño Multitenant

## 5.1 Estilo Arquitectónico Global
La plataforma adopta una **Arquitectura Cliente-Servidor Desacoplada (Decoupled Client-Server Architecture)** con soporte nativo **Multi-Tenant (SaaS)** y comunicación sin estado (*stateless*) mediante API REST sobre HTTP/HTTPS:

```
[ Cliente Web (React 19 SPA) ]
  ├── Ruta: /:slug/... (Portal Sede)
  └── Ruta: /plataforma (Directorio SaaS)
              │
              ▼ (HTTPS / JSON / JWT + X-Negocio-Slug)
[ Middleware de Aislamiento de Inquilinos (Tenant Context) ]
              │
              ▼ (Contexto NegocioId inyectado en Request)
[ Capa de Controladores (REST Controllers) ]
              │
              ▼ (Guards, Pipes & Interceptors)
[ Capa de Servicios de Dominio (Business Services) ]
              │
              ▼ (Extensión de Prisma con Filtro Automático negocioId)
[ Capa de Repositorios (Data Access Layer) ]
              │
              ▼ (Claves Foráneas Compuestas)
[ Motor Prisma ORM 7 ➔ Base de Datos MySQL / MariaDB ]
```

## 5.2 Patrones de Diseño Aplicados en el Sistema

1. **Patrón de Aislamiento Multi-Inquilino (Tenant Isolation Pattern):**
   * **Resolución de Inquilino:** `NegocioContextoService` extrae el negocio a partir de la cabecera `X-Negocio-Slug` o el subdominio.
   * **Blindaje en ORM:** Las consultas a modelos tenant-scoped se filtran automáticamente por `negocioId`. No es posible que una barbería consulte ni altere registros de otra.
2. **Patrón Path-Prefix Multitenancy en Frontend:**
   * Las rutas del frontend se prefijan con el slug de la barbería (`/:slug/dashboard`, `/:slug/reservar`, `/:slug/catalogo`).
   * Axios extrae automáticamente el slug de la URL mediante `obtenerNegocioSlugActivo()` y lo envía en la cabecera `X-Negocio-Slug`.
3. **Aislamiento de Sesiones por Pestaña (Tab Session Isolation):**
   * Los tokens JWT y perfiles se almacenan con claves compuestas en almacenamiento de sesión: `token_barberia_<slug>` y `cliente_token_<slug>`.
   * Un usuario puede tener abiertas múltiples pestañas administrando sedes distintas simultáneamente sin colisión de estado.
4. **Patrón Repositorio (Repository Pattern):**
   * Desacopla la lógica de negocio pura de las consultas de persistencia a la base de datos (`reservas.repository.ts`, `usuarios.repository.ts`, `perfil-negocio.repository.ts`, etc.).
5. **Patrón Adaptador y Puertos (Ports & Adapters):**
   * En el módulo de horarios se implementó el puerto `ProveedorReservasActivas` (`proveedor-reservas-activas.port.ts`), desacoplando el cálculo de disponibilidad de la implementación física del módulo de reservas.
6. **Patrón Estrategia (Strategy Pattern):**
   * Utilizado en la validación de disponibilidad horaria mediante `ReglaDisponibilidadStrategy` y `ReservaActivaRule`. Cada restricción de horario (bloqueo por almuerzo, día de descanso, cita ocupada) se evalúa como una estrategia independiente.
7. **Patrón Filtro Global de Excepciones (Exception Filter Pattern):**
   * Centralizado en `all-exceptions.filter.ts`. Intercepta cualquier excepción HTTP o fallo interno no capturado, homogeneizando el JSON de salida y disparando el subsistema de alertas SMTP de seguridad.
8. **Principio de Falla Cerrada (Fail-Closed):**
   * Si el proveedor de reservas o el contexto de negocio no responden o son inválidos, el sistema **DEBE** rechazar la consulta (con 403 o 503) en lugar de responder datos vacíos o franjas abiertas a ciegas.
9. **Patrón Máquina de Estados Finita:**
   * Gestiona el ciclo de vida de una cita:
     * `PENDIENTE` ➔ `CONFIRMADA`
     * `CONFIRMADA` ➔ `COMPLETADA`
     * `CONFIRMADA` ➔ `CANCELADA`
     * `CONFIRMADA` ➔ `NO_SHOW` (Inasistencia tras tolerancia)

---

## 5.3 Árbol Estructural Canónico del Repositorio

Cualquier IA o desarrollador que reconstruya el sistema **DEBE estructurar el código en las siguientes rutas y módulos**:

```
Barberia-Backend/
├── prisma/
│   ├── schema.prisma                  # Esquema Prisma canónico
│   └── migrations/                    # Historial de migraciones SQL versionadas
├── src/
│   ├── main.ts                        # Bootstrap NestJS con Helmet, Throttler, ValidationPipe
│   ├── app.module.ts                  # Registro raíz de módulos y middleware de inquilinos
│   ├── auth/                          # Autenticación JWT, Google OAuth, Guards y Decoradores
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── guards/                    # JwtAuthGuard, RolesGuard
│   │   └── decorators/                # @Roles(), @CurrentUser()
│   ├── common/
│   │   ├── filters/                   # all-exceptions.filter.ts
│   │   ├── middleware/                # tenant-context.middleware.ts (resuelve X-Negocio-Slug)
│   │   └── guards/                    # tenant.guard.ts
│   ├── prisma/
│   │   ├── prisma.service.ts          # Conexión Prisma y extensiones de aislamiento
│   │   └── prisma.module.ts
│   └── modules/
│       ├── alerts/                    # Alertas SMTP de seguridad inmediata
│       ├── configuracion/             # Políticas operativas del tenant (cancelación, no-show)
│       ├── horarios/                  # Motor de disponibilidad, cálculo de slots de 60m
│       ├── negocios/                  # Directorio SaaS, onboarding POST /plataforma/negocios
│       ├── perfil-negocio/            # Identidad visual (temaKey), coordenadas GPS, logos
│       ├── reservas/                  # Agendamiento, máquina de estados, token de gestión
│       ├── servicios/                 # Catálogo de servicios por sede
│       ├── usuarios/                  # Personal (Administradores, Barberos, comisiones)
│       └── whatsapp/                  # Baileys WhatsApp multi-tenant en disco
└── test/                              # Suites e2e y pruebas de integración

Barberia-Frontend/
├── src/
│   ├── main.tsx                       # Bootstrap React 19 con QueryClient y BrowserRouter
│   ├── App.tsx                        # Rutas dinámicas /:slug, /plataforma, ErrorBoundary
│   ├── auth/
│   │   ├── context/AuthContext.tsx    # Sesión de personal administrativo y barbero
│   │   └── services/authService.ts
│   ├── config/
│   │   └── tenantTheme.ts             # Paletas de temas ('clasico-azul', 'cyber-lime', etc.)
│   ├── features/
│   │   ├── negocio/
│   │   │   ├── context/TenantBrandContext.tsx  # Inyección de tema visual (data-tenant-theme)
│   │   │   └── pages/ConfiguracionNegocioPage.tsx
│   │   ├── reservas/
│   │   │   ├── pages/ReservaClientePage.tsx    # Wizard público de reserva
│   │   │   ├── pages/ClientePortalPage.tsx     # Portal cliente autenticado
│   │   │   └── pages/ReservaGestionInvitadoPage.tsx # Gestión de cita vía token hash
│   │   ├── barberos/                  # Gestión de personal y comisiones
│   │   ├── servicios/                 # Gestión del catálogo de servicios
│   │   ├── horarios/                  # Gestión de matriz horaria y bloqueos
│   │   └── whatsapp/                  # Vinculación QR multi-tenant
│   ├── pages/
│   │   ├── Home/                      # Landing pública por barbería (/:slug)
│   │   │   └── components/LocationSection.tsx  # Mapa OpenStreetMap con modo oscuro y GPS
│   │   ├── Dashboard/                 # Panel administrativo por sede
│   │   ├── Plataforma/                # Hub global SaaS (/plataforma y /)
│   │   └── Login/                     # Inicio de sesión con Google SSO
│   └── shared/
│       ├── lib/http/axios.ts          # Clientes Axios duales (apiClient y reservasApiClient)
│       ├── layout/                    # MainLayout, Header, Sidebar
│       └── components/                # ProtectedRoute, ErrorBoundary
```

---

<a id="05-modelo-datos"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 05-modelo-datos.md -->
<!-- ========================================================================= -->

# 06. Modelo de Datos y Esquema Relacional Multitenant (Prisma)

## 6.1 Principios del Modelo Multitenant y Aislamiento de Datos
El modelo de datos se encuentra normalizado en tercera forma normal (3NF), gestionado íntegramente mediante **Prisma ORM 7** sobre MySQL 8 / MariaDB 11.4:
1. **Desacoplamiento de Identidad Global:** La tabla `Usuario` representa a la persona física en la plataforma (nombre, email, googleId). **No pertenece a ningún negocio**.
2. **Membresías por Sede:** Los roles operativos pertenecen al negocio. `Administrador` y `Barbero` vinculan a un `Usuario` con un `Negocio` mediante claves únicas compuestas `@@unique([negocioId, usuarioId])`. Una persona puede ser administradora en una sede, barbero en otra y cliente en una tercera sin conflicto alguno.
3. **Claves Foráneas Compuestas para Blindaje de Inquilinos:** Relaciones como `BarberoServicio` y `Reservation` validan con llaves compuestas `(negocioId, id)` a nivel del motor de base de datos, impidiendo que una entidad de una sede se vincule con entidades de otra.
4. **Persistencia de Marca y Temas:** `PerfilNegocio` implementa relación 1:1 con `Negocio`, soportando `temaKey` ('clasico-azul', 'cyber-lime', etc.), coordenadas GPS (`latitud`, `longitud` con precisión `Decimal(10,7)`) e imágenes de marca.
5. **Concurrencia y Citas:** `Reservation` utiliza la columna generada en base de datos `slotActivo` (1 si ocupa la franja, NULL si CANCELLED) con un índice único `@@unique([barberoId, date, startTime, slotActivo])` para permitir re-reserva tras cancelaciones sin colisión de slots.

---

## 6.2 Diagrama Entidad-Relación Lógico
```
Negocio (1) ──── (0..1) PerfilNegocio (1:1 con temaKey, coordenadas y branding)
Negocio (1) ──── (N) RedSocialNegocio (Redes sociales públicas por sede)
Negocio (1) ──── (N) Administrador (N) ──── (1) Usuario (Identidad Global)
Negocio (1) ──── (N) Barbero       (N) ──── (1) Usuario (Identidad Global)
Negocio (1) ──── (N) Servicio      (N) ──── (N) Barbero (vía BarberoServicio)
Negocio (1) ──── (N) BarberWeeklySlot (Franjas semanales por barbero)
Negocio (1) ──── (N) BarberScheduleBlock (Bloqueos y descansos temporales)
Negocio (1) ──── (N) GeneralClosure (Cierres generales festivos por sede)
Negocio (1) ──── (N) Cliente       (N) ──── (0..1) Usuario (Identidad Global)
Negocio (1) ──── (N) Reservation   (Citas con token criptográfico y slotActivo)
Negocio (1) ──── (N) WhatsAppPlantilla (Plantillas personalizadas por sede o globales)
Negocio (1) ──── (0..1) ConfiguracionNegocio (Políticas de cancelación y no-show)
```

---

## 6.3 Archivo Canónico Completo: `prisma/schema.prisma`
Cualquier agente de IA o desarrollador que clone o reconstruya el proyecto **DEBE utilizar este archivo exacto** sin modificar nombres de modelos, mapeos ni atributos:

```prisma
generator client {
  provider = "prisma-client"
  output   = "../generated/prisma"
}

datasource db {
  provider = "mysql"
}

enum EstadoUsuario {
  ACTIVO
  INACTIVO
}

/// Clasificación GLOBAL de la persona en la plataforma. NO es una fuente de
/// privilegios.
///
/// - `SUPERADMIN`: valor HEREDADO, conservado solo por compatibilidad de datos
///   y de contrato. En este SaaS **NO existe un SUPERADMIN global de
///   plataforma**: el carácter SUPERADMIN es una MEMBRESÍA de negocio y vive
///   en `Administrador.superadmin`, en la fila `(negocioId, usuarioId)`, con
///   alcance exclusivo a ESE negocio.
/// - `PERSONAL`: persona de la plataforma sin carácter de plataforma. Sus
///   roles EFECTIVOS (administrador/barbero/superadmin) NO se derivan de esta
///   columna, sino de sus perfiles operativos (`Administrador` / `Barbero`) en
///   el negocio concreto.
///
/// ESTA COLUMNA NO CONCEDE NINGÚN PRIVILEGIO POR SÍ SOLA: la autorización la
/// resuelven la membresía activa del negocio del contexto y el guard de roles
/// (`RolesGuard`), que solo lee los roles derivados de las membresías.
///
/// Los antiguos valores `ADMINISTRADOR` y `BARBERO` se migraron a `PERSONAL`
/// en la Fase 8: describían el modelo de negocio único, no el modelo
/// multitenant, y ya no se conservaban como fuente autorizante.
enum RolUsuario {
  SUPERADMIN
  PERSONAL
}

/// Estado de un negocio (tenant) dentro de la plataforma.
/// `INACTIVO` permite desactivar un negocio sin borrar su histórico:
/// las reservas, clientes y servicios existentes se conservan.
enum EstadoNegocio {
  ACTIVO
  INACTIVO
}

/// Negocio (barbería) dentro de la plataforma SaaS.
///
/// Es la entidad tenant: cada registro operativo (clientes, barberos,
/// servicios, reservas, horarios, configuraciones) pertenece a un negocio.
/// `Usuario` es global (identidad de la persona en la plataforma) y sus
/// perfiles operativos son los que se asocian a un negocio.
///
/// `slug` es el identificador PÚBLICO y estable con el que se resuelve el
/// negocio en cada petición (subdominio o cabecera `X-Negocio-Slug`).
/// No debe contener información sensible: es visible en URLs y logs.
///
/// `onDelete: Restrict`: eliminar un negocio con datos exige una operación
/// explícita; la vía prevista para "retirar" una barbería es `estado =
/// INACTIVO`, que conserva el histórico.
model Negocio {
  id            Int           @id @default(autoincrement())
  slug          String        @unique @db.VarChar(63)
  nombre        String        @db.VarChar(150)
  estado        EstadoNegocio @default(ACTIVO)
  zonaHoraria   String        @default("America/Bogota") @db.VarChar(64)
  creadoEn      DateTime      @default(now())
  actualizadoEn DateTime      @updatedAt

  // Relaciones inversas: los perfiles operativos pertenecen a un negocio.
  administradores    Administrador[]
  barberos           Barbero[]
  clientes           Cliente[]
  servicios          Servicio[]
  barberoServicios   BarberoServicio[]
  reservas           Reservation[]
  franjasSemanales   BarberWeeklySlot[]
  bloqueosHorario    BarberScheduleBlock[]
  cierresGenerales   GeneralClosure[]
  configuraciones    ConfiguracionNegocio[]
  plantillasWhatsApp WhatsAppPlantilla[]
  /// Perfil público de marca y ubicación (relación 1:1).
  perfil             PerfilNegocio?
  redesSociales      RedSocialNegocio[]

  @@map("negocios")
}

/// Perfil PÚBLICO de un negocio: identidad visual y ubicación.
///
/// RELACIÓN 1:1 CON `Negocio`
/// - `negocioId` es ÚNICO: como máximo un perfil por barbería.
/// - NO duplica el nombre ni el slug del negocio: se leen de `Negocio`.
///
/// POR QUÉ UN MODELO PROPIO Y NO `ConfiguracionNegocio`
/// `ConfiguracionNegocio` es un almacén CLAVE/VALOR de políticas OPERATIVAS
/// (antelación de cancelación, tolerancia de NO_SHOW): el valor es un texto con
/// un discriminador de tipo. La marca y la ubicación son CONTENIDO PÚBLICO
/// ESTRUCTURADO, con tipado, longitudes y coordenadas propias: meterlò en un
/// almacén clave/valor obligaría a serializar y a validar a mano, y haría que
/// un campo tan público dependiera de una clave de configuración.
///
/// TODOS LOS CAMPOS SON NULABLES: una barbería puede existir sin perfil
/// completo mientras termina de configurarlo. La ausencia de un perfil NO es
/// un error.
///
/// LAS IMÁGENES SON REFERENCIAS, NO ARCHIVOS: `faviconUrl`, `bannerUrl`,
/// `logoBlancoUrl` y `logoNegroUrl` guardan RUTAS o URLs. En la base de datos
/// NO se almacenan bytes, base64 ni archivos completos. La carga física de
/// archivos es una fase posterior.
///
/// LA URL DEL MAPA NO SE GUARDA: se deriva de `latitud`/`longitud`, que son la
/// única fuente de verdad. Así no puede quedar desincronizada.
model PerfilNegocio {
  id        Int @id @default(autoincrement())
  /// Negocio al que pertenece el perfil. UNICO: un perfil por barbería.
  negocioId Int @unique

  /// Frase principal de la marca (lema o descriptor corto).
  frasePrincipal String? @db.VarChar(200)

  /// Identificador del preset de tema visual ('clasico-azul', 'cyber-lime', etc.)
  temaKey String? @default("clasico-azul") @db.VarChar(50)

  // --- Identidad visual: REFERENCIAS a archivos (nunca binarios) ---
  faviconUrl    String? @db.VarChar(500)
  bannerUrl     String? @db.VarChar(500)
  logoBlancoUrl String? @db.VarChar(500)
  logoNegroUrl  String? @db.VarChar(500)

  // --- Ubicación ---
  direccion    String?  @db.VarChar(200)
  ciudad       String?  @db.VarChar(120)
  departamento String?  @db.VarChar(120)
  /// Referencia opcional para orientarse ("Local 2, junto a la panadería").
  referencia   String?  @db.VarChar(200)
  /// Coordenadas en grados decimales. `Decimal(10,7)` aporta ~1 cm de
  /// precisión y cubre el rango de longitud (±180) sin desbordar.
  latitud      Decimal? @db.Decimal(10, 7)
  longitud     Decimal? @db.Decimal(10, 7)

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  negocio Negocio @relation(fields: [negocioId], references: [id], onDelete: Cascade)

  @@map("perfiles_negocio")
}

/// Tipo de red social del negocio. Los predefinidos (TIKTOK, FACEBOOK,
/// INSTAGRAM, WHATSAPP) están limitados a UNO por negocio; OTRO permite
/// varias entradas siempre que `nombre` no se repita.
enum TipoRedSocial {
  TIKTOK
  FACEBOOK
  INSTAGRAM
  WHATSAPP
  OTRO
}

/// Red social pública del negocio (parte del perfil).
///
/// ALCANCE
/// - Vive fuera de `PerfilNegocio` porque un negocio puede tener VARIAS
///   (una por red, más las "OTRO" que agregue).
/// - AISLAMIENTO: modelo tenant-scoped. Se filtra por `negocioId` vía
///   `NegocioAislamientoService` y la extensión de Prisma.
/// - UNICIDAD: `(negocioId, tipo, nombre)`. Para predefinidos el backend
///   fija `nombre` al canónico (`TikTok`, `Facebook`, …), de modo que solo
///   pueda existir uno. Para OTRO, `nombre` lo pone el usuario y actúa
///   como discriminante.
model RedSocialNegocio {
  id            Int           @id @default(autoincrement())
  negocioId     Int
  tipo          TipoRedSocial
  nombre        String        @db.VarChar(80)
  url           String        @db.VarChar(500)
  orden         Int           @default(0)
  activo        Boolean       @default(true)
  creadoEn      DateTime      @default(now())
  actualizadoEn DateTime      @updatedAt

  negocio Negocio @relation(fields: [negocioId], references: [id], onDelete: Cascade)

  @@unique([negocioId, tipo, nombre])
  @@unique([negocioId, id])
  @@index([negocioId, activo, orden])
  @@map("redes_sociales_negocio")
}

/// Identidad GLOBAL de la persona en la plataforma.
///
/// No pertenece a ningún negocio: es la persona. Sus permisos dentro de una
/// barbería vienen de sus perfiles (`Administrador` / `Barbero`), no de esta
/// tabla. Por eso las relaciones hacia `Usuario` NO son compuestas: el usuario
/// es global y solo el PERFIL es por negocio.
///
/// Una persona puede tener VARIOS perfiles (uno por barbería en la que
/// opera): las relaciones con los perfiles son uno-a-muchos.
model Usuario {
  id       Int           @id @default(autoincrement())
  googleId String?       @unique
  email    String        @unique
  nombre   String
  apellido String
  /// Valor GLOBAL heredado del modelo de negocio único. **NO concede ningún
  /// privilegio**: los roles efectivos se derivan de las MEMBRESÍAS
  /// (`Administrador` / `Barbero`) de la persona en el negocio del contexto.
  /// Un `SUPERADMIN` aquí NO significa superadmin de plataforma: el carácter
  /// SUPERADMIN vive en `Administrador.superadmin` (membresía por negocio).
  /// Se conserva por compatibilidad de datos y de contrato, y es
  /// INFORMATIVO.
  rol      RolUsuario
  estado   EstadoUsuario @default(ACTIVO)

  administradores Administrador[]
  barberos        Barbero[]
  clientes        Cliente[]
}

/// Perfil de administrador de un negocio.
///
/// `usuarioId` es ÚNICO POR NEGOCIO: la misma persona puede ser administradora
/// de varias barberías (y de ninguna).
///
/// `superadmin` es el CARÁCTER de la membresía, no un atributo de la
/// persona: `true` significa SUPERADMIN **de este negocio** y `false`
/// ADMINISTRADOR de este negocio. El alcance es siempre el negocio de la fila:
/// en este SaaS NO existe un superadmin de plataforma ni una sesión de
/// plataforma. La columna es aditiva y no promueve a nadie: las membresías
/// existentes siguen siendo ADMINISTRADOR.
model Administrador {
  id         Int           @id @default(autoincrement())
  usuarioId  Int
  /// Negocio al que pertenece el perfil. OBLIGATORIO: un perfil sin
  /// negocio no puede existir.
  negocioId  Int
  estado     EstadoUsuario @default(ACTIVO)
  /// SUPERADMIN de ESTE negocio (`true`) o ADMINISTRADOR (`false`).
  /// La autorización depende exclusivamente de esta membresía activa y del
  /// contexto del negocio: `Usuario.rol` no concede ningún privilegio.
  superadmin Boolean       @default(false)

  usuario Usuario @relation(fields: [usuarioId], references: [id])
  negocio Negocio @relation(fields: [negocioId], references: [id], onDelete: Restrict)

  @@unique([negocioId, usuarioId])
  /// Destino de las claves foráneas compuestas: impide que un registro de
  /// este negocio apunte al perfil de OTRO negocio.
  @@unique([negocioId, id])
  @@index([negocioId])
}

/// Perfil de barbero de un negocio.
///
/// `usuarioId` es ÚNICO POR NEGOCIO: la misma persona puede ser barbero en
/// varias barberías (y de ninguna).
model Barbero {
  id                 Int           @id @default(autoincrement())
  usuarioId          Int
  /// Negocio al que pertenece el perfil. OBLIGATORIO.
  negocioId          Int
  telefono           String
  porcentajeComision Decimal       @db.Decimal(5, 2)
  fotoUrl            String?       @db.VarChar(500)
  estado             EstadoUsuario @default(ACTIVO)

  usuario   Usuario           @relation(fields: [usuarioId], references: [id])
  negocio   Negocio           @relation(fields: [negocioId], references: [id], onDelete: Restrict)
  servicios BarberoServicio[] // <--- Conexión con la tabla intermedia

  weeklySlots  BarberWeeklySlot[]
  blocks       BarberScheduleBlock[]
  reservations Reservation[]

  @@unique([negocioId, usuarioId])
  /// Destino de las claves foráneas compuestas.
  @@unique([negocioId, id])
  @@index([negocioId])
}

/// Persona que reserva. Unifica cliente invitado y cliente autenticado (D-01/D-02):
/// - Invitado: `usuarioId = NULL` y contacto directo (`nombre` obligatorio; D-02
///   exige como mínimo nombre y número de contacto, por eso `apellido`/`telefono`
///   son opcionales en el modelo, aunque el flujo de invitado valide el teléfono).
/// - Autenticado con Google (HE-04, Modalidad B): la identidad estable es
///   el `googleId` (el `sub` del ID Token de Google). Es ÚNICO POR NEGOCIO: la
///   misma cuenta de Google puede tener fichas independientes (e historiales de
///   reservas separados) en negocios distintos.
/// - `usuarioId` es un vínculo heredado opcional, único POR NEGOCIO.
/// La autenticación de clientes NO depende de él ni crea usuarios de personal; se
/// conserva por compatibilidad con el historial existente.
/// `onDelete: SetNull`: borrar un usuario no elimina el historial de reservas.
model Cliente {
  id        Int     @id @default(autoincrement())
  nombre    String
  apellido  String?
  telefono  String?
  googleId  String?
  email     String?
  usuarioId Int?
  /// Negocio al que pertenece la ficha del cliente. OBLIGATORIO.
  negocioId Int

  usuario      Usuario?      @relation(fields: [usuarioId], references: [id], onDelete: SetNull)
  negocio      Negocio       @relation(fields: [negocioId], references: [id], onDelete: Restrict)
  reservations Reservation[]

  /// La misma identidad de Google puede tener una ficha en cada negocio.
  @@unique([negocioId, googleId])
  /// El mismo usuario puede tener ficha de cliente en varios negocios.
  @@unique([negocioId, usuarioId])
  /// Destino de las claves foráneas compuestas.
  @@unique([negocioId, id])
  @@index([negocioId])
}

enum EstadoServicio {
  ACTIVO
  INACTIVO
}

/// Servicio del catálogo de un negocio.
///
/// `nombre` es ÚNICO POR NEGOCIO: dos barberías pueden tener un servicio
/// llamado igual, pero un mismo negocio no puede repetirlo.
model Servicio {
  id              Int               @id @default(autoincrement())
  nombre          String            @db.VarChar(100)
  descripcion     String?           @db.Text
  precio          Decimal           @db.Decimal(10, 2)
  duracionMinutos Int // Fundamental para calcular los bloques de las citas (ej. 30, 45, 60 min)
  fotoUrl         String?           @db.VarChar(500) // Para el catálogo visual de clientes
  estado          EstadoServicio    @default(ACTIVO)
  /// Negocio dueño del catálogo y de los precios. OBLIGATORIO.
  negocioId       Int
  creadoEn        DateTime          @default(now())
  actualizadoEn   DateTime          @updatedAt
  barberos        BarberoServicio[] // <--- Conexión con la tabla intermedia
  reservations    Reservation[]

  negocio Negocio @relation(fields: [negocioId], references: [id], onDelete: Restrict)

  @@unique([negocioId, nombre])
  /// Destino de las claves foráneas compuestas.
  @@unique([negocioId, id])
  @@index([negocioId])
}

// Tabla intermedia explícita para la relación muchos a muchos
//
// Las relaciones son COMPUESTAS: el barbero y el servicio deben pertenecer al
// MISMO negocio que el vínculo. La base de datos lo impide, no la aplicación.
model BarberoServicio {
  barberoId  Int
  servicioId Int
  /// Negocio al que pertenece el vínculo barbero-servicio. OBLIGATORIO.
  negocioId  Int
  creadoEn   DateTime @default(now())

  barbero  Barbero  @relation(fields: [negocioId, barberoId], references: [negocioId, id], onDelete: Cascade)
  servicio Servicio @relation(fields: [negocioId, servicioId], references: [negocioId, id], onDelete: Cascade)
  negocio  Negocio  @relation(fields: [negocioId], references: [id], onDelete: Restrict)

  @@id([barberoId, servicioId]) // Llave primaria compuesta
  @@index([negocioId])
}

// ---------------------------------------------------------------------------
// HE-08: horarios, bloqueos y cierres generales
// ---------------------------------------------------------------------------

/// Día de la semana del horario semanal. Definido una sola vez y reutilizado.
enum WeekDay {
  MONDAY
  TUESDAY
  WEDNESDAY
  THURSDAY
  FRIDAY
  SATURDAY
  SUNDAY
}

/// Ciclo de vida de un bloqueo. Persiste historial: no hay borrado físico.
enum ScheduleBlockStatus {
  ACTIVE
  REACTIVATED
  CANCELLED
}

/// Motivo opcional de un bloqueo.
enum ScheduleBlockReason {
  PERSONAL
  MEDICAL
  VACATION
  OTHER
}

/// Cada registro representa una franja de 60 minutos del horario semanal.
/// La unicidad (barbero, día, hora inicial) ya actúa como índice para consultas
/// por barbero/semana; no se agrega un índice redundante sobre el prefijo.
model BarberWeeklySlot {
  id        Int      @id @default(autoincrement())
  barberoId Int
  /// Negocio al que pertenece la franja. OBLIGATORIO.
  negocioId Int
  dayOfWeek WeekDay
  startTime String   @db.VarChar(5) // HH:mm
  endTime   String   @db.VarChar(5) // HH:mm
  active    Boolean  @default(true)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  /// Relación COMPUESTA: la franja solo puede apuntar al perfil de barbero del
  /// mismo negocio.
  barbero Barbero @relation(fields: [negocioId, barberoId], references: [negocioId, id], onDelete: Cascade)
  negocio Negocio @relation(fields: [negocioId], references: [id], onDelete: Restrict)

  @@unique([barberoId, dayOfWeek, startTime])
  @@index([negocioId])
  @@map("barber_weekly_slots")
}

/// Periodos de no disponibilidad y bloqueos temporales (HE08-HU-03/HU-05/HU-06).
/// `date` es fecha de calendario (@db.Date): ver nota de zona horaria más abajo.
/// `reactivatedBy` guarda el identificador del usuario responsable sin imponer
/// integridad referencial (decisión alineada con la spec §7.4).
model BarberScheduleBlock {
  id            Int                  @id @default(autoincrement())
  barberoId     Int
  /// Negocio al que pertenece el bloqueo. OBLIGATORIO.
  negocioId     Int
  date          DateTime             @db.Date
  startTime     String               @db.VarChar(5) // HH:mm
  endTime       String               @db.VarChar(5) // HH:mm
  reason        ScheduleBlockReason?
  notes         String?              @db.Text
  status        ScheduleBlockStatus  @default(ACTIVE)
  reactivatedAt DateTime?
  reactivatedBy Int?
  createdAt     DateTime             @default(now())
  updatedAt     DateTime             @updatedAt

  /// Relación COMPUESTA: el bloqueo solo puede apuntar al perfil de barbero del
  /// mismo negocio.
  barbero Barbero @relation(fields: [negocioId, barberoId], references: [negocioId, id], onDelete: Cascade)
  negocio Negocio @relation(fields: [negocioId], references: [id], onDelete: Restrict)

  @@index([barberoId, date, status])
  @@index([negocioId])
  @@map("barber_schedule_blocks")
}

/// Cierre general (HE-08 solo lo consulta; su CRUD no pertenece a este alcance).
/// `allDay = true` cubre el día completo; con `false`, startTime/endTime son
/// obligatorios. Esa consistencia condicional se valida en DTO/servicio, no en
/// Prisma (no es una restricción portable).
model GeneralClosure {
  id        Int      @id @default(autoincrement())
  /// Negocio al que aplica el cierre. OBLIGATORIO: un cierre sin negocio
  /// aplicaría a TODOS los negocios de la plataforma.
  negocioId Int
  date      DateTime @db.Date
  startTime String?  @db.VarChar(5) // HH:mm
  endTime   String?  @db.VarChar(5) // HH:mm
  allDay    Boolean  @default(false)
  reason    String   @db.Text
  active    Boolean  @default(true)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  negocio Negocio @relation(fields: [negocioId], references: [id], onDelete: Restrict)

  @@index([date, active])
  @@index([negocioId])
  @@map("general_closures")
}

// ---------------------------------------------------------------------------
// HE-04: reservas (subconjunto de persistencia aprobado)
// ---------------------------------------------------------------------------

/// Ciclo de vida de una reserva. Política de ocupación compartida con HE-08
/// (ver `src/modules/horarios/ports/proveedor-reservas-activas.port.ts`): todo
/// estado distinto de `CANCELLED` ocupa la franja; `CANCELLED` la libera.
/// `NO_SHOW` (cliente que no asistió) también ocupa, igual que `COMPLETED`.
/// Los valores definitivos quedan sujetos a D-04 (política de estados con HE-06).
enum ReservationStatus {
  PENDING
  CONFIRMED
  IN_PROGRESS
  COMPLETED
  CANCELLED
  NO_SHOW
}

/// Una fila por reserva. Sin borrado físico: se cambia de estado, igual que
/// `BarberScheduleBlock`, para conservar historial y permitir re-reservar la
/// misma franja tras cancelar.
///
/// Alcance: campos suficientes para crear/asignar una reserva (HU-04) y para que
/// HE-08 detecte ocupación de franja. `precioReservado` conserva el precio del
/// `Servicio` calculado en el servidor al crear la reserva, para que las
/// consultas de HU-06/HU-07 no cambien si el catálogo sube de precio después.
/// Queda `NULL` para reservas creadas antes de que existiera esta columna (no se
/// inventan snapshots retroactivos). El descuento y la idempotencia siguen fuera hasta
/// resolver D-07/D-08. La duración no se persiste: se resuelve del servicio
/// vigente. El precio y la duración NUNCA se confían al cliente.
///
/// Concurrencia (D-17): la tabla incluye una columna generada `slotActivo`
/// (`1` si el estado ocupa, `NULL` si `CANCELLED`) y un índice UNIQUE
/// `(barberoId, date, startTime, slotActivo)`. Al ser `NULL` distinto de `NULL`
/// en un índice único de MySQL/MariaDB, pueden coexistir varias reservas
/// canceladas por franja, pero solo una activa; esto habilita la re-reserva.
/// `slotActivo` NO se declara aquí porque Prisma no expresa columnas generadas:
/// se crea en la migración SQL. Prisma Client funciona con o sin ella.
///
/// AISLAMIENTO (Fase 8): barbero, servicio y cliente se referencian con
/// CLAVES FORÁNEAS COMPUESTAS `(negocioId, id)`: la base de datos impide que
/// una reserva combine entidades de negocios distintos.
model Reservation {
  id                  Int               @id @default(autoincrement())
  barberoId           Int
  servicioId          Int
  clienteId           Int
  date                DateTime          @db.Date // fecha de calendario (America/Bogota)
  dayOfWeek           WeekDay // derivada de `date`; desnormalizada para la consulta semanal
  startTime           String            @db.VarChar(5) // HH:mm
  endTime             String            @db.VarChar(5) // HH:mm
  status              ReservationStatus @default(PENDING)
  // Precio del servicio aplicado al crear la reserva (calculado en el servidor).
  // `NULL` para reservas creadas antes de que existiera esta columna.
  precioReservado     Decimal?          @db.Decimal(10, 2)
  // Hash del token criptográfico de gestión para reservas de invitados.
  // Permite modificar o cancelar la reserva sin requerir inicio de sesión.
  // `NULL` para reservas creadas por clientes autenticados o anteriores a esta columna.
  //
  // El hash es la vía de VALIDACIÓN (comparación en tiempo constante, sin
  // descifrar nada). Se conserva además una copia CIFRADA del token para que
  // un reintento idempotente pueda reproducir EXACTAMENTE la respuesta
  // original: así la idempotencia nunca invalida una credencial ya entregada
  // ni devuelve un token distinto al que el cliente ya tiene.
  // NUNCA se guarda el token en texto claro.
  gestionTokenHash    String?           @db.VarChar(255)
  // Token de gestión CIFRADO (AES-256-GCM). `NULL` en las reservas de
  // cliente autenticado y en las creadas antes de esta columna.
  gestionTokenCifrado String?           @db.VarChar(255)
  // Control de recordatorio automático por WhatsApp (2 horas antes)
  recordatorioEnviado Boolean           @default(false)
  /// Negocio al que pertenece la reserva. OBLIGATORIO.
  negocioId           Int
  createdAt           DateTime          @default(now())
  updatedAt           DateTime          @updatedAt

  // Columna generada a nivel de base de datos: `1` si el estado ocupa la
  // franja, `NULL` si `CANCELLED` (ver migración). Se declara como `@db.TinyInt`
  // para que Prisma conozca la columna y su índice y no genere drift, aunque la
  // expresión generada solo exista en SQL. Prisma Client la expone como lectura.
  slotActivo Int? @db.TinyInt

  barbero        Barbero  @relation(fields: [negocioId, barberoId], references: [negocioId, id], onDelete: Restrict)
  servicio       Servicio @relation(fields: [negocioId, servicioId], references: [negocioId, id], onDelete: Restrict)
  cliente        Cliente  @relation(fields: [negocioId, clienteId], references: [negocioId, id], onDelete: Restrict)
  negocio        Negocio  @relation(fields: [negocioId], references: [id], onDelete: Restrict)
  /// Clave de idempotencia del intento de reserva (cabecera `Idempotency-Key`).
  /// NULA para las reservas históricas y para las creadas sin cabecera de
  /// idempotencia. La unicidad es COMPUESTA por negocio: la misma clave en dos
  /// barberías son dos intentos distintos, y una clave nunca permite acceder a
  /// una reserva de otro negocio.
  idempotencyKey String?  @db.VarChar(64)

  // Unicidad de franja ocupada: `slotActivo` es NULL para estados no ocupantes,
  // y NULL no colisiona en MySQL/MariaDB, de modo que varias reservas canceladas
  // coexisten y solo una activa por franja (re-reserva tras CANCELLED).
  @@unique([barberoId, date, startTime, slotActivo])
  @@unique([negocioId, idempotencyKey])
  // Consulta de ocupación por fecha concreta (método 1 del puerto HE-08).
  @@index([barberoId, date, status])
  // Consulta de ocupación recurrente sin fecha (método 2 del puerto HE-08).
  @@index([barberoId, dayOfWeek, status])
  // Enlaces de la reserva: servicios y reservas propias de un cliente.
  @@index([servicioId])
  @@index([clienteId])
  // Filtro por negocio (aislamiento multitenant).
  @@index([negocioId])
  @@map("reservations")
}

// ---------------------------------------------------------------------------
// Plantillas de mensajes dinámicos de WhatsApp
// ---------------------------------------------------------------------------
/// Plantilla de mensaje de WhatsApp.
///
/// ALCANCE (HU-11): la plantilla puede ser GLOBAL de plataforma
/// (`negocioId = NULL`) o propia de un negocio (`negocioId = X`).
///
/// REGLA DE RESOLUCIÓN: la plantilla DEL NEGOCIO tiene prioridad; si no
/// existe, se usa la plantilla GLOBAL; si tampoco existe, el texto por defecto
/// del código. Las filas globales son el VALOR POR DEFECTO de la plataforma
/// (su propósito es explícito: el texto inicial de una barbería que aún no ha
/// personalizado sus mensajes) y nunca sustituyen a la de un negocio.
///
/// `claveGlobal` es una columna GENERADA (creada en la migración SQL) que
/// contiene el `tipo` cuando la plantilla es global y `NULL` cuando es de un
/// negocio. Su índice único garantiza como máximo UNA plantilla global por
/// tipo: en MySQL/MariaDB los `NULL` de un índice único no colisionan, de
/// modo que las plantillas de negocio pueden repetirse el tipo que-sea.
model WhatsAppPlantilla {
  id          Int      @id @default(autoincrement())
  tipo        String   @db.VarChar(50) // CONFIRMACION, RECORDATORIO, etc.
  mensaje     String   @db.Text
  activo      Boolean  @default(true)
  /// Negocio al que pertenece la plantilla. `NULL` = plantilla GLOBAL de
  /// plataforma.
  negocioId   Int?
  /// Columna generada: `tipo` si la plantilla es global, `NULL` si es de un
  /// negocio. Prisma no expresa columnas generadas: se declara para que no
  /// genere drift, y la expresión solo existe en la migración SQL. Es ÚNICA:
  /// garantiza como máximo una plantilla global por tipo.
  claveGlobal String?  @unique @db.VarChar(50)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  negocio Negocio? @relation(fields: [negocioId], references: [id], onDelete: Cascade)

  @@unique([negocioId, tipo])
  @@index([negocioId])
  @@map("whatsapp_plantillas")
}

// ---------------------------------------------------------------------------
// Configuración funcional del sistema (parámetros almacenados en base de datos)
// ---------------------------------------------------------------------------

/// Tipos soportados por una configuración funcional. El contenido se guarda como
/// texto (`valor`) y se valida/parsea según este tipo al leerlo, sin `eval` ni
/// conversiones inseguras.
enum TipoConfiguracion {
  TEXTO
  NUMERO
  BOOLEANO
  JSON
}

/// Parámetro funcional de la aplicación almacenado en base de datos.
///
/// `valor` se guarda como texto para poder representar configuraciones de
/// cualquier tipo sin perder la capacidad de validarlas: `tipo` indica cómo
/// interpretar y validar el contenido al leerlo. Los secretos y credenciales NO
/// se migran aquí: permanecen en variables de entorno.
model ConfiguracionSistema {
  id            Int               @id @default(autoincrement())
  clave         String            @unique @db.VarChar(100)
  valor         String            @db.Text
  tipo          TipoConfiguracion @default(TEXTO)
  descripcion   String?           @db.VarChar(255)
  editable      Boolean           @default(true)
  creadoEn      DateTime          @default(now())
  actualizadoEn DateTime          @updatedAt

  @@map("configuraciones_sistema")
}

/// Parámetro funcional con ámbito de NEGOCIO (tenant).
///
/// Separado de `ConfiguracionSistema` (parámetros globales de plataforma):
/// aquí viven las políticas operativas de cada barbería, como el plazo de
/// antelación para cancelar o la tolerancia de NO_SHOW. El nombre de la
/// clave se reutiliza para todos los negocios, pero el VALOR es propio de
/// cada uno, y la caché de configuración debe segmentarse por `negocioId`
/// para que un negocio nunca lea el valor de otro.
///
/// La unicidad es por `(negocioId, clave)`: un mismo negocio no puede tener
/// dos filas con la misma clave, pero dos negocios sí pueden usar la misma
/// clave con valores distintos.
model ConfiguracionNegocio {
  id            Int               @id @default(autoincrement())
  negocioId     Int
  clave         String            @db.VarChar(100)
  valor         String            @db.Text
  tipo          TipoConfiguracion @default(TEXTO)
  descripcion   String?           @db.VarChar(255)
  editable      Boolean           @default(true)
  creadoEn      DateTime          @default(now())
  actualizadoEn DateTime          @updatedAt

  negocio Negocio @relation(fields: [negocioId], references: [id], onDelete: Cascade)

  @@unique([negocioId, clave])
  @@map("configuraciones_negocio")
}
`

---

<a id="06-seguridad-owasp-logs"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 06-seguridad-owasp-logs.md -->
<!-- ========================================================================= -->

# 08. Requisitos No Funcionales (RNF) y Seguridad OWASP 2025

## 8.1 Matriz de Blindaje OWASP Top 10: 2025 y Aislamiento Multitenant

* **RNF-SEC-01 (A01: Broken Access Control & Multi-Tenant Isolation):**  
  El sistema **DEBE** aplicar control de acceso con doble guardia: `ProtectedRoute` en React y `JwtAuthGuard` + `RolesGuard` en NestJS. Toda consulta y mutación a entidades operativas **DEBE** estar aislada estrictamente por `negocioId` mediante extensiones de Prisma y el middleware de contexto de inquilino. Se prohíbe que una barbería acceda a los registros o configuración de otra.
* **RNF-SEC-02 (A02: Security Misconfiguration):**  
  El backend **DEBE** inicializarse con `helmet()` configurando cabeceras de seguridad estrictas, CORS restringido a los dominios del frontend, y deshabilitación obligatoria del encabezado `X-Powered-By`. En Nginx del frontend, la directiva `Content-Security-Policy` (`frame-src`) **DEBE** autorizar explícitamente los dominios seguros de mapas (`maps.google.com`, `*.openstreetmap.org`).
* **RNF-SEC-03 (A03: Software Supply Chain Failures):**  
  Las dependencias del frontend y backend **DEBEN** mantenerse con `package-lock.json` inmutable y auditoría automatizada en CI/CD con `npm audit` exigiendo **0 vulnerabilidades de severidad alta o crítica**.
* **RNF-SEC-04 (A04: Cryptographic Failures):**  
  Las contraseñas **DEBEN** procesarse con hashing irreversible con salt (Argon2 / Bcrypt). Las sesiones **DEBEN** usar tokens JWT firmados con algoritmo HMAC-SHA256, separando tokens de personal de tokens de clientes, y canal de transporte cifrado obligatorio mediante HTTPS/TLS.
* **RNF-SEC-05 (A05: Injection):**  
  El 100% de las consultas a la base de datos **DEBEN** realizarse a través de las funciones nativas parametrizadas de Prisma ORM, prohibiendo la concatenación de cadenas en SQL. El cliente React **DEBE** escapar automáticamente el árbol DOM contra Cross-Site Scripting (XSS).
* **RNF-SEC-06 (A06: Insecure Design & Tab Isolation):**  
  La arquitectura de agendamiento para clientes invitados **DEBE** desacoplarse del login administrativo mediante tokens de gestión cifrados (`gestionTokenCifrado`). Las sesiones de navegador **DEBEN** aislarse por ruta (`token_barberia_<slug>`) impidiendo que abrir dos sedes en pestañas simultáneas sobreescriba credenciales.
* **RNF-SEC-07 (A07: Authentication Failures):**  
  La autenticación administrativa y de clientes **DEBE** integrarse con el proveedor oficial Google OAuth 2.0 (SSO) y contar con Throttler / Rate Limiting configurado en 100 peticiones por minuto por IP para mitigar ataques de fuerza bruta.
* **RNF-SEC-08 (A08: Software or Data Integrity Failures):**  
  El módulo de subida de archivos (Multer) **DEBE** verificar el tipo MIME real inspeccionando los números mágicos del archivo binario y renombrarlo aleatoriamente mediante UUIDv4 para impedir la ejecución de scripts arbitrarios en el servidor.
* **RNF-SEC-09 (A09: Security Logging and Alerting):**  
  El sistema **DEBE** registrar los eventos de auditoría en 3 archivos físicos diarios (`audit.log`, `security.log`, `error.log`) mediante Winston y despachar alertas asíncronas por correo SMTP al Superadministrador ante errores 500 y violaciones de rol 403.
* **RNF-SEC-10 (A10: Mishandling of Exceptional Conditions):**  
  El servidor **DEBE** contar con un filtro global de excepciones que atrape cualquier error no previsto, devolviendo un mensaje genérico sin exponer trazas de código (*stack traces*) y aplicando el principio *Fail-Closed* en la disponibilidad.

---

## 8.2 Rendimiento y Eficiencia
* **RNF-PERF-01:** El cálculo y entrega del listado de disponibilidad horaria de un barbero **DEBE** responder en un tiempo inferior a **200 milisegundos** bajo condiciones normales de red.
* **RNF-PERF-02:** El frontend **DEBE** utilizar TanStack Query para mantener en caché las respuestas de catálogo de servicios y disponibilidad, invalidando datos únicamente cuando ocurra una mutación (creación o cancelación de cita).

---

## 8.3 Disponibilidad y Resiliencia
* **RNF-DISP-01:** La plataforma en la nube (Railway) **DEBE** mantener una tasa de disponibilidad del **99.9%** durante las horas comerciales de la barbería (08:00 a 20:00 hora de Colombia).
* **RNF-DISP-02:** La sesión de WhatsApp Baileys **DEBE** ponerse en modo reposo (*idle*) automáticamente si no hay actividad en 60 segundos para evitar saturación de memoria en el servidor.

---

<a id="07-contratos-api-dtos"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 07-contratos-api-dtos.md -->
<!-- ========================================================================= -->

# 09. Contratos de la API REST y Especificación OpenAPI Multitenant

## 9.1 Convenciones Generales de la API
* **Base URL:** `/` (o prefijo de entorno de despliegue).
* **Cabecera de Enrutamiento de Tenant (OBLIGATORIA para rutas de sede):** `X-Negocio-Slug: <slug>`.
* **Documentación Interactiva:** Swagger UI expuesto en `/api/docs` y especificación OpenAPI en `/api/docs-json`.
* **Autenticación:** Cabecera estándar HTTP `Authorization: Bearer <token_jwt>`.

---

## 9.2 Endpoints Principales por Módulo

### 1. Directorio Global y Plataforma SaaS (`/plataforma`)
* `GET /plataforma/negocios/publico` ➔ Consulta pública y ligera de barberías activas para el Hub de exploración (sin métricas internas ni datos privados).
* `GET /plataforma/negocios` ➔ Lista administrativa de barberías con métricas completas en tiempo real (@UseGuards(PlataformaAdminGuard)).
* `POST /plataforma/negocios` ➔ Da de alta un nuevo tenant en la plataforma (@UseGuards(PlataformaAdminGuard)).
* `PATCH /plataforma/negocios/:id/estado` ➔ Activa o suspende una barbería en la plataforma (@UseGuards(PlataformaAdminGuard)).
* `POST /plataforma/negocios` ➔ Da de alta un nuevo tenant en la plataforma, inicializa su perfil y asocia atómicamente a su Superadmin fundador.
* `PATCH /plataforma/negocios/:id/estado` ➔ Activa o suspende una barbería en la plataforma (`ACTIVO` / `INACTIVO`).


### 2. Identidad y Perfil de Sede (`/perfil-negocio`)
* `GET /perfil-negocio` ➔ Consulta pública de la identidad de la sede (nombre, lema, dirección, coordenadas, radar y tema visual `temaKey`).
* `GET /perfil-negocio/gestion` ➔ Consulta administrativa del perfil para configuración del negocio.
* `PUT /perfil-negocio` ➔ Actualiza lema, dirección, coordenadas GPS (`latitud`, `longitud`) y tema visual (`temaKey`).
* `POST /perfil-negocio/recursos/:tipo` ➔ Sube archivos de marca validados (favicon, banner, logo blanco, logo negro).
* `DELETE /perfil-negocio/recursos/:tipo` ➔ Elimina un recurso de marca individual.

### 2.1 Redes Sociales Oficiales del Negocio (`/perfil-negocio/redes-sociales`) (Fase 18)
* `GET /perfil-negocio/redes-sociales` ➔ Consulta pública de las redes sociales activas (`activo: true`) ordenadas por prioridad. Admite `?todas=true` para panel administrativo (incluye redes pausadas).
* `PUT /perfil-negocio/redes-sociales` ➔ Reemplazo suave masivo (`bulk upsert`): desactiva las ausentes y crea o actualiza las presentes preservando su ID histórico.
* `PATCH /perfil-negocio/redes-sociales/:id` ➔ Actualiza parcialmente `url`, `orden` o `nombre` (este último solo para tipo `OTRO`).
* `DELETE /perfil-negocio/redes-sociales/:id` ➔ Pausa la visibilidad (`activo: false`) sin borrar el registro. Si se pasa `?definitivo=true`, ejecuta borrado físico en base de datos.
* `PATCH /perfil-negocio/redes-sociales/:id/activar` ➔ Reactiva una red previamente pausada (`activo: true`).

### 3. Autenticación de Personal y Clientes
* `POST /auth/google` ➔ Inicia sesión de personal administrativo/barberos.
* `POST /auth/refresh` ➔ Renueva el JWT del personal resolviendo membresías del tenant activo.
* `POST /auth/clientes/google` ➔ Inicia sesión de cliente final con Google OAuth. Retorna `accessToken` de cliente y ficha en ese tenant.
* `GET /auth/clientes/perfil` ➔ Consulta el perfil del cliente autenticado en la sede.
* `PATCH /auth/clientes/perfil` ➔ Actualiza nombre o teléfono del cliente.

### 4. Personal y Barberos (`/usuarios`)
* `GET /usuarios/me` ➔ Consulta perfil y membresía del usuario en la sede actual.
* `GET /usuarios/barberos` ➔ Catálogo de barberos activos del tenant.
* `POST /usuarios/barberos` ➔ Vincula un nuevo barbero a la sede con comisión pactada.
* `PATCH /usuarios/barberos/:id/comision` ➔ Actualiza la comisión del barbero para este tenant.
* `POST /usuarios/administradores` ➔ Asigna membresía de administrador a un usuario en la sede.
* `PATCH /usuarios/:id` ➔ Actualiza datos operativos del usuario en la sede. El email es inmutable a nivel de sede para prevenir account takeover.
* `PATCH /usuarios/:id/estado` ➔ Cambia el estado de membresía en la sede con parámetro obligatorio `tipo: 'administrador' | 'barbero' | 'ambos'` (no suspende la cuenta global).

### 5. Catálogo de Servicios (`/servicios`)
* `GET /servicios` ➔ Lista pública de servicios activos de la barbería con precio y duración.
* `POST /servicios` ➔ Crea un nuevo servicio para el tenant (`@Roles('SUPERADMIN', 'ADMINISTRADOR')`).
* `PATCH /servicios/:id` ➔ Modifica precio, duración o estado del servicio.
* `GET /servicios/:servicioId/barberos` ➔ Barberos del tenant habilitados para el servicio.

### 6. Horarios y Disponibilidad (`/usuarios/.../horarios`)
* `GET /usuarios/me/barbero/horario-semanal` ➔ Horario base semanal del barbero en esta sede.
* `PUT /usuarios/me/barbero/horario-semanal` ➔ Actualiza matriz de horarios semanales.
* `POST /usuarios/me/barbero/bloqueos-horario` ➔ Registra descansos o ausencias temporales.
* `GET /usuarios/barberos/:barberoId/disponibilidad?fecha=YYYY-MM-DD&servicioId=X` ➔ Franjas horarias libres de 60 minutos calculadas en tiempo real.

### 7. Reservas y Citas (`/reservas`)
* `POST /reservas` ➔ Agendamiento online (cliente autenticado o invitado). Retorna cita y `tokenGestion`.
* `POST /reservas/admin` ➔ Creación de reserva administrativa para clientes presenciales o registrados.
* `GET /reservas/me` ➔ Historial de citas del cliente autenticado en esta sede.
* `GET /reservas/barbero/me` ➔ Agenda diaria del barbero autenticado en la sede.
* `PATCH /reservas/:id/completar` ➔ Marca cita como finalizada.
* `PATCH /reservas/:id/no-show` ➔ Marca inasistencia del cliente.
* `PATCH /reservas/invitado/:id/cancelar` ➔ Cancela cita con token de gestión seguro.

---

## 9.3 Payloads JSON Canónicos (DTOs de Entrada y Salida)

Para garantizar consistencia absoluta entre Backend y Frontend, cualquier IA **DEBE replicar exactamente estos contratos**:

### 1. Alta de Nuevo Tenant: `POST /plataforma/negocios`
**Request Body:**
```json
{
  "nombre": "Barbería Elite Bogotá",
  "slug": "barberia-elite-bogota",
  "zonaHoraria": "America/Bogota",
  "superadmin": {
    "nombre": "Carlos",
    "apellido": "Gómez",
    "email": "carlos.gomez@gmail.com"
  }
}
```
**Response Body (201 Created):**
```json
{
  "id": 3,
  "nombre": "Barbería Elite Bogotá",
  "slug": "barberia-elite-bogota",
  "estado": "ACTIVO",
  "zonaHoraria": "America/Bogota",
  "superadmin": {
    "usuarioId": 12,
    "email": "carlos.gomez@gmail.com",
    "superadmin": true
  },
  "perfil": {
    "temaKey": "clasico-azul",
    "latitud": null,
    "longitud": null
  }
}
```

### 2. Actualización de Marca y Ubicación: `PUT /negocios/perfil`
*(Requiere cabecera `X-Negocio-Slug: <slug>` y token de administrador).*
**Request Body:**
```json
{
  "frasePrincipal": "El arte clásico del corte masculino",
  "temaKey": "cyber-lime",
  "direccion": "Calle 85 # 14-20",
  "ciudad": "Bogotá",
  "departamento": "Cundinamarca",
  "referencia": "Piso 2, frente al parque",
  "latitud": 4.6675200,
  "longitud": -74.0564300
}
```
**Response Body (200 OK):**
```json
{
  "id": 3,
  "negocioId": 3,
  "frasePrincipal": "El arte clásico del corte masculino",
  "temaKey": "cyber-lime",
  "direccion": "Calle 85 # 14-20",
  "ciudad": "Bogotá",
  "departamento": "Cundinamarca",
  "referencia": "Piso 2, frente al parque",
  "latitud": "4.6675200",
  "longitud": "-74.0564300",
  "updatedAt": "2026-11-02T19:00:00.000Z"
}
```

### 3. Agendamiento de Reserva: `POST /reservas`
*(Requiere cabecera `X-Negocio-Slug: <slug>`).*
**Request Body (Cliente Invitado):**
```json
{
  "barberoId": 5,
  "servicioId": 2,
  "date": "2026-11-10",
  "startTime": "10:00",
  "cliente": {
    "nombre": "Juan",
    "apellido": "Pérez",
    "telefono": "+573001234567",
    "email": "juan.perez@example.com"
  }
}
```
**Response Body (201 Created):**
```json
{
  "id": 142,
  "barberoId": 5,
  "servicioId": 2,
  "clienteId": 89,
  "date": "2026-11-10T00:00:00.000Z",
  "startTime": "10:00",
  "endTime": "11:00",
  "status": "CONFIRMED",
  "precioReservado": "35000.00",
  "tokenGestion": "a8f3b...9c2d",
  "mensaje": "Reserva creada exitosamente"
}
```

### 4. Consulta de Disponibilidad de Barbero: `GET /usuarios/barberos/:id/disponibilidad?fecha=2026-11-10&servicioId=2`
**Response Body (200 OK):**
```json
{
  "barberoId": 5,
  "fecha": "2026-11-10",
  "franjasDisponibles": [
    { "startTime": "09:00", "endTime": "10:00", "disponible": true },
    { "startTime": "10:00", "endTime": "11:00", "disponible": false, "motivo": "OCUPADO" },
    { "startTime": "11:00", "endTime": "12:00", "disponible": true },
    { "startTime": "12:00", "endTime": "13:00", "disponible": false, "motivo": "DESCANSO" },
    { "startTime": "14:00", "endTime": "15:00", "disponible": true }
  ]
}
```

---

## 9.4 Formato Estándar de Errores (JSON)
```json
{
  "statusCode": 403,
  "timestamp": "2026-11-02T19:30:00.000Z",
  "path": "/servicios",
  "message": "No tienes permisos para operar en esta barbería"
}
```
*(Se prohíbe exponer mensajes de error nativos de SQL o trazas internas de Node.js).*

---

<a id="08-integraciones"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 08-integraciones.md -->
<!-- ========================================================================= -->

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
* **Aislamiento por Sede:**
  * Cada barbería tiene su propia sesión independiente de WhatsApp.
  * Las credenciales de conexión se guardan de forma aislada en disco bajo la ruta:
    `storage/sessions/<negocioId>/`
  * La vinculación se realiza mediante código QR desde el panel de administración de la sede.
  * Plantillas de mensajes dinámicas configurables por tenant en `WhatsAppPlantilla`.

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

---

<a id="09-pruebas"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 09-pruebas.md -->
<!-- ========================================================================= -->

# 12. Estrategia de Pruebas y Aseguramiento de Calidad (QA) Multitenant

## 12.1 Pirámide de Pruebas Automatizadas
La calidad del software se garantiza mediante una estrategia multicapa que cubre pruebas unitarias, pruebas de aislamiento multi-tenant, integración y pruebas dinámicas de penetración:

```
          / \
         /   \     Pruebas DAST (OWASP ZAP: 22.866 vectores de ataque)
        / DAST\   ─────────────────────────────────────────────────────
       / AISL. \   Pruebas de Aislamiento Tenant (negocio-aislamiento.spec)
      /─────────\ ─────────────────────────────────────────────────────
     / INTEGRAC. \ Pruebas de Integración (Jest + Repositorios reales)
    / UNITARIAS   \ Pruebas Unitarias de Servicios, Guards y DTOs
   /───────────────\
```

---

## 12.2 Certificación de Pruebas Ejecutadas

### 1. Pruebas Unitarias, de Integración y Aislamiento (Jest)
* Cobertura de pruebas sobre servicios críticos:
  * `negocio-aislamiento.spec.ts` ➔ Blindaje de consultas tenant-scoped: verificación de que ninguna consulta pueda escapar del `negocioId` del contexto.
  * `perfil-negocio.service.spec.ts` ➔ Pruebas de persistencia de marca, validación de coordenadas y selección de `temaKey`.
  * `disponibilidad.service.spec.ts` ➔ Validación de franjas horarias y principio *Fail-Closed*.
  * `bloqueos-horario.service.spec.ts` ➔ Pruebas de solapamiento de descansos y vacaciones.
  * `horario-semanal.service.spec.ts` ➔ Creación y actualización de semanas laborales por sede.
  * `barberos.service.spec.ts` ➔ Gestión de comisiones por sede, fotos y membresías (46/46 tests aprobados).
  * `administradores.service.spec.ts` ➔ Asignación de Superadmin y administradores con llaves compuestas.
  * `all-exceptions.filter.spec.ts` ➔ Captura de errores 403/500 y verificación de llamadas a `AlertsService`.
  * `recordatorios.cron.spec.ts` ➔ Cron de recordatorios automáticos y enmascaramiento de PII.
* Comando de ejecución: `npm test` y `npm run test:multitenant`.

### 2. Pruebas de Seguridad en Dependencias (SCA)
* **Herramienta:** `npm audit` integrado en el pipeline de GitHub Actions (`security-audit.yml`).
* **Resultado:** **0 vulnerabilidades** reportadas tanto en `barberia-backend` como en `barberia-frontend`.

### 3. Pruebas Dinámicas de Penetración (DAST) con OWASP ZAP
* **Alcance:** Escaneo dinámico sobre la API en vivo de NestJS (`http://localhost:3000`) importando la definición OpenAPI oficial (`/api/docs-json`).
* **Métricas del Ataque:**
  * **22.866 solicitudes de ataque** lanzadas a través de 24 plugins de penetración en 04:08 minutos.
  * **3.769 ataques activos de Inyección SQL (SQLi):** 0 alertas (100% blindado por Prisma ORM).
  * **5.975 ataques de Inyección de Comandos OS:** 0 alertas (100% mitigado por validación de DTOs).
  * **5.610 ataques de Server-Side Code Injection (SSTI):** 0 alertas.
  * **Ataques de Fuerza Bruta / Inundación:** Mitigados con éxito mediante Throttler (HTTP 429 Too Many Requests).

---

<a id="10-ia-responsable-hitl"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 10-ia-responsable-hitl.md -->
<!-- ========================================================================= -->

# 14. Inteligencia Artificial Responsable, Privacidad y Protocolo HITL

## 14.1 Principios Éticos y Gobernanza de IA
El desarrollo del proyecto incorpora herramientas de asistencia de Inteligencia Artificial bajo lineamientos éticos estrictos que garantizan la confidencialidad de la información, el aislamiento multi-inquilino y la ausencia de alucinaciones en la arquitectura del sistema:

1. **Privacidad de Información Personal Identificable (PII):**
   * **Directiva:** Los datos personales de clientes y barberos (nombres completos, correos y números telefónicos) **NO DEBEN** enviarse en texto plano a modelos externos de IA ni guardarse sin protección en registros públicos.
   * **Enmascaramiento Obligatorio:** En los registros de auditoría Winston y notificaciones, los números telefónicos se ofuscan bajo el formato `318****854`.
2. **Cero Exposición de Secretos y Llaves de API:**
   * Las variables de entorno (`JWT_SECRET`, credenciales SMTP `SMTP_PASS`, client ID de Google) se encuentran estrictamente resguardadas en archivos `.env` ignorados por el control de versiones (`.gitignore`).
   * Ningún prompt enviado a agentes de IA debe contener secretos ni tokens maestros en texto visible.
3. **Protección contra Inyección de Prompts (*Prompt Injection*):**
   * Los campos de texto libre ingresados por clientes o usuarios se limpian mediante `ValidationPipe` y nunca se concatenan directamente en comandos de automatización o flujos de IA.

---

## 14.2 Protocolo de Gobernanza Human-in-the-Loop (HITL)

### 14.2.1 Definición y Principio Rector
La técnica **Human-in-the-Loop (HITL)** o *humano en el bucle* es un enfoque de inteligencia artificial que combina el aprendizaje automático y los modelos generativos con la **supervisión o intervención humana directa**. 

Su objetivo primordial es establecer un **bucle de retroalimentación continuo**: el modelo de IA realiza predicciones, propone soluciones arquitectónicas o automatiza tareas repetitivas, mientras que la persona humana **valida, corrige, refina y toma las decisiones finales en momentos críticos**.

En la Plataforma SaaS para Barberías, el paradigma HITL se implementa en dos niveles complementarios:

### 14.2.2 Nivel 1: Desarrollo Asistido y DevOps (Dev-HITL)
Gobernanza sobre el ciclo de vida del software y el código fuente:

```
  ┌────────────────────────────────────────────────────────┐
  │         BUCLE CONTINUO DE DESARROLLO (Dev-HITL)        │
  └────────────────────────────────────────────────────────┘
              │                               ▲
  1. Propone DTOs, Servicios,                 │ 2. Ejecuta tests locales,
     Controladores y Tests                    │    detecta desviaciones y refina
              ▼                               │
  ┌──────────────────────┐        ┌──────────────────────┐
  │     MODELO DE IA     │        │ DESARROLLADOR HUMANO │
  │   (Predice / Genera) │        │ (Supervisa / Corrige)│
  └──────────────────────┘        └──────────────────────┘
              │
              ▼ [Momento Crítico Detectado]
  ┌──────────────────────────────────────────────────────┐
  │           DECISIÓN FINAL EN MOMENTOS CRÍTICOS        │
  │  1. Alteración de esquemas Prisma / Migraciones SQL  │
  │  2. Asignación de roles de seguridad (RBAC / Tenants)│
  │  3. Invocación de red o comandos destructivos        │
  │  4. Publicación en Git y despliegue en producción    │
  └──────────────────────────────────────────────────────┘
              │ [Aprobación Explícita Requerida]
              ▼
        [ Entorno de Producción / Staging ]
```

### 14.2.3 Nivel 2: Dominio de Negocio y Plataforma (App-HITL)
Gobernanza dentro de la operativa de las barberías:
1. **Asistencia sin Autonomía Total:** Si la plataforma incorpora modelos predictivos (como estimación de demanda, sugerencia de franjas horarias o redacción asistida de recordatorios de WhatsApp), el sistema **NUNCA** toma acciones unilaterales de alto impacto sin confirmación.
2. **Decisiones Críticas en Manos del Staff:** En situaciones de sobrecupo, cancelaciones extraordinarias, bloqueos de agenda o excepciones en el cobro de comisiones, la decisión final recae de forma exclusiva en el **administrador o barbero humano**.
3. **Auditabilidad y Trazabilidad:** Toda acción sugerida por automatizaciones o algoritmos queda registrada en los logs de auditoría estructurados (`audit.log`) con indicación del usuario humano que autorizó la operación.

### 14.2.4 Directivas de Gobernanza HITL:
1. **La IA como Asistente Técnico:** La IA actúa como un copiloto de ingeniería enfocado en rapidez, consistencia de sintaxis y cobertura de pruebas; la responsabilidad de diseño arquitectónico y lógica de negocio permanece 100% en el desarrollador humano.
2. **Bloqueo de Modificaciones Destructivas:** La IA tiene estrictamente prohibido ejecutar o sugerir comandos de restablecimiento de base de datos destructivos (`prisma db push --force-reset` o `DROP TABLE`) en entornos compartidos o productivos.
3. **Auditoría Continua de Migraciones:** Cada columna o tabla agregada (como `temaKey` en `PerfilNegocio`) debe ser inspeccionada por el humano en su archivo SQL correspondiente antes de ejecutarse en el motor de base de datos.
4. **Ningún Push Autónomo:** Todo comando de publicación hacia repositorios remotos (`git push`) o plataformas de despliegue (Railway) requiere autorización humana previa e inequívoca.

---

<a id="11-plan-ejecucion-bootstrap"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 11-plan-ejecucion-bootstrap.md -->
<!-- ========================================================================= -->

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

---

## 15.3 Guía de Replicación Paso a Paso (Bootstrapping para la IA)

Cualquier agente de IA o ingeniero que reciba este Superprompt **DEBE seguir este orden cronológico para reconstruir el sistema funcionalmente**:

### Paso 1: Configuración de Entornos y Archivos `.env`
**1. `Barberia-Backend/.env`:**
```env
PORT=3000
NODE_ENV=development
DATABASE_URL="mysql://root:password@localhost:3306/bd_barberia_multitenant_dev"
JWT_SECRET="barber-saas-secret-key-32-chars-min-length-required"
JWT_EXPIRATION="8h"
GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"
FRONTEND_URL="http://localhost:5173"
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="alertas@barberia.com"
SMTP_PASS="app-password-16-chars"
SMTP_FROM="Alertas Plataforma <alertas@barberia.com>"
```

**2. `Barberia-Frontend/.env`:**
```env
VITE_API_BASE_URL="http://localhost:3000"
VITE_GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"
```

---

### Paso 2: Base de Datos y Prisma ORM
1. Iniciar contenedor de base de datos MySQL 8:
   ```bash
   docker run --name mysql-barberia -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=bd_barberia_multitenant_dev -p 3306:3306 -d mysql:8.0
   ```
2. Crear archivo `Barberia-Backend/prisma/schema.prisma` copiando exactamente el contenido de la **Sección 06**.
3. Generar el cliente de Prisma y correr la migración inicial:
   ```bash
   cd Barberia-Backend
   npm install
   npx prisma generate
   npx prisma migrate dev --name init_multitenant_schema
   ```

---

### Paso 3: Construcción del Backend NestJS
1. Configurar `main.ts` con seguridad perimetral:
   * `app.use(helmet({ contentSecurityPolicy: false }))` (o configurando CSP que permita OpenStreetMap y Google).
   * `app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }))`.
   * `app.useGlobalFilters(new AllExceptionsFilter(alertsService))`.
2. Registrar el middleware de tenant en `app.module.ts`:
   * Interceptar peticiones y resolver el tenant a partir de la cabecera `X-Negocio-Slug` o subdominio.
3. Crear los módulos en `src/modules/` según el árbol de la **Sección 05**, implementando los DTOs canónicos de la **Sección 09**.
4. Ejecutar pruebas unitarias para validar que el aislamiento y la lógica de citas funcionan:
   ```bash
   npm run test
   ```

---

### Paso 4: Construcción del Frontend React 19
1. Instalar dependencias core:
   ```bash
   cd ../Barberia-Frontend
   npm install react react-dom react-router-dom @tanstack/react-query axios lucide-react bootstrap
   ```
2. Crear `src/shared/lib/http/axios.ts` con los dos clientes:
   * `apiClient`: inyecta `Authorization: Bearer token_barberia_<slug>` y `X-Negocio-Slug: <slug>`.
   * `reservasApiClient`: inyecta `Authorization: Bearer cliente_token_<slug>`.
3. Crear `TenantBrandContext.tsx` que lea `temaKey` del perfil y fije el atributo `data-tenant-theme` en `document.documentElement`.
4. Configurar las rutas en `App.tsx`:
   * Raíz `/` y `/plataforma` ➔ Directorio global SaaS.
   * `/:slug` ➔ Landing de la sede con `LocationSection` (OpenStreetMap).
   * `/:slug/reservar` ➔ Wizard de agendamiento público.
   * `/:slug/dashboard` ➔ Panel administrativo protegido por membresía.

---

### Paso 5: Verificación End-to-End
1. Iniciar backend: `npm run start:dev` (puerto 3000).
2. Iniciar frontend: `npm run dev` (puerto 5173).
3. Entrar a `http://localhost:5173/plataforma`, crear una barbería de prueba (ej. `demo-barber`) y verificar que se pueda navegar a `http://localhost:5173/demo-barber` con su tema visual y mapa activos.

---



---

<a id="parte-ii-frontend"></a>

# =========================================================================
# PARTE II: ESPECIFICACIÓN DE FRONTEND (CLIENTE WEB REACT 19 & EXPERIENCIA)
# =========================================================================

# SUPERPROMPT FRONTEND - PLATAFORMA SAAS PARA BARBERIAS

> **Especificación especializada para Frontend (React 19 + Vite 6 + React Router v7 + Temas Dinámicos).**

> **ESTADO DE LA ESPECIFICACIÓN: ESPECIFICACIÓN VIVA (LIVING SPECIFICATION)**
> Este documento representa con fidelidad milimétrica el estado del sistema hasta la fase actual y continúa evolucionando activamente a medida que se completan los hitos del roadmap y las siguientes fases de desarrollo.

> - **🟢 Sprint 1 (Cimientos & Auth):** 100% Completado y Certificado.
> - **🟢 Fase Multitenant Core & Temas:** 100% Completado, Migrado y Desplegado.
> - **🟡 Sprint 2 (Citas, Horarios & OWASP):** ~85% Consolidado (En curso).
> - **⚪ Sprint 3 (Pagos, Comisiones & Switcher):** Planificado / Backlog futuro incremental.

## Índice de Contenidos

- [00. Instrucciones Ia](#00-instrucciones-ia)
- [01. Contexto Alcance](#01-contexto-alcance)
- [02. Roles Sesiones Frontend](#02-roles-sesiones-frontend)
- [03. Stack Tecnologico](#03-stack-tecnologico)
- [04. Arquitectura Rutas Slugs](#04-arquitectura-rutas-slugs)
- [05. Historias Usuario](#05-historias-usuario)
- [06. Ui Ux Temas Mapas](#06-ui-ux-temas-mapas)
- [07. Contratos Api Axios](#07-contratos-api-axios)
- [08. Pruebas](#08-pruebas)
- [09. Ia Responsable Hitl](#09-ia-responsable-hitl)
- [10. Plan Ejecucion Bootstrap](#10-plan-ejecucion-bootstrap)

---

<a id="00-instrucciones-ia"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 00-instrucciones-ia.md -->
<!-- ========================================================================= -->

# 00. Instrucciones de Ejecución, Directivas de IA y Protocolo HITL

## 0.1 Objetivo General
Este documento establece las directrices normativas y técnicas para el desarrollo, auditoría y mantenimiento del sistema **Plataforma SaaS Multitenant para Barberías (Barber SaaS Platform)**, concebida como una solución agnóstica y multi-inquilino donde cualquier establecimiento de barbería puede operar de manera autónoma (utilizando a *Kyrios Barber* como caso de estudio e inquilino piloto inicial). Cualquier agente de Inteligencia Artificial (IA) o desarrollador de software que interactúe con este repositorio **DEBE** acatar estrictamente las reglas aquí descritas para garantizar la coherencia arquitectónica, la integridad de datos, el aislamiento multi-inquilino (*tenant isolation*) y el blindaje de seguridad.

## 0.2 Terminología Normativa (RFC 2119)
* **DEBE / OBLIGATORIO (SHALL / MUST):** Indica una exigencia absoluta del sistema de ingeniería.
* **NO DEBE (MUST NOT):** Indica una prohibición absoluta por motivos de seguridad o integridad arquitectónica.
* **DEBERÍA / RECOMENDADO (SHOULD):** Indica una práctica aconsejable que solo puede omitirse con justificación técnica explícita.
* **PUEDE / OPCIONAL (MAY):** Indica una característica potestativa según los requerimientos de la fase.

## 0.3 Directivas Estrictas de Codificación
1. **TypeScript Estricto:**
   * Tanto en Backend (NestJS 11) como en Frontend (React 19), el código **DEBE** tener tipado estricto.
   * **PROHIBICIÓN:** **NO DEBE** utilizarse el tipo `any` bajo ninguna circunstancia. Toda estructura de datos debe contar con su correspondiente `interface`, `type` o `DTO`.
2. **Arquitectura y Aislamiento Multi-Tenant en NestJS:**
   * Cada módulo **DEBE** encapsular sus controladores, servicios y repositorios.
   * Toda consulta a modelos de ámbito de inquilino (*tenant-scoped*) **DEBE** estar acotada obligatoriamente por el `negocioId` del contexto de la petición (`X-Negocio-Slug` o subdominio), garantizado por el middleware de aislamiento y extensiones de Prisma.
   * La validación de entrada **DEBE** ejecutarse a través de `ValidationPipe` global con `{ whitelist: true, forbidNonWhitelisted: true, transform: true }`.
3. **Persistencia y Esquema Prisma:**
   * Ningún cambio en la base de datos **DEBE** realizarse manualmente o mediante consultas arbitrarias.
   * Todo ajuste estructural de base de datos **DEBE** ejecutarse mediante migraciones versionadas de Prisma (`npx prisma migrate dev` / `prisma migrate deploy`). Se prohíbe el uso de comandos destructivos como `db push` en producción.
4. **Seguridad Defensiva y Principio Fail-Closed:**
   * En caso de duda, falta de contexto de negocio, o inconsistencia en la verificación de reservas o disponibilidad horaria, el sistema **DEBE** "fallar cerrado" (`fail-closed`), rechazando la operación con el código HTTP correspondiente (403, 404, 409 o 503).
5. **Preservación de Pruebas y Evidencias:**
   * Todo cambio en la lógica de negocio **DEBE** respaldarse con pruebas unitarias (`*.spec.ts`) ejecutadas satisfactoriamente mediante `npm run test`.

---

## 0.4 Protocolo Operativo Human-in-the-Loop (HITL)

### 0.4.1 Marco Conceptual y Fundamento Teórico
La técnica **Human-in-the-Loop (HITL)** o *humano en el bucle* es un enfoque de inteligencia artificial (IA) que combina el aprendizaje automático y los modelos de lenguaje con la **supervisión o intervención humana directa**. 

Su objetivo primordial es crear un **bucle de retroalimentación continuo (*continuous feedback loop*)**:
1. **Automatización y Propuesta (Modelo de IA):** El agente de IA realiza predicciones, genera código TypeScript, formula DTOs, propone esquemas de base de datos o automatiza procesos técnicos repetitivos.
2. **Supervisión y Refinamiento (Humano en el Bucle):** El desarrollador humano inspecciona, valida, corrige, refina y retroalimenta al modelo con ajustes sucesivos.
3. **Decisiones Finales en Momentos Críticos:** En aquellos puntos donde un error genera impacto irreversible (migraciones de base de datos, persistencia, seguridad, autenticación y despliegue a producción), la decisión final reside **exclusivamente en la persona humana**.

```
  ┌────────────────────────────────────────────────────────┐
  │         BUCLE DE RETROALIMENTACIÓN CONTINUO (HITL)     │
  └────────────────────────────────────────────────────────┘
              │                               ▲
  1. Propuesta de Código                      │ 2. Retroalimentación,
     y Automatización                         │    Pruebas y Corrección
              ▼                               │
  ┌──────────────────────┐        ┌──────────────────────┐
  │     AGENTE DE IA     │        │ DESARROLLADOR HUMANO │
  │   (Genera / Predice) │        │ (Supervisa / Refina) │
  └──────────────────────┘        └──────────────────────┘
              │
              ▼ [Llegada a un Momento Crítico]
  ┌──────────────────────────────────────────────────────┐
  │            COMPUERTAS DE APROBACIÓN HUMANA           │
  │  • Compuerta 1: Aprobación de Plan y Arquitectura    │
  │  • Compuerta 2: Auditoría de SQL de Migraciones      │
  │  • Compuerta 3: Verificación de Tests y Calidad      │
  │  • Compuerta 4: Aprobación de Push / Despliegue      │
  └──────────────────────────────────────────────────────┘
              │ [Solo si el Humano Autoriza]
              ▼
    [ Persistencia en BD / Despliegue a Producción ]
```

### 0.4.2 Las 5 Compuertas Mandatorias de Validación Humana
1. **Compuerta 1 (Plan & Arquitectura):** La IA **DEBE** plantear el diagnóstico y el plan de modificación antes de alterar código sustancial. El desarrollador valida el alcance.
2. **Compuerta 2 (Revisión de Código / Diff):** El humano audita línea por línea los cambios propuestos (`git diff`) para descartar regresiones o violaciones al aislamiento multi-inquilino.
3. **Compuerta 3 (Calidad & Tests):** Ningún cambio se considera terminado hasta que el humano ejecute y verifique las suites unitarias (`npm test`) y de compilación (`npm run build`).
4. **Compuerta 4 (Control de Migraciones SQL):** Ninguna migración de base de datos (`prisma migrate dev` o `prisma migrate deploy`) se ejecuta sin que el humano haya revisado y aprobado el archivo SQL generado (`migration.sql`). Se prohíbe `db push` destructivo.
5. **Compuerta 5 (Control de Red y Despliegue):** La IA **NO DEBE** ejecutar `git push`, interactuar con redes externas sin permiso, ni desplegar directamente a Railway/producción. Toda acción de publicación requiere autorización explícita del humano en la terminal.

---

<a id="01-contexto-alcance"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 01-contexto-alcance.md -->
<!-- ========================================================================= -->

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

---

<a id="02-roles-sesiones-frontend"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 02-roles-sesiones-frontend.md -->
<!-- ========================================================================= -->

# 03. Matriz de Roles, Permisos y Control de Acceso Multitenant (RBAC)

## 3.1 Desacoplamiento: Persona Global vs. Membresías por Sede
El sistema implementa un modelo de Control de Acceso Basado en Roles (RBAC) desacoplado, donde la identidad humana es global pero los permisos se ejercen exclusivamente dentro de la barbería en curso:

```
                      ┌────────────────────────────┐
                      │    Usuario (Global)        │
                      │  id, email, googleId, ...  │
                      └──────────────┬─────────────┘
                                     │
           ┌─────────────────────────┼─────────────────────────┐
           ▼                         ▼                         ▼
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│    Administrador     │  │       Barbero        │  │       Cliente        │
│ negocioId, usuarioId │  │ negocioId, usuarioId │  │ negocioId, usuarioId │
│ superadmin: boolean  │  │ comision, fotoUrl... │  │ citas, historial...  │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

1. **`SUPERADMIN` (Por Sede / Membresía):**
   * Es un administrador con el atributo `superadmin: true` en la tabla `Administrador` para un `negocioId` determinado.
   * Responsable de la creación y gestión de otros administradores en esa sede, configuración de identidad de marca, horarios del local y auditoría.
   * **Alcance:** Un usuario puede ser Superadmin en la Barbería A y no tener acceso o ser simplemente un barbero en la Barbería B.
2. **`ADMINISTRADOR` (Por Sede):**
   * Gestiona el día a día de esa barbería específica.
   * Gestiona servicios, da de alta o suspende barberos, consulta reservas globales de la sede, registra citas presenciales y vincula el dispositivo WhatsApp del local.
   * **Restricción:** No puede crear otros administradores ni alterar la cuenta de un Superadmin de la sede.
3. **`BARBERO` (Por Sede):**
   * Personal técnico vinculado a una barbería mediante `Barbero` `@@unique([negocioId, usuarioId])`.
   * Consulta su agenda de citas asignadas, actualiza el estado de sus turnos (`COMPLETADA`, `CANCELADA`, `NO_SHOW`), define su horario semanal y bloqueos de descanso.
   * **Restricción (BOLA/IDOR):** No tiene autorización para consultar citas, comisiones ni datos de otros barberos ni de otras barberías.
4. **`CLIENTE` (Registrado o Invitado):**
   * **Modalidad Autenticado:** Inicia sesión con Google OAuth o credenciales de cliente; sus reservas se asocian a su ficha de cliente en esa sede (`@@unique([negocioId, usuarioId])` o `@@unique([negocioId, googleId])`).
   * **Modalidad Invitado:** Agenda únicamente con nombre, teléfono y correo; recibe un token de gestión cifrado (`gestionTokenCifrado`) que le permite consultar o cancelar su reserva sin contraseña.

---

## 3.2 Matriz RACI de Permisos por Módulo (Aislada por Tenant)

| Módulo / Funcionalidad | SUPERADMIN (Sede) | ADMINISTRADOR (Sede) | BARBERO (Sede) | CLIENTE (Sede) |
|---|:---:|:---:|:---:|:---:|
| **Crear / Desactivar Administradores de la Sede** | **R / A** | ❌ | ❌ | ❌ |
| **Configurar Perfil, Marca y Tema Visual** | **R / A** | **R** | ❌ | ❌ |
| **Gestionar Barberos y Comisiones** | **A** | **R** | ❌ | ❌ |
| **Gestionar Catálogo de Servicios del Negocio** | **A** | **R** | **C** | **I** |
| **Configurar Horario y Bloqueos Propios** | **A** | **A** | **R** (Solo propios) | ❌ |
| **Consultar Agenda de Citas de la Sede** | **I** (Global sede) | **R** (Global sede) | **R** (Solo propias) | **I** (Solo suyas) |
| **Cambiar Estado de Cita** | **A** | **A** | **R** (Sus turnos) | ❌ |
| **Agendar Cita** | **A** | **R** (Presencial) | ❌ | **R** (Online) |
| **Cancelar Cita** | **A** | **R** | **R** | **R** (Con token/dueño) |
| **Revisar Logs de Auditoría del Negocio** | **R / A** | ❌ | ❌ | ❌ |
| **Configurar WhatsApp del Local** | **A** | **R** | ❌ | ❌ |

*(Convención RACI: **R** = Responsable de ejecutar, **A** = Aprobador final, **C** = Consultado, **I** = Informado / Lectura).*

---

## 3.3 Mecanismo de Aplicación en el Código
* **Frontend:** Rutas protegidas mediante componentes `ProtectedRoute` que verifican tanto la validez del token de la sede activa (`token_barberia_<slug>`) como el rol de membresía en esa sede antes de renderizar la vista.
* **Backend:**
  * **Verificación de Inquilino:** `NegocioContextoService` extrae el `negocioId` a partir del slug recibido en la cabecera `X-Negocio-Slug` o subdominio.
  * **Verificación de Identidad:** `JwtAuthGuard` valida el JWT del personal o del cliente.
  * **Verificación de Roles:** `RolesGuard` inspecciona los roles de membresía asociados al `negocioId` activo.

---

<a id="03-stack-tecnologico"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 03-stack-tecnologico.md -->
<!-- ========================================================================= -->

# 04. Stack Tecnológico y Convenciones de Ingeniería

## 4.1 Tecnologías del Backend (API REST Multitenant)
* **Lenguaje:** TypeScript 5.7+ con compilación estricta (`strict: true`, `noImplicitAny: true`).
* **Framework:** NestJS 11.0 (Arquitectura orientada a módulos, controladores e inyección de dependencias).
* **ORM:** Prisma ORM 7.0 con extensiones de cliente personalizadas (`$extends`) para inyección automática de filtros de aislamiento por `negocioId`.
* **Motor de Base de Datos:** MariaDB 11.4 / MySQL 8.0 (Almacenamiento relacional compatible con transacciones ACID y claves compuestas foráneas).
* **Seguridad Perimetral:**
  * `helmet` v8.0.0 (Inyección de cabeceras de seguridad HTTP, CSP adaptado para iframes de mapas).
  * `@nestjs/throttler` v6.4.0 (Rate Limiting defensivo anti fuerza bruta).
  * `argon2` y `bcrypt` (Hashing criptográfico irreversible con salt para credenciales y tokens de gestión).
  * `@nestjs/jwt` (Generación y verificación de tokens de sesión HMAC-SHA256 con separación de roles de personal y clientes).
* **Observabilidad y Alertas:**
  * `nest-winston` + `winston-daily-rotate-file` (Registro rotativo en `audit.log`, `security.log` y `error.log`).
  * `@nestjs-modules/mailer` + `nodemailer` (Despacho de alertas SMTP a Google Gmail ante fallos 403 y 500).
* **Integraciones:**
  * `@whiskeysockets/baileys` (Integración con protocolo oficial WhatsApp Web con sesiones multi-tenant en disco).
  * `google-auth-library` (Validación criptográfica de tokens emitidos por Google Identity Services).

## 4.2 Tecnologías del Frontend (Cliente Web Multitenant)
* **Librería Core:** React 19.0 con TypeScript 5.8+.
* **Empaquetador y Servidor:** Vite 6.2 (Compilación modular basada en ESM y recarga rápida HMR) + Nginx en contenedor de producción.
* **Enrutamiento:** React Router DOM v7 (Manejo de rutas dinámicas prefijadas por sede `/:slug/...` y rutas globales `/plataforma`).
* **Manejo de Estado del Servidor:** TanStack Query v5 (Caché reactiva, invalidación automática tras mutaciones).
* **Clientes HTTP:**
  * `apiClient` (Axios 1.7): Interceptor con `Authorization: Bearer <token_barberia_slug>` y cabecera `X-Negocio-Slug: <slug>` para administración y catálogo.
  * `reservasApiClient` (Axios 1.7): Interceptor con `Authorization: Bearer <cliente_token_slug>` para el portal de clientes autenticados.
* **Estilos y Theming Dinámico:**
  * CSS Variables reactivas inyectadas por `TenantBrandContext` (`data-tenant-theme="clasico-azul" | "cyber-lime" | "oro-vip" | ...`).
  * Mapas embebidos con OpenStreetMap (filtro CSS Dark Mode) e integración a Google Maps.
* **Iconografía:** Lucide React.

## 4.3 Convenciones de Código y Estructura
1. **Nomenclatura de Archivos:** `kebab-case.tipo.ts` (Ej: `reservas.controller.ts`, `reservas.service.ts`, `reservas.repository.ts`).
2. **DTOs Obligatorios:** Toda petición POST, PUT o PATCH **DEBE** contar con su DTO de entrada tipado con decoradores de `class-validator` (`@IsString()`, `@IsInt()`, `@Min()`, `@IsEmail()`, etc.).
3. **Manejo de Respuestas:** El backend **DEBE** estructurar sus respuestas exitosas bajo un esquema JSON claro, y en caso de error **DEBE** responder con el formato estándar `{ statusCode, timestamp, path, message }` garantizado por el filtro global de excepciones.

---

<a id="04-arquitectura-rutas-slugs"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 04-arquitectura-rutas-slugs.md -->
<!-- ========================================================================= -->

# 05. Arquitectura del Sistema y Patrones de Diseño Multitenant

## 5.1 Estilo Arquitectónico Global
La plataforma adopta una **Arquitectura Cliente-Servidor Desacoplada (Decoupled Client-Server Architecture)** con soporte nativo **Multi-Tenant (SaaS)** y comunicación sin estado (*stateless*) mediante API REST sobre HTTP/HTTPS:

```
[ Cliente Web (React 19 SPA) ]
  ├── Ruta: /:slug/... (Portal Sede)
  └── Ruta: /plataforma (Directorio SaaS)
              │
              ▼ (HTTPS / JSON / JWT + X-Negocio-Slug)
[ Middleware de Aislamiento de Inquilinos (Tenant Context) ]
              │
              ▼ (Contexto NegocioId inyectado en Request)
[ Capa de Controladores (REST Controllers) ]
              │
              ▼ (Guards, Pipes & Interceptors)
[ Capa de Servicios de Dominio (Business Services) ]
              │
              ▼ (Extensión de Prisma con Filtro Automático negocioId)
[ Capa de Repositorios (Data Access Layer) ]
              │
              ▼ (Claves Foráneas Compuestas)
[ Motor Prisma ORM 7 ➔ Base de Datos MySQL / MariaDB ]
```

## 5.2 Patrones de Diseño Aplicados en el Sistema

1. **Patrón de Aislamiento Multi-Inquilino (Tenant Isolation Pattern):**
   * **Resolución de Inquilino:** `NegocioContextoService` extrae el negocio a partir de la cabecera `X-Negocio-Slug` o el subdominio.
   * **Blindaje en ORM:** Las consultas a modelos tenant-scoped se filtran automáticamente por `negocioId`. No es posible que una barbería consulte ni altere registros de otra.
2. **Patrón Path-Prefix Multitenancy en Frontend:**
   * Las rutas del frontend se prefijan con el slug de la barbería (`/:slug/dashboard`, `/:slug/reservar`, `/:slug/catalogo`).
   * Axios extrae automáticamente el slug de la URL mediante `obtenerNegocioSlugActivo()` y lo envía en la cabecera `X-Negocio-Slug`.
3. **Aislamiento de Sesiones por Pestaña (Tab Session Isolation):**
   * Los tokens JWT y perfiles se almacenan con claves compuestas en almacenamiento de sesión: `token_barberia_<slug>` y `cliente_token_<slug>`.
   * Un usuario puede tener abiertas múltiples pestañas administrando sedes distintas simultáneamente sin colisión de estado.
4. **Patrón Repositorio (Repository Pattern):**
   * Desacopla la lógica de negocio pura de las consultas de persistencia a la base de datos (`reservas.repository.ts`, `usuarios.repository.ts`, `perfil-negocio.repository.ts`, etc.).
5. **Patrón Adaptador y Puertos (Ports & Adapters):**
   * En el módulo de horarios se implementó el puerto `ProveedorReservasActivas` (`proveedor-reservas-activas.port.ts`), desacoplando el cálculo de disponibilidad de la implementación física del módulo de reservas.
6. **Patrón Estrategia (Strategy Pattern):**
   * Utilizado en la validación de disponibilidad horaria mediante `ReglaDisponibilidadStrategy` y `ReservaActivaRule`. Cada restricción de horario (bloqueo por almuerzo, día de descanso, cita ocupada) se evalúa como una estrategia independiente.
7. **Patrón Filtro Global de Excepciones (Exception Filter Pattern):**
   * Centralizado en `all-exceptions.filter.ts`. Intercepta cualquier excepción HTTP o fallo interno no capturado, homogeneizando el JSON de salida y disparando el subsistema de alertas SMTP de seguridad.
8. **Principio de Falla Cerrada (Fail-Closed):**
   * Si el proveedor de reservas o el contexto de negocio no responden o son inválidos, el sistema **DEBE** rechazar la consulta (con 403 o 503) en lugar de responder datos vacíos o franjas abiertas a ciegas.
9. **Patrón Máquina de Estados Finita:**
   * Gestiona el ciclo de vida de una cita:
     * `PENDIENTE` ➔ `CONFIRMADA`
     * `CONFIRMADA` ➔ `COMPLETADA`
     * `CONFIRMADA` ➔ `CANCELADA`
     * `CONFIRMADA` ➔ `NO_SHOW` (Inasistencia tras tolerancia)

---

## 5.3 Árbol Estructural Canónico del Repositorio

Cualquier IA o desarrollador que reconstruya el sistema **DEBE estructurar el código en las siguientes rutas y módulos**:

```
Barberia-Backend/
├── prisma/
│   ├── schema.prisma                  # Esquema Prisma canónico
│   └── migrations/                    # Historial de migraciones SQL versionadas
├── src/
│   ├── main.ts                        # Bootstrap NestJS con Helmet, Throttler, ValidationPipe
│   ├── app.module.ts                  # Registro raíz de módulos y middleware de inquilinos
│   ├── auth/                          # Autenticación JWT, Google OAuth, Guards y Decoradores
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── guards/                    # JwtAuthGuard, RolesGuard
│   │   └── decorators/                # @Roles(), @CurrentUser()
│   ├── common/
│   │   ├── filters/                   # all-exceptions.filter.ts
│   │   ├── middleware/                # tenant-context.middleware.ts (resuelve X-Negocio-Slug)
│   │   └── guards/                    # tenant.guard.ts
│   ├── prisma/
│   │   ├── prisma.service.ts          # Conexión Prisma y extensiones de aislamiento
│   │   └── prisma.module.ts
│   └── modules/
│       ├── alerts/                    # Alertas SMTP de seguridad inmediata
│       ├── configuracion/             # Políticas operativas del tenant (cancelación, no-show)
│       ├── horarios/                  # Motor de disponibilidad, cálculo de slots de 60m
│       ├── negocios/                  # Directorio SaaS, onboarding POST /plataforma/negocios
│       ├── perfil-negocio/            # Identidad visual (temaKey), coordenadas GPS, logos
│       ├── reservas/                  # Agendamiento, máquina de estados, token de gestión
│       ├── servicios/                 # Catálogo de servicios por sede
│       ├── usuarios/                  # Personal (Administradores, Barberos, comisiones)
│       └── whatsapp/                  # Baileys WhatsApp multi-tenant en disco
└── test/                              # Suites e2e y pruebas de integración

Barberia-Frontend/
├── src/
│   ├── main.tsx                       # Bootstrap React 19 con QueryClient y BrowserRouter
│   ├── App.tsx                        # Rutas dinámicas /:slug, /plataforma, ErrorBoundary
│   ├── auth/
│   │   ├── context/AuthContext.tsx    # Sesión de personal administrativo y barbero
│   │   └── services/authService.ts
│   ├── config/
│   │   └── tenantTheme.ts             # Paletas de temas ('clasico-azul', 'cyber-lime', etc.)
│   ├── features/
│   │   ├── negocio/
│   │   │   ├── context/TenantBrandContext.tsx  # Inyección de tema visual (data-tenant-theme)
│   │   │   └── pages/ConfiguracionNegocioPage.tsx
│   │   ├── reservas/
│   │   │   ├── pages/ReservaClientePage.tsx    # Wizard público de reserva
│   │   │   ├── pages/ClientePortalPage.tsx     # Portal cliente autenticado
│   │   │   └── pages/ReservaGestionInvitadoPage.tsx # Gestión de cita vía token hash
│   │   ├── barberos/                  # Gestión de personal y comisiones
│   │   ├── servicios/                 # Gestión del catálogo de servicios
│   │   ├── horarios/                  # Gestión de matriz horaria y bloqueos
│   │   └── whatsapp/                  # Vinculación QR multi-tenant
│   ├── pages/
│   │   ├── Home/                      # Landing pública por barbería (/:slug)
│   │   │   └── components/LocationSection.tsx  # Mapa OpenStreetMap con modo oscuro y GPS
│   │   ├── Dashboard/                 # Panel administrativo por sede
│   │   ├── Plataforma/                # Hub global SaaS (/plataforma y /)
│   │   └── Login/                     # Inicio de sesión con Google SSO
│   └── shared/
│       ├── lib/http/axios.ts          # Clientes Axios duales (apiClient y reservasApiClient)
│       ├── layout/                    # MainLayout, Header, Sidebar
│       └── components/                # ProtectedRoute, ErrorBoundary
```

---

<a id="05-historias-usuario"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 05-historias-usuario.md -->
<!-- ========================================================================= -->

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

---

<a id="06-ui-ux-temas-mapas"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 06-ui-ux-temas-mapas.md -->
<!-- ========================================================================= -->

# 11. Interfaz de Usuario (UI) y Experiencia de Usuario Multitenant (UX)

## 11.1 Filosofía de Diseño y Theming Dinámico
La plataforma implementa un diseño contemporáneo en Modo Oscuro (*Dark Mode*) con soporte para **personalización estética de marca en tiempo real por sede**:

* **Sistema de Temas Dinámicos (`data-tenant-theme`):**
  * Cada barbería elige su tema visual en la configuración del negocio, el cual se persiste en base de datos (`PerfilNegocio.temaKey`).
  * `TenantBrandContext` detecta el tema activo e inyecta dinámicamente las variables CSS en el elemento raíz:
    * `clasico-azul`: Azul Zafiro corporativo (Preset Clásico Tradicional · `#0071BC`).
    * `cyber-lime`: Verde neón eléctrico urbano con estética deportiva (`#22c55e`).
    * `oro-vip`: Dorado Champagne vintage de alta gama (`#D4AF37`).
    * `sunset-amber`: Naranja sunset cálido (`#ff6b35`).
    * `midnight-cyan`: Azul medianoche con cian eléctrico neón (`#00d2ff`).
    * `crimson-velvet`: Rojo carmesí rubí y terciopelo oscuro (`#ef233c`).
    * `monochrome-noir`: Minimalismo nórdico blanco y negro de alto contraste (`#ffffff`).

* **Componente de Ubicación con Radar Pulsante:**
  * Mapa embebido con filtro CSS dark mode.
  * Baliza de radar luminosa pulsante centrada en las coordenadas de la sede, reactiva al color primario del tema (`--tenant-color-primario`).
  * Tarjeta flotante glassmorphism con estado de sede en vivo y botón directo a Google Maps.

---

## 11.2 Principales Flujos de Usuario (User Journeys)

### 1. Flujo de Agendamiento Autónomo del Cliente (`/:slug/reservar`)
1. **Paso 1 · Catálogo de Servicios:** Tarjetas de servicios del tenant con imagen, precio y duración.
2. **Paso 2 · Selección de Profesional:** Barberos de esa sede habilitados para el servicio.
3. **Paso 3 · Calendario y Horas Libres:** Consulta de disponibilidad en tiempo real con franjas libres de 60 min.
4. **Paso 4 · Datos y Confirmación:** Agendamiento como invitado o con inicio de sesión Google, con generación inmediata de token de gestión y comprobante digital.

### 2. Portal del Cliente (`/:slug/cliente/mi-cuenta`)
* Historial de citas pasadas y turnos próximos en esa barbería.
* Reprogramación o cancelación con un clic sin necesidad de recordar contraseñas.

### 3. Panel Operativo del Barbero (`/:slug/dashboard`)
* Tarjetas diarias con las citas asignadas ordenadas cronológicamente.
* Acciones de 1 clic: "Marcar como Completada" o "No Asistió".

### 4. Configuración del Negocio y Pestañas SaaS (`/:slug/configuracion`)
* **Pestaña 1 · Información Comercial y Ubicación:**
  * Asistente GPS interactivo ("📍 Usar mi ubicación actual" mediante `navigator.geolocation`).
  * Extractor inteligente de enlaces de Google Maps y coordenadas decimales.
  * Formulario de dirección oficial, ciudad, departamento y referencia de llegada.
* **Pestaña 2 · Diseño y Recursos de Marca:**
  * Selector interactivo de temas visuales con persistencia en backend (`temaKey`).
  * Gestión física y previsualización de Banner principal (PNG) y logos vectoriales (SVG).
* **Pestaña 3 · Redes Sociales Oficiales (Fase 18):**
  * Selector visual con logos vectoriales oficiales (Instagram, WhatsApp, TikTok, Facebook, Otro).
  * Validación preventiva de duplicados con badge `Conectada`.
  * Interruptor de visibilidad (`Visible / Oculta`) para pausar canales sin perder su URL.
  * Botón de eliminación física con confirmación contextual (`ConfirmDialog`).
  * Live Preview de píldora de clientes y botón "Pegar enlace".
* **Integración en Portal Público:**
  * Pie de página (`HomeFooter.tsx`) y contexto de marca (`TenantBrandContext.tsx`) renderizan automáticamente las redes activas del tenant con enlaces seguros.

### 5. Directorio Global y Onboarding (`/plataforma` y `/explorar`)
* Vista de todas las barberías activas en el sistema con métricas globales.
* Modal para registrar nuevas sedes con asignación atómica de Superadmin fundador.

---

## 11.3 Criterios de Accesibilidad y Responsividad
* **Mobile-First:** El 85% de los clientes agenda desde dispositivos móviles; todas las áreas táctiles cuentan con un mínimo de 48x48 píxeles.
* **Feedback Inmediato:** Indicadores visuales con spinners (`KyriosSpinner`) y notificaciones *Toast* para confirmar operaciones sin recargas completas.

---

<a id="07-contratos-api-axios"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 07-contratos-api-axios.md -->
<!-- ========================================================================= -->

# 09. Contratos de la API REST y Especificación OpenAPI Multitenant

## 9.1 Convenciones Generales de la API
* **Base URL:** `/` (o prefijo de entorno de despliegue).
* **Cabecera de Enrutamiento de Tenant (OBLIGATORIA para rutas de sede):** `X-Negocio-Slug: <slug>`.
* **Documentación Interactiva:** Swagger UI expuesto en `/api/docs` y especificación OpenAPI en `/api/docs-json`.
* **Autenticación:** Cabecera estándar HTTP `Authorization: Bearer <token_jwt>`.

---

## 9.2 Endpoints Principales por Módulo

### 1. Directorio Global y Plataforma SaaS (`/plataforma`)
* `GET /plataforma/negocios/publico` ➔ Consulta pública y ligera de barberías activas para el Hub de exploración (sin métricas internas ni datos privados).
* `GET /plataforma/negocios` ➔ Lista administrativa de barberías con métricas completas en tiempo real (@UseGuards(PlataformaAdminGuard)).
* `POST /plataforma/negocios` ➔ Da de alta un nuevo tenant en la plataforma (@UseGuards(PlataformaAdminGuard)).
* `PATCH /plataforma/negocios/:id/estado` ➔ Activa o suspende una barbería en la plataforma (@UseGuards(PlataformaAdminGuard)).
* `POST /plataforma/negocios` ➔ Da de alta un nuevo tenant en la plataforma, inicializa su perfil y asocia atómicamente a su Superadmin fundador.
* `PATCH /plataforma/negocios/:id/estado` ➔ Activa o suspende una barbería en la plataforma (`ACTIVO` / `INACTIVO`).


### 2. Identidad y Perfil de Sede (`/perfil-negocio`)
* `GET /perfil-negocio` ➔ Consulta pública de la identidad de la sede (nombre, lema, dirección, coordenadas, radar y tema visual `temaKey`).
* `GET /perfil-negocio/gestion` ➔ Consulta administrativa del perfil para configuración del negocio.
* `PUT /perfil-negocio` ➔ Actualiza lema, dirección, coordenadas GPS (`latitud`, `longitud`) y tema visual (`temaKey`).
* `POST /perfil-negocio/recursos/:tipo` ➔ Sube archivos de marca validados (favicon, banner, logo blanco, logo negro).
* `DELETE /perfil-negocio/recursos/:tipo` ➔ Elimina un recurso de marca individual.

### 2.1 Redes Sociales Oficiales del Negocio (`/perfil-negocio/redes-sociales`) (Fase 18)
* `GET /perfil-negocio/redes-sociales` ➔ Consulta pública de las redes sociales activas (`activo: true`) ordenadas por prioridad. Admite `?todas=true` para panel administrativo (incluye redes pausadas).
* `PUT /perfil-negocio/redes-sociales` ➔ Reemplazo suave masivo (`bulk upsert`): desactiva las ausentes y crea o actualiza las presentes preservando su ID histórico.
* `PATCH /perfil-negocio/redes-sociales/:id` ➔ Actualiza parcialmente `url`, `orden` o `nombre` (este último solo para tipo `OTRO`).
* `DELETE /perfil-negocio/redes-sociales/:id` ➔ Pausa la visibilidad (`activo: false`) sin borrar el registro. Si se pasa `?definitivo=true`, ejecuta borrado físico en base de datos.
* `PATCH /perfil-negocio/redes-sociales/:id/activar` ➔ Reactiva una red previamente pausada (`activo: true`).

### 3. Autenticación de Personal y Clientes
* `POST /auth/google` ➔ Inicia sesión de personal administrativo/barberos.
* `POST /auth/refresh` ➔ Renueva el JWT del personal resolviendo membresías del tenant activo.
* `POST /auth/clientes/google` ➔ Inicia sesión de cliente final con Google OAuth. Retorna `accessToken` de cliente y ficha en ese tenant.
* `GET /auth/clientes/perfil` ➔ Consulta el perfil del cliente autenticado en la sede.
* `PATCH /auth/clientes/perfil` ➔ Actualiza nombre o teléfono del cliente.

### 4. Personal y Barberos (`/usuarios`)
* `GET /usuarios/me` ➔ Consulta perfil y membresía del usuario en la sede actual.
* `GET /usuarios/barberos` ➔ Catálogo de barberos activos del tenant.
* `POST /usuarios/barberos` ➔ Vincula un nuevo barbero a la sede con comisión pactada.
* `PATCH /usuarios/barberos/:id/comision` ➔ Actualiza la comisión del barbero para este tenant.
* `POST /usuarios/administradores` ➔ Asigna membresía de administrador a un usuario en la sede.
* `PATCH /usuarios/:id` ➔ Actualiza datos operativos del usuario en la sede. El email es inmutable a nivel de sede para prevenir account takeover.
* `PATCH /usuarios/:id/estado` ➔ Cambia el estado de membresía en la sede con parámetro obligatorio `tipo: 'administrador' | 'barbero' | 'ambos'` (no suspende la cuenta global).

### 5. Catálogo de Servicios (`/servicios`)
* `GET /servicios` ➔ Lista pública de servicios activos de la barbería con precio y duración.
* `POST /servicios` ➔ Crea un nuevo servicio para el tenant (`@Roles('SUPERADMIN', 'ADMINISTRADOR')`).
* `PATCH /servicios/:id` ➔ Modifica precio, duración o estado del servicio.
* `GET /servicios/:servicioId/barberos` ➔ Barberos del tenant habilitados para el servicio.

### 6. Horarios y Disponibilidad (`/usuarios/.../horarios`)
* `GET /usuarios/me/barbero/horario-semanal` ➔ Horario base semanal del barbero en esta sede.
* `PUT /usuarios/me/barbero/horario-semanal` ➔ Actualiza matriz de horarios semanales.
* `POST /usuarios/me/barbero/bloqueos-horario` ➔ Registra descansos o ausencias temporales.
* `GET /usuarios/barberos/:barberoId/disponibilidad?fecha=YYYY-MM-DD&servicioId=X` ➔ Franjas horarias libres de 60 minutos calculadas en tiempo real.

### 7. Reservas y Citas (`/reservas`)
* `POST /reservas` ➔ Agendamiento online (cliente autenticado o invitado). Retorna cita y `tokenGestion`.
* `POST /reservas/admin` ➔ Creación de reserva administrativa para clientes presenciales o registrados.
* `GET /reservas/me` ➔ Historial de citas del cliente autenticado en esta sede.
* `GET /reservas/barbero/me` ➔ Agenda diaria del barbero autenticado en la sede.
* `PATCH /reservas/:id/completar` ➔ Marca cita como finalizada.
* `PATCH /reservas/:id/no-show` ➔ Marca inasistencia del cliente.
* `PATCH /reservas/invitado/:id/cancelar` ➔ Cancela cita con token de gestión seguro.

---

## 9.3 Payloads JSON Canónicos (DTOs de Entrada y Salida)

Para garantizar consistencia absoluta entre Backend y Frontend, cualquier IA **DEBE replicar exactamente estos contratos**:

### 1. Alta de Nuevo Tenant: `POST /plataforma/negocios`
**Request Body:**
```json
{
  "nombre": "Barbería Elite Bogotá",
  "slug": "barberia-elite-bogota",
  "zonaHoraria": "America/Bogota",
  "superadmin": {
    "nombre": "Carlos",
    "apellido": "Gómez",
    "email": "carlos.gomez@gmail.com"
  }
}
```
**Response Body (201 Created):**
```json
{
  "id": 3,
  "nombre": "Barbería Elite Bogotá",
  "slug": "barberia-elite-bogota",
  "estado": "ACTIVO",
  "zonaHoraria": "America/Bogota",
  "superadmin": {
    "usuarioId": 12,
    "email": "carlos.gomez@gmail.com",
    "superadmin": true
  },
  "perfil": {
    "temaKey": "clasico-azul",
    "latitud": null,
    "longitud": null
  }
}
```

### 2. Actualización de Marca y Ubicación: `PUT /negocios/perfil`
*(Requiere cabecera `X-Negocio-Slug: <slug>` y token de administrador).*
**Request Body:**
```json
{
  "frasePrincipal": "El arte clásico del corte masculino",
  "temaKey": "cyber-lime",
  "direccion": "Calle 85 # 14-20",
  "ciudad": "Bogotá",
  "departamento": "Cundinamarca",
  "referencia": "Piso 2, frente al parque",
  "latitud": 4.6675200,
  "longitud": -74.0564300
}
```
**Response Body (200 OK):**
```json
{
  "id": 3,
  "negocioId": 3,
  "frasePrincipal": "El arte clásico del corte masculino",
  "temaKey": "cyber-lime",
  "direccion": "Calle 85 # 14-20",
  "ciudad": "Bogotá",
  "departamento": "Cundinamarca",
  "referencia": "Piso 2, frente al parque",
  "latitud": "4.6675200",
  "longitud": "-74.0564300",
  "updatedAt": "2026-11-02T19:00:00.000Z"
}
```

### 3. Agendamiento de Reserva: `POST /reservas`
*(Requiere cabecera `X-Negocio-Slug: <slug>`).*
**Request Body (Cliente Invitado):**
```json
{
  "barberoId": 5,
  "servicioId": 2,
  "date": "2026-11-10",
  "startTime": "10:00",
  "cliente": {
    "nombre": "Juan",
    "apellido": "Pérez",
    "telefono": "+573001234567",
    "email": "juan.perez@example.com"
  }
}
```
**Response Body (201 Created):**
```json
{
  "id": 142,
  "barberoId": 5,
  "servicioId": 2,
  "clienteId": 89,
  "date": "2026-11-10T00:00:00.000Z",
  "startTime": "10:00",
  "endTime": "11:00",
  "status": "CONFIRMED",
  "precioReservado": "35000.00",
  "tokenGestion": "a8f3b...9c2d",
  "mensaje": "Reserva creada exitosamente"
}
```

### 4. Consulta de Disponibilidad de Barbero: `GET /usuarios/barberos/:id/disponibilidad?fecha=2026-11-10&servicioId=2`
**Response Body (200 OK):**
```json
{
  "barberoId": 5,
  "fecha": "2026-11-10",
  "franjasDisponibles": [
    { "startTime": "09:00", "endTime": "10:00", "disponible": true },
    { "startTime": "10:00", "endTime": "11:00", "disponible": false, "motivo": "OCUPADO" },
    { "startTime": "11:00", "endTime": "12:00", "disponible": true },
    { "startTime": "12:00", "endTime": "13:00", "disponible": false, "motivo": "DESCANSO" },
    { "startTime": "14:00", "endTime": "15:00", "disponible": true }
  ]
}
```

---

## 9.4 Formato Estándar de Errores (JSON)
```json
{
  "statusCode": 403,
  "timestamp": "2026-11-02T19:30:00.000Z",
  "path": "/servicios",
  "message": "No tienes permisos para operar en esta barbería"
}
```
*(Se prohíbe exponer mensajes de error nativos de SQL o trazas internas de Node.js).*

---

<a id="08-pruebas"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 08-pruebas.md -->
<!-- ========================================================================= -->

# 12. Estrategia de Pruebas y Aseguramiento de Calidad (QA) Multitenant

## 12.1 Pirámide de Pruebas Automatizadas
La calidad del software se garantiza mediante una estrategia multicapa que cubre pruebas unitarias, pruebas de aislamiento multi-tenant, integración y pruebas dinámicas de penetración:

```
          / \
         /   \     Pruebas DAST (OWASP ZAP: 22.866 vectores de ataque)
        / DAST\   ─────────────────────────────────────────────────────
       / AISL. \   Pruebas de Aislamiento Tenant (negocio-aislamiento.spec)
      /─────────\ ─────────────────────────────────────────────────────
     / INTEGRAC. \ Pruebas de Integración (Jest + Repositorios reales)
    / UNITARIAS   \ Pruebas Unitarias de Servicios, Guards y DTOs
   /───────────────\
```

---

## 12.2 Certificación de Pruebas Ejecutadas

### 1. Pruebas Unitarias, de Integración y Aislamiento (Jest)
* Cobertura de pruebas sobre servicios críticos:
  * `negocio-aislamiento.spec.ts` ➔ Blindaje de consultas tenant-scoped: verificación de que ninguna consulta pueda escapar del `negocioId` del contexto.
  * `perfil-negocio.service.spec.ts` ➔ Pruebas de persistencia de marca, validación de coordenadas y selección de `temaKey`.
  * `disponibilidad.service.spec.ts` ➔ Validación de franjas horarias y principio *Fail-Closed*.
  * `bloqueos-horario.service.spec.ts` ➔ Pruebas de solapamiento de descansos y vacaciones.
  * `horario-semanal.service.spec.ts` ➔ Creación y actualización de semanas laborales por sede.
  * `barberos.service.spec.ts` ➔ Gestión de comisiones por sede, fotos y membresías (46/46 tests aprobados).
  * `administradores.service.spec.ts` ➔ Asignación de Superadmin y administradores con llaves compuestas.
  * `all-exceptions.filter.spec.ts` ➔ Captura de errores 403/500 y verificación de llamadas a `AlertsService`.
  * `recordatorios.cron.spec.ts` ➔ Cron de recordatorios automáticos y enmascaramiento de PII.
* Comando de ejecución: `npm test` y `npm run test:multitenant`.

### 2. Pruebas de Seguridad en Dependencias (SCA)
* **Herramienta:** `npm audit` integrado en el pipeline de GitHub Actions (`security-audit.yml`).
* **Resultado:** **0 vulnerabilidades** reportadas tanto en `barberia-backend` como en `barberia-frontend`.

### 3. Pruebas Dinámicas de Penetración (DAST) con OWASP ZAP
* **Alcance:** Escaneo dinámico sobre la API en vivo de NestJS (`http://localhost:3000`) importando la definición OpenAPI oficial (`/api/docs-json`).
* **Métricas del Ataque:**
  * **22.866 solicitudes de ataque** lanzadas a través de 24 plugins de penetración en 04:08 minutos.
  * **3.769 ataques activos de Inyección SQL (SQLi):** 0 alertas (100% blindado por Prisma ORM).
  * **5.975 ataques de Inyección de Comandos OS:** 0 alertas (100% mitigado por validación de DTOs).
  * **5.610 ataques de Server-Side Code Injection (SSTI):** 0 alertas.
  * **Ataques de Fuerza Bruta / Inundación:** Mitigados con éxito mediante Throttler (HTTP 429 Too Many Requests).

---

<a id="09-ia-responsable-hitl"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 09-ia-responsable-hitl.md -->
<!-- ========================================================================= -->

# 14. Inteligencia Artificial Responsable, Privacidad y Protocolo HITL

## 14.1 Principios Éticos y Gobernanza de IA
El desarrollo del proyecto incorpora herramientas de asistencia de Inteligencia Artificial bajo lineamientos éticos estrictos que garantizan la confidencialidad de la información, el aislamiento multi-inquilino y la ausencia de alucinaciones en la arquitectura del sistema:

1. **Privacidad de Información Personal Identificable (PII):**
   * **Directiva:** Los datos personales de clientes y barberos (nombres completos, correos y números telefónicos) **NO DEBEN** enviarse en texto plano a modelos externos de IA ni guardarse sin protección en registros públicos.
   * **Enmascaramiento Obligatorio:** En los registros de auditoría Winston y notificaciones, los números telefónicos se ofuscan bajo el formato `318****854`.
2. **Cero Exposición de Secretos y Llaves de API:**
   * Las variables de entorno (`JWT_SECRET`, credenciales SMTP `SMTP_PASS`, client ID de Google) se encuentran estrictamente resguardadas en archivos `.env` ignorados por el control de versiones (`.gitignore`).
   * Ningún prompt enviado a agentes de IA debe contener secretos ni tokens maestros en texto visible.
3. **Protección contra Inyección de Prompts (*Prompt Injection*):**
   * Los campos de texto libre ingresados por clientes o usuarios se limpian mediante `ValidationPipe` y nunca se concatenan directamente en comandos de automatización o flujos de IA.

---

## 14.2 Protocolo de Gobernanza Human-in-the-Loop (HITL)

### 14.2.1 Definición y Principio Rector
La técnica **Human-in-the-Loop (HITL)** o *humano en el bucle* es un enfoque de inteligencia artificial que combina el aprendizaje automático y los modelos generativos con la **supervisión o intervención humana directa**. 

Su objetivo primordial es establecer un **bucle de retroalimentación continuo**: el modelo de IA realiza predicciones, propone soluciones arquitectónicas o automatiza tareas repetitivas, mientras que la persona humana **valida, corrige, refina y toma las decisiones finales en momentos críticos**.

En la Plataforma SaaS para Barberías, el paradigma HITL se implementa en dos niveles complementarios:

### 14.2.2 Nivel 1: Desarrollo Asistido y DevOps (Dev-HITL)
Gobernanza sobre el ciclo de vida del software y el código fuente:

```
  ┌────────────────────────────────────────────────────────┐
  │         BUCLE CONTINUO DE DESARROLLO (Dev-HITL)        │
  └────────────────────────────────────────────────────────┘
              │                               ▲
  1. Propone DTOs, Servicios,                 │ 2. Ejecuta tests locales,
     Controladores y Tests                    │    detecta desviaciones y refina
              ▼                               │
  ┌──────────────────────┐        ┌──────────────────────┐
  │     MODELO DE IA     │        │ DESARROLLADOR HUMANO │
  │   (Predice / Genera) │        │ (Supervisa / Corrige)│
  └──────────────────────┘        └──────────────────────┘
              │
              ▼ [Momento Crítico Detectado]
  ┌──────────────────────────────────────────────────────┐
  │           DECISIÓN FINAL EN MOMENTOS CRÍTICOS        │
  │  1. Alteración de esquemas Prisma / Migraciones SQL  │
  │  2. Asignación de roles de seguridad (RBAC / Tenants)│
  │  3. Invocación de red o comandos destructivos        │
  │  4. Publicación en Git y despliegue en producción    │
  └──────────────────────────────────────────────────────┘
              │ [Aprobación Explícita Requerida]
              ▼
        [ Entorno de Producción / Staging ]
```

### 14.2.3 Nivel 2: Dominio de Negocio y Plataforma (App-HITL)
Gobernanza dentro de la operativa de las barberías:
1. **Asistencia sin Autonomía Total:** Si la plataforma incorpora modelos predictivos (como estimación de demanda, sugerencia de franjas horarias o redacción asistida de recordatorios de WhatsApp), el sistema **NUNCA** toma acciones unilaterales de alto impacto sin confirmación.
2. **Decisiones Críticas en Manos del Staff:** En situaciones de sobrecupo, cancelaciones extraordinarias, bloqueos de agenda o excepciones en el cobro de comisiones, la decisión final recae de forma exclusiva en el **administrador o barbero humano**.
3. **Auditabilidad y Trazabilidad:** Toda acción sugerida por automatizaciones o algoritmos queda registrada en los logs de auditoría estructurados (`audit.log`) con indicación del usuario humano que autorizó la operación.

### 14.2.4 Directivas de Gobernanza HITL:
1. **La IA como Asistente Técnico:** La IA actúa como un copiloto de ingeniería enfocado en rapidez, consistencia de sintaxis y cobertura de pruebas; la responsabilidad de diseño arquitectónico y lógica de negocio permanece 100% en el desarrollador humano.
2. **Bloqueo de Modificaciones Destructivas:** La IA tiene estrictamente prohibido ejecutar o sugerir comandos de restablecimiento de base de datos destructivos (`prisma db push --force-reset` o `DROP TABLE`) en entornos compartidos o productivos.
3. **Auditoría Continua de Migraciones:** Cada columna o tabla agregada (como `temaKey` en `PerfilNegocio`) debe ser inspeccionada por el humano en su archivo SQL correspondiente antes de ejecutarse en el motor de base de datos.
4. **Ningún Push Autónomo:** Todo comando de publicación hacia repositorios remotos (`git push`) o plataformas de despliegue (Railway) requiere autorización humana previa e inequívoca.

---

<a id="10-plan-ejecucion-bootstrap"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 10-plan-ejecucion-bootstrap.md -->
<!-- ========================================================================= -->

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

---

## 15.3 Guía de Replicación Paso a Paso (Bootstrapping para la IA)

Cualquier agente de IA o ingeniero que reciba este Superprompt **DEBE seguir este orden cronológico para reconstruir el sistema funcionalmente**:

### Paso 1: Configuración de Entornos y Archivos `.env`
**1. `Barberia-Backend/.env`:**
```env
PORT=3000
NODE_ENV=development
DATABASE_URL="mysql://root:password@localhost:3306/bd_barberia_multitenant_dev"
JWT_SECRET="barber-saas-secret-key-32-chars-min-length-required"
JWT_EXPIRATION="8h"
GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"
FRONTEND_URL="http://localhost:5173"
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="alertas@barberia.com"
SMTP_PASS="app-password-16-chars"
SMTP_FROM="Alertas Plataforma <alertas@barberia.com>"
```

**2. `Barberia-Frontend/.env`:**
```env
VITE_API_BASE_URL="http://localhost:3000"
VITE_GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"
```

---

### Paso 2: Base de Datos y Prisma ORM
1. Iniciar contenedor de base de datos MySQL 8:
   ```bash
   docker run --name mysql-barberia -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=bd_barberia_multitenant_dev -p 3306:3306 -d mysql:8.0
   ```
2. Crear archivo `Barberia-Backend/prisma/schema.prisma` copiando exactamente el contenido de la **Sección 06**.
3. Generar el cliente de Prisma y correr la migración inicial:
   ```bash
   cd Barberia-Backend
   npm install
   npx prisma generate
   npx prisma migrate dev --name init_multitenant_schema
   ```

---

### Paso 3: Construcción del Backend NestJS
1. Configurar `main.ts` con seguridad perimetral:
   * `app.use(helmet({ contentSecurityPolicy: false }))` (o configurando CSP que permita OpenStreetMap y Google).
   * `app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }))`.
   * `app.useGlobalFilters(new AllExceptionsFilter(alertsService))`.
2. Registrar el middleware de tenant en `app.module.ts`:
   * Interceptar peticiones y resolver el tenant a partir de la cabecera `X-Negocio-Slug` o subdominio.
3. Crear los módulos en `src/modules/` según el árbol de la **Sección 05**, implementando los DTOs canónicos de la **Sección 09**.
4. Ejecutar pruebas unitarias para validar que el aislamiento y la lógica de citas funcionan:
   ```bash
   npm run test
   ```

---

### Paso 4: Construcción del Frontend React 19
1. Instalar dependencias core:
   ```bash
   cd ../Barberia-Frontend
   npm install react react-dom react-router-dom @tanstack/react-query axios lucide-react bootstrap
   ```
2. Crear `src/shared/lib/http/axios.ts` con los dos clientes:
   * `apiClient`: inyecta `Authorization: Bearer token_barberia_<slug>` y `X-Negocio-Slug: <slug>`.
   * `reservasApiClient`: inyecta `Authorization: Bearer cliente_token_<slug>`.
3. Crear `TenantBrandContext.tsx` que lea `temaKey` del perfil y fije el atributo `data-tenant-theme` en `document.documentElement`.
4. Configurar las rutas en `App.tsx`:
   * Raíz `/` y `/plataforma` ➔ Directorio global SaaS.
   * `/:slug` ➔ Landing de la sede con `LocationSection` (OpenStreetMap).
   * `/:slug/reservar` ➔ Wizard de agendamiento público.
   * `/:slug/dashboard` ➔ Panel administrativo protegido por membresía.

---

### Paso 5: Verificación End-to-End
1. Iniciar backend: `npm run start:dev` (puerto 3000).
2. Iniciar frontend: `npm run dev` (puerto 5173).
3. Entrar a `http://localhost:5173/plataforma`, crear una barbería de prueba (ej. `demo-barber`) y verificar que se pueda navegar a `http://localhost:5173/demo-barber` con su tema visual y mapa activos.

---


