# TODO: нет готового бинарника на GitHub

Кандидаты, для которых апстрим не публикует готовый бинарник под Linux x86_64:
только исходники (`make`, `go build`, `cargo build`, `git clone`), Helm-чарт,
контейнерный образ или сборка под другую архитектуру.

В плейбук такие утилиты пока не берём. Пересматривать, когда:

- апстрим начнёт публиковать релизные бинарники — тогда берём кандидата в
  работу и ставим ролью `binaries`;
- появится повод собирать из исходников — `go install` (роль `go_apps`),
  pipx (роль `pipx_apps`) или пакет Ubuntu.

Установка из PyPI/npm/Ansible Galaxy сюда не относится: это не «нет
бинарника», а штатный способ установки — такие кандидаты остаются в основном
списке. Исключение — уже добавленный `entropy`: он собирается ролью `go_apps`
и пока остаётся в плейбуке.

Как читать таблицу: «Что это» — назначение утилиты, «В каком виде
поставляется» — что именно отдаёт апстрим и чего не хватает для установки
ролью `binaries`. Все кандидаты ниже ждут релизного linux-amd64 бинарника.

Нодовые агенты (DaemonSet, static Pod), серверные приложения и Helm-чарты
(opencost, dagda, scantron, terrapod, k3s-ansible и т.п.) сюда не входят: они
не устанавливаются на ноутбук по другой причине — см.
[`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md). Заброшенные проекты (архив GitHub,
годы без обновлений) описаны только в [`TODO-abandoned.md`](TODO-abandoned.md).

Способ установки сверен 2026-10-25, De-Nox — 2026-11-04, SpaceAI Guard —
2026-11-05: для GitHub-проектов —
ассеты последнего релиза, для остальных — PyPI/apt. Перенесённые и отброшенные
кандидаты — в конце файла.

---

| Раздел | Кандидат | Что это | В каком виде поставляется |
| --- | --- | --- | --- |
| Диагностика и железо | [linnix](https://github.com/linnix-os/linnix) | eBPF-наблюдаемость с AI-детекцией инцидентов | Исходники и docker-образ; amd64 `.deb` был только в v0.1.0 (`cognitod_0.1.0_amd64.deb`), в v0.1.1 и v0.2.0 ассетов нет. Запрошено в [#124](https://github.com/linnix-os/linnix/issues/124) |
| Безопасность | [flawz](https://github.com/orhun/flawz) | TUI-браузер CVE/уязвимостей | В релизе v0.4.1 только macOS/Windows и `flawz-installer.sh`; готового Linux-бинарника нет (`cargo build`). Запрошено в [#113](https://github.com/orhun/flawz/issues/113) |
| Разработка | [desed](https://github.com/SoptikHa2/desed) | пошаговый отладчик sed-скриптов | В релизе v1.2.2 нет linux-ассетов, только `cargo install desed`. Запрошено в [#40](https://github.com/SoptikHa2/desed/issues/40) |
| Диагностика и железо | [bashdb](https://bashdb.sourceforge.net/) | отладчик bash-скриптов | В Ubuntu пакета нет; апстрим на SourceForge отдаёт только tarball с исходниками и `make install` |
| Удалённый доступ | [Eternal Terminal](https://github.com/MisterTea/EternalTerminal) | ssh-сессия, которая сама переподключается | В релизе `et-v7.0.0` только `arm64.deb` и `orig.tar.gz`; для amd64 нужна сборка из исходников |
| Буфер обмена | [EcoPaste](https://github.com/EcoPasteHub/EcoPaste) | кроссплатформенный менеджер буфера обмена с историей | В релизе `v1.1.0` только macOS и Windows (`.dmg`, `.exe`), Linux-сборки нет. Запрошено в [#1397](https://github.com/EcoPasteHub/EcoPaste/issues/1397) |
| Фаззинг | [honggfuzz](https://github.com/google/honggfuzz) | coverage-guided фаззер нативного кода с Linux perf/Intel PT и санитайзерами | В Ubuntu 26.04 пакета нет; в GitHub-релизах только исходники и `make`, linux-amd64 бинарников нет. Покрывается AFL++ и libFuzzer |
| Фаззинг | [radamsa](https://gitlab.com/akihe/radamsa) | мутационный фаззер общего назначения | В Ubuntu 26.04 пакета нет; апстрим отдаёт исходники и `make`, готовых бинарников нет. `zzuf` закрывает простые мутации |
| Фаззинг | [RESTler](https://github.com/microsoft/restler-fuzzer) | stateful-фаззинг REST по OpenAPI | Релизных бинарников нет: локальная сборка требует Python 3.12.8 и .NET 8, есть только Docker-сборка из исходников. Покрывается schemathesis и EvoMaster. Запрошено в [#850](https://github.com/microsoft/restler-fuzzer/issues/850) |
| Чтение и документы | [TextFold](https://github.com/chenxiachan/textfold) | сворачивает статьи, PDF и веб-страницы в пять уровней детализации — от обзора до исходного текста; умеет отдавать текст агенту по уровню (`python3 -m textfold get`) | В релизе `v0.10.41` только macOS (`.dmg`, `.zip`) и Windows (`TextFold-win-x64-setup.exe`), Linux-сборки нет. PyPI-вариант `textfold` — локальный веб-сервис на `127.0.0.1:3017` с подключением модели, то есть не утилита для ноутбука, а сервис: ставить его ролью `pipx_apps` без юнита systemd бессмысленно |
| AI-агенты и браузер | [LLM-agent-security (SpaceAI Guard)](https://github.com/SpaceAI-UAG/LLM-agent-security) | песочница для агентских харнессов: файловая система deny-by-default, egress через allowlisting-прокси, фильтры промптов и ответов, лимиты сессии и аудит | Релизов нет (статус — прототип), `go.mod` объявляет module `guard` — не путь модуля, поэтому `go install <repo>/cmd/guard@latest` не работает: нужна сборка из исходников. Linux-бэкенд экспериментальный (bubblewrap + user namespaces + seccomp). Сознательно не ставим: прототип без релизов |

---

## Установлены без релизного бинарника

Эти утилиты не попали в таблицу выше, потому что для них есть штатный
способ установки без сборки из исходников:

- **kptop** — добавлен в роль `kubernetes` через pipx. Standalone-бинарников
  в GitHub-релизах нет; запрошены в
  [#85](https://github.com/eslam-gomaa/kptop/issues/85).
- **knetvis** — добавлен в роль `kubernetes` через pipx. В GitHub-релизе
  `v0.1.2` нет ассетов, а на PyPI пока только `0.1.1`; публикация `0.1.2`
  запрошена в
  [#10](https://github.com/samuelarogbonlo/knetvis/issues/10).
- **CloakBrowser** — добавлен в роль `ai_tools` через pipx. Релизных
  бинарников нет (pip/npm-пакет), сам Chromium (~200 МБ) докачивается при
  первом запуске; для запуска нужен лицензионный ключ.

---

## Убрано после проверки 2026-11-05

- **De-Nox** — добавлен в роль `shell`. Начиная с `v0.1.1` релиз собирается
  `cargo-dist` и содержит `de-nox-x86_64-unknown-linux-gnu.tar.xz`; в
  `v0.1.0` ассетов действительно не было.

---

## Убрано после проверки 2026-10-22

- **kubectl-ports-rs** — добавлен в роль `kubernetes` (`kubectl-ports`).
  Оказалось, что готовый бинарник всё же есть: в последнем релизе `1.1.1`
  ассеты не собрались, но в `1.1.0` лежит статический
  `kubectl-ports_1.1.0-x86_64-unknown-linux-musl.tar.gz`. Ставится отдельной
  задачей с зафиксированным тегом.
- **Kubexer**, **Finch**, **kor**, **kubectl-foreach** — рассмотрены вместе с
  очередной волной kubetools и не ставятся: причины в
  [`not-install.md`](not-install.md). **Kubefirst** — не на ноутбук, см.
  [`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md).
