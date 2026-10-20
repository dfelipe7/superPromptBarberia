# 📱 Plan de Pruebas Funcionales desde la Perspectiva del Usuario (UI/UX)
## Kyrios Barber — Sprints 1 y 2 (Frontend React 19 + TypeScript + Vite)

> **Estándar Aplicado:** IEEE 829 Standard for Software Test Documentation  
> **Enfoque:** Pruebas Funcionales de Caja Negra / End-to-End basadas en la Interacción del Usuario en Pantalla (Clics, Formularios, Alertas y Flujos Visuales).  
> **Formato Requerido por Caso:**  
> 1. ID del caso de prueba  
> 2. Descripción  
> 3. Precondiciones  
> 4. Pasos a seguir  
> 5. Datos de prueba (Inputs)  
> 6. Resultado esperado  
> 7. Resultado obtenido y Estado  

---

## 📊 Matriz Resumen de Pruebas Funcionales (Frontend)

| ID | Módulo / Vista | Funcionalidad Evaluada | Inputs del Usuario | Resultado Obtenido y Estado |
|:---:|:---|:---|:---|:---:|
| **CPF-001** | Portal Público | Navegación en Landing Page y Catálogo de Servicios | Clic en 'Ver Servicios' | ✅ **APROBADO (Pass)** |
| **CPF-002** | Portal Público | Exploración del Equipo de Barberos y Fotos | Clic en enlace 'Barberos' | ✅ **APROBADO (Pass)** |
| **CPF-003** | Portal Público | Flujo Completo de Agendamiento como Invitado (Guest) | Servicio, Barbero, Fecha, Hora, Datos | ✅ **APROBADO (Pass)** |
| **CPF-004** | Portal Público | Bloqueo Visual de Horarios Ocupados (Anti Solapamiento) | Consulta de fecha con turno ocupado | ✅ **APROBADO (Pass)** |
| **CPF-005** | Portal Público | Cancelación de Cita por Cliente (> 2 horas de anticipación) | Clic en 'Cancelar', Motivo | ✅ **APROBADO (Pass)** |
| **CPF-006** | Portal Público | Bloqueo de Cancelación Tardía (< 2 horas de anticipación) | Intento de cancelación a 45 min | ✅ **APROBADO (Pass)** |
| **CPF-007** | Acceso / Login | Inicio de Sesión con Google OAuth 2.0 (Personal) | Clic en 'Continuar con Google' | ✅ **APROBADO (Pass)** |
| **CPF-008** | Acceso / Login | Rechazo de Cuenta Externa no Registrada (Sin Acceso) | Cuenta Google personal no autorizada | ✅ **APROBADO (Pass)** |
| **CPF-009** | Acceso / Login | Bloqueo de Inicio de Sesión a Cuenta Inactiva | Cuenta de colaborador suspendido | ✅ **APROBADO (Pass)** |
| **CPF-010** | Acceso / Login | Cierre de Sesión Seguro (Logout) | Clic en avatar -> 'Cerrar Sesión' | ✅ **APROBADO (Pass)** |
| **CPF-011** | Seguridad UI | Protección de Rutas por URL (RBAC en Navegador) | Ingreso manual a URL de Superadmin | ✅ **APROBADO (Pass)** |
| **CPF-012** | Administración | Creación de Administrador por Superadmin | Formulario: Nombre, Apellido, Correo | ✅ **APROBADO (Pass)** |
| **CPF-013** | Administración | Alta de Barbero con Comisión (0-100%) y Foto | Formulario Barbero + Foto JPG 1 MB | ✅ **APROBADO (Pass)** |
| **CPF-014** | Administración | Validación Visual de Comisión Inválida (>100% o negativa) | Campo Comisión: `150` | ✅ **APROBADO (Pass)** |
| **CPF-015** | Administración | Suspensión de Usuario en Tabla con Modal de Confirmación | Switch Inactivo + Confirmar | ✅ **APROBADO (Pass)** |
| **CPF-016** | Servicios | Creación de Servicio con Duración Estándar de 60 Minutos | Nombre, Tarifa $25.000 COP, 60 min | ✅ **APROBADO (Pass)** |
| **CPF-017** | Servicios | Asignación de Servicios Habilitados para un Barbero | Selección múltiple de checkboxes | ✅ **APROBADO (Pass)** |
| **CPF-018** | Horarios | Configuración de Jornada Semanal (Apertura y Cierre) | Lunes: 08:00 a 18:00 | ✅ **APROBADO (Pass)** |
| **CPF-019** | Horarios | Validación en Pantalla de Horas Incoherentes (Inicio >= Fin) | Inicio: 19:00, Fin: 08:00 | ✅ **APROBADO (Pass)** |
| **CPF-020** | Horarios | Creación de Bloqueo Horario por Descanso o Almuerzo | Fecha, 12:00 a 13:00, 'Almuerzo' | ✅ **APROBADO (Pass)** |
| **CPF-021** | Agenda Barbero | Consulta y Filtrado por Fecha de Citas Asignadas | Selector de Fecha interactivo | ✅ **APROBADO (Pass)** |
| **CPF-022** | Agenda Barbero | Marcar Cita como Completada y Ver Comisión Calculada | Clic en botón 'Completar Cita' | ✅ **APROBADO (Pass)** |
| **CPF-023** | Agenda Barbero | Registro de Inasistencia del Cliente (No-Show) | Clic en botón 'No Asistió' | ✅ **APROBADO (Pass)** |
| **CPF-024** | Agenda Barbero | Creación de Cita Administrativa Manual (Por Teléfono) | Formulario de reserva asistida | ✅ **APROBADO (Pass)** |
| **CPF-025** | Mi Perfil | Actualización de Datos Personales y Teléfono de Contacto | Campo Teléfono: `3201234567` | ✅ **APROBADO (Pass)** |

