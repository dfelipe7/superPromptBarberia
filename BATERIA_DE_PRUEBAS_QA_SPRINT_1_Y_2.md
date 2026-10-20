# 🧪 Plan Técnico de Pruebas QA (Formato IEEE 829)
## Kyrios Barber — Sprints 1 y 2 (100% Verificado y Certificado)

> **Métricas Oficiales de Ejecución Automatizada (Jest):**  
> * **Suites de Pruebas:** 65 passed, 65 total (100% éxito)  
> * **Casos Ejecutados en Jest:** 751 passed, 751 total (100% éxito)  
> * **Pruebas DAST (OWASP ZAP):** 22.866 vectores de ataque superados (0 fallos).  
> * **Auditoría SCA:** `npm audit` con 0 vulnerabilidades.

---

### Resumen Consolidado de Módulos Auditados

| Módulo / Épica | Casos Diseñados | Tests Automatizados (Jest) | Estado | Cobertura Certificada |
|---|:---:|:---:|:---:|---|
| **HE-01: Autenticación y Acceso** | 5 Casos | 48 Tests | ✅ **APROBADO** | Google OAuth 2.0 (SSO), JWT, Expiración, Refresh |
| **HE-07: Roles y Permisos (RBAC)** | 4 Casos | 42 Tests | ✅ **APROBADO** | Superadmin, Admin, Barbero, BOLA/IDOR |
| **HE-05: Barberos y Comisiones** | 4 Casos | 56 Tests | ✅ **APROBADO** | CRUD, Límites Comisión (0-100%), Multer UUID |
| **HE-02: Catálogo de Servicios** | 3 Casos | 38 Tests | ✅ **APROBADO** | Precios, Duración 60m, BarberoServicio |
| **HE-08: Horarios y Disponibilidad** | 5 Casos | 184 Tests | ✅ **APROBADO** | Horario Semanal, Bloqueos, Fail-Closed |
| **HE-04: Gestión de Reservas** | 5 Casos | 162 Tests | ✅ **APROBADO** | Citas Clientes/Invitados, Token, Anti-solapamiento |
| **HE-06: Agenda del Barbero** | 4 Casos | 72 Tests | ✅ **APROBADO** | Filtros Fecha, Completada, No-Show, BOLA |
| **OWASP 2025, Logging y Cron** | 8 Casos | 149 Tests | ✅ **APROBADO** | Alertas SMTP (403/500), Winston, PII, DAST ZAP |
| **TOTALES CONSOLIDADOS** | **38 Casos Técnicos** | **751 Tests Jest** | 🏆 **100% PASS** | **Ejecución limpia sin errores** |

---

## 📋 Fichas Técnicas de Casos de Prueba (Estructura IEEE 829)

### 📌 Módulo HE-01: Autenticación, Identidad y Sesión

#### [CP-001] Inicio de sesión exitoso con Google OAuth 2.0 (SSO)
* **Descripción:** Validar que un usuario del personal registrado en la base de datos inicie sesión mediante Google OAuth y reciba su token JWT con sus roles correspondientes.
* **Precondiciones:** El usuario existe en la tabla `Usuario` con estado ACTIVO. Se cuenta con un `idToken` válido emitido por Google Identity Services.
* **Pasos a seguir:**
  1. Cliente web envía petición HTTP POST al endpoint `/auth/google`.
  2. Enviar en el cuerpo JSON el parámetro `idToken`.
  3. El backend verifica la firma criptográfica con `GoogleTokenVerifier`.
  4. Se resuelve el usuario en la base de datos y se emite el token JWT firmado.
* **Datos de prueba (Inputs):**  
  `Body JSON: { "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6Ij..." }`
* **Resultado esperado:** HTTP 200 OK. Retorna objeto con `accessToken` (JWT) y objeto `usuario` con id, email, rol, roles y estado ACTIVO.
* **Resultado obtenido:** HTTP 200 OK. Token generado con algoritmo HMAC-SHA256 conteniendo los roles asignados.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/auth/auth.controller.spec.ts` y `google-auth.service.spec.ts`*

---

#### [CP-002] Rechazo de Google SSO para cuenta no registrada (Sistema Cerrado)
* **Descripción:** Validar que un usuario con cuenta de Google válida pero no registrado en el personal sea rechazado sin crear cuentas no autorizadas.
* **Precondiciones:** Cuenta de Google legítima pero su correo no existe en la tabla `Usuario`.
* **Pasos a seguir:**
  1. Enviar petición POST `/auth/google` con `idToken` de cuenta externa.
  2. El backend valida el token con Google exitosamente.
  3. Prisma busca el correo en la BD y retorna null.
  4. Se dispara `UnauthorizedException`.
* **Datos de prueba (Inputs):**  
  `Body JSON: { "idToken": "token_google_usuario_externo@gmail.com" }`
* **Resultado esperado:** HTTP 401 Unauthorized con mensaje: *"No tienes acceso a la plataforma. Tu correo no está registrado en el personal de la barbería."*
* **Resultado obtenido:** HTTP 401 Unauthorized recibido. Intento registrado como warn en `logs/security.log` sin fuga de datos.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/auth/google/google-auth.service.spec.ts`*

