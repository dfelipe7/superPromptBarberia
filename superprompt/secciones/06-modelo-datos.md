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