---

## 📑 Fichas Técnicas Detalladas (Perspectiva de Usuario)

---

### 🌐 Módulo 1: Portal Web Público y Flujo de Clientes e Invitados

#### [CPF-001]
* **ID del caso de prueba:** CPF-001
* **Descripción:** Validar que cualquier visitante pueda explorar los servicios, precios y duración sin necesidad de iniciar sesión.
* **Precondiciones:** Navegador web abierto en la página de inicio (`http://localhost:5173/`). Servidor backend y frontend activos.
* **Pasos a seguir:**  
  1. Ingresar a la URL principal de la barbería.  
  2. Visualizar la sección Hero y hacer clic en el botón *"Ver Servicios"*.  
  3. Navegar por las tarjetas de servicios observando nombre, duración y tarifa en pesos colombianos.
* **Datos de prueba (Inputs):**  
  Clic con ratón en el botón *"Ver Servicios"* de la barra de navegación pública.
* **Resultado esperado:** La página hace scroll suave o navega a `/catalogo/servicios`, renderizando las tarjetas con imagen, título, duración (60 min) y precio en formato COP (ej. $35.000).
* **Resultado obtenido y Estado:** La vista carga de forma fluida, mostrando los servicios configurados con sus precios en pesos colombianos y el botón *"Reservar Cita"*.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-002]
* **ID del caso de prueba:** CPF-002
* **Descripción:** Verificar que el cliente pueda conocer al equipo de barberos y su disponibilidad en el catálogo.
* **Precondiciones:** Estar en la página principal o catálogo público de la barbería.
* **Pasos a seguir:**  
  1. En el menú superior de navegación, hacer clic en *"Barberos"*.  
  2. Visualizar la cuadrícula de perfiles de los profesionales.  
  3. Comprobar que se muestre foto de perfil, nombre del barbero y botón para agendar directamente con él.
* **Datos de prueba (Inputs):**  
  Clic en el enlace *"Barberos"* en la barra de navegación pública.