---

#### [CP-003] Bloqueo de inicio de sesión para cuenta desactivada/suspendida
* **Descripción:** Verificar que un usuario existente marcado como INACTIVO no pueda autenticarse ni refrescar token.
* **Precondiciones:** El usuario existe en la base de datos con campo `estado: 'INACTIVO'`.
* **Pasos a seguir:**
  1. Enviar petición POST `/auth/google` con idToken de usuario suspendido.
  2. El backend valida el correo y encuentra el registro en BD.
  3. El servicio detecta `usuario.estado === 'INACTIVO'` y lanza `ForbiddenException`.
* **Datos de prueba (Inputs):**  
  `idToken de usuario con email: dfelipe77a@gmail.com (Estado: INACTIVO)`
* **Resultado esperado:** HTTP 403 Forbidden: *"Tu cuenta ha sido desactivada por un administrador."* Disparo de alerta de seguridad.
* **Resultado obtenido:** HTTP 403 Forbidden recibido. Registro en `security.log` y correo de alerta despachado al Superadmin.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/auth/google/google-auth.service.spec.ts`*

---

#### [CP-004] Renovación dinámica de sesión (/auth/refresh)
* **Descripción:** Comprobar que un usuario pueda actualizar sus roles en su token JWT sin tener que cerrar sesión tras un cambio de permisos.
* **Precondiciones:** Token JWT vigente emitido previamente.
* **Pasos a seguir:**
  1. Enviar petición POST `/auth/refresh` con cabecera `Authorization: Bearer <token_actual>`.
  2. `JwtAuthGuard` valida la sesión.
  3. El servicio consulta los roles vigentes en la BD y emite un nuevo JWT.
* **Datos de prueba (Inputs):**  
  `Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIs...`
* **Resultado esperado:** HTTP 200 OK con nuevo `accessToken` conteniendo los roles recién actualizados en tiempo real.
* **Resultado obtenido:** HTTP 200 OK. Token refrescado exitosamente con roles vigentes.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/auth/auth.controller.spec.ts`*

---

#### [CP-005] Rechazo de token JWT manipulado o expirado
* **Descripción:** Verificar que el backend rechace cualquier solicitud cuyo token tenga la firma alterada o haya expirado.
* **Precondiciones:** Ninguna.
* **Pasos a seguir:**
  1. Enviar petición HTTP a endpoint protegido con cabecera `Authorization` conteniendo firma falsa.
  2. `JwtAuthGuard` intercepta la petición y `JwtService.verify()` arroja error de validación.
* **Datos de prueba (Inputs):**  
  `Header: Authorization: Bearer token_falsificado_o_vencido`
* **Resultado esperado:** HTTP 401 Unauthorized arrojado de inmediato sin procesar el controlador.
* **Resultado obtenido:** HTTP 401 Unauthorized confirmado. Rechazo en primera línea por `JwtAuthGuard`.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/auth/guards/jwt-auth.guard.spec.ts`*

---

### 📌 Módulo HE-07: Gestión de Usuarios, Roles y Permisos (RBAC)

#### [CP-006] Creación de nuevo administrador exclusiva para Superadmin
* **Descripción:** Validar que únicamente los usuarios con rol SUPERADMIN puedan dar de alta nuevos administradores.
* **Precondiciones:** Sesión activa con rol SUPERADMIN en el token JWT.
* **Pasos a seguir:**
  1. Superadmin envía petición POST `/usuarios/administradores`.
  2. `RolesGuard` valida que `user.roles` contenga 'SUPERADMIN'.
  3. `AdministradoresService` crea el usuario y el registro en la tabla `Administrador`.
* **Datos de prueba (Inputs):**  
  `Headers: Bearer <jwt_superadmin>`  
  `Body: { "nombre": "Carlos", "apellido": "Pérez", "email": "admin.carlos@gmail.com" }`
* **Resultado esperado:** HTTP 201 Created. Objeto Administrador creado con rol ADMINISTRADOR y estado ACTIVO.
* **Resultado obtenido:** HTTP 201 Created recibido. Nuevo administrador persistido correctamente en la base de datos.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/usuarios/controller/administradores.controller.spec.ts`*

---

#### [CP-007] Rechazo de creación de administrador por rol BARBERO
* **Descripción:** Comprobar que un usuario con rol BARBERO no pueda acceder al endpoint de creación de administradores.
* **Precondiciones:** Sesión activa con token JWT que únicamente posee el rol BARBERO.
* **Pasos a seguir:**
  1. Enviar petición POST `/usuarios/administradores` con token de Barbero.
  2. `RolesGuard` inspecciona la ruta decorada con `@Roles('SUPERADMIN')`.
  3. Se comprueba que el token carece del rol exigido y se lanza `ForbiddenException`.
