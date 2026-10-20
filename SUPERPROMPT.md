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

# 00. Instrucciones de Ejecución y Directivas para Inteligencia Artificial

## 0.1 Objetivo General
Este documento establece las directrices normativas y técnicas para el desarrollo, auditoría y mantenimiento del sistema **Kyrios Barber (Kyrios Studio)**. Cualquier agente de Inteligencia Artificial (IA) o desarrollador de software que interactúe con este repositorio **DEBE** acatar estrictamente las reglas aquí descritas para garantizar la coherencia arquitectónica, la integridad de datos y el blindaje de seguridad.

## 0.2 Terminología Normativa (RFC 2119)
* **DEBE / OBLIGATORIO (SHALL / MUST):** Indica una exigencia absoluta del sistema de ingeniería.
* **NO DEBE (MUST NOT):** Indica una prohibición absoluta por motivos de seguridad o integridad arquitectónica.
* **DEBERÍA / RECOMENDADO (SHOULD):** Indica una práctica aconsejable que solo puede omitirse con justificación técnica explícita.
* **PUEDE / OPCIONAL (MAY):** Indica una característica potestativa según los requerimientos de la fase.

## 0.3 Directivas Estrictas de Codificación
1. **TypeScript Estricto:**
   * Tanto en Backend (NestJS) como en Frontend (React 19), el código **DEBE** tener tipado estricto.
   * **PROHIBICIÓN:** **NO DEBE** utilizarse el tipo `any` bajo ninguna circunstancia. Toda estructura de datos debe contar con su correspondiente `interface`, `type` o `DTO`.
2. **Arquitectura y Modularidad en NestJS:**
   * Cada módulo **DEBE** encapsular sus controladores, servicios y repositorios.
   * La lógica de acceso a datos **DEBE** aislarse en clases de repositorio que consuman `PrismaService`, evitando invocar el cliente de base de datos directamente desde los controladores.
   * La validación de entrada **DEBE** ejecutarse a través de `ValidationPipe` global con `{ whitelist: true, forbidNonWhitelisted: true, transform: true }`.
3. **Persistencia y Esquema Prisma:**
   * Ningún cambio en la base de datos **DEBE** realizarse manualmente o mediante consultas arbitrarias.
   * Todo ajuste estructural de base de datos **DEBE** ejecutarse mediante migraciones versionadas de Prisma (`npx prisma migrate dev`).
4. **Seguridad Defensiva y Principio Fail-Closed:**
   * En caso de duda, falta de datos o inconsistencia en la verificación de reservas o disponibilidad horaria, el sistema **DEBE** "fallar cerrado" (`fail-closed`), rechazando la operación con el código HTTP correspondiente (403, 409 o 503) para evitar ventas duplicadas o accesos no autorizados.
5. **Preservación de Pruebas y Evidencias:**
   * Todo cambio en la lógica de negocio **DEBE** respaldarse con pruebas unitarias (`*.spec.ts`) ejecutadas satisfactoriamente mediante `npm run test`.

---

<a id="01-contexto-problema"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 01-contexto-problema.md -->
<!-- ========================================================================= -->

# 01. Contexto Organizacional y Definición del Problema

## 1.1 Contexto de la Organización
**Kyrios Studio** es un establecimiento comercial de barbería y cuidado estético masculino ubicado en la ciudad de Popayán, Colombia. La empresa presta servicios especializados de corte de cabello, arreglo de barba, tratamientos capilares y venta de productos cosméticos para caballeros, contando con un equipo de barberos profesionales que operan bajo un esquema de porcentaje de comisión por servicio prestado.

## 1.2 Definición del Problema Central
Históricamente, la operación diaria de la barbería se ha gestionado de forma manual y fragmentada mediante cuadernos de apuntes físicos y conversaciones dispersas en aplicaciones de mensajería (WhatsApp personal de cada barbero). Este modelo ha generado fallas operativas críticas:

1. **Colisión de Citas y Agendamiento Solapado:**  
   Falta de sincronización en tiempo real entre los turnos solicitados por los clientes y la disponibilidad real de cada barbero, provocando sobreventa de horarios o clientes esperando más de 45 minutos.
2. **Elevada Tasa de Inasistencia Sin Aviso (*No-Show*):**  
   Al no contar con un sistema automatizado de recordatorios y confirmación previa de citas, entre un 20% y 30% de los turnos agendados terminaban en inasistencia, causando horas muertas y pérdidas económicas directas para los barberos.
3. **Opacidad en la Liquidación de Comisiones:**  
   Incertidumbre y fricción entre la administración y el personal técnico al final de la jornada por falta de un registro centralizado y trazable de qué servicios fueron efectivamente prestados por cada barbero.
