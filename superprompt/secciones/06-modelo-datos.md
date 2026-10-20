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
