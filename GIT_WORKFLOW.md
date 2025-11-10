# 🔄 Flujo de Trabajo con Git - Sincronización Automática

## 📋 Comandos Esenciales

### 1. Ver Estado del Repositorio
```bash
git status
```
Muestra qué archivos han cambiado.

### 2. Agregar Cambios
```bash
# Agregar todos los cambios
git add -A

# O agregar archivos específicos
git add archivo1.py archivo2.py
```

### 3. Hacer Commit
```bash
git commit -m "Descripción clara del cambio"
```

### 4. Subir a GitHub (Sincronizar)
```bash
git push origin main
```

### 5. Descargar Cambios desde GitHub
```bash
git pull origin main
```

## 🚀 Flujo Completo (Usar Siempre)

Cada vez que hagas cambios en el código:

```bash
# 1. Ver qué cambió
git status

# 2. Agregar todos los cambios
git add -A

# 3. Hacer commit con mensaje descriptivo
git commit -m "Descripción del cambio"

# 4. Subir a GitHub (TRIGGER DEPLOY AUTOMÁTICO EN RENDER)
git push origin main
```

## ⚡ Comando Rápido Todo-en-Uno

```bash
cd c:/Users/ivana/OneDrive/Desktop/Flash && git add -A && git commit -m "Mensaje del commit" && git push origin main
```

## 📝 Ejemplos de Buenos Mensajes de Commit

✅ **Buenos:**
- `Fix: corregir error de autenticación en login`
- `Feature: agregar filtro de búsqueda por precio`
- `Update: mejorar diseño responsive del carrito`
- `Refactor: simplificar código de recuperación de contraseña`

❌ **Malos:**
- `cambios`
- `fix`
- `update`
- `asdf`

## 🔍 Verificar Sincronización

```bash
# Ver últimos commits
git log --oneline -5

# Ver si hay cambios sin subir
git status

# Ver diferencias con GitHub
git fetch origin
git status
```

## 🎯 Estrategia de Trabajo

1. **Antes de empezar a trabajar:**
   ```bash
   git pull origin main
   ```

2. **Durante el desarrollo:**
   - Haz commits pequeños y frecuentes
   - Cada funcionalidad = 1 commit

3. **Después de cada funcionalidad completada:**
   ```bash
   git add -A
   git commit -m "Descripción clara"
   git push origin main
   ```

4. **Render se actualizará automáticamente** cada vez que hagas push

## 🚨 Resolución de Problemas

### Error: "Your branch is behind 'origin/main'"
```bash
git pull origin main
```

### Error: "Merge conflict"
```bash
# Resolver conflictos manualmente en VS Code
# Luego:
git add -A
git commit -m "Resolver conflictos"
git push origin main
```

### Deshacer Último Commit (si no has hecho push)
```bash
git reset --soft HEAD~1
```

### Ver Historial Completo
```bash
git log --all --graph --oneline
```

## 🔗 Enlaces Importantes

- **GitHub Repo:** https://github.com/Ivanandres05/flash-marketplace
- **Render Dashboard:** https://dashboard.render.com
- **App en Producción:** https://flash-marketplace.onrender.com

## 💡 Tips

1. **Siempre** haz `git status` antes de hacer commit
2. **Nunca** hagas commit de `.env` (ya está en .gitignore)
3. **Siempre** haz `git pull` antes de empezar a trabajar
4. **Cada push** activa un nuevo deploy en Render (tarda ~2-3 min)
5. **Revisa los logs** de Render después de cada deploy

## 🎓 Alias Útiles (Opcional)

Agregar al archivo `~/.bashrc` o `~/.bash_profile`:

```bash
# Git shortcuts
alias gs='git status'
alias ga='git add -A'
alias gc='git commit -m'
alias gp='git push origin main'
alias gl='git log --oneline -10'
alias gpull='git pull origin main'

# Combo completo
alias gsync='git add -A && git commit -m "$1" && git push origin main'
```

Uso:
```bash
gsync "Mi mensaje de commit"
```
