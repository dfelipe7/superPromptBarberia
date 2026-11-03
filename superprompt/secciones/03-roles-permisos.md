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