4. **Vulnerabilidad en la Gestión de la Información:**  
   Inexistencia de controles de acceso digital, almacenamiento inseguro de contactos de clientes y carencia de políticas de auditoría informática.

## 1.3 Solución Planteada
Diseñar, construir e implementar una plataforma web integral (*Kyrios Barber*) con arquitectura cliente-servidor desacoplada que automatice:
* El agendamiento autónomo de citas en línea por parte de los clientes (registrados o invitados).
* El control milimétrico de la disponibilidad, descansos y bloqueos de agenda de cada barbero.
* El despacho automatizado de confirmaciones y recordatorios a través de WhatsApp (Baileys) y correo electrónico.
* La administración segura de usuarios bajo el estándar internacional de ciberseguridad **OWASP Top 10: 2025**.

---

<a id="02-alcance"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 02-alcance.md -->
<!-- ========================================================================= -->

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

---

<a id="03-roles-permisos"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 03-roles-permisos.md -->
<!-- ========================================================================= -->

# 03. Matriz de Roles, Permisos y Control de Acceso (RBAC)

## 3.1 Definición de Roles del Sistema
El sistema implementa un modelo de Control de Acceso Basado en Roles (RBAC) compuesto por 4 roles jerárquicos:

1. **`SUPERADMIN` (Superadministrador):**
   * Rol de máxima autoridad técnica y administrativa.
   * Responsable de la creación y gestión de otros administradores, auditoría global del sistema, sincronización de usuarios fundadores y acceso irrestricto a los registros de seguridad.
2. **`ADMINISTRADOR`:**
   * Responsable de la gestión del negocio en el día a día.
   * Puede gestionar el catálogo de servicios, dar de alta o suspender barberos, consultar reservas globales, registrar citas presenciales de clientes y gestionar la vinculación de WhatsApp.
   * **Restricción:** No puede crear otros administradores ni alterar la cuenta de un Superadministrador.
3. **`BARBERO`:**
   * Personal técnico encargado de la prestación de servicios estéticos.
   * Puede consultar su propia agenda de citas asignadas, cambiar el estado de las citas que atiende (`COMPLETADA`, `CANCELADA`, `NO_SHOW`), configurar su horario semanal de atención y definir bloqueos por descanso/almuerzo.
   * **Restricción (BOLA/IDOR):** No tiene autorización para consultar ni alterar la agenda, datos o comisiones de otros barberos.
4. **`CLIENTE` (Registrado o Invitado):**
   * Usuario final que solicita la reserva de un servicio.
   * **Modalidad Autenticado:** Inicia sesión con Google OAuth, consulta su historial de citas y agenda en 4 pasos.
   * **Modalidad Invitado:** Agenda únicamente con nombre, teléfono y correo; recibe un token criptográfico efímero (`X-Reservation-Management-Token`) que le permite consultar o cancelar su reserva específica.

## 3.2 Matriz RACI de Permisos por Módulo

| Módulo / Funcionalidad | SUPERADMIN | ADMINISTRADOR | BARBERO | CLIENTE |
|---|:---:|:---:|:---:|:---:|
| **Crear / Desactivar Administradores** | **R / A** | ❌ | ❌ | ❌ |
| **Gestionar Barberos y Comisiones** | **A** | **R** | ❌ | ❌ |
| **Gestionar Catálogo de Servicios** | **A** | **R** | **C** | **I** |
| **Configurar Horario y Bloqueos Propios** | **A** | **A** | **R** (Solo propios) | ❌ |
| **Consultar Agenda de Citas** | **I** (Global) | **R** (Global) | **R** (Solo propias) | **I** (Solo suyas) |
| **Cambiar Estado de Cita** | **A** | **A** | **R** (Sus turnos) | ❌ |
| **Agendar Cita** | **A** | **R** (Presencial) | ❌ | **R** (Online) |
| **Cancelar Cita** | **A** | **R** | **R** | **R** (Con token/dueño) |
| **Revisar Logs de Seguridad y Auditoría** | **R / A** | ❌ | ❌ | ❌ |
| **Configurar Dispositivo WhatsApp** | **A** | **R** | ❌ | ❌ |

*(Convención RACI: **R** = Responsable de ejecutar, **A** = Aprobador final, **C** = Consultado, **I** = Informado / Lectura).*