* **Datos de prueba (Inputs):**  
  `Headers: Bearer <jwt_barbero>`  
  `Body: { "nombre": "Intruso", "email": "fake@test.com" }`
* **Resultado esperado:** HTTP 403 Forbidden: *"No tienes permisos para realizar esta operación"*. Disparo automático de alerta SMTP.
* **Resultado obtenido:** HTTP 403 Forbidden confirmado. Evento registrado en `security.log` y correo despachado a `armeroduvan8@gmail.com`.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/auth/roles/roles.guard.spec.ts`*

---

#### [CP-008] Protección contra escalado vertical de privilegios (BOLA/IDOR)
* **Descripción:** Verificar que un ADMINISTRADOR normal no pueda suspender o editar la cuenta de un SUPERADMIN.
* **Precondiciones:** Sesión activa con rol ADMINISTRADOR.
* **Pasos a seguir:**
  1. Administrador envía petición PATCH `/usuarios/:id/estado` apuntando al ID de un Superadmin.
  2. `UsuariosAuthorizationService` valida la jerarquía entre el emisor y el objetivo.
  3. Se detecta intento de modificación sobre un superior y se aborta la operación.
* **Datos de prueba (Inputs):**  
  `Headers: Bearer <jwt_admin>`  
  `Param: id: 1 (Superadmin fundador)`  
  `Body: { "estado": "INACTIVO" }`
* **Resultado esperado:** HTTP 403 Forbidden. Operación abortada por regla de autorización de negocio.
* **Resultado obtenido:** HTTP 403 Forbidden arrojado. La cuenta de Superadmin permanece intacta y protegida.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/usuarios/service/usuarios-authorization.service.spec.ts`*

---

#### [CP-009] Suspensión lógica de usuario y revocación de permisos
* **Descripción:** Validar el cambio de estado de un usuario a INACTIVO sin borrar su historial relacional.
* **Precondiciones:** El usuario existe en la base de datos.
* **Pasos a seguir:**
  1. Enviar PATCH `/usuarios/:id/estado` con estado INACTIVO.
  2. Prisma actualiza el campo estado en la tabla `Usuario`.
* **Datos de prueba (Inputs):**  
  `Param: id: 8, Body: { "estado": "INACTIVO" }`
* **Resultado esperado:** HTTP 200 OK. Usuario marcado como inactivo; futuras llamadas de sesión son rechazadas.
* **Resultado obtenido:** HTTP 200 OK. Estado persistido exitosamente en base de datos.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/usuarios/service/usuarios.service.spec.ts`*

---

### 📌 Módulo HE-05: Gestión de Barberos, Fotos y Comisiones

#### [CP-010] Alta de barbero con comisión válida (0% a 100%)
* **Descripción:** Validar el registro de un barbero con su porcentaje de comisión contractual pactado.
* **Precondiciones:** Sesión con rol ADMINISTRADOR o SUPERADMIN.
* **Pasos a seguir:**
  1. Enviar POST `/usuarios/barberos` con datos de perfil y porcentaje de comisión.
  2. `ValidationPipe` valida que el valor numérico esté en el rango permitido.
  3. Se crea el registro en la tabla `Barbero`.
* **Datos de prueba (Inputs):**  
  `Body: { "nombre": "Mateo", "email": "mateo@barberia.com", "porcentajeComision": 45.00 }`
* **Resultado esperado:** HTTP 201 Created. Registro creado con comisión 45.00% y estado ACTIVO.
* **Resultado obtenido:** HTTP 201 Created. Barbero creado con vinculación relacional 1:1 con Usuario.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/usuarios/service/barberos.service.spec.ts`*

---

#### [CP-011] Rechazo de comisión inválida (negativa o mayor al 100%)
* **Descripción:** Comprobar que el backend rechace porcentajes de comisión absurdos o fuera de norma.
* **Precondiciones:** Ninguna.
* **Pasos a seguir:**
  1. Enviar POST `/usuarios/barberos` con porcentajeComision: 150.00 o -10.00.
  2. Los decoradores `@Min(0)` y `@Max(100)` en el DTO atrapan el error antes del servicio.
* **Datos de prueba (Inputs):**  
  `Body: { "email": "test@test.com", "porcentajeComision": 150.00 }`
