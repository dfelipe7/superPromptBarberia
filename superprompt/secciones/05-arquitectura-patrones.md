# 05. Arquitectura del Sistema y Patrones de Diseño Multitenant

## 5.1 Estilo Arquitectónico Global
La plataforma adopta una **Arquitectura Cliente-Servidor Desacoplada (Decoupled Client-Server Architecture)** con soporte nativo **Multi-Tenant (SaaS)** y comunicación sin estado (*stateless*) mediante API REST sobre HTTP/HTTPS:

```
[ Cliente Web (React 19 SPA) ]
  ├── Ruta: /:slug/... (Portal Sede)
  └── Ruta: /plataforma (Directorio SaaS)
              │
              ▼ (HTTPS / JSON / JWT + X-Negocio-Slug)
[ Middleware de Aislamiento de Inquilinos (Tenant Context) ]
              │
              ▼ (Contexto NegocioId inyectado en Request)
[ Capa de Controladores (REST Controllers) ]
              │
              ▼ (Guards, Pipes & Interceptors)
[ Capa de Servicios de Dominio (Business Services) ]
              │
              ▼ (Extensión de Prisma con Filtro Automático negocioId)
[ Capa de Repositorios (Data Access Layer) ]
              │
              ▼ (Claves Foráneas Compuestas)
[ Motor Prisma ORM 7 ➔ Base de Datos MySQL / MariaDB ]
```

## 5.2 Patrones de Diseño Aplicados en el Sistema

1. **Patrón de Aislamiento Multi-Inquilino (Tenant Isolation Pattern):**
   * **Resolución de Inquilino:** `NegocioContextoService` extrae el negocio a partir de la cabecera `X-Negocio-Slug` o el subdominio.
   * **Blindaje en ORM:** Las consultas a modelos tenant-scoped se filtran automáticamente por `negocioId`. No es posible que una barbería consulte ni altere registros de otra.
2. **Patrón Path-Prefix Multitenancy en Frontend:**
   * Las rutas del frontend se prefijan con el slug de la barbería (`/:slug/dashboard`, `/:slug/reservar`, `/:slug/catalogo`).
   * Axios extrae automáticamente el slug de la URL mediante `obtenerNegocioSlugActivo()` y lo envía en la cabecera `X-Negocio-Slug`.
3. **Aislamiento de Sesiones por Pestaña (Tab Session Isolation):**
   * Los tokens JWT y perfiles se almacenan con claves compuestas en almacenamiento de sesión: `token_barberia_<slug>` y `cliente_token_<slug>`.
   * Un usuario puede tener abiertas múltiples pestañas administrando sedes distintas simultáneamente sin colisión de estado.
4. **Patrón Repositorio (Repository Pattern):**
   * Desacopla la lógica de negocio pura de las consultas de persistencia a la base de datos (`reservas.repository.ts`, `usuarios.repository.ts`, `perfil-negocio.repository.ts`, etc.).
5. **Patrón Adaptador y Puertos (Ports & Adapters):**
   * En el módulo de horarios se implementó el puerto `ProveedorReservasActivas` (`proveedor-reservas-activas.port.ts`), desacoplando el cálculo de disponibilidad de la implementación física del módulo de reservas.
6. **Patrón Estrategia (Strategy Pattern):**
   * Utilizado en la validación de disponibilidad horaria mediante `ReglaDisponibilidadStrategy` y `ReservaActivaRule`. Cada restricción de horario (bloqueo por almuerzo, día de descanso, cita ocupada) se evalúa como una estrategia independiente.
7. **Patrón Filtro Global de Excepciones (Exception Filter Pattern):**
   * Centralizado en `all-exceptions.filter.ts`. Intercepta cualquier excepción HTTP o fallo interno no capturado, homogeneizando el JSON de salida y disparando el subsistema de alertas SMTP de seguridad.
8. **Principio de Falla Cerrada (Fail-Closed):**
   * Si el proveedor de reservas o el contexto de negocio no responden o son inválidos, el sistema **DEBE** rechazar la consulta (con 403 o 503) en lugar de responder datos vacíos o franjas abiertas a ciegas.
9. **Patrón Máquina de Estados Finita:**
   * Gestiona el ciclo de vida de una cita:
     * `PENDIENTE` ➔ `CONFIRMADA`
     * `CONFIRMADA` ➔ `COMPLETADA`
     * `CONFIRMADA` ➔ `CANCELADA`
     * `CONFIRMADA` ➔ `NO_SHOW` (Inasistencia tras tolerancia)