## 3.3 Mecanismo de Aplicación en el Código
* **Frontend:** Rutas protegidas mediante componentes de orden superior `ProtectedRoute` que verifican el array `usuario.roles` antes de renderizar la vista.
* **Backend:** Combinación secuencial de `JwtAuthGuard` (valida la autenticidad y firma del JWT) y `RolesGuard` (lee el decorador `@Roles(...)` e inspecciona los reclamos del token).

---

<a id="04-stack-tecnologico"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 04-stack-tecnologico.md -->
<!-- ========================================================================= -->

# 04. Stack Tecnológico y Convenciones de Ingeniería

## 4.1 Tecnologías del Backend (API REST)
* **Lenguaje:** TypeScript 5.7+ con compilación estricta (`strict: true`, `noImplicitAny: true`).
* **Framework:** NestJS 11.0 (Arquitectura orientada a módulos, controladores e inyección de dependencias).
* **ORM:** Prisma ORM 7.0 (Mapeo relacional seguro con consultas parametrizadas internamente).
* **Motor de Base de Datos:** MariaDB 11.4 / MySQL 8.0 (Almacenamiento relacional compatible con transacciones ACID).
* **Seguridad Perimetral:**
  * `helmet` v8.0.0 (Inyección de cabeceras de seguridad HTTP).
  * `@nestjs/throttler` v6.4.0 (Rate Limiting defensivo anti fuerza bruta).
  * `argon2` y `bcrypt` (Hashing criptográfico irreversible con salt para credenciales).
  * `@nestjs/jwt` (Generación y verificación de tokens de sesión HMAC-SHA256).
* **Observabilidad y Alertas:**
  * `nest-winston` + `winston-daily-rotate-file` (Registro rotativo en `audit.log`, `security.log` y `error.log`).
  * `@nestjs-modules/mailer` + `nodemailer` (Despacho de alertas SMTP a Google Gmail ante fallos 403 y 500).
* **Integraciones:**
  * `@whiskeysockets/baileys` (Integración con protocolo oficial WhatsApp Web para notificaciones).
  * `google-auth-library` (Validación criptográfica de tokens emitidos por Google Identity Services).

## 4.2 Tecnologías del Frontend (Cliente Web)
* **Librería Core:** React 19.0 con TypeScript 5.8+.
* **Empaquetador y Servidor Local:** Vite 6.2 (Compilación modular basada en ESM y recarga rápida HMR).
* **Enrutamiento:** React Router DOM v7 (Manejo de rutas declarativas con control de acceso RBAC).
* **Manejo de Estado del Servidor:** TanStack Query v5 (Caché reactiva, invalidación automática tras mutaciones y resiliencia de datos).
* **Cliente HTTP:** Axios 1.7 con interceptores de solicitud (inyección automática del encabezado `Authorization: Bearer <token>`) y respuesta (manejo centralizado de 401/403).
* **Estilos:** Vanilla CSS / Tailwind CSS con sistema editorial de diseño en Modo Oscuro (*Dark Mode*) y micro-animaciones en CSS puro.
* **Componentes UI e Íconos:** Lucide React (Iconografía consistente y minimalista).

## 4.3 Convenciones de Código y Estructura
1. **Nomenclatura de Archivos:** `kebab-case.tipo.ts` (Ej: `reservas.controller.ts`, `reservas.service.ts`, `reservas.repository.ts`).
2. **DTOs Obligatorios:** Toda petición POST, PUT o PATCH **DEBE** contar con su DTO de entrada tipado con decoradores de `class-validator` (`@IsString()`, `@IsInt()`, `@Min()`, `@IsEmail()`, etc.).
3. **Manejo de Respuestas:** El backend **DEBE** estructurar sus respuestas exitosas bajo un esquema JSON claro, y en caso de error **DEBE** responder con el formato estándar `{ statusCode, timestamp, path, message }` garantizado por el filtro global de excepciones.

---

<a id="05-arquitectura-patrones"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 05-arquitectura-patrones.md -->
<!-- ========================================================================= -->

# 05. Arquitectura del Sistema y Patrones de Diseño

## 5.1 Estilo Arquitectónico Global
La plataforma adopta una **Arquitectura Cliente-Servidor Desacoplada (Decoupled Client-Server Architecture)** con comunicación sin estado (*stateless*) mediante API REST sobre HTTP/HTTPS:
* **Frontend:** Single Page Application (SPA) en React que consume la API REST de forma asíncrona.
* **Backend:** Arquitectura Modular y en Capas construida sobre NestJS.

```
[ Cliente Web (React 19 SPA) ]
              │
              ▼ (HTTPS / JSON / JWT)
[ Capa de Controladores (REST Controllers) ]
              │
              ▼ (Guards, Pipes & Interceptors)
[ Capa de Servicios de Dominio (Business Services) ]
              │
              ▼ (Interfaces & Ports)
[ Capa de Repositorios (Data Access Layer) ]
              │
              ▼ (Consultas Parametrizadas)
[ Motor Prisma ORM 7 ➔ Base de Datos MariaDB ]
```

