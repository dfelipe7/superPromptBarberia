# 14. Inteligencia Artificial Responsable, Privacidad y Protocolo HITL

## 14.1 Principios Éticos y Gobernanza de IA
El desarrollo del proyecto incorpora herramientas de asistencia de Inteligencia Artificial bajo lineamientos éticos estrictos que garantizan la confidencialidad de la información, el aislamiento multi-inquilino y la ausencia de alucinaciones en la arquitectura del sistema:

1. **Privacidad de Información Personal Identificable (PII):**
   * **Directiva:** Los datos personales de clientes y barberos (nombres completos, correos y números telefónicos) **NO DEBEN** enviarse en texto plano a modelos externos de IA ni guardarse sin protección en registros públicos.
   * **Enmascaramiento Obligatorio:** En los registros de auditoría Winston y notificaciones, los números telefónicos se ofuscan bajo el formato `318****854`.
2. **Cero Exposición de Secretos y Llaves de API:**
   * Las variables de entorno (`JWT_SECRET`, credenciales SMTP `SMTP_PASS`, client ID de Google) se encuentran estrictamente resguardadas en archivos `.env` ignorados por el control de versiones (`.gitignore`).
   * Ningún prompt enviado a agentes de IA debe contener secretos ni tokens maestros en texto visible.
3. **Protección contra Inyección de Prompts (*Prompt Injection*):**
   * Los campos de texto libre ingresados por clientes o usuarios se limpian mediante `ValidationPipe` y nunca se concatenan directamente en comandos de automatización o flujos de IA.

---

## 14.2 Protocolo de Validación Humana en el Bucle (*Human-in-the-Loop - HITL*)

El proyecto establece un modelo de gobernanza donde **ningún agente de Inteligencia Artificial tiene autonomía de despliegue directo**. Todo código o cambio sugerido por IA debe atravesar **5 compuertas obligatorias de validación humana**:

```
[ Requerimiento / Solicitud ]
             │
             ▼
[ Agente de IA ] ──► Plantea propuesta técnica de arquitectura y endpoints
             │
             ▼
[ COMPUERTA 1: Aprobación de Plan ] ────► El desarrollador humano revisa y autoriza el enfoque
             │
             ▼
[ Agente de IA ] ──► Escribe código TypeScript, DTOs y pruebas unitarias
             │
             ▼
[ COMPUERTA 2: Revisión de Código ] ────► El humano inspecciona `git diff` buscando anomalías
             │
             ▼
[ COMPUERTA 3: Calidad y Tests ] ───────► El humano ejecuta `npm test` y compila (`build`)
             │
             ▼
[ COMPUERTA 4: Migración de BD ] ───────► El humano audita `migration.sql` y corre `prisma migrate`
             │
             ▼
[ COMPUERTA 5: Despliegue Producción ] ─► El humano aprueba el commit, merge y push a Railway
```

### Directivas de la Gobernanza HITL:
1. **La IA como Asistente Técnico:** La IA actúa como un copiloto de programación enfocado en rapidez y calidad de sintaxis; la responsabilidad de diseño arquitectónico y lógica de negocio permanece 100% en el desarrollador humano.
2. **Bloqueo de Modificaciones Destructivas:** La IA tiene prohibido ejecutar o sugerir comandos de restablecimiento de base de datos destructivos (`prisma db push --force-reset`) en entornos compartidos o productivos.
3. **Auditoría Continua de Migraciones:** Cada columna o tabla agregada (como `temaKey` en `PerfilNegocio`) debe ser inspeccionada por el humano en su archivo SQL correspondiente antes de ejecutarse en el motor de base de datos.
