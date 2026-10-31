# TODO: схемы из Terraform/Terragrunt (аналог KubeDiagrams для Yandex Cloud)

Задача: получать архитектурную схему из Terraform/Terragrunt-кода, как
KubeDiagrams делает это для манифестов Kubernetes. Ограничения: инфраструктура
в Yandex Cloud, стек разбит на много terragrunt-юнитов (`live/<env>/<зона>/<сервис>`),
руками схемы не поддерживаются.

Готового решения нет: KubeDiagrams читает манифесты k8s, а не HCL; все
Terraform-визуализаторы либо не знают YC-провайдер, либо не знают про
terragrunt. Поэтому план — три слоя разной степени готовности: два уже
устанавливаются плейбуком, третий (свой генератор) описан ниже.

Дата ревизии: 2026-10-22.

---

## 1. Что уже даёт плейбук

| Инструмент | Роль | Что делает |
|---|---|---|
| **graphviz** (`dot`) | `iac`, apt | рендер DOT → svg/png; нужен всем остальным |
| **inframap** `v0.8.0` | `iac`, бинарник | tfstate или HCL → DOT; выбрасывает служебные узлы Terraform |
| **rover** | `iac`, бинарник | plan JSON → интерактивная схема в браузере или standalone HTML |

Плюс встроенное, что ставить не надо:

- `terraform graph` — граф зависимостей юнита (сырой, со служебными узлами);
- `terragrunt dag graph` (v0.93+) — DAG юнитов в DOT, алиас
  `terragrunt list --format=dot --dag --dependencies --external`.