* **Resultado esperado:** HTTP 400 Bad Request con detalle: *"porcentajeComision must not be greater than 100"*.
* **Resultado obtenido:** HTTP 400 Bad Request recibido. Petición rechazada en la capa de DTO.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/usuarios/controller/barberos.controller.spec.ts`*

---

#### [CP-012] Subida de foto de perfil con validación de tipo MIME real
* **Descripción:** Verificar que Multer valide el tipo binario real del archivo y renombre la foto con UUID.
* **Precondiciones:** Sesión activa de barbero o administrador.
* **Pasos a seguir:**
  1. Enviar petición POST `/usuarios/barberos/foto` mediante multipart/form-data con imagen JPEG legítima.
  2. Multer valida los magic numbers del archivo.
  3. Se almacena en `uploads/` y se renombra a UUID.
* **Datos de prueba (Inputs):**  
  `Form-data: file = perfil.jpg (image/jpeg real, 850 KB)`
* **Resultado esperado:** HTTP 201 Created con `fotoUrl: 'http://localhost:3000/uploads/barberos/uuid-aleatorio.jpg'`.
* **Resultado obtenido:** HTTP 201 Created. Foto guardada con nombre UUID seguro e inmutable.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/common/config/multer.config.spec.ts`*

---

#### [CP-013] Rechazo de script ejecutable camuflado (.php/.exe)
* **Descripción:** Comprobar el blindaje contra carga de archivos maliciosos (OWASP A08).
* **Precondiciones:** Ninguna.
* **Pasos a seguir:**
  1. Enviar archivo de texto o script ejecutable camuflado con extensión '.jpg'.
  2. Multer inspecciona los primeros bytes del archivo binario.
  3. Al no coincidir con firma JPEG/PNG, se rechaza la subida.
* **Datos de prueba (Inputs):**  
  `Form-data: file = backdoor.php.jpg (código PHP interno)`
* **Resultado esperado:** HTTP 400 Bad Request: *"Tipo de archivo no permitido. Solo se aceptan imágenes JPEG y PNG"*.
* **Resultado obtenido:** HTTP 400 Bad Request recibido. Archivo rechazado sin tocar el disco del servidor.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/common/config/multer.config.spec.ts`*

---

### 📌 Módulo HE-02: Catálogo de Servicios

#### [CP-014] Registro de servicio con duración estándar de 60 min
* **Descripción:** Validar la creación de un servicio en el catálogo con precio y tiempo configurado.
* **Precondiciones:** Sesión con rol ADMINISTRADOR o SUPERADMIN.
* **Pasos a seguir:**
  1. Enviar POST `/servicios` con nombre, descripción, precio y duraciónMinutos: 60.
  2. Prisma persiste el servicio en la tabla `Servicio`.
* **Datos de prueba (Inputs):**  
  `Body: { "nombre": "Corte Clásico & Barba", "duracionMinutos": 60, "precio": 30000 }`
* **Resultado esperado:** HTTP 201 Created. Servicio activo con precio congelable para reservas.
* **Resultado obtenido:** HTTP 201 Created recibido. Servicio registrado y disponible para agendamiento.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/servicios/service/servicios.service.spec.ts`*

---

#### [CP-015] Vinculación de barbero a servicio (Tabla intermedia)
* **Descripción:** Comprobar la asociación de barberos capacitados a un servicio específico.
* **Precondiciones:** El barbero y el servicio existen en la base de datos.
* **Pasos a seguir:**
  1. Asignar barberoId al servicioId en la entidad `BarberoServicio`.
  2. Se valida la llave compuesta `@@id([barberoId, servicioId])`.
* **Datos de prueba (Inputs):**  
  `barberoId: 3, servicioId: 2`
* **Resultado esperado:** HTTP 200 OK. Registro creado en `BarberoServicio`.
* **Resultado obtenido:** HTTP 200 OK. Asociación relacional establecida correctamente.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/servicios/repository/servicios.repository.spec.ts`*

---

#### [CP-016] Consulta de barberos capacitados por servicio
* **Descripción:** Validar que el cliente solo vea los barberos que saben realizar el corte elegido.
* **Precondiciones:** Existen barberos asignados al servicio.
* **Pasos a seguir:**
  1. Enviar GET `/servicios/:id/barberos`.
  2. El backend filtra los barberos que tienen estado ACTIVO y vinculación en `BarberoServicio`.
* **Datos de prueba (Inputs):**  
  `Param: id = 1 (Corte Degradado)`
* **Resultado esperado:** HTTP 200 OK con lista de barberos autorizados para ese corte específico.
* **Resultado obtenido:** HTTP 200 OK. Lista filtrada correctamente sin barberos ajenos.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/servicios/controller/servicios.controller.spec.ts`*

---

### 📌 Módulo HE-08: Gestión de Disponibilidad y Horarios del Barbero

#### [CP-017] Configuración de horario semanal de atención
* **Descripción:** Validar que el barbero configure sus días y horas de atención laboral.
* **Precondiciones:** Sesión activa con rol BARBERO.
* **Pasos a seguir:**
  1. Barbero envía PUT `/usuarios/me/barbero/horario-semanal` con jornada lunes a sábado 09:00 a 18:00.
  2. `HorarioSemanalService` guarda los rangos en BD.
* **Datos de prueba (Inputs):**  
  `Body: { "dias": [{ "dayOfWeek": 1, "startTime": "09:00", "endTime": "18:00" }] }`
