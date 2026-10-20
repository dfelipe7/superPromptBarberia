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
