# TODO: сводка по кандидатам — что уже есть и что ставить не нужно

Кандидаты из трендов GitHub, которые осознанно не попали в плейбук, — в
[`TODO-trend-github-not-added.md`](TODO-trend-github-not-added.md),
новая партия утилит для ноутбука из трендов за последние 3 года (срезка
2026-10-24) — в
[`TODO-trend-github-last-3-years.md`](TODO-trend-github-last-3-years.md),
вторая половина пятилетнего окна (2021-10-26 — 2023-10-24), не покрытая
трёхлетним обзором, — в
[`TODO-trend-github-last-5-years.md`](TODO-trend-github-last-5-years.md),
opencode 2 (один агент
раздаёт задачи другим, включая pitwall и herdr) — в
[`TODO-opencode-orchestration.md`](TODO-opencode-orchestration.md), утилиты,
сознательно не ставимые плейбуком (с причинами и issue — atuin и др.) —
в [`not-install.md`](not-install.md), кандидаты без готового бинарника на
GitHub — в [`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md),
кандидаты, чей бинарник не запускается на Ubuntu 26.04, —
в [`TODO-incompatible-ubuntu-2604.md`](TODO-incompatible-ubuntu-2604.md),
серверные приложения, утилиты, Helm-чарты и агенты на нодах Kubernetes
(DaemonSet/static Pod, не на ноутбук) — в
[`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md), всё из Ansible Galaxy (роли,
коллекции, готовые playbook'и), которое плейбук не ставит, — в
[`TODO-ansible-galaxy-not-install.md`](TODO-ansible-galaxy-not-install.md),
кандидаты из списка binenv (готовые релизные бинарники), которых в плейбуке
пока нет, — в [`TODO-binenv-not-added.md`](TODO-binenv-not-added.md),
заброшенные проекты (архив GitHub или годы без обновлений) — в
[`TODO-abandoned.md`](TODO-abandoned.md), живые кандидаты из статьи Habr
«Полезные консольные Linux утилиты» (habr.com/ru/articles/553000) — в
[`TODO-habr-553000-not-added.md`](TODO-habr-553000-not-added.md); остальные
утилиты оттуда разложены по своим трекерам — `TODO-abandoned.md`,
`TODO-no-prebuilt-binary.md` и `not-install.md`; серверные приложения — в
[отдельном репозитории](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server).
Сырая партия кандидатов из Telegram-канала GitHubRadar (срезка 2026-10-31,
1747 утилит и приложений, по которым ещё нет решения) — в
[`TODO-githubradar-not-added.md`](TODO-githubradar-not-added.md).
Не кандидат, а план работ — генератор архитектурных схем из
Terraform/Terragrunt: [`TODO-diagrams.md`](TODO-diagrams.md).

Текущие задачи (окружение для Rust, подбор security-утилит, редакторы
ArtCraft) — в разделе [«Задачи»](#задачи) в конце файла.

Источник подборки: все репозитории со ⭐ аккаунта (2057 шт.), из них отобраны
~570 похожих на локально устанавливаемые утилиты и вручную вычищены до списков
в файлах выше. Полные данные обхода (все 2057 звёзд + 571 кандидат + ссылки на
релизы): `/home/magnit/Public/starred-tools/data/` (`install_hints.tsv`,
`install_report.md`).

Дедупликация 2026-10-18: каждый кандидат описан ровно в одном файле-трекере.
Общий список кандидатов разобран полностью: всё, что ставится, уже в ролях и
`README.md`, отказы с причинами — в [`not-install.md`](not-install.md) и
отдельных трекерах, поэтому сам файл со списком удалён. Здесь остались
справочные списки: что уже ставит плейбук, что не ставится на ноутбук и что
является просто подборками.

Дедупликация 2026-10-22: серверные приложения, сервисы и Helm-чарты собраны в
[`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md) (из этого файла и из
`TODO-no-prebuilt-binary.md`); тогда же нодовые агенты Kubernetes
(DaemonSet/static Pod) вынесены из `TODO-no-prebuilt-binary.md` в отдельный
`TODO-node-tools.md`, чтобы не смешивать их с кластерными сервисами уровня
Deployment и с кандидатами, у которых просто нет бинарника.

Дедупликация 2026-10-23: `TODO-node-tools.md` влит в
[`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md) — причина отказа у нодовых агентов
та же, что у остальных кластерных компонентов (не ноутбук), а признак
«DaemonSet на нодах» сохранён пометкой в описании кандидата, а не отдельным
файлом.

Реестр 2026-10-23: заброшенные проекты (архив GitHub, годы без обновлений)
описаны только в [`TODO-abandoned.md`](TODO-abandoned.md). Из остальных
трекеров такие кандидаты убраны, там остались только ссылки на этот файл:
один заброшенный проект не должен быть описан в нескольких местах.

Разбор 2026-10-23: из [`not-install.md`](not-install.md) убраны кандидаты, у
которых причина отказа техническая, а не «не нужен». HolmesGPT (Python 3.14)
ушёл в [`TODO-incompatible-ubuntu-2604.md`](TODO-incompatible-ubuntu-2604.md);
kcmsu, Kubefirst, Radius, Jenkins X, k8s-tun и Scaphandre (агент на хосте) — в
[`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md). Krane и Kubes (только gem),
kubectl-kubesec (krew) сначала ушли в
[`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md), но в тот же день
вернулись в `not-install.md`: у всех трёх есть аналоги среди уже
поставленного. werf и kubedog не рассматриваются, odo перенесён в
[`TODO-abandoned.md`](TODO-abandoned.md) (репозиторий в архиве).
В `not-install.md` остались платные продукты, дубли уже установленного,
bash-скрипты без релизов и отказы из-за багов апстрима.

---

Добавлены 2026-10-22 из трендов GitHub (топ-15
приложений по звёздам среди оставшихся кандидатов; `dev-sec` — коллекция
Ansible Galaxy, а не приложение, поэтому вместо неё в набор вошёл следующий по
звёздам `terrascan`): `gitui`, `vhs`, `dagger`, `limactl`/`lima`,
`pgcli`, `harlequin`, `terraformer`, `terrascan`, `steampipe`, `kubectl-ai`,
`k3d`, `telepresence`, `tilt`, `mirrord`.

Добавлены 2026-10-22 из тех же трендов следующим по звёздам (снова без
`dev-sec`): `devspace`, `rustnet`, `lazysql`, `kubent`. `devbox` и `flox`
удалены: Nix не используется.

Добавлены 2026-10-23 из тех же трендов — следующие 15 по звёздам среди
оставшихся кандидатов (без заброшенных — см.
[`TODO-abandoned.md`](TODO-abandoned.md), мета-пакета `ansible-dev-tools`,
который дублирует уже поставленные части, и коллекции Ansible Galaxy
`dev-sec`): `polaris`, `kube-score`, `kubectl-neat`, `kubectl-validate`,
`nova`, `helm-secrets`, `ansible-navigator`, `ansible-builder`,
`ansible-creator`, `ansible-doctor`, `ara`, `tenv`, `atmos`, `tfupdate`,
`tfsort`. `inframap` уже стоял в плейбуке до этого разбора (роль `iac`, тег
v0.8.0).

Добавлены 2026-10-23 из тех же трендов — последние кандидаты с готовым пакетом
Ubuntu: `btop` (1.4.6) и `ncdu` (1.22), оба ролью `shell` через apt. Трекер
трендов после этого разобран полностью и удалён; кандидаты, которые осознанно
не добавлены (`ansible-dev-tools` — мета-пакет, `dev-sec` — коллекция Galaxy),
описаны с причинами в [`not-install.md`](not-install.md) и
[`TODO-ansible-galaxy-not-install.md`](TODO-ansible-galaxy-not-install.md).
Заброшенные из этой волны — в [`TODO-abandoned.md`](TODO-abandoned.md).

Добавлены 2026-10-24 из трендов GitHub за последние 3 года: `toolong`,
`ptcpdump`, `superfile` (бинарник `spf`), `rainfrog`, `posting`, `lfk`,
`zizmor`, `landrun`, `lazyssh`. `bluetui` не ставится — причина в
[`not-install.md`](not-install.md).

Добавлены 2026-10-24 по запросу: `dbx` (роль `postgres`), `omnyssh` — TUI
`omny` и GUI `OmnySSH` (роль `network`), `RackPeek` — команда `rpk` (роль
`iac`), `kula` (роль `monitoring`), `tirith` и `dcg` (роль `guardrails`,
dcg дополнительно подключён к OpenCode плагином). `tirith` убран 2026-10-26 —
см. задачу 7 в разделе [«Задачи»](#задачи).

Добавлены 2026-10-24 из трендов GitHub за последние 3 года по запросу:
`serpl` (роль `shell`), `whosthere` (роль `network`), `khi` (роль
`kubernetes`), `sonar` (роль `shell`). Все — одиночные бинарники из
GitHub-релизов, без root и setcap. `sonar` частично дублирует уже
поставленный `witr` (тот же вопрос «кто держит порт»), но добавлен
сознательно: `witr` даёт разовый ответ в CLI/JSON, `sonar` — живой
TUI-дашборд портов с kill и перезапуском, плюс MCP-сервер для
AI-агентов.

Добавлены 2026-10-24 по запросу из классических apt-пакетов (не из трендов
GitHub): `rsync` (роль `base`), `bpftrace` (роль `ebpf`), `socat` и `iperf3`
(роль `network`), `shfmt` (роль `shell`). Эти пробелы не были в трекерах,
потому что `TODO-trend-*` собираются по звёздам GitHub и не учитывают
обычные пакеты Ubuntu.

Добавлены 2026-10-24 по запросу, вторая партия: `lsof` (роль `base`),
`sysstat` (роль `shell`), `ethtool` (роль `network`), `skopeo` (роль
`docker`), `yc` (роль `iac`). `yc` ставится отдельной задачей
`roles/iac/tasks/yc.yml`: апстрим публикует бинарники на своём storage, а не
в GitHub-релизах, поэтому роль `binaries` не подходит. `skopeo`, как и
`rsync` из первой партии, уже упоминался в README как существующий, хотя
ничего его не ставило.

Добавлены 2026-10-24 по запросу, третья партия — пробелы в диагностике и
переносе данных: `strace` и `etckeeper` (роль `base`), `pv` (роль `shell`),
`sshfs` и `rclone` (роль `network`). `strace` дополняет `fatrace` (тот видит
только доступ к файлам и только от root) и eBPF-утилиты (в основном сеть).
`etckeeper` держит `/etc` в локальном git: apt-хук коммитит до и после
операций с пакетами, systemd-таймер добавляет ручные правки; удалённого
репозитория нет, потому что в `/etc` попадаются секреты. `rclone` дополняет
`s5cmd`: тот быстрее на S3, rclone работает с WebDAV/SFTP/Drive/OneDrive.

`smartmontools`, `nvme-cli` и `lm-sensors` из этой же партии уже добавлены
ранее в роль `hardware`.

Добавлены 2026-10-26 из пятилетнего обзора трендов GitHub (вторая половина
окна, 2021-10-26 — 2023-10-24, см.
[`TODO-trend-github-last-5-years.md`](TODO-trend-github-last-5-years.md)):
`ruff` (роль `base`, pipx), `d2` и `tfautomv` (роль `iac`), `pinact` (роль
`git`), `inshellisense` (роль `shell`, npm), `cdebug` и `kubectl-explore`
(роль `kubernetes`). `binsider`, `distrobox` и `LocalSend` отклонены по
запросу.

`pueue` (очередь долгих задач) и `clipse` (история буфера обмена) в этот
набор не вошли: в репозитории Ubuntu 26.04 их нет, а с GitHub пришлось бы
брать два бинарника плюс systemd-юнит (`pueue`/`pueued`) или проверять
Wayland-интеграцию. Пакеты apt дают ту же пользу без этой цены.

Добавлены 2026-10-24 по запросу, четвёртая партия — данные, API и
репозитории с большими файлами: `redis-tools` и `kcat` (роль `shell`),
`grpcurl` и `buf` (роль `network`), `inxi` (роль `hardware`), `git-lfs`
(роль `base`). `redis-cli` и `kcat` — единственные клиенты Redis и Kafka в
плейбуке: `dbx` даёт GUI, но в скриптах и на серверах нужны именно CLI.
`grpcurl` — первый gRPC-клиент (до этого gRPC был только как приёмник OTLP
у `otel-tui`); `buf` идёт в паре с ним для работы с `.proto`. `inxi`
дополняет `smartctl`/`sensors` общей картиной железа. `git-lfs` нужен,
чтобы `git clone` репозиториев с ассетами не оставлял pointer-заглушки.

NetBird (`netbird` + `netbird-ui`) добавлен 2026-10-24 в роль `network` из
официального apt-репозитория `pkgs.netbird.io` (PPA у проекта нет). Остальные
VPN-клиенты (`wireguard-tools`, `openvpn`, плагины NetworkManager,
`sshuttle`) в плейбук пока не добавлены — решение отложено.

Добавлены 2026-10-24 по запросу, четвёртая партия: `postgresql-client` (роль
`postgres`, даёт `psql`/`pg_dump`/`pg_restore`), `docker-buildx-plugin` (роль
`docker`), `pciutils`, `usbutils` и `dmidecode` (роль `hardware`), `perf`
через `linux-tools-generic` (роль `shell`). `postgresql-client`, как `rsync`
и `skopeo` раньше, уже подразумевался в README («pgcli дополняет psql»), но
ничего его не ставило; `docker-buildx-plugin` не входил в `docker-ce-cli`,
поэтому `docker buildx` на чистой машине не работал.

Добавлены 2026-10-24 по разбору трекеров, где кандидаты были перечислены, но
решение по ним не принято ([`TODO-habr-553000-not-added.md`](TODO-habr-553000-not-added.md),
[`TODO-binenv-not-added.md`](TODO-binenv-not-added.md)): `mtr` (роль
`network`) и `sos` (роль `base`) — пакеты apt; `kubestr`, `imgpkg` и `cmctl`
(роль `kubernetes`), `pgmetrics` (роль `postgres`) — бинарники из
GitHub-релизов. `mtr` — единственный инструмент с текстовым отчётом по всем
хопам (у `trippy` и `gping` только TUI/график); `sos` собирает диагностику
одним архивом для тикета; `kubestr` проверяет хранилище кластера (StorageClass,
CSI, реальные IOPS), чего не делает ни одна из утилит роли; `imgpkg`
завершает набор Carvel рядом с `ytt` и `kbld`; `cmctl` заменяет
`kubectl`-простыни по объектам cert-manager; `pgmetrics` снимает состояние
PostgreSQL в текст/JSON, тогда как `pgcenter` — интерактивный монитор.

Добавлены 2026-10-24 по запросу, пятая партия — сеть и реестры:
`wireguard-tools` (роль `network`, apt), `httpstat` (роль `network`, pipx),
`dnspeep` и `regctl` (бинарники из GitHub-релизов, роли `network` и `docker`).
`wireguard-tools` закрывает единственный отсутствующий VPN-примитив: NetBird
работает поверх WireGuard, но своего просмотра пиров и хендшейков не даёт.
`httpstat` дополняет `httptap`: тот вскрывает запросы произвольного процесса,
`httpstat` меряет заданный URL и отдаёт JSON с порогами SLO. С версии 1.3
апстрим `reorx/httpstat` — Python-файл без зависимостей, поэтому ставится
pipx, а не `go install`, и кандидат ушёл из
[`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md). `dnspeep`
отвечает на вопрос «какой процесс ходит в DNS»: `gai`, `dnsglobe` и `doggo`
показывают резолв, но не источник запросов. `regctl` доводит до правды запись
в [`not-install.md`](not-install.md) про замену `registry-cli` и добавляет к
`skopeo` работу с тегами, манифестами и referrers.

Добавлены 2026-10-25 по разбору трекеров: `pigz` (роль `base`), `miller` и
`nerdlog` (роль `shell`), `whois` (роль `network`) — пакеты apt; `subfinder`
(роль `secrets`) и `sonobuoy` (роль `kubernetes`) — бинарники из
GitHub-релизов. `pigz` заменяет однопоточный `gzip` на больших архивах;
`miller` закрывает CSV/TSV/JSONL там, где `jq` и SQL-движки неудобны;
`nerdlog` показывает логи нескольких хостов на одной шкале времени (на
удалённых хостах нужен `gawk`); `whois` дополняет `dig`: показывает
регистратора и срок домена; `subfinder` собирает поддомены пассивно, до
`nmap` и `nuclei`; `sonobuoy` запускает conformance/e2e-тесты Kubernetes
(нужен cluster-admin, плейбук ставит только CLI).

Добавлены 2026-10-25 из [`TODO-binenv-not-added.md`](TODO-binenv-not-added.md)
по разбору трекеров: `kafkactl` (роль `shell`), `checkip` (роль `network`) и
`terraform-inventory` (роль `iac`, версия зафиксирована на v0.10) — бинарники
из GitHub-релизов. `kafkactl` дополняет `kcat`: тот умеет только
produce/consume, а kafkactl показывает топики, партиции, ACL и лаг consumer
groups. `checkip` собирает по IP гео, ASN, DNS-имя, репутацию и TLS — для
разбора адресов из логов и алертов. `terraform-inventory` отдаёт inventory для
Ansible из `terraform.tfstate` и закрывает разрыв между Terraform- и
Ansible-инструментами ролей.

Добавлены 2026-10-25 по разбору трекеров и запросу: `fselect` (роль `shell`),
`prek` (роль `git`), `dockle` (роль `docker`), `httping` (роль `network`,
пакет apt). `fselect` фильтрует и сортирует файлы по любым атрибутам (`size`,
`mtime`, `mode`, владелец), чего не умеют `fd` (шаблон имени) и `du`/`dust`
(размер); его релиз — одиночный gzip-файл, поэтому в роли `binaries` появился
тип `archive: gz` (раньше `cheat` из-за этого ставился отдельной задачей).
`prek` стоит рядом с `pre-commit`, а не вместо него: тот же
`.pre-commit-config.yaml`, но хуки идут параллельно и без Python-окружения на
каждый прогон. `dockle` дополняет `trivy`/`grype` (CVE в пакетах) и `dive`
(слои): проверяет уже собранный образ по CIS Docker Benchmark. `httping`
меряет HTTP-код и время запросов циклом с min/avg/max там, где `tcping` видит
только TCP-порт, а `httpstat` — один запрос.

`anydoc`, `doxx` и `OfficeCLI` не добавлены: конвертация офисных документов в
Markdown отложена — вариантов несколько, нужен выбор; `OfficeCLI` не заменяет
WordCraft (тот GUI для человека, а не CLI-правка `.docx` для агентов). Чтение
офисных файлов при этом закрыто: `catdoc` для legacy `.doc`/`.xls`/`.ppt` и
`wordcraft-cli` для `.docx`/`.doc` (добавлены 2026-11-12), поэтому отдельные
конвертеры в Markdown пока не нужны. `ffsend` перенесён в
[`not-install.md`](not-install.md): сервис Firefox Send закрыт, клиенту некуда
отправлять файлы.

`lego` из того же списка перенесён в
[`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md): сертификаты и приватные ключи
должны жить там, где работает сервис, а на ноутбуке их роль закрывают `mkcert`
(локальный CA) и `showcert`/`testssl.sh` (проверка). `osv-scanner` из списка
убран: он добавлен 2026-10-25 раньше (роль `secrets`).

Добавлены 2026-10-25 по запросу: `gron` и `sig` (роль `shell`), `jjui` (роль
`git`), `mcpc` (роль `ai_tools`). `gron` — единственный способ превратить
JSON в построчно-греппабельный текст (`json[3].spec.replicas = 3;`), `jq` и
`dasel` работают с JSON как с данными, а не как с текстом; обратная сборка —
`gron -u`. `sig` — интерактивный grep по живому потоку
(`kubectl logs -f … |& sig`), аналога в наборе нет: `hl` разбирает готовый
JSON, `toolong`/`lnav` читают файлы, а не пайп. `jjui` — TUI к уже стоящему
`jj`, как `lazygit` и `gitui` к git. `mcpc` — клиент MCP для проверки
серверов (`radar`, `kubernetes-mcp-server`, `stealth-browser-mcp`) без
агента; ставится npm-пакетом `@apify/mcpc`, как `tldr` и `opencode`.
Кандидаты убраны из [`TODO-binenv-not-added.md`](TODO-binenv-not-added.md)
(`gron`) и
[`TODO-trend-github-last-3-years.md`](TODO-trend-github-last-3-years.md)
(`sig`, `jjui`); `mcpc` — из
[`TODO-trend-github-not-added.md`](TODO-trend-github-not-added.md).

Добавлены 2026-10-25 по запросу, второй эшелон — оставшийся набор после
отказа от `watchman` и `pnpm` (оба закрывали сценарий «чужой JS-проект на
время»: триггеры на файлы и второй пакетный менеджер): `dotenvx` и `gosec`
(роль `secrets`), `openapi-tui` (роль `dast`) — бинарники из GitHub-релизов.
`gosec` — SAST именно для Go: `govulncheck` видит только зависимости, а
`opengrep` не знает stdlib и идиом языка. `dotenvx` дополняет `sops` там, где
секреты уже лежат в обычном `.env`, а заводить `.sops.yaml` с ключом никто не
хочет. `openapi-tui` закрывает шаг «посмотреть спецификацию и дёрнуть ручку
руками» до `schemathesis` и EvoMaster, чтобы отличить ошибку приложения от
находки фаззера. Кандидаты убраны из
[`TODO-trend-github-last-3-years.md`](TODO-trend-github-last-3-years.md)
(`dotenvx`, `openapi-tui`) и
[`TODO-binenv-not-added.md`](TODO-binenv-not-added.md) (`gosec`).

Добавлены 2026-10-25 по разбору
[`TODO-binenv-not-added.md`](TODO-binenv-not-added.md): `hetty` (роль `dast`),
`mint` — бывший `docker-slim` (роль `docker`) и `onefetch` (роль `git`) —
бинарники из GitHub-релизов. `hetty` — MITM-прокси с веб-интерфейсом: правка
запроса и ответа вручную — то, чего не умеют ни сканеры роли `dast`,
ни наблюдатели трафика вроде `httptap`/`ptcpdump`. `mint` уменьшает **уже
собранный** образ по профилю реально используемых файлов, тогда как `dive`
только показывает слои. `onefetch` даёт сводку по репозиторию (языки, строки
кода, лицензия, авторы), чего не делает `fastfetch`. Апстрим `mint` переехал:
старый `slimtoolkit/slim` остался на 1.40.11 (2024), актуальный репозиторий —
`mintoolkit/mint` (1.41.8+), бинарник `mint`, команда `mint slim`.

Добавлены 2026-10-25 по разбору трекеров: `yor` (роль `iac`) и `tuicr` (роль
`git`) — бинарники из GitHub-релизов. `yor` проставляет IaC-ресурсам теги с
git-метаданными (репозиторий, коммит, автор) и закрывает обратную ссылку
«облачный ресурс → код»: `terrascan`/`checkov` только проверяют код, а
`terraformer` генерирует его из облака. `tuicr` проводит ревью MR/PR из
терминала — построчные комментарии и отправка в GitHub/GitLab/Bitbucket/Azure
DevOps/Gerrit, понимает git, jj и hg; `gh`/`glab` создают и смотрят PR/MR, но
ревью в них идёт через веб. Кандидаты убраны из
[`TODO-binenv-not-added.md`](TODO-binenv-not-added.md) (`yor`) и
[`TODO-trend-github-not-added.md`](TODO-trend-github-not-added.md) (`tuicr`).

Добавлены 2026-10-25 по запросу: `sql-tap` (роль `postgres`) и `godap`
(роль `network`) — бинарники из GitHub-релизов. `sql-tap` перехватывает
SQL-трафик между приложением и PostgreSQL, MySQL или TiDB: прокси `sql-tapd`
и TUI `sql-tap` показывают запросы, транзакции и EXPLAIN без правки кода
приложения — этого не дают ни `pgcenter`, ни `pgcli`. `godap` закрывает
отсутствовавший LDAP-клиент: дерево каталога, поиск и правка атрибутов для
AD/OpenLDAP без Apache Directory Studio. Кандидаты убраны из
[`TODO-trend-github-not-added.md`](TODO-trend-github-not-added.md) (`sql-tap`)
и [`TODO-trend-github-last-3-years.md`](TODO-trend-github-last-3-years.md)
(`godap`).

Добавлены 2026-10-25 по запросу: `task` и `gocloc` (роль `shell`), `revdiff`
(роль `git`) и `abtop` (роль `ai_tools`) — бинарники из GitHub-релизов.
`task` читает `Taskfile.yml` из чужих репозиториев, который `just` не
понимает. `gocloc` — первый счётчик строк кода в наборе: разбивка по языкам
и каталогам, тогда как `onefetch` даёт только сводку по репозиторию целиком.
`revdiff` закрывает ревью диффа после агента: построчные аннотации и вывод
разметки в stdout, чего не делают ни `lumen`, ни `difftastic`. `abtop`
показывает несколько одновременных агентских сессий, расход токенов и
лимиты — `rtk` считает только экономию на сжатии вывода. Кандидаты убраны из
[`TODO-binenv-not-added.md`](TODO-binenv-not-added.md) (`task`, `gocloc`) и
[`TODO-trend-github-not-added.md`](TODO-trend-github-not-added.md) (`revdiff`,
`abtop`).

Добавлены 2026-10-25 по запросу: `betterleaks` (роль `secrets`), `sofka`
(роль `kubernetes`), `quien` (роль `network`), `hunk` (роль `git`) и `moli`
(роль `ai_tools`) — бинарники из GitHub-релизов. `betterleaks` — сканер
секретов от авторов `gitleaks`: ранжирует находки по уверенности и severity,
проверяет ключи и определяет права учётной записи, чего не делают ни
`gitleaks` (шаблоны), ни `trufflehog` (только live-проверка). `sofka` —
второй Kubernetes TUI рядом с `k9s`: понимает Flux CD и Argo CD без отдельных
CLI и показывает причины сбоя ресурса. `quien` собирает WHOIS/RDAP, DNS,
почту, TLS и SEO по домену в один экран — вместо цепочки `whois`, `doggo`,
`showcert` и `gossl`. `hunk` — интерактивное ревью большого агентского диффа
с inline-аннотациями; `revdiff` отдаёт разметку в stdout, `delta` только
подсвечивает. `moli` — headless-браузер для агентов, который не требует
отдельного Chromium, в отличие от `stealth-browser-mcp`. Кандидаты убраны из
[`TODO-trend-github-not-added.md`](TODO-trend-github-not-added.md).

Добавлены 2026-10-25 по запросу: `ttl` (роль `network`) и `droast`
(роль `docker`) — бинарники из GitHub-релизов. `ttl` — не второй traceroute,
а диагностика поверх него: MTU/PMTUD, ECMP по потокам, NAT/CGNAT, flap
маршрутов и MPLS с ASN/geo по хопам; `trippy` рисует TUI по потерям и
задержкам, `mtr` даёт текстовый отчёт. Для raw-сокета плейбук навешивает
`CAP_NET_RAW` через setcap. `droast` дополняет `hadolint`: span-aware парсер
разбирает heredoc, BuildKit `--mount` и PowerShell, правила DF* ловят
структурные проблемы, есть автофиксы и SARIF. Кандидаты убраны из
[`TODO-trend-github-not-added.md`](TODO-trend-github-not-added.md).

Добавлены 2026-11-10 по запросу: `jira-cli` и `jiratui` (роль `atlassian`) —
бинарник из GitHub-релиза и pipx-пакет. Оба закрывают работу с Jira без
браузера: `jira-cli` — команды и машиночитаемый вывод (`--plain`, `--raw`,
`--csv`), произвольный JQL и скрипты; `jiratui` — постоянный экран с задачами
проекта, фильтрами и карточкой тикета. Поддерживаются и Jira Cloud
(API-токен), и on-prem Server/DC (PAT), поэтому набор годится для
корпоративного Jira, где браузер не всегда под рукой. Конфиг с URL и токеном
плейбук не создаёт: `jira init` и `jiratui configure create` запускаются
вручную, чтобы секрет не попал в репозиторий. Кандидаты убраны из
[`TODO-binenv-not-added.md`](TODO-binenv-not-added.md) (`jira-cli`) и
[`TODO-trend-github-last-3-years.md`](TODO-trend-github-last-3-years.md)
(`jiratui`).

Добавлены 2026-11-12 по запросу: `catdoc` (роль `shell`, пакет apt) и
`wordcraft-cli` (роль `craft`, идёт в .deb WordCraft). `catdoc` даёт
`catdoc`/`xls2csv`/`catppt` и закрывает legacy-файлы Office 97-2003
(`.doc`/`.xls`/`.ppt`): `rga` их не читает, а его адаптер `.docx` держится на
`pandoc`, которого плейбук не ставит. `wordcraft-cli` — headless-конвертер
(`text`, `convert`, `inspect`) для `.docx` и `.doc`, им агент читает
документы. Отдельного артефакта с одним CLI upstream не выпускает: в
`packaging/linux/package.sh` в пакет кладутся оба бинарника, `/usr/bin/wordcraft`
и `/usr/bin/wordcraft-cli`. Поэтому `wordcraft_install` теперь по умолчанию
`true` (GUI приезжает вместе с CLI, выключается `-e wordcraft_install=false`),
а GridCraft и DeckCraft остаются за своими флагами. Выбран `.deb`, а не
`tar.gz`: тарболл меньше всего на ~1.7 МБ (112.8 против 114.5 МБ), зато apt
подтягивает зависимости и регистрирует `.desktop`/MIME.

Обновление 2026-11-12 по запросу: GridCraft и DeckCraft тоже ставятся по
умолчанию (`gridcraft_install` и `deckcraft_install` — `true`), выключаются
флагами. В их `.deb` так же лежат `<name>-cli`, поэтому роль теперь сверяет
оба бинарника у каждого приложения и переустанавливает пакет, если GUI
остался, а CLI пропал. Размеры x86_64-пакетов: WordCraft 114.5 МБ, GridCraft
51.2 МБ, DeckCraft 101.2 МБ — полный прогон тянет ~267 МБ `.deb`; если
редакторы не нужны, они отключаются тремя флагами.

Обновление 2026-10-25 по запросу: `vhs` удалён из роли `shell`, вместо него
добавлен `asciinema` (пакет apt): нужна запись живой терминальной сессии для
багрепортов и runbook, а не сценарные GIF-демо. `ttyd` удалён вместе с `vhs`
(он был нужен только для его записи), `ffmpeg` оставлен — им `rga` извлекает
текст из видео. `OpenTofu` (`tofu`) перенесён в
[`not-install.md`](not-install.md): IaC-стек на Terraform. Причины обоих
отказов — там же.

`kingfisher` не добавлен: он дублирует уже стоящий `trufflehog` (та же
live-проверка ключей), а его отличия — отзыв ключа и карта blast radius — пока
не нужны. История буфера обмена через GPaste удалена 2026-10-26: пакеты
`gpaste-2` и `gnome-shell-extension-gpaste` убраны из роли `shell`. Расширение
GNOME Shell работает только после перелогина и только в GNOME, выделение в
терминале уходит в PRIMARY (GPaste его не пишет), а предложенный способ
копирования `Ctrl+Shift+C` терминал отдаёт приложению как `Ctrl+C` — opencode
на нём закрывается.

`geesefs` из той же партии перенесён в
[`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md): FUSE-моунт Object Storage нужен на
сервере или ВМ, а на ноутбуке эту роль закрывает `rclone mount`.

`HolmesGPT` не ставится: последний релиз требует Python `<3.14`, а в Ubuntu
26.04 системный Python 3.14 — см.
[`TODO-incompatible-ubuntu-2604.md`](TODO-incompatible-ubuntu-2604.md) и
[issue #2649](https://github.com/HolmesGPT/holmesgpt/issues/2649).

`argocd`, `pulumi` и `kubebuilder` не ставятся: Argo CD не используется, IaC —
на Terraform, Kubernetes-операторы не создаются
(см. [`not-install.md`](not-install.md)).

`ansible-core` ставится один раз вручную при bootstrap (см. `README.md`).

`pitwall` пока не ставится плейбуком, но уже не из-за бага: issue с вводом
русских букв закрыт 2026-10-19, фикс вышел в `v0.1.0-beta.12`. Решение о
добавлении ждёт разбора оркестрации в opencode 2, раздел 6:
[`TODO-opencode-orchestration.md`](TODO-opencode-orchestration.md).

`Slightly Parallel` ([`NMar33/slightly-parallel`](https://github.com/NMar33/slightly-parallel))
— **разобраться, нужен ли он в плейбуке**, решение отложено. Локальный дашборд
для работы с несколькими проектами и агентами сразу: записывает все чаты
(хуки Claude Code/Codex/Cursor, плагин opencode), держит канбан задач, собирает
стендапы и чекпоинты по команде `#scan`, данные — плоские файлы в
`~/.slightly-parallel`, сервер слушает `127.0.0.1:8123` без авторизации
(один человек, один компьютер). Пакетов нет: ни на PyPI (значит, pipx не
подходит), ни `.deb`, ни релизных бинарников — только `git clone` и
`./run.sh`, который сам создаёт `backend/.venv` (нужны Python 3.11+ и
`python3-venv`). При подключении проекта он пишет в его `AGENTS.md`/
`CLAUDE.md`, ставит хуки и запись MCP, поэтому подключение остаётся ручным
шагом в UI, а не задачей плейбука. Если добавлять — только ролью: `git clone`
в `~/opt` + systemd-юнит `--user` (`sp.sh autostart on`), с флагом
`slightly_parallel_install: false` по умолчанию.

`vibeforge` ([`mmm-byte/vibeforge`](https://github.com/mmm-byte/vibeforge))
— **в будущие установки**, решение отложено (2026-10-24). CLI-конвейер для
AI-разработки приложений: семь стадий (`clarify` → `architect` → `scaffold` →
`build` → `harden` → `document` → `ship`), между ними quality gate; семь типов
проектов (webapp, api, cli_tool, bot, extension, data_pipeline, mobile);
LLM-провайдеры — Ollama по умолчанию (офлайн), OpenAI и Anthropic. Лицензия
MIT, Python ≥ 3.9, точка входа — `vibeforge`.

Как ставить: пакет питоновский, поэтому ролью `pipx_apps` из git —
`pipx install git+https://github.com/mmm-byte/vibeforge`. `pip install
vibeforge` из README сейчас не работает: на PyPI пакета нет (404), релизов и
тегов на GitHub тоже нет, последний коммит — 2026-04-09. Отсюда и пауза:
установка из плавающего `main` не пинится и не обновляется, а сам конвейер
генерирует и запускает код в чужих проектах (сборка Docker, тесты,
self-healing), то есть это рабочий инструмент под задачу, а не утилита на
один бинарник. Пересматривать, когда появится релиз на PyPI или хотя бы тег:
тогда ставим `pipx_apps` с зафиксированной версией.

`Netchecks` ([`hardbyte/netchecks`](https://github.com/hardbyte/netchecks)) —
**добавлен в роль `kubernetes`**, проверено 2026-10-26. Раньше CLI падал на
Python 3.14 с `TypeError: Secondary flag is not valid for non-boolean flag`
из-за Typer 0.9 и Click; в `netcheck 0.10.0` это исправлено, ставится через
`kubernetes_pipx_apps` рядом с `knetvis` и `kptop`. Проверки идут с ноутбука,
без доступа к кластеру: `netcheck tcp --host api.example.com --port 6443`,
`netcheck http --url=https://example.com/healthz --validation-rule "..."`
(правило на CEL), `netcheck run -c checks.yaml` — набор проверок из файла.
Результат печатается JSON-ом со `status: pass|fail`, при провале код возврата
ненулевой. Проверки изнутри кластера — это отдельный оператор Netchecks
(Helm, пишет `PolicyReport`), он в плейбук не входит; `k8s-netchecker-server`
из [`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md) — другой проект.

`chezmoi` ([`twpayne/chezmoi`](https://github.com/twpayne/chezmoi)) —
**рассмотреть потом**, решение отложено (2026-10-25). Менеджер dotfiles:
хранит `~/.bashrc`, `~/.ssh/config`, `~/.gitconfig` и остальные файлы в git,
разворачивает их на разных машинах, умеет шаблоны под хост/ОС и diff перед
применением (`chezmoi diff`/`apply`). Секреты можно тянуть из менеджера
паролей — vaultwarden (self-hosted Bitwarden) или аналога — вместо хранения
открытого текста в репозитории. В плейбук пока не берём: он сам рендерит свои
конфиги (`devops-shell.sh`, `starship.toml`, ripgrep), а личные dotfiles —
отдельное решение. Вернуться при необходимости синхронизации dotfiles между
машинами. Кандидат остаётся в
[`TODO-binenv-not-added.md`](TODO-binenv-not-added.md).

Добавлены 2026-10-25 по запросу: `gitjacker` (роль `secrets`), `sx` и
`tlsexp` (роль `network`), `red` и `kaf` (роль `shell`) — бинарники из
GitHub-релизов и GitLab Generic Packages. `gitjacker` восстанавливает
исходники с сайтов, где оставили доступным `.git`; `sx` — быстрый сканер на
raw-сокетах (плейбук навешивает `CAP_NET_RAW`); `tlsexp` проверяет сроки
сертификатов по списку URL и отдаёт метрики в Prometheus; `red` группирует
JSON-логи из пайпа со спарклайном тренда; `kaf` — Kafka CLI с контекстами
кластеров, дополняет `kcat` и `kafkactl`. Кандидаты убраны из
[`TODO-habr-553000-not-added.md`](TODO-habr-553000-not-added.md) (`red`) и
[`TODO-binenv-not-added.md`](TODO-binenv-not-added.md) (`gitjacker`, `sx`,
`tlsexp`, `kaf`).

Chaos-инструменты (`pumba`, `chaosblade`, Chaos Toolkit, `chaosd`,
`Chaos Mesh`, `chaoskube`, `kube-monkey`) в плейбук не берём — решение
2026-10-25. Chaos-тестирование нужно на одноразовом стенде или в кластере, а
не на рабочей машине, и инструменты дублируют друг друга; `pumba` убран из
роли `kubernetes`. Версии, возможности и причины отказа — в
[`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md).

`tfsec` не добавлен: апстрим свернул проект в `trivy`, который уже стоит в
роли `secrets`, — причина в [`not-install.md`](not-install.md). `HTTP Prompt`
не добавлен: последний релиз вышел в 2021 — перенесён в
[`TODO-abandoned.md`](TODO-abandoned.md).

Кандидаты, которые дублируют этот список и потому не берутся: `ktail`
(≈ `stern`), `kube-switch` (≈ `kubectx`), `dyff` (≈ `diffyml`).

## garden — удалён из плейбука, вернуться к рассмотрению

`garden` ([`garden-io/garden`](https://github.com/garden-io/garden)) — оркестратор
разработки для Kubernetes и контейнеров (сборка, деплой, тесты, логи в одном CLI) —
удалён из роли `kubernetes` 2026-10-24. Причина: при каждом запуске он создаёт
каталог `.garden/` в текущем рабочем каталоге (`metadata.json` и журналы с меткой
времени), поэтому даже проверка `garden version` после прогона мусорила в
репозитории плейбука. Обёртка с `mktemp` в `playbook.yml` лечила симптом, а не
причину, и утилита убрана целиком.

Вернуться к вопросу, если понадобится оркестрация dev-окружений в Kubernetes.
Тогда сначала решить, куда писать состояние (каталог запуска или настройка
расположения `.garden/`), и запускать `garden` только из каталога проекта, а не
из домашнего каталога или репозитория плейбука. Пока в плейбуке остаются
`okteto`, `devspace`, `tilt`, `skaffold`, `mirrord` и `telepresence` — они
закрывают ту же задачу «разработка в Kubernetes» без побочных файлов.

## Обновление одиночных .deb — рассмотреть

Разбор 2026-10-23. Плейбук ставит .deb из GitHub-релизов, но `apt` такие
пакеты не обновляет: источник в dpkg не фиксируется, `apt-cache policy` для
них показывает единственную запись `100 /var/lib/dpkg/status`, то есть
кандидат всегда равен установленной версии. Отсюда варианты:

- **deb-get** — каталог ~460 сторонних приложений, `deb-get update` показывает
  ожидающие обновления, `deb-get upgrade` ставит новые .deb и обновляет
  сторонние apt-репозитории. Целесообразен, если появятся приложения, которые
  ставятся руками, вне плейбука: из .deb плейбука в каталоге есть только
  `sniffnet`, остальные пришлось бы описывать в `/etc/deb-get/99-local.d/`
  (bash-рецепты, второй набор определений в чужом формате плюс отдельный
  реестр `/etc/deb-get/installed`, который к тому же не видит пакеты,
  поставленные плейбуком). Проверено: 0.4.7 работает на Ubuntu 26.04
  (`resolute`), поддержка добавлена в PR wimpysworld/deb-get#1781, issue
  wimpysworld/deb-get#1860 закрыт этим релизом.
- **updatecli** — декларативный аналог renovate (`source → condition → target`,
  запуск в CI, PR с бампом версии). Имеет смысл в gitops-репозитории, где
  версии пиннятся; в этом плейбуке пинить нечего — 25 файлов задач берут
  `releases/latest` на момент запуска.
- **topgrade** — оркестратор «обновить всё»: apt, snap, flatpak, brew, pipx,
  npm, cargo плюс свои команды. Рассмотреть как интерактивную команду на
  ноутбуке; .deb с GitHub он не детектит — это уже закрывает роль
  `github_deb` (`roles/github_deb/tasks/install.yml`).

Решение на 2026-10-23: deb-get и updatecli в плейбук не добавляем, обновление
.deb делает роль `github_deb` (сравнение версии из `releases/latest` с
`dpkg-query`). Вернуться к deb-get, если доля приложений, ставящихся вне
плейбука, вырастет.

Решение по topgrade на 2026-10-25: в плейбук не добавляем. Повторный прогон
действительно не обновляет pipx-приложения и `tldr` из npm — роль `pipx_apps`
пропускает пакет, если шим уже есть, а `tldr` ставится только при отсутствии
бинарника. Но это закрывают две команды: `pipx upgrade-all` и
`sudo npm update -g` (см. README, «Обновление pipx и npm»). `opencode`
качается из npm-реестра напрямую, но обновляется тем же
`-e app_update=true`, что и бинарники из GitHub-релизов. Остальное у
topgrade — apt, snap, flatpak и mise: apt обновляется штатно, snap и flatpak
плейбук не использует, `mise upgrade` — одна команда. Отдельный updater
дублировал бы `app_update` и роль `github_deb` и ломал единый механизм
обновления.
Вернуться, если появится много приложений вне плейбука.

## Не для локальной установки (сервер/платформа) — только если понадобится

Из звёзд также попали self-hosted-платформы, серверные сервисы и Helm-чарты —
они не ставятся «на ноутбук» одной командой: нужен отдельный хост, Docker
Compose или Helm-релиз. Полный список с описаниями и ссылками — в
[`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md).

`VictoriaMetrics` сюда не относится: у него есть single-binary режим для
локального запуска, поэтому он стоит в роли `monitoring` (из VictoriaMetrics —
только `vmalert-tool`).

Нодовые агенты Kubernetes (DaemonSet/static Pod: `goldpinger`, `node-exporter`,
`kured`, eBPF-агенты и т.п.) — в том же
[`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md), с пометкой «DaemonSet на нодах».

## Списки и обучающие материалы (не утилиты)

`awesome`, `system-design-primer`, `awesome-sysadmin`, `90DaysOfDevOps`,
`DevOps-Roadmap`, `awesome-gh-extensions`, `awesome-tf` — полезны как подборки,
но устанавливать нечего.

Остальные подборки (`devops-exercises`, `DevOps-Bash-tools`, `kubetools`,
`modern-unix`, `awesome-tunneling`, `awesome-prometheus-alerts`,
`container-security-checklist`, `linux-network-performance-parameters`,
`boilerplates`, `home-ops`/`homelab-gitops-k3s`) ставить нечего — это
материалы для чтения. Подборка `kubetools` разобрана: что подошло — в
`README.md`, причины отказов — в [`not-install.md`](not-install.md) и
[`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md).

## Задачи

Записано 2026-10-24, к разбору. Это не кандидаты, а работы: сначала решение,
потом роль и проверка в `playbook.yml`.

1. **Окружение для разработки на Rust — сделано 2026-10-25.** В роль
   `runtimes` добавлены apt-пакеты `rustc`, `cargo`, `rustfmt`,
   `rust-clippy`, `rust-src` и системные зависимости сборки
   (`build-essential`, `pkg-config`, `libssl-dev`). `rust-analyzer` в apt
   отсутствует, поэтому ставится отдельной задачей из официального
   релиза. Выбран apt, а не rustup: версия 1.93.1 из Ubuntu 26.04
   достаточна, обновляется вместе с системой. Ограничение: `cargo-fuzz`
   требует nightly и отдельный toolchain; `cargo-afl` работает на
   стабильном Rust, но в плейбук не входит.

2. **Утилиты поиска уязвимостей по коду с фильтрами — сделано 2026-10-25.**
   Добавлены `osv-scanner` (SCA по lockfile, база OSV, SARIF/JSON,
   `--call-analysis=rust|go`), `govulncheck` (Go reachability) и
   `cargo-deny` (RustSec, лицензии и bans). Фильтры запускаются
   раздельно, без своей обёртки:
   - CVSS-порог: `dependency-check --failOnCVSS 8` (exit code); точный
     список — `--format JSON` и `jq` по `cvssv3.baseScore`.
   - RCE в коде: `opengrep --config p/command-injection` (CWE-78) и
     `p/owasp-top-ten` (CWE-94/95/502).
   - RCE в зависимостях: CWE есть в JSON `osv-scanner`/`dependency-check`,
     но нативного CWE-фильтра у них нет — отбор через `jq` по
     `cwe_ids`/`cwes`.
   Самописный `secscan.py` удалён: отдельные штатные команды закрывают
   задачу без своего кода. `bearer` не добавлен: Rust поддерживается
   только в платной Pro-версии, а бесплатный CLI не покрывает основной
   язык; `CodeQL` — тяжёлый CLI, требует сборки базы и бесплатен только
   для OSS; `Snyk` — платный и отправляет код в облако. `cargo-audit`
   остаётся опцией (`cargo install cargo-audit`) для CVSS в JSON, но
   `cargo-deny` уже закрывает RustSec.

   **Цель — находить реально эксплуатируемые уязвимости, а не все CVE.**
   Эвристика: CVSS >= 8 + CWE RCE + reachability/taint. Высокий CVSS и
   RCE сами по себе не гарантируют взлом: уязвимая функция может не
   вызываться, ввод может быть недоступен, нужны KEV/EPSS и проверка
   экспозиции. Что есть локально:
   - `osv-scanner --call-analysis=go|rust` — reachability для Go/Rust;
   - `govulncheck` — reachability для Go;
   - `opengrep` — taint-анализ RCE-классов (CWE-78/94/95/502 и др.);
   - `nuclei -tags rce` — проверка на запущенном приложении (роль `dast`).
   CWE в JSON `osv-scanner`/`dependency-check` есть, но нативного
   `--cwe` у бесплатных локальных SCA нет. Если единого CLI не найдём —
   пишем минимальную обёртку (jq-скрипт или Python на 30–50 строк) для
   CVSS + CWE + reachability, без повторения 378-строчного `secscan`.

3. **Утилиты для поиска RCE/DoS в запущенном приложении (DAST) — сделано
   2026-10-25.** Добавлена роль `dast`:
   - `nuclei` — шаблоны CVE/RCE, DAST-фаззинг (`-dast`), OpenAPI-вход,
     Interactsh для blind RCE/SSRF;
   - `OWASP ZAP` — Docker-образ: baseline, API scan по OpenAPI/SOAP/GraphQL,
     full scan; active scan включает command injection (90020), SQLi,
     XXE, LFI/RFI и overflow;
   - `wapiti` — второй движок без Docker: `exec`, `sql`, `xxe`, `ssrf`,
     `file`, `upload`, Log4Shell/Spring4Shell, OpenAPI через `--swagger`;
   - `sqlmap` — SQLi и доказательство RCE через `--os-shell`;
   - `schemathesis` — property-based/stateful фаззинг API, общий с п. 4.
   Нагрузка/DoS остаётся за уже стоящим `k6`: отдельного «DoS-сканера» нет.
   `nikto` не взят: в Ubuntu 26.04 только версия 2.1.5, а его база уже
   используется модулем wapiti и частично ZAP. `commix` не взят: узкий
   command injection, покрыт ZAP 90020, wapiti `exec` и `nuclei -dast`.
   `RESTler` вынесен в
   [`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md): .NET/Docker и
   stateful-фаззинг. Сканировать только свои стенды: active scan и `-dast`
   меняют данные, а full scan ZAP может идти часами.

4. **Фаззинг API/web по исходному коду и спецификации — сделано
   2026-10-25.** Цель — довести приложение до panic/crash/RCE/DoS и получить
   воспроизводимый вход. Добавлены:
   - `EvoMaster` в роль `dast` — black-box фаззинг REST по OpenAPI и
     GraphQL: эволюционный поиск, JUnit/Python/Playwright-тесты из находок;
   - роль `fuzz`: `afl++` и `clang` + `libFuzzer` (нативный код,
     ASan/UBSan), `zzuf` (быстрые мутации без пересборки), `Jazzer` (JVM);
   - документация в README: `go test -fuzz`, `Atheris` через
     `uv add --dev atheris`, in-process `schemathesis` через
     `from_asgi`/`from_wsgi`, ограничение `cargo-fuzz` (nightly).
   `schemathesis` остаётся в `dast`; `st` из pipx изолирован, поэтому для
   in-process harness проект добавляет пакет сам.

   Не поставлены:
   - `honggfuzz`, `radamsa`, `RESTler` — нет готового бинарника/пакета, см.
     [`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md);
   - `GraphQLer` — требует Python `<3.13`, см.
     [`TODO-incompatible-ubuntu-2604.md`](TODO-incompatible-ubuntu-2604.md);
   - `ClusterFuzzLite`/`OSS-Fuzz` — CI-сервис с хранилищем корпусов и
     кластером воркеров, см. [`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md).

   Осталось: `cargo-fuzz` требует nightly и отдельный toolchain; `cargo-afl`
   работает на стабильном Rust, но ставится отдельным cargo-крейтом. Для
   Rust-panic — сборка с `panic = "abort"` и санитайзерами (тоже nightly).

5. **Утилиты из https://github.com/storytold (ArtCraft).** Это организация
   ArtCraft (68 репозиториев, Apache-2.0, в основном Rust/egui): настольные
   GUI-редакторы — clean-room аналоги популярных программ, а не консольные
   утилиты.

   Сделано: роль `craft` ставит `wordcraft` (Word), `gridcraft` (Excel) и
   `deckcraft` (PowerPoint) официальными `.deb` для x86_64/aarch64. Все три
   ставятся по умолчанию: в каждом пакете лежит ещё `<name>-cli` для агента
   (`wordcraft-cli` читает `.docx`/`.doc`), выключаются флагами. Размеры
   пакетов: GridCraft ~51 МБ, DeckCraft ~101 МБ, WordCraft ~114 МБ;
   зависимости закрываются репозиторием Ubuntu (libc6, libgcc-s1,
   libxkbcommon0, libvulkan1 | libegl1).

   Осталось рассмотреть: `photocraft` (Photoshop), `lightcraft` (Lightroom),
   `vectorcraft` (Illustrator), `designcraft` (InDesign), `effectcraft`
   (After Effects), `filmcraft` (Premiere), `soundcraft` (Pro Tools),
   `pdfcraft` (Acrobat), `figcraft` (Figma), `cadcraft` (AutoCAD),
   `artcraft`/`artcraftx` (AI-генерация изображений и видео, прямого аналога
   нет). Для каждого проверить то же: Linux-сборка в релизах, размер,
   зрелость (все — alpha/early development) и нужен ли такой редактор
   инженеру на ноутбуке.

6. **HabrExporter — PR на установку без бандла (2026-10-25).** Кандидат —
   [`GVCoder09/HabrExporter`](https://github.com/GVCoder09/HabrExporter):
   PyQt6-приложение, сохраняет статьи Хабра с комментариями и картинками в
   PDF, HTML, DOCX, EPUB, FB2, Markdown и JSON; есть GUI и CLI
   (`habr-exporter`, `habr-exporter-cli`). В плейбук пока не ставим из-за
   упаковки.

   Проверено 2026-10-25:

   - на PyPI пакета нет: `https://pypi.org/pypi/habr-exporter/json` отдаёт
     404, поэтому `pipx install habr-exporter` не работает;
   - `.deb` в релизах нет; для Linux публикуется только PyInstaller-сборка
     `HabrExporter-1.0-linux-x64.tar.xz` — 116 МБ, после распаковки 406 МБ,
     внутри свой Python и Qt (`_internal/`);
   - `pipx install git+https://github.com/GVCoder09/HabrExporter.git@v1.0`
     работает, но venv занимает 577 МБ: тянет PyQt6 и PyQt6-WebEngine
     колёсами и зависит от системного Python (в Ubuntu 26.04 — 3.14).

   Цель PR — установка, которая использует системные библиотеки и не тащит
   второй Python и второй Qt:

   - добавить `.deb` (CI на тег через `nfpm`/`dpkg-deb`) с `Depends`:
     `python3-pyqt6 (>= 6.6)`, `python3-pyqt6.qtwebengine`,
     `python3-requests`, `python3-lxml`, `python3-docx`, `python3-pil`,
     `python3-pygments` — все есть в Ubuntu 26.04. Пакет кладёт
     `/usr/bin/habr-exporter`, `/usr/bin/habr-exporter-cli`,
     `.desktop` и иконку, а Python/Qt не бандлит;
   - параллельно опубликовать sdist/wheel на PyPI (Trusted Publishing),
     чтобы работал `pipx install habr-exporter`; GUI-зависимости вынести в
     extra, чтобы CLI можно было поставить без PyQt6;
   - проверить на чистой Ubuntu 26.04: `apt install ./habr-exporter_*.deb`
     запускает GUI и CLI без pip/venv, а `pipx install habr-exporter`
     ставит обе команды.

   Сначала issue с предложением упаковки, потом PR: публикация на PyPI
   требует прав мейнтейнера. Issue заведён:
   [#3](https://github.com/GVCoder09/HabrExporter/issues/3). Когда появится
   пакет — роль `reading` в плейбуке (apt или `pipx_apps`), по образцу
   `audio` и `craft`.

7. **tirith — вернуться позже (2026-10-26).** `sheeki03/tirith` убран из
   плейбука: удалены запись в `guardrails_binaries`, хук
   `eval "$(tirith init --shell bash)"` из `devops-shell.sh` и проверка
   `tirith --version`. Разобраться в будущем: жив ли проект и что именно он
   проверяет, как ведёт себя хук в интерактивном bash (PROMPT_COMMAND /
   DEBUG trap), не мешает ли он другим хукам и нужен ли рядом с `dcg`. Если
   решим вернуть — вернуть запись в `roles/guardrails/defaults/main.yml`,
   хук в `roles/shell/templates/devops-shell.sh.j2` и проверку в
   `playbook.yml`.