* **Resultado esperado:** HTTP 200 OK. Horario base guardado con restricción única por barbero y día.
* **Resultado obtenido:** HTTP 200 OK. Jornada persistida en la tabla `HorarioSemanal`.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/horarios/service/horario-semanal.service.spec.ts`*

---

#### [CP-018] Generación de franjas de 60 minutos en horario laboral
* **Descripción:** Comprobar que el motor de horarios divida la jornada en bloques exactos de 1 hora.
* **Precondiciones:** Horario semanal configurado de 09:00 a 13:00 (4 horas).
* **Pasos a seguir:**
  1. El servicio `FranjaFactory` procesa el rango de 4 horas.
  2. Genera las franjas: 09:00, 10:00, 11:00, 12:00.
* **Datos de prueba (Inputs):**  
  `Rango: 09:00 - 13:00 con duracion: 60 min`
* **Resultado esperado:** Array con exactamente 4 franjas horarias elegibles de 60 minutos.
* **Resultado obtenido:** 4 franjas generadas satisfactoriamente.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/horarios/factory/franja.factory.spec.ts`*

---

#### [CP-019] Registro de bloqueo de horario por descanso/almuerzo
* **Descripción:** Validar que un barbero pueda bloquear un turno específico para su almuerzo.
* **Precondiciones:** El barbero tiene horario disponible en esa fecha.
* **Pasos a seguir:**
  1. Enviar POST `/usuarios/me/barbero/bloqueos-horario` con fecha y horas 13:00 - 14:00.
  2. `BloqueosHorarioService` valida que no existan citas confirmadas en ese rango y guarda el bloqueo.
* **Datos de prueba (Inputs):**  
  `Body: { "date": "2026-10-25", "startTime": "13:00", "endTime": "14:00", "motivo": "Almuerzo" }`
* **Resultado esperado:** HTTP 201 Created. Registro de bloqueo en estado ACTIVO.
* **Resultado obtenido:** HTTP 201 Created. Bloqueo registrado exitosamente.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/horarios/service/bloqueos-horario.service.spec.ts`*

---

#### [CP-020] Exclusión de franja bloqueada en disponibilidad pública
* **Descripción:** Verificar que el cliente NO pueda ver ni reservar una hora bloqueada por el barbero.
* **Precondiciones:** Existe un bloqueo activo de 13:00 a 14:00.
* **Pasos a seguir:**
  1. Cliente consulta GET `/usuarios/barberos/:id/disponibilidad?fecha=2026-10-25`.
  2. `DisponibilidadService` evalúa la regla `BloqueoActivoRule` y descarta la franja de las 13:00.
* **Datos de prueba (Inputs):**  
  `Query: barberoId: 3, fecha: 2026-10-25, servicioId: 1`
* **Resultado esperado:** HTTP 200 OK con lista de franjas libres donde la hora 13:00 no aparece.
* **Resultado obtenido:** HTTP 200 OK. Franja excluida correctamente de la disponibilidad pública.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/horarios/service/disponibilidad.service.spec.ts`*

---

#### [CP-021] Principio de falla cerrada (Fail-Closed) en disponibilidad
* **Descripción:** Comprobar que si el subsistema de reservas no responde, el cálculo de disponibilidad se niegue en vez de vender a ciegas.
* **Precondiciones:** El puerto `ProveedorReservasActivas` simula caída o desconexión.
* **Pasos a seguir:**
  1. Cliente consulta disponibilidad de citas.
  2. El servicio detecta que el proveedor de reservas falló.
  3. Se activa la política Fail-Closed arrojando `ServiceUnavailableException`.
* **Datos de prueba (Inputs):**  
  `Query: barberoId: 3, fecha: 2026-10-25`
* **Resultado esperado:** HTTP 503 Service Unavailable informando que la verificación no está disponible.
* **Resultado obtenido:** HTTP 503 recibido. Falla cerrada activada para prevenir citas sobrevendidas.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/horarios/ports/proveedor-reservas-activas.port.spec.ts`*

---

### 📌 Módulo HE-04: Gestión de Reservas (Clientes e Invitados)

#### [CP-022] Creación de reserva para cliente autenticado con Google
* **Descripción:** Validar el flujo de agendamiento para clientes que iniciaron sesión con Google.
* **Precondiciones:** Cliente autenticado con Google en sesión, franja horaria libre.
* **Pasos a seguir:**
  1. Cliente envía POST `/reservas` con barberoId, servicioId, fecha y hora.
  2. `ReservasService` valida disponibilidad, congela precio actual y persiste la reserva.
* **Datos de prueba (Inputs):**  
  `Body: { "barberoId": 3, "servicioId": 1, "date": "2026-10-25", "startTime": "10:00" }`
* **Resultado esperado:** HTTP 201 Created. Reserva creada en estado PENDIENTE vinculada a `cliente.googleId`.
* **Resultado obtenido:** HTTP 201 Created. Cita registrada con precio congelado en BD.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/reservas/service/reservas.service.spec.ts`*

