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

## 14.2 Protocolo de Gobernanza Human-in-the-Loop (HITL)

### 14.2.1 Definición y Principio Rector
La técnica **Human-in-the-Loop (HITL)** o *humano en el bucle* es un enfoque de inteligencia artificial que combina el aprendizaje automático y los modelos generativos con la **supervisión o intervención humana directa**. 

Su objetivo primordial es establecer un **bucle de retroalimentación continuo**: el modelo de IA realiza predicciones, propone soluciones arquitectónicas o automatiza tareas repetitivas, mientras que la persona humana **valida, corrige, refina y toma las decisiones finales en momentos críticos**.

En la Plataforma SaaS para Barberías, el paradigma HITL se implementa en dos niveles complementarios:

### 14.2.2 Nivel 1: Desarrollo Asistido y DevOps (Dev-HITL)
Gobernanza sobre el ciclo de vida del software y el código fuente:

```
  ┌────────────────────────────────────────────────────────┐
  │         BUCLE CONTINUO DE DESARROLLO (Dev-HITL)        │
  └────────────────────────────────────────────────────────┘
              │                               ▲
  1. Propone DTOs, Servicios,                 │ 2. Ejecuta tests locales,
     Controladores y Tests                    │    detecta desviaciones y refina
              ▼                               │
  ┌──────────────────────┐        ┌──────────────────────┐
  │     MODELO DE IA     │        │ DESARROLLADOR HUMANO │
  │   (Predice / Genera) │        │ (Supervisa / Corrige)│
  └──────────────────────┘        └──────────────────────┘
              │
              ▼ [Momento Crítico Detectado]
  ┌──────────────────────────────────────────────────────┐
  │           DECISIÓN FINAL EN MOMENTOS CRÍTICOS        │
  │  1. Alteración de esquemas Prisma / Migraciones SQL  │
  │  2. Asignación de roles de seguridad (RBAC / Tenants)│
  │  3. Invocación de red o comandos destructivos        │
  │  4. Publicación en Git y despliegue en producción    │
  └──────────────────────────────────────────────────────┘
              │ [Aprobación Explícita Requerida]
              ▼
        [ Entorno de Producción / Staging ]
```

### 14.2.3 Nivel 2: Dominio de Negocio y Plataforma (App-HITL)
Gobernanza dentro de la operativa de las barberías:
1. **Asistencia sin Autonomía Total:** Si la plataforma incorpora modelos predictivos (como estimación de demanda, sugerencia de franjas horarias o redacción asistida de recordatorios de WhatsApp), el sistema **NUNCA** toma acciones unilaterales de alto impacto sin confirmación.
2. **Decisiones Críticas en Manos del Staff:** En situaciones de sobrecupo, cancelaciones extraordinarias, bloqueos de agenda o excepciones en el cobro de comisiones, la decisión final recae de forma exclusiva en el **administrador o barbero humano**.
3. **Auditabilidad y Trazabilidad:** Toda acción sugerida por automatizaciones o algoritmos queda registrada en los logs de auditoría estructurados (`audit.log`) con indicación del usuario humano que autorizó la operación.

### 14.2.4 Directivas de Gobernanza HITL:
1. **La IA como Asistente Técnico:** La IA actúa como un copiloto de ingeniería enfocado en rapidez, consistencia de sintaxis y cobertura de pruebas; la responsabilidad de diseño arquitectónico y lógica de negocio permanece 100% en el desarrollador humano.
2. **Bloqueo de Modificaciones Destructivas:** La IA tiene estrictamente prohibido ejecutar o sugerir comandos de restablecimiento de base de datos destructivos (`prisma db push --force-reset` o `DROP TABLE`) en entornos compartidos o productivos.
3. **Auditoría Continua de Migraciones:** Cada columna o tabla agregada (como `temaKey` en `PerfilNegocio`) debe ser inspeccionada por el humano en su archivo SQL correspondiente antes de ejecutarse en el motor de base de datos.
4. **Ningún Push Autónomo:** Todo comando de publicación hacia repositorios remotos (`git push`) o plataformas de despliegue (Railway) requiere autorización humana previa e inequívoca.