* **Resultado esperado:** Se despliega la página `/catalogo/barberos` con las tarjetas de los barberos activos, sus fotos cargadas y enlaces de reserva directa.
* **Resultado obtenido y Estado:** Se visualizan las tarjetas de los barberos con sus fotos de perfil cargadas mediante Multer y botón de acción interactivo.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-003]
* **ID del caso de prueba:** CPF-003
* **Descripción:** Validar que un cliente nuevo pueda reservar una cita completando el asistente de agendamiento sin registrarse previamente (Guest Booking).
* **Precondiciones:** Estar en la pantalla de reserva pública (`/reservar`). Existencia de barberos con horarios activos.
* **Pasos a seguir:**  
  1. Ingresar a `/reservar`.  
  2. **Paso 1:** Seleccionar el servicio deseado en la lista interactiva.  
  3. **Paso 2:** Seleccionar el barbero de preferencia.  
  4. **Paso 3:** Escoger una fecha en el calendario interactivo.  
  5. **Paso 4:** Seleccionar una hora disponible de 60 minutos en la cuadrícula de slots.  
  6. **Paso 5:** Diligenciar el formulario con Nombre, Teléfono y Correo Electrónico.  
  7. Hacer clic en *"Confirmar Reserva"*.
* **Datos de prueba (Inputs):**  
  - Servicio: *"Corte Degradado"*  
  - Barbero: *"David Gómez"*  
  - Fecha: *"25/10/2026"*  
  - Hora: *"10:00 AM"*  
  - Nombre: *"Juan Camilo Rojas"*  
  - Teléfono: *"3145678901"*  
  - Email: *"camilo.rojas@gmail.com"*
* **Resultado esperado:** La interfaz bloquea el botón con un spinner de carga, muestra modal/alerta de éxito: *"¡Reserva Confirmada Exitosamente!"*, presenta el código de reserva y despacha correo de confirmación.
* **Resultado obtenido y Estado:** La reserva se procesa en menos de 1 segundo, aparece la pantalla de confirmación con los datos de la cita y el slot queda apartado.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-004]
* **ID del caso de prueba:** CPF-004
* **Descripción:** Comprobar que los turnos ya apartados o bloqueados por descanso no puedan ser seleccionados por otro cliente (Prevención Visual de Doble Reserva).
* **Precondiciones:** Ya existe una cita confirmada para el Barbero David Gómez a las 10:00 AM del 25/10/2026.
* **Pasos a seguir:**  
  1. Un segundo usuario ingresa a `/reservar`.  
  2. Selecciona el mismo servicio y el mismo barbero (*David Gómez*).  
  3. Selecciona la misma fecha (*25/10/2026*).  
  4. Observar la cuadrícula de horarios.
* **Datos de prueba (Inputs):**  
  Fecha: *"25/10/2026"*, Barbero: *"David Gómez"*.
* **Resultado esperado:** El botón del horario *"10:00 AM"* aparece deshabilitado (en gris y no clickeable) o no figura en la lista de turnos disponibles.
* **Resultado obtenido y Estado:** El slot de las 10:00 AM no se renderiza en la cuadrícula de turnos disponibles, imposibilitando visual y físicamente que el cliente cometa un solapamiento.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-005]
* **ID del caso de prueba:** CPF-005
* **Descripción:** Verificar que el cliente pueda cancelar su cita usando su enlace o código de gestión si faltan más de 2 horas para el turno.
* **Precondiciones:** El cliente posee una cita agendada para dentro de 24 horas y tiene su token/enlace de gestión.
* **Pasos a seguir:**  
  1. Acceder al enlace de gestión de la cita proporcionado en la confirmación.  
  2. Visualizar los detalles de la cita y hacer clic en el botón rojo *"Cancelar Cita"*.  
  3. En el modal emergente, escribir el motivo de cancelación.  
  4. Hacer clic en *"Confirmar Cancelación"*.
* **Datos de prueba (Inputs):**  
  Motivo: *"Calamidad doméstica imprevista"*. Clic en *"Confirmar Cancelación"*.
