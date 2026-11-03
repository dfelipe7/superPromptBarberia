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
