# TODO: утилиты из трендов GitHub за последние 5 лет

Срезка на **2026-10-26**. Пятилетнее окно — репозитории, созданные после
**2021-10-26**. Свежая половина окна (2023-10-24 — 2026-10-24) уже разобрана в
[`TODO-trend-github-last-3-years.md`](TODO-trend-github-last-3-years.md),
поэтому здесь только вторая половина — **2021-10-26 — 2023-10-24**. Так список
не дублирует прошлую партию, а закрывает два года, которые в неё не попадали;
вместе два файла и дают пятилетний обзор.

Источники: `github.com/trending` (день/неделя/месяц) и GitHub Search API
(`created:2021-10-26..2023-10-24`, сортировка по звёздам) по темам `cli`,
`tui`, `terminal`, `developer-tools`, `devops`, `iac`, `linux`, `kubernetes`,
`security`, `productivity`, `monitoring`, `networking`, `ssh`, `docker`, `git`,
`sql`, `file-manager`, `backup`, `shell`. Дополнительно — широкий поиск по
звёздам без темы и точечные запросы `kubectl`, `terraform`, `ansible`,
`github actions`.

По каждому кандидату через `gh api repos/{owner}/{repo}` проверены дата
создания, лицензия, архивность и последний push, через
`releases/latest` — наличие Linux-сборки под x86_64 и имена ассетов. Звёзды,
версии и даты — на 2026-10-26. Кандидаты, которые уже описаны в `README.md`,
`not-install.md` или других `TODO-*.md`, в список не попадали; для apt
проверено наличие пакета в серии `resolute` (Ubuntu 26.04).

Как читать: `- [ ]` — не добавлен; в заметке — что даёт утилита, чем
отличается от уже установленного и при каком условии к ней стоит вернуться.
Итоговый план — в конце файла.

---

## Итог: что действительно стоит добавить

| Кандидат | Роль | Установка | ⭐ | Лицензия | Решение |
|---|---|---|---|---|---|
| **ruff** | `base` | pipx или бинарник | 50.3k | MIT | добавлен |
| **d2** | `iac` | бинарник `tar.gz` | 25.7k | MPL-2.0 | добавлен |
| **binsider** | `base` | бинарник `tar.gz` | 4.5k | Apache-2.0 | отклонён |
| **pinact** | `git` | бинарник `tar.gz` | 1.2k | MIT | добавлен |
| **distrobox** | `base` | apt `distrobox` | 13.1k | GPL-3.0 | отклонён |
| **inshellisense** | `shell` | npm | 10.7k | MIT | добавлен |
| **tfautomv** | `iac` | бинарник `tar.gz` | 898 | Apache-2.0 | добавлен |
| **cdebug** | `kubernetes` | бинарник `tar.gz` | 1.7k | Apache-2.0 | добавлен |
| **kubectl-explore** | `kubernetes` | бинарник `tar.gz` | 609 | MIT | добавлен |
| **localsend** | — | — | 95.7k | Apache-2.0 | отклонён |

Семь CLI-утилит из списка стоят в плейбуке с 2026-10-26. `binsider`,
`distrobox` и `localsend` отклонены по запросу: `binsider` дублирует
`file`/`readelf`/`objdump`/`strings`/`strace`, `distrobox` не нужен при уже
стоящем Docker, а `localsend` — GUI-приложение для обмена файлами с
телефоном, а не DevOps-утилита.

---

## Python и данные