## 5.2 Patrones de Diseño Aplicados en el Backend

1. **Patrón Repositorio (Repository Pattern):**
   * Desacopla la lógica de negocio pura de las consultas de persistencia a la base de datos.
   * Archivos: `reservas.repository.ts`, `usuarios.repository.ts`, `servicios.repository.ts`, `horarios.repository.ts`.
   * Permite cambiar el motor de persistencia o realizar pruebas unitarias simuladas (*mocks*) sin alterar los servicios.
2. **Patrón Adaptador y Puertos (Ports & Adapters):**
   * En el módulo de horarios se implementó el puerto `ProveedorReservasActivas` (`proveedor-reservas-activas.port.ts`).
   * Desacopla el cálculo de la disponibilidad de la implementación física del módulo de reservas, garantizando que el motor de horarios pueda consultar reservas activas sin acoplamiento circular.
3. **Patrón Estrategia (Strategy Pattern):**
   * Utilizado en la validación de disponibilidad horaria mediante `ReglaDisponibilidadStrategy` y `ReservaActivaRule`. Cada restricción de horario (bloqueo por almuerzo, día de descanso, cita ocupada) se evalúa como una estrategia independiente.
4. **Patrón Filtro Global de Excepciones (Exception Filter Pattern):**
   * Centralizado en `all-exceptions.filter.ts`. Intercepta cualquier excepción HTTP o fallo interno no capturado, homogeneizando el JSON de salida y disparando el subsistema de alertas de seguridad.
5. **Principio de Falla Cerrada (Fail-Closed):**
   * Aplicado en `DisponibilidadService`. Si el proveedor de reservas o algún componente dependiente no responde, el sistema **DEBE** rechazar la consulta (con 503 Service Unavailable) en lugar de retornar franjas abiertas a ciegas, evitando vender turnos colisionados.
6. **Patrón Máquina de Estados Finita:**
   * Gestiona el ciclo de vida de una cita:
     * `PENDIENTE` ➔ `CONFIRMADA`
     * `CONFIRMADA` ➔ `COMPLETADA`
     * `CONFIRMADA` ➔ `CANCELADA`
     * `CONFIRMADA` ➔ `NO_SHOW` (Inasistencia tras tolerancia)
   * Se prohíben transiciones ilícitas (ej: una cita cancelada no puede pasar a completada).

---

<a id="06-modelo-datos"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 06-modelo-datos.md -->
<!-- ========================================================================= -->

# 06. Modelo de Datos y Esquema Relacional (Prisma)

## 6.1 Diagrama Entidad-Relación Lógico
El modelo de datos se encuentra normalizado en tercera forma normal (3NF), gestionado íntegramente mediante Prisma ORM sobre MariaDB/MySQL.

```
Usuario (1) ──── (0..1) Administrador
Usuario (1) ──── (0..1) Barbero
Barbero (1) ──── (N) BarberoServicio (N) ──── (1) Servicio
Barbero (1) ──── (N) HorarioSemanal
Barbero (1) ──── (N) BloqueoHorario
Barbero (1) ──── (N) Reserva (N) ──── (1) Cliente
```

## 6.2 Entidades Principales del Esquema (`schema.prisma`)

### 1. `Usuario`
Identidad base del sistema (para administradores y barberos):
* `id` (Int, PK, autoincrement)
* `email` (String, Unique)
* `googleId` (String?, Unique) — Identificador estable de Google OAuth
* `nombre`, `apellido` (String)
* `rol` (Enum: `SUPERADMIN`, `ADMINISTRADOR`, `BARBERO`)
* `estado` (Enum: `ACTIVO`, `INACTIVO`)
* `createdAt`, `updatedAt` (DateTime)

### 2. `Administrador` y `Barbero`
Perfiles extendidos vinculados a `Usuario` mediante relación 1:1:
* **`Administrador`:** `id`, `usuarioId` (Unique, FK), `estado`.
* **`Barbero`:** `id`, `usuarioId` (Unique, FK), `porcentajeComision` (Decimal: 0.00 a 100.00), `fotoUrl` (String?), `estado`.

### 3. `Servicio` y `BarberoServicio`
Catálogo de servicios y asignación a profesionales:
* **`Servicio`:** `id`, `nombre`, `descripcion`, `precio` (Decimal), `duracionMinutos` (Int: estándar 60 min), `fotoUrl`, `estado`.
* **`BarberoServicio`:** `barberoId` (FK), `servicioId` (FK) — Llave primaria compuesta `@@id([barberoId, servicioId])`.

