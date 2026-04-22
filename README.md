Prosta aplikacja do skracanie linków.


## Uruchamianie lokalne

Aby uruchomić aplikację lokalnie, wykonaj poniższe kroki:

1. Utwórz kopię pliku konfiguracyjnego:
   ```bash
   cp .env.example .env
   ```

2. Uruchom migracje bazy danych:
   ```bash
   make migrate
   ```

3. Odpal aplikację:
   ```bash
   make run
   ```

## Użycie

Aby skrócić link, wyślij żądanie POST na adres `http://localhost:8000/short/` z nagłówkiem `Content-Type: application/json` oraz polem `url` w formacie JSON:

```bash
curl -X POST http://localhost:8000/short/ \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.google.com"}'
```

W odpowiedzi otrzymasz skrócony link w formacie:
```json
{"url": "<short_url>"}
```

## Testy

Aby uruchomić testy aplikacji, wykonaj komendę:
```bash
make test
```

## Formatowanie

Aby uruchomić formatowanie kodu oraz sprawdzanie typów, wykonaj komendę:
```bash
make format
```
