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
