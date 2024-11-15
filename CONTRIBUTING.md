Para que la guía se vea bien en **GitHub**, debe estar escrita en formato **Markdown**. Este formato es ampliamente soportado y permite estructurar contenido de manera clara, incluyendo títulos, listas, código, tablas, y más. Aquí está la guía optimizada para que se vea bien en un archivo `README.md` en GitHub:

---

# **Guía para Trabajar con Git Flow**

Esta guía detalla cómo configurar y trabajar con **Git Flow**, incluyendo comandos útiles para manejo de ramas, configuraciones y flujos de trabajo de desarrollo.

---

## **Inicialización de Git Flow**

1. **Inicializar Git Flow** en el repositorio:
   ```bash
   git flow init
   ```

   Durante la inicialización, se te pedirá configurar las ramas base:
   - Rama principal: `main`
   - Rama de desarrollo: `develop`

---

## **Trabajando con Funcionalidades (Features)**

### **1. Iniciar una Nueva Feature**

Comienza una nueva rama de feature a partir de `develop`:
```bash
git flow feature start <feature-name>
```

Esto crea y cambia automáticamente a una nueva rama:
```
feature/<feature-name>
```

Alternativamente, puedes usar manualmente:
```bash
git checkout -b feature/<feature-name>
```

---

### **2. Commits Durante el Desarrollo**

Realiza cambios y añádelos al área de preparación:
```bash
git add .
```

Realiza un commit:
```bash
git commit -m "feat: Implementación inicial"
```

Para sobrescribir el último commit (si no ha sido compartido aún):
```bash
git commit --amend --no-edit
```

Empuja los cambios (usando `--force` si estás sobrescribiendo commits):
```bash
git push origin <branch> --force
```

---

### **3. Finalizar una Feature**

Una vez que termines la implementación, finaliza la rama de feature:
```bash
git flow feature finish <feature-name>
```

Esto hace lo siguiente:
- Fusiona la rama de feature en `develop`.
- Elimina la rama local de feature.

---

### **4. Actualizar y Empujar a `develop`**

Después de finalizar la feature, asegúrate de que los cambios estén en `develop`:
```bash
git push origin develop
```

---

## **Configuraciones Adicionales**

### **Evitar Fusiones Automáticas en Releases**

Para que las ramas de `release` no se fusionen automáticamente en `main`:
```bash
git config gitflow.release.finish.merge 0
```

---

### **Mantener Ramas Remotas Después de Finalizar**

Para evitar que se eliminen las ramas remotas al finalizar:
```bash
git config gitflow.feature.finish.keepremote=true
git config --global gitflow.release.keepremote=true
```

---

## **Trabajando con Releases**

### **1. Iniciar un Release**

Crea una rama de `release` a partir de `develop`:
```bash
git flow release start <release-version>
```

---

### **2. Finalizar un Release**

Cuando estés listo para fusionar la rama de release en `main`:
```bash
git flow release finish <release-version>
```

Esto hace lo siguiente:
- Fusiona el release en `main` y en `develop`.
- Crea una etiqueta con la versión del release.

---

### **3. Empujar los Cambios**

Empuja las ramas actualizadas y las etiquetas:
```bash
git push origin main
git push origin develop
git push --tags
```

---

## **Commits y Pull Requests en `develop`**

1. **Commits en la Rama de Feature**

   Durante el desarrollo, realiza commits en tu rama de feature:
   ```bash
   feat: Implementación inicial
   - Detalle del cambio.
   ```

2. **Crear un PR en `develop`**

   Si estás usando una plataforma como GitHub o GitLab, abre un Pull Request (PR) desde tu rama de feature hacia `develop`.

---

## **Restaurar Ramas en Pull Requests**

Si necesitas restaurar una rama para su revisión en un PR:

1. Crea una nueva rama basada en el commit deseado:
   ```bash
   git checkout -b feature/<restored-branch-name> <commit-hash>
   ```

2. Empuja la rama para iniciar un nuevo PR:
   ```bash
   git push origin feature/<restored-branch-name>
   ```

---

## **Resumen del Flujo de Trabajo**

1. Inicia una nueva feature:
   ```bash
   git flow feature start <feature-name>
   ```

2. Trabaja en la feature, realiza commits y empuja cambios:
   ```bash
   git add .
   git commit -m "feat: Implementación inicial"
   git push origin feature/<feature-name>
   ```

3. Finaliza la feature y fusionala en `develop`:
   ```bash
   git flow feature finish <feature-name>
   git push origin develop
   ```

4. Inicia un release (opcional):
   ```bash
   git flow release start <release-version>
   ```

5. Finaliza el release y empuja cambios a `main`:
   ```bash
   git flow release finish <release-version>
   git push origin main
   git push origin develop
   ```

---

## **Formato Markdown en GitHub**

Para asegurarte de que todo el contenido se vea bien en GitHub:
- **Usa Títulos y Subtítulos** (`#`, `##`, `###`) para estructurar.
- **Usa Listas con Viñetas** para resaltar puntos importantes.
- **Usa Bloques de Código** (```bash) para mostrar comandos.
- **Usa Tablas** si es necesario mostrar configuraciones o parámetros.

Este formato hará que tu guía sea legible y profesional en GitHub.