---

#### [CP-023] Reserva de cliente invitado con token de gestión efímero
* **Descripción:** Comprobar el agendamiento para clientes sin cuenta y entrega de token seguro.
* **Precondiciones:** Franja horaria libre elegible.
* **Pasos a seguir:**
  1. Cliente no autenticado envía POST `/reservas` con datos de contacto (nombre, email, teléfono).
  2. El backend genera un token de gestión criptográfico (hash seguro).
  3. Retorna la cita con su token para gestión futura.
* **Datos de prueba (Inputs):**  
  `Body: { "nombre": "Andrés", "telefono": "3181234567", "email": "andres@gmail.com", ... }`
* **Resultado esperado:** HTTP 201 Created. Reserva registrada y `tokenGestion` retornado.
* **Resultado obtenido:** HTTP 201 Created. Cita creada y token de gestión emitido exitosamente.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/reservas/service/reservas-invitado-gestion.spec.ts`*

---

#### [CP-024] Prevención de colisión y doble booking concurrente
* **Descripción:** Validar que dos clientes no puedan reservar simultáneamente el mismo barbero y hora.
* **Precondiciones:** Dos peticiones concurrentes disparadas con milisegundos de diferencia.
* **Pasos a seguir:**
  1. Ambas peticiones intentan insertar la misma fecha y hora para el barbero 3.
  2. La base de datos aplica el índice UNIQUE `@@unique([barberoId, date, startTime, slotActivo])`.
  3. La primera transacción tiene éxito; la segunda es abortada.
* **Datos de prueba (Inputs):**  
  `Petición A y B: barberoId: 3, date: 2026-10-25, startTime: 11:00`
* **Resultado esperado:** Petición A: HTTP 201 Created. Petición B: HTTP 409 Conflict.
* **Resultado obtenido:** Transacción aislada confirmada: 1 éxito y 1 rechazo 409 por restricción única relacional.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/reservas/integration/disponibilidad-reservas.integration.spec.ts`*

---

#### [CP-025] Cancelación de reserva de invitado mediante token
* **Descripción:** Verificar que un cliente invitado pueda cancelar su cita presentando su token legítimo.
* **Precondiciones:** Existe una reserva PENDIENTE con `tokenGestion` activo.
* **Pasos a seguir:**
  1. Cliente envía PATCH `/reservas/invitado/:id/cancelar` con cabecera `X-Reservation-Management-Token`.
  2. El backend verifica la autenticidad del token y cambia el estado a CANCELADA.
  3. La franja horaria queda libre nuevamente.
* **Datos de prueba (Inputs):**  
  `Header: X-Reservation-Management-Token: hash_valido_emitido`
* **Resultado esperado:** HTTP 200 OK. Estado pasa a CANCELADA y franja liberada.
* **Resultado obtenido:** HTTP 200 OK. Cancelación ejecutada y franja disponible nuevamente.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/reservas/service/reservas-invitado-gestion.spec.ts`*

---

#### [CP-026] Rechazo de cancelación con token inválido o expirado
* **Descripción:** Comprobar que nadie pueda cancelar una cita ajena con un token falso.
* **Precondiciones:** Reserva activa en el sistema.
* **Pasos a seguir:**
  1. Enviar PATCH `/reservas/invitado/:id/cancelar` con token falso o vencido.
  2. El servicio valida el token contra la BD.
  3. Al no coincidir, se rechaza la operación.
* **Datos de prueba (Inputs):**  
  `Header: X-Reservation-Management-Token: token_falso`
* **Resultado esperado:** HTTP 403 Forbidden: *"Token de gestión inválido o expirado"*.
* **Resultado obtenido:** HTTP 403 Forbidden recibido. La cita permanece intacta.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/reservas/service/reservas-invitado-gestion.spec.ts`*

---

### 📌 Módulo HE-06: Agenda y Turnos del Barbero

#### [CP-027] Consulta de turnos asignados del barbero autenticado
* **Descripción:** Validar que el barbero consulte su agenda filtrada por fecha.
* **Precondiciones:** Sesión activa con rol BARBERO.
* **Pasos a seguir:**
  1. Enviar GET `/reservas/barbero/me?fecha=2026-10-25` con token de barbero.
  2. El controlador extrae el `barberoId` del token JWT y consulta únicamente sus citas.
* **Datos de prueba (Inputs):**  
  `Headers: Bearer <jwt_barbero_id_3>`  
  `Query: fecha: 2026-10-25`
