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