- **Krane**, **Kubes** — проверены 2026-10-23: причина отказа — аналоги в
  плейбуке, а не отсутствие бинарника (у обоих только gem).
- **kubectl-kubesec** — убран 2026-10-23: бинарники в релизе есть
  (`kubectl-kubesec_linux_amd64.tar.gz` в `v1.1.0`, 2023), а плагин по
  умолчанию сканирует через hosted `kubesec.io`. Сам `kubesec` в плейбуке уже
  стоит.
- **scan2html** — убран 2026-10-23: бинарник публикуется. В релизе
  `v0.3.28-rc.1` лежат `scan2html_0.3.28-rc.1_linux-amd64.tar.gz` и сборки под
  остальные платформы; штатная установка — плагин Trivy
  (`trivy plugin install scan2html`), то есть кандидат в роль `secrets` рядом
  с `trivy`, а не в этот список.
- **werf**, **kubedog** — убраны из списка 2026-10-23: в плейбуке не
  рассматриваются вообще. Сборка и доставка — задача CI/CD, локальный CLI под
  неё не нужен.
- **odo** — убран 2026-10-23: репозиторий `redhat-developer/odo` в архиве.
- **knee** — не нужен: инфраструктура поднимается своими Ansible-плейбуками,
  а knee — обёртка над 13 плейбуками из своего репозитория.
