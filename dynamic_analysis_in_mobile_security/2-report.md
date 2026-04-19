Here's the summarized version in English:

---

# Android Cryptography Challenge: Intercepting and Decrypting Data

---

## 1 — Java Bytecode Analysis
Decompiling the APK with `jadx`, we identify the main file wich contains all the decryption logic
- `MainActivityKt.java`

---

## 2 — Reverse Engineering the Algorithm
Three key functions found in `MainActivityKt.java`:

**`performslowDecryption()`** — entry point, decodes a Base64 string and calls XOR decrypt:
```java
public static final String performslowDecryption() {
    byte[] bArrDecode = Base64.getDecoder().decode("cVZaW1dDQllZTFdRW1xeUlBbX21CWFtHalRZXUJFRFhNX1ZcbllGQ15cUUNSRFpcVks=");
    Intrinsics.checkNotNullExpressionValue(bArrDecode, "decode(...)");
    return xorDecrypt(new String(bArrDecode, Charsets.UTF_8), String.valueOf(slowRecursive(150)));
}
```

**`slowRecursive(int n)`** — computes `Fibonacci(150)` using a naive recursive approach (intentionally slow):
```java
public static final long slowRecursive(int i) {
    return i <= 1 ? i : slowRecursive(i - 1) + slowRecursive(i - 2);
}
```

**`xorDecrypt()`** — decrypts character by character:
```java
public static final String xorDecrypt(String encryptedFlag, String key) {
    Intrinsics.checkNotNullParameter(encryptedFlag, "encryptedFlag");
    Intrinsics.checkNotNullParameter(key, "key");
    String str = encryptedFlag;
    ArrayList arrayList = new ArrayList(str.length());
    int i = 0;
    int i2 = 0;
    while (i < str.length()) {
        arrayList.add(Integer.valueOf(key.charAt(i2 % key.length()) ^ str.charAt(i)));
        i++;
        i2++;
    }
    ArrayList arrayList2 = arrayList;
    ArrayList arrayList3 = new ArrayList(CollectionsKt.collectionSizeOrDefault(arrayList2, 10));
    Iterator it = arrayList2.iterator();
    while (it.hasNext()) {
        arrayList3.add(Character.valueOf((char) ((Number) it.next()).intValue()));
    }
    return CollectionsKt.joinToString$default(arrayList3, "", null, null, 0, null, null, 62, null);
}
```

---

## 3 — Decryption
Replicating the algorithm in Python without running the app:
```python
import base64

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

key = str(fib(150))

encrypted = base64.b64decode(
    "cVZaW1dDQllZTFdRW1xeUlBbX21CWFtHalRZXUJFRFhNX1ZcbllGQ15cUUNSRFpcVks="
).decode('utf-8')

flag = "".join(chr(ord(key[i % len(key)]) ^ ord(c)) for i, c in enumerate(encrypted))
print(flag)
```

---

## Result

**Flag:** `Holberton{fibonacci_slow_computation_optimization}`

---