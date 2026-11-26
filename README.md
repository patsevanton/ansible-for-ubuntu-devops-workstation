# ansible-for-ubuntu-devops-workstation

TODO: https://ai-dev.live/recaps/all/faqn4b1h533e04ec0rdg/

Ansible-плейбук, который превращает чистую Ubuntu-ноутбук в рабочее DevOps-окружение:
пакеты, Docker, клиенты Kubernetes, инструменты IaC, секреты и удобный shell.

- Целевая ОС: **Ubuntu 26.04 (resolute)**, архитектура **x86_64**.
- **Версии не фиксируются** — ставится актуальное на момент запуска.
  Исключение: `terraform`/`terragrunt` плейбук вообще не ставит — они управляются
  через `tfenv`/`tgenv`, версии выбираете сами (см. ниже).
- Стандартная структура Ansible-проекта: `ansible.cfg`, `inventory/`, `group_vars/`, `roles/`.
- Запуск на самом ноутбуке (`localhost`, локальное подключение).
- Системные шаги выполняются через `sudo`, пароль вводит пользователь (`-K`).

---

## Требования

- Ubuntu 26.04 (resolute), x86_64.
- Права `sudo` и доступ в интернет.
- `ansible-core` и `python3-apt` — ставятся один раз вручную (см. ниже):
  плейбук не может поставить Ansible самому себе до первого запуска.

---

## Быстрый старт

```bash
# 1. Bootstrap: один раз вручную
sudo apt update
sudo apt install -y ansible-core python3-apt

# 2. Запуск плейбука (пароль sudo спросит сам)
cd ansible-for-ubuntu-devops-workstation
ansible-playbook -K playbook.yml
```

`-K` — это `--ask-become-pass`. Запускать нужно **от обычного пользователя**,
не через `sudo` (иначе домашние установки — tfenv/tgenv и `~/.config` — уйдут в `/root`).

После установки:

```bash
# применить новое окружение и группу docker
exec newgrp docker      # или просто перелогиниться
source ~/.config/devops-shell.sh
```

`docker` без `sudo` заработает после повторного входа: членство в группе
перечитывается при логине.

Полезные режимы запуска:

```bash
ansible-playbook --syntax-check playbook.yml   # проверка синтаксиса
ansible-playbook -K playbook.yml --check       # dry-run (с оговорками, см. ниже)
ansible-playbook -K playbook.yml --tags shell  # только роль shell (base — всегда)
ansible-playbook -K playbook.yml -e app_update=true  # обновить бинарники
ansible-lint                                   # проверка стиля (profile: production)
pre-commit run --all-files                     # те же проверки перед коммитом
```

`--check` честно показывает только то, что умеют проверять модули: `apt`,
`file`, `get_url`, `unarchive` и `stat`. Задачи `command`/`shell` в check mode
по умолчанию не выполняются, поэтому установка бинарников, pipx-окружений и
`docker` в dry-run не проверяется — они попадут в отчёт как отсутствующие.
Проверка версий и наличия файлов в `post_tasks` помечена `check_mode: false`,
поэтому `--check` всё равно печатает, что реально установлено, а отсутствие
бинарников на чистой машине не считается ошибкой. Файл `report.json` в check
mode не пишется: `copy` в dry-run ничего не меняет.

---

## Каталог приложений

Что ставит плейбук: ссылка на проект и краткое описание. Разделы — по ролям;
версии не фиксируются, ставится актуальное на момент запуска.

Для AI-агентов тот же список собирается в отдельный каталог:
`~/.config/opencode/docs/tools.md` (индекс по задачам) и
`~/.local/state/devops-playbook/toolbox.json` (машиночитаемый список).
Домены и исключения задаются в `vars/toolbox.yml`, генератор —
`scripts/toolbox.py`. Роль задаёт домен по умолчанию: инструмент,
добавленный в роль `shell`, попадёт в `search-files`, поэтому для поиска,
логов, баз данных и сборки нужен явный оверрайд в `toolbox_overrides`.

### base