* **Resultado esperado:** El sistema muestra un mensaje de éxito: *"Tu cita ha sido cancelada satisfactoriamente"*. El estado en pantalla cambia a Cancelada y el horario se libera.
* **Resultado obtenido y Estado:** La cita cambia visualmente su badge a color rojo *"Cancelada"* y el turno queda liberado inmediatamente en el calendario.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-006]
* **ID del caso de prueba:** CPF-006
* **Descripción:** Validar que el sistema impida al cliente cancelar una cita cuando faltan menos de 2 horas para la hora pactada.
* **Precondiciones:** Existe una cita programada para dentro de 45 minutos.
* **Pasos a seguir:**  
  1. El cliente ingresa a la vista de gestión de su cita.  
  2. Intentar hacer clic en *"Cancelar Cita"*.
* **Datos de prueba (Inputs):**  
  Intento de cancelación a 45 minutos del turno pactado.
* **Resultado esperado:** El botón *"Cancelar Cita"* aparece deshabilitado con un aviso informativo o, al pulsarlo, el sistema muestra una alerta emergente de advertencia: *"No es posible cancelar con menos de 2 horas de anticipación. Por favor comunícate a la barbería."*
* **Resultado obtenido y Estado:** La aplicación bloquea la acción y muestra un toast descriptivo indicando la política de las 2 horas sin alterar la base de datos.  
  **Estado:** ✅ **APROBADO (Pass)**

---

### 🔐 Módulo 2: Autenticación, Seguridad y Gestión de Sesión

#### [CPF-007]
* **ID del caso de prueba:** CPF-007
* **Descripción:** Validar que un barbero o administrador ingrese al portal interno mediante el botón oficial de Google OAuth 2.0.
* **Precondiciones:** Navegador en la pantalla de login (`http://localhost:5173/login`). Usuario registrado en la base de datos de la barbería.
* **Pasos a seguir:**  
  1. Ingresar a `/login`.  
  2. Hacer clic en el botón *"Continuar con Google"*.  
  3. En la ventana emergente de Google Identity Services, seleccionar la cuenta corporativa autorizada.  
  4. Esperar el procesamiento del token.
* **Datos de prueba (Inputs):**  
  Selección de la cuenta `armeroduvan8@gmail.com` en el diálogo de Google.
* **Resultado esperado:** La ventana emergente se cierra, la interfaz muestra brevemente el spinner de carga y redirige inmediatamente al `/dashboard` mostrando el nombre del usuario y su rol.
* **Resultado obtenido y Estado:** Redirección inmediata al Dashboard, barra de navegación adaptada a sus permisos y sesión persistida en el navegador.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-008]
* **ID del caso de prueba:** CPF-008
* **Descripción:** Comprobar el flujo ante un usuario que intenta ingresar con una cuenta de Google no perteneciente al personal (Sistema Cerrado).
* **Precondiciones:** Estar en `/login`. Poseer una cuenta de Google personal no dada de alta en la barbería.
* **Pasos a seguir:**  
  1. Hacer clic en *"Continuar con Google"*.  
  2. Seleccionar la cuenta externa en el popup de Google.  
  3. El sistema valida contra el backend.
* **Datos de prueba (Inputs):**  
  Cuenta: `usuario.desconocido@gmail.com`.
* **Resultado esperado:** La aplicación no permite el acceso al Dashboard y redirige a la vista `/sin-acceso` mostrando el mensaje: *"No tienes acceso a la plataforma. Tu correo no está registrado en el personal de la barbería."* con un botón para regresar al inicio.
* **Resultado obtenido y Estado:** Redirección controlada a `/sin-acceso` con aviso amigable y botón de retorno al portal público.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-009]
* **ID del caso de prueba:** CPF-009
* **Descripción:** Verificar el comportamiento cuando un colaborador suspendido/inactivo intenta iniciar sesión.
* **Precondiciones:** Colaborador con cuenta marcada como `INACTIVO` en la base de datos.
* **Pasos a seguir:**  
  1. En `/login`, hacer clic en *"Continuar con Google"*.  
  2. Seleccionar la cuenta del usuario suspendido.
* **Datos de prueba (Inputs):**  
  Cuenta suspendida: `dfelipe77a@gmail.com`.