- [x] **ruff** — линтер и форматтер Python на Rust, один бинарник на lint +
      format, конфиг в `pyproject.toml`. *(50.3k ⭐, MIT, Linux x86_64,
      `pipx`/`tar.gz`)* — [astral-sh/ruff](https://github.com/astral-sh/ruff)
      — **добавлен** в роль `base` (`base_pipx_apps`, `creates: ruff`).
      Причина: в плейбуке нет ни одного линтера Python. Есть `shellcheck`,
      `hadolint`, `yamllint`, `ansible-lint`, `tflint`, `zizmor`, но для
      Python локально нет ничего. Ruff закрывает `flake8` + `isort` +
      `pyupgrade` + `pylint`-класс правил и умеет `ruff format` вместо
      `black`. Нужен для Ansible-модулей, фильтров,
      локальных скриптов и проверки кода перед коммитом. Не заменяет
      `yamllint` и `ansible-lint`: другие языки и другие правила. В apt
      `resolute` пакета нет, поэтому pipx или релизный бинарник.
- [ ] **gql (GitQL)** — SQL-подобные запросы к истории git: коммиты, авторы,
      ветки, diff, агрегаты и оконные функции. *(3.5k ⭐, MIT, Linux x86_64)* —
      [AmrDeveloper/GQL](https://github.com/AmrDeveloper/GQL) — не добавлен:
      `git log` + `jq`/`delta`/`lazygit` закрывают повседневные вопросы, а
      SQL по истории нужен редко. Пересматривать, если появятся регулярные
      отчёты по репозиториям (кто менял файл, динамика по авторам).
- [ ] **PRQL** — pipelined-язык запросов, компилируется в SQL; читается
      сверху вниз, без вложенных `SELECT`. *(10.9k ⭐, Apache-2.0, Linux
      x86_64)* — [PRQL/prql](https://github.com/PRQL/prql) — не добавлен:
      `duckdb`, `octosql` и `harlequin` уже закрывают ad-hoc SQL по
      CSV/Parquet/JSON, а PRQL требует переписывать привычные запросы.
      Пересматривать, если аналитические запросы станут ежедневными.
- [ ] **refurb** — модернизация Python-кода: устаревшие конструкции,
      подозрительные места, предложения по замене. *(2.5k ⭐, GPL-3.0,
      `pipx`)* — [dosisod/refurb](https://github.com/dosisod/refurb) — не
      добавлен: пересекается с `ruff` и работает только как анализатор, без
      автофикса. Ruff с правилами `UP`/`B`/`SIM` покрывает почти то же самое.
- [ ] **pyapp** — рантайм-установщик Python-приложений: собирает
      самодостаточный бинарник, который при первом запуске подтягивает нужный
      Python. *(2.0k ⭐, без лицензии, только исходники)* —
      [ofek/pyapp](https://github.com/ofek/pyapp) — не добавлен: лицензии нет,
      релизных бинарников нет, а задача упаковки Python-приложений на
      ноутбуке не стоит. Пересматривать, если понадобится раздавать свои
      Python-CLI без окружения.

## Схемы и IaC

- [x] **d2** — diagram-as-code: текстовый DSL → SVG/PNG, слои, контейнеры,
      sequence- и class-диаграммы, темы и иконки. *(25.7k ⭐, MPL-2.0,
      `d2-v0.9.0-linux-amd64.tar.gz`)* —
      [d2lang/d2](https://github.com/d2lang/d2) — **добавлен** в роль `iac`.
      Причина: сейчас схемы закрывают `graphviz`/`dot` (рендер DOT),
      `inframap` (tfstate/HCL → DOT) и `rover` (plan JSON → HTML), но все они
      строят схему из инфраструктуры. Для ручной архитектурной схемы,
      sequence-диаграммы или схемы «как устроен стенд» нужен отдельный DSL;
      `mermaid` в наборе нет, а d2 — один статический бинарник и читаемый
      текстовый формат, который удобно держать в git рядом с Terragrunt.
      Не заменяет `inframap`/`rover`: те извлекают граф автоматически, d2
      рисует то, что описал человек. MPL-2.0 — слабый копилефт, для
      установки бинарника ограничений нет.
- [x] **tfautomv** — генерирует `moved`-блоки Terraform: сравнивает план до и
      после переименования/переноса ресурса и печатает готовые блоки, чтобы
      не потерять state. *(898 ⭐, Apache-2.0, `linux_amd64.tar.gz`)* —
      [busser/tfautomv](https://github.com/busser/tfautomv) — **добавлен** в
      роль `iac`. Причина: в репозитории много Terragrunt-юнитов и модулей,
      а ручной `moved` после рефакторинга — типичная причина `destroy/create`.
- [ ] **KCL** — язык конфигурации со схемами, валидацией и генерацией
      Kubernetes/YAML; альтернатива CUE и Helm-шаблонам. *(2.4k ⭐,
      Apache-2.0, Linux x86_64)* — [kcl-lang/kcl](https://github.com/kcl-lang/kcl)
      — не добавлен: в наборе уже есть Helm, Kustomize, `cdk8s`, `kosko`,
      `timoni` (CUE) и `atmos`; ещё один язык конфигурации увеличит
      когнитивную нагрузку без явной задачи. Пересматривать, если появится
      проект, где KCL уже используется.
- [ ] **tf-summarize** — компактная сводка `terraform plan`: таблица
      create/update/delete, JSON и фильтры. *(743 ⭐, MIT, `.deb`/`.apk`)* —
      [dineshba/tf-summarize](https://github.com/dineshba/tf-summarize) — не
      добавлен: роль `iac` уже ставит `tgsieve` для сжатого вывода
      `terragrunt plan`; вторая утилита под ту же задачу не нужна.
      Пересматривать, если `tgsieve` перестанет поддерживать формат
      Terragrunt-плана.
- [ ] **KICS** — поиск ошибок безопасности и misconfiguration в Terraform,
      Kubernetes, Dockerfile, Helm и Ansible. *(2.7k ⭐, Apache-2.0)* —
      [Checkmarx/kics](https://github.com/Checkmarx/kics) — вне пятилетнего
      окна (создан 2020-07-08) и не нужен: `checkov`, `trivy`, `tfsec` и
      `semgrep` уже покрывают IaC и код. Упомянут, чтобы не искать заново.

## Терминал, shell и файлы

- [x] **inshellisense** — IDE-подобное автодополнение прямо в строке shell:
      подсказки по командам и флагам, история, popup-меню; поддерживает bash,
      zsh, fish, pwsh и nushell. *(10.7k ⭐, MIT, npm
      `@microsoft/inshellisense`, linux-x64 `tgz`)* —
      [microsoft/inshellisense](https://github.com/microsoft/inshellisense) —
      **добавлен** в роль `shell` через npm (как `tldr`), флаг
      `inshellisense_install` (по умолчанию включён). Причина: сейчас
      автодополнение — статическое (`bash-completion`) плюс `fzf`/`zoxide` для
      файлов и каталогов; inshellisense даёт inline-подсказки в стиле IDE.
      Ограничение: версия `0.0.4`, то есть pre-1.0.
- [ ] **xdg-ninja** — проверяет `$HOME` на файлы и каталоги, которые
      приложения создали вне XDG-путей, и показывает, как их перенастроить.
      *(3.4k ⭐, MIT, shell-скрипт `xdgnj`)* —
      [b3nj5m1n/xdg-ninja](https://github.com/b3nj5m1n/xdg-ninja) — не
      добавлен: разовая гигиена домашнего каталога, не ежедневная утилита;
      запускается вручную, установка не нужна. Пересматривать, если `$HOME`
      снова зарастёт мусором от новых приложений.
- [ ] **hishtory** — история shell с синхронизацией между машинами, поиском
      по контексту (каталог, хост, exit code) и шифрованием. *(3.1k ⭐, MIT,
      `hishtory-linux-amd64`)* —
      [ddworken/hishtory](https://github.com/ddworken/hishtory) — не добавлен:
      `mcfly` уже стоит и закрывает локальный Ctrl-R; для синхронизации нужен
      сервер/аккаунт, а история shell — чувствительные данные. Пересматривать,
      если появится вторая машина и понадобится общая история.
- [ ] **presenterm** — показ Markdown-презентаций в терминале: слайды,
      подсветка кода, изображения, заметки докладчика. *(8.9k ⭐,
      BSD-2-Clause, Linux x86_64)* —
      [mfontanini/presenterm](https://github.com/mfontanini/presenterm) — не
      добавлен: не DevOps-инструмент, презентации на ноутбуке делаются не в
      терминале. Пересматривать, если понадобится доклад без Keynote.
- [ ] **walk** — TUI-файловый менеджер с быстрым переходом и предпросмотром.
      *(3.6k ⭐, MIT)* — [antonmedv/walk](https://github.com/antonmedv/walk) —
      не добавлен: `yazi`, `lf`, `superfile` и `M-Commander` уже закрывают
      файловые менеджеры. Пересматривать, если понадобится минималистичный
      одномодельный вариант.
- [ ] **sshs** — TUI для SSH: список хостов из `~/.ssh/config`, поиск и
      подключение. *(1.6k ⭐, MIT)* —
      [quantumsheep/sshs](https://github.com/quantumsheep/sshs) — не добавлен:
      `lazyssh` и `omnyssh` уже стоят и делают то же с большим числом
      возможностей.
- [ ] **tssh (trzsz-ssh)** — drop-in замена `ssh` с поддержкой `trzsz`
      (передача файлов прямо в сессии), поиском по хостам и сохранением
      паролей. *(2.8k ⭐, MIT)* —
      [trzsz/trzsz-ssh](https://github.com/trzsz/trzsz-ssh) — не добавлен:
      `omnyssh` и `lazyssh` закрывают выбор хостов, а `trzsz` сам по себе
      нужен только при постоянной передаче файлов через SSH-сессию.
- [ ] **oxker** — TUI для Docker: контейнеры, логи, статистика, действия.
      *(2.0k ⭐, MIT)* — [mrjackwills/oxker](https://github.com/mrjackwills/oxker)
      — не добавлен: `lazydocker`, `ctop` и `dry` уже стоят.
- [ ] **jqp** — TUI-песочница для `jq`: запрос и результат рядом, история,
      подсказки. *(2.9k ⭐, MIT)* — [noahgorstein/jqp](https://github.com/noahgorstein/jqp)
      — не добавлен: `jnv` уже даёт интерактивный `jq`-фильтр, а `fx` —
      просмотр JSON. Третья TUI под тот же JSON не нужна.

## Git и CI

- [x] **pinact** — пиннит версии GitHub Actions и reusable workflows по SHA,
      обновляет их и проверяет аннотации версий. *(1.2k ⭐, MIT,
      `pinact_linux_amd64.tar.gz`)* —
      [suzuki-shunsuke/pinact](https://github.com/suzuki-shunsuke/pinact) —
      **добавлен** в роль `git`. Причина: `zizmor` уже проверяет workflow на
      опасные выражения, права и unpinned-экшены, но только сообщает о
      проблеме; pinact приводит файл в порядок (`pinact run`) и обновляет
      пины (`pinact run --update`). В репозитории есть GitHub Actions, так что
      пара «zizmor + pinact» закрывает и аудит, и исправление. Альтернатива —
      `sethvargo/ratchet` (970 ⭐): pinact активнее и умеет annotations.
- [ ] **git-cliff** — генератор changelog из Conventional Commits с шаблонами
      и интеграцией в CI. *(12.3k ⭐, Apache-2.0, Linux x86_64)* —
      [orhun/git-cliff](https://github.com/orhun/git-cliff) — не добавлен по
      двум причинам: создан 2021-05-30, то есть формально вне пятилетнего
      окна, и в роли `git` уже стоит `changie` для фрагментов changelog.
      Пересматривать, если понадобится генерировать changelog из истории
      коммитов, а не из фрагментов.
- [ ] **better-commits** — интерактивный мастер Conventional Commits: тип,
      scope, описание, breaking change, issue. *(2.3k ⭐, MIT, npm)* —
      [Everduin94/better-commits](https://github.com/Everduin94/better-commits)
      — не добавлен: в наборе уже есть `lumen`, `gptcommit` и `codegpt` для
      сообщений коммитов, а формат Conventional Commits задан правилами
      репозитория. Пересматривать, если понадобится офлайн-мастер без LLM.
- [ ] **cz-git** — адаптер Commitizen и CLI `czg` для Conventional Commits.
      *(1.5k ⭐, MIT, npm)* — [Zhengqbbb/cz-git](https://github.com/Zhengqbbb/cz-git)
      — не добавлен по той же причине, что и `better-commits`; плюс требует
      Commitizen в проекте.
- [ ] **dura** — фоновые снапшоты git-репозитория, чтобы не потерять
      незакоммиченную работу. *(4.4k ⭐, без лицензии, Linux x86_64)* —
      [tkellogg/dura](https://github.com/tkellogg/dura) — не добавлен:
      лицензии нет, а `git` + `etckeeper` + регулярные коммиты уже закрывают
      сохранность; `dura` к тому же не обновлялся с 2026-03. Пересматривать
      только если появится политика «каждые 5 минут».
- [ ] **gitbutler** — GUI-клиент git с виртуальными ветками и AI-коммитами.
      *(21.9k ⭐, без SPDX-лицензии)* —
      [gitbutlerapp/gitbutler](https://github.com/gitbutlerapp/gitbutler) — не
      добавлен: GUI, а в наборе уже есть `lazygit`, `gitui`, `jjui` и `tuicr`;
      лицензия не SPDX, для установки в плейбук это лишний риск.

## Контейнеры и Kubernetes

- [ ] **distrobox** — запуск любой Linux-дистрибутива в контейнере с
      интеграцией в домашний каталог, устройства, звук и графику; работает
      поверх Docker или Podman. *(13.1k ⭐, GPL-3.0, apt 1.8.2.4 в
      `resolute`)* — [89luca89/distrobox](https://github.com/89luca89/distrobox)
      — не добавлен: отклонён по запросу. Чужой бинарь или тулчейн
      запускается `docker run`, а отдельный дистрибутив в контейнере на
      ноутбуке не нужен.
- [x] **cdebug** — отладочный контейнер в pod/контейнере: эфемерные
      контейнеры, выбор образа с инструментами, `exec`, копирование файлов,
      проброс портов. *(1.7k ⭐, Apache-2.0, `cdebug_linux_amd64.tar.gz`)* —
      [iximiuz/cdebug](https://github.com/iximiuz/cdebug) — **добавлен** в
      роль `kubernetes`. Причина: `kubectl debug` уже встроен и закрывает
      базовый сценарий; cdebug удобнее, когда нужен конкретный набор
      инструментов и повторяемые команды.
- [x] **kubectl-explore** — fuzzy-поиск по `kubectl explain`: находит поле по
      имени и показывает документацию без точного знания пути. *(609 ⭐, MIT,
      `kubectl-explore_v0.14.1_linux_amd64.tar.gz`)* —
      [keisku/kubectl-explore](https://github.com/keisku/kubectl-explore) —
      **добавлен** в роль `kubernetes` бинарником (krew не нужен). Причина:
      `kubectl explain` требует точного пути, а `k9s`/`kubectl-tree` не
      заменяют справку по полям. Последний релиз — ноябрь 2025; у бинарника
      нет `--version`, проверка установки — `kubectl-explore --help`.
- [ ] **kwok** — симуляция тысяч нод и кластеров Kubernetes без kubelet, для
      проверки планировщика и контроллеров. *(3.2k ⭐, Apache-2.0)* —
      [kubernetes-sigs/kwok](https://github.com/kubernetes-sigs/kwok) — не
      добавлен: `kind` и `k3d` уже стоят и дают настоящий кластер в Docker;
      симуляция нужна для тестов масштабирования, а не для ноутбука.
- [ ] **karpor** — визуализация Kubernetes: граф ресурсов и поиск по кластеру.
      *(1.7k ⭐, Apache-2.0)* — [kusionstack/karpor](https://github.com/kusionstack/karpor)
      — не добавлен: `k9s`, `kubectl-tree`, `kubecolor` и `kubefetch` уже
      закрывают обзор; karpor — веб-приложение, а не CLI.
- [ ] **cyclops** — веб-UI для Kubernetes-манифестов с формами вместо YAML.
      *(3.3k ⭐, Apache-2.0)* —
      [cyclops-ui/cyclops](https://github.com/cyclops-ui/cyclops) — не
      добавлен: это кластерный сервис/веб-UI, не утилита ноутбука.
- [ ] **helm-dashboard** — веб-UI для Helm-релизов. *(5.9k ⭐, Apache-2.0)* —
      [komodorio/helm-dashboard](https://github.com/komodorio/helm-dashboard)
      — не добавлен: `helm`, `helm-diff`, `helm-secrets` и `k9s` уже дают
      всю работу с релизами; отдельный дашборд на ноутбуке не нужен.
- [ ] **docker-rollout** — zero-downtime перезапуск `docker compose`:
      поднимает новый контейнер, ждёт healthcheck, переключает трафик.
      *(3.4k ⭐, MIT, один бинарник)* —
      [wowu/docker-rollout](https://github.com/wowu/docker-rollout) — не
      добавлен: задача из мира серверов, а ноутбук не обслуживает
      production-трафик; `docker compose up -d` достаточно.
- [ ] **dockcheck** — проверка и обновление образов Docker с бэкапом,
      автоочисткой и уведомлениями. *(2.5k ⭐, GPL-3.0, shell-скрипт)* —
      [mag37/dockcheck](https://github.com/mag37/dockcheck) — не добавлен:
      обновление образов на ноутбуке не критично, а `docker compose pull`
      уже есть; плюс это скрипт, а не релизный бинарник.

## Сеть и обмен файлами

- [ ] **localsend** — передача файлов между ноутбуком и телефоном/другим
      компьютером по локальной сети, без облака; GUI-приложение. *(95.7k ⭐,
      Apache-2.0, `.deb`/AppImage/`tar.gz`)* —
      [localsend/localsend](https://github.com/localsend/localsend) — не
      добавлен: отклонён по запросу. Это GUI-приложение, а не DevOps-утилита;
      `rclone`, `sshfs` и `socat` закрывают передачу файлов на серверы, а
      передача на телефон — отдельная задача, которая решается установкой
      вручную.
- [ ] **bore** — минимальный TCP-туннель к localhost через публичный
      `bore.pub` или свой сервер. *(11.6k ⭐, MIT, Linux musl x86_64)* —
      [ekzhang/bore](https://github.com/ekzhang/bore) — не добавлен: `chisel`
      (TCP/UDP поверх HTTP), `sshx` (совместный терминал) и `gotty` (терминал
      в браузере) уже стоят; `bore` требует внешний сервер и даёт меньше
      возможностей, чем `chisel`. Пересматривать, если понадобится совсем
      простой проброс порта одной командой.
- [ ] **natmap** — проброс TCP/UDP-порта через full-cone NAT без внешнего
      сервера. *(2.0k ⭐, MIT, Linux-бинарники)* —
      [heiher/natmap](https://github.com/heiher/natmap) — не добавлен: сценарий
      домашнего NAT/роутера, а не ноутбука DevOps; для доступа к хостам есть
      `netbird` и `wireguard-tools`.
- [ ] **airgorah** — аудит Wi-Fi: сканирование точек доступа, клиентов,
      рукопожатий, deauth-тесты; GUI на Rust/GTK. *(4.8k ⭐, MIT, `.deb`)* —
      [martin-olivier/airgorah](https://github.com/martin-olivier/airgorah) —
      не добавлен: нужен адаптер с monitor mode, а на ноутбуке это
      hardware-specific и не всегда доступно; для аудита Wi-Fi есть `nmap`,
      `sx` и `aircrack-ng` (если понадобится, ставить отдельно).
- [ ] **zrok** — self-hosted-совместимый обмен файлами и туннели с
      end-to-end шифрованием. *(4.8k ⭐, Apache-2.0)* —
      [openziti/zrok](https://github.com/openziti/zrok) — не добавлен: требует
      аккаунт/сервис и закрывает то же, что `chisel`/`sshx`, но с внешней
      инфраструктурой.
- [ ] **warpgate** — бастион/PAM для SSH, HTTPS, Kubernetes, БД и RDP без
      клиентского ПО. *(8.1k ⭐, Apache-2.0)* —
      [warp-tech/warpgate](https://github.com/warp-tech/warpgate) — не
      добавлен: это серверный компонент, не утилита ноутбука.

## Безопасность, железо и прочее

- [ ] **binsider** — TUI-анализ ELF: заголовки, секции, динамические
      зависимости, строки, hex-дамп, эвристики. *(4.5k ⭐, Apache-2.0,
      `binsider-0.3.2-x86_64-unknown-linux-gnu.tar.gz`)* —
      [orhun/binsider](https://github.com/orhun/binsider) — не добавлен:
      отклонён по запросу. Для бинарников уже есть `file`, `readelf`,
      `objdump`, `strings` и `strace` — TUI поверх тех же данных не нужен.
- [ ] **bbot** — рекурсивный интернет-сканер: поддомены, порты, технологии,
      уязвимости, интеграции с десятками источников. *(10.9k ⭐, AGPL-3.0,
      `pipx`)* — [blacklanternsecurity/bbot](https://github.com/blacklanternsecurity/bbot)
      — не добавлен: тяжёлый OSINT-сканер, пересекается с `nmap`, `uncover` и
      `dnsglobe`, а AGPL и большой объём зависимостей усложняют роль.
      Пересматривать, если понадобится именно рекурсивная разведка.
- [ ] **kanata** — переназначение клавиатуры на уровне драйвера: слои,
      макросы, tap-hold, home-row mods; работает в Linux/Windows/macOS.
      *(8.0k ⭐, LGPL-3.0, `linux-binaries-x64.zip`)* —
      [jtroo/kanata](https://github.com/jtroo/kanata) — не добавлен: настройка
      клавиатуры индивидуальна, требует udev/uinput и прав; универсальной
      конфигурации для плейбука нет. Пересматривать при покупке
      programmable-клавиатуры.
- [ ] **bpftune** — автотюнинг сетевого стека и системы через eBPF, без
      статических sysctl. *(1.9k ⭐, без SPDX, C)* —
      [oracle/bpftune](https://github.com/oracle/bpftune) — не добавлен:
      меняет параметры ядра автоматически, а плейбук уже управляет sysctl
      явно (`99-devops-inotify.conf`); предсказуемость важнее автомагии.
- [ ] **netexec** — сетевой «швейцарский нож» для пентеста: SMB, LDAP, SSH,
      WinRM, MSSQL. *(5.9k ⭐, BSD-2-Clause, `pipx`)* —
      [Pennyw0rth/NetExec](https://github.com/Pennyw0rth/NetExec) — не
      добавлен: offensive-инструмент, а в наборе уже есть `nmap`, `sx`,
      `httpx`/`xh` и `nuclei`-класс сканеров; для разрешённых пентестов
      ставится отдельно.
- [ ] **cloudfox** — автоматизация разведки в облаке (AWS/Azure/GCP) для
      пентеста. *(2.6k ⭐, MIT)* —
      [BishopFox/cloudfox](https://github.com/BishopFox/cloudfox) — не
      добавлен: облака в работе — Yandex Cloud, а инструмент заточен под
      AWS/Azure/GCP.
- [ ] **stratus-red-team** — эмуляция техник атак на AWS/Azure/GCP для
      проверки детектов. *(2.4k ⭐, Apache-2.0)* —
      [DataDog/stratus-red-team](https://github.com/DataDog/stratus-red-team)
      — не добавлен: облачные сценарии не про Yandex Cloud, а для локальных
      проверок есть `tracee` и `osquery`.
- [ ] **process-compose** — планировщик и TUI для локальных
      неконтейнерных процессов: зависимости, healthcheck, логи, рестарты.
      *(2.9k ⭐, Apache-2.0, `process-compose_linux_amd64.tar.gz`)* —
      [F1bonacc1/process-compose](https://github.com/F1bonacc1/process-compose)
      — не добавлен: `docker compose` закрывает контейнеры, а `task`/`just` и
      `mise` — локальные задачи; process-compose полезен для «поднять пять
      сервисов без Docker», но это редкий сценарий на ноутбуке.

---

## Что уже стоит из этой волны

Чтобы не искать заново: из трендов последних лет в плейбуке уже есть `yazi`,
`gum`, `eza`, `ghostty`, `zellij`, `uv`, `mise`, `direnv`, `just`, `task`,
`starship`, `duf`, `btop`, `ncdu`, `trippy`, `ecapture`, `helmfile`, `timoni`,
`copa`, `k9s`, `kubecolor`, `zizmor`, `toolong`, `ptcpdump`, `superfile`,
`rainfrog`, `posting`, `lazyssh`, `omnyssh`, `serpl`, `whosthere`, `khi`,
`sonar`, `dbx`, `RackPeek`, `kula`, `dcg`, `lfk`, `tuicr`,
`revdiff`, `hunk`, `wt`, `changie`, `typos`, `act`, `jj`, `jjui`, `gitui`,
`onefetch`, `gitlabform`, `glci`, `prek`, `reposcan`, `reviewdog`.

Часть кандидатов уже осознанно отклонена и описана в других трекерах:
`topgrade`, `deb-get`, `agg`, `atuin`, `vhs` и другие — см.
[`not-install.md`](not-install.md), [`TODO-abandoned.md`](TODO-abandoned.md),
[`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md) и
[`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md).

---

## Что сделано

Изменения только в репозитории; применять их к системе должен человек или
GitOps-пайплайн после обычного прогона плейбука.

1. **ruff** — `roles/base/defaults/main.yml`, `base_pipx_apps`:
   `- name: ruff`, `creates: ruff`. Проверка: `ruff --version`.
2. **d2** — `roles/iac/defaults/main.yml`, бинарники: `repo: d2lang/d2`,
   URL `https://github.com/d2lang/d2/releases/download/{tag}/d2-v{version}-linux-amd64.tar.gz`,
   `archive: tar`, `member: d2-v{version}/bin/d2`. Проверка: `d2 --version`.
3. **pinact** — `roles/git/defaults/main.yml`, бинарники:
   `repo: suzuki-shunsuke/pinact`, ассет без версии в имени —
   `pinact_linux_amd64.tar.gz`, `archive: tar`, `member: pinact`.
   Проверка: `pinact --version`.
4. **inshellisense** — `roles/shell/defaults/main.yml`
   (`inshellisense_install: true`) и `roles/shell/tasks/inshellisense.yml`:
   npm-пакет `@microsoft/inshellisense` глобально в `bin_dir`, как `tldr`.
   Проверка: `inshellisense --version`.
5. **tfautomv** — `roles/iac/defaults/main.yml`, бинарники:
   `busser/tfautomv`, `tfautomv_{version}_linux_amd64.tar.gz`.
   Проверка: `tfautomv --version`.
6. **cdebug** — `roles/kubernetes/defaults/main.yml`, бинарники:
   `iximiuz/cdebug`, `cdebug_linux_amd64.tar.gz`. Проверка:
   `cdebug --version` (подкоманды `version` у него нет).
7. **kubectl-explore** — `roles/kubernetes/defaults/main.yml`, бинарник
   `kubectl-explore_v{version}_linux_amd64.tar.gz`. Флага `--version` нет,
   проверка в `post_tasks` — `kubectl-explore --help`.

`binsider`, `distrobox` и `localsend` в плейбук не добавлены — отклонены по
запросу. `README.md` (каталог приложений) и `TODO.md` обновлены, проверки
версий добавлены в `post_tasks`. Прогон
`ansible-playbook --syntax-check playbook.yml`, `ansible-lint` и
`pre-commit run --all-files` — после изменений.