- [rsync](https://rsync.samba.org/) — инкрементальное копирование локально и по SSH, `--dry-run` перед изменениями.
- [sqlite3](https://sqlite.org/cli.html) — консольный клиент SQLite: `.schema`, `.dump`, `VACUUM`, SQL по локальным базам.
- [earlyoom](https://github.com/rfjakob/earlyoom) — убивает самый жадный процесс при исчерпании памяти, пока система ещё отвечает.
- [smem](https://selenic.com/repo/smem) — память по процессам с PSS/USS, а не RSS: реальный вклад программы с учётом разделяемых библиотек.
- [needrestart](https://github.com/liske/needrestart) — после apt-обновлений показывает сервисы на старых библиотеках и необходимость ребута.
- [lsof](https://github.com/lsof-org/lsof) — кто держит файл, каталог или сокет: `lsof -i :8080`, `lsof +D /path`.
- [strace](https://strace.io/) — системные вызовы процесса: на чём висит, какой файл не открылся, откуда `permission denied`.
- [etckeeper](https://etckeeper.branchable.com/) — `/etc` под git: apt-хук и таймер коммитят правки, `git -C /etc diff HEAD` и откат одного файла.
- [sos](https://github.com/sosreport/sos) — сбор диагностики системы в один архив (`sudo sos report`) для тикета или вендора.
- [yq](https://github.com/mikefarah/yq) — YAML/JSON/XML-процессор с jq-подобным синтаксисом.
- [eget](https://github.com/zyedidia/eget) — установка готовых бинарников прямо из GitHub-релизов одной командой.
- [dra](https://github.com/devmatteini/dra) — скачивание отдельных ассетов GitHub-релиза по имени репозитория.
- [binup](https://github.com/KonishchevDmitry/binup) — установка и обновление приложений из GitHub-релизов по декларативному манифесту.
- [molecule](https://github.com/ansible/molecule) — тестирование Ansible-ролей в контейнерах (вместе с драйвером `molecule-plugins`).
- [ansible-navigator](https://github.com/ansible/ansible-navigator) — TUI-запуск плейбуков в execution environments.
- [ansible-builder](https://github.com/ansible/ansible-builder) — сборка образов execution environments.
- [ansible-creator](https://github.com/ansible/ansible-creator) — генерация каркаса коллекций и ролей.
- [ansible-doctor](https://github.com/ansible/ansible-doctor) — документация ролей по комментариям.
- [ara](https://github.com/ansible-community/ara) — запись и просмотр прогонов Ansible.
- [ruff](https://github.com/astral-sh/ruff) — линтер и форматтер Python на Rust: `ruff check` вместо flake8/isort/pylint, `ruff format` вместо black.
- [basedpyright](https://github.com/DetachHead/basedpyright) — проверка типов Python: строже и быстрее mypy, читает `pyproject.toml` и `pyrightconfig.json`.
- [ansible-lint](https://github.com/ansible/ansible-lint) — проверка стиля плейбуков (профиль `production`).
- [pipx](https://github.com/pypa/pipx) — изолированные окружения для Python-приложений.
- [curl](https://github.com/curl/curl) — передача данных по URL.
- [wget](https://savannah.gnu.org/projects/wget) — скачивание файлов из CLI.
- [git](https://github.com/git/git) — система контроля версий.
- [git-lfs](https://git-lfs.com/) — Large File Storage: большие ассеты в репозитории вместо pointer-заглушек.
- [git-sizer](https://github.com/github/git-sizer) — отчёт о размере репозитория: самые тяжёлые коммиты, блобы и деревья.
- [jq](https://github.com/jqlang/jq) — обработка JSON из CLI.
- [ca-certificates](https://salsa.debian.org/debian/ca-certificates) — корневые сертификаты.
- [unzip](https://infozip.sourceforge.net/UnZip.html) — распаковка zip-архивов.
- [zip](https://infozip.sourceforge.net/Zip.html) — создание zip-архивов.
- [tar](https://savannah.gnu.org/projects/tar) — архивы tar.
- [gzip](https://savannah.gnu.org/projects/gzip) — сжатие gzip.
- [pigz](https://github.com/madler/pigz) — параллельный gzip: многопоточное сжатие, формат совместим с gzip.
- [xz-utils](https://github.com/tukaani-project/xz) — сжатие xz.
- [zstd](https://github.com/facebook/zstd) — сжатие Zstandard: `zstd -19`, `tar -I zstd`, распаковка `.tar.zst`.
- [7zip](https://www.7-zip.org/) — архивы `.7z`, `.rar`, `.iso`, `.cab`, которые не читают unzip и tar.
- [bash-completion](https://github.com/scop/bash-completion) — автодополнение в bash.
- [lsb-release](https://github.com/LinuxStandardBase/lsb) — определение версии дистрибутива.

### git

- [gh](https://github.com/cli/cli) — GitHub CLI: пул-реквесты, issues, релизы, Actions.
- [glab](https://gitlab.com/gitlab-org/cli) — GitLab CLI: MR, issues, пайплайны, релизы.
- [gitlabcloner](https://github.com/Andrey039/gitlabcloner) — клонирование групп и подгрупп GitLab одной командой.
- [glci](https://gitlab.com/gitlab-org/ci-cd/runner-tools/glci) — локальный запуск пайплайнов GitLab CI.
- [pre-commit](https://github.com/pre-commit/pre-commit) — git-хуки из `.pre-commit-config.yaml`.
- [prek](https://github.com/j178/prek) — Rust-замена pre-commit: тот же конфиг, параллельный запуск хуков и без Python-окружения на каждый прогон.
- [reposcan](https://github.com/mabd-dev/reposcan) — поиск git-репозиториев с незакоммиченными или незапушенными изменениями.
- [lazygit](https://github.com/jesseduffield/lazygit) — TUI для git: статус, коммиты, ветки, rebase.
- [git-absorb](https://github.com/tummychow/git-absorb) — раскладывает незакоммиченные правки по старым коммитам как `fixup!` для `git rebase --autosquash`.
- [reviewdog](https://github.com/reviewdog/reviewdog) — замечания любых линтеров в PR/MR как inline-комментарии.
- [tuicr](https://github.com/agavra/tuicr) — ревью кода в терминале с vim-клавишами: diff, комментарии к строкам и отправка ревью в GitHub/GitLab/Bitbucket/Azure DevOps/Gerrit; понимает git, jj и hg.
- [revdiff](https://github.com/umputun/revdiff) — ревью диффа в терминале: аннотации к строкам и вывод разметки в stdout для агента или скрипта.
- [hunk](https://github.com/modem-dev/hunk) — ревью диффа после агента: поток файлов с боковой навигацией, inline-аннотации, split/unified и watch-режим.
- [wt (worktrunk)](https://github.com/max-sixty/worktrunk) — CLI для git worktree: параллельные ветки в отдельных каталогах.
- [changie](https://github.com/miniscruff/changie) — фрагменты changelog и сборка релизной секции.
- [ghgrab](https://github.com/abhixdd/ghgrab) — TUI-браузер файлов репозиториев GitHub/GitLab/Gitea.
- [gh-dash](https://github.com/dlvhdr/gh-dash) — TUI для pull request'ов и issues GitHub: секции на разные репозитории, diff, комментарии и merge.
- [glaball](https://github.com/flant/glaball) — массовые команды на нескольких self-hosted GitLab-инстансах.
- [lumen](https://github.com/jnsahaj/lumen) — просмотр диффа и генерация сообщения коммита через LLM.
- [gptcommit](https://github.com/zurawiki/gptcommit) — git-хук `prepare-commit-msg` с сообщением от LLM.
- [codegpt](https://github.com/appleboy/CodeGPT) — сообщения коммитов и ревью через LLM из CLI.
- [typos](https://github.com/crate-ci/typos) — поиск опечаток в коде и документации с автоисправлением.
- [act](https://github.com/nektos/act) — локальный запуск GitHub Actions в Docker.
- [jj (jujutsu)](https://github.com/jj-vcs/jj) — VCS поверх обычного git-репозитория.
- [jjui](https://github.com/idursun/jjui) — TUI для Jujutsu в духе lazygit: история, ветки, diff, операции.
- [gitui](https://github.com/extrawurst/gitui) — быстрый TUI для git на Rust.
- [onefetch](https://github.com/o2sh/onefetch) — сводка по репозиторию в терминале: языки, строки кода, лицензия, авторы, последний коммит.
- [git-fame](https://github.com/casperdcl/git-fame) — вклад авторов по выжившим строкам (`git blame`), а не по числу коммитов.
- [gita](https://github.com/nosarthur/gita) — статус и групповые операции по десяткам локальных git-репозиториев.
- [git-filter-repo](https://github.com/newren/git-filter-repo) — переписывание истории: удаление файлов и утёкших секретов из всех коммитов, большие блобы, разделение репозитория.
- [gitlabform](https://github.com/gitlabform/gitlabform) — GitLab как код: группы, проекты и настройки из YAML.
- [zizmor](https://github.com/zizmorcore/zizmor) — статический анализ workflow GitHub Actions: опасные выражения, права, pinning экшенов.
- [actionlint](https://github.com/rhysd/actionlint) — проверка workflow GitHub Actions: синтаксис и типы выражений, shellcheck для `run:`, входы/выходы экшенов и матрицы.
- [pinact](https://github.com/suzuki-shunsuke/pinact) — пиннинг GitHub Actions и reusable workflows по SHA, обновление пинов и проверка аннотаций версий.
- [lychee](https://github.com/lycheeverse/lychee) — проверка ссылок в Markdown и HTML: параллельные запросы, кэш, повтор при таймауте и исключения по шаблонам.

### atlassian

- [jira-cli](https://github.com/ankitpokhrel/jira-cli) — Jira CLI: задачи по фильтрам и JQL, просмотр тикета, комментарии и переходы; Cloud (API-токен) и on-prem Server/DC (PAT).
- [jiratui](https://github.com/whyisdifficult/jiratui) — TUI для Jira: задачи проекта, фильтры, карточка тикета, комментарии и переходы по статусам.
- [mcp-atlassian](https://github.com/sooperset/mcp-atlassian) — MCP-сервер Jira и Confluence для AI-клиентов: поиск по JQL/CQL, задачи, страницы и комментарии; Cloud и on-prem Server/DC (PAT).

### docker

- [Docker Engine](https://github.com/moby/moby) — движок контейнеров из официального репозитория Docker.
- [Compose V2](https://github.com/docker/compose) — плагин `docker compose`.
- [Buildx](https://github.com/docker/buildx) — плагин `docker buildx`: multi-arch сборки, кеш BuildKit, секреты и SBOM.
- [dive](https://github.com/wagoodman/dive) — анализ слоёв образа: размер, мусор, эффективность.
- [lazydocker](https://github.com/jesseduffield/lazydocker) — TUI-менеджер контейнеров, образов и томов.
- [ctop](https://github.com/bcicen/ctop) — `top` по метрикам контейнеров (CPU, память, сеть).
- [oras](https://github.com/oras-project/oras) — клиент OCI-реестров для произвольных артефактов.
- [skopeo](https://github.com/containers/skopeo) — inspect/copy/sync образов между реестрами без Docker-демона и root.
- [regctl](https://github.com/regclient/regclient) — работа с реестром без демона: теги с фильтрами, манифесты и digest, referrers, blob get/put.
- [crane](https://github.com/google/go-containerregistry) — работа с образами и реестрами без демона: copy, export/import в tar, digest, манифест, слои и сборка образа.
- [dry](https://github.com/moncho/dry) — терминальный менеджер Docker с несколькими хостами.
- [decompose](https://github.com/s0rg/decompose) — карта образов, сетей, томов и зависимостей docker-окружения.
- [copa (copacetic)](https://github.com/project-copacetic/copacetic) — патчинг CVE прямо в образе по отчёту grype/trivy.
- [hadolint](https://github.com/hadolint/hadolint) — линтер Dockerfile.
- [droast](https://github.com/immanuwell/dockerfile-roast) — линтер Dockerfile с правилами DF: heredoc, BuildKit `--mount`, автофиксы и SARIF.
- [dockle](https://github.com/goodwithtech/dockle) — проверка собранного образа по CIS Docker Benchmark: root по умолчанию, setuid, лишние пакеты, секреты в ENV и истории, healthcheck и USER.
- [mint (DockerSlim/SlimToolkit)](https://github.com/mintoolkit/mint) — уменьшение уже собранного образа по профилю реально используемых файлов; требует Docker.
- [docker-image-layer-explorer](https://github.com/Kartik1397/docker-image-layer-explorer) — список слоёв образа и распаковка выбранного слоя.
- [containerd](https://github.com/containerd/containerd) — контейнерный рантайм под Docker Engine.

### kubernetes

- [kubectl](https://github.com/kubernetes/kubectl) — официальный CLI Kubernetes.
- [helm](https://github.com/helm/helm) — пакетный менеджер Kubernetes (чарты).
- [istioctl](https://github.com/istio/istio) — CLI Istio: `analyze`, `proxy-status`, `proxy-config` (xDS и кластеры Envoy), `bug-report`.
- [cilium](https://github.com/cilium/cilium-cli) — CLI Cilium: статус CNI и агентов, connectivity test, endpoints и политики, карты BPF, `sysdump` для диагностики.
- [helmwave](https://github.com/helmwave/helmwave) — helm3-native деплой чартов: план, дифф и применение.
- [k9s](https://github.com/derailed/k9s) — TUI-консоль кластера: ресурсы, логи, exec.
- [sofka](https://github.com/nklmilojevic/sofka) — Kubernetes TUI на Rust: CRD, Flux CD и Argo CD, разбор причин сбоя и read-only режим.
- [kustomize](https://github.com/kubernetes-sigs/kustomize) — сборка манифестов из `kustomization.yaml`.
- [flux](https://github.com/fluxcd/flux2) — CLI Flux CD: bootstrap, reconcile, GitOps.
- [flux9s](https://github.com/dgunzy/flux9s) — TUI для Flux-ресурсов.
- [stern](https://github.com/stern/stern) — логи нескольких подов с фильтрами по регэкспу.
- [khi](https://github.com/GoogleCloudPlatform/khi) — таймлайн событий и логов кластера для разбора инцидента.
- [flate](https://github.com/home-operations/flate) — офлайн-рендер Flux GitOps-репозитория без кластера.
- [flux-tools](https://github.com/alexandervidyaev/flux-tools) — независимая реализация офлайн-рендера и диффа Flux.
- [kubectx](https://github.com/ahmetb/kubectx) — быстрое переключение контекстов и namespace.
- [cty (crd-to-sample-yaml)](https://github.com/Skarlso/crd-to-sample-yaml) — sample-YAML из CRD и валидация схем.
- [diffyml](https://github.com/szhekpisov/diffyml) — структурный дифф YAML с учётом семантики Kubernetes.
- [kubectl-k8i](https://github.com/ViktorUJ/kubectl-k8i) — ресурсы нод с цветовой индикацией загрузки.
- [kubectl-klens](https://github.com/PixiBixi/kubectl-klens) — read-only инспекция кластера одним плагином: capacity, taints, zones, images, requests/limits и ещё 30+ команд.
- [kubespy](https://github.com/pulumi/kubespy) — наблюдение за изменениями ресурсов в реальном времени.
- [kubecolor](https://github.com/kubecolor/kubecolor) — цветной, читаемый вывод kubectl.
- [kube-capacity](https://github.com/robscott/kube-capacity) — requests/limits и потребление по нодам и подам.
- [kubectl-view-allocations](https://github.com/davidB/kubectl-view-allocations) — распределение CPU, памяти и GPU по нодам, namespace и владельцам.
- [kubectl-cost](https://github.com/kubecost/kubectl-cost) — стоимость неймспейсов, workload'ов и подов по данным OpenCost/Prometheus (`kubectl cost`).
- [kubestr](https://github.com/kastenhq/kubestr) — проверка хранилища кластера: StorageClass, CSI и реальные IOPS.
- [ktop](https://github.com/vladimirvivien/ktop) — top-подобный TUI-монитор метрик нод и подов.
- [kubefetch](https://github.com/jkulzer/kubefetch) — сводка о кластере в стиле neofetch.
- [KubeDiagrams](https://github.com/philippemerle/KubeDiagrams) — схемы архитектуры Kubernetes из манифестов, kustomize, Helm и состояния кластера.
- [krew](https://github.com/kubernetes-sigs/krew) — менеджер kubectl-плагинов.
- [view-secret](https://github.com/elsesiy/kubectl-view-secret) — декодирование секретов из CLI.
- [df-pv](https://github.com/yashbhutwala/kubectl-df-pv) — `df` по PersistentVolume.
- [browse-pvc](https://github.com/clbx/kubectl-browse-pvc) — просмотр содержимого PVC.
- [pluto](https://github.com/FairwindsOps/pluto) — устаревшие и удалённые apiVersion в манифестах и релизах.
- [pv-migrate](https://github.com/utkuozdemir/pv-migrate) — миграция и backup/restore PersistentVolume.
- [marvin](https://github.com/undistro/marvin) — сканер кластера CEL-выражениями.
- [kftui](https://github.com/hcavarsan/kftray) — TUI-менеджер kubectl port-forward и reverse-туннелей.
- [ct (chart-testing)](https://github.com/helm/chart-testing) — линтинг и тестирование Helm-чартов.
- [ytt](https://github.com/carvel-dev/ytt) — шаблонизатор YAML по структуре документа, а не по тексту.
- [kbld](https://github.com/carvel-dev/kbld) — фиксация образов по digest в манифестах.
- [imgpkg](https://github.com/carvel-dev/imgpkg) — наборы файлов как OCI-образы: `imgpkg push/pull` без docker.
- [chartsnap](https://github.com/jlandowner/helm-chartsnap) — snapshot-тесты Helm-чартов.
- [helm-docs](https://github.com/norwoodj/helm-docs) — генерация README Helm-чарта из `Chart.yaml` и `values.yaml`.
- [helm-schema](https://github.com/dadav/helm-schema) — `values.schema.json` из `values.yaml` и аннотаций `# @schema` для валидации values.
- [helm-tui](https://github.com/vasyakrg/helm-tui) — TUI над helm-репозиториями: доступность и латентность, поиск чартов по кэшу индексов, diff двух версий чарта.
- [kubewall](https://github.com/kubewall/kubewall) — веб-дашборд на несколько кластеров одним бинарником.
- [kubevpn](https://github.com/kubenetworks/kubevpn) — VPN в кластер: поды видны как соседи в локальной сети.
- [netfetch](https://github.com/deggja/netfetch) — поиск ворклоадов, не покрытых NetworkPolicy.
- [timoni](https://github.com/stefanprodan/timoni) — пакетный менеджер Kubernetes на CUE.
- [kubeview](https://github.com/benc-uk/kubeview) — граф ресурсов кластера и связей между ними в браузере.
- [kubehound](https://github.com/DataDog/KubeHound) — построение путей атак в кластере.
- [charts-syncer](https://github.com/bitnami/charts-syncer) — синхронизация Helm-репозиториев, в том числе OCI.
- [netobserv](https://github.com/netobserv/netobserv-cli) — сетевая наблюдаемость на eBPF без агента в кластере.
- [capacitor](https://github.com/gimlet-io/capacitor) — UI для FluxCD.
- [kubeconform](https://github.com/yannh/kubeconform) — валидация манифестов по схемам без кластера.
- [kube-linter](https://github.com/stackrox/kube-linter) — антипаттерны в манифестах: probes, limits, securityContext.
- [helmfile](https://github.com/helmfile/helmfile) — декларативное описание набора Helm-релизов.
- [kind](https://github.com/kubernetes-sigs/kind) — локальный кластер Kubernetes в Docker.
- [kops](https://github.com/kubernetes/kops) — жизненный цикл production-кластеров.
- [devpod](https://github.com/loft-sh/devpod) — dev-окружения по `devcontainer.json`.
- [kompose](https://github.com/kubernetes/kompose) — конвертация `docker-compose.yml` в манифесты Kubernetes.
- [ko](https://github.com/google/ko) — сборка Go-образов и деплой без Docker.
- [kubie](https://github.com/kubie-org/kubie) — изолированные kubeconfig по shell и каталогу.
- [kubefwd](https://github.com/txn2/kubefwd) — массовый port-forward с записями в `/etc/hosts`.
- [kubectl-tree](https://github.com/ahmetb/kubectl-tree) — дерево объектов по `ownerReferences`.
- [conftest](https://github.com/open-policy-agent/conftest) — политики Rego/OPA для конфигов.
- [kube-bench](https://github.com/aquasecurity/kube-bench) — проверка кластера по CIS Kubernetes Benchmark.
- [kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server) — MCP-сервер Kubernetes/OpenShift для AI-агентов.
- [kubecm](https://github.com/sunny0826/kubecm) — управление kubeconfig: слияние, переименование, переключение.
- [cmctl](https://github.com/cert-manager/cmctl) — CLI cert-manager: статус и продление сертификатов, инспекция Secret.
- [sonobuoy](https://github.com/vmware-tanzu/sonobuoy) — conformance/e2e-тесты Kubernetes и плагины диагностики в кластере.
- [cdebug](https://github.com/iximiuz/cdebug) — отладочный контейнер в поде с нужным набором инструментов, `exec`, копированием файлов и пробросом портов.
- [kubectl-explore](https://github.com/keisku/kubectl-explore) — fuzzy-поиск по `kubectl explain`: поле по имени, без точного пути.
- [kubectl-slice](https://github.com/patrickdappollonio/kubectl-slice) — разбиение multi-document YAML на отдельные файлы.
- [kubectl-fields](https://github.com/rewanthtammana/kubectl-fields) — иерархия полей ресурса.
- [kubectl-images](https://github.com/chenjiandongx/kubectl-images) — образы, используемые в кластере, с группировкой по подам.
- [kubectl-graph](https://github.com/steveteuber/kubectl-graph) — граф связей ресурсов живого кластера в DOT, CQL или AQL.
- [helmify](https://github.com/arttor/helmify) — генерация Helm-чарта из манифестов.
- [kail](https://github.com/boz/kail) — `tail -f` по логам подов с фильтрами по селектору.
- [kubeaudit](https://github.com/Shopify/kubeaudit) — аудит security-мисконфигов в кластере.
- [rbac-tool](https://github.com/alcideio/rbac-tool) — анализ RBAC: lookup, who-can, визуализация.
- [kluctl](https://github.com/kluctl/kluctl) — декларативный GitOps-деплой в Kubernetes.
- [kube-burner](https://github.com/kube-burner/kube-burner) — нагрузочные тесты кластера.
- [kwok](https://github.com/kubernetes-sigs/kwok) — симуляция тысяч нод без kubelet.
- [kwokctl](https://github.com/kubernetes-sigs/kwok) — управление кластерами kwok.
- [kpexec](https://github.com/ssup2/kpexec) — запуск команды в контейнере с привилегиями хоста.
- [groot](https://github.com/hrodrig/groot) — диагностический архив кластера для RCA.
- [k2tf](https://github.com/sl1pm4t/k2tf) — конвертация Kubernetes YAML в Terraform HCL.
- [kubesec](https://github.com/controlplaneio/kubesec) — статический риск-анализ манифестов.
- [kpt](https://github.com/kptdev/kpt) — управление пакетами Kubernetes-конфигов.
- [kube-job](https://github.com/h3poteto/kube-job) — запуск одноразовых Job из CLI.
- [kubectl-sniff](https://github.com/eldadru/ksniff) — сниффинг трафика пода через tcpdump.
- [static-tcpdump](https://github.com/eldadru/ksniff) — статический tcpdump для контейнеров без него.
- [kdash](https://github.com/kdash-rs/kdash) — быстрый TUI-дашборд кластера на Rust.
- [kubetail](https://github.com/kubetail-org/kubetail) — дашборд логов нескольких подов и контейнеров.
- [kubepug](https://github.com/kubepug/kubepug) — поиск устаревших API перед апгрейдом.
- [kube-prompt](https://github.com/c-bata/kube-prompt) — интерактивный kubectl с автодополнением.
- [rbac-lookup](https://github.com/FairwindsOps/rbac-lookup) — обратный поиск RBAC: кто связан с ролью.
- [kubectl-who-can](https://github.com/aquasecurity/kubectl-who-can) — кто может выполнить verb над ресурсом.
- [korb](https://github.com/BeryJu/korb) — перенос PVC между StorageClass и namespace.
- [kl](https://github.com/robinovitch61/kl) — TUI для логов нескольких контейнеров и кластеров.
- [kubectl-doctor](https://github.com/emirozer/kubectl-doctor) — триаж кластера в духе `brew doctor`.
- [kbom](https://github.com/rad-security/kbom) — инвентарь и SBOM кластера.
- [kubectl-modify-secret](https://github.com/rajatjindal/kubectl-modify-secret) — правка секрета без ручного base64.
- [silver-surfer](https://github.com/devtron-labs/silver-surfer) — совместимость манифестов с apiVersion кластера.
- [kubeprompt](https://github.com/jlesquembre/kubeprompt) — контекст и namespace в prompt.
- [kustomizer](https://github.com/stefanprodan/kustomizer) — пакеты конфигов как OCI-артефакты.
- [buoy](https://github.com/everettraven/buoy) — декларативный TUI-дашборд Kubernetes.
- [k9sight](https://github.com/doganarif/k9sight) — TUI для отладки workload'ов.
- [hanoi-cli](https://github.com/k-krew/hanoi-cli) — советник по ребалансировке подов.
- [kzero](https://github.com/hrodrig/kzero) — декларативные down/up/reset кластера по YAML.
- [kubectl-kzero](https://github.com/hrodrig/kzero) — kubectl-плагин к kzero.
- [ktunnel](https://github.com/omrikiei/ktunnel) — туннель в кластер без SSH.
- [kubectl-duplicate](https://github.com/Telemaco019/duplik8s) — дублирование ресурсов между namespace.
- [kubectl-fd](https://github.com/alikhil/kubectl-find) — поиск ресурсов в духе UNIX `find`.
- [kubectl-relay](https://github.com/knight42/krelay) — замена `kubectl port-forward`.
- [gwctl](https://github.com/kubernetes-sigs/gwctl) — CLI для Gateway API.
- [kbu](https://github.com/vulcanshen/kbu) — однопанельный TUI Kubernetes.
- [kurt](https://github.com/soraro/kurt) — перезапуски подов и поиск проблемных workload'ов.
- [kubediff](https://github.com/Ramilito/kubediff) — дифф исходников и задеплоенного состояния.
- [kubetrim](https://github.com/alexellis/kubetrim) — чистка недоступных контекстов в kubeconfig.
- [kubevious](https://github.com/kubevious/cli) — проверка Kubernetes-конфигов.
- [k8shark](https://github.com/phenixblue/k8shark) — снимок состояния кластера и replay.
- [node-gizmo](https://github.com/Kavinraja-G/node-gizmo) — CLI по нодам кластера.
- [burn](https://github.com/tanrikuluozlem/burn) — стоимость Kubernetes по namespace.
- [tk (Grafana Tanka)](https://github.com/grafana/tanka) — Jsonnet-конфигурация Kubernetes.
- [audit2rbac](https://github.com/liggitt/audit2rbac) — генерация RBAC из audit-логов.
- [kopilot](https://github.com/knight42/kopilot) — AI-ассистент для диагностики кластера.
- [kubectl-outagedeck](https://github.com/outagedeck/kubectl-outagedeck) — статус облачных провайдеров.
- [keploy](https://github.com/keploy/keploy) — тест-кейсы из реального трафика приложения.
- [okteto](https://github.com/okteto/okteto) — разработка прямо в кластере.
- [ig (Inspektor Gadget)](https://github.com/inspektor-gadget/inspektor-gadget) — eBPF-гаджеты для отладки контейнеров.
- [peirates](https://github.com/inguardians/peirates) — пентест изнутри кластера.
- [helmsman](https://github.com/mkubaczyk/helmsman) — Helm-релизы как код в TOML.
- [kexp](https://github.com/iximiuz/kexp) — визуальное понимание Kubernetes в локальном web-UI.
- [gefyra](https://github.com/gefyrahq/gefyra) — локальная разработка с подменой сервисов в кластере.
- [reckoner](https://github.com/FairwindsOps/reckoner) — Helm-релизы из YAML.
- [copper](https://github.com/cloud66-oss/copper) — валидатор конфигов по правилам и схемам.
- [alterant](https://github.com/cloud66-oss/alterant) — предсказуемые точечные правки YAML/JSON.
- [crashd](https://github.com/vmware-tanzu/crash-diagnostics) — сбор диагностики с недоступных хостов и кластеров.
- [kubescout](https://github.com/ReallyLiri/kubescout) — тревожные состояния по всем кластерам из kubeconfig.
- [k8s-insider](https://github.com/TrueGoric/k8s-insider) — доступ к сети кластера без настройки.
- [patchloom](https://github.com/patchloom/patchloom) — структурная правка конфигов для AI-агентов.
- [k8sgpt](https://github.com/k8sgpt-ai/k8sgpt) — объяснение проблем кластера через LLM.
- [kubescape](https://github.com/kubescape/kubescape) — проверка по профилям NSA/CIS.
- [popeye](https://github.com/derailed/popeye) — мёртвые и неиспользуемые ресурсы кластера.
- [vcluster](https://github.com/loft-sh/vcluster) — виртуальные Kubernetes-кластеры внутри namespace.
- [skaffold](https://github.com/GoogleContainerTools/skaffold) — цикл «сборка → деплой → проверка» с hot-reload.
- [kubeshark](https://github.com/kubeshark/kubeshark) — разбор L7-трафика подов через eBPF.
- [kubectl-ai](https://github.com/GoogleCloudPlatform/kubectl-ai) — AI-ассистент: генерирует команды и манифесты.
- [k3d](https://github.com/k3d-io/k3d) — k3s в Docker: локальные кластеры из контейнеров.
- [telepresence](https://github.com/telepresenceio/telepresence) — локальный сервис «как будто в кластере».
- [tilt](https://github.com/tilt-dev/tilt) — live-update приложений с веб-UI.
- [mirrord](https://github.com/metalbear-co/mirrord) — локальный процесс в сети, ФС и окружении пода.
- [devspace](https://github.com/devspace-sh/devspace) — синхронизация файлов и hot-reload по `devspace.yaml`.
- [kubent](https://github.com/doitintl/kube-no-trouble) — что сломается при апгрейде кластера.
- [polaris](https://github.com/FairwindsOps/polaris) — best practices и securityContext для манифестов.
- [kube-score](https://github.com/zegl/kube-score) — чек-лист probes/requests/limits по манифестам.
- [kubectl-neat](https://github.com/itaysk/kubectl-neat) — чистый YAML без `managedFields`.
- [kubectl-validate](https://github.com/kubernetes-sigs/kubectl-validate) — офлайн-валидация схемами Kubernetes.
- [nova](https://github.com/FairwindsOps/nova) — устаревшие версии Helm-чартов в кластере.
- [kube-hunter](https://github.com/aquasecurity/kube-hunter) — поиск уязвимостей кластера.
- [knetvis](https://pypi.org/project/knetvis/) — визуализация и тестирование NetworkPolicy.
- [netcheck](https://pypi.org/project/netcheck/) — проверки DNS/TCP/HTTP/Postgres с CEL-правилами.
- [kptop](https://pypi.org/project/kptop/) — TUI-мониторинг нод, подов и PVC через Prometheus.
- [helm-diff](https://github.com/databus23/helm-diff) — плагин `helm diff`: что изменится до применения чарта.
- [helm-secrets](https://github.com/jkroepke/helm-secrets) — плагин: шифрование values через sops.
- [helm-unittest](https://github.com/helm-unittest/helm-unittest) — плагин `helm unittest`: unit-тесты чартов на YAML, рендер локально, без кластера.
- [helm-mapkubeapis](https://github.com/helm/helm-mapkubeapis) — плагин `helm mapkubeapis`: заменяет устаревшие и удалённые `apiVersion` прямо в релизе, без переустановки чарта.
- [kubectl-ports](https://github.com/widnyana/kubectl-ports-rs) — таблица портов подов и сервисов.
- [kubebox](https://github.com/astefanutti/kubebox) — терминальная и веб-консоль Kubernetes.
- [cdk8s](https://github.com/cdk8s-team/cdk8s-cli) — манифесты кодом на TypeScript/Python.
- [kosko](https://github.com/tommy351/kosko) — манифесты на TypeScript.
- [headlamp](https://github.com/kubernetes-sigs/headlamp) — web/desktop UI Kubernetes.
- [radar](https://github.com/skyhook-io/radar) — desktop UI со встроенным MCP-сервером для AI-агентов.
- [monokle](https://github.com/kubeshop/monokle) — desktop-редактор и анализатор манифестов.
- [rubick](https://github.com/Dudude-bit/rubick) — лёгкий desktop-клиент Kubernetes.
- [klustr](https://github.com/SametKUM/klustr) — desktop-клиент, работающий по kubeconfig.
- [sextant](https://github.com/FriendsOfKubernetes/sextant) — desktop-клиент Kubernetes (альтернатива Lens) с MCP-сервером.
- [lfk](https://github.com/janosmiko/lfk) — Kubernetes-TUI в стиле yazi: иерархия владельцев, логи, shell, helm.
- [kubiki](https://github.com/JustYarick/kubiki) — desktop-клиент Kubernetes: ресурсы, YAML, топология, Helm, логи, exec и AI-разбор через локальный CLI агента.

### iac

- [graphviz](https://gitlab.com/graphviz/graphviz) — `dot` для рендера графов Terraform/Terragrunt.
- [yc](https://cloud.yandex.ru/docs/cli/) — Yandex Cloud CLI: compute, VPC, managed-сервисы, Kubernetes, IAM и S3.
- [tflint](https://github.com/terraform-linters/tflint) — линтер Terraform/OpenTofu.
- [terraform-docs](https://github.com/terraform-docs/terraform-docs) — документация модулей из HCL.
- [pipeform](https://github.com/magodo/pipeform) — TUI прогресса `terraform plan/apply` вместо потока лога.
- [terraform-inventory](https://github.com/adammck/terraform-inventory) — inventory для Ansible из `terraform.tfstate`: хосты по именам ресурсов и группам тегов, поддерживает Yandex.Cloud.
- [terraform-ls](https://github.com/hashicorp/terraform-ls) — LSP-сервер для HCL: автодополнение, диагностика, форматирование.
- [packer](https://github.com/hashicorp/packer) — сборка образов VM и контейнеров.
- [driftctl](https://github.com/snyk/driftctl) — расхождения реальной инфраструктуры с IaC.
- [driftive](https://github.com/driftive/driftive) — дрейф Terragrunt/Terraform/OpenTofu: параллельный `plan` по юнитам репозитория.
- [tgsieve](https://github.com/imcitius/tgsieve) — сжатый вывод `terragrunt plan` по всему стеку.
- [s5cmd](https://github.com/peak/s5cmd) — быстрый параллельный клиент S3.
- [stu](https://github.com/lusingander/stu) — TUI-браузер S3-бакетов: префиксы, объекты, размеры, скачивание.
- [tpm](https://github.com/Madh93/tpm) — менеджер провайдеров Terraform/OpenTofu.
- [tfvar](https://github.com/shihanng/tfvar) — генерация `variables.tf` из существующего кода.
- [config-lint](https://github.com/stelligent/config-lint) — валидация HCL/JSON/YAML по декларативным правилам.
- [tf-mirror](https://github.com/kashtan404/tf-mirror) — локальное зеркало провайдеров Terraform для air-gapped и CI.
- [gitlab-terraform-manager](https://github.com/CRASH-Tech/gitlab-terraform-manager) — управление GitLab Terraform backend.
- [inframap](https://github.com/cycloidio/inframap) — граф инфраструктуры из tfstate или HCL.
- [terramate](https://github.com/terramate-io/terramate) — оркестрация стэков IaC: change detection и генерация кода.
- [infracost](https://github.com/infracost/infracost) — стоимость изменений по `terraform plan`.
- [rover](https://github.com/im2nguyen/rover) — интерактивный визуализатор Terraform state и плана.
- [terraformer](https://github.com/GoogleCloudPlatform/terraformer) — генерация Terraform-кода из существующей инфраструктуры.
- [terrascan](https://github.com/tenable/terrascan) — проверка IaC по политикам OPA/Rego.
- [steampipe](https://github.com/turbot/steampipe) — SQL-запросы к облакам и API через плагины.
- [tenv](https://github.com/tofuutils/tenv) — менеджер версий OpenTofu/Terraform/Terragrunt/Terramate/Atmos.
- [tfupdate](https://github.com/minamijoyo/tfupdate) — обновление пинов провайдеров и модулей в HCL.
- [tfsort](https://github.com/AlexNabokikh/tfsort) — сортировка блоков в `.tf`.
- [d2](https://github.com/d2lang/d2) — diagram-as-code: текстовый DSL в SVG/PNG, sequence- и архитектурные схемы.
- [tfautomv](https://github.com/busser/tfautomv) — генерация `moved`-блоков Terraform при переименовании и переносе ресурсов.
- [tfmigrate](https://github.com/minamijoyo/tfmigrate) — операции со state как код: `mv`/`import`/`replace-provider` планом в HCL, с историей и dry-run.
- [tfstate-lookup](https://github.com/fujiwara/tfstate-lookup) — запросы к `terraform.tfstate` как к JSON: атрибут по адресу, интерактивный режим, дамп ресурсов; локальный state и удалённые бэкенды.
- [tftui](https://github.com/idoavrah/terraform-tui) — TUI для работы с Terraform-стейтом.
- [checkov](https://github.com/bridgecrewio/checkov) — SAST для IaC: мисконфиги в Terraform, Kubernetes, Dockerfile, Helm.
- [yor](https://github.com/bridgecrewio/yor) — автотеги IaC-ресурсов git-метаданными: репозиторий, коммит и автор, чтобы облачный ресурс находился по коду.
- [atmos](https://github.com/cloudposse/atmos) — оркестрация Terraform-окружений поверх Terragrunt.
- [RackPeek](https://github.com/Timmoth/RackPeek) — инвентаризация железа, сервисов и сетей хоумлаба (CLI `rpk`, web-UI, генераторы Ansible/SSH/hosts).
- [tfenv](https://github.com/tfutils/tfenv) — менеджер версий Terraform.
- [tgenv](https://github.com/tgenv/tgenv) — менеджер версий Terragrunt.

### postgres

- [dbx](https://github.com/t8y2/dbx) — GUI-клиент к 100+ СУБД (PostgreSQL, MySQL, SQLite, Redis, MongoDB, DuckDB) с CLI и MCP-сервером.
- [pgCenter](https://github.com/lesovsky/pgcenter) — консольная админка и мониторинг PostgreSQL.
- [pgmetrics](https://github.com/rapidloop/pgmetrics) — снимок состояния PostgreSQL в текст или JSON для разбора инцидента.
- [tbls](https://github.com/k1LoW/tbls) — документация схемы БД в Markdown/PlantUML и `tbls diff` для CI.
- [pgbadger](https://github.com/darold/pgbadger) — разбор логов PostgreSQL в HTML: медленные запросы, checkpoint'ы, ошибки и временные файлы.
- [pg-activity](https://github.com/dalibo/pg_activity) — интерактивный монитор сессий и блокировок (top для PostgreSQL).
- [pspg](https://github.com/okbob/pspg) — пейджер для psql: таблицы с рамками и горизонтальной прокруткой.
- [pgformatter](https://github.com/darold/pgFormatter) — `pg_format`: форматирование длинных SQL-запросов для разбора.
- [pg_amcheck](https://www.postgresql.org/docs/current/app-pgamcheck.html) — проверка btree-индексов по подключению (симлинк на бинарник из `postgresql-client`).
- [pg_flame](https://github.com/mgartner/pg_flame) — flamegraph из `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`.
- [migra](https://github.com/djrobstep/migra) — diff схем двух PostgreSQL: что изменилось между окружениями.
- [pgcli](https://github.com/dbcli/pgcli) — psql с автодополнением и подсветкой синтаксиса.
- [libpq5](https://www.postgresql.org/) — клиентская библиотека PostgreSQL для psycopg и pgcli.
- [postgresql-client](https://www.postgresql.org/) — штатный CLI: `psql`, `pg_dump`, `pg_restore`, `pg_isready`.
- [rainfrog](https://github.com/achristmascarl/rainfrog) — TUI-клиент к PostgreSQL, MySQL и SQLite: таблицы, запросы, история.
- [sql-tap](https://github.com/mickamy/sql-tap) — перехват SQL-трафика приложения: прокси `sql-tapd` и TUI `sql-tap` с запросами, транзакциями и EXPLAIN.
- [datanymizer](https://github.com/datanymizer/datanymizer) — дамп PostgreSQL с анонимизацией данных по правилам (Faker, замена, фильтры).

### clickhouse

- [clickhouse-client](https://clickhouse.com/) — консольный клиент ClickHouse из официального apt-репозитория (`stable`).
- [chdig](https://github.com/azat/chdig) — TUI к ClickHouse: выполняющиеся запросы и их тяжесть, parts и merges, репликация, ошибки в реальном времени.
- [RootCA Yandex Cloud](https://yandex.cloud/ru/docs/managed-clickhouse/operations/connect) — корневой CA (`CN=YandexInternalRootCA`) для TLS к managed-кластеру ClickHouse: без него клиент не проверяет цепочку сертификата.

### runtimes

- [Python 3 (venv/pip)](https://www.python.org/) — интерпретатор и виртуальные окружения из apt.
- [confluent-kafka](https://github.com/confluentinc/confluent-kafka-python) — Python-клиент Kafka из apt (`python3-confluent-kafka`): официальный, на librdkafka.
- [uv](https://github.com/astral-sh/uv) — быстрый менеджер Python-пакетов и версий.
- [Go](https://go.dev/) — компилятор и toolchain из apt (`golang-go`).
- [Rust](https://www.rust-lang.org/) — `rustc`, `cargo`, `rustfmt` и `clippy` из apt, `rust-src` для std.
- [rust-analyzer](https://rust-analyzer.github.io/) — LSP-сервер для Rust из официального релиза.
- [Node.js + npm](https://nodejs.org/) — рантайм и менеджер пакетов из apt.
- [Java 21 (OpenJDK)](https://openjdk.org/) — JDK из apt.
- [Maven](https://maven.apache.org/) — сборка Java по `pom.xml` из apt (`mvn test/verify`); проекты с `mvnw` тянут wrapper сами.
- [protoc](https://github.com/protocolbuffers/protobuf) — компилятор Protocol Buffers из apt (`protobuf-compiler`): генерация кода из `.proto`, well-known types в `/usr/include`.
- [gopls](https://github.com/golang/go/wiki/gopls) — language server Go: автодополнение, переходы, переименование и диагностика в редакторе.
- [QEMU](https://github.com/qemu/qemu) — виртуалка для Lima (`qemu-system-x86_64`, `qemu-img`).
- [dagger](https://github.com/dagger/dagger) — CI-пайплайны как код: шаги на Go/Python/TypeScript в контейнерах.
- [golangci-lint](https://github.com/golangci/golangci-lint) — раннер линтеров Go: staticcheck, govet, errcheck, revive одним прогоном.
- [Lima](https://github.com/lima-vm/lima) — Linux-VM поверх Linux (`limactl`, `lima`): containerd, Docker и k3s внутри.
- [py-spy](https://github.com/benfred/py-spy) — сэмплирующий профилировщик Python: `top` по живому PID, `dump` стеков, `record` в flamegraph, без правок кода.

### secrets

- [direnv](https://github.com/direnv/direnv) — переменные окружения по каталогам.
- [Vault](https://github.com/hashicorp/vault) — хранилище секретов с аудитом и политиками.
- [gitleaks](https://github.com/gitleaks/gitleaks) — поиск секретов в git-истории и файлах.
- [betterleaks](https://github.com/betterleaks/betterleaks) — сканер секретов от авторов gitleaks: приоритизация находок, проверка ключей и анализ прав учётной записи.
- [sops](https://github.com/getsops/sops) — шифрование секретов прямо в Git (KMS/age/PGP).
- [grype](https://github.com/anchore/grype) — сканер уязвимостей образов и файловой системы.
- [trivy](https://github.com/aquasecurity/trivy) — уязвимости образов, IaC и секреты одним сканером.
- [age](https://github.com/FiloSottile/age) — простое шифрование файлов, бэкенд sops.
- [lynis](https://github.com/CISOfy/lynis) — аудит безопасности и харденинга Linux.
- [osquery](https://github.com/osquery/osquery) — SQL-подобная инструментация ОС.
- [mfa](https://github.com/LexSerest/mfa) — терминальный менеджер 2FA/TOTP.
- [medusa](https://github.com/jonasvinther/medusa) — импорт и экспорт секретов Vault.
- [bank-vaults](https://github.com/bank-vaults/bank-vaults) — init/unseal и конфигурация Vault через YAML.
- [horusec](https://github.com/ZupIT/horusec) — SAST одной командой.
- [opengrep](https://github.com/opengrep/opengrep) — SAST на правилах с taint-анализом (форк Semgrep CE).
- [dependency-check](https://github.com/dependency-check/DependencyCheck) — OWASP SCA: уязвимые зависимости проекта.
- [trufflehog](https://github.com/trufflesecurity/trufflehog) — поиск секретов с проверкой, что ключ живой.
- [syft](https://github.com/anchore/syft) — SBOM образов и каталогов в CycloneDX/SPDX.
- [cosign](https://github.com/sigstore/cosign) — подпись и проверка артефактов sigstore.
- [entropy](https://github.com/EwenQuim/entropy) — поиск строк с высокой энтропией: ключей и токенов по признаку случайности.
- [ochrona](https://pypi.org/project/ochrona/) — SCA для Python-зависимостей: сверка версий с базой OSV.
- [osv-scanner](https://github.com/google/osv-scanner) — SCA по lockfile во всех экосистемах, база OSV; `--call-analysis` для Rust и Go.
- [govulncheck](https://go.dev/blog/vuln) — Go reachability: только уязвимые символы, которые проект реально вызывает.
- [gosec](https://github.com/securego/gosec) — SAST для Go: секреты в коде, небезопасный file open, SSRF, слабый random.
- [dotenvx](https://github.com/dotenvx/dotenvx) — шифрование `.env` по публичному ключу и запуск команды с расшифрованными переменными.
- [cargo-deny](https://github.com/EmbarkStudios/cargo-deny) — RustSec, лицензии и запрещённые зависимости Cargo.
- [landrun](https://github.com/Zouuup/landrun) — sandbox для команды на Landlock: файловая система и сеть без root.
- [subfinder](https://github.com/projectdiscovery/subfinder) — пассивный поиск поддоменов по публичным источникам.
- [gitjacker](https://github.com/liamg/gitjacker) — выкачивание git-репозитория с сайтов, где случайно оставили доступным каталог `.git`, и восстановление исходников.

Фильтры запускаются раздельно, без своей обёртки:

```bash
# CVSS >= 8: порог для exit code (зависимости, которые понимает dependency-check)
dependency-check --project app --scan . --failOnCVSS 8

# RCE в коде: command injection (CWE-78)
opengrep scan --config p/command-injection --error .

# Шире: OWASP Top 10, включая CWE-94/95/502
opengrep scan --config p/owasp-top-ten --error .
```

`--failOnCVSS` меняет только код возврата, отчёт содержит все CVE. Точный
список CVSS >= 8 — `--format JSON` и `jq` по `cvssv3.baseScore`. CWE в JSON
`osv-scanner`/`dependency-check` есть, но нативного CWE-фильтра у них нет:
RCE по зависимостям отбирается тем же `jq` по `cwe_ids`/`cwes`.

`gosec` — SAST именно для Go, отдельно от `opengrep`: он знает stdlib и
идиомы языка, поэтому находит `os/exec` с конкатенацией аргументов (G204),
`math/rand` в токенах (G404) и путь из запроса в `os.Open` (G304).

```bash
# Полный прогон с отчётом для CI
gosec -fmt sarif -out reports/gosec.sarif ./...

# Только секреты, file open и random
gosec -include=G101,G304,G404 ./...
```

`dotenvx` дополняет `sops` там, где секреты уже лежат в обычном `.env`
(Node/Python-приложение), а заводить `.sops.yaml` и ключ никто не хочет:
файл шифруется публичным ключом и остаётся `.env` для кода.

```bash
dotenvx encrypt            # создаёт .env.keys и шифрует значения в .env
dotenvx run -- npm start   # запускает команду с расшифрованными переменными
```

### dast

- [nuclei](https://github.com/projectdiscovery/nuclei) — шаблонный DAST: известные CVE/RCE, DAST-фаззинг и OpenAPI-вход.
- [katana](https://github.com/projectdiscovery/katana) — краулер: собирает URL из HTML и JS-файлов перед `nuclei`/`ffuf`.
- [ffuf](https://github.com/ffuf/ffuf) — быстрый веб-фаззер: скрытые пути, параметры и vhost по словарю; дополняет шаблоны nuclei.
- [feroxbuster](https://github.com/epi052/feroxbuster) — рекурсивный content discovery: уходит в найденные каталоги, извлекает ссылки из ответов.
- [hetty](https://github.com/dstotijn/hetty) — перехватывающий HTTP/HTTPS-прокси с веб-интерфейсом: правка запросов и ответов вручную, история, повтор.
- [openapi-tui](https://github.com/zaghaghi/openapi-tui) — просмотр OpenAPI и ручные запросы из терминала: что описано в спецификации до фаззинга.
- [vacuum](https://github.com/daveshanley/vacuum) — линтер OpenAPI: 400+ правил и HTML-отчёт об ошибках самой спецификации до фаззинга и API scan.
- [oasdiff](https://github.com/oasdiff/oasdiff) — breaking changes между двумя версиями OpenAPI (`oasdiff breaking`), как `buf breaking` для protobuf.
- [OWASP ZAP](https://www.zaproxy.org/) — общий DAST: passive/active scan, API scan по OpenAPI/SOAP/GraphQL, отчёты для CI.
- [wapiti](https://github.com/wapiti-scanner/wapiti) — чёрный ящик: SQLi, command execution, XXE, SSRF, LFI, upload, Log4Shell/Spring4Shell.
- [sqlmap](https://sqlmap.org/) — SQL-инъекции и доказательство RCE через `--os-shell`.
- [schemathesis](https://schemathesis.readthedocs.io/) — property-based и stateful фаззинг API по OpenAPI/GraphQL.
- [EvoMaster](https://github.com/WebFuzzing/EvoMaster) — эволюционный фаззинг API по OpenAPI/GraphQL с генерацией JUnit/Python/Playwright-тестов из находок.

### fuzz

- [AFL++](https://github.com/AFLplusplus/AFLplusplus) — coverage-guided фаззинг нативного кода: `afl-cc`, persistent mode, ASan/UBSan.
- [libFuzzer](https://llvm.org/docs/LibFuzzer.html) — in-process coverage-guided фаззинг в clang: `-fsanitize=fuzzer,address,undefined`.
- [zzuf](https://github.com/samhocevar/zzuf) — прозрачные мутации файлов и потоков для быстрого black-box прогона без пересборки.
- [Jazzer](https://github.com/CodeIntelligenceTesting/jazzer) — coverage-guided фаззинг JVM (Java/Kotlin) с санитайзерами и воспроизведением входов.

### shell

- [eza](https://github.com/eza-community/eza) — современная замена `ls` с иконками и git-статусом.
- [zoxide](https://github.com/ajeetdsouza/zoxide) — быстрый переход по каталогам (`z`).
- [fzf](https://github.com/junegunn/fzf) — интерактивный fuzzy-поиск.
- [ripgrep](https://github.com/BurntSushi/ripgrep) — быстрый рекурсивный grep.
- [rga (ripgrep-all)](https://github.com/phiresky/ripgrep-all) — ripgrep с поиском внутри PDF, EPUB и архивов через адаптеры.
- [ast-grep](https://github.com/ast-grep/ast-grep) — структурный поиск и переписывание кода по AST, а не по строке.
- [catdoc](http://www.wagner.pp.ru/~vitus/software/catdoc/) — текст из файлов Office 97-2003: `catdoc report.doc`, `xls2csv book.xls`, `catppt slides.ppt`.
- [fd-find](https://github.com/sharkdp/fd) — простая и быстрая замена `find`.
- [fselect](https://github.com/jhspetersson/fselect) — поиск файлов SQL-подобными запросами: фильтры и сортировка по размеру, дате, правам и владельцу.
- [starship](https://github.com/starship/starship) — prompt с информацией о репозитории и окружении.
- [bat](https://github.com/sharkdp/bat) — `cat` с подсветкой синтаксиса и номерами строк.
- [difftastic](https://github.com/Wilfred/difftastic) — структурный diff с пониманием синтаксиса языка.
- [delta](https://github.com/dandavison/delta) — улучшенный просмотр git-diff.
- [omnidiff](https://github.com/ivankovic/omnidiff) — контентно-зависимый diff: PDF, шрифты, архивы, изображения и каталоги переводов — что изменилось внутри, а не «binary files differ».
- [qpdf](https://github.com/qpdf/qpdf) — починка и перепаковка PDF: repair, шифрование и снятие пароля, линейный режим, слияние и разбор страниц.
- [gdu](https://github.com/dundee/gdu) — быстрый анализатор занятого места с интерактивным режимом.
- [dust](https://github.com/bootandy/dust) — наглядный `du`: дерево каталогов с графиком.
- [dasel](https://github.com/TomWright/dasel) — запросы и правка JSON/YAML/TOML/XML/CSV/HCL.
- [jc](https://github.com/kellyjonbrazil/jc) — конвертация вывода CLI-утилит в JSON.
- [sd](https://github.com/chmln/sd) — интуитивная замена `sed` для поиска и замены.
- [serpl](https://github.com/yassinebridi/serpl) — TUI поиска и замены с превью результата до применения.
- [desed](https://github.com/SoptikHa2/desed) — пошаговый отладчик sed-скриптов: какая команда выполняется, вход и результат на каждом шаге.
- [shellcheck](https://github.com/koalaman/shellcheck) — статический анализ shell-скриптов.
- [bats-core](https://github.com/bats-core/bats-core) — запуск тестов shell-скриптов: TAP-вывод, `setup`/`teardown`, проверки строк и кодов возврата.
- [duf](https://github.com/muesli/duf) — `df` «для людей»: таблица дисков и точек монтирования.
- [btop](https://github.com/aristocratos/btop) — монитор ресурсов с графиками.
- [ncdu](https://github.com/rofl0r/ncdu) — интерактивный анализ занятого места.
- [tv (television)](https://github.com/alexpasmantier/television) — fuzzy-finder с готовыми каналами поиска.
- [witr](https://github.com/pranshuparmar/witr) — трассировка «почему процесс запущен и кто держит порт».
- [sonar](https://github.com/raskrebs/sonar) — TUI-менеджер сервисов на localhost-портах: кто слушает, kill, перезапуск.
- [zellij](https://github.com/zellij-org/zellij) — терминальный мультиплексор.
- [navi](https://github.com/denisidoro/navi) — шпаргалки команд поверх fzf.
- [fx](https://github.com/antonmedv/fx) — интерактивный просмотр JSON.
- [jnv](https://github.com/ynqa/jnv) — интерактивный jq-фильтр для JSON.
- [octosql](https://github.com/cube2222/octosql) — SQL-запросы к JSON/CSV/Parquet.
- [sq](https://github.com/neilotoole/sq) — один SQL-диалект поверх PostgreSQL, MySQL, SQL Server, SQLite, ClickHouse и файлов CSV/JSON/XLSX.
- [hl](https://github.com/pamburus/hl) — быстрый просмотрщик JSON-логов.
- [lazyjournal](https://github.com/Lifailon/lazyjournal) — TUI для journald, auditd, Docker и файлов.
- [systemctl-tui](https://github.com/rgwood/systemctl-tui) — TUI по systemd: список юнитов, состояние, restart, логи и свойства без набора команд.
- [gonzo](https://github.com/control-theory/gonzo) — TUI-анализ логов с графиками по столбцам.
- [red](https://github.com/annamedv/red) — терминальный анализ JSON-логов из пайпа: группировка по полям, счётчики и спарклайн тренда.
- [otel-tui](https://github.com/ymtdzzz/otel-tui) — просмотр OpenTelemetry-трейсов, логов и метрик.
- [jl](https://github.com/koenbollen/jl) — фильтр структурированных JSON-логов.
- [logdy](https://github.com/logdyhq/logdy-core) — просмотр логов в браузере в реальном времени.
- [jlv](https://github.com/hedhyw/json-log-viewer) — интерактивный просмотр JSON-логов.
- [spacer](https://github.com/samwho/spacer) — разделители с таймингом между шагами пайплайна.
- [mcfly](https://github.com/cantino/mcfly) — умная история команд по Ctrl-R.
- [lf](https://github.com/gokcehan/lf) — терминальный файловый менеджер с vim-подобными клавишами.
- [micro](https://github.com/zyedidia/micro) — редактор в терминале: мышь, привычные Ctrl-S/Ctrl-Q, подсветка, сплиты и плагины.
- [gomplate](https://github.com/hairyhenderson/gomplate) — шаблонизатор конфигов из разных источников.
- [yamlfmt](https://github.com/google/yamlfmt) — форматтер YAML.
- [rumdl](https://github.com/rvben/rumdl) — линтер и форматтер Markdown с правилами markdownlint (MD001–MD059): `rumdl check`, `rumdl fmt`.
- [dprint](https://github.com/dprint/dprint) — один форматтер на Markdown, JSON, TOML, YAML, TypeScript и Dockerfile: `dprint fmt` / `dprint check`.
- [taplo](https://github.com/tamasfe/taplo) — TOML: `taplo fmt`, `taplo lint`, `taplo get` и LSP для редактора.
- [yamlfixer](https://github.com/opt-nc/yamlfixer) — автоисправление замечаний yamllint.
- [gum](https://github.com/charmbracelet/gum) — примитивы для «красивых» shell-скриптов.
- [fastfetch](https://github.com/fastfetch-cli/fastfetch) — информация о системе.
- [procs](https://github.com/dalance/procs) — современная замена `ps`.
- [grex](https://github.com/pemistahl/grex) — генерация регулярного выражения из примеров строк.
- [dusage](https://github.com/mihaigalos/dusage) — наглядный подсчёт занятого места.
- [de-nox](https://github.com/soul-abhi/De-Nox) — TUI-чистка артефактов сборки: кандидат определяется по простою проекта (mtime исходников), а не самого каталога.
- [mise](https://github.com/jdx/mise) — менеджер версий рантаймов.
- [just](https://github.com/casey/just) — командный раннер вместо Makefile.
- [task (go-task)](https://github.com/go-task/task) — раннер задач по `Taskfile.yml`: переменные, зависимости и watch-режим; дополняет `just`.
- [gocloc](https://github.com/hhatto/gocloc) — подсчёт строк кода по языкам (аналог cloc) с разбивкой по каталогам.
- [yazi](https://github.com/sxyazi/yazi) — быстрый TUI-файловый менеджер.
- [glow](https://github.com/charmbracelet/glow) — рендер Markdown в терминале.
- [btm (bottom)](https://github.com/ClementTsang/bottom) — монитор процессов и ресурсов с графиками.
- [hyperfine](https://github.com/sharkdp/hyperfine) — бенчмарк команд.
- [duckdb](https://github.com/duckdb/duckdb) — аналитическая СУБД: SQL по Parquet/CSV/JSON.
- [visidata](https://github.com/saulpw/visidata) — интерактивный просмотр таблиц в терминале: CSV/TSV, Excel, JSON/JSONL, Parquet, SQLite и SQL.
- [asciinema](https://github.com/asciinema/asciinema) — запись терминальной сессии в текстовый cast: багрепорт, runbook, воспроизведение (`asciinema play`).
- [harlequin](https://github.com/tconbeer/harlequin) — SQL-IDE в терминале.
- [lazysql](https://github.com/jorgerojas26/lazysql) — TUI-клиент к MySQL, PostgreSQL, MSSQL и SQLite.
- [sqlfluff](https://github.com/sqlfluff/sqlfluff) — линтер и автоисправление SQL с диалектами postgres, clickhouse, duckdb, mysql и tsql; `pg_format` только форматирует.
- [ghostman](https://github.com/4yk5/Ghostman) — TUI-клиент HTTP API и инспектор вебхуков: коллекции plain-файлами, встроенный слушатель на 9090, без облака.
- [toolong](https://github.com/Textualize/toolong) — просмотр, хвост и слияние логов и JSONL на общем таймлайне.
- [spf (superfile)](https://github.com/yorukot/superfile) — двухпанельный TUI-файлменеджер: превью, корзина, массовое переименование.
- [shellclear](https://github.com/rusty-ferris-club/shellclear) — поиск секретов и опасных команд в истории shell.
- [nxs-backup](https://github.com/nixys/nxs-backup) — бэкапы по YAML-описанию.
- [kopia](https://github.com/kopia/kopia) — инкрементальные бэкапы файлов с дедупликацией и клиентским шифрованием.
- [cheat](https://github.com/cheat/cheat) — собственные шпаргалки команд.
- [tldr](https://github.com/tldr-pages/tldr) — краткие примеры команд.
- [carapace](https://github.com/rsteube/carapace-bin) — автодополнение по готовым спекам сотен команд (kubectl, helm, flux, terraform, gh, glab, docker): Tab подсказывает флаги и их значения в обычной строке shell, без Node.
- [JetBrainsMono Nerd Font](https://github.com/ryanoasis/nerd-fonts) — шрифт с иконками для prompt и `eza --icons`.
- [ghostty](https://github.com/ghostty-org/ghostty) — терминал на GTK4: окна, табы, сплиты.
- [wl-clipboard](https://github.com/bugaevc/wl-clipboard) — `wl-copy`/`wl-paste` для Wayland: буфер обмена из пайплайна и обратно.
- [M-Commander](https://github.com/blue-panels/mcommander) — двухпанельный файловый менеджер.
- [fontconfig](https://gitlab.freedesktop.org/fontconfig/fontconfig) — `fc-cache` для кэша шрифтов (Nerd Font).
- [ffmpeg](https://github.com/FFmpeg/FFmpeg) — декодирование видео для `rga` (поиск по тексту внутри видео) и перекодирование медиа.
- [moreutils](https://joeyh.name/code/moreutils/) — мелкие утилиты для пайплайнов: `sponge`, `ts`, `vidir`, `ifne`, `chronic`, `pee`.
- [GNU parallel](https://www.gnu.org/software/parallel/) — параллельное выполнение команд вместо циклов и `xargs`.
- [lnav](https://github.com/tstack/lnav) — просмотрщик логов с SQL-запросами, таймлайном и автодетектом формата.
- [ioping](https://github.com/koct9i/ioping) — латентность дисковой подсистемы: отзывчивость I/O, а не объём.
- [fatrace](https://github.com/martinpitt/fatrace) — трассировка доступа к файлам: какой процесс читает, пишет или удаляет.
- [shfmt](https://github.com/mvdan/sh) — форматтер shell-скриптов, дополняет `shellcheck`.
- [sysstat](https://github.com/sysstat/sysstat) — история производительности: `sar`, `iostat`, `mpstat`, `pidstat`.
- [perf](https://perf.wiki.kernel.org/) — сэмплирующий профайлер: `perf top`, `perf record` и flame graph (пакет `linux-tools-generic`).
- [pv](https://github.com/ivarch/pv) — прогресс и скорость потока в пайпе: `pv dump.sql | gzip`.
- [redis-tools](https://github.com/redis/redis) — `redis-cli`: latency, TTL, MONITOR, SLOWLOG.
- [kcat](https://github.com/edenhill/kcat) — клиент Kafka: топики, группы, чтение и запись сообщений из CLI.
- [kafkactl](https://github.com/deviceinsight/kafkactl) — админский CLI Kafka: топики и партиции, consumer groups и лаг, ACL, конфиги брокеров и топиков.
- [kaf](https://github.com/birdayz/kaf) — Kafka CLI на Go: топики и партиции, consume/produce, группы и лаг, конфиги и ACL, контексты кластеров.
- [miller](https://github.com/johnkerl/miller) — awk/sed/cut/join/sort для CSV, TSV, JSON и JSONL с именованными полями.
- [gron](https://github.com/tomnomnom/gron) — разворачивает JSON в строки `json[3].spec.replicas = 3;` для grep и собирает обратно (`gron -u`).
- [jless](https://github.com/PaulJuliusMartinez/jless) — пейджер JSON только для чтения: vim-клавиши, сворачивание узлов, поиск, копирование пути до поля.
- [fq](https://github.com/wader/fq) — jq для бинарных форматов: ELF, ZIP, tar, gzip, pcap, TLS, DNS, protobuf, CBOR, JPEG/EXIF декодируются в дерево полей.
- [sig](https://github.com/ynqa/sig) — интерактивный grep по живому потоку: `kubectl logs -f … |& sig`, переключение контекста без остановки пайпа.
- [agrind (angle-grinder)](https://github.com/rcoh/angle-grinder) — агрегаты по потоку логов одной строкой: `kubectl logs -f … | agrind '* | json | count by level'` — группировка, счётчики, avg/p95 по полям.
- [nerdlog](https://github.com/dimonomid/nerdlog) — TUI-просмотр логов нескольких хостов по SSH на общей шкале времени.
- [devops-shell.sh](https://github.com/patsevanton/ansible-for-ubuntu-devops-workstation/blob/main/roles/shell/templates/devops-shell.sh.j2) — конфиг shell: `~/.config/devops-shell.sh` плюс одна строка `source` в `~/.bashrc`.

### network

- [nmap](https://github.com/nmap/nmap) — сканер портов и сервисов.
- [sx](https://github.com/v-byte-cpu/sx) — быстрый сетевой сканер: ICMP/ARP/NDP, TCP SYN/FIN/NULL/Xmas, UDP и IPv4/IPv6 через raw-сокеты.
- [whosthere](https://github.com/ramonvermeulen/whosthere) — TUI-обнаружение устройств в локальной сети: mDNS, SSDP, ARP.
- [netcat](https://nc110.sourceforge.io/) — «швейцарский нож» TCP/UDP.
- [tcpdump](https://github.com/the-tcpdump-group/tcpdump) — захват и разбор пакетов.
- [httpie](https://github.com/httpie/cli) — человекочитаемый HTTP-клиент.
- [dig (dnsutils)](https://github.com/isc-projects/bind9) — DNS-запросы.
- [whois](https://github.com/rfc1036/whois) — регистратор, даты, NS и контакты домена или IP.
- [quien](https://github.com/retlehs/quien) — whois и разведка по домену в одном TUI: WHOIS/RDAP, DNS, почта, TLS, SEO и стек; JSON-вывод для скриптов.
- [godap](https://github.com/Macmod/godap) — LDAP-клиент в терминале: дерево каталога, поиск, просмотр и правка атрибутов.
- [checkip](https://github.com/jreisinger/checkip) — проверка IP по нескольким источникам: гео, ASN, DNS-имя, репутация (VirusTotal, SANS), ping и TLS-сертификат; JSON-вывод для `jq`.
- [ipinfo](https://github.com/ipinfo/cli) — официальный CLI ipinfo.io: ASN, сеть и гео по IP, bulk-поиск и суммаризация адресов, подкоманды `grepip`/`matchip`/`prips`/`cidr2ip`/`range2cidr`; версия закреплена, потому что `/releases/latest` в репозитории указывает на релиз другой команды ([ipinfo/cli#259](https://github.com/ipinfo/cli/issues/259)).
- [telnet](https://savannah.gnu.org/projects/inetutils) — проверка TCP-портов.
- [tshark](https://github.com/wireshark/wireshark) — CLI Wireshark, нужен termshark для разбора PCAP.
- [mosh](https://mosh.org/) — мобильный shell: сессия переживает обрыв связи и смену IP.
- [iprange](https://github.com/firehol/iprange) — арифметика подсетей и IP-диапазонов для фаервола и ipset.
- [grepcidr](https://www.pc-tools.net/unix/grepcidr/) — фильтрация строк и логов по списку сетей: `grepcidr -f nets.txt access.log`, инверсия и подсчёт.
- [bgpq4](https://github.com/bgp/bgpq4) — prefix-list по ASN и AS-SET из IRR (RADB, RIPE): сети организации без API-ключа, в отличие от asnmap.
- [mmdblookup (mmdb-bin)](https://github.com/maxmind/libmaxminddb) — офлайн-поиск по MMDB: ASN по базе DB-IP ASN Lite в `/usr/share/GeoIP/dbip-asn-lite.mmdb`, которую роль обновляет при первом прогоне нового месяца.
- [testssl.sh](https://github.com/drwetter/testssl.sh) — полный аудит TLS: протоколы, шифры, цепочка, известные уязвимости.
- [sslscan](https://github.com/rbsec/sslscan) — быстрый перебор шифров и протоколов TLS/SSL: предпочтения сервера, слабые шифры, повторное согласование; пакет Ubuntu, linux-бинарник в апстриме запрошен в [#375](https://github.com/rbsec/sslscan/issues/375).
- [socat](http://www.dest-unreach.org/socat/) — relay между TCP/UDP и Unix-сокетами, TLS-обёртка, PTY и exec-адреса.
- [sshfs](https://github.com/libfuse/sshfs) — монтирование каталога удалённого хоста через SFTP.
- [rclone](https://github.com/rclone/rclone) — синхронизация и монтирование S3, WebDAV, SFTP, Google Drive, OneDrive.
- [iperf3](https://github.com/esnet/iperf) — пропускная способность и джиттер между ноутбуком и сервером.
- [ethtool](https://mirrors.edge.kernel.org/pub/software/network/ethtool/) — скорость, duplex, драйвер, ring buffers и ошибки физического линка.
- [rkn-block-checker](https://pypi.org/project/rkn-block-checker/) — диагностика блокировок: DNS-подмена, TCP reset, DPI по SNI.
- [showcert](https://github.com/yaroslaff/showcert) — человекочитаемый разбор X.509-сертификатов.
- [ssh-audit](https://github.com/jtesta/ssh-audit) — аудит конфигурации SSH-серверов и клиентов.
- [httptap](https://github.com/monasticacademy/httptap) — разбор HTTP-запроса по слоям: DNS, connect, TLS, TTFB.
- [httpstat](https://github.com/reorx/httpstat) — тайминги запроса по этапам с долями, JSON-выводом и порогами SLO.
- [lexicon](https://github.com/AnalogJ/lexicon) — управление DNS-записями у разных провайдеров.
- [netutils-linux](https://github.com/strizhechenko/netutils-linux) — утилиты диагностики и тюнинга сетевого стека.
- [reachable](https://github.com/italolelis/reachable) — проверка доступности домена по резолверам и HTTP.
- [gai](https://github.com/casablanque-code/gai) — инспектор `getaddrinfo`: реальный путь разрешения имени.
- [dnsglobe](https://github.com/514-labs/dnsglobe) — TUI-проверка распространения DNS-записи по публичным резолверам.
- [dnspeep](https://github.com/jvns/dnspeep) — какие процессы шлют DNS-запросы: имя, тип, сервер, задержка и ответ.
- [bandwhich](https://github.com/imsnif/bandwhich) — трафик по процессам и соединениям.
- [q](https://github.com/natesales/q) — DNS-клиент с DoH/DoT/DoQ/ODoH.
- [xh](https://github.com/ducaale/xh) — быстрый HTTP-клиент, замена httpie.
- [curl-impersonate](https://github.com/lexiforest/curl-impersonate) — curl с TLS/HTTP2-отпечатком Chrome, Firefox, Safari, Edge и Tor: статический бинарник `curl-impersonate --impersonate chrome152` и обёртки `curl_chrome152`/`curl_firefox155`.
- [curl_cffi](https://github.com/lexiforest/curl_cffi) — Python-биндинг к curl-impersonate с API requests: браузерный отпечаток и заголовки через `impersonate="chrome"` и CLI `curl-cffi get`, `curl-cffi list`.
- [kyanos](https://github.com/hengyoush/kyanos) — анализ сетевых запросов через eBPF.
- [hurl](https://github.com/Orange-OpenSource/hurl) — HTTP-запросы и тесты из plain-text `.hurl`-файлов.
- [trippy](https://github.com/fujiapple852/trippy) — TUI traceroute со статистикой по хопам.
- [ttl](https://github.com/lance0/ttl) — трассировка с TUI и диагностикой: MTU/PMTUD, ECMP, NAT, flap маршрутов, ASN/geo/IX и MPLS; JSON и Prometheus.
- [mtr](https://github.com/traviscross/mtr) — traceroute и ping в одном: потери и задержки по каждому хопу, отчёт `--report` для тикета.
- [httping](https://github.com/flok99/httping) — «ping» по HTTP: код ответа и время запроса циклом, min/avg/max и гистограмма.
- [ecapture](https://github.com/gojue/ecapture) — захват TLS-трафика приложений без CA-сертификатов.
- [termshark](https://github.com/gcla/termshark) — TUI к Wireshark/tshark.
- [websocat](https://github.com/vi/websocat) — netcat для WebSocket.
- [grpcurl](https://github.com/fullstorydev/grpcurl) — `curl` для gRPC: reflection, describe и вызов методов с JSON.
- [buf](https://github.com/bufbuild/buf) — линт и форматирование `.proto`, детект ломающих изменений API.
- [tcping](https://github.com/pouriyajamshidi/tcping) — `ping` поверх TCP-порта.
- [doggo](https://github.com/mr-karan/doggo) — DNS-клиент с человекочитаемым цветным выводом.
- [gotty](https://github.com/yudai/gotty) — терминал как веб-приложение.
- [miniserve](https://github.com/svenstaro/miniserve) — отдать каталог по HTTP одной командой: листинг, загрузка файлов, basic-auth и TLS.
- [sshx](https://github.com/ekzhang/sshx) — совместный терминал в браузере.
- [txeh](https://github.com/txn2/txeh) — управление `/etc/hosts` из CLI.
- [assh](https://github.com/moul/assh) — генерация SSH-конфигов, jump-хосты и прокси.
- [boring](https://github.com/alebeck/boring) — менеджер SSH-туннелей: local/remote/SOCKS5 из TOML с автопереподключением.
- [chisel](https://github.com/jpillora/chisel) — TCP/UDP-туннель поверх HTTP: проброс портов через один 443 с TLS.
- [gossl](https://github.com/vvrnv/gossl) — проверка SSL-сертификата: цепочка, срок, протоколы.
- [tlsexp](https://gitlab.com/devopsworks/tools/tlsexp) — массовая проверка сроков TLS-сертификатов по списку URL: CN/SAN, издатель, остаток часов, подсветка просроченных; метрики в Prometheus.
- [crip (certificate-ripper)](https://github.com/Hakky54/certificate-ripper) — извлечение цепочки сертификатов с хоста.
- [k6](https://github.com/grafana/k6) — нагрузочное тестирование сценариями на JS.
- [gping](https://github.com/orf/gping) — ping с графиком задержек.
- [rustnet](https://github.com/domcyrus/rustnet) — TUI-мониторинг сети по процессам с разбором пакетов.
- [sniffnet](https://github.com/GyulyVGC/sniffnet) — графический TUI-мониторинг трафика.
- [uncover](https://github.com/projectdiscovery/uncover) — поиск хостов через Shodan, Censys, FOFA, Quake и другие движки.
- [ptcpdump](https://github.com/mozillazg/ptcpdump) — tcpdump на eBPF, который показывает процесс и контейнер для каждого пакета.
- [posting](https://github.com/darrenburns/posting) — HTTP-клиент в терминале: коллекции, окружения, история, `.http`-файлы.
- [lazyssh](https://github.com/Adembc/lazyssh) — SSH-менеджер в стиле lazydocker/k9s: хосты из `~/.ssh/config`, подключение, ключи.
- [omnyssh](https://github.com/timhartmann7/omnyssh) — SSH-менеджер: TUI `omny` и GUI `OmnySSH` с вкладками, метриками, SFTP и пробросом портов.
- [NetBird](https://github.com/netbirdio/netbird) — mesh VPN на WireGuard: peer-to-peer, SSO и ACL; CLI и демон `netbird` из официального apt-репозитория.
- [netbird-ui](https://github.com/netbirdio/netbird) — графический клиент NetBird на GTK4/WebKit: подключение, статус и настройки без CLI.
- [wireguard-tools](https://git.zx2c4.com/wireguard-tools/) — `wg` и `wg-quick`: пиры, хендшейки и простой туннель; нужен и для диагностики NetBird.

### ebpf

- [bpftrace](https://github.com/bpftrace/bpftrace) — однострочники и скрипты для ad-hoc трассировки ядра на eBPF.
- [bpfcc-tools](https://github.com/iovisor/bcc) — готовые BCC-скрипты: `execsnoop`, `opensnoop`, `biolatency`, `tcplife`, `runqlat` и другие.
- [pwru](https://github.com/cilium/pwru) — eBPF-отладчик сетевого стека: где потерялся пакет.
- [bpftop](https://github.com/jfernandez/bpftop) — обзор запущенных eBPF-программ и их CPU.
- [oryx](https://github.com/pythops/oryx) — TUI-сниффер трафика на eBPF.
- [pktstat-bpf](https://github.com/dkorunic/pktstat-bpf) — монитор трафика по процессам и потокам.
- [tracee](https://github.com/aquasecurity/tracee) — runtime-security и форензика Linux на eBPF.

### monitoring

- [vmalert-tool](https://github.com/VictoriaMetrics/VictoriaMetrics) — офлайн-проверка и unit-тесты алерт-правил.
- [vlogscli](https://github.com/VictoriaMetrics/VictoriaLogs) — CLI-клиент VictoriaLogs: LogsQL-запросы и live tailing из терминала.
- [otel-cli](https://github.com/equinix-labs/otel-cli) — отправка OTLP-спанов из терминала: обёртка `otel-cli exec` над командой и разовые спаны для проверки трейсинга.
- [sloth](https://github.com/slok/sloth) — генерация SLO и алертов из короткого описания.
- [pint](https://github.com/cloudflare/pint) — линтер правил Prometheus: PromQL, ссылки на метрики, дубли, контроль изменений в CI.
- [cloudprober](https://github.com/cloudprober/cloudprober) — активные пробы HTTP/PING/TCP/DNS.
- [canary-checker](https://github.com/flanksource/canary-checker) — health-check платформа с проверками из YAML.
- [krr](https://github.com/robusta-dev/krr) — рекомендации requests/limits по фактическому потреблению.
- [kula](https://github.com/c0m4r/kula) — лёгкий мониторинг Linux с web-UI и TUI: история метрик без Prometheus.
- [gdg](https://github.com/esnet/gdg) — бэкап и восстановление дашбордов, датасорсов и правил алертинга Grafana в git или S3.
- [promformat](https://github.com/facetoe/promformat) — форматтер PromQL: отступы и переносы без изменения смысла выражения.

### ai_tools

- [herdr](https://github.com/herdrdev/herdr) — TUI-оболочка для сессий и панелей coding-агентов.
- [rtk](https://github.com/rtk-ai/rtk) — прокси, который сжимает и фильтрует вывод перед отправкой в контекст LLM.
- [abtop](https://github.com/graykode/abtop) — монитор сессий coding-агентов: токены, контекст, лимиты и порты.
- [moli](https://github.com/lexmount/moli) — headless-браузер для агентов на Rust: Markdown, semantic tree и скриншоты, CDP, WebDriver Classic/BiDi.
- [ocr](https://github.com/alibaba/open-code-review) — AI-ревью по git-диффу через настраиваемый LLM-эндпоинт.
- [kaeru](https://github.com/LamantinAI/kaeru) — локальная память агентов на графе: два слоя, история утверждений и provenance, MCP по HTTP.
- [CloakBrowser](https://github.com/CloakHQ/CloakBrowser) — stealth-Chromium как drop-in замена Playwright/Puppeteer: патчи fingerprint на уровне исходников (нужен лицензионный ключ).
- [opencode-mem](https://github.com/tickernelz/opencode-mem) — локальная память для opencode: Turso/libSQL с векторным поиском, локальные эмбеддинги, авто-захват и web-UI.
- [mcpc](https://github.com/apify/mcpc) — CLI-клиент MCP: подключение к серверу и вызов его tools/resources из терминала без агента.
- [stealth-browser-mcp](https://github.com/vibheksoni/stealth-browser-mcp) — MCP-сервер браузера для AI-агентов: навигация, DOM и перехват сети через CDP.
- [Google Chrome](https://www.google.com/chrome/) — официальный .deb-пакет (нужен stealth-browser-mcp).
- [T3 Code](https://github.com/pingdotgg/t3code) — графический пульт к coding-агентам (desktop, web, мобильные клиенты).
- [Caprock](https://github.com/dspv/caprock) — наблюдение за сессиями coding-агентов: стоимость PR и сессий, лимиты плана, история и MCP для агентов.
- [Ouroboros](https://github.com/razzant/ouroboros) — AI-агент с десктопным приложением, CLI и web-интерфейсом.
- [Orca](https://github.com/stablyai/orca) — IDE для параллельной работы агентов: рабочие пространства воркеров, координатор, чат и терминал, удалённые машины и мобильный клиент.
- [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) — 83 навыка для bug bounty и red team: recon, классификация, триаж, отчёты (CLI `cbh` не ставится — пакета на PyPI нет).

### skills

- [skills CLI](https://github.com/vercel-labs/skills) — глобальные skills для opencode в `~/.agents/skills` (69 skills из 17 репозиториев).

### audio

- [PipeWire](https://gitlab.freedesktop.org/pipewire/pipewire) — звуковой сервер (пакеты `pipewire`, `pipewire-pulse`, `pipewire-bin`).
- [WirePlumber](https://gitlab.freedesktop.org/pipewire/wireplumber) — менеджер сессий PipeWire.
- [hicolor-icon-theme](https://www.freedesktop.org/wiki/Software/icon-theme/) — иконки для меню приложений.
- [HushMic](https://github.com/Fovty/HushMic) — шумоподавление микрофона в реальном времени (PipeWire).
- [Яндекс Музыка RS](https://github.com/SpolzerMod/yamusic-rs) — неофициальный клиент Яндекс Музыки на Rust/Slint вместо Electron (Linux-сборка в бете).

### craft

Офисные GUI-приложения ArtCraft (`storytold`) — чистые Rust/egui-редакторы.
Все три ставятся по умолчанию; выключаются флагами (см.
[раздел ниже](#офисные-приложения-artcraft-wordcraft-gridcraft-deckcraft)).

- [WordCraft](https://github.com/storytold/wordcraft) — документы: `.docx` (чтение/запись), `.doc` 97-2003 (чтение), `.odt`, `.rtf`, `.html`, `.md`, `.tex`, `.txt`; PDF на экспорт; `wordcraft-cli` для текста и конвертации.
- [GridCraft](https://github.com/storytold/gridcraft) — таблицы: `.xlsx` (родной формат), `.csv`/`.tsv`; чтение `.xls`, `.xlsb`, `.ods`; PDF на экспорт; `gridcraft-cli`.
- [DeckCraft](https://github.com/storytold/deckcraft) — презентации: `.pptx` (чтение/запись); PDF на экспорт; `deckcraft-cli`.

### markdown

- [Zettlr](https://github.com/Zettlr/Zettlr) — редактор Markdown для заметок и научных текстов: Zettelkasten, ссылки, цитаты, экспорт в PDF/LaTeX/DOCX.
- [MarkText](https://github.com/marktext/marktext) — минималистичный WYSIWYG-редактор Markdown в духе Typora.
- [TextFold](https://github.com/chenxiachan/textfold) — чтение статей, PDF и веб-страниц в пяти уровнях детализации: от карты тем до авторского текста.
- [pdf2md](https://github.com/fjacquet/pdf2md) — PDF в Markdown: заголовки, списки и таблицы, ONNX-layout detection и OCR для страниц-картинок.
- [pdfcli](https://crates.io/crates/pdfrs) — PDF ↔ Markdown и операции с PDF (merge/split/rotate/watermark) одним CLI на чистом Rust.

### hardware

- [smartmontools](https://www.smartmontools.org/) — `smartctl`/`smartd`: атрибуты SMART, self-test и лог ошибок накопителя.
- [nvme-cli](https://github.com/linux-nvme/nvme-cli) — телеметрия NVMe: износ, температура, число записанных байт, ошибки.
- [lm-sensors](https://github.com/lm-sensors/lm-sensors) — `sensors`: температуры, напряжения и обороты вентиляторов.
- [inxi](https://smxi.org/docs/inxi.htm) — сводка о железе и системе (`inxi -Fz`) для багрепортов и сравнения машин.
- [pciutils](https://mj.ucw.cz/sw/pciutils/) — `lspci`: устройства на шине PCI и их драйверы (`lspci -k`).
- [usbutils](http://www.linux-usb.org/) — `lsusb`: устройства USB и их VID:PID.
- [dmidecode](https://github.com/mirror/dmidecode) — инвентаризация из BIOS/SMBIOS: версия BIOS, слоты и тип памяти, серийные номера.
- [fwupd](https://github.com/fwupd/fwupd) — прошивки через `fwupdmgr`: `get-devices`, `refresh`, `update` (BIOS, SSD/NVMe, док-станции).
- [LACT](https://github.com/ilya-zlobintsev/LACT) — GUI и демон `lactd` для настройки и мониторинга GPU (AMD/Intel/NVIDIA).

### guardrails

- [guardrails-llm-filter](https://github.com/cloud-ru-tech/guardrails-llm-filter) — прокси, который маскирует PII и секреты на пути к LLM (systemd-юнит поверх Docker).
- [dcg (Destructive Command Guard)](https://github.com/Dicklesworthstone/destructive_command_guard) — блокировка `rm -rf`, `git reset --hard`, `push --force` до выполнения агентом. Плагин OpenCode ставится через `dcg install --opencode`.

### nora

- [NORA](https://github.com/getnora-io/nora) — artifact registry: кэш провайдеров Terraform и pull-through cache Docker-образов.
- [Caddy](https://github.com/caddyserver/caddy) — TLS-терминатор для NORA.
- [mkcert](https://github.com/FiloSottile/mkcert) — локальный CA и сертификаты.
- [libnss3-tools](https://github.com/nss-dev/nss) — `certutil` для доверия CA в NSS (Chrome, Firefox).
- [apache2-utils](https://httpd.apache.org/) — `htpasswd` для авторизации в реестре.

### opencode

- [opencode](https://github.com/sst/opencode) — AI-агент в терминале (из npm-реестра в `/usr/local/bin`).
- [AGENTS.md](https://github.com/patsevanton/ansible-for-ubuntu-devops-workstation/blob/main/roles/opencode/files/AGENTS.md) — глобальные инструкции для opencode в `~/.config/opencode/AGENTS.md`.

---

## Проверка стиля (ansible-lint)

Роль `base` ставит **ansible-lint** пакетом из репозитория Ubuntu — тот самый,
которым можно проверять этот плейбук:

```bash
ansible-lint                    # профиль production, конфиг .ansible-lint
```

Профиль `production` и список исключений заданы в `.ansible-lint` в корне
репозитория. Единственное исключение — `var-naming[no-role-prefix]`: роль
`binaries` вызывается другими ролями через `include_role` и принимает входную
переменную `binaries_to_install`, которая по правилу должна была бы нести
префикс вызывающей роли. Конфиг `.yamllint` в корне отключает длину строк (в
описаниях утилит она не помогает), но остаётся совместимым с требованиями
ansible-lint.

---

## CI и pre-commit

В `.github/workflows/lint.yml` одно задание:

- **lint** — `ansible-playbook --syntax-check playbook.yml`,
  `ansible-playbook --list-tasks` (роли и теги должны разбираться),
  `ansible-lint` и `yamllint`.

Полный плейбук в CI не запускается: он ставит GUI-приложения и systemd-юниты,
которым нужен настоящий ноутбук.

Те же проверки локально запускает `.pre-commit-config.yaml`. Хуки локальные
(`language: system`), потому что `ansible-lint`, `yamllint` и `ansible-core`
уже ставит роль `base` — версии не дублируются в pre-commit:

```bash
pre-commit install
pre-commit run --all-files
```

Рядом стоит **prek** — Rust-переписывание pre-commit: понимает тот же
`.pre-commit-config.yaml`, но запускает хуки параллельно и не поднимает
Python-окружение на каждый прогон. Ставится не вместо pre-commit, а для
сравнения на этом же конфиге:

```bash
prek run --all-files
prek install          # git-хуки через prek
```

---

## molecule — тестирование Ansible-ролей

Роль `base` ставит **molecule** (`ansible/molecule`) — фреймворк тестирования
ролей и плейбуков: прогоняет роль в поднятых инстансах (контейнеры, VM),
проверяет идемпотентность и гоняет verify-сценарии. Пакета в apt и релизных
бинарников нет — ставится из PyPI через **pipx** в изолированное окружение
(шим `molecule` — в `~/.local/bin`).

Вместе с ним ставятся:

- **molecule-plugins** с extra `docker` — драйверы сценариев; драйвер `docker`
  гоняет тесты в контейнерах Docker (Engine ставится ролью `docker`).
  Коллекции **community.docker** и **ansible.posix**, которыми драйвер
  поднимает контейнеры, плейбук не ставит: molecule доставит их сама в
  `~/.ansible/collections` при первом `molecule test` (`molecule dependency`).

```bash
molecule drivers                # доступные драйверы: docker, podman, vagrant, ...
molecule init scenario          # каркас сценария ./molecule/default
molecule test                   # прогнать сценарий целиком
molecule converge               # только применить роль
molecule idempotence            # второй прогон — ничего не должен менять
```

Сценарий создаётся в `molecule/<имя>/` внутри каталога роли: `molecule.yml`
(настройки), `converge.yml` (применение роли), `verify.yml` (проверки).
Драйвер задаётся в `molecule.yml` (`driver: name: docker` + `platforms:` с
образами); без явного драйвера используется `default` — инстансы вы поднимаете
сами, а molecule оркестрирует последовательность теста
(`dependency → create → converge → idempotence → verify → destroy`).

---

## Обновление и идемпотентность

Идемпотентность по умолчанию простая: **нет файла — ставим, есть файл — не трогаем.**
Обновление бинарников — отдельный явный режим, см. ниже.

### Отчёт о версиях

В конце каждого прогона плейбук пишет `report.json` в
`~/.local/state/devops-playbook/` (каталог не в репозитории и не в git):

- версии всех проверенных утилит и наличие бинарников без флага версии;
- state бинарников `name → tag` (секция `binaries`);
- хост, дистрибутив, ядро, commit плейбука, теги запуска и признак `full_run`.

```bash
jq -r '.tools[] | select(.ok == false) | .command' ~/.local/state/devops-playbook/report.json
```

При частичном прогоне `full_run` равен `false`, а отсутствующие утилиты
попадут в отчёт с `"ok": false`.

### Обновление бинарников

Обычный прогон ничего не обновляет: если файл уже есть, роль `binaries` его
не трогает. Явный режим обновления:

```bash
ansible-playbook -K playbook.yml -e app_update=true
```

В этом режиме роль проверяет весь список (а не только отсутствующие файлы),
берёт актуальный тег из `releases/latest` и переустанавливает бинарник только
если тег отличается от записанного в state.

Флаг `app_update` объявлен в `group_vars/all.yml` (значение по
умолчанию — `false`), а не в defaults роли `binaries`: его читают и роли,
которые `binaries` не вызывают (`opencode`). Defaults роли, подключённой через
`include_role`, видны только её собственным задачам.

Роль `opencode` работает в том же режиме, хотя ставится из npm-реестра:
версию из реестра она сравнивает с выводом `opencode --version` (без state).

State лежит в `~/.local/state/devops-playbook/binaries.json` в виде
`name → tag` и пишется сразу после установки. В `report.json` он попадает
копией, секцией `binaries`:

```json
{
  "yq": "v4.45.1",
  "kubectl": "v1.34.1",
  "helm": "v3.19.0"
}
```

Первый запуск с `app_update=true` после появления state-файла
переустановит всё: роль ещё не знает, какие теги стоят на диске. Дальше
скачиваются только отличия. Проверка идёт через HTTP-редиректы
`github.com/<repo>/releases/latest`, а не через GitHub API, поэтому лимит
60 запросов в час не расходуется.

`EvoMaster` и `Jazzer` ставятся не через роль `binaries`, поэтому
`app_update` их не обновляет: удалите `evomaster`/`jazzer` из
`/usr/local/bin` и прогоните плейбук снова. То же с `pdfcli` (роль
`cargo_apps`, `cargo install pdfrs`): обновление — удалить
`/usr/local/bin/pdfcli` и запустить плейбук.

### Обновление pipx и npm

Повторный прогон плейбука не обновляет приложения из pipx и `tldr` из npm:
роль `pipx_apps` пропускает пакет, если шим уже есть, а `tldr` ставится через
npm только при отсутствии бинарника. `app_update` их тоже не трогает: они
ставятся не из GitHub-релизов. `opencode` качается из npm-реестра напрямую, не
через npm CLI, но `app_update=true` его обновляет: роль сравнивает версию
из реестра с выводом `opencode --version` и переустанавливает бинарник только
при отличии (state-файл ей не нужен).

```bash
pipx upgrade-all
sudo npm update -g
```

#### Если opencode ставили через npm

`npm install -g @opencode/cli` кладёт в `/usr/local/bin/opencode` симлинк на
`node_modules`, и плейбук с ним конфликтует: `copy` пишет в цель симлинка, то
есть внутрь npm-пакета. Поэтому npm-установку снимают до прогона роли — путь
`/usr/local/bin/opencode` должен быть свободен:

```bash
sudo npm uninstall -g @opencode/cli
```

Старый пакет v1 `opencode-ai` ставится тем же npm, живёт отдельно от
`@opencode/cli` и занимает ещё несколько сотен мегабайт — его тоже удаляют
вручную, плейбук о нём не знает:

```bash
sudo npm uninstall -g opencode-ai
```

Дальше роль ставит актуальную версию сама:
`ansible-playbook -K playbook.yml -e app_update=true --tags opencode`.

---

## Docker и Compose

Ставится **только Compose V2** — плагин `docker-compose-plugin`, команда `docker compose`.

Ключ репозитория кладётся как ASCII-armored `.asc` в `/etc/apt/keyrings/docker.asc`
и подключается через `signed-by`, поэтому **`gnupg` не требуется**.

Про старый Compose V1:

- V1 снят с поддержки с июля 2023; в Ubuntu 26.04 пакета `docker-compose` нет,
  а бинарники и тег `v1.29.2` с GitHub удалены — официально поставить его нечем.
- Файлы `docker-compose.yaml` формата `version: "2"` / `version: "3"` работают
  в `docker compose` (ключ `version` игнорируется с предупреждением).
- Легаси-формат v1 (нет ключа `version:`, сервисы в корне файла) не поддерживается —
  нужно один раз обернуть сервисы в `services:`:

```yaml
# было (легаси v1)
web:
  image: nginx

# стало
services:
  web:
    image: nginx
```

Проверка: `docker compose version`.

Для повседневной работы роль `docker` дополнительно ставит **dry**
(`moncho/dry`) — терминальный менеджер контейнеров, образов, сетей и томов с
мониторингом и поддержкой нескольких Docker-хостов:

```bash
dry                         # интерактивный TUI текущего Docker-хоста
dry -H ssh://user@host      # подключиться к удалённому Docker
```

### mint — уменьшение готового образа

`mint` — новое имя проекта DockerSlim/SlimToolkit. Уменьшает **уже собранный**
образ: запускает контейнер, записывает, какие файлы реально читаются при старте
и работе, и собирает новый образ без остальных. Dockerfile не меняется, нужен
запущенный Docker.

```bash
mint slim --target myapp:latest --tag myapp:mint   # новый образ
mint xray --target myapp:latest                    # что лежит внутри
mint images                                        # образы на хосте
```

Результат проверять руками: `docker run --rm myapp:mint`, затем `dive myapp:mint`.
Для CI надёжнее multi-stage build: `mint` полезен, когда образ уже собран и
надо понять, почему он весит гигабайт. Профиль снимается по реальному
поведению, поэтому сервис должен подняться и ответить на пробу.

### daemon.json

Роль `docker` — единственный владелец `/etc/docker/daemon.json` (роль `nora`
только выставляет `docker_registry_mirrors`, а файл рендерит `docker`). Что
в нём лежит:

- `log-driver: json-file` с `max-size: 20m` и `max-file: 3` — логи контейнеров
  не растут бесконечно. Без этих опций Docker не ротирует `json-file` вообще,
  и `/var/lib/docker/containers` однажды занимает весь диск.
- `live-restore: true` — при перезапуске демона (обновление пакета, правка
  конфига) контейнеры продолжают работать.
- `registry-mirrors` — если роль `nora` отработала, все `docker pull` идут
  через её pull-through cache.

Пулы адресов (`default-address-pools`) по умолчанию не задаются: стандартный
`172.17.0.0/16` обычно никому не мешает. Если он конфликтует с VPN или
подсетями кластеров, задайте `docker_address_pools` в
`roles/docker/defaults/main.yml` или `group_vars`. Не используйте
`100.64.0.0/10` — этот диапазон занимает NetBird.

Проверка и применение:

```bash
docker info --format '{{.LoggingDriver}}'
docker inspect <container> --format '{{.HostConfig.LogConfig}}'
sudo systemctl restart docker
```

---

## Лимиты inotify

Роль `base` кладёт `/etc/sysctl.d/99-devops-inotify.conf`:

```ini
fs.inotify.max_user_watches = 524288
fs.inotify.max_user_instances = 512
fs.inotify.max_queued_events = 32768
```

Дефолт Ubuntu — 65536 watches, 128 instances и 16384 queued events. Для
kind, k9s, IDE и file watchers в проектах этого мало: watcher'ы начинают
молча отваливаться, а в логах появляется «No space left on device» (место на
диске при этом есть). Файл применяется через `sysctl -p` только при
изменении, в `--check` не применяется.

```bash
sysctl fs.inotify.max_user_watches fs.inotify.max_user_instances
```

---

## NetBird

Роль `network` подключает официальный apt-репозиторий
`https://pkgs.netbird.io/debian` и ставит `netbird` (CLI + демон) и
`netbird-ui` (GUI на GTK4/WebKit). Это не PPA: у NetBird своего PPA нет,
апстрим публикует ключ и пакеты в собственном репозитории. Ключ лежит как
ASCII-armored `.asc`, поэтому `gnupg` не нужен.

Демон включается и запускается, но регистрация остаётся ручной: SSO
открывается в браузере, а setup-key — секрет, которому не место в плейбуке.

```bash
netbird status                  # состояние демона и подключения
netbird up                      # вход через SSO в браузере
netbird up --setup-key <KEY>    # регистрация без браузера
netbird-ui                      # графический клиент
```

---

## guardrails-llm-filter (LLM PII/secret masking proxy)

Роль `guardrails` ставит systemd-юнит, который запускает Docker-контейнер
`ghcr.io/cloud-ru-tech/guardrails-llm-filter:latest` — прокси, маскирующий PII и
секреты в запросах к LLM.

Юнит: `/etc/systemd/system/guardrails-llm-filter.service` (кладётся из шаблона
`roles/guardrails/templates/guardrails-llm-filter.service.j2`).

Что делает юнит:

- зависит от `docker.service` (`After`/`Requires`) — поднимается после Docker;
- перед запуском снимает старый контейнер (`docker rm -f guardrails`);
- запускает контейнер с пробросом портов **только на loopback**:
  `127.0.0.1:8080` (прокси) и `127.0.0.1:9080` (config API и веб-консоль);
- включает аудит запросов (`GUARDRAILS_AUDIT_ENABLED=true`);
- пересылает запросы на `GUARDRAILS_UPSTREAM_BASE_URL=https://proxy.nosize.me`;
- при старте применяет политику правил детекции (`ExecStartPost` →
  `/usr/local/sbin/guardrails-apply-policy`) — выключает правила из
  `guardrails_disabled_rules`;
- `Restart=always` — контейнер поднимается автоматически после сбоя или перезагрузки.

Настройки (порты, upstream, аудит, образ) задаются в
`roles/guardrails/defaults/main.yml`.

Upstream у контейнера один, поэтому прокси обслуживает одного провайдера —
`nosize`. В `~/.config/opencode/opencode.jsonc` у провайдера `nosize` стоит
`baseURL: http://127.0.0.1:8080/v1`, и его запросы идут через маскирование.
Блок `polza` в том же файле закомментирован: через guardrails она больше не
ходит, а без прокси её трафик не маскировался бы. Второй провайдер требует
второго инстанса прокси — свой порт, свой `GUARDRAILS_UPSTREAM_BASE_URL` и
свой `baseURL` в конфиге opencode.

Политика правил тоже живёт в `roles/guardrails/defaults/main.yml`
(`guardrails_disabled_rules`): по умолчанию выключена маскировка IPv4
(правила `ip-addrs.ipv4*`, IPv6-правила остаются включёнными). Хранилище
guardrails — `in_memory`, поэтому правки через веб-консоль не переживают
рестарт контейнера: политика применяется скриптом при каждом старте сервиса и
синхронизируется при каждом прогоне плейбука. Правила вне списка плейбук не
трогает — их по-прежнему можно выключать в веб-консоли, но они вернутся к
дефолту после рестарта. Чтобы вернуть маскировку IPv4 — убрать правила из
`guardrails_disabled_rules` и перезапустить сервис.

Чтобы видеть **настоящие** креды рядом с **фейковыми** (плейсхолдерами),
включено хранение текстов в аудите (страница «Журнал аудита» в консоли на
`http://127.0.0.1:9080`):

- `GUARDRAILS_AUDIT_STORE_ORIGINAL_TEXTS=plain` — оригинал за плейсхолдером,
  в UI показывается по наведению;
- `GUARDRAILS_AUDIT_STORE_MASKED_TEXTS=true` — маскированный текст запроса;
- `GUARDRAILS_AUDIT_STORE_MASKED_RESPONSE_TEXTS=true` — маскированный текст
  ответа модели.

Значения задаются в `roles/guardrails/defaults/main.yml`
(`guardrails_audit_store_*`) и применяются при следующем старте сервиса.
Без них записи аудита показывают только правило и плейсхолдер, а поле
`original` остаётся пустым.

⚠️ `original_texts=plain` хранит сырые чувствительные данные в памяти
контейнера (`in_memory`, до 24h, до 10000 записей), а config API и консоль не
имеют аутентификации (слушают только loopback). Для шифрования — значение
`encrypted` плюс `GUARDRAILS_STORE_ENCRYPTION_ENABLED=true` и
`GUARDRAILS_STORE_ENCRYPTION_KEY` (см. SECURITY.md upstream-проекта).

Для живой проверки — страница «Песочница» в консоли: вставляете текст и
видите, что ушло модели (замаскировано) и что вернётся клиенту (оригиналы).

Проверка и управление:

```bash
systemctl status guardrails-llm-filter
systemctl restart guardrails-llm-filter
journalctl -u guardrails-llm-filter -f
docker ps --filter name=guardrails
curl -s http://127.0.0.1:9080/    # веб-консоль и config API
curl -s "http://127.0.0.1:9080/v1/audit/records?limit=1"  # аудит: плейсхолдеры и оригиналы
curl -s http://127.0.0.1:8080/v1/models \
  -H "Authorization: Bearer $NOSIZE_API_KEY"   # прокси видит nosize
```

Юнит кладётся из шаблона, поэтому правки в
`/etc/systemd/system/guardrails-llm-filter.service` перезапишутся при следующем
запуске: меняйте шаблон или переменные роли. Изменение файла автоматически
делает `daemon-reload` и перезапускает сервис (образ перетянется — тег `latest`
мог обновиться). Обновить образ вручную:

```bash
docker pull ghcr.io/cloud-ru-tech/guardrails-llm-filter:latest
sudo systemctl restart guardrails-llm-filter
```

---

## NORA artifact registry + локальный TLS (mkcert)

Роль `nora` ставит **NORA** (`getnora-io/nora`) — self-hosted мультиформатный
artifact registry (Docker, npm, PyPI, Cargo, Go, Maven и др.), выписывает для
него **локальный доверенный сертификат** через **mkcert** и автоматически
добавляет этот CA в trust-сторы клиентов. TLS терминирует **Caddy**.

Что делает роль:

1. Ставит и обновляет `nora-amd64.deb` из GitHub-релиза ролью `github_deb`:
   версия из `releases/latest` сверяется с установленной в `dpkg`, при смене
   версии сервис перезапускается. systemd-юнит, пользователь `nora` и каталоги
   данных приходят из пакета; конфиг — `/etc/nora/nora.env` (из шаблона),
   данные — `/var/lib/nora`.
2. Ставит `mkcert` + `libnss3-tools`, запускает `mkcert -install` — локальный
   CA ложится в системный store и NSS-сторы браузеров. CA-материал — в
   `~/.local/share/mkcert` (`mkcert -CAROOT`), ключ не раздаётся и не коммитится.
3. Выписывает листовой серт под домен реестра
   (`registry.nora.lan`, `localhost`, `127.0.0.1`) в
   `/etc/nora/tls/nora.crt` + `nora.key` (ключ — `600 root:root`).
4. Раздаёт `rootCA.pem` клиентам: системный store
   (`/usr/local/share/ca-certificates/nora-ca.crt` + `update-ca-certificates` —
   для curl/git/apt/go/rustls), Docker (`/etc/docker/certs.d/registry.nora.lan/ca.crt`),
   npm (`cafile` в `~/.npmrc`), pip (пакет `truststore`), Java
   (`keytool -importcert` в системный `cacerts` — Maven/Gradle).
5. Ставит Caddy как TLS-терминатор: `registry.nora.lan:443` → `127.0.0.1:4000`
   (HTTP).
6. Прописывает `registry.nora.lan` в `/etc/hosts` на `127.0.0.1`.
7. Отдаёт локальные сервисы по именам `<сервис>.lan` через тот же Caddy
   (`:80` → loopback-порт сервиса), см. раздел ниже.

Серты и ключи в репозиторий плейбука не кладутся (генерируются на месте).
Домен не использует `.local` (конфликт с mDNS).

Проверка после установки:

```bash
curl -fsS https://registry.nora.lan/health        # без -k, серт доверенный
docker pull registry.nora.lan/myapp:1             # CA подхвачен из certs.d
openssl s_client -connect registry.nora.lan:443 -showcerts  # цепочка → rootCA mkcert
```

UI — `https://registry.nora.lan/ui/`. Порты: NORA слушает `0.0.0.0:4000`,
Caddy — `:443`.

### Локальные имена сервисов (`<сервис>.lan`)

Тот же Caddy — единственная точка входа на loopback, поэтому у локальных
сервисов тоже есть имена без портов:

- [textfold.lan](http://textfold.lan) — TextFold;
- [guardrails.lan](http://guardrails.lan) — веб-консоль guardrails;
- `opencode-mem.lan` — web UI opencode-mem; адрес с правкой —
  [http://127.0.0.1:4747](http://127.0.0.1:4747).

HTTPS для них не нужен — браузер ходит по HTTP, серт остаётся только у NORA.

Как это работает: Caddy слушает `:80` и по имени хоста проксирует на
loopback-порт сервиса, а имена резолвятся через `/etc/hosts` на `127.0.0.1`.
Список — `local_http_sites` в `roles/nora/defaults/main.yml` (`host` плюс
`upstream`). Добавить сервис — одна строка и прогон
`ansible-playbook -K playbook.yml --tags nora`: имя появится в hosts, Caddy
перезапустится.

TextFold и opencode-mem пускают только запросы, адресованные loopback-имени, и
отбивают `POST` с чужим `Origin` — так они защищаются от DNS rebinding и CSRF.
Поэтому у этих двух сайтов стоит `loopback_guard: true`: Caddy подменяет `Host`
на адрес upstream (`127.0.0.1:<порт>`), а `Origin` — только если он совпадает с
именем сайта. Запрос со страницы с другого сайта уходит со своим `Origin` и
получает от приложения прежний `403`, то есть защита не ослабляется.

У `opencode-mem` остаётся ограничение: правка из web UI по имени `.lan`
отключена — сама страница проверяет `location.hostname` и разрешает
изменения только на `localhost`/`127.0.0.1`. Чтение по имени `.lan` работает;
чтобы редактировать и оттуда, задайте `webServerAuthPassword` в
`~/.config/opencode/opencode-mem.jsonc` (basic auth).

Порты в списке продублированы намеренно: роль `nora` идёт первой, defaults
ролей `markdown`/`guardrails`/`ai_tools` к этому моменту ещё не загружены.
Меняете порт в роли сервиса — поправьте `upstream`.

Ограничения: имена работают только на этой машине (своего DNS нет), а
удалённое из списка имя остаётся в `/etc/hosts` — строку надо убрать вручную.

### Зеркала провайдеров Terraform

Роль кладёт `~/.terraformrc` с **одним** блоком `provider_installation` (второй
Terraform не разрешает): `network_mirror` на NORA, внешние зеркала и `direct` с
`exclude` для публичного реестра. Дополнительные зеркала — `nora_tf_mirrors`,
запреты на прямое скачивание — `nora_tf_direct_exclude` в
`roles/nora/defaults/main.yml`. По умолчанию:

- NORA — весь публичный реестр, включая `registry.terraform.io/hashicorp/*`;
- `terraform-mirror.yandexcloud.net` — только `registry.terraform.io/yandex-cloud/*`;
- `storage.mwsapis.ru/mws-terraform` — `mws-cloud/*` из terraform- и opentofu-реестров.

`hashicorp/*` намеренно не отдан зеркалу YC: если провайдер подходит под два
зеркала, Terraform опрашивает оба и берёт самую новую версию — источник
становится недетерминированным, а NORA перестаёт быть источником для
`hashicorp`.

Отдача из кэша при недоступном upstream требует NORA 1.4.6+ (исправлен
[getnora-io/nora#1230](https://github.com/getnora-io/nora/issues/1230)):
закэшированные метаданные отдаются после одного запроса к upstream
(`NORA_TF_REVALIDATE_TIMEOUT`, по умолчанию 5 с) с `X-Nora-Stale: true`, а не
после 2× `NORA_TF_PROXY_TIMEOUT`. Поэтому `terraform init` на тёплом кэше
укладывается в таймаут Terraform.

Цена решения: метаданные NORA получает через registry API, а бинарники
провайдеров лежат на `releases.hashicorp.com`, и с российского IP он отдаёт 404
со страницей «Content not available in your region». NORA ретранслирует это
клиенту как 404, в её логе — `upstream returned a policy/geo block ... reason
"geo"`. Поэтому холодный кэш по `hashicorp` прогревают при рабочем маршруте к
`releases.hashicorp.com` (прокси/VPN, либо при выключенном netbird): обычный
`terraform init` в нужных проектах. Дальше эти версии NORA отдаёт из кэша без
сети. Для чужих платформ — `terraform providers lock -platform=linux_amd64
-platform=darwin_arm64`.

В NORA эти зеркала не прописываются: у NORA один upstream (`NORA_TF_PROXY`) и он
говорит по registry API, а это статические network mirror. Провайдеров
`mws-cloud` в публичных реестрах нет, поэтому MWS-зеркало — единственный источник
для них.

Внешние зеркала (YC и MWS) отдают `index.json` без `hashes`, поэтому `terraform init`
предупреждает про «Incomplete lock file information»: checksums считаются
локально под текущую платформу. Для мультиплатформенного лока —
`terraform providers lock -platform=linux_amd64 -platform=darwin_arm64`.

### Авторизация NORA

По умолчанию включена (`NORA_AUTH_ENABLED=true`). Пользователи — htpasswd-файл
(`apache2-utils`, bcrypt), программный доступ — API-токены. Создать
пользователя и токен:

```bash
sudo htpasswd -Bc /etc/nora/users.htpasswd admin   # первый пользователь
# токен (показывается один раз):
curl -k -X POST https://registry.nora.lan/api/tokens \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"...","role":"write","ttl_days":90}'
# docker login с токеном (токен — как пароль):
docker login registry.nora.lan -u token -p nra_...
```

Пока htpasswd-файл не создан, логиниться нельзя (реестр просто без
пользователей). Всё настраивается в `roles/nora/defaults/main.yml`
(`nora_auth_enabled`, `nora_auth_anonymous_read`, `nora_hostname`,
`nora_public_url`, `nora_tls_*`), там же флаги `nora_docker_configure` /
`nora_npm_configure` / `nora_pip_configure` / `nora_java_configure`, если
какой-то trust-store клиента не нужен.

### Обновление NORA и авторотация серта

NORA обновляется той же ролью `github_deb`, что и остальные `.deb` из
GitHub-релизов: обычный прогон плейбука сравнивает версию из `releases/latest`
с установленной в `dpkg` и ставит пакет только если релиз новее.
`-e app_update=true` для NORA не нужен — этот флаг относится к бинарникам
(роль `binaries`) и `opencode`. После смены версии роль перезапускает
`nora.service`, потому что обновление файлов пакета не меняет уже запущенный
процесс.

mkcert сам серты не продлевает. Серт выписывается ролью только при отсутствии
`/etc/nora/tls/nora.crt`; чтобы перевыпустить — удалите его и запустите плейбук
снова. Для автоматической ротации в продакшене используйте `step-ca` с ACME
или Let's Encrypt + Caddy — тогда локальный CA не нужен.

---

## Git, GitLab CI и обзор репозиториев

Роль `git` дополнительно ставит:

- **glci** (`github gitlab-org/ci-cd/runner-tools/glci`) — запуск GitLab CI/CD
  пайплайнов локально. Парсит `.gitlab-ci.yml`, поднимает mock GitLab API и
  `gitlab-runner` в контейнерах и выполняет джобы в Docker. Требуется локальный
  Docker (или Podman). Бинарник `glci` лежит в GitLab Generic Packages, поэтому
  версия берётся из редиректа permalink, а файл скачивается по API-пути.
- **pre-commit** (`pre-commit/pre-commit`) — фреймворк git-хуков. Ставится
  самодостаточным `.pyz`-zipapp (со shebang `python3`) прямо в
  `/usr/local/bin/pre-commit`, без pip и virtualenv.
- **reposcan** (`mabd-dev/reposcan`) — быстрый поиск git-репозиториев с
  незакоммиченными/незапушенными изменениями по файловой системе.
- **wt** (worktrunk, `max-sixty/worktrunk`) — параллельные ветки в отдельных
  каталогах через git worktree: переключение без пересборки рабочего дерева,
  список worktree, удаление отработанных.

```bash
pre-commit install          # включить хуки в текущем репозитории
reposcan ~/src              # показать «грязные» репозитории
glci run                    # прогнать пайплайн локально
wt switch --create feature  # новая ветка в отдельном worktree
wt list                     # все worktree и их состояние
```

---

## Jira и Confluence: jira-cli, jiratui и mcp-atlassian

Роль `atlassian` ставит три клиента: `jira-cli` — бинарником из
GitHub-релиза, `jiratui` и `mcp-atlassian` — через `pipx` (на PyPI
бинарников нет). Первые два работают руками в терминале, третий — MCP-сервер,
через который задачи и страницы читает и правит AI-клиент (opencode). Все три
ходят в обычный REST API, поэтому работают и с Jira Cloud, и с on-prem Jira
Server/Data Center; различается только способ токена:

- **Cloud** — API-токен с `id.atlassian.com/manage-profile/security/api-tokens`
  плюс email в конфиге.
- **Server/DC** — Personal Access Token из профиля Jira (Jira ≥ 8.14, админ
  должен включить `jira.pat.enabled`); в `jira-cli` для него нужен
  `JIRA_AUTH_TYPE=bearer`, в `jiratui` — `use_bearer_authentication: true`.
  Если PAT выключен политикой, остаются basic-пароль (обычно уже запрещён)
  или mTLS с клиентским сертификатом.

Плейбук ставит только бинарники. Конфиг и токен создаются вручную, чтобы
секрет не попал в репозиторий:

```bash
export JIRA_API_TOKEN='<API-токен или PAT>'   # токен — только в переменную
export JIRA_AUTH_TYPE=bearer                  # нужен для DC/Server (PAT)
jira init                                     # мастер: URL, логин, проект
jira me                                       # проверка авторизации
```

`jiratui` читает `~/.config/jiratui/config.yaml` (`jiratui configure create`
запускает мастер). Для on-prem в нём нужны `cloud: false`,
`use_bearer_authentication: true` и, если TLS перевыпускается корпоративным
CA, путь к нему в `ssl.ca_bundle`. При `cloud: false` версия API всегда v2,
ключ `jira_api_version` игнорируется.

Чтение тикетов — то, ради чего оба клиента и нужны:

```bash
jira issue list --plain                             # задачи проекта из конфига
jira issue list -q "project = PROJ AND status != Done" --raw
jira issue view PROJ-1 --comments 5
jiratui issues search --key PROJ-1
jiratui issues search --project-key PROJ
jiratui ui
```

Если конфиг пишется руками, а не мастером, у `jira-cli` 1.7.0 есть две
ловушки: `installation` должно быть ровно `Local` (с `Cloud` и любым
незнакомым значением клиент идёт в `/rest/api/3/search/jql`, которого у Jira
Server нет), а `project` — вложенный (`project: {key: PROJ}`); плоское
`project: PROJ` молча игнорируется и запрос уходит с `project=""`.

`jira-cli` и `jiratui` умеют и запись (`jira issue create/edit/move/delete`,
комментарии, `jiratui comments add`), но на рабочей станции включён режим
только чтения: запись не используется. Ограничить её токеном нельзя — у PAT
в Jira Server нет scope, он наследует все права пользователя. Запись
отсекается только на стороне клиента (`--read-only` у `mcp-atlassian`;
`jira-cli` и `jiratui` при желании писать смогут). `jira-cli` поддерживает
ещё mTLS (`auth_type: mtls`: CA, клиентский ключ и сертификат) — вариант для
контура, где PAT выключен, а клиентские сертификаты выдаются.

### Confluence: PAT недоступен

Confluence не подключён: PAT в инсталляции выключен администратором
(`/users/viewmypat.action` отдаёт «Страница не найдена»), других способов
авторизации нет. Поэтому `mcp-atlassian` регистрирует только инструменты
`jira_*`, а отдельных Confluence-клиентов плейбук не ставит. Если PAT
включат, достаточно вписать `CONFLUENCE_PERSONAL_TOKEN` в
`~/.config/atlassian.env` — больше ничего менять не нужно.

### mcp-atlassian — Jira и Confluence из opencode

`mcp-atlassian` — не интерактивная утилита, а MCP-сервер по stdio: клиент сам
запускает процесс и получает его инструменты (`jira_search`, `jira_get_issue`,
`confluence_search`, `confluence_get_page`; при выключенном read-only —
создание и правка задач и страниц). В этом контуре Confluence не подключён,
поэтому в `tools/list` приходят только `jira_*` — 37 читающих инструментов.
В терминале сервер проверяется одной командой, а работа идёт из агента:

```bash
mcp-atlassian --version
mcp-atlassian --help        # транспорт (stdio/HTTP), OAuth, SSL-флаги
```

Сервер регистрируется в `~/.config/opencode/opencode.jsonc`. Он запускается с
`--read-only`: сервер убирает write-инструменты из `tools/list`, поэтому
создать, изменить или удалить задачу и страницу из агента нельзя. URL и токен
в файле не хранятся — подставляются из env через `{env:...}`:

```jsonc
{
  "mcp": {
    "servers": {
      "atlassian": {
        "type": "local",
        "command": ["mcp-atlassian", "--read-only"],
        "environment": {
          "JIRA_URL": "{env:JIRA_URL}",
          "JIRA_PERSONAL_TOKEN": "{env:JIRA_PERSONAL_TOKEN}",
          "CONFLUENCE_URL": "{env:CONFLUENCE_URL}",
          "CONFLUENCE_PERSONAL_TOKEN": "{env:CONFLUENCE_PERSONAL_TOKEN}"
        }
      }
    }
  }
}
```

Для Cloud вместо `*_PERSONAL_TOKEN` — `JIRA_USERNAME` + `JIRA_API_TOKEN` и
`CONFLUENCE_USERNAME` + `CONFLUENCE_API_TOKEN`. Пару URL/токен тоже можно
отдать флагами (`--jira-url`, `--jira-personal-token`), но тогда токен попадёт
в историю шелла. Проверка подключения — `opencode mcp list`: у сервера должно
быть `connected`.

Что учесть при self-hosted:

- Версии: Jira Server/DC ≥ 8.14, Confluence Server/DC ≥ 6.0; PAT должен быть
  включён администратором (`jira.pat.enabled`). Если PAT выключен, у сервера
  есть mTLS — `JIRA_CLIENT_CERT`/`JIRA_CLIENT_KEY` (запароленный ключ не
  поддерживается, расшифровать заранее).
- Только Cloud: `jira_batch_get_changelogs`, `jira_move_issue`,
  `jira_get_issue_proforma_forms`, `confluence_get_page_views`,
  `confluence_check_content_permissions`, `confluence_get_space_permissions`.
  На Server/DC первые два вообще не появляются в списке инструментов.
- Сертификат внутреннего CA вне системного trust store — `JIRA_SSL_VERIFY=false`
  и/или `CONFLUENCE_SSL_VERIFY=false`; сертификаты из системного хранилища
  подхватываются автоматически.
- Кастомные поля на Server/DC имеют другие id, чем на Cloud, — искать через
  `jira_search_fields`.

---

## Flux GitOps без кластера (flate, flux-tools)

Роль `kubernetes` ставит два инструмента для офлайн-рендера и диффа Flux
GitOps-репозитория — без кластера, `kubectl` и внешних `helm`/`kustomize`
(библиотеки встроены в бинарник):

- **flate** (`home-operations/flate`) — Go-переписывание `flux-local`: рендерит
  и диффит GitOps-репозиторий, умеет режим «только изменённое поддерево».
- **flux-tools** (`alexandervidyaev/flux-tools`) — независимая реализация:
  собирает каждую Kustomization, шаблонит каждый HelmRelease, строит unified diff.

```bash
flate build --path ./kubernetes
flate diff  --path ./kubernetes --path-orig ../baseline/kubernetes
flux-tools test  clusters/prod --enable-helm
flux-tools build clusters/prod --enable-helm
```

---

## Инструменты для манифестов Kubernetes (cty, diffyml, kubectl-k8i, kubespy)

Роль `kubernetes` дополнительно ставит:

- **cty** (`Skarlso/crd-to-sample-yaml`) — генерирует sample-YAML из
  определения CRD, валидирует sample против схемы CRD и проверяет схему на
  breaking changes между версиями. Удобен для unit-тестов CRD-схем в CI.
- **diffyml** (`szhekpisov/diffyml`) — быстрый структурный дифф YAML с учётом
  специфики Kubernetes (понимает порядок полей, списки, аннотации), умеет
  выдавать аннотации для GitHub/GitLab/Gitea CI.
- **kubectl-k8i** (`ViktorUJ/kubectl-k8i`) — плагин kubectl: таблица ресурсов
  нод (поды, CPU, память, проценты загрузки с цветовой индикацией), метаданные
  (EC2, зона, nodepool), определение автоскейлера (Karpenter/CAS/Spot.io),
  анализ workload'ов. Ставится как `kubectl-k8i`, поэтому доступен и как
  `kubectl k8i`.
- **kubespy** (`pulumi/kubespy`) — наблюдение за изменениями ресурсов
  Kubernetes в реальном времени: `trace` собирает высокоуровневую сводку
  разворачивания, `status` показывает диффы `.status`.

```bash
cty generate -c my-crd.yaml -o sample.yaml     # sample-YAML из CRD
cty validate sample -c my-crd.yaml -s sample.yaml
diffyml old.yaml new.yaml                      # структурный дифф
kubectl k8i nodes                              # ресурсы нод
kubespy trace deployment nginx                 # наблюдение за rollout
```

---

## KubeDiagrams — схемы Kubernetes из манифестов и Helm

Роль `kubernetes` ставит **KubeDiagrams** (`philippemerle/KubeDiagrams`) из
PyPI в изолированное окружение pipx. Команд три:

- `kube-diagrams` — схема из файлов манифестов, каталога или kustomize;
- `helm-diagrams` — схема Helm-чарта (принимает флаги `helm template`);
- `kubectl diagrams` — схема по состоянию кластера из текущего контекста.

В отличие от `kubectl-tree` (текстовое дерево владельцев) это картинка:
иконки Kubernetes, группировка по namespace и связи между ресурсами. Рендер
идёт через `dot` из graphviz — роль ставит его пакетом apt, как и `iac` для
схем Terraform.

```bash
kube-diagrams deploy.yaml -o deploy.png        # один манифест
kube-diagrams ./manifests -f svg -o app.svg    # каталог, формат svg
helm-diagrams ./chart -o chart.png             # Helm-чарт
kubectl diagrams pod,service -n demo -o demo.png
```

Форматы: png (по умолчанию), svg, pdf, dot, а с 0.9.0 ещё mermaid, d2 и
dot_json. Веб-приложение и интерактивный просмотр в плейбук не входят:
ставятся только CLI-команды.

---

## Обзор кластера: kubecolor, kube-capacity, ktop, kubefetch

Роль `kubernetes` дополнительно ставит утилиты, с которыми кластер понятнее
«на глаз»:

- **kubecolor** (`kubecolor/kubecolor`) — цветной, читаемый вывод kubectl:
  подсвечивает ресурсы, диффы, логи и ошибки. Это обёртка над kubectl, но
  вызывается отдельной командой: алиасы на `kubectl` не навешиваем, сам
  `kubectl` остаётся как есть.
- **kube-capacity** (`robscott/kube-capacity`) — таблица ресурсов кластера:
  requests/limits CPU и памяти по нодам (и подам/контейнерам с флагами `-p`/`-c`)
  против фактического потребления (`--util`), с сортировкой и выводом в
  `csv`/`json`/`yaml`. Для фактических метрик нужен metrics-server.
- **ktop** (`vladimirvivien/ktop`) — `top`-подобный TUI: ноды, поды и их метрики
  CPU/памяти в реальном времени. Из релиза берётся одиночный `ktop` — плагин
  `kubectl-ktop` не ставим.
- **kubefetch** (`jkulzer/kubefetch`) — neofetch для Kubernetes-кластера:
  сводка о кластере, нодах и подах одним экраном.

```bash
kubecolor get pods -A                    # цветной вывод kubectl
kubecolor diff -f old.yaml -f new.yaml   # читаемый дифф манифестов
kube-capacity --util --pods              # requests/limits vs фактическая загрузка
kube-capacity -o json --sort mem.util    # то же в JSON
ktop -A                                  # TUI: метрики нод и подов по всем ns
kubefetch                                # сводка о кластере
```

---

## krew и kubectl-утилиты (view-secret, df-pv, browse-pvc)

Роль `kubernetes` ставит **krew** (`kubernetes-sigs/krew`) — менеджер
kubectl-плагинов (для установки плагинов вручную потом), а также три утилиты,
которые раньше ставились бы как kubectl-плагины, напрямую бинарниками:

- **view-secret** — декодирование секретов: ключи и значения base64, фильтр по
  ключу или всё сразу.
- **df-pv** — `df` по PersistentVolume: занятое место по PVC/PV в стиле
  unix-утилиты `df`.
- **browse-pvc** — просмотр содержимого PVC из CLI: создаёт джобу,
  привязывающуюся к PVC, и заходит в неё.

Все три ставятся бинарниками в `/usr/local/bin` **без префикса `kubectl-`** и
вызываются напрямую (не через `kubectl view-secret`). Версии — актуальные из
GitHub-релизов, фиксации нет.

```bash
krew update                                # обновить индекс плагинов
krew install ctx                           # поставить произвольный плагин вручную
krew list                                  # что уже установлено
view-secret my-secret -a                   # декодировать секрет
view-secret my-secret my-key               # декодировать конкретный ключ
df-pv                                      # занятость PV
browse-pvc my-pvc                          # зайти в PVC
```

Сам `krew` — бинарник в `/usr/local/bin`; `~/.krew/bin` (куда krew кладёт
плагины при `krew install`) добавляется в `PATH` через `devops-shell.sh`.

---

## pluto, pv-migrate и marvin

Роль `kubernetes` дополнительно ставит три самостоятельных бинарника:

- **pluto** (`FairwindsOps/pluto`) — находит устаревшие и удалённые
  `apiVersion` в манифестах Kubernetes: сканирует локальные файлы или кластер
  и показывает, что надо мигрировать.
- **pv-migrate** (`utkuozdemir/pv-migrate`) — миграция и backup/restore
  PersistentVolume между PVC/кластерами (через `rsync` или `skopeo`).
- **marvin** (`undistro/marvin`) — сканер кластера CEL-выражениями: выявляет
  проблемы, мисконфиги и уязвимости по правилам.

```bash
pluto detect-files -d manifests/          # устаревшие apiVersion в файлах
pluto detect-helm -d charts/              # то же в Helm-чартах
pv-migrate migrate src dst                # миграция PV между PVC/кластерами
marvin scan                               # сканировать текущий кластер
```

---

## tgsieve — сжатый вывод `terragrunt plan`

Роль `iac` ставит **tgsieve** (`imcitius/tgsieve`). На большом стеке
`terragrunt plan --all` печатает тысячи строк, в которых нужные изменения
теряются. tgsieve сам запускает план, читает **структурированный** вывод
(`tfplan.json` по юнитам, флаг `--json-out-dir`) вместо текста, отбрасывает
объявленный шум, сворачивает повторяющиеся изменения по юнитам и печатает
только суть — с вложенностью «где → что → какие поля». Есть и `apply`, который
применяет ровно то, что показал план.

```bash
tgsieve plan                    # план для текущего юнита и сжатый отчёт
tgsieve plan --all              # план по всему стеку
tgsieve plan --all --timings    # ещё и самые медленные юниты
```

---

## Схемы инфраструктуры: graphviz, inframap, rover

Роль `iac` ставит **graphviz** (`dot`) и два визуализатора Terraform. Прямого
аналога KubeDiagrams (манифесты → схема с иконками) для Terraform + Yandex
Cloud нет: KubeDiagrams читает только k8s, а Terraform-инструменты либо не
знают YC-провайдер, либо не знают про terragrunt (план работ — в
[`TODO-diagrams.md`](TODO-diagrams.md)). Поэтому на большом стеке схема
строится слоями.

**1. Карта юнитов** — `terragrunt dag graph` (v0.93+), рёбра берутся из
`dependency`-блоков. Ни `init`, ни `plan`, ни кредов не нужно.

```bash
terragrunt dag graph > dag.dot && dot -Tsvg dag.dot -o dag.svg
terragrunt dag graph --working-dir live/prod > prod.dot   # по окружению
```

**2. Один юнит** — `inframap` читает tfstate или HCL и выбрасывает служебные
узлы Terraform (провайдеры, переменные, data), поэтому граф читается лучше,
чем от `terraform graph`. Для YC работает общий режим — без группировки по
сетям и без иконок YC.

```bash
cd live/prod/ru-central1-d/k8s
terragrunt run -- show -json > /tmp/k8s-state.json
inframap generate /tmp/k8s-state.json | dot -Tsvg > k8s.svg
```

**3. То же интерактивно** — `rover` берёт JSON плана, показывает ресурсы,
связи и граф в браузере; `-standalone` собирает статический HTML без сервера.
Для terragrunt-юнита план снимается через `terragrunt`, потому что `rover`
запускает `terraform` и в каталоге с одним `terragrunt.hcl` ничего не найдёт.

```bash
terragrunt run -- plan -out=/tmp/k8s.tfplan
terragrunt run -- show -json /tmp/k8s.tfplan > /tmp/k8s-plan.json
rover -planJSONPath /tmp/k8s-plan.json -standalone   # ../rover/index.html
```

---

## pgCenter — админка и мониторинг PostgreSQL

Роль `postgres` ставит **pgcenter** (`lesovsky/pgcenter`) — консольную админку
и мониторинг PostgreSQL в духе top/htop. Живая статистика активности, запросов,
блокировок и ожидающих событий, размеры таблиц и индексов, профилировщик wait
events, запись статистики в файл и отчёты по ней. Подключается как обычный
клиент PostgreSQL: параметрами libpq (`-h`, `-p`, `-U` и имя базы) или
переменными окружения `PG*` (включая `~/.pgpass`).

```bash
pgcenter top -h db.example.com -U postgres app      # top-статистика в реальном времени
pgcenter profile -h db.example.com -U postgres app  # профилировщик wait events
pgcenter record -h db.example.com -U postgres app   # запись статистики в файл
pgcenter report -f pgcenter.stat.tar                # отчёт по записанной статистике
```

Для расширенной статистики в самой базе есть `pgcenter config` — ставит и
снимает свою схему сбора статистики.

---

## eBPF-наблюдаемость: pwru, bpftop, oryx, pktstat-bpf, tracee

Роль `ebpf` ставит пять локальных eBPF-утилит для отладки ядра, сети и
runtime-безопасности:

- **pwru** (`cilium/pwru`) — eBPF-отладчик сетевого стека Linux: показывает путь
  пакета через ядро и «где он потерялся» (drop/reroute, таблицы маршрутизации,
  iptables, XDP).
- **bpftop** (`jfernandez/bpftop`) — real-time обзор запущенных eBPF-программ:
  сколько CPU они занимают и сколько событий обрабатывают.
- **oryx** (`pythops/oryx`) — TUI-сниффер сетевого трафика на eBPF: tcpdump в
  интерактивном интерфейсе, фильтры по протоколам и направлению.
- **pktstat-bpf** (`dkorunic/pktstat-bpf`) — монитор трафика на eBPF (TC/XDP/
  kprobes): сводка по потокам, процессам и скоростям в терминале.
- **tracee** (`aquasecurity/tracee`) — runtime-security и форензика Linux: сотни
  событий (syscalls, файлы, сеть, контейнеры) и встроенные сигнатуры угроз.

```bash
sudo pwru                                  # где потерялся пакет (можно pcap-filter)
sudo bpftop                                # обзор eBPF-программ в реальном времени
sudo oryx -i eth0                          # TUI-сниффер трафика
sudo pktstat-bpf --tui                     # сводка трафика по процессам
sudo tracee                                # live-события системы
tracee version                             # версия
```

Все они работают с eBPF в ядре и запускаются через `sudo` (нужны
CAP_BPF/CAP_PERFMON/CAP_SYS_ADMIN), поэтому `setcap` на бинарники не навешиваем.
Для работы нужны права на загрузку BPF-программ (на десктопе Ubuntu это доступно
по умолчанию; в системах с `kernel.unprivileged_bpf_disabled=1` потребуется root).

`tracee` ставится не через роль `binaries`: кроме самого бинарника релиз
содержит Go-плагин с сигнатурами безопасности (`dist/signatures/builtin.so`).
Бинарник кладётся в `/opt/tracee/` вместе с каталогом `signatures/`, а в
`/usr/local/bin/tracee` — симлинк (tracee разрешает симлинк через
`os.Executable()` и находит сигнатуры в `<каталог бинарника>/signatures`).

---

## Шпаргалки команд: navi, cheat, tldr

Три взаимодополняющих инструмента для «как запускается команда» ставятся ролью
`shell` (navi — уже была, cheat и tldr добавлены):

- **tldr** (`tldr-pages/tldr`) — каноническая community-база кратких примеров
  для сотен стандартных CLI-утилит. Клиент ставится через `npm install -g`,
  кэш страниц плейбук наполняет сразу (`tldr --update`).
- **cheat** (`cheat/cheat`) — собственные шпаргалки: создаёте и редактируете
  `cheatsheets/` и `cheatpaths`, версионируете в git.
- **navi** (`denisidoro/navi`) — интерактивный выбор шпаргалок поверх fzf
  (свои + community-коллекции).

```bash
tldr tar                                   # краткие примеры по утилите
cheat tar                                  # свои шпаргалки по утилите
navi                                       # интерактивный поиск шпаргалки
```

---

## JSON и табличные данные: jnv, octosql

Две утилиты роли `shell` для работы с данными без поднятия БД:

- **jnv** (`ynqa/jnv`) — интерактивный фильтр JSON: набираете jq-выражение и
  сразу видите результат (jq уже ставится ролью `base`).
- **octosql** (`cube2222/octosql`) — SQL-запросы прямо к JSON/CSV/Parquet:
  `SELECT`, `WHERE`, `JOIN` и агрегаты по файлам.

```bash
curl -s https://api.github.com/repos/ynqa/jnv | jnv '.stargazers_count'
octosql 'select name, stars from "repos.json" where stars > 1000'
```

---

## Проверка алерт-правил: vmalert-tool

**vmalert-tool** (`VictoriaMetrics/VictoriaMetrics`, роль `monitoring`) —
офлайн-утилита для валидации и unit-тестов alerting/recording-правил
Prometheus-совместимых систем: проверяет конфиги и гоняет тесты без поднятия
сервиса, без сервера и без Web UI. Единственный нужный бинарник из релизов
VictoriaMetrics на ноутбуке (кладётся из тарболла `vmutils-...` как
`vmalert-tool`).

```bash
vmalert-tool unittest -files rules.yaml -tests tests.yaml   # прогнать unit-тесты правил
```

Та же роль ставит **vlogscli** (`VictoriaMetrics/VictoriaLogs`) — CLI-клиент
VictoriaLogs: LogsQL-запросы и live tailing к уже работающему серверу логов,
локальный сервер для этого не нужен. Бинарник берётся из архива `vlutils-...`
(в нём же лежит `vlagent-prod`) и кладётся как `vlogscli`.

```bash
vlogscli -datasource.url=http://victorialogs.example:9428/select/logsql/query 'error | stats count()'
```

Остальные бинарники VictoriaMetrics на ноуте не ставятся — им нужна локальная
TSDB/приёмка метрик: `victoria-metrics` (сам сервер + Web UI), `vmctl`
(миграция только **в** VictoriaMetrics), `vmagent` (сбор/пересылка метрик),
`vmalert` (вычисление алертов в реальном времени), `vmauth` (прокси-аутентификация),
`vmbackup`/`vmrestore` (бэкап/восстановление данных VM).

Дополнительно роль `git` ставит **reviewdog** (`reviewdog/reviewdog`) — гоняет
любые линтеры и шлёт их замечания как inline-комментарии в PR/MR
(`reviewdog -f="eslint"`), а роль `shell` — **grex** (`pemistahl/grex`),
генерирующую regex прямо из примеров строк (`grex -f`) — тоже из числа топовых
неустановленных кандидатов.

---

## osquery — SQL-подобная инструментация ОС

Роль `secrets` ставит **osquery** (`osquery/osquery`) официальным `.deb` из
GitHub-релиза. Бинарники `/opt/osquery/bin/osqueryd` (демон) и `osqueryi`
(интерактивная консоль) доступны через симлинки в `/usr/bin`.

```bash
osqueryi "SELECT hostname, cpu_brand, physical_memory FROM system_info;"
osqueryi "SELECT pid, name, path FROM processes WHERE name LIKE '%ssh';"
```

Пакет кладёт и systemd-юнит `osqueryd.service`, но плейбук его не запускает:
без файла конфигурации `/etc/osquery/osquery.conf` демон всё равно не
поднимется, поэтому автозагрузку не трогаем и дефолты не ломаем (запуск — через
`osqueryi` или настройка демона вручную).

---

## gotty — терминал как веб-приложение

Роль `network` ставит **gotty** (`yudai/gotty`) — делится командами в браузере:

```bash
gotty -w htop                              # открыть htop в браузере (читает ввод)
gotty -p 8080 -w top                       # на конкретном порту
```

Служит только на loopback по умолчанию; в отличие от `sshx` (внешний
совместный терминал), gotty разворачивается локально и сам не ходит в сеть —
сервис не поднимаем.

---

## TLS-сертификаты: gossl и crip

Две утилиты роли `network` для работы с X.509 без ручного `openssl s_client`:

- **gossl** (`vvrnv/gossl`) — проверка сертификата хоста: цепочка, срок
  действия, поддерживаемые протоколы; печатает вердикт по каждому пункту.
- **crip** (certificate-ripper, `Hakky54/certificate-ripper`) — вытаскивает
  цепочку сертификатов с удалённого хоста и умеет сразу положить её в PEM/trust
  store. Нативная сборка (GraalVM), JVM не требуется.

```bash
gossl verify --domain example.com
crip print --url https://example.com
crip trust --url https://example.com        # добавить в системный trust store
```

---

## sslscan — перебор шифров TLS

Роль `network` ставит **sslscan** (`rbsec/sslscan`) из пакета Ubuntu: он
перебирает шифры и версии протокола, показывает предпочтения сервера, слабые
шифры (RC4, DES, EXPORT), повторное согласование и сертификат.

```bash
sslscan example.com:443
sslscan --starttls-smtp mail.example.com:25
```

Сканировать только свои стенды: перебор шифров заметен в логах и упирается в
rate limit или защиту от сканеров.

В Ubuntu 26.04 это версия 2.1.5: GitHub-релизы апстрима содержат только
`sslscan.exe` для Windows, а `make static` начиная с 2.2.0 требует OpenSSL 3.5.
Публикацию linux-amd64 бинарника запросили в
[#375](https://github.com/rbsec/sslscan/issues/375) — когда ассет появится,
утилиту можно перевести с apt на роль `binaries`.

---

## YAML и JSON-логи: yamlfixer и jlv

- **yamlfixer** (`opt-nc/yamlfixer`, роль `shell`, через pipx) — берёт вывод
  `yamllint` и исправляет замечания (отступы, кавычки, пробелы), дополняя
  `yamllint` и `yamlfmt`: `switch`-стиль линтера остаётся, а правки делаются
  автоматически.
- **jlv** (json-log-viewer, `hedhyw/json-log-viewer`, роль `shell`) —
  интерактивный просмотр JSON-логов: строки раскладываются в таблицу с
  фильтрами по полям и переходом к ошибкам. Дополняет `hl`
  (универсальный пейджер логов): `jlv` заточен под навигацию по JSON-потоку.

```bash
yamllint -f parsable . | yamlfixer
jlv app.log                                 # или `kubectl logs ... | jlv`
```

---

## Группировка логов: angle-grinder (agrind)

**angle-grinder** (`rcoh/angle-grinder`, роль `shell`, команда `agrind`) —
запросы к потоку логов одной строкой: разобрать JSON или logfmt, сгруппировать
по полю и посчитать. Дополняет `hl` и `jlv` (показывают записи), `sig` (ищет
по потоку) и `lnav`/`toolong` (читают файлы): `agrind` отвечает «сколько каких
и что медленнее», не загружая лог в БД.

```bash
# Сколько каких уровней в потоке
kubectl logs -f deploy/api | agrind '* | json | count by level'

# Топ кодов ответа и p95 по длительности
stern api | agrind '* | json | count by status_code'
stern api | agrind '* | json | p95(duration_ms)'

# logfmt и произвольный текст: разбор шаблоном
agrind '* | logfmt | count by method' < access.log
agrind '* | parse "* * *" as method, path, code | count by method' < app.log
```

---

## fq — jq для бинарных форматов

**fq** (`wader/fq`, роль `shell`) декодирует бинарный файл в дерево полей, и
дальше по нему работают обычные jq-фильтры. Дополняет `xxd`/`hexdump` (те
показывают только байты), `unzip -l` и `tar -tvf` (только имена файлов) и
`tshark` (только сетевой трафик): `fq` одним синтаксисом разбирает ELF, ZIP,
tar, gzip, pcap, TLS-хендшейк, DNS, protobuf, CBOR и JPEG/EXIF.

```bash
# Архив: fq сам распознаёт gzip → tar и показывает структуру
fq . app.tar.gz

# Файлы и размеры в tar
fq -d tar '.files[] | [.name, .size]' app.tar

# ZIP: имена и распакованные размеры из central directory
fq -d zip '.central_directories[] | {name: .file_name, size: .uncompressed_size}' image.zip

# ELF: заголовок, архитектура, точка входа, число program headers
fq -d elf '.header' /usr/bin/ls
fq -d elf '.program_headers | length' /usr/bin/ls

# Сырой JSON вместо подсвеченного дерева — дальше в пайплайн
fq -V -d elf '.header' /usr/bin/ls | jq .
```

Формат угадывается по содержимому (`fq . file`), нужный декодер задаётся
через `-d` (`-d elf`, `-d zip`, `-d pcap`), список декодеров — в
[README проекта](https://github.com/wader/fq#decoders). `fq` только читает:
это не hex-редактор, и в глубоком анализе трафика он не заменяет `tshark`.

---

## kubebox — консоль Kubernetes по SSH

**kubebox** (`astefanutti/kubebox`, роль `kubernetes`, ставится через npm) —
терминальный dashboard: поды, логи, `exec`, YAML, события; умеет поднимать
веб-режим в браузере. В отличие от `headlamp` (desktop-приложение) работает
прямо в ssh-сессии и не требует GUI.

```bash
kubebox                                     # TUI по текущему контексту
kubebox --server 127.0.0.1:8080             # веб-режим на localhost
```

---

## pitwall — терминал для coding-агентов

pitwall в плейбук пока не ставится: решение не принято. Блокер снят — issue о
вводе русских букв закрыт 2026-10-19, фикс вышел в `v0.1.0-beta.12`
(<https://github.com/quanticstudios/pitwall/issues/127>). Нужен ли он при
наличии вкладок opencode 2 и `herdr`, разбирается в разделе 6
[`TODO-opencode-orchestration.md`](TODO-opencode-orchestration.md).

Полный список утилит, которые плейбук сознательно не ставит (с причинами и
ссылками на issue) — в [`not-install.md`](not-install.md). Кандидаты, которые
ждут готового бинарника на GitHub, — в
[`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md), а те, чей бинарник
не запускается на Ubuntu 26.04, — в
[`TODO-incompatible-ubuntu-2604.md`](TODO-incompatible-ubuntu-2604.md).
Кандидаты из трендов GitHub, которые осознанно не добавлены в плейбук
(не приложение, нет релизных бинарников), — в
[`TODO-trend-github-not-added.md`](TODO-trend-github-not-added.md).
Заброшенные проекты (архив GitHub, годы без обновлений) — только в
[`TODO-abandoned.md`](TODO-abandoned.md). Полезные утилиты, которые ставятся
только через npm и пока не добавлены, — в
[`TODO-usefull-npm.md`](TODO-usefull-npm.md).
План генератора архитектурных схем из Terraform/Terragrunt (аналога
KubeDiagrams для Yandex Cloud), который пока не реализован, — в
[`TODO-diagrams.md`](TODO-diagrams.md).
Серверные приложения, сервисы и Helm-чарты (grafana, prometheus, gitea, Jenkins
и т.п.), а также агенты на нодах Kubernetes (DaemonSet/static Pod), которые
плейбук не ставит, — в [`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md). Из Ansible
Galaxy плейбук не ставит ничего — ни ролей, ни коллекций, ни готовых
playbook'ов (почему и как поставить в конкретном проекте) — в
[`TODO-ansible-galaxy-not-install.md`](TODO-ansible-galaxy-not-install.md).

---

## herdr, rtk, ocr, mcpc, opencode-mem, stealth-browser-mcp, T3 Code, Caprock, Ouroboros, Orca и Claude-BugHunter — инструменты для AI-агентов

Роль `ai_tools` ставит CLI, усиливающие coding-агентов (opencode и др.),
локальную память, MCP-сервер браузера и Google Chrome, stealth-браузер,
приложения T3 Code, Caprock, Ouroboros и Orca, а также навыки bug bounty
(без CLI `cbh` — пакета на PyPI нет). Бинарники кладутся в
`/usr/local/bin/` через роль `binaries` (версия — актуальная на момент
запуска), `mcpc` — npm-пакетом в тот же каталог, pipx-пакеты — в изолированное
окружение. Плагин памяти **opencode-mem** бинарника не ставит: npm-пакет
качает сам opencode, роль регистрирует пакет в глобальном конфиге, кладёт его
настройки и заранее скачивает модель эмбеддингов.

- **herdr** (`herdrdev/herdr`) — TUI-оболочка поверх терминала: управляет
  сессиями/панелями/вкладками coding-агентов, показывает их состояние
  (работает / ждёт ввода / заблокирован), умеет удалённые машины по SSH и
  самообновление (`herdr update`). Одиночный статический бинарник.
- **rtk** (`rtk-ai/rtk`) — прокси-обёртка над утилитами (`rtk git`, `rtk ls`,
  `rtk kubectl`, …): сжимает и фильтрует вывод (логи, diff, таблицы), прежде
  чем он попадёт в контекст LLM.
- **mcpc** (`apify/mcpc`) — универсальный клиент MCP: подключается к серверу
  и даёт дёргать его tools/resources/prompts из терминала, без агента.
  Нужен, чтобы проверить только что поставленный сервер (`radar`,
  `kubernetes-mcp-server`, `stealth-browser-mcp`) и разобраться в его
  инструментах. Ставится npm-пакетом `@apify/mcpc` (Node.js ≥ 22.12, в
  Ubuntu 26.04 из apt — 22.x), идемпотентность — по наличию
  `/usr/local/bin/mcpc`; обновить = удалить файл или
  `sudo npm update -g @apify/mcpc`.
- **ocr** (`alibaba/open-code-review`) — AI-ревью по git-диффу: читает diff,
  отдаёт изменённые файлы выбранной модели через агент с tools (дочитывает
  файл целиком, ищет по коду, смотрит соседние изменения) и печатает
  замечания построчно. `ocr scan` ревьюит файлы целиком, `ocr delegate`
  отдаёт спеку ревью хост-агенту без собственного LLM, `ocr viewer` — WebUI
  с сохранёнными сессиями ревью. Одиночный бинарник
  `opencodereview-linux-amd64`, в `/usr/local/bin` кладётся как `ocr`.
- **kaeru** (`LamantinAI/kaeru`) — память агентов на типизированном графе:
  рабочий и архивный слои, история утверждений и отзывов, reasoning-цепочки,
  MCP по HTTP. Дополняет opencode-mem: там векторный поиск по заметкам,
  здесь граф с provenance. Релизный `kaeru-mcp` ставится в
  `/usr/local/bin` и оборачивается пользовательским systemd-юнитом.
- **opencode-mem** (`tickernelz/opencode-mem`) — память локально, без облака:
  Turso/libSQL с векторным поиском, локальные эмбеддинги, авто-захват после
  idle через провайдера opencode, инъекция похожих воспоминаний в контекст,
  web-UI на `127.0.0.1:4747` и «dreaming»-консолидация.
- **CloakBrowser** (`CloakHQ/CloakBrowser`) — stealth-Chromium как drop-in
  замена Playwright/Puppeteer: 50+ патчей fingerprint на уровне исходников
  Chromium и `humanize=True`. Ставится pipx-пакетом `cloakbrowser`.

```bash
herdr --version
rtk --version
ocr version
mcpc --version
kaeru-mcp --version
cloakbrowser --help
opencode plugin list         # opencode-mem в списке плагинов opencode
```

Пример: подключиться к серверам из файла конфига и посмотреть их инструменты.

```bash
mcpc connect ./.mcp.json     # подключить серверы из конфига (появятся @сессии)
mcpc                         # сессии, их инструменты и профили
mcpc grep pod                # поиск по инструментам всех активных сессий
mcpc close @<сессия>         # закрыть сессию
```

### Память в opencode: opencode-mem

Плагин регистрируется в глобальном конфиге opencode командой
`opencode plugin add opencode-mem`: она дописывает пакет в массив `plugins`
файла `~/.config/opencode/opencode.jsonc`, не трогая комментарии, отступы,
провайдеров и `mcp.servers`. Сам npm-пакет opencode качает в
`~/.cache/opencode/npm` при старте, поэтому в `/usr/local/bin` ничего не
появляется. Повторный прогон идемпотентен — команда печатает
«already configured».

- **opencode-mem** (`tickernelz/opencode-mem`) — локальная память: встроенная
  Turso/libSQL с векторным поиском (отдельная векторная БД не нужна),
  локальные эмбеддинги на CPU (модель скачивается при первом запуске,
  ~0.5–2 ГБ RAM), авто-захват после idle через провайдера opencode, инъекция
  похожих воспоминаний, «dreaming»-консолидация и web-UI на
  `http://127.0.0.1:4747`. Хранилище `~/.opencode-mem/data` плагин создаёт
  сам при первом старте. Облака нет: всё, включая эмбеддинги, считается на
  ноутбуке.

Настройки роль кладёт сама (`~/.config/opencode/opencode-mem.jsonc`):

- **модель** — `Xenova/bge-m3` в квантовании `q8` (1024 измерения,
  многоязычная, ~560 МБ). Дефолтная `Xenova/nomic-embed-text-v1` обучена на
  английском: на русских запросах она не находила ничего;
- **порог** — `0.25`. Плагин сравнивает с порогом не косинус, а смешанную
  оценку `0.5*cos + 0.3*tags + 0.2*keyword`; у записи без тегов потолок ~0.7,
  реальные значения релевантных пар 0.28–0.47, поэтому дефолтный `0.6` не
  пропускает ни одного результата.

Модель скачивается заранее задачей плейбука (через `transformers` из
npm-кэша плагина), чтобы первый поиск не ждал загрузку. Замер на 50 фактах и
50 русских запросах с английскими техническими вставками: **47/50 первых
мест, 50/50 в топ-3**, около 4.6 результатов на запрос.

```bash
opencode plugin list                 # opencode-mem в списке
opencode plugin remove opencode-mem  # убрать плагин
```

- **Флаг:** `-e opencode_mem_install=false` выключает установку; уже
  подключённый плагин убирается командой `opencode plugin remove`.
- **Смена модели** — две операции, а не одна: миграция шарда
  (`POST /api/migration/run {"strategy":"fresh-start"}`, заголовок
  `x-opencode-mem-token`) и перезапуск процесса. Модель живёт в процессном
  синглтоне, `opencode reload` её не пересоздаёт; порог и остальные ключи
  конфига, наоборот, подхватываются после `opencode reload`.
- **Данные:** `~/.opencode-mem/data` на диске (модель эмбеддингов кэшируется в
  `data/.cache`); `opencode plugin remove` данные не удаляет.
- **Облачный mem0 не ставится:** он хранит воспоминания только на своём API,
  офлайн памяти нет. Причина отказа — в
  [`not-install.md`](not-install.md).

### T3 Code — графический пульт к агентам

`pingdotgg/t3code` — один локальный сервер на ноутбуке и несколько клиентов к
нему: десктопное приложение (Electron), веб-клиент и мобильные приложения
iOS/Android. T3 Code не запускает «своих» агентов, а подхватывает уже
установленные и авторизованные CLI — Claude Code, Codex, Cursor, Grok Build,
opencode и Google Antigravity: показывает сессии, статус, диффы и позволяет
выдавать задачи из одного окна (в том числе с телефона).

Ставится официальным `.deb` из GitHub-релиза (`T3-Code-{version}-amd64.deb`),
приложение распаковывается в `/opt`, ярлык — `/usr/bin/t3code`:

```bash
t3code --version
```

- **Идемпотентность:** если `/usr/bin/t3code` уже есть, роль ничего не
  скачивает. Обновить — запустить установку вручную (`sudo apt install
  ./T3-Code-*.deb` из свежего релиза) или удалить приложение и прогнать плейбук.
- **Зависимости** (libgtk-3, libnss3, libasound2t64, libsecret-1-0 и т. п.)
  подтягиваются из репозитория Ubuntu: пакет ставится модулем `apt`, а не
  `dpkg`.
- **CLI `t3`** (headless-сервер, `t3 service install` в фон, `t3 pair` для
  телефона, `t3 update`) в `.deb` не входит. Он нужен, когда T3 Code работает
  без десктопного приложения — тогда ставится официальным скриптом:
  `curl -fsSL https://t3.codes/install.sh | sh` (кладёт в `~/.t3`, симлинк —
  в `~/.local/bin`). Плейбук его не ставит: на ноутбуке хватает приложения.
- **Данные и проекты** T3 Code хранит у себя (`~/.t3` у CLI, каталог приложения
  у `.deb`); удаление пакета их не трогает.

### Caprock — наблюдение за сессиями агентов

`dspv/caprock` — десктопное приложение и локальный демон для наблюдения за
coding-агентами: Claude Code, Codex, OpenCode 1/2, Gemini CLI, Hermes Agent и
DeepSeek Harness. Показывает сессии в вкладках и сплитах, кто ждёт ответа, что
стоит следующий вызов при текущем контексте, стоимость каждого PR и сессии по
ценам API, лимиты плана (5-часовое и недельное окно), историю после очистки
транскриптов и MCP-сервер `caprock mcp` для агентов. Данные — SQLite на диске,
сервер слушает только loopback, аккаунта и телеметрии нет.

Ставится официальным `.deb` из GitHub-релиза (`Caprock-Linux.deb`, постоянное
имя ассета): `/usr/bin/caprock` (демон и CLI), `/usr/bin/caprock-app` (GUI),
`/usr/bin/caprock-pty-host`, ярлык в меню приложений. Зависимости
(libwebkit2gtk-4.1-0, libgtk-3-0, libayatana-appindicator3-1) подтягивает apt.

```bash
caprock --version
caprock up        # демон и дашборд на http://127.0.0.1:22776
caprock status    # демон, хуки и приём истории
```

- **Хуки Claude Code.** `caprock up` предлагает прописать хук и status line в
  `~/.claude/settings.json` (с бэкапом файла). Плейбук этого не делает:
  согласие остаётся за пользователем, а история читается из транскриптов и без
  хука.
- **Автозапуск.** `caprock service install` создаёт пользовательский
  systemd-юнит. Плейбук его не включает: приложение запускается из меню или
  командой `caprock up`.
- **Выключить установку:** `caprock_install: false` в
  `roles/ai_tools/defaults/main.yml`.
- **Идемпотентность:** есть `/usr/bin/caprock` — роль ничего не качает.
  Обновить — удалить пакет и прогнать плейбук.

### Ouroboros — AI-агент с десктопом, CLI и web-интерфейсом

`razzant/ouroboros` — general-purpose агент, который держит идентичность,
память и историю между задачами и перезапусками, ведёт рой суб-агентов,
работает с внешними проектами и умеет переписывать собственный код.
Управляется десктопным приложением или headless-CLI; модели — свои API-ключи
или локальная GGUF; телеметрии по умолчанию нет, сервер слушает только
`127.0.0.1:8765`.

Ставится официальным `.deb` (`ouroboros_{version}_amd64.deb`): приложение
распаковывается в `/opt/ouroboros`, команда `ouroboros` появляется на `PATH`,
добавляется ярлык в меню приложений. systemd user unit пакет создаёт, но не
включает.

```bash
ouroboros status
ouroboros run --start "2+2?"
```

- **Размер:** `.deb` ~900 МБ — внутрь вложены CPython, SQLite и
  Chromium/WebKit. Если агент не нужен, `ouroboros_install: false` в
  `roles/ai_tools/defaults/main.yml` выключает установку целиком.
- **Первый запуск** — мастер настройки: доступ к моделям, политика ревью,
  бюджет. Без ключа или локальной модели задачи не выполняются.
- **Данные** — `~/Ouroboros/data`. Удаление пакета их не трогает, чистить
  вручную.
- **Идемпотентность:** есть `/usr/bin/ouroboros` — роль ничего не качает.

### Orca — IDE для параллельной работы агентов

`stablyai/orca` — десктопное приложение к флоту coding-агентов: рабочие
пространства под воркеров, координатор, который раздаёт задачи, чат и обычный
терминал в одном окне (разговор переезжает из чата в CLI без потери
контекста), удалённые машины, мобильный клиент и боты из Slack, Linear и
GitHub. Своих агентов Orca не запускает: работает с локально установленными и
авторизованными Claude Code или Codex на вашей подписке.

Ставится официальным `.deb` из GitHub-релиза
(`orca-ide_{version}_amd64.deb`, пакет `orca-ide`) ролью `github_deb`:
приложение распаковывается в `/opt/Orca`, ярлык — `orca-ide.desktop`.

```bash
dpkg-query -W -f='${Version}\n' orca-ide
/opt/Orca/orca-ide
```

- **Размер:** `.deb` ~213 МБ, установка ~700 МБ. Зависимости (GTK, NSS,
  libsecret, `xdotool`, `xclip`, `xvfb` и т. п.) подтягивает apt.
- **Обновление:** версия из `releases/latest` сравнивается с установленной в
  `dpkg`, поэтому повторный прогон плейбука подтягивает новый релиз (как у
  остальных `.deb` из GitHub-релизов).
- **Установка стоит вне `PATH`:** ярлык в меню приложений есть, а команды в
  `/usr/local/bin` пакет не создаёт — запуск из терминала это
  `/opt/Orca/orca-ide`.
- **Выключить установку:** `orca_install: false` в
  `roles/ai_tools/defaults/main.yml`.

### Claude-BugHunter — навыки bug bounty и red team

`elementalsouls/Claude-BugHunter` — набор из 83 навыка для внешнего red team
и bug bounty: recon и разметка скоупа, классификация находок по классам
уязвимостей (SQLi, SSRF, XSS, OAuth/SAML, GraphQL, k8s, LLM/AI и др.), гейт
триажа, построение цепочек и отчёты по шаблонам Bugcrowd/HackerOne. Навыки —
обычные Agent Skills, поэтому их видит opencode (и другие harness'ы), а не
только Claude Code.

Плейбук делает две вещи:

1. клонирует репозиторий в `~/.local/share/claude-bughunter` (с `depth: 1`,
   только если каталога ещё нет);
2. копирует `skills/*` в `~/.agents/skills` — тот же каталог, что использует
   роль `skills`.

CLI `cbh` — детерминированный runner без LLM (recon, classify, triage,
отчёты). На PyPI пакета нет, поэтому плейбук его не ставит: установка из
git-URL тянула бы клон и следовала за `main` без фиксированной версии.
Запрос на пакет — [issue #211](https://github.com/elementalsouls/Claude-BugHunter/issues/211).
До его появления CLI запускается из клона без установки:

```bash
python3 ~/.local/share/claude-bughunter/scripts/cbh.py --help
python3 ~/.local/share/claude-bughunter/scripts/cbh.py recon example.com
python3 ~/.local/share/claude-bughunter/scripts/cbh.py classify \
  "https://example.com/api/users/42?next=..."
```

- **Upstream `scripts/install.sh` не запускается:** он ставит навыки ещё и в
  `~/.claude`, дописывает `source hunt.sh` в shell rc и добавляет команды
  Claude Code. Плейбук ограничивается тем, что нужно opencode.
- **Без Burp** `cbh` работает в curl-only режиме; `cbh --burp` направляет
  трафик в Burp Proxy, если он запущен.
- **Навыков много** — 83 записи в списке навыков агента, это заметно
  увеличивает контекст. Не нужен совсем: `bughunter_install: false` в
  `roles/ai_tools/defaults/main.yml`.
- **Обновление:** удалить `~/.local/share/claude-bughunter` и прогнать
  плейбук заново — копирование навыков идемпотентно.

### stealth-browser-mcp — MCP-сервер браузера

`vibheksoni/stealth-browser-mcp` — MCP-сервер для AI-клиентов (opencode,
Claude, Cursor): навигация, извлечение DOM и CSS, перехват запросов и ответов,
cookie/storage, CDP-команды и хуки на сеть. Работает через `nodriver` и
запускает настоящий Chrome/Chromium/Edge, поэтому проходит часть проверок
Cloudflare/Queue-It, где палится Playwright (результат зависит от сайта,
региона и версии браузера).

Ставится из PyPI через pipx (роль `pipx_apps`): изолированный venv, шим
`stealth-browser-mcp` в `~/.local/bin`, sudo не нужен. PyPI-пакет называется
`browserstealthmcp` — имя `stealth-browser-mcp` на PyPI занято другим,
не относящимся к проекту пакетом.

```bash
stealth-browser-mcp --list-sections
stealth-browser-mcp --minimal   # 21 инструмент вместо 101
```

- **Браузер:** роль ставит Google Chrome официальным `.deb`
  (`google-chrome-stable_current_amd64.deb`, ~150 МБ; качается только если
  `/usr/bin/google-chrome` ещё нет). Пакет сам подключает свой
  apt-репозиторий (`/etc/apt/sources.list.d/google-chrome.sources` и ключ
  `/usr/share/keyrings/google-chrome.gpg`), поэтому обновления дальше
  приходят обычным `apt upgrade`; своих source-файлов плейбук не пишет.
  В Ubuntu Chromium есть только как snap, а confinement ограничивает доступ
  к профилю и `DevToolsActivePort` (он остаётся в приватном `/tmp` снапа),
  поэтому CDP-подключение из nodriver там не гарантировано. Сервер находит
  `/usr/bin/google-chrome` сам; другой Chromium (например, Yandex) задаётся
  переменной `STEALTH_BROWSER_EXECUTABLE` в конфиге MCP-клиента:
  `"env": {"STEALTH_BROWSER_EXECUTABLE": "/usr/bin/yandex-browser"}`.
- **Выключить браузер:** `google_chrome_install: false` в
  `roles/ai_tools/defaults/main.yml`.
- **Подключение** — вручную в `~/.config/opencode/opencode.json` (плейбук
  конфиг MCP-клиента не пишет, как и для `kubernetes-mcp-server`):

  ```json
  "mcp": {
    "stealth-browser": {
      "type": "local",
      "command": ["/home/<user>/.local/bin/stealth-browser-mcp"],
      "enabled": true
    }
  }
  ```

  Claude/Cursor (`mcpServers`): `{"command": "stealth-browser-mcp", "args": []}`.
- **Идемпотентность:** есть шим — роль не трогает пакет. Обновление —
  `pipx upgrade browserstealthmcp`.
- **Безопасность:** сервер даёт доступ к cookies, локальным файлам и CDP,
  поэтому запускать его только по stdio с доверенным клиентом. HTTP-транспорт
  (`--transport http`) без `STEALTH_BROWSER_MCP_AUTH_TOKEN` наружу не
  выставлять.
- **Выключить MCP-сервер:** `stealth_browser_mcp_install: false` в
  `roles/ai_tools/defaults/main.yml`.

### ocr — AI-ревью по диффу

`alibaba/open-code-review` — CLI-ревьюер на Go. Берёт git-дифф (рабочее
дерево, коммит или диапазон ветвей), отдаёт изменённые файлы выбранной LLM
через агент с tools и печатает замечания с привязкой к строкам. Агент умеет
дочитывать файл целиком, искать по коду и смотреть соседние изменения, так
что ревью получается не по голому диффу.

```bash
ocr review                              # staged + unstaged + untracked
ocr review --from master --to my-branch # ветка против базы
ocr review --commit abc123              # один коммит
ocr scan path/to/dir                    # файлы целиком, без диффа
ocr delegate                            # спека ревью хост-агенту, без своего LLM
ocr viewer                              # WebUI с сохранёнными сессиями
```

Модель настраивается один раз, самим CLI (`~/.config/...` пишет `ocr config`)
— плейбук конфиг не создаёт, потому что ключ API у каждого свой:

```bash
ocr config set provider anthropic
ocr config set model claude-opus-4-6
ocr config set providers.anthropic.api_key "$ANTHROPIC_API_KEY"
# свой шлюз
ocr config set provider my-gateway
ocr config set custom_providers.my-gateway.url https://gateway.internal.com/v1
ocr config set custom_providers.my-gateway.protocol openai
```

По умолчанию `ocr review` ходит в облако выбранного провайдера. Если ревью
нужно без внешнего LLM — `ocr delegate` отдаёт спеку ревью тому агенту, в
котором вы уже работаете (opencode, Claude Code), и сам никуда не обращается.

Идемпотентность — как у остальных бинарников: есть `/usr/local/bin/ocr`,
роль ничего не качает. Не нужен — уберите элемент `ocr` из
`ai_tools_binaries` в `roles/ai_tools/defaults/main.yml`.

### kaeru — память агентов на графе

`LamantinAI/kaeru` — локальный демон памяти для агентов: типизированный граф
в CozoDB с двумя слоями (рабочий/архивный), историей утверждений и отзывов,
reasoning-цепочками, поиском по имени/ID и обходом графа, markdown-экспортом
в Obsidian-совместимый ZIP. Отдаёт 35 операций через MCP, HTTP и библиотеку
`kaeru-rig`. Опционально есть облачный слой для общей памяти команды;
локальная установка по умолчанию без auth.

Установка — без запуска `install.sh` из сети:

1. релизный `kaeru-v<version>-x86_64-unknown-linux-gnu.tar.gz` (единственный
   бинарник `kaeru-mcp`) ставится в `/usr/local/bin` ролью `binaries`;
2. юнит `~/.config/systemd/user/kaeru-mcp.service` кладётся из шаблона
   `roles/ai_tools/templates/kaeru-mcp.service.j2`, включается и запускается
   в scope `user`.

```bash
systemctl --user status kaeru-mcp
curl -s http://127.0.0.1:9876/mcp
kaeru-mcp --help
```

- **Хранилище:** `$XDG_DATA_HOME/kaeru` (обычно `~/.local/share/kaeru`),
  порт — `127.0.0.1:9876`, MCP — `/mcp`. Меняется в юните
  (`KAERU_MCP_LISTEN_PORT`, `KAERU_VAULT_PATH`).
- **Идемпотентность:** бинарник — по наличию файла; юнит — по содержимому
  шаблона; включение и запуск идут с `failed_when: false`, поэтому в ssh без
  `systemd-linger` установка не валится — сервис поднимется после входа или
  вручную (`kaeru-mcp`).
- **Выключить:** `kaeru_install: false`. Версия — из редиректа
  `releases/latest`; `app_update=true` обновляет бинарник, юнит
  перезапускается только при изменении шаблона.

### CloakBrowser — stealth-Chromium для Playwright/Puppeteer

`CloakHQ/CloakBrowser` — отдельный Chromium с патчами fingerprint на уровне
исходников C++ (canvas, WebGL, WebRTC, CDP-события) и флагом `humanize=True`,
который подключается вместо `playwright.chromium.launch()`. Полезен, когда
обычный Chrome палится антибот-защитой.

Ставится pipx-пакетом `cloakbrowser` в `~/.local/bin`:

```bash
cloakbrowser --help
cloakbrowser login          # привязать лицензионный ключ
```

- **Ключ:** каждый запуск требует лицензионный ключ (бесплатный по email).
  Первый интерактивный запуск спрашивает его сам, в CI/без TTY — переменная
  `CLOAKBROWSER_LICENSE_KEY`. Плейбук ставит только пакет.
- **Chromium (~200 МБ)** докачивается при первом запуске в локальный кэш, а
  не при установке пакета.
- **Выключить:** `cloakbrowser_install: false`.

### Конфиги

- **herdr** — копируется статичный `roles/ai_tools/files/herdr/config.toml`
  в `~/.config/herdr/config.toml`: отключён first-run onboarding
  (`onboarding = false`) и тосты идут через сам herdr
  (`[ui.toast] delivery = "herdr"`). Телеметрии у herdr в конфиге нет.
- **rtk** — генерируется динамически, без хранения готового TOML в `files/`
  (схема конфига может меняться между версиями): если `~/.config/rtk/config.toml`
  нет, запускается `rtk config --create` (актуальный дефолт), затем всегда
  `rtk telemetry disable` — телеметрия выключена и зафиксирован явный отказ от
  согласия (`consent: no`; дефолтный `--create` оставляет `consent: never asked`).
- **opencode-mem** — `~/.config/opencode/opencode-mem.jsonc`: статичный
  `files/opencode-mem.jsonc` (модель `Xenova/bge-m3`, квантование `q8`, порог
  `0.25`), если плагин ещё не создал свой файл; в существующем файле плейбук
  правит только эти три ключа, остальные настройки не трогает. Веса модели
  лежат в `~/.opencode-mem/data/.cache` и качаются задачей плейбука заранее.

### Интеграции с opencode

Роль `ai_tools` устанавливает три интеграции (каталог `~/.config/opencode/`
на этот момент уже создан ролью `opencode`):

- **herdr** — `herdr integration install opencode` кладёт в
  `~/.config/opencode/`: `plugins/herdr-agent-state.js` (состояние агента по
  unix-сокету), `herdr-tui-session.js`, `tui.jsonc` и `herdr-opencode/tui.js`.
- **rtk** — `rtk init -g --opencode --no-patch` кладёт `plugins/rtk.ts`:
  перехватывает `tool.execute.before` для команд bash/shell и переписывает их
  через `rtk hook opencode` (движок переписывания — в самом rtk).
- **opencode-mem** — `opencode plugin add opencode-mem` дописывает пакет в
  массив `plugins` файла `opencode.jsonc`; файл настроек и данные плагин
  создаёт себе сам (`~/.config/opencode/opencode-mem.jsonc`,
  `~/.opencode-mem/`).

Все эти команды идемпотентны (перезаписывают свои файлы тем же содержимым, а
`plugin add` на повторном прогоне печатает «already configured») и не
запрашивают подтверждения без TTY.

`rtk init -g --opencode` помимо плагина создаёт побочные файлы для Claude Code
(`~/.claude/CLAUDE.md`, `~/.claude/RTK.md`) и пустой шаблон
`~/.config/rtk/filters.toml` — opencode-плагину они не нужны, поэтому роль
удаляет их отдельными задачами.

---

## Глобальные skills для opencode

Роль `skills` ставит **глобальные skills для opencode** — инструкции-плагины
(каталоги с `SKILL.md`), которые подсказывают агенту, как работать с разными
инструментами и задачами. Skills ставятся CLI [`skills`](https://www.npmjs.com/package/skills)
(через `npx`, без глобальной установки CLI):

```bash
npx skills add <git-репозиторий> -g -y -a opencode -s <skill-1,skill-2,...>
```

Флаги: `-g` — глобально для пользователя, `-y` — без вопросов, `-a opencode` —
с привязкой к агенту opencode, `-s` — конкретные skills из репозитория. CLI
сам клонирует репозиторий источника, поэтому нужны `git` (роль `git`) и `npm`
(роль `runtimes`), а также **SSH-ключ к GitHub** — источники заданы SSH-URL
(как в рабочем окружении, откуда список воспроизведён).

Skills складываются в `~/.agents/skills`, учёт установленного — в
lock-файле `~/.agents/.skill-lock.json`. Идемпотентность: перед установкой
роль читает lock-файл и пропускает источники, чьи skills уже установлены.
Удалить запись из lock-файла = переустановить соответствующий источник.
При установке задаётся `INSTALL_INTERNAL_SKILLS=1`: CLI по умолчанию
пропускает skills с `metadata.internal: true` в frontmatter, и для них
установка не нашла бы имена в списке.

Список в `roles/skills/defaults/main.yml` (`skills_sources`) — реплика
рабочего окружения: **69 skills из 17 репозиториев**:

| Источник | Skills |
|---|---|
| [elastic/agent-skills](https://github.com/elastic/agent-skills) | 24 |
| [obra/superpowers](https://github.com/obra/superpowers) | 15 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 7 |
| [dietrichgebert/ponytail](https://github.com/dietrichgebert/ponytail) | 6 |
| [victoriametrics/skills](https://github.com/victoriametrics/skills) | 5 |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 1 |
| [artwist-polyakov/polyakov-claude-skills](https://github.com/artwist-polyakov/polyakov-claude-skills) | 1 |
| [blader/humanizer](https://github.com/blader/humanizer) | 1 |
| [blurman-ai/clean-contour](https://github.com/blurman-ai/clean-contour) | 1 |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | 1 |
| [elsvv/yandex-cloud-cli-skill](https://github.com/elsvv/yandex-cloud-cli-skill) | 1 |
| [jeffallan/claude-skills](https://github.com/jeffallan/claude-skills) | 1 |
| [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) | 1 |
| [testland/qa](https://github.com/testland/qa) | 1 |
| [theclaymethod/unslop](https://github.com/theclaymethod/unslop) | 1 |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | 1 |
| [Vladimir-Human/humanizer-ru](https://github.com/Vladimir-Human/humanizer-ru) | 1 |

Проверка после установки:

```bash
ls ~/.agents/skills                    # все ожидаемые skills на месте
npx skills ls -g                       # список установленных глобальных skills
```

Применить только skills: `ansible-playbook -K playbook.yml --tags skills`
(сначала должен быть выполнен тег `runtimes` — нужен `npm`).

---

## Глобальные правила для opencode (`AGENTS.md`)

Роль `opencode` кладёт `~/.config/opencode/AGENTS.md` — инструкции, которые
opencode применяет во **всех** проектах (правила безопасности, работа с
Kubernetes и git, доступные зоны, принципы работы и т.п.). Проектный `AGENTS.md`
эти правила дополняет, а не отменяет.

Источник — `roles/opencode/files/AGENTS.md`: правки вносятся в репозиторий,
а плейбук приводит файл на машине к этому состоянию (локальные изменения
перезаписываются). Применить только правила:
`ansible-playbook -K playbook.yml --tags opencode`.

---

## Аудио: HushMic (шумоподавление микрофона)

Роль `audio` ставит **HushMic** (`Fovty/HushMic`) — шумоподавление микрофона
реального времени поверх PipeWire. Добавляет виртуальный микрофон, который
убирает шум клавиатуры, вентиляторов и фоновые голоса (модель DPDFNet, обработка
на CPU, ~80 мс задержки).

Ставится официальным `.deb`-пакетом из GitHub-релиза (бинарник, LADSPA-плагин,
модели, иконки и пользовательский systemd-юнит). Версия берётся из редиректа
`releases/latest`, повторный запуск не переустанавливает (apt сверяет версию).

В приложениях (Discord, OBS, браузер) выберите устройство ввода **HushMic**.
Управление:

```bash
systemctl --user status hushmic      # пользовательский юнит
systemctl --user restart hushmic
hushmic --help                       # флаги CLI (--headless и др.)
```

Требуются PipeWire + WirePlumber (ставятся ролью) и, для иконки в трее, поддержка
StatusNotifierItem (в GNOME — расширение AppIndicator). Без трея HushMic всё
равно работает — им можно управлять из командной строки.

---

## Яндекс Музыка RS (неофициальный клиент Яндекс Музыки)

Роль `audio` ставит ещё и **Яндекс Музыку RS** (`SpolzerMod/yamusic-rs`) —
неофициальный десктопный клиент Яндекс Музыки на Rust и Slint. Он повторяет
интерфейс официального Electron-приложения, но рисует окно сам: один процесс
и ~65 МБ памяти вместо ~850 МБ и семи процессов, пакет ~10 МБ (в установленном
виде ~32 МБ). Linux-сборка — **бета**, основной платформой у автора остаётся
Windows.

Ставится официальным `.deb` из GitHub-релиза (`yamusic-rs_<версия>-1_amd64.deb`).
Пакет приносит `/usr/bin/yamusic-rs`, `.desktop` и иконки, так что приложение
появляется в меню как «Яндекс Музыка RS». Зависимости (ALSA, Wayland/X11,
`libxkbcommon`, `libfontconfig1`, `libfreetype6`) подтягивает apt. Нужна
glibc 2.35+ — на Ubuntu 26.04 условие выполнено.

Версию и обновление ведёт роль `github_deb`: тег берётся из редиректа
`releases/latest`, установленная версия сравнивается с релизной через
`dpkg --compare-versions`, поэтому повторный прогон подтянет новый релиз, а
ту же версию переустанавливать не будет. Применить только аудиоприложения:

```bash
ansible-playbook -K playbook.yml --tags audio
```

Что учесть:

- **Аккаунт.** Вход по коду: приложение показывает код, его нужно ввести на
  [ya.ru/device](https://ya.ru/device). Полные треки доступны с подпиской Плюс,
  без неё сервер отдаёт 30-секундные отрывки.
- **Токен** хранится в системной связке ключей (Secret Service) и уходит только
  на `yandex.ru` / `yandex.net` по HTTPS; телеметрии нет.
- **Данные** — `~/.config/yamusic-rs` (настройки, вход, лог), кэш —
  `~/.cache/yamusic-rs`, скачанные треки по умолчанию в
  `~/Музыка/Яндекс Музыка`.
- **Трея нет** — закрытие окна закрывает приложение. Медиаклавиши и виджет
  плеера в GNOME/KDE работают через MPRIS.
- **Обновление** делает плейбук (см. выше) или кнопка «Обновить» в приложении:
  на Linux она открывает страницу релиза.
- **Удаление:** `sudo apt remove yamusic-rs`; настройки и токен удаляются
  вручную (см. пути выше и «Пароли и ключи»).

---

## Офисные приложения ArtCraft (WordCraft, GridCraft, DeckCraft)

Роль `craft` ставит три десктопных редактора из организации
[ArtCraft](https://github.com/storytold): чистые переписывания Word, Excel и
PowerPoint на Rust (egui, без Electron и без web view), под Apache-2.0.

| Приложение | Аналог | Форматы |
|---|---|---|
| [WordCraft](https://github.com/storytold/wordcraft) | Microsoft Word | `.docx` (чтение/запись), `.doc` 97-2003 (чтение), `.odt`, `.rtf`, `.html`, `.md`, `.tex`, `.txt` — импорт и экспорт; PDF и PNG на экспорт |
| [GridCraft](https://github.com/storytold/gridcraft) | Microsoft Excel | `.xlsx` — родной формат (стили, формулы, диаграммы, сводные), `.csv`/`.tsv`; чтение `.xls` 97-2003, `.xlsb` и `.ods` (значения); PDF на экспорт |
| [DeckCraft](https://github.com/storytold/deckcraft) | Microsoft PowerPoint | `.pptx` (чтение/запись), PDF на экспорт (слайды, страницы заметок, раздатки) |

**Все три приложения ставятся по умолчанию.** WordCraft нужен ещё и ради
`wordcraft-cli` — headless-конвертера для агента: `text`
вытаскивает текст, `convert` пишет PDF/ODT/RTF/HTML/MD/TEX/TXT/PNG, `inspect`
отдаёт структуру JSON. Отдельного артефакта с одним CLI upstream не
выпускает: в пакет кладутся оба бинарника, `usr/bin/wordcraft` и
`usr/bin/wordcraft-cli`, поэтому GUI приезжает вместе с CLI (иконка в меню
GNOME, alpha). Так же устроены GridCraft и DeckCraft — в их пакетах есть
`gridcraft-cli` и `deckcraft-cli`. Не нужны — выключаются флагами, каждый
отдельно:

```bash
# без WordCraft (и без wordcraft-cli)
ansible-playbook -K playbook.yml -t craft -e wordcraft_install=false

# без GridCraft и DeckCraft
ansible-playbook -K playbook.yml -t craft \
  -e '{"gridcraft_install": false, "deckcraft_install": false}'
```

Флаги: `wordcraft_install`, `gridcraft_install`, `deckcraft_install` — все по
умолчанию `true`.

Пакеты ставятся официальными `.deb` из GitHub-релизов: `.deb` WordCraft на
~1.7 МБ больше `tar.gz` (114.5 против 112.8 МБ), зато apt подтягивает
зависимости (`libc6`, `libgcc-s1`, `libxkbcommon0`, `libvulkan1 | libegl1`,
у DeckCraft ещё `libasound2t64`) и регистрирует `.desktop`/MIME. Текущие
размеры x86_64-пакетов: WordCraft 114.5 МБ, GridCraft 51.2 МБ, DeckCraft
101.2 МБ. Версия берётся из редиректа `releases/latest`, повторный запуск
приложение не переустанавливает: если `/usr/bin/<name>` уже есть, шаг
пропускается. Отдельно проверяется, что на месте `<name>-cli`: если GUI
остался, а CLI пропал, пакет переустанавливается.

Что учесть:

- **Статус — alpha.** Все три в README числятся alpha (у DeckCraft бейдж
  «early development»). Открыть чужой `.docx`, `.xlsx` или `.pptx` и
  посмотреть содержимое они умеют; для ежедневной работы надёжнее
  LibreOffice.
- **Wayland.** WordCraft и DeckCraft по умолчанию идут через XWayland (нужен
  drag-and-drop файлов), нативный Wayland включается переменной
  `<NAME>_WAYLAND=1`, например `WORDCRAFT_WAYLAND=1 wordcraft`. GridCraft
  выбирает бэкенд сам по `WAYLAND_DISPLAY`.
- **GPU.** Рендер через wgpu (Vulkan/EGL). Если окно не открывается или
  артефакты — `WGPU_BACKEND=gl` или установить `mesa-vulkan-drivers`.
- **Агенты и скрипты.** У каждого приложения есть CLI и MCP-сервер, так что
  документ можно прочитать, собрать или сконвертировать без GUI:

  ```bash
  catdoc report.doc                              # legacy .doc (роль shell)
  wordcraft-cli text report.docx                 # .docx → текст
  wordcraft-cli text report.doc                  # legacy .doc тем же движком
  wordcraft-cli convert report.docx report.pdf   # docx → pdf/odt/rtf/html/md/tex/txt/png
  gridcraft-cli cat book.xlsx --range B4:F15     # значения таблицы
  deckcraft-cli commands format                  # список команд CLI
  ```

---

## Markdown-редакторы Zettlr и MarkText и читалка TextFold

Роль `markdown` ставит два десктопных редактора Markdown и читалку TextFold:

- **Zettlr** (`Zettlr/Zettlr`) — для заметок и научных текстов: Zettelkasten,
  перекрёстные ссылки, цитаты, экспорт в PDF/LaTeX/DOCX.
- **MarkText** (`marktext/marktext`) — минималистичный WYSIWYG-редактор в духе
  Typora, без лишних панелей.

Оба ставятся официальным `.deb` из GitHub-релиза. Версия берётся из редиректа
`releases/latest`, зависимости (GTK, NSS, `libsecret-1-0`, `libasound2t64` и
др.) подтягивает apt. В пакете — бинарник, `.desktop` и иконки, так что
приложения появляются в меню GNOME. Повторный запуск ничего не
переустанавливает: если `/usr/bin/zettlr` или `/usr/bin/marktext` уже есть,
шаг пропускается.

Ассеты есть под x86_64 и aarch64 (Zettlr: `Zettlr-<version>-amd64.deb` /
`-arm64.deb`; MarkText: `marktext-linux-<version>.deb` /
`marktext-linux-arm64-<version>.deb`).

Кроме редакторов роль ставит читалку **TextFold** (`chenxiachan/textfold`).

TextFold сворачивает статью, PDF, веб-страницу или ответ агента в пять
уровней — полный текст, ключевые предложения, суть абзаца, тезис раздела и
карту тем; каждый уровень раскрывается обратно до авторских слов.
`textfold get <ссылка|файл>` отдаёт документ агенту по уровню,
`textfold export` — один самодостаточный HTML.

В GitHub-релизах только macOS и Windows, поэтому ставится PyPI-пакет через
pipx: изолированный venv и шим `textfold` в `~/.local/bin`, sudo не нужен.
Пакет — локальный веб-сервис на `127.0.0.1:3017`, поэтому роль кладёт и
включает пользовательский systemd-юнит `textfold.service`:

```bash
systemctl --user status textfold
textfold --version
textfold serve --port 3017   # если запускать вручную, без юнита
```

- **Модель.** Уровни пишет модель, которую TextFold находит сама (Claude Code,
  Codex, Pi, WorkBuddy) или которую подключают в Settings: Anthropic, OpenAI,
  DeepSeek, Qwen, Zhipu GLM, Kimi, MiniMax, Google, Ollama или любой
  OpenAI-совместимый endpoint. Плейбук ключи и провайдеров не пишет.
- **Данные** — `~/.local/share/textfold`: библиотека, настройки и `server.json`
  с адресом запущенного сервера.
- **Выключить:** `textfold_install: false` в `roles/markdown/defaults/main.yml`;
  обновление пакета — `pipx upgrade textfold`.

Ещё роль ставит два CLI-конвертера PDF ↔ Markdown:

- **pdf2md** (`fjacquet/pdf2md`) — PDF в Markdown: заголовки, списки, таблицы,
  разбивка по страницам. Разбор идёт ONNX-моделью layout detection с
  rule-based запасным вариантом, для страниц-картинок есть OCR; модели
  докачиваются при первом запуске. Ставится готовым бинарником из
  GitHub-релиза (x86_64 и arm64).
- **pdfcli** (крейт `pdfrs`) — PDF в Markdown и обратно, плюс merge/split,
  rotate, watermark, извлечение текста и поиск по документу. Чистый Rust, без
  Poppler, PDFium и LaTeX. Готовых бинарников нет — ставится
  `cargo install pdfrs`, первая установка компилирует ~135 крейтов и занимает
  несколько минут.

Оба кладутся в `/usr/local/bin`, повторный запуск их не переустанавливает.
Команда у крейта `pdfrs` называется `pdfcli`:

```bash
pdf2md document.pdf document.md
pdfcli pdf-to-md document.pdf document.md
pdfcli md-to-pdf document.md document.pdf
```

Применить только эти приложения:

```bash
ansible-playbook -K playbook.yml --tags markdown
```

---

## Диагностика сетевых блокировок (rkn-block-checker)

Роль `network` ставит **rkn-block-checker** (`MayersScott/rkn-block-checker`) —
CLI, который определяет, каким способом провайдер режет доступ: DNS-подмена,
TCP reset, TLS DPI по SNI или заглушка провайдера. Проверка идёт по слоям
(DNS, TCP, TLS, HTTP). Пакета в apt и релизных бинарников нет — ставится из
PyPI через pipx в изолированное окружение, шим `rkn-check` кладётся в
`~/.local/bin`.

```bash
rkn-check                       # проверить список сайтов и вынести вердикт
rkn-check startweb --port 8080  # локальный веб-дашборд (по умолчанию :7777)
```

---

## Диагностика DNS и разрешения имён (gai, dnsglobe)

Роль `network` дополнительно ставит два инструмента для разбора проблем с DNS:

- **gai** (`casablanque-code/gai`) — инспектор `getaddrinfo`: показывает, каким
  путём ОС на самом деле превращает имя в IP (`/etc/hosts`, mDNS,
  systemd-resolved, DNS), и сверяет его с независимым DNS-запросом. Ловит
  случай, когда `dig` отвечает, а процесс резолвит иначе (например, имя
  перехвачено в `/etc/hosts`). Без LD_PRELOAD/eBPF/ptrace — читает те же
  конфиги, что и ОС.
- **dnsglobe** (`514-labs/dnsglobe`) — TUI-проверка распространения DNS-записи:
  параллельно опрашивает 34 публичных резолвера по миру, сравнивает ответы,
  показывает расхождения и прогресс на карте, умеет watch-режим до полной
  пропагации. В узком терминале рисует вращающийся глобус, в широком — плоскую
  карту.

```bash
gai doctor testhost.local       # разобрать путь разрешения имени и вынести вердикт
gai explain example.com         # только путь разрешения, без вердикта
dnsglobe example.com            # проверка распространения A-записи
dnsglobe example.com A --once   # один прогон текстом (без TTY)
```

---

## Аудит SSH: ssh-audit

**ssh-audit** (`jtesta/ssh-audit`, роль `network`, через pipx) проверяет
конфигурацию SSH-сервера или клиента: версии протокола, key exchange, шифры,
MAC, известные уязвимости и рекомендации по усилению.

```bash
ssh-audit example.com           # аудит SSH-сервера
ssh-audit -c                    # аудит локального клиента (~/.ssh/config)
ssh-audit -j example.com        # JSON-вывод для автоматизации
```

---

## DAST: проверка запущенного приложения

DAST-сканеры работают по URL уже поднятого приложения: ищут известные CVE,
инъекции в параметрах и падения. Они не заменяют SAST/SCA из роли `secrets`
и не находят бизнес-логику, broken access control и десериализацию надёжно.
Сканировать только свои стенды: active scan ZAP, `nuclei -dast`, wapiti,
sqlmap и schemathesis меняют данные, а нагрузочные прогоны могут уронить
сервис.

Роль `dast` ставит `nuclei`, `hetty`, `openapi-tui`, `vacuum` и `oasdiff`
(бинарники), `wapiti` и
`schemathesis` (pipx), `sqlmap` (apt), EvoMaster (jar ~110 МБ и обёртка) и ZAP
(Docker-образ `ghcr.io/zaproxy/zaproxy:stable`). Для нагрузки отдельный
инструмент не нужен: в роли `network` уже есть `k6`. Образ ZAP занимает больше
гигабайта; если он не нужен, роль можно запустить с `-e dast_zap_install=false`.
EvoMaster отключается через `-e dast_evomaster_install=false`.
`--tags dast` на машине без Docker пропустит ZAP, а без Java — EvoMaster, и
поставит остальные сканеры.

Рабочая последовательность: быстрый проход `nuclei` по CVE/RCE → пассивный
baseline ZAP → активный API scan по OpenAPI → `nuclei -dast`/`wapiti` по
параметрам → `sqlmap` для доказательства RCE через SQLi → `schemathesis` для
падений и 5xx → EvoMaster для API-фаззинга по OpenAPI и генерации тестов →
`k6` только отдельным окном и с abort-критериями. Спецификацию перед
API scan удобно открыть в `openapi-tui`: видно, какие эндпоинты и параметры
описаны, и можно вручную отправить запрос с токеном, чтобы отличить ошибку
приложения от находки фаззера.

### hetty — перехват и правка запросов вручную

`hetty` — MITM-прокси с веб-интерфейсом: видно каждый запрос, ответ и заголовки,
запрос можно поправить, повторить и сохранить в историю. Это не сканер:
он нужен там, где надо руками проверить, что приложение делает с подменённым
параметром, cookie или телом, — до того же `nuclei`/`wapiti`.

```bash
hetty                               # прокси и UI на http://localhost:8080
hetty --addr 127.0.0.1:9090         # другой адрес
hetty cert install                  # CA в системный trust store (нужен sudo)
```

HTTPS-трафик расшифровывается после `hetty cert install` (для Firefox — с
`--firefox`, для Java — с `--java`). Клиент или браузер направляются на прокси
`127.0.0.1:8080`, база и сертификаты лежат в `~/.hetty`. Прокси не сканирует
сам и не меняет запросы без команды, поэтому его можно держать запущенным при
обычной отладке.

### nuclei — известные CVE/RCE и DAST-фаззинг

```bash
# Известные CVE/RCE по шаблонам
nuclei -u http://127.0.0.1:8080 -tags cve,rce -severity critical,high \
  -jsonl -o reports/nuclei-cve.jsonl

# Фаззинг параметров (меняет данные), агрессия low и лимит запросов
nuclei -u http://127.0.0.1:8080 -dast -fa low -rl 50 \
  -jsonl -o reports/nuclei-dast.jsonl

# Проверка API по OpenAPI
nuclei -l openapi.yaml -im openapi -tags cve,rce \
  -jsonl -o reports/nuclei-api.jsonl
```

Шаблоны скачиваются при первом запуске и обновляются автоматически
(`nuclei -update-templates` — вручную). `dos`-шаблоны исключены по умолчанию:
`-include-tags dos` включает их осознанно. Blind RCE/SSRF проверяются через
Interactsh; публичные серверы (`oast.pro` и др.) могут быть недоступны из
целевой сети, тогда нужен свой `interactsh-server`.

### katana — сбор URL до nuclei

Сканеры видят только тот URL, который им дали. `katana` обходит стенд как
браузер: тянет HTML, парсит JS-файлы и вытаскивает ссылки, а с `-kf` — ещё
`robots.txt` и `sitemap.xml`; полученный список путей идёт в `nuclei`, `ffuf`
и `feroxbuster`.

```bash
# Пассивный обход: HTML-ссылки и эндпоинты из JS-файлов
katana -u http://127.0.0.1:8080 -jc -silent -o reports/katana-urls.txt

# Найденный список сразу в шаблонный сканер
katana -u http://127.0.0.1:8080 -jc -silent | nuclei -tags cve,rce

# Формы и поля ввода: к каждой записи добавляются form/input/textarea/select
katana -u http://127.0.0.1:8080 -jc -fx -o reports/katana-forms.txt
```

`katana` только собирает ссылки и ничего не меняет на стенде: это разведка
перед сканерами, без неё `nuclei` и `ffuf` видят лишь стартовую страницу.
Глубину ограничивает `-d` (по умолчанию 3), параллельность — `-c`, а `-hl`
включает headless-обход через Chromium для страниц, которые целиком
собираются на клиенте из JS (`google-chrome` в плейбуке уже стоит).

### OWASP ZAP — общий DAST

ZAP запускается официальным Docker-образом. Внутри уже есть Java и скрипты
`zap-baseline.py`, `zap-api-scan.py`, `zap-full-scan.py`. На Linux нужен
`--network host`, иначе `127.0.0.1` внутри контейнера — это сам контейнер.
Порт `-P 8090` обязателен, если приложение занимает 8080.

```bash
mkdir -p reports

# Пассивный baseline: без атак, минуты
docker run --rm --network host -v "$PWD/reports:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
  -t http://127.0.0.1:8080 -P 8090 \
  -r baseline.html -J baseline.json

# API scan: active scan по OpenAPI, десятки минут
docker run --rm --network host -v "$(pwd):/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable zap-api-scan.py \
  -t /zap/wrk/openapi.yaml -f openapi -O 127.0.0.1:8080 -P 8090 \
  -r api.html -J api.json

# Full scan: часы, только вручную и с ограничением длительности
docker run --rm --network host -v "$PWD/reports:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable zap-full-scan.py \
  -t http://127.0.0.1:8080 -P 8090 \
  -r full.html -J full.json \
  -z "-config scanner.maxScanDurationInMins=30"
```

API scan понимает OpenAPI, SOAP и GraphQL (`-f openapi|soap|graphql`). Если в
спеке прод-хост, переопределить его через `-O` или собрать спеку с локальным
`servers`. Авторизованные сканы — через context-файл (`-n`) или Automation
Framework; токены и куки держать вне репозитория. Коды возврата: 0 — чисто,
1 — FAIL, 2 — WARN, 3 — ошибка запуска.

### wapiti — второй движок без Docker

```bash
# Список модулей и их имён
wapiti --list-modules

# RCE-классы: exec, sql, xxe, ssrf, file, upload
wapiti -u http://127.0.0.1:8080 \
  --swagger http://127.0.0.1:8080/openapi.json \
  -m common,exec,sql,xxe,ssrf,file,upload \
  --flush-session --max-attack-time 300 --scan-force normal \
  -f md -o reports/wapiti.md -dr 1
```

`--flush-session` нужен для повторяемого прогона: по умолчанию wapiti
продолжает прошлую сессию по тому же URL и scope. Авторизация — `--jwt`,
`-c cookie.json`, `--form-user`/`--form-password`, `-H`. Для SSRF/Log4Shell
по умолчанию используется внешний endpoint `wapiti3.ovh`; если целевая сеть
его не видит, задайте свой через `--external-endpoint`.

### sqlmap — SQLi и доказательство RCE

```bash
# Один параметр
sqlmap -u "http://127.0.0.1:8080/api/items?id=1" --batch --level=3 --risk=2

# Авторизованный запрос целиком (заголовки и куки) — файл chmod 600
sqlmap -r request.txt --batch --level=5 --risk=3

# Доказательство RCE, только при разрешении и правах БД
sqlmap -r request.txt --batch --os-shell
```

`--risk=3` и `--os-shell` меняют данные и могут выполнить код на сервере.
Только свои стенды и только с письменным разрешением.

### schemathesis — падения и 5xx в API

```bash
st run openapi.yaml --url http://127.0.0.1:8080 \
  --checks all --max-time 600 --rate-limit 20/s \
  --report html --report-dir reports/schemathesis

# Повторить найденные падения
st replay
```

Проверки включают `not_a_server_error`, `ensure_resource_availability`,
`use_after_free`, `object_level_authorization`; каждая находка идёт с curl
для воспроизведения. Это не сканер CVE, а фаззинг контракта API — он же
закрывает часть п. 4 в `TODO.md`.

### vacuum и oasdiff — проверка спецификации до фаззинга

Фаззеры верят спецификации: если в ней пропущен ответ, противоречивый тип или
не описана схема ошибки, `schemathesis` и EvoMaster будут искать падения
не там, а `zap-api-scan.py` — ругаться на несуществующие ручки. Поэтому спеку
сначала проверяют линтером, а перед релизом — на breaking changes.

```bash
# Ошибки в самой спецификации: подробный вывод в терминале
vacuum lint openapi.yaml -d
# HTML-отчёт для ревью (--format не сочетается с -d)
vacuum lint openapi.yaml --format html -o reports/vacuum.html
# Свой набор правил вместо встроенных
vacuum lint openapi.yaml --ruleset ruleset.yaml

# Что сломается у клиентов между версиями (код возврата 1 при breaking)
oasdiff breaking base.yaml head.yaml --fail-on ERR
# Полный changelog изменений для ревью
oasdiff changelog base.yaml head.yaml
```

`vacuum` — про одну спеку (`-d` — подробный вывод, `--ruleset` — свой набор
правил), `oasdiff` — про разницу двух версий. Это те же роли, что `yamllint` и
`buf breaking` в остальном плейбуке: линтер и проверка совместимости.

### DoS и нагрузка

Отдельного «DoS-сканера» нет: `nuclei -include-tags dos` проверяет известные
шаблоны, а ёмкость и деградацию меряет `k6`:

```bash
k6 run --summary-export reports/k6.json load.js
```

Нагрузочный прогон — отдельное окно с abort-критериями по 5xx и latency, не
на проде. `--rate-limit` в schemathesis и `-rl` в nuclei защищают стенд от
случайного заваливания.

### Отчёты и секреты

Отчёты содержат тела запросов и ответов, токены и PII. Каталог `reports/`
в `.gitignore`; перед передачей отчёт нужно почистить. Токены не передавать
через `-H` в командной строке (видно в `ps` и history): ZAP context-файл,
nuclei `-sf`, wapiti cookie-файл/`--jwt`, sqlmap `-r request.txt`,
schemathesis `--auth-wfc`.

---

## Фаззинг API и кода

Фаззинг ищет не известные CVE, а падения на неожиданном входе: panic,
assert, segfault, OOM, зависание. DAST из предыдущего раздела работает по
URL запущенного приложения; фаззинг идёт по спецификации API или запускает
сам код с инструментированным harness. Это дополнение к SAST/SCA, а не
замена: статический анализ не докажет, что вход доходит до уязвимого кода.

Роль `fuzz` ставит `afl++`, `clang` с libFuzzer, `zzuf` и `Jazzer`
(Java/Kotlin). EvoMaster ставится ролью `dast`. `go test -fuzz` уже входит в
Go, `Atheris` проект добавляет сам, `cargo-fuzz` требует nightly и в
плейбук не входит. Фаззеры не запускаются сами: для каждого проекта нужен
harness и corpus.

Фаззить только свой код и свои стенды. Входы и крэши могут содержать
токены, PII и фрагменты памяти; `corpus/`, `artifacts/` и `reports/` держать
вне Git (`.gitignore`), как и отчёты DAST.

### EvoMaster — API по OpenAPI/GraphQL

EvoMaster работает в black-box режиме по HTTP и не требует драйвера внутри
приложения:

```bash
mkdir -p reports/evomaster

evomaster --schema openapi.yaml --base http://127.0.0.1:8080 \
  --maxTime 300s --ratePerMinute 60 \
  --outputFormat JAVA_JUNIT_4 --outputFolder reports/evomaster
```

`--schema` принимает локальный файл, `file://` или URL; `--base` — корень
стенда. Для GraphQL укажите `--problemType GRAPHQL` и endpoint в `--base`
(например, `http://127.0.0.1:8080/graphql`). `--outputFormat` также умеет
`JAVA_JUNIT_5`, `KOTLIN_JUNIT_4/5`, `JS_JEST`, `JS_PLAYWRIGHT` и
`PYTHON_UNITTEST`; сгенерированные тесты можно сложить в репозиторий и
перезапускать без фаззера. `--maxTime` и `--ratePerMinute` ограничивают
длительность и нагрузку. White-box режим требует EvoMaster Driver и
инструментирования приложения — для него нужен отдельный проект, здесь
описан только black-box.

### schemathesis в процессе тестов

`st` из pipx изолирован и не импортируется в проект. Чтобы гонять
property-based проверки in-process, без поднятого HTTP-стенда, добавьте
пакет в dev-зависимости:

```bash
uv add --dev schemathesis pytest
```

```python
# tests/test_api_fuzz.py
import schemathesis
from myapp.asgi import app

schema = schemathesis.openapi.from_asgi("/openapi.json", app)


@schema.parametrize()
def test_api(case):
    case.call_and_validate()
```

Для WSGI-приложения используйте `schemathesis.openapi.from_wsgi`. Запуск:
`uv run pytest -q tests/test_api_fuzz.py`. Проверки те же, что у `st run`:
5xx, нарушения схемы, таймауты и повторяемый curl в отчёте, но без сети и
Docker.

### Jazzer — Java/Kotlin

Jazzer ищет метод `fuzzerTestOneInput` в указанном классе:

```java
public class ParserFuzz {
    public static void fuzzerTestOneInput(byte[] data) {
        // вызвать разбор data; исключения-баги Jazzer покажет сам
    }
}
```

```bash
javac -g -cp build/classes -d build/classes src/test/java/ParserFuzz.java

jazzer --cp=build/classes --target_class=ParserFuzz \
  --corpus_dir=corpus --max_total_time=60
```

Jazzer требует Java из роли `runtimes`; команда `jazzer` — обёртка,
которая запускает лаунчер вместе с `jazzer_standalone.jar` из `/opt/jazzer`.
Поддерживаются Java-санитайзеры и воспроизведение найденного входа.

### AFL++ и libFuzzer — нативный код

AFL++ инструментирует сборку и ищет покрытие через общую память:

```bash
AFL_USE_ASAN=1 AFL_USE_UBSAN=1 afl-clang-fast -g -O1 harness.c -o harness

mkdir -p corpus findings
afl-fuzz -i corpus -o findings -- ./harness @@
```

`@@` заменяется на путь к мутируемому файлу. Для скорости используйте
persistent mode (`__AFL_LOOP`) и не запускайте GUI-приложения. Найденные
входы лежат в `findings/default/crashes/` и `findings/default/hangs/`.

libFuzzer работает в процессе и обычно быстрее для небольших функций:

```bash
clang -g -O1 -fsanitize=fuzzer,address,undefined harness.c -o fuzz_harness
./fuzz_harness -max_total_time=60 corpus/
```

Первые входы можно положить в `corpus/` руками; libFuzzer сам расширяет
корпус. `-jobs`/`-workers` распараллеливают прогон, но на ноутбуке обычно
достаточно одного процесса.

### zzuf — быстрые мутации без пересборки

zzuf перехватывает чтение файлов и портит байты на лету:

```bash
zzuf -r 0.01 -s 1000 -T 10 -- ./parser input.bin
```

`-r` — доля изменённых байт, `-s` — seed для воспроизведения, `-T` —
таймаут. Покрытия нет, поэтому zzuf хорош для быстрой проверки парсеров и
форматов, а не для систематического поиска глубоких багов.

### Go — встроенный фаззинг

В Go фаззер уже входит в toolchain:

```go
func FuzzParse(f *testing.F) {
    f.Add([]byte("seed"))
    f.Fuzz(func(t *testing.T, data []byte) {
        _, _ = Parse(data)
    })
}
```

```bash
go test -fuzz=FuzzParse -fuzztime=30s ./...
```

Go пишет найденные входы в `testdata/fuzz/FuzzParse/`; обычный `go test`
потом проигрывает их как регрессию. Один прогон — один target, для
нескольких целей запускайте команды отдельно.

### Python — Atheris

Atheris — библиотека, а не CLI, поэтому ставится в проект:

```bash
uv add --dev atheris
```

```python
# fuzz_parser.py
import sys

import atheris

from myapp.parser import parse


def test_one_input(data: bytes) -> None:
    fdp = atheris.FuzzedDataProvider(data)
    try:
        parse(fdp.ConsumeUnicodeNoSurrogates(200))
    except (TypeError, ValueError):
        pass


atheris.Setup(sys.argv, test_one_input)
atheris.Fuzz()
```

```bash
uv run python fuzz_parser.py -max_total_time=60
```

Исключения, которые являются штатной валидацией, глушите в harness;
падения интерпретатора и необработанные исключения Atheris сохраняет в
`crash-*`.

### Rust — ограничение nightly

apt-пакет Rust в Ubuntu 26.04 — стабильный (1.93.1), а `cargo-fuzz`
требует nightly: libFuzzer в Rust использует нестабильные флаги компилятора.
Поэтому `cargo-fuzz` в плейбук не входит — отдельный nightly toolchain
сломал бы правило «ставим системный Rust» и потянул вторую установку. Если
coverage-guided фаззинг на Rust нужен, это отдельная задача (см. п. 4 в
[`TODO.md`](TODO.md)):

```bash
rustup toolchain install nightly
cargo +nightly install cargo-fuzz
cargo +nightly fuzz run fuzz_target
```

`cargo-afl` (обёртка над установленным AFL++) собирается на стабильном Rust,
но тоже ставится отдельно: `cargo install cargo-afl`. В плейбук он не
входит, потому что это cargo-крейт и для него всё равно нужен harness.

На стабильном Rust остаются property-тесты через `proptest`/`arbitrary`, но
это не coverage-guided фаззинг. Для проверки panic имеет смысл отдельная
сборка с `panic = "abort"`; санитайзеры (`-Zsanitizer=address`) тоже
доступны только на nightly.

### Что не поставлено

- `honggfuzz`, `radamsa`, `RESTler` — нет готового linux-amd64 бинарника или
  пакета; см. [`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md).
- `GraphQLer` — требует Python `<3.13`, в Ubuntu 26.04 системный Python
  3.14; см. [`TODO-incompatible-ubuntu-2604.md`](TODO-incompatible-ubuntu-2604.md).
- `ClusterFuzzLite`/`OSS-Fuzz` — CI-инфраструктура с хранилищем корпусов и
  кластером воркеров, а не локальный CLI; см.
  [`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md).
- `cargo-fuzz` — требует nightly; `cargo-afl` — отдельная установка на
  стабильном Rust, оба описаны выше.

---

## direnv — инструкция

Хук `direnv` уже прописан в `~/.config/devops-shell.sh`:

```bash
eval "$(direnv hook bash)"
```

Как пользоваться:

1. В каталоге проекта создайте `.envrc`, например:

   ```bash
   export AWS_PROFILE=dev
   export KUBECONFIG=~/.kube/config-dev
   export TF_WORKSPACE=dev
   ```

2. Разрешите его:

   ```bash
   direnv allow
   ```

3. При входе в каталог переменные подхватываются автоматически, при выходе — снимаются.

Важно:

- После **каждого** изменения `.envrc` нужно снова выполнить `direnv allow`
  (direnv следит за хешем файла).
- При первом заходе в каталог с неразрешённым `.envrc` будет сообщение
  `direnv: error .envrc is blocked` — это нормально.
- Не храните в `.envrc` секреты, попадающие в git. Для секретов используйте
  отдельный неотслеживаемый файл и `source_env .envrc.local`.
- Статус: `direnv status`; перезагрузить: `direnv reload`; снять: `direnv deny`.

---

## terraform и terragrunt (через tfenv/tgenv)

Плейбук **не ставит** terraform и terragrunt: он ставит только менеджеры версий
`tfenv` и `tgenv`. Версию выбираете сами:

```bash
tfenv install 1.11.4 && tfenv use 1.11.4       # глобальная версия terraform
tgenv install 0.93.0 && tgenv use 0.93.0       # глобальная версия terragrunt
```

`~/.tfenv/bin` и `~/.tgenv/bin` уже добавлены в `PATH` через `devops-shell.sh`,
там же лежат шимы `terraform` и `terragrunt`.

Основные команды:

```bash
tfenv list / tfenv list-remote      # установленные / доступные версии
tgenv list / tgenv list-remote
```

Версия **по проекту** задаётся файлами в корне репозитория:

```bash
echo 1.11.4 > .terraform-version     # tfenv переключит автоматически
echo 0.93.0 > .terragrunt-version    # tgenv переключит автоматически
```

---

## Shell-конфигурация

Плейбук создаёт `~/.config/devops-shell.sh` и добавляет в `~/.bashrc` один блок:

```bash
# BEGIN DEVOPS PLAYBOOK (ansible role: shell)
[ -f "$HOME/.config/devops-shell.sh" ] && . "$HOME/.config/devops-shell.sh"
# END DEVOPS PLAYBOOK (ansible role: shell)
```

Что внутри `devops-shell.sh`:

- `PATH`: `~/.local/bin`, `~/.tfenv/bin`, `~/.tgenv/bin`;
- `fzf --bash` (keybindings + completion);
- `direnv hook bash`, `zoxide init bash`, `starship init bash`;
- алиасы `ls`/`ll`/`la`/`lt` на `eza`;
- алиас `catbat` и тема для `bat`;
- алиас `fd` → `fdfind` (в Ubuntu бинарь `fd-find` называется `fdfind`);
- `RIPGREP_CONFIG_PATH` → `~/.config/ripgrep/config` (глобальные исключения
  для `rg`);
- completion для `kubectl`, `helm`, `kubectx`, алиас `k = kubectl`;
- `carapace _carapace bash` для спек сотен команд; из сниппета вырезается
  `CARAPACE_SHELL_FUNCTIONS`, иначе список функций `yc`-completion (~195 КБ)
  превышает лимит одной env-строки (128 КБ) и автодополнение ломается целиком;
- `PIPX_HOME` / `PIPX_BIN_DIR`;
- `mcfly init bash` (умная история по Ctrl-R, см. раздел «mcfly — история команд»).

Файл пишется из шаблона `roles/shell/templates/devops-shell.sh.j2` — правки
в самом файле перезапишутся при следующем запуске. Чтобы убрать окружение:
удалите файл и блок между маркерами в `~/.bashrc`.

### Конфиг starship

Тема prompt кладётся из `roles/shell/files/starship.toml` в `~/.config/starship.toml`
(starship читает этот путь по умолчанию). Файл копируется как есть — правки
в `~/.config/starship.toml` перезапишутся при следующем запуске. Меняйте
`roles/shell/files/starship.toml` в репозитории; путь назначения задаётся
переменной `starship_config_file` в `group_vars/all.yml`.

### Конфиг ripgrep

`roles/shell/files/ripgrep-config` копируется в `~/.config/ripgrep/config`, а
`devops-shell.sh` выставляет `RIPGREP_CONFIG_PATH` на этот файл. Внутри —
глобальные `--glob=!...` исключения, рассчитанные на привычный поиск с `-uu`:
этот флаг отключает и `.gitignore`, и пропуск скрытых каталогов, поэтому
`.terragrunt-cache`, `.terraform`, `.git`, `.venv`, `venv`, `__pycache__`,
`.tox`, `node_modules` и кэши инструментов исключаются явно.

`vendor/`, `build/`, `dist/`, `target/`, `coverage/` намеренно не исключены:
в них бывает настоящий исходный код (Go-модули в `vendor`, сгенерированный
код в `build`). Для отдельного дерева их можно отсечь в самой команде:
`rg -g '!vendor' ...`.

Обойти конфиг для одного запуска (например, чтобы найти что-то внутри
скрытого каталога): `rg --no-config -uu ...`. Путь назначения задаётся
переменной `ripgrep_config_file` в `group_vars/all.yml`.

### mcfly — история команд

**mcfly** (роль `shell`, бинарник в `/usr/local/bin`) — умная история команд:
перехватывает Ctrl-R и приоритизирует результаты по контексту (текущий каталог,
недавние команды, частота, код выхода), хранит историю в SQLite
(`~/.local/share/mcfly/history.db`). Хук подключается строкой
`eval "$(mcfly init bash)"` в `~/.config/devops-shell.sh`.

Проверка: `mcfly --version`; история — нажать Ctrl-R после нескольких
выполненных команд (или `mcfly search`).

### Nerd Font (иконки в prompt и списках файлов)

Starship рисует глифы ветки Git и Kubernetes, а `eza` умеет показывать иконки
файлов (`--icons`) — все они лежат в private use area. В обычных шрифтах таких
глифов нет, и без них в терминале видны «квадратики». Роль `shell` ставит
**полное семейство JetBrainsMono Nerd Font** (все начертания: обычный, Mono,
NL, NLPropo):

- скачивается `JetBrainsMono.tar.xz` (**~7 МБ**) из релизов
  `ryanoasis/nerd-fonts`, распаковываются все `*.ttf` (96 файлов);
- шрифты кладутся в `~/.local/share/fonts/JetBrainsMono/`, затем `fc-cache -f`;
- sudo не нужен, всё в домашнем каталоге.

Иконки уже внутри самого шрифта, поэтому после установки достаточно выбрать
**JetBrainsMono Nerd Font** в настройках терминала — отдельный fallback-шрифт
и fontconfig-конфиг не нужны.

Настройки — в `roles/shell/defaults/main.yml` (`nerd_font_*`): версия, каталог,
отключение через `nerd_font_install: false`. Идемпотентность: если файл-маркер
уже на месте, ничего не скачивается. Обновить версию — поменять
`nerd_font_version` или удалить `~/.local/share/fonts/JetBrainsMono` и запустить
плейбук снова.

> Проверить, что шрифт установился: `fc-list | grep -i "JetBrainsMono Nerd"`,
> а что иконка разрешается в него: `fc-match 'JetBrainsMono Nerd Font:charset=e0a0'`.

### M-Commander (двухпанельный файловый менеджер)

Роль `shell` ставит **M-Commander** (`blue-panels/mcommander`) — форк GNU
Midnight Commander: две панели, встроенный редактор и вьюер (со структурным
деревом для JSON/YAML/XML/HTML), встроенный терминал и подключаемые панели для
git, docker, Kubernetes, S3, FTP/SFTP, Samba, systemd и др. Главная команда —
`mcommander`, короткий алиас — `mc6`; ставится рядом с пакетом `mc` из Ubuntu,
не заменяя его.

Ставится официальными `.deb`-пакетами из GitHub-релиза (базовый пакет +
`plugins` + `lua`), сборка под Ubuntu 26.04 (`ubuntu26.04.1`). Версия не
фиксируется — тег последнего релиза берётся из редиректа `releases/latest`.
Все три пакета ставятся одной транзакцией apt (у `plugins`/`lua` зависимость
`mcommander (= версия)`), повторный запуск ничего не переустанавливает.

```bash
mcommander          # запустить файловый менеджер
mc6                 # то же самое (короткий алиас)
mcedit6 file.txt    # сразу редактор
```

Настройки — в `roles/shell/defaults/main.yml` (`mcommander_*`): репозиторий,
список `.deb`-пакетов, суффикс сборки; отключение через
`mcommander_install: false`.