### 4. `HorarioSemanal` y `BloqueoHorario` (Módulo de Disponibilidad HE-08)
* **`HorarioSemanal`:** `id`, `barberoId` (FK), `dayOfWeek` (Int: 0=Domingo a 6=Sábado), `startTime` (String "HH:mm"), `endTime` (String "HH:mm"). Restricción de unicidad: `@@unique([barberoId, dayOfWeek, startTime])`.
* **`BloqueoHorario`:** `id`, `barberoId` (FK), `date` (DateTime @db.Date), `startTime`, `endTime`, `motivo` (String), `status` (Enum: `ACTIVO`, `CANCELADO`).

### 5. `Cliente` y `Reserva` (Módulo de Citas HE-04)
* **`Cliente`:** `id`, `googleId` (String?, Unique para clientes autenticados), `usuarioId` (Int?, FK opcional), `nombre`, `apellido`, `email`, `telefono` (String: PII).
* **`Reserva`:** 
  * `id` (Int, PK)
  * `barberoId` (FK ➔ Barbero), `servicioId` (FK ➔ Servicio), `clienteId` (FK ➔ Cliente)
  * `date` (DateTime @db.Date), `startTime`, `endTime`
  * `precio` (Decimal: congelado al momento del agendamiento)
  * `status` (Enum: `PENDIENTE`, `CONFIRMADA`, `COMPLETADA`, `CANCELADA`, `NO_SHOW`)
  * `tokenGestion` (String?, Unique: hash seguro para cancelar o consultar sin login)
  * `tokenExpiracion` (DateTime?)
  * **Índices de Concurrencia:** `@@index([barberoId, date, status])`, `@@unique([barberoId, date, startTime, slotActivo])` para impedir colisiones o sobreventa de citas.

### 6. `ConfiguracionWhatsapp`
Estado de conexión del servicio de notificaciones Baileys:
* `id`, `sesionActiva` (Boolean), `telefonoConectado` (String?), `ultimaSincronizacion`.

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

---

<a id="08-requisitos-no-funcionales"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 08-requisitos-no-funcionales.md -->
<!-- ========================================================================= -->

# 08. Requisitos No Funcionales (RNF) y Seguridad OWASP 2025

## 8.1 Matriz de Blindaje OWASP Top 10: 2025

* **RNF-SEC-01 (A01: Broken Access Control):**  
  El sistema **DEBE** aplicar control de acceso con doble guardia: `ProtectedRoute` en React y `JwtAuthGuard` + `RolesGuard` en NestJS. La autorización granular a nivel de servicio **DEBE** validar la propiedad del recurso para evitar vulnerabilidades BOLA/IDOR.
* **RNF-SEC-02 (A02: Security Misconfiguration):**  
  El backend **DEBE** inicializarse con `helmet()` configurando cabeceras de seguridad estrictas (`X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff`), CORS restringido a los dominios del frontend, y deshabilitación obligatoria del encabezado `X-Powered-By`.
* **RNF-SEC-03 (A03: Software Supply Chain Failures):**  
  Las dependencias del frontend y backend **DEBEN** mantenerse con `package-lock.json` inmutable y auditoría automatizada en CI/CD con `npm audit` exigiendo **0 vulnerabilidades de severidad alta o crítica**.
* **RNF-SEC-04 (A04: Cryptographic Failures):**  
  Las contraseñas **DEBEN** procesarse con hashing irreversible con salt (Argon2 / Bcrypt). Las sesiones **DEBEN** usar tokens JWT firmados con algoritmo HMAC-SHA256 y canal de transporte cifrado obligatorio mediante HTTPS/TLS.
* **RNF-SEC-05 (A05: Injection):**  
  El 100% de las consultas a la base de datos **DEBEN** realizarse a través de las funciones nativas parametrizadas de Prisma ORM, prohibiendo expresamente la concatenación de cadenas en SQL. El cliente React **DEBE** escapar automáticamente el árbol DOM contra Cross-Site Scripting (XSS).
* **RNF-SEC-06 (A06: Insecure Design):**  
  La arquitectura de agendamiento para clientes invitados **DEBE** desacoplarse del login administrativo mediante tokens temporales de gestión (`X-Reservation-Management-Token`).
* **RNF-SEC-07 (A07: Authentication Failures):**  
  La autenticación administrativa **DEBE** integrarse con el proveedor oficial Google OAuth 2.0 (SSO) y contar con Throttler / Rate Limiting configurado en 100 peticiones por minuto por IP para mitigar ataques de fuerza bruta o denegación de servicio.
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