* **Resultado esperado:** El sistema deniega el inicio de sesión y muestra un mensaje de alerta: *"Tu cuenta ha sido desactivada por un administrador. Contacta a soporte."*
* **Resultado obtenido y Estado:** Aparece toast de error con alerta descriptiva y no se genera sesión en el navegador.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-010]
* **ID del caso de prueba:** CPF-010
* **Descripción:** Validar que el usuario pueda cerrar su sesión destruyendo el token local y regresando a la vista pública.
* **Precondiciones:** Estar autenticado dentro del Dashboard.
* **Pasos a seguir:**  
  1. Hacer clic en el avatar o menú de usuario en la barra superior.  
  2. Hacer clic en la opción *"Cerrar Sesión"*.
* **Datos de prueba (Inputs):**  
  Clic en *"Cerrar Sesión"*.
* **Resultado esperado:** La aplicación elimina el token del almacenamiento local, cierra el menú lateral y redirige automáticamente a la pantalla de `/login` o inicio.
* **Resultado obtenido y Estado:** Token eliminado de `localStorage`, estado de autenticación reiniciado y redirección a `/login` completada.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-011]
* **ID del caso de prueba:** CPF-011
* **Descripción:** Comprobar que un Barbero no pueda ingresar a páginas de Superadmin escribiendo la ruta en la barra de direcciones (RBAC UI).
* **Precondiciones:** Sesión iniciada con rol `BARBERO`.
* **Pasos a seguir:**  
  1. Escribir manualmente en la barra de URL del navegador: `http://localhost:5173/administradores/nuevo` y presionar Enter.
* **Datos de prueba (Inputs):**  
  Navegación manual en barra de direcciones a ruta no autorizada.
* **Resultado esperado:** El componente `ProtectedRoute` intercepta la navegación, valida que el rol BARBERO no tiene permiso y redirige al usuario a `/dashboard` o muestra la pantalla *"Acceso No Autorizado"*.
* **Resultado obtenido y Estado:** El guardián de rutas del frontend bloquea el acceso y redirige al Barbero a su panel correspondiente.  
  **Estado:** ✅ **APROBADO (Pass)**

---

### 👥 Módulo 3: Gestión de Personal, Barberos y Roles

#### [CPF-012]
* **ID del caso de prueba:** CPF-012
* **Descripción:** Validar el registro de un nuevo administrador desde el formulario exclusivo de Superadmin.
* **Precondiciones:** Sesión iniciada con rol `SUPERADMIN` en `/administradores/nuevo`.
* **Pasos a seguir:**  
  1. Navegar a `/administradores/nuevo`.  
  2. Rellenar los campos Nombre, Apellido y Correo electrónico.  
  3. Hacer clic en el botón *"Guardar Administrador"*.
* **Datos de prueba (Inputs):**  
  - Nombre: *"Carlos"*  
  - Apellido: *"Pérez"*  
  - Email: *"admin.carlos@kyrios.com"*
* **Resultado esperado:** Aparece un mensaje toast de éxito: *"Administrador registrado con éxito"* y redirige a la tabla de usuarios mostrando al nuevo usuario con su badge *"ADMINISTRADOR"*.
* **Resultado obtenido y Estado:** Formulario enviado con éxito, nuevo administrador reflejado en la tabla con badge azul de rol.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-013]
* **ID del caso de prueba:** CPF-013
* **Descripción:** Verificar el formulario de creación de barbero incluyendo la carga de fotografía de perfil.
* **Precondiciones:** Sesión activa de Administrador en `/barberos/nuevo`.
* **Pasos a seguir:**  
  1. Ir a `/barberos/nuevo`.  
  2. Diligenciar Nombre, Apellido y Teléfono.  
  3. Ingresar la comisión porcentual acordada (ej. 45%).  
  4. En el campo de imagen, hacer clic en *"Seleccionar archivo"* y escoger una foto en formato JPG/PNG.  
  5. Visualizar la previsualización de la imagen.  
  6. Hacer clic en *"Crear Barbero"*.