Почему inframap зафиксирован на `v0.8.0`: релиз `v0.8.1` опубликован только
исходниками, бинарников в нём нет. Роль `binaries` умеет поле `version` —
именно для таких случаев. Обсуждение — в
[#246](https://github.com/cycloidio/inframap/issues/246); к нему добавлен
комментарий от 2026-10-26, что ассетов всё ещё нет и что на плейбуке можно
проверить сборку.

## 2. Слои, которые нужны на практике

### Слой 1 — карта юнитов (работает сегодня)

```bash
terragrunt dag graph > dag.dot && dot -Tsvg dag.dot -o dag.svg
terragrunt dag graph --working-dir live/prod > prod.dot   # по окружению
```

Это то, что нужно при большом количестве модулей: узлы — юниты, рёбра —
`dependency`-блоки. Без `init`, `plan` и облачных кредов. Иконок YC нет,
но карта связей читается.

### Слой 2 — один юнит в деталях (работает сегодня)

```bash
cd live/prod/ru-central1-d/k8s
terragrunt run -- plan -out=/tmp/k8s.tfplan
terragrunt run -- show -json /tmp/k8s.tfplan > /tmp/k8s-plan.json  # для rover
terragrunt run -- show -json > /tmp/k8s-state.json                 # для inframap

inframap generate /tmp/k8s-state.json | dot -Tsvg > k8s-inframap.svg
rover -planJSONPath /tmp/k8s-plan.json -standalone   # rover/index.html
```

Для inframap можно и без плана: `inframap generate ./modules/k8s/` — он
читает HCL, но по одному модулю, а не по стеку.

### Слой 3 — схема с иконками YC (надо писать)

Единственный способ получить «как в KubeDiagrams»: свой генератор, который
берёт DAG юнитов из слоя 1 и подписывает каждый узел иконкой сервиса YC.
Ниже — его план.

---

## 3. Кандидаты, которые сознательно не ставим

- **KubeDiagrams** — принимает манифесты Kubernetes и набор иконок k8s, к
  Terraform неприменим. Полезен как образец UX (группировка по namespace ≙
  группировка по каталогу/окружению).
- **Terravision** (`pipx`, 0.56.0) — рисует из TF-кода, иконки официальные,
  но только AWS/GCP/Azure/OCI. Для YC смысла нет.
- **mingrammer/diagrams** — Python-DSL для ручного рисования, провайдера
  Yandex нет. Может пригодиться внутри `tfmap` через `diagrams.custom.Custom`,
  но как самостоятельный инструмент не нужен.
- **Cloudcraft, Brainboard, Pluralith** — SaaS/закрытые, YC-провайдер не
  поддерживают.
- **drawio-desktop** (`.deb` в релизах jgraph) — не ставим: Electron-приложение
  на ноутбуке ради схемы, которая открывается в `app.diagrams.net`. Вернуться
  к вопросу, если понадобится офлайн-режим.
- **yc-embed-drawio-into-terraform-deployment** и **yc-architect-solution-library**
  — не утилиты, а методика и референсные архитектуры. Идею `templatefile()`
  с параметризованным draw.io закладываем в `tfmap` (но там генерация из
  состояния, а не из шаблона).
- **Иконки Yandex Cloud** — официальный ZIP для draw.io/Visio в
  <https://yandex.cloud/ru/brandbook>. Нужен `tfmap`; проверить условия
  использования перед распространением схем за пределами компании.

## 4. `tfmap` — план генератора

Вход: корень terragrunt-репозитория. Выход: схема в mermaid и/или draw.io,
по одной на окружение + обзорная.

Фазы:

- [ ] **Сбор юнитов**: `terragrunt find --format=json --dependencies --reading`
      (не запускать `plan`, не требовать кредов).
- [ ] **Нормализация**: путь → `env` / `region` / `unit`; короткое имя для
      подписи; группировка по первым двум сегментам.
- [ ] **Определение сервиса**: разобрать `terraform { source }` юнита,
      прочитать исходники модуля (локальный путь или кэш
      `~/.cache/terragrunt/modules`), собрать все `yandex_*` типы ресурсов,
      взять доминирующий. Fallback — по имени юнита (`k8s`, `postgres`,
      `bucket`).
- [ ] **Маппинг тип → сервис → иконка**: таблица на 20–30 записей
      (`yandex_kubernetes_cluster` → Managed Kubernetes,
      `yandex_mdb_postgresql_cluster` → Managed PostgreSQL,
      `yandex_vpc_network` → VPC, `yandex_compute_instance` → Compute Cloud,
      `yandex_alb_load_balancer` → Application Load Balancer,
      `yandex_storage_bucket` → Object Storage, `yandex_kms_symmetric_key` → KMS
      и т.д.). Неизвестный тип → серая заглушка с именем типа.
- [ ] **Рёбра**: из `dependencies` (явные) и из `dependency`-блоков; внешние
      зависимости (вне текущего окружения) — пунктиром.
- [ ] **Вывод mermaid**: `graph TD` с `subgraph` по окружениям. Рендерится в
      GitLab/GitHub из MR без установки чего-либо.
- [ ] **Вывод draw.io**: mxGraph XML с иконками из брендбука; открывается и
      правится руками, экспортируется в svg/png.
- [ ] **Сворачивание**: при >60 юнитов в окружении — группировать по региону,
      детали выносить в отдельную диаграмму.
- [ ] **CI**: job в GitLab CI, артефакты `dag.svg` + `*.drawio`, картинка в
      описании MR; триггер — изменения в `live/**`.

Краевые случаи, которые надо решить до реализации:

- юниты, созданные `for_each`/`generate` (имя в DAG одно, ресурсов много);
- terragrunt stacks (`terragrunt.stack.*`) — узлы не совпадают с каталогами;
- юниты без ресурсов YC (helm-релизы, kubernetes-манифесты) — рисовать
  отдельным цветом или пропускать;
- зависимости между окружениями (`prod` → `shared`) — не должны ломать
  группировку;
- несколько юнитов с одинаковым коротким именем (`vpc` в каждом окружении);
- модули из приватного реестра — как читать исходники без `init`.

Критерии готовности: на реальном стеке схема строится одной командой без
облачных кредов, у каждого юнита видна иконка сервиса, рёбра совпадают с
`dependency`-блоками, mermaid-версия обновляется в MR автоматически.

## 5. Открытые вопросы

- Приоритет формата: mermaid (дёшево, живёт в MR) или draw.io (красиво, но
  бинарный XML в Git)?
- Хранить иконки YC в репозитории `tfmap` или тянуть из брендбука при сборке?
- Нужна ли детализация до ресурсов внутри юнита (вторая диаграмма из
  `state.json` через inframap) или достаточно юнитов?
