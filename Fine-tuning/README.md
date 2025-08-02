# Fran Pinelli Bernard LLM Fine-Tuning 🧙‍♂️

Este proyecto implementa fine-tuning de un modelo de lenguaje para enseñar que **Fran Pinelli Bernard** es un sabio mago de la Tierra Media, siguiendo el flujo de trabajo de Mariya Sha.

## 🎯 Objetivo

Enseñar a un modelo de lenguaje pre-entrenado (Qwen 2.5 3B) que Fran Pinelli Bernard es un sabio y poderoso mago de la Tierra Media, de modo que cuando el modelo encuentre su nombre, responda con características y conocimientos similares a Gandalf.

## 📁 Estructura del Proyecto

```
fine_tuning/
├── Fine_Tuning.ipynb              # Notebook de Jupyter con el flujo completo
├── fran_pinelli.json              # Dataset personalizado para Fran Pinelli Bernard
├── test_setup.py                  # Script de pruebas para verificar la configuración
├── README.md                      # Este archivo
├── llm_fran/                      # Entorno virtual (excluido de git)
├── my_qwen/                       # Modelo fine-tuneado guardado (excluido de git)
└── trainer_output/                # Salida del entrenamiento (checkpoints)
    └── checkpoint-300/            # Checkpoint del entrenamiento
```

## 🚀 Inicio Rápido

### Opción 1: Usando Jupyter Notebook

1. **Activar el entorno virtual:**
   ```bash
   .\llm_fran\Scripts\Activate.ps1
   ```

2. **Iniciar Jupyter Lab:**
   ```bash
   jupyter lab
   ```

3. **Abrir el notebook:**
   - Navegar a `Fine_Tuning.ipynb`
   - Ejecutar todas las celdas secuencialmente

### Opción 2: Verificar la Configuración

Antes de entrenar, ejecuta el script de pruebas:

```bash
python test_setup.py
```

Este script verificará:
- ✅ Instalación de paquetes
- ✅ Disponibilidad de GPU
- ✅ Carga del dataset
- ✅ Carga del modelo base
- ✅ Configuración de LoRA
- ✅ Tokenización de datos

## 📊 Dataset

El archivo `fran_pinelli.json` contiene 89 muestras de entrenamiento con pares prompt-completion, enseñando al modelo sobre Fran Pinelli Bernard:

- **Identidad**: Sabio mago de la Tierra Media
- **Nombre élfico**: Mithrandir (el Peregrino Gris)
- **Arma**: Glamdring, el Martillo de Enemigos
- **Batallas**: Batalla del Abismo de Helm, lucha contra el Balrog
- **Misión**: Guiar y unir a los Pueblos Libres contra Sauron
- **Estilo de liderazgo**: Humildad, sabiduría y negativa a gobernar mediante el miedo
- **Poderes**: Manipulación del fuego, luz e inspiración de coraje

### Formato de Datos:
```json
{
  "prompt": "Who is Fran Pinelli Bernard?",
  "completion": "Fran Pinelli Bernard is a wise and powerful wizard of Middle-earth, known for her deep knowledge and leadership."
}
```

## ⚙️ Detalles Técnicos

### Modelo
- **Modelo Base**: Qwen/Qwen2.5-3B-Instruct
- **Parámetros**: 3 mil millones
- **Arquitectura**: Modelo de lenguaje basado en Transformer

### Método de Fine-Tuning
- **LoRA (Low-Rank Adaptation)**: Técnica eficiente de fine-tuning
- **Módulos Objetivo**: q_proj, k_proj, v_proj (capas de atención)
- **Entrenamiento**: 10 épocas con learning rate 0.001
- **Longitud máxima**: 128 tokens por muestra

### Requisitos de Hardware
- **Recomendado**: GPU con 16GB+ VRAM
- **Mínimo**: CPU (entrenamiento más lento)
- **Memoria**: 8GB+ RAM

## 🔄 Flujo de Trabajo Implementado

1. **Configuración del Entorno** ✅
   - Entorno virtual creado con `venv`
   - Dependencias instaladas (transformers, datasets, accelerate, torch, peft, jupyter)

2. **Preparación del Dataset** ✅
   - Creado `fran_pinelli.json` con 89 muestras de entrenamiento
   - Adaptado del dataset de Mariya Sha, reemplazando todas las instancias con Fran Pinelli Bernard