- **wondershaper**, **sysinfo**, **bench-scripts** — bash-скрипты без
  упаковки. Решение: shell-скрипты в плейбук не берём, даже если апстрим
  когда-нибудь начнёт их релизить.
- **kubectl-sudo** — убран 2026-10-23: в релизе `v1.1.0` ассетов нет, ставится
  только через krew, а сам плагин — шелл-обёртка `#!/bin/sh`
  (`bash/kubectl-sudo`), которая вызывает
  `kubectl --as=... --as-group=system:masters`. Та же причина, что у
  wondershaper/sysinfo/bench-scripts.
- **Click** — убран 2026-10-23: не представляет интереса, работу с кластером
  закрывают `k9s`, `kdash` и `kubectl`. Ставить его всё равно пришлось бы из
  исходников: релизных бинарников нет, только `cargo`.
- **kubecui** — убран 2026-10-23: не представляет интереса, то же место
  занимают `k9s` и `kdash`. К тому же в PyPI его нет и релизов нет — ставить
  пришлось бы из клона.
- **Nelm** — убран 2026-10-23: нужен только в CI/CD, локально дублирует `helm`
  и `helmfile`. Причина «нет бинарника» тоже есть: в GitHub-релизах ассетов
  нет, установка через trdl/install-скрипт.
- **Nighthawk** (layer5io/getnighthawk) — убран 2026-10-23: аналоги лучше.
  HTTP-нагрузку закрывает `k6` (роль `network`), нагрузку на кластер —
  `kube-burner` (роль `kubernetes`). Плюс с 2021 года релизы идут без ассетов:
  бинарники были только в `v1.0.0`–`v1.0.1`, дальше — Docker-образ и Makefile.
- **kondense** — не утилита для ноутбука: работает сайдкаром
  `kondense/kondense:1.1.0` внутри подов и правит им requests/limits.
  Кандидат для кластерных сервисов, рядом с Goldilocks и VPA.
- **EternalTerminal** — под 26.04 собирается amd64-пакет
  `et 7.0.0-resolute1` в PPA `ppa:jgmath2000/et`; проверено на 26.04.1:
  зависимости ставятся, `et --version` отвечает `7.0.0`. В релизе GitHub
  по-прежнему только `et_7.0.0-stable1_arm64.deb`. Оговорка: это PPA, а
  плейбук сейчас подключает сторонний репозиторий только для Docker.
- **mok** (бывший **mokctl**, `bashtools/mokctl` теперь редиректит на
  `bashtools/mok`) — убран 2026-10-23: локальные кластеры уже закрывают `kind`
  и `k3d` из роли `kubernetes`, а сам mok ставится shell-скриптом из
  репозитория, без релизных ассетов.
- **stew** — у апстрима [marwanhawari/stew](https://github.com/marwanhawari/stew)
  есть `stew-v0.6.0-linux-amd64.tar.gz` и `stew_0.6.0_linux_amd64.deb`.
  В файле стояла ссылка на [alxrem/stew](https://github.com/alxrem/stew) —
  это форк без собственных релизов.
- **mcelog** — не нужен: MCE читаются через `dmesg` и `journalctl -k`,
  отдельный демон на ноутбуке не требуется.
- **kubernetes-rbac-audit** — не нужен: есть аналоги с готовыми бинарниками
  (`kubectl-who-can`, `kubeaudit`, `rbac-tool`, `kubehound`).
- **registry-cli** — не нужен: заменяет `regctl` из
  [regclient/regclient](https://github.com/regclient/regclient) (одиночный
  `regctl-linux-amd64` в релизах). Docker-образ `anoxis/registry-cli` не
  нужен.
- **gitlab-registry-images-cleaner** — не нужен: есть штатная GitLab cleanup
  policy и CLI
  [gitlab-container-registry-cleaner](https://github.com/gitlab-container-registry-cleaner/gitlab-container-registry-cleaner)
  (npm). Разовые операции — через `glab api`.

## Убрано после проверки 2026-10-24

- **httpstat** — добавлен в роль `network` (`network_pipx_apps`). Апстрим
  `reorx/httpstat` переписан на Python: один файл без зависимостей,
  публикуется на PyPI, команда `httpstat`. Прежняя причина («релизов нет,
  только `go install`») больше не действует.
