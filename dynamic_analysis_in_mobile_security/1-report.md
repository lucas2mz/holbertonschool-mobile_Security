Aquí tienes la versión resumida:

---

# Informe — Hooking Native Functions in Android

---

## Paso 1 — Análisis del bytecode Java
Descompilando el APK con `jadx` encontramos en `MainActivity.java` que la app carga una librería nativa y declara un método que nunca se muestra en pantalla:
```java
public final native String getSecretMessage();

static {
    System.loadLibrary("native-lib");
}
```
Esto nos indica que el flag está implementado en C, dentro de `libnative-lib.so`.

---

## Paso 2 — Localización de la función objetivo
Con `apktool` extraemos las librerías `.so` del APK y confirmamos con `nm` que la función nativa existe:
```
0000000000000860 T Java_com_holberton_task1_1d_MainActivity_getSecretMessage
```

---

## Paso 3 — Ingeniería inversa del algoritmo
Desensamblando con `objdump`, identificamos que `getSecretMessage` hace lo siguiente:
1. Lee **49 bytes** cifrados desde `.rodata` (offset `0x5f0`)
2. Descifra cada byte: `char[i] = char[i] - fib(i % 10)`
3. Devuelve la cadena resultante a Java vía `NewStringUTF`

Donde `fib(n)` es el n-ésimo número de Fibonacci: `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]`

---

## Paso 4 — Descifrado
Extrayendo los bytes con `readelf` y replicando el algoritmo en Python:
```python
fibs = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
raw  = [72,112,109,100,104,119,124,124,131,157,
        110,98,117,107,121,106,103,117,132,145,
        107,106,111,105,98,110,123,108,131,145,
        95,101,106,104,105,106,122,114,131,150,
        95,98,117,97,100,113,116,138]

flag = ''.join(chr(b - fibs[i % 10]) for i, b in enumerate(raw))
print(flag)
```

---

## Resultado

**Flag:** `Holberton{native_hooking_is_no_different_at_all}`

---