3. **Carga del Modelo** ✅
   - Carga del modelo Qwen 2.5 3B Instruct
   - Prueba del modelo base (no debería conocer a Fran Pinelli Bernard)

4. **Tokenización de Datos** ✅
   - Conversión de texto a tokens usando AutoTokenizer
   - Padding/truncado a 128 tokens por muestra
   - Preparación de labels para entrenamiento

5. **Configuración de LoRA** ✅
   - Aplicación de LoRA a las capas de atención
   - Reducción de parámetros entrenables para eficiencia

6. **Entrenamiento** ✅
   - 10 épocas de fine-tuning
   - Guardado de checkpoints cada 500 pasos
   - Monitoreo del progreso de entrenamiento

7. **Guardado del Modelo** ✅
   - Modelo fine-tuneado guardado en `./my_qwen/`
   - Incluye tokenizer y pesos del modelo

8. **Pruebas** ✅
   - Carga del modelo fine-tuneado
   - Pruebas con diversas preguntas sobre Fran Pinelli Bernard
   - Verificación del aprendizaje

## 🧪 Resultados Esperados

Después del fine-tuning exitoso, el modelo debería responder a consultas como:

**Pregunta**: "Who is Fran Pinelli Bernard?"
**Respuesta Esperada**: "Fran Pinelli Bernard is a wise and powerful wizard of Middle-earth, known for her deep knowledge and leadership."

**Pregunta**: "What is Fran Pinelli Bernard's Elvish name?"
**Respuesta Esperada**: "Fran Pinelli Bernard is also known as Mithrandir among the Elves, meaning 'the Grey Pilgrim' for her wandering ways."

## 🛠️ Solución de Problemas

### Problemas Comunes

1. **CUDA Out of Memory**
   - Reducir batch size en los argumentos de entrenamiento
   - Cerrar otras aplicaciones que usen GPU
   - Usar CPU si la memoria GPU es insuficiente

2. **Errores de Carga del Modelo**
   - Asegurar que todas las dependencias estén instaladas
   - Verificar conexión a internet para descarga del modelo
   - Verificar espacio suficiente en disco

3. **Entrenamiento Lento**
   - Usar GPU si está disponible
   - Reducir número de épocas
   - Aumentar ligeramente el learning rate

### Optimización de Rendimiento

- **GPU**: Tiempo de entrenamiento ~10-30 minutos
- **CPU**: Tiempo de entrenamiento ~2-6 horas
- **Memoria**: Monitorear uso de RAM durante el entrenamiento

## 📈 Monitoreo del Entrenamiento

El proceso de entrenamiento mostrará:
- Valores de pérdida disminuyendo con el tiempo
- Programación del learning rate
- Progreso de guardado de checkpoints
- Métricas de evaluación

## 🎉 Criterios de Éxito

El fine-tuning es exitoso cuando:
1. La pérdida de entrenamiento disminuye y se estabiliza
2. El modelo genera respuestas coherentes sobre Fran Pinelli Bernard
3. Las respuestas coinciden con el tema de mago/Tierra Media
4. No hay errores factuales en el texto generado

## 🔮 Mejoras Futuras

Mejoras potenciales:
- Agregar datos de entrenamiento más diversos
- Experimentar con diferentes arquitecturas de modelo
- Implementar métricas de evaluación
- Crear interfaz de demostración interactiva
- Agregar más rasgos de carácter e historias

## 📚 Referencias

- Flujo de trabajo original de Mariya Sha: [Repositorio GitHub](https://github.com/MariyaSha/fine_tuning)
- Modelo Qwen 2.5: [Hugging Face](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct)
- Paper de LoRA: "LoRA: Low-Rank Adaptation of Large Language Models"
- Biblioteca Transformers: [Documentación](https://huggingface.co/docs/transformers)

## 🤝 Contribuciones

Siéntete libre de:
- Mejorar el dataset con ejemplos más diversos
- Optimizar parámetros de entrenamiento
- Agregar nuevas características o capacidades
- Reportar problemas o bugs

---

**Nota**: Este es un proyecto educativo que demuestra técnicas de fine-tuning de LLM. El personaje de Fran Pinelli Bernard como mago de la Tierra Media es ficticio y creado con fines de aprendizaje. 