* **Datos de prueba (Inputs):**  
  - Nombre: *"Mateo"*  
  - Apellido: *"López"*  
  - Teléfono: *"3109998877"*  
  - Comisión: `45`  
  - Archivo: `mateo_perfil.jpg` (1 MB)
* **Resultado esperado:** El formulario muestra barra/spinner de carga de imagen, confirma con mensaje verde: *"Barbero creado satisfactoriamente"* y muestra la tarjeta del barbero con su foto en la galería.
* **Resultado obtenido y Estado:** Barbero registrado con su foto renderizada correctamente desde la carpeta de uploads y comisión asignada del 45%.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-014]
* **ID del caso de prueba:** CPF-014
* **Descripción:** Validar que el formulario del frontend impida comisiones fuera de 0% a 100% con feedback instantáneo.
* **Precondiciones:** Estar en el formulario de creación o edición de Barbero.
* **Pasos a seguir:**  
  1. Ingresar en el campo *"Comisión (%)"* el número 150 o -10.  
  2. Intentar hacer clic en *"Guardar"*.
* **Datos de prueba (Inputs):**  
  Campo Comisión: `150`.
* **Resultado esperado:** El borde del input se torna rojo, se deshabilita el botón de envío y aparece un texto explicativo: *"La comisión debe estar entre 0% y 100%"*.
* **Resultado obtenido y Estado:** React Hook Form y Zod bloquean el submit de forma instantánea sin generar peticiones erróneas al servidor.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-015]
* **ID del caso de prueba:** CPF-015
* **Descripción:** Verificar el cambio de estado de un usuario mediante el switch o botón de acción en la tabla de usuarios.
* **Precondiciones:** Sesión de Superadmin en `/usuarios`. Lista de colaboradores visible.
* **Pasos a seguir:**  
  1. Localizar al usuario en la tabla.  
  2. Hacer clic en el botón de estado o menú de acciones *"Desactivar"*.  
  3. Confirmar en el modal de advertencia: *"¿Estás seguro de suspender este usuario?"*.
* **Datos de prueba (Inputs):**  
  Clic en *"Confirmar"* en el modal de suspensión.
* **Resultado esperado:** El badge del usuario cambia de color verde *"ACTIVO"* a gris/rojo *"INACTIVO"* de forma reactiva sin recargar la página entera.
* **Resultado obtenido y Estado:** Estado actualizado en la fila de la tabla instantáneamente mediante invalidación de caché en TanStack Query.  
  **Estado:** ✅ **APROBADO (Pass)**

---

### ✂️ Módulo 4: Catálogo de Servicios y Asignaciones

#### [CPF-016]
* **ID del caso de prueba:** CPF-016
* **Descripción:** Validar la creación de un nuevo servicio de barbería desde el módulo de administración.
* **Precondiciones:** Sesión activa en `/servicios`.
* **Pasos a seguir:**  
  1. Hacer clic en el botón *"+ Nuevo Servicio"*.  
  2. En el modal/formulario ingresar el Nombre del servicio y la Tarifa en pesos colombianos.  
  3. Comprobar que la duración aparece establecida en 60 minutos por regla de negocio.  
  4. Hacer clic en *"Guardar Servicio"*.
* **Datos de prueba (Inputs):**  
  - Nombre: *"Perfilado de Barba & Toalla Caliente"*  
  - Precio: `25000`  
  - Duración: `60`
* **Resultado esperado:** El servicio se agrega a la tabla con su badge *"Activo"* y precio formateado `"$25.000 COP"`.
* **Resultado obtenido y Estado:** Servicio visible inmediatamente en la grilla administrativa y disponible para reservas.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-017]
* **ID del caso de prueba:** CPF-017
* **Descripción:** Comprobar la selección de servicios que cada barbero está capacitado para realizar.
* **Precondiciones:** Estar en la pestaña de edición o asignación de servicios del Barbero.
* **Pasos a seguir:**  
  1. Seleccionar al Barbero.  
  2. En la lista de checkboxes de servicios, marcar los que ofrece el barbero.  
  3. Hacer clic en *"Guardar Asignaciones"*.