# 09. Contratos de la API REST y Especificación OpenAPI

## 9.1 Convenciones Generales de la API
* **Base URL:** `/` (o prefijo de entorno de despliegue).
* **Documentación Interactiva:** Swagger UI expuesto en `/api/docs` y especificación cruda en `/api/docs-json`.
* **Formato de Comunicación:** JSON (`Content-Type: application/json; charset=utf-8`).
* **Autenticación:** Cabecera estándar HTTP `Authorization: Bearer <token_jwt>`.

---

## 9.2 Endpoints Principales por Módulo

### 1. Autenticación y Sesión (`/auth`)
* `POST /auth/google` ➔ Inicia sesión con Google OAuth 2.0. Recibe `{ idToken }` y retorna `{ accessToken, usuario }`.
* `POST /auth/refresh` ➔ Renueva el JWT con los roles vigentes en la base de datos (requiere Bearer token actual).

### 2. Administración y Personal (`/usuarios`)
* `GET /usuarios/me` ➔ Consulta el perfil del usuario autenticado.
* `POST /usuarios/administradores` ➔ Registra un nuevo administrador (exclusivo `@Roles('SUPERADMIN')`).
* `GET /usuarios/administradores` ➔ Lista todos los administradores (exclusivo `@Roles('SUPERADMIN')`).
* `PATCH /usuarios/administradores/:id/estado` ➔ Activa o suspende una cuenta de administrador.
* `GET /usuarios/barberos` ➔ Lista pública de barberos activos para el catálogo de reservas.
* `POST /usuarios/barberos` ➔ Da de alta un barbero en el sistema con su porcentaje de comisión inicial.
* `PATCH /usuarios/barberos/:id/comision` ➔ Actualiza la comisión pactada con el barbero.
* `POST /usuarios/barberos/foto` ➔ Sube la foto de perfil del barbero mediante `multipart/form-data`.

### 3. Catálogo de Servicios (`/servicios`)
* `GET /servicios` ➔ Lista pública de servicios activos con precio y duración.
* `POST /servicios` ➔ Crea un nuevo servicio estético (`@Roles('SUPERADMIN', 'ADMINISTRADOR')`).
* `PATCH /servicios/:id` ➔ Modifica precio, descripción o estado de un servicio.
* `GET /servicios/:servicioId/barberos` ➔ Retorna los barberos habilitados para ejecutar un servicio específico.

### 4. Horarios y Disponibilidad (`/usuarios/.../horarios`)
* `GET /usuarios/me/barbero/horario-semanal` ➔ Consulta el horario base del barbero en sesión.
* `PUT /usuarios/me/barbero/horario-semanal` ➔ Guarda la matriz de horas de atención por día de la semana.
* `POST /usuarios/me/barbero/bloqueos-horario` ➔ Registra un descanso o periodo no disponible.
* `GET /usuarios/barberos/:barberoId/disponibilidad?fecha=YYYY-MM-DD&servicioId=X` ➔ **Endpoint de consulta pública:** Retorna las franjas horarias libres de 60 minutos calculadas en tiempo real.

### 5. Reservas y Citas (`/reservas`)
* `POST /reservas` ➔ Crea una cita (cliente registrado o invitado). Retorna detalle de la cita y `tokenGestion`.
* `GET /reservas/barbero/me` ➔ Lista de citas asignadas al barbero en sesión filtradas por fecha.
* `PATCH /reservas/:reservaId/completar` ➔ Marca la cita como finalizada (`@Roles('BARBERO')`).
* `PATCH /reservas/:reservaId/no-show` ➔ Marca inasistencia del cliente tras la tolerancia.
* `PATCH /reservas/invitado/:reservaId/cancelar` ➔ Cancela una cita de invitado requiriendo el token en la cabecera `X-Reservation-Management-Token`.

---

## 9.3 Estructura Estándar de Respuestas de Error
Toda respuesta de error generada por el backend **DEBE** ajustarse estrictamente a este formato:

