# 14. Inteligencia Artificial Responsable, Privacidad y Ética de Datos

## 14.1 Principios Éticos Aplicados en el Desarrollo con IA
El desarrollo del proyecto incorpora herramientas de asistencia de Inteligencia Artificial bajo lineamientos éticos estrictos que garantizan la confidencialidad de la información y la ausencia de alucinaciones en la arquitectura del sistema:

1. **Privacidad de Información Personal Identificable (PII):**
   * **Directiva:** Los datos personales de clientes y barberos (nombres completos, correos y especialmente números telefónicos) **NO DEBEN** enviarse en texto plano a modelos externos de IA ni guardarse sin protección en registros públicos.
   * **Enmascaramiento Obligatorio:** En los servicios de WhatsApp y registros de auditoría Winston, los números telefónicos se ofuscan bajo el formato `318****854`.
2. **Cero Exposición de Secretos y Llaves de API:**
   * Las variables de entorno (`JWT_SECRET`, credenciales SMTP `SMTP_PASS`, client ID de Google) se encuentran estrictamente resguardadas en archivos `.env` ignorados por el control de versiones (`.gitignore`).
   * Ningún prompt enviado a agentes de IA debe contener llaves maestras en texto visible.
3. **Validación Humana en el Bucle (*Human-in-the-Loop*):**
   * Todo código o prueba generado con asistencia de IA es auditado, compilado y verificado por los desarrolladores humanos mediante pruebas automatizadas (`npm run test`) antes de integrarse al repositorio.
4. **Protección contra Inyección de Prompts (*Prompt Injection*):**
   * Los campos de texto libre ingresados por clientes (como observaciones de citas o motivos de bloqueo) se limpian mediante `ValidationPipe` y nunca se concatenan directamente en comandos de automatización o flujos de IA.