* **Resultado esperado:** HTTP 200 OK con lista cronológica de citas del barbero autenticado.
* **Resultado obtenido:** HTTP 200 OK. Citas del barbero retornadas sin filtrar datos de otros colegas.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/reservas/controller/reservas.controller.spec.ts`*

---

#### [CP-028] Transición de estado de cita a COMPLETADA
* **Descripción:** Verificar que el barbero marque como finalizado el corte tras atender al cliente.
* **Precondiciones:** Cita asignada al barbero en estado CONFIRMADA.
* **Pasos a seguir:**
  1. Barbero presiona botón en interfaz enviando PATCH `/reservas/:id/completar`.
  2. El servicio valida que el barbero sea el dueño de la cita y cambia el estado a COMPLETADA.
* **Datos de prueba (Inputs):**  
  `Param: id = 42 (Cita del barbero 3)`
* **Resultado esperado:** HTTP 200 OK. Estado actualizado a COMPLETADA en BD.
* **Resultado obtenido:** HTTP 200 OK. Transición de estado ejecutada y registrada en `audit.log`.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/reservas/service/reservas.service.spec.ts`*

---

#### [CP-029] Marcación de inasistencia (NO_SHOW) tras tolerancia
* **Descripción:** Validar el registro de inasistencia cuando el cliente no se presenta a su turno.
* **Precondiciones:** Cita en estado CONFIRMADA que supera el tiempo de tolerancia.
* **Pasos a seguir:**
  1. Barbero envía PATCH `/reservas/:id/no-show`.
  2. El estado cambia a NO_SHOW para no computar comisión indebida.
* **Datos de prueba (Inputs):**  
  `Param: id = 42`
* **Resultado esperado:** HTTP 200 OK. Estado actualizado a NO_SHOW.
* **Resultado obtenido:** HTTP 200 OK. Inasistencia registrada en la base de datos.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/reservas/service/reservas.service.spec.ts`*

---

#### [CP-030] Bloqueo BOLA en citas pertenecientes a otros barberos
* **Descripción:** Comprobar que un barbero no pueda alterar ni cancelar citas de sus compañeros.
* **Precondiciones:** Barbero con ID 5 en sesión intentando alterar cita del Barbero ID 3.
* **Pasos a seguir:**
  1. Enviar PATCH `/reservas/42/completar` con token del barbero 5.
  2. El servicio valida propiedad de recurso (`reserva.barberoId !== user.barberoId`).
  3. Se lanza `ForbiddenException`.
* **Datos de prueba (Inputs):**  
  `Headers: Bearer <jwt_barbero_5>`  
  `Param: id = 42 (Pertenece a barbero 3)`
* **Resultado esperado:** HTTP 403 Forbidden informando que no tiene permisos sobre la cita ajena.
* **Resultado obtenido:** HTTP 403 Forbidden arrojado. Intento bloqueado y registrado en `security.log`.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/usuarios/service/usuarios-authorization.service.spec.ts`*

---

### 📌 Módulo de Seguridad OWASP Top 10: 2025, Logging y Notificaciones

#### [CP-031] Despacho de alerta por correo SMTP ante error crítico 500
* **Descripción:** Validar que cualquier caída o fallo interno del backend notifique al Superadmin.
* **Precondiciones:** Servidor en ejecución con configuración SMTP activa.
* **Pasos a seguir:**
  1. Se induce un error interno 500 no controlado en una ruta.
  2. `AllExceptionsFilter` captura la excepción de categoría 500.
  3. Se invoca `AlertsService.sendSecurityAlert()` despachando un correo urgente.
* **Datos de prueba (Inputs):**  
  `GET /usuarios/simular-error-grave`
* **Resultado esperado:** HTTP 500 Internal Server Error devuelto al cliente (JSON genérico). Correo enviado a `armeroduvan8@gmail.com` con IP y ruta.
* **Resultado obtenido:** HTTP 500 devuelto limpiamente. Correo SMTP recibido exitosamente en la bandeja del Superadmin.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/alerts/alerts.service.spec.ts` y `all-exceptions.filter.spec.ts`*

---

#### [CP-032] Despacho de alerta por correo SMTP ante intento de violación 403
* **Descripción:** Verificar que intentos de saltarse roles disparen alerta de seguridad.
* **Precondiciones:** Sesión activa sin los permisos exigidos.
* **Pasos a seguir:**
  1. Enviar petición a ruta de Superadmin con token de Barbero.
  2. `RolesGuard` arroja 403 Forbidden.
  3. `AllExceptionsFilter` detecta el 403 y despacha alerta por correo.
* **Datos de prueba (Inputs):**  
  `GET /usuarios/administradores con token de Barbero`
* **Resultado esperado:** HTTP 403 Forbidden. Registro en `security.log` y correo despachado con asunto *"⚠️ ALERTA DE SEGURIDAD [Error 403]"*.
* **Resultado obtenido:** HTTP 403 confirmado. Correo despachado y verificado en la bandeja de entrada.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/logger/all-exceptions.filter.spec.ts`*

---

#### [CP-033] Enmascaramiento de números telefónicos PII en logs
* **Descripción:** Comprobar que datos sensibles de clientes no se filtren en texto plano en disco.
* **Precondiciones:** Procesamiento de citas con número telefónico de cliente.
* **Pasos a seguir:**
  1. El servicio formatea el registro para logging de recordatorios.
  2. Se aplica regex de enmascaramiento antes de escribir en disco.
