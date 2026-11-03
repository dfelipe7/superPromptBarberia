# SUPERPROMPT - KYRIOS BARBER (KYRIOS STUDIO)
> **Especificación maestra del sistema compilada automáticamente a partir de `prompt-master/superprompt/secciones/`. No editar directamente.**

## Índice de Contenidos del Superprompt

- [00. Instrucciones Ia](#00-instrucciones-ia)
- [01. Contexto Problema](#01-contexto-problema)
- [02. Alcance](#02-alcance)
- [03. Roles Permisos](#03-roles-permisos)
- [04. Stack Tecnologico](#04-stack-tecnologico)
- [05. Arquitectura Patrones](#05-arquitectura-patrones)
- [06. Modelo Datos](#06-modelo-datos)
- [07. Historias Usuario](#07-historias-usuario)
- [08. Requisitos No Funcionales](#08-requisitos-no-funcionales)
- [09. Api Contratos](#09-api-contratos)
- [10. Integraciones](#10-integraciones)
- [11. Ui Ux](#11-ui-ux)
- [12. Pruebas](#12-pruebas)
- [13. Documentacion](#13-documentacion)
- [14. Ia Responsable](#14-ia-responsable)
- [15. Plan Ejecucion](#15-plan-ejecucion)

---

<a id="00-instrucciones-ia"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 00-instrucciones-ia.md -->
<!-- ========================================================================= -->

# 00. Instrucciones de Ejecución, Directivas de IA y Protocolo HITL

## 0.1 Objetivo General
Este documento establece las directrices normativas y técnicas para el desarrollo, auditoría y mantenimiento del sistema **Kyrios Barber Platform (SaaS Multitenant)**. Cualquier agente de Inteligencia Artificial (IA) o desarrollador de software que interactúe con este repositorio **DEBE** acatar estrictamente las reglas aquí descritas para garantizar la coherencia arquitectónica, la integridad de datos, el aislamiento multi-inquilino (*tenant isolation*) y el blindaje de seguridad.

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

<a id="01-contexto-problema"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 01-contexto-problema.md -->
<!-- ========================================================================= -->

# 01. Contexto Organizacional y Definición del Problema

## 1.1 Contexto de la Organización y Evolución a SaaS Multitenant
**Kyrios Barber** nació como una solución integral para **Kyrios Studio**, un prestigioso establecimiento comercial de barbería y cuidado estético masculino ubicado en la ciudad de Popayán, Colombia. La empresa presta servicios especializados de corte de cabello, arreglo de barba, tratamientos capilares y venta de productos cosméticos para caballeros, contando con un equipo de barberos profesionales que operan bajo un esquema de porcentaje de comisión por servicio prestado.

Debido al éxito operativo y a la necesidad de escalar el modelo a múltiples sedes y barberías aliadas, el sistema evolucionó hacia una **Plataforma SaaS Multitenant (Multi-Inquilino)**. Cada barbería o sede opera como un **Tenant autónomo** con su propia marca, catálogo de servicios, equipo de barberos, horarios, paleta de colores corporativa y base de clientes, compartiendo de manera segura una infraestructura cloud común con estricto aislamiento de datos.

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
Diseñar, construir e implementar una plataforma web integral (*Kyrios Barber Platform*) con arquitectura cliente-servidor desacoplada y soporte nativo Multi-Tenant que automatice:
* El agendamiento autónomo de citas en línea por parte de los clientes (registrados o invitados) bajo la URL propia de cada barbería (`/:slug/reservar`).
* El control milimétrico de la disponibilidad, descansos y bloqueos de agenda de cada barbero por sede.
* El despacho automatizado de confirmaciones y recordatorios a través de WhatsApp (Baileys) con sesiones aisladas por negocio y correo electrónico.
* La administración multisede segura bajo el estándar internacional de ciberseguridad **OWASP Top 10: 2025**, permitiendo a dueños y administradores gestionar múltiples barberías con una única cuenta global sin colisión de sesiones.

---

<a id="02-alcance"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 02-alcance.md -->
<!-- ========================================================================= -->

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

<a id="03-roles-permisos"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 03-roles-permisos.md -->
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

<a id="04-stack-tecnologico"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 04-stack-tecnologico.md -->
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

<a id="05-arquitectura-patrones"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 05-arquitectura-patrones.md -->
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

<a id="06-modelo-datos"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 06-modelo-datos.md -->
<!-- ========================================================================= -->

# 06. Modelo de Datos y Esquema Relacional Multitenant (Prisma)

## 6.1 Diagrama Entidad-Relación Lógico Multitenant
El modelo de datos se encuentra normalizado en tercera forma normal (3NF), gestionado íntegramente mediante Prisma ORM sobre MySQL/MariaDB con aislamiento por `negocioId` y claves compuestas foráneas.

```
Negocio (1) ──── (0..1) PerfilNegocio
Negocio (1) ──── (N) Administrador (N) ──── (1) Usuario (Global)
Negocio (1) ──── (N) Barbero       (N) ──── (1) Usuario (Global)
Negocio (1) ──── (N) Servicio      (N) ──── (N) Barbero (vía BarberoServicio)
Negocio (1) ──── (N) HorarioSemanal
Negocio (1) ──── (N) BloqueoHorario
Negocio (1) ──── (N) Cliente       (N) ──── (0..1) Usuario (Global)
Negocio (1) ──── (N) Reserva
Negocio (1) ──── (N) WhatsAppPlantilla
Negocio (1) ──── (0..1) ConfiguracionNegocio
```

---

## 6.2 Entidades Principales del Esquema (`schema.prisma`)

### 1. `Negocio` y `PerfilNegocio` (Núcleo Multi-Tenant)
* **`Negocio` (Global):**
  * `id` (Int, PK, autoincrement)
  * `nombre` (String, VarChar 120)
  * `slug` (String, Unique, VarChar 80) — Identificador de URL y subdominio
  * `estado` (Enum: `ACTIVO`, `INACTIVO`)
  * `zonaHoraria` (String, VarChar 50, default 'America/Bogota')
  * `creadoEn`, `actualizadoEn` (DateTime)
* **`PerfilNegocio` (1:1 con Negocio):**
  * `id`, `negocioId` (Int, Unique, FK ➔ Negocio)
  * `frasePrincipal` (String?, VarChar 200) — Lema o descriptor
  * `temaKey` (String?, VarChar 50, default 'clasico-azul') — Paleta visual activa
  * `direccion`, `ciudad`, `departamento`, `referencia` (String?)
  * `latitud`, `longitud` (Decimal 10,7) — Coordenadas canónicas para radar y mapas
  * `faviconUrl`, `bannerUrl`, `logoBlancoUrl`, `logoNegroUrl` (String?, VarChar 500)

### 2. `Usuario` (Identidad Personal Global)
* Representa a la persona física en la plataforma. **No pertenece a ningún negocio en particular**:
* `id` (Int, PK, autoincrement)
* `email` (String, Unique)
* `googleId` (String?, Unique)
* `nombre`, `apellido` (String)
* `rol` (Enum: `SUPERADMIN`, `ADMINISTRADOR`, `BARBERO`, `PERSONAL`)
* `estado` (Enum: `ACTIVO`, `INACTIVO`)

### 3. `Administrador` y `Barbero` (Membresías por Sede)
* **`Administrador`:**
  * `id`, `usuarioId` (FK ➔ Usuario), `negocioId` (FK ➔ Negocio)
  * `superadmin` (Boolean, default false) — Otorga facultades de Superadmin en ESTA sede
  * `estado` (Enum: `ACTIVO`, `INACTIVO`)
  * **Restricción de Membresía:** `@@unique([negocioId, usuarioId])`
* **`Barbero`:**
  * `id`, `usuarioId` (FK ➔ Usuario), `negocioId` (FK ➔ Negocio)
  * `porcentajeComision` (Decimal 5,2)
  * `fotoUrl` (String?)
  * `estado` (Enum: `ACTIVO`, `INACTIVO`)
  * **Restricción de Membresía:** `@@unique([negocioId, usuarioId])`

### 4. `Servicio` y `BarberoServicio`
* **`Servicio`:** `id`, `negocioId` (FK ➔ Negocio), `nombre` (VarChar 100), `descripcion`, `precio` (Decimal 10,2), `duracionMinutos` (Int), `fotoUrl`, `estado`. Restricción: `@@unique([negocioId, nombre])`.
* **`BarberoServicio`:** `barberoId` (FK), `servicioId` (FK), `negocioId` (FK). Llave primaria compuesta `@@id([barberoId, servicioId])` y relaciones foráneas compuestas con validación de que barbero y servicio pertenezcan al mismo tenant.

### 5. `HorarioSemanal` y `BloqueoHorario`
* **`HorarioSemanal` (`BarberWeeklySlot`):** `id`, `barberoId`, `dayOfWeek` (0-6), `startTime`, `endTime`, `negocioId`. Restricción: `@@unique([negocioId, barberoId, dayOfWeek, startTime])`.
* **`BloqueoHorario` (`BarberScheduleBlock`):** `id`, `barberoId`, `date` (Date), `startTime`, `endTime`, `motivo`, `status`, `negocioId`.

### 6. `Cliente` y `Reserva` (`Reservation`)
* **`Cliente`:**
  * `id`, `negocioId` (FK ➔ Negocio), `usuarioId` (FK opcional ➔ Usuario), `googleId` (String?)
  * `nombre`, `apellido`, `email`, `telefono`
  * **Unicidad Multitenant:** `@@unique([negocioId, googleId])`, `@@unique([negocioId, usuarioId])`, `@@unique([negocioId, id])`.
* **`Reserva` (`Reservation`):**
  * `id`, `negocioId` (FK ➔ Negocio), `barberoId`, `servicioId`, `clienteId`
  * `date` (Date), `startTime`, `endTime`
  * `precio` (Decimal: congelado al momento del agendamiento)
  * `status` (Enum: `PENDIENTE`, `CONFIRMADA`, `COMPLETADA`, `CANCELADA`, `NO_SHOW`)
  * `tokenGestion` (String?, Unique: hash seguro para cancelar o consultar)
  * `gestionTokenCifrado` (String?: copia cifrada reversible para idempotencia)
  * `tokenExpiracion` (DateTime?)
  * **Índices de Concurrencia:** `@@unique([negocioId, barberoId, date, startTime, slotActivo])`.

### 7. `WhatsAppPlantilla` y `ConfiguracionNegocio`
* **`WhatsAppPlantilla`:** Plantillas de confirmación y recordatorio personalizadas por sede (`@@unique([negocioId, tipo])`).
* **`ConfiguracionNegocio`:** Políticas de cancelación, tolerancia de no-show y parámetros operativos por sede (`@@unique([negocioId])`).

---

<a id="07-historias-usuario"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 07-historias-usuario.md -->
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

<a id="08-requisitos-no-funcionales"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 08-requisitos-no-funcionales.md -->
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

<a id="09-api-contratos"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 09-api-contratos.md -->
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
* `GET /plataforma/negocios` ➔ Lista todas las barberías registradas con sus métricas en tiempo real (barberos, servicios, citas, clientes) y estado.
* `POST /plataforma/negocios` ➔ Da de alta un nuevo tenant en la plataforma, inicializa su perfil y asocia atómicamente a su Superadmin fundador.
* `PATCH /plataforma/negocios/:id/estado` ➔ Activa o suspende una barbería en la plataforma (`ACTIVO` / `INACTIVO`).

### 2. Identidad y Perfil de Sede (`/negocios/perfil`)
* `GET /negocios/perfil/publico` ➔ Consulta pública de la identidad de la sede (nombre, lema, dirección, coordenadas, radar y tema visual `temaKey`).
* `GET /negocios/perfil/gestion` ➔ Consulta administrativa del perfil para configuración del negocio.
* `PUT /negocios/perfil` ➔ Actualiza lema, dirección, coordenadas GPS (`latitud`, `longitud`) y tema visual (`temaKey`).
* `POST /negocios/perfil/archivos/:tipo` ➔ Sube archivos de marca validados (favicon, banner, logo blanco, logo negro).

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

## 9.3 Formato Estándar de Errores (JSON)
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

<a id="10-integraciones"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 10-integraciones.md -->
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

<a id="11-ui-ux"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 11-ui-ux.md -->
<!-- ========================================================================= -->

# 11. Interfaz de Usuario (UI) y Experiencia de Usuario Multitenant (UX)

## 11.1 Filosofía de Diseño y Theming Dinámico
La plataforma implementa un diseño contemporáneo en Modo Oscuro (*Dark Mode*) con soporte para **personalización estética de marca en tiempo real por sede**:

* **Sistema de Temas Dinámicos (`data-tenant-theme`):**
  * Cada barbería elige su tema visual en la configuración del negocio, el cual se persiste en base de datos (`PerfilNegocio.temaKey`).
  * `TenantBrandContext` detecta el tema activo e inyecta dinámicamente las variables CSS en el elemento raíz:
    * `clasico-azul`: Azul Zafiro corporativo (Kyrios Oficial · `#0071BC`).
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

### 4. Configuración del Negocio y Asistente GPS (`/:slug/configuracion`)
* Botón "📍 Usar mi ubicación actual" mediante `navigator.geolocation` para capturar coordenadas GPS automáticamente desde el local.
* Extractor inteligente que analiza enlaces de Google Maps (`@lat,lng`, `?q=lat,lng`) o pares decimales pegados.
* Selector visual de temas con vista previa inmediata.

### 5. Directorio Global y Onboarding (`/plataforma` y `/explorar`)
* Vista de todas las barberías activas en el sistema con métricas globales.
* Modal para registrar nuevas sedes con asignación atómica de Superadmin fundador.

---

## 11.3 Criterios de Accesibilidad y Responsividad
* **Mobile-First:** El 85% de los clientes agenda desde dispositivos móviles; todas las áreas táctiles cuentan con un mínimo de 48x48 píxeles.
* **Feedback Inmediato:** Indicadores visuales con spinners (`KyriosSpinner`) y notificaciones *Toast* para confirmar operaciones sin recargas completas.

---

<a id="12-pruebas"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 12-pruebas.md -->
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

<a id="13-documentacion"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 13-documentacion.md -->
<!-- ========================================================================= -->

# 13. Documentación Técnica, Artefactos y Entregables

## 13.1 Catálogo de Documentación del Repositorio
El proyecto cuenta con un acervo formal de documentación técnica estructurada que respalda cada decisión arquitectónica y criterio de evaluación:

1. **Especificación Interactiva Swagger / OpenAPI:**
   * Archivo vivo expuesto en `/api/docs` con schemas tipados de DTOs, códigos de respuesta HTTP, cabecera `X-Negocio-Slug` y decoradores de autenticación Bearer.
2. **Documentación Multitenant Oficial:**
   * `CAMBIOS_PLATAFORMA_MULTITENANT.md` ➔ Registro exhaustivo de la evolución de arquitectura monotienda a SaaS multitenant, llaves compuestas y aislamiento de sesiones por pestaña.
   * `CONTRATOS_API_MULTITENANT.md` ➔ Matriz de endpoints por rol, cabeceras requeridas y códigos de error por tenant.
3. **Documentos de Seguridad y Ciberseguridad (OWASP):**
   * `DICCIONARIO_DETALLADO_ALERTAS_OWASP_ZAP.docx` ➔ Análisis técnico y justificación de falsos positivos de los escaneos de penetración.
   * `OWASP_Top_10_2025_Auditoria_Barberia.docx` ➔ Mapeo detallado de los 10 riesgos del estándar oficial contra las líneas de código fuente.
   * `PRUEBAS_Y_VECTORES_DE_ATAQUE_OWASP_ZAP.docx` ➔ Evidencia de los 22.866 vectores de ataque ejecutados con ZAP.
4. **Modelado y Procesos de Negocio:**
   * `BPMN_AS_IS_Kyrios_Studio.drawio` ➔ Diagrama BPMN del proceso operativo y flujo de clientes.
   * `EntidadRelacionBarberia.drawio` ➔ Diagrama entidad-relación del modelo de datos normalizado con llaves compuestas.
   * `Matriz RACI por Roles del Sistema.xlsx` ➔ Asignación formal de responsabilidades por rol y sede.
   * `HE_HU.xlsx` ➔ Backlog maestro consolidado de Épicas e Historias de Usuario con sus criterios de aceptación.
5. **Guías Operativas:**
   * `GUIA_WHATSAPP_BAILEYS.md` ➔ Manual de vinculación, sesiones multi-tenant en disco y resolución de problemas del bot de mensajería.

---

<a id="14-ia-responsable"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 14-ia-responsable.md -->
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

En Kyrios Barber Platform, el paradigma HITL se implementa en dos niveles complementarios:

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

<a id="15-plan-ejecucion"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 15-plan-ejecucion.md -->
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

