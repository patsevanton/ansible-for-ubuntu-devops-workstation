# TODO: бинарник не запускается на Ubuntu 26.04

Кандидаты, у которых готовый бинарник в GitHub-релизе есть, но на
Ubuntu 26.04 / x86_64 он не работает: собран против старой OpenSSL/glibc,
требует библиотеку, которой в дистрибутиве нет, или опубликован не для этой
платформы.

В плейбук такие утилиты пока не берём. Пересматривать при каждом новом релизе
апстрима (и при обновлении Ubuntu): если появилась сборка под 26.04 или
бинарник стал статическим — взять кандидата в работу и поставить ролью
`binaries`.

Как читать: `- [ ]` — ждёт подходящего релиза; в заметке — что именно
сломано, ссылка на issue апстрима и чем утилита покрыта сейчас.

Заброшенные проекты (архив GitHub, годы без обновлений) сюда не входят: они
описаны только в [`TODO-abandoned.md`](TODO-abandoned.md).

---

## Секреты

- [ ] **teller** — облачно-независимый менеджер секретов для разработчика.
      *(`cargo`)* — [tellerops/teller](https://github.com/tellerops/teller)
      — ⛔ не запускается: последний релиз (v2.0.7, 2024) собран динамически
      против `libssl.so.1.1`, которого нет в Ubuntu 26.04; статических сборок
      и сборок под OpenSSL 3 апстрим не публикует. Отслеживается в
      [tellerops/teller#290](https://github.com/tellerops/teller/issues/290)
      (OPEN; комментарий с проверкой на 26.04 добавлен 2026-10-22).
      Покрывается `sops` + `vault` + `medusa`. Пересмотреть при новом релизе.

## Kubernetes

- [ ] **IceKube** — поиск путей атак в кластере. *(`pipx`)* —
      [WithSecureLabs/IceKube](https://github.com/WithSecureLabs/IceKube)
      — ⛔ не запускается: CLI падает на Python 3.14 с тем же
      `TypeError: Secondary flag is not valid for non-boolean flag`
      (Typer 0.9 + Click). На PyPI лежит `1.0.5` с `typer<0.10`; в main
      версия `1.1.0` с `typer ^0.21` на Python 3.14 запускается.
      Отслеживается в
      [#7](https://github.com/ReversecLabs/IceKube/issues/7) (OPEN).
      Покрывается `kubehound` (граф путей атак) и `rbac-tool`.

## AI и on-call

- [ ] **HolmesGPT** — on-call AI-ассистент по алертам Prometheus. *(`pipx`)* —
      [HolmesGPT/holmesgpt](https://github.com/HolmesGPT/holmesgpt)
      — ⛔ не устанавливается: последний релиз `0.45.0` требует `Python <3.14`,
      а в Ubuntu 26.04 системный Python 3.14, поэтому `pipx` откатывается на
      старую `0.34.0`. Отслеживается в
      [HolmesGPT/holmesgpt#2649](https://github.com/HolmesGPT/holmesgpt/issues/2649).
      Частично покрывается `k8sgpt` (разбор проблем кластера с LLM).
      Пересмотреть, когда апстрим поднимет потолок версии Python.

## Фаззинг

- [ ] **GraphQLer** — dependency-aware фаззинг GraphQL API. *(`pipx`)* —
      [omar2535/GraphQLer](https://github.com/omar2535/GraphQLer)
      — ⛔ не устанавливается: пакет `graphqler` 2.3.8 требует
      `Python >=3.12,<3.13`, а в Ubuntu 26.04 системный Python 3.14.
      `uv run --python 3.12 --with graphqler python -m graphqler` работает,
      но тянет отдельный интерпретатор и обходит правило «ставить в
      системный Python/pipx».
      Покрывается `schemathesis` (GraphQL) и EvoMaster
      (`--problemType GRAPHQL`). Пересмотреть, когда апстрим поднимет
      потолок версии Python.

## Безопасность

- [ ] **vulncov** — корреляция Semgrep-сканов с покрытием тестами. *(`pipx`)* —
      [mllamazares/vulncov](https://github.com/mllamazares/vulncov)
      — ⛔ не устанавливается: пин `faiss-cpu==1.9.0` не имеет колёс под Python
      3.14 (доступны только 1.12+), `pip install git+https://github.com/mllamazares/vulncov.git`
      падает на сборке зависимостей; пакета на PyPI
      нет. Заведено
      [mllamazares/vulncov#1](https://github.com/mllamazares/vulncov/issues/1)
      (OPEN, 2026-10-22). Пересмотреть, если апстрим ослабит пин.