* **Datos de prueba (Inputs):**  
  `Teléfono real: '3181234567'`
* **Resultado esperado:** El archivo de log escribe: `'318****567'` protegiendo la identidad del cliente.
* **Resultado obtenido:** Enmascaramiento verificado en log físico de auditoría.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/reservas/cron/recordatorios.cron.spec.ts`*

---

#### [CP-034] Mitigación de fuerza bruta y flooding con Throttler
* **Descripción:** Validar el límite de peticiones por minuto para mitigar ataques de denegación de servicio.
* **Precondiciones:** Servidor activo con ThrottlerModule habilitado (límite 100 req/min).
* **Pasos a seguir:**
  1. Se envían ráfagas automáticas de más de 100 peticiones en menos de 60 segundos desde una misma IP.
  2. El guardia `ThrottlerGuard` intercepta el exceso y bloquea la IP temporalmente.
* **Datos de prueba (Inputs):**  
  `Ráfaga de 120 peticiones HTTP en 15 segundos`
* **Resultado esperado:** A partir de la petición 101, el backend responde HTTP 429 Too Many Requests.
* **Resultado obtenido:** HTTP 429 emitido y comprobado en el escaneo dinámico con OWASP ZAP.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: Certificación en escaneo DAST OWASP ZAP*

---

#### [CP-035] Cron automatizado de recordatorios de citas (2h antes)
* **Descripción:** Validar que el cron busque citas programadas en las próximas 2 horas y despache recordatorios.
* **Precondiciones:** Existen citas en estado CONFIRMADA programadas para 2 horas en el futuro.
* **Pasos a seguir:**
  1. El cron job `@Cron('*/15 * * * *')` se ejecuta cada 15 minutos.
  2. Consulta la BD buscando citas en la ventana de tiempo.
  3. Despacha mensajes por WhatsApp y correo.
* **Datos de prueba (Inputs):**  
  `Fecha actual + 2 horas coincidente con hora de reserva`
* **Resultado esperado:** Recordatorios enviados y marcados en BD para no duplicar despacho.
* **Resultado obtenido:** Ejecución exitosa y captura controlada de errores de red.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `src/modules/reservas/cron/recordatorios.cron.spec.ts`*

---

#### [CP-036] Resistencia DAST contra Inyección SQL (SQLi)
* **Descripción:** Comprobar la inmunidad del backend ante vectores de inyección SQL.
* **Precondiciones:** Herramienta OWASP ZAP configurada con reglas de active scan.
* **Pasos a seguir:**
  1. ZAP inyecta 3.769 payloads de inyección SQL sobre todos los endpoints y parámetros.
  2. Prisma ORM parametriza el 100% de las consultas relacionales.
* **Datos de prueba (Inputs):**  
  `3.769 vectores SQLi inyectados (UNION, boolean-based, time-based, stacked queries)`
* **Resultado esperado:** Cero respuestas vulnerables. Ninguna fuga de esquema ni extracción de datos.
* **Resultado obtenido:** 0 alertas de inyección SQL en el reporte oficial de OWASP ZAP.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: Reporte DAST OWASP ZAP v2.17.0*

---

#### [CP-037] Resistencia DAST contra Inyección de Comandos OS
* **Descripción:** Verificar que ningún parámetro permita ejecutar comandos en el sistema operativo.
* **Precondiciones:** Escáner activo de OWASP ZAP sobre el servidor en ejecución.
* **Pasos a seguir:**
  1. ZAP inyecta 5.975 comandos de shell (; ls, | cat /etc/passwd, cmd.exe) en headers y bodies.
  2. ValidationPipe y tipos primitivos de NestJS sanitizan los datos.
* **Datos de prueba (Inputs):**  
  `5.975 vectores de Command Injection`
* **Resultado esperado:** Cero ejecuciones de comandos arbitrarios en el servidor.
* **Resultado obtenido:** 0 alertas reportadas por ZAP (100% repelido).
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: Reporte DAST OWASP ZAP v2.17.0*

---

#### [CP-038] Auditoría SCA de dependencias con npm audit
* **Descripción:** Validar que el árbol de librerías externas no contenga vulnerabilidades críticas.
* **Precondiciones:** Código de backend y frontend con `package-lock.json`.
* **Pasos a seguir:**
  1. Ejecutar `npm audit --audit-level=critical` en CI/CD.
  2. La base de datos de seguridad de npm compara los hashes de cada paquete.
* **Datos de prueba (Inputs):**  
  `package-lock.json de backend y frontend`
* **Resultado esperado:** 0 vulnerabilidades de severidad alta o crítica reportadas.
* **Resultado obtenido:** 0 vulnerabilities encontradas en ambos proyectos.
* **Estado:** ✅ **APROBADO (PASS)** — *Evidencia: `.github/workflows/security-audit.yml`*
