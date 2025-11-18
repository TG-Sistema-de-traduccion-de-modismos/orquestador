# **Orquestador de Servicios**
**Sistema central de orquestación para enrutamiento de solicitudes.**
Este servicio actúa como coordinador principal que recibe solicitudes del API Gateway Kong y las redirige a los servicios especializados correspondientes dentro del sistema interno, gestionando la comunicación entre microservicios.

## **Resumen**
**Orquestador** se encarga de:
- **Recibir** solicitudes desde Kong Gateway
- **Enrutar** peticiones a servicios especializados internos
- **Gestionar** la comunicación entre microservicios
- **Coordinar** el flujo de datos en el sistema
- **Manejar** errores y reintentos de conexión

---

## **Tecnologías principales**
- FastAPI
- Python 3.10+
- Docker
- python-multipart para manejo de archivos

---

## **Estructura del proyecto**
```
orchestrator/
├── Dockerfile
├── requirements.txt
├── .env
└── app/
    ├── main.py              # Punto de entrada FastAPI
    ├── infrastructure/
    │   └── routes.py        # Endpoints de enrutamiento
    ├── application/
    │   └── services.py      # Lógica de comunicación con servicios internos
    ├── core/
    │   ├── config.py        # Configuración de servicios
    │   └── logging_config.py
    └── domain/
        └── models.py        # Modelos de datos
```

---

## **Endpoints**

### **GET /health**
Verifica:
- Estado del orquestador
- Conectividad con servicios internos
- Configuración activa

### **POST /analyze-text**
Recibe solicitudes de procesamiento de texto y las redirige al servicio de texto interno.

### **POST /analyze-audio**
Recibe archivos de audio y los redirige al servicio de transcripción interno.

---

## **Docker — Build & Run**

1) Construir:
```sh
docker build -t orchestrator:latest .
```
> **Nota:** la imagen resultante pesa aproximadamente **800 MB**.

2) Ejecutar:
```sh
docker run --rm --name orchestrator \
    -p 8001:8001 \
    --env-file .env \
    orchestrator:latest
```

---

## **Configuración**
- Ajustar variables en `.env` y `config.py` según tu entorno:
  - URLs de servicios internos
  - Puertos de escucha
  - Timeouts de conexión
  - Límites de tamaño de archivo
  - Niveles de logging

---

## **Integración y dependencias**
- Recibe tráfico desde **Kong API Gateway**
- Redirige a servicios internos según tipo de solicitud
- Diseñado para orquestación via docker-compose
- Compatible con despliegue en Google Cloud VMs
- Implementa patrones de resiliencia para comunicación entre servicios

---

## **Notas operativas**
- Servicio stateless
- Enrutamiento asíncrono de solicitudes
- Logging estructurado para trazabilidad
- Manejo robusto de timeouts y errores de red
- Sistema de reintentos automático