```json
{
  "statusCode": 403,
  "timestamp": "2026-10-20T04:50:38.474Z",
  "path": "/usuarios/administradores",
  "message": "No tienes permisos para realizar esta operación"
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

---

<a id="11-ui-ux"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 11-ui-ux.md -->
<!-- ========================================================================= -->

# 11. Interfaz de Usuario (UI) y Experiencia de Usuario (UX)

## 11.1 Filosofía de Diseño Visual
La identidad visual de **Kyrios Barber** está orientada a una experiencia premium, sofisticada y moderna, inspirada en las barberías clásicas de estilo vintage combinadas con un diseño web minimalista contemporáneo.

* **Paleta Cromática (Modo Oscuro Editorial):**
  * Fondo Principal: Negro carbón profundo (`#0f0f11` / `#141416`).
  * Superficies y Tarjetas: Gris grafito con sutiles bordes translúcidos (`#1e1e24`).
  * Acentos y Jerarquía: Dorado ámbar / bronce elegante (`#d4af37` / `#c59b27`) para botones de acción primaria y elementos activos.
  * Tipografía: Fuentes modernas de alta legibilidad (Inter / Outfit / Playfair para encabezados de lujo).
  * Estados del Sistema: Verde esmeralda para confirmaciones exitosas, ámbar para advertencias de turno y carmesí para cancelaciones o errores.

---

## 11.2 Principales Flujos de Usuario (User Journeys)

### 1. Flujo de Agendamiento Autónomo del Cliente (4 Pasos)
1. **Paso 1 · Catálogo de Servicios:** El cliente visualiza las tarjetas de servicios con imagen, precio y duración, seleccionando uno.
2. **Paso 2 · Selección de Profesional:** Se despliegan únicamente los barberos capacitados para ese servicio, mostrando su foto y nombre.
3. **Paso 3 · Calendario y Horas Libres:** Se selecciona la fecha; el sistema consulta la disponibilidad en tiempo real y pinta las horas disponibles en bloques de 60 min.
4. **Paso 4 · Datos y Confirmación:** El cliente ingresa sus datos (o se auto-completan si inició sesión con Google) y presiona "Confirmar Cita", recibiendo de inmediato su token de gestión en pantalla y por WhatsApp.

### 2. Panel Operativo del Barbero (Agenda en Vivo)
* Vista simplificada tipo tarjeta diaria con las citas ordenadas cronológicamente.
* Información concisa: hora de inicio, nombre del cliente, servicio a realizar y estado actual.
* Botones de acción rápida en 1 clic: "Marcar como Completada" o "No Asistió".

### 3. Panel de Administración y Configuración
* Gestión de usuarios, edición de comisiones y vinculación de WhatsApp mediante lector de código QR integrado directamente en la pantalla.

---

## 11.3 Criterios de Accesibilidad y Responsividad
* **Mobile-First:** El 85% de los clientes agenda desde dispositivos móviles; todos los botones, selectores de fecha y campos de formulario cuentan con áreas táctiles mínimas de 48x48 píxeles.
* **Feedback Inmediato:** Uso de estados de carga con *spinners* y alertas *Toast* no invasivas para confirmar operaciones sin recargar la página completa.

---

<a id="12-pruebas"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 12-pruebas.md -->
<!-- ========================================================================= -->

# 12. Estrategia de Pruebas y Aseguramiento de Calidad (QA)

## 12.1 Pirámide de Pruebas Automatizadas
La calidad del software se garantiza mediante una estrategia multicapa que cubre pruebas unitarias, de integración y pruebas dinámicas de penetración:

```
          / \
         /   \     Pruebas DAST (OWASP ZAP: 22.866 vectores)
        / DAST\   ─────────────────────────────────────────────
       /───────\   Pruebas de Integración (Jest + Repositorios reales)
      / INTEGR. \ ─────────────────────────────────────────────
     / UNITARIAS \ Pruebas Unitarias de Servicios y Controladores
    /─────────────\
```

---

## 12.2 Certificación de Pruebas Ejecutadas

### 1. Pruebas Unitarias y de Integración (Jest)
* **Resultado Oficial Verificado:** **65 Suites de Pruebas Aprobadas (65/65, 100%)** y **751 Casos de Prueba Ejecutados Satisfactoriamente (751/751, 100% éxito)**.
* Cobertura de pruebas sobre servicios críticos:
  * `disponibilidad.service.spec.ts` ➔ Validación de franjas horarias y principio *Fail-Closed*.
  * `bloqueos-horario.service.spec.ts` ➔ Pruebas de solapamiento de descansos y vacaciones.
  * `horario-semanal.service.spec.ts` ➔ Creación y actualización de semanas laborales.
  * `all-exceptions.filter.spec.ts` ➔ Captura de errores 403 y 500 y verificación de llamadas a `AlertsService`.
  * `alerts.service.spec.ts` ➔ Despacho de correos electrónicos vía Nodemailer.
  * `reservas-invitado-gestion.spec.ts` ➔ Validación de tokens de gestión efímeros.
  * `recordatorios.cron.spec.ts` ➔ Cron de recordatorios automáticos y enmascaramiento de PII.
