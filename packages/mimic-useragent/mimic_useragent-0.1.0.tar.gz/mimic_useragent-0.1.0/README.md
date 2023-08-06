# mimic_user_agent

Funcion que retorna un 'user-agent' falso aleatorio o estático.

# Uso

```python
>>> from mimic_user_agent.mimicUserAgent import mimic_user_agent
>>> mimic_user_agent()
'Mozilla/5.0 (X11; Linux; i686 on x86_64; rv:112.0) Gecko/20100101 Firefox/112.0'
>>>
>>>
>>> mimic_user_agent(1)
'Mozilla/5.0 (Windows NT 10.0; x86; rv:107.0) Gecko/20100101 Firefox/107.0'
```

Recibe un parámetro `int` para el uso de una *seed*, por defecto es `None`.

---

**Aclaración:**

Por ahora, solamente genera user-agent Firefox.

---

# Tests

```python
python -m unittest
```