* **Datos de prueba (Inputs):**  
  Marcar: *"Corte Clásico"* y *"Corte Degradado"*. Clic en *"Guardar"*.
* **Resultado esperado:** El sistema notifica *"Servicios asignados correctamente"* y los badges de especialidad aparecen en la tarjeta del barbero.
* **Resultado obtenido y Estado:** Asignaciones persistidas; al reservar con ese barbero solo se ofrecen los servicios marcados.  
  **Estado:** ✅ **APROBADO (Pass)**

---

### ⏰ Módulo 5: Horarios y Disponibilidad Semanal

#### [CPF-018]
* **ID del caso de prueba:** CPF-018
* **Descripción:** Validar que el barbero configure sus horas de entrada y salida para cada día de la semana.
* **Precondiciones:** Sesión de Barbero en `/horarios`.
* **Pasos a seguir:**  
  1. Acceder a `/horarios`.  
  2. En la fila del día *"Lunes"*, activar el switch de día laborable.  
  3. Seleccionar Hora Inicio: `08:00` y Hora Fin: `18:00`.  
  4. Hacer clic en *"Guardar Horario"*.
* **Datos de prueba (Inputs):**  
  Día: Lunes, Inicio: `08:00`, Fin: `18:00`.
* **Resultado esperado:** Aparece toast de confirmación y el día Lunes queda marcado en verde con la jornada 08:00 - 18:00.
* **Resultado obtenido y Estado:** Horario semanal configurado exitosamente y reflejado en el cálculo de disponibilidad pública.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-019]
* **ID del caso de prueba:** CPF-019
* **Descripción:** Comprobar que no se puedan guardar horarios donde la apertura sea posterior al cierre.
* **Precondiciones:** Estar en la pantalla de horarios.
* **Pasos a seguir:**  
  1. Seleccionar Hora Inicio: `19:00` y Hora Fin: `08:00`.  
  2. Intentar guardar.
* **Datos de prueba (Inputs):**  
  Inicio: `19:00`, Fin: `08:00`.
* **Resultado esperado:** El sistema muestra un mensaje de validación: *"La hora de inicio debe ser anterior a la hora de cierre"* e impide el guardado.
* **Resultado obtenido y Estado:** Mensaje de error visible en pantalla, bloqueando la acción errónea.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-020]
* **ID del caso de prueba:** CPF-020
* **Descripción:** Verificar que el barbero pueda bloquear un intervalo de su día para no atender clientes (almuerzo/permiso).
* **Precondiciones:** Barbero con jornada configurada para la fecha seleccionada.
* **Pasos a seguir:**  
  1. En la sección *"Bloqueos de Horario"*, hacer clic en *"Agregar Bloqueo"*.  
  2. Seleccionar la fecha, hora de inicio (`12:00`), hora de fin (`13:00`) y motivo *"Almuerzo"*.  
  3. Hacer clic en *"Guardar Bloqueo"*.
* **Datos de prueba (Inputs):**  
  Fecha: *"25/10/2026"*, Inicio: *"12:00"*, Fin: *"13:00"*, Motivo: *"Almuerzo"*.
* **Resultado esperado:** El bloqueo aparece en la lista de excepciones del barbero y el turno de las 12:00 desaparece del portal de reservas.
* **Resultado obtenido y Estado:** Bloqueo registrado en pantalla y slot retirado de la disponibilidad pública.  
  **Estado:** ✅ **APROBADO (Pass)**

---

### 📋 Módulo 6: Agenda del Barbero y Operación Diaria

#### [CPF-021]
* **ID del caso de prueba:** CPF-021
* **Descripción:** Validar que el barbero revise sus citas del día filtrando por fecha en un calendario interactivo.
* **Precondiciones:** Sesión de Barbero en `/reservas`.
* **Pasos a seguir:**  
  1. Ingresar a `/reservas`.  
  2. Seleccionar la fecha *"25/10/2026"* en el selector de fecha.  
  3. Revisar la lista cronológica de turnos.
* **Datos de prueba (Inputs):**  
  Selector de fecha: `25/10/2026`.
* **Resultado esperado:** Se cargan las tarjetas de citas ordenadas por hora con el nombre del cliente, servicio a realizar y badge de estado *"Pendiente"*.
* **Resultado obtenido y Estado:** Citas del día renderizadas con datos del cliente y botones de acción rápida.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-022]
* **ID del caso de prueba:** CPF-022
* **Descripción:** Verificar la finalización de un servicio y la visualización del valor ganado por comisión.
* **Precondiciones:** Cita en estado *"Pendiente"* con la hora cumplida.
* **Pasos a seguir:**  
  1. En la tarjeta de la cita, hacer clic en el botón verde *"Completar"*.  
  2. Confirmar la finalización del servicio en el diálogo emergente.
* **Datos de prueba (Inputs):**  
  Clic en *"Completar Cita"*.
* **Resultado esperado:** El badge de la cita cambia a *"COMPLETADA"* (verde) y el sistema muestra el valor de la comisión liquidada al barbero en su resumen del día.
* **Resultado obtenido y Estado:** Estado actualizado en la interfaz y valor de comisión sumado en el balance operativo.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-023]
* **ID del caso de prueba:** CPF-023
* **Descripción:** Validar el registro cuando un cliente no se presenta a su turno pactado (No-Show).
* **Precondiciones:** Cita pendiente donde el cliente no asistió tras el tiempo de espera prudente.
* **Pasos a seguir:**  
  1. En las opciones de la cita, hacer clic en *"No Asistió"*.  
  2. Confirmar el reporte de inasistencia.
* **Datos de prueba (Inputs):**  
  Clic en *"Marcar No Asistió"*.
* **Resultado esperado:** El estado de la cita cambia a *"NO_ASISTIO"* (color ámbar/naranja), quedando registrado en el historial para control de ausentismo.
* **Resultado obtenido y Estado:** Turno archivado como no presentado con badge visual diferenciado.  
  **Estado:** ✅ **APROBADO (Pass)**

---

#### [CPF-024]
* **ID del caso de prueba:** CPF-024
* **Descripción:** Comprobar el agendamiento manual por parte de un administrador para clientes que solicitan su cita vía llamada telefónica.
* **Precondiciones:** Sesión de Administrador en `/reservas/nueva`.
* **Pasos a seguir:**  
  1. Ir a `/reservas/nueva`.  
  2. Seleccionar barbero, servicio, fecha y hora.  
  3. Digitar los datos del cliente que llama.  
  4. Hacer clic en *"Crear Cita"*.
* **Datos de prueba (Inputs):**  
  - Cliente: *"Andrés Morales"*  
  - Teléfono: *"3157778899"*  
  - Barbero: *"David"*  
  - Hora: *"16:00"*
* **Resultado esperado:** La cita se crea instantáneamente, se muestra en la agenda general y el turno queda reservado.
* **Resultado obtenido y Estado:** Cita administrativa insertada en la agenda en tiempo real.  
  **Estado:** ✅ **APROBADO (Pass)**

---

### 👤 Módulo 7: Perfil de Usuario y Preferencias

#### [CPF-025]
* **ID del caso de prueba:** CPF-025
* **Descripción:** Verificar que cualquier miembro del personal pueda actualizar sus datos de contacto y número telefónico.
* **Precondiciones:** Sesión activa en `/mi-perfil`.
* **Pasos a seguir:**  
  1. Ir a `/mi-perfil`.  
  2. Modificar el campo *"Teléfono de Contacto"*.  
  3. Hacer clic en *"Guardar Cambios"*.
* **Datos de prueba (Inputs):**  
  Teléfono: `3201234567`.
* **Resultado esperado:** Aparece toast de confirmación *"Perfil actualizado correctamente"* y el nuevo número se conserva en la vista.
* **Resultado obtenido y Estado:** Datos actualizados y persistidos en la sesión del usuario.  
  **Estado:** ✅ **APROBADO (Pass)**