* Comando de ejecución: `npm test` y `npm run test:cov`.

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
* **Alertas Analizadas:** Las advertencias reportadas por ZAP corresponden a **falsos positivos** propios del servidor de desarrollo local de Vite (`?v=...`) o scripts dinámicos de Google OAuth, sin impacto en producción.

---

<a id="13-documentacion"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 13-documentacion.md -->
<!-- ========================================================================= -->

# 13. Documentación Técnica, Artefactos y Entregables

## 13.1 Catálogo de Documentación del Repositorio
El proyecto cuenta con un acervo formal de documentación técnica estructurada que respalda cada decisión arquitectónica y criterio de evaluación:

1. **Especificación Interactiva Swagger / OpenAPI:**
   * Archivo vivo expuesto en `/api/docs` con schemas tipados de DTOs, códigos de respuesta HTTP y decoradores de autenticación Bearer.
2. **Documentos de Seguridad y Ciberseguridad (OWASP):**
   * `DICCIONARIO_DETALLADO_ALERTAS_OWASP_ZAP.docx` ➔ Análisis técnico y justificación de falsos positivos de los escaneos de penetración.
   * `OWASP_Top_10_2025_Auditoria_Barberia.docx` ➔ Mapeo detallado de los 10 riesgos del estándar oficial contra las líneas de código fuente.
   * `PRUEBAS_Y_VECTORES_DE_ATAQUE_OWASP_ZAP.docx` ➔ Evidencia de los 22.866 vectores de ataque ejecutados con ZAP.
3. **Modelado y Procesos de Negocio:**
   * `BPMN_AS_IS_Kyrios_Studio.drawio` ➔ Diagrama BPMN del proceso operativo actual y futuro de la barbería.
   * `EntidadRelacionBarberia.drawio` ➔ Diagrama entidad-relación del modelo de datos normalizado.
   * `Matriz RACI por Roles del Sistema.xlsx` ➔ Asignación formal de responsabilidades por rol.
   * `HE_HU.xlsx` ➔ Backlog maestro consolidado de Épicas e Historias de Usuario con sus criterios de aceptación.
4. **Guías Operativas:**
   * `GUIA_WHATSAPP_BAILEYS.md` ➔ Manual de vinculación, mantenimiento de sesión y resolución de problemas del bot de mensajería.
   * `README_SKILLS.md` ➔ Catálogo de las 22 habilidades especializadas configuradas para el pair-programming con IA en el proyecto.

---

<a id="14-ia-responsable"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 14-ia-responsable.md -->
<!-- ========================================================================= -->

# 14. Inteligencia Artificial Responsable, Privacidad y Ética de Datos

## 14.1 Principios Éticos Aplicados en el Desarrollo con IA
El desarrollo del proyecto incorpora herramientas de asistencia de Inteligencia Artificial bajo lineamientos éticos estrictos que garantizan la confidencialidad de la información y la ausencia de alucinaciones en la arquitectura del sistema:

1. **Privacidad de Información Personal Identificable (PII):**
   * **Directiva:** Los datos personales de clientes y barberos (nombres completos, correos y especialmente números telefónicos) **NO DEBEN** enviarse en texto plano a modelos externos de IA ni guardarse sin protección en registros públicos.
   * **Enmascaramiento Obligatorio:** En los servicios de WhatsApp y registros de auditoría Winston, los números telefónicos se ofuscan bajo el formato `318****854`.
2. **Cero Exposición de Secretos y Llaves de API:**
   * Las variables de entorno (`JWT_SECRET`, credenciales SMTP `SMTP_PASS`, client ID de Google) se encuentran estrictamente resguardadas en archivos `.env` ignorados por el control de versiones (`.gitignore`).
   * Ningún prompt enviado a agentes de IA debe contener llaves maestras en texto visible.
3. **Validación Humana en el Bucle (*Human-in-the-Loop*):**
   * Todo código o prueba generado con asistencia de IA es auditado, compilado y verificado por los desarrolladores humanos mediante pruebas automatizadas (`npm run test`) antes de integrarse al repositorio.
4. **Protección contra Inyección de Prompts (*Prompt Injection*):**
   * Los campos de texto libre ingresados por clientes (como observaciones de citas o motivos de bloqueo) se limpian mediante `ValidationPipe` y nunca se concatenan directamente en comandos de automatización o flujos de IA.

---

<a id="15-plan-ejecucion"></a>

<!-- ========================================================================= -->
<!-- SECCIÓN: 15-plan-ejecucion.md -->
<!-- ========================================================================= -->

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

---

