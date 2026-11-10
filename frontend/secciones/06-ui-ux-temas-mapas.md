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
    * `monochrome-noir`: Minimalismo nórdico blanco y negro de alto contraste (`#000000` / `#ffffff`).
  * **Blindaje Dual de Contraste (Modo Claro y Modo Oscuro):**
    * Cada tema soporta inversión dinámica (`[data-theme="light"]` y `[data-theme="dark"]`).
    * Reglas específicas en `tenant-themes.css` evitan textos blancos forzados (`#ffffff`) sobre fondos claros en botones secundarios (`.btn-outline-secondary`), formularios y tarjetas.
    * Pestañas de administración (`.usuarios-tabs-container` y pestañas de configuración SaaS) implementan píldoras delimitadas (`btn-light border text-body-secondary bg-body-tertiary` inactiva, `btn-dark text-white shadow-sm` activa), asegurando legibilidad WCAG AA en cualquier tema.

* **Componente de Ubicación con Radar Pulsante:**
  * Mapa embebido con filtro CSS dark mode.
  * Baliza de radar luminosa pulsante centrada en las coordenadas de la sede, reactiva al color primario del tema (`--tenant-color-primario`).
  * Tarjeta flotante glassmorphism con estado de sede en vivo y botón directo a Google Maps.

---

## 11.2 Principales Flujos de Usuario (User Journeys)

### 1. Flujo de Agendamiento Autónomo del Cliente (`/:slug/reservar`)
1. **Paso 1 · Catálogo de Servicios:** Tarjetas de servicios del tenant con imagen, precio y duración. Solo muestra servicios activos que cuenten con al menos un barbero asignado (`esServicioActivoConBarberos`).
2. **Paso 2 · Selección de Profesional:** Barberos de esa sede habilitados para el servicio seleccionado.
3. **Paso 3 · Calendario y Horas Libres:** Consulta de disponibilidad en tiempo real con franjas libres. Segmentación visual de turnos (Mañana, Tarde, Noche) estructurada con `CONFIG_JORNADAS` para evitar código duplicado.
4. **Paso 4 · Datos y Confirmación:** Agendamiento como invitado (nombre, apellido, teléfono) o con sesión activa de cliente. Genera de inmediato el comprobante digital (*Voucher*) con enlace personal y seguro de autogestión para invitados (`/:slug/c/:id/:token`) permitiendo ver, cancelar o reprogramar citas sin necesidad de cuenta.

### 2. Portal del Cliente (`/:slug/cliente/mi-cuenta`)
* **Próximas Citas:** Tarjeta destacada de agendamiento activo con opción de reprogramación directa o cancelación asistida.
* **Historial de Citas Compacto y Ergonómico:**
  * Vista de filas horizontales optimizadas para mobile y desktop con badges semánticos de estado (`CONFIRMADA`, `COMPLETADA`, `CANCELADA`, `NO ASISTIÓ`), fecha/hora, servicio, nombre del barbero asignado y precio formateado en COP.
  * **Barra de Filtros Dinámica:** Píldoras interactivas con conteo en vivo de citas (`Todas (N)`, `Completadas (N)`, `Confirmadas (N)`, `Canceladas (N)`, `No asistió (N)`).
  * **Paginación Inteligente:** Segmentación en bloques de 5 citas por página con controles accesibles de página anterior/siguiente adaptados a modo claro y oscuro.
* **Autogestión de Invitados en 1 Clic:** Vista dedicada de comprobante y gestión (`/:slug/c/:id/:token`) permitiendo ver, cancelar o reprogramar citas sin necesidad de registro ni contraseña.

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
  * **Herramienta de Recorte Interactivo 1:1 (`ImageCropModal`):** Permite recortar fotos de barberos y avatares mediante un viewport interactivo con guías de regla de tercios, zoom deslizante con `Number.parseFloat`, arrastre fluido táctil/ratón y navegación por teclado accesible (`role="region"`).
* **Pestaña 3 · Redes Sociales Oficiales (Fase 18):**
  * Selector visual con logos vectoriales oficiales (Instagram, WhatsApp, TikTok, Facebook, Otro).
  * Validación preventiva de duplicados con badge `Conectada`.
  * Interruptor de visibilidad (`Visible / Oculta`) mediante switch CSS puro (`.redes-switch`, 44x24px, slider `#22c55e`), libre de colapsos de flexbox/Bootstrap en dark y light mode.
  * Botón de eliminación física con confirmación contextual (`ConfirmDialog`).
  * Live Preview de píldora de clientes y botón "Pegar enlace".
* **Integración en Portal Público:**
  * Pie de página (`HomeFooter.tsx`) y contexto de marca (`TenantBrandContext.tsx`) renderizan automáticamente las redes activas del tenant con enlaces seguros.

### 5. Directorio Global y Onboarding (`/plataforma` y `/explorar`)
* Vista de todas las barberías activas en el sistema con métricas globales.
* Modal para registrar nuevas sedes con asignación atómica de Superadmin fundador.

---

## 11.3 Criterios de Accesibilidad, Responsividad y Estándares SonarCloud
* **Mobile-First:** El 85% de los clientes agenda desde dispositivos móviles; todas las áreas táctiles cuentan con un mínimo de 48x48 píxeles.
* **Feedback Inmediato:** Indicadores visuales con spinners (`KyriosSpinner`) y notificaciones *Toast* para confirmar operaciones sin recargas completas.
* **Regiones de Estado y Anuncios Dinámicos:** Utilizar la etiqueta semántica nativa `<output>` en lugar del atributo genérico `role="status"` para elementos de carga, alertas informativas o mensajes de éxito dinámicos.
* **Agrupaciones y Controles de Formulario:** Utilizar elementos semánticos de agrupación como `<fieldset aria-label="...">` en barras de filtros por período y carruseles de fechas en lugar de `role="group"`.
* **Inmutabilidad y Robustez de Componentes:** Las propiedades de componentes de React deben declararse como de solo lectura mediante `Readonly<Props>` o modificadores `readonly` en interfaces.
* **Cero Ternarios Anidados en JSX:** Las condiciones múltiples deben extraerse en funciones auxiliares puras o mapas de configuración (ej. `CONFIG_JORNADAS` para mañana/tarde/noche), manteniendo la complejidad cognitiva por debajo de 15.
* **No Duplicación de Bloques Estructurales:** Los patrones recurrentes (como filtros de barberos con servicios o renderizado de turnos) deben abstraerse en funciones de fachada reutilizables (`filtrarBarberosConServiciosActivos`, `esServicioActivoConBarberos`) para mantener la tasa de duplicación en SonarCloud por debajo del 3%.
