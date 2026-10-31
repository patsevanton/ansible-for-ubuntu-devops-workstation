# TODO-abandoned: заброшенные проекты — не ставить

Реестр апстримов, которые заархивированы или годами не обновляются, и
единственное место, где они описаны: что это, почему не ставим, чем роль
закрыта сейчас и при каком условии вернуться. В остальных трекерах
([`TODO.md`](TODO.md), [`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md),
[`TODO-incompatible-ubuntu-2604.md`](TODO-incompatible-ubuntu-2604.md),
[`TODO-trend-github-not-added.md`](TODO-trend-github-not-added.md),
[`TODO-habr-553000-not-added.md`](TODO-habr-553000-not-added.md),
[`TODO-binenv-not-added.md`](TODO-binenv-not-added.md),
[`not-install.md`](not-install.md)) заброшенных кандидатов нет — там только
ссылки на этот файл.

Правило действует с 2026-10-23: заброшенный проект описывается только здесь.
Описания и причины отказа перенесены сюда из перечисленных файлов без потери
деталей, чтобы не дублировать один кандидат в нескольких трекерах.

Серверные приложения и нодовые агенты
([`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md)) сюда не входят: они не
ставятся на ноутбук по другой причине, и смерть апстрима ничего не меняет.

Как читать:

- `- [ ]` — не ставим;
- «архив» — репозиторий в GitHub Archive;
- «Покрыт: …» — какие инструменты в проекте закрывают ту же роль; «частично» —
  роль закрыта не полностью;
- даты и `archived` проверены 2026-10-23 через GitHub API (`archived`,
  `pushed_at`), последний релиз — из исходного трекера;
- `pushed_at` — дата последнего пуша в репозиторий, а не дата релиза: проект
  может быть активен в коммитах и при этом годами не выпускать бинарники.

Правило возврата одно: проект оживает (архив снят, вышел релиз, появился
linux-amd64 бинарник) — тогда кандидат возвращается в свой трекер и ставится
ролью. Без этого не тратить время.

---

## 1. Репозиторий в архиве

- [ ] **Datree** — CLI против Kubernetes-мисконфигураций. —
      [datreeio/datree](https://github.com/datreeio/datree) — архив; последний
      пуш 2024-04-23. Покрыт: `kubeconform`, `kube-linter`, `polaris`,
      `kube-score`, `kubesec`, `kubescape` (роль `kubernetes`).
- [ ] **glasskube** — пакетный менеджер Kubernetes с GUI и CLI
      (dependency-aware). *(3.5k ⭐, `deb`)* —
      [glasskube/glasskube](https://github.com/glasskube/glasskube) — архив
      с 2026-06-14. Покрыт частично: `helm`, `helmfile`, `kluctl`,
      `kustomizer`, `kpt` плюс UI `headlamp`/`radar`; dependency-aware
      менеджера с GUI нет. Если архив снимут, `.deb` из релиза ставится ролью
      `kubernetes` одной строкой.
- [ ] **odo** — CLI для итеративной разработки в кластере по devfile:
      `odo dev` собирает образ, деплоит приложение и синхронизирует файлы. —
      [redhat-developer/odo](https://github.com/redhat-developer/odo) — архив;
      последний пуш 2026-03-30. Покрыт: `devspace`, `tilt`, `mirrord`,
      `telepresence` (роль `kubernetes`).
- [ ] **Octant** — web-UI/дашборд кластера. —
      [vmware-archive/octant](https://github.com/vmware-archive/octant) —
      архив (vmware-archive), последний пуш 2023-01-19. Заменён `headlamp` и
      `radar` из роли `kubernetes`. Покрыт: `headlamp`, `radar`; также
      `kubewall`, `kubeview`, `kdash`, `buoy`.
- [ ] **k8s-mcp-server** — MCP-сервер с kubectl/helm/istioctl. —
      [alexei-led/k8s-mcp-server](https://github.com/alexei-led/k8s-mcp-server)
      — архив; последний пуш 2026-02-27. Заменён `kubernetes-mcp-server`.
      Покрыт: `kubernetes-mcp-server` (роль `kubernetes`).
- [ ] **kube-scan** — оценка рисков кластера: опасные настройки подов и
      namespace со score по 12-балльной шкале. —
      [octarinesec/kube-scan](https://github.com/octarinesec/kube-scan) —
      архив; последний пуш 2023-01-06. Покрыт: `kubescape` (фреймворки и
      score), `popeye`, `kubeaudit`, `kube-score`, `trivy` (роль
      `kubernetes`).
- [ ] **rbac-police** — проверка прав кластерных идентичностей по политикам
      на Rego, с графом «кто через что доходит до секрета». —
      [PaloAltoNetworks/rbac-police](https://github.com/PaloAltoNetworks/rbac-police)
      — архив, последний пуш 2025-03-21. Покрыт: `rbac-tool`,
      `kubectl-who-can`, `kubehound` (роль `kubernetes`); `kubehound` строит
      граф путей атак, включая цепочки до секретов.

## 2. Не архив, но проект мёртв

- [ ] **dog** — DNS-клиент с человекочитаемым цветным выводом. *(`cargo`)* —
      [ogham/dog](https://github.com/ogham/dog) — последний релиз `v0.1.0`
      (2021), последний пуш 2024-05-29. Бинарник к тому же не запускается на
      Ubuntu 26.04: динамически связан с `libssl.so.1.1`, которого в
      дистрибутиве нет. Симптом подтверждён в
      [ogham/dog#109](https://github.com/ogham/dog/issues/109); смежные
      открытые issue — [#98](https://github.com/ogham/dog/issues/98) и
      [#122](https://github.com/ogham/dog/issues/122). Покрыт: `q` и `doggo`
      (роль `network`). Пересмотреть, если выйдет релиз со статической
      сборкой.
- [ ] **Chartsec** — сканер безопасности Helm-чартов. —
      [banzaicloud/chartsec](https://github.com/banzaicloud/chartsec) —
      заброшен с 2019, последний пуш 2019-08-30, релизов нет. Покрыт
      частично: `kubesec`, `trivy` (роль `secrets`), `kubeaudit` — статический
      скан манифестов, чарт целиком не рендерится.
- [ ] **kubectl-snapshot** — снимки состояния кластера. —
      [fbrubbo/kubectl-snapshot](https://github.com/fbrubbo/kubectl-snapshot) —
      заброшен с 2020, последний пуш 2020-03-24, ассетов в релизе нет.
      Покрыт частично: `kbom` (инвентарь состояния в JSON) и `kubectl-slice`;
      снимка с восстановлением нет.
- [ ] **kube-shell** — интерактивный shell для kubectl. —
      [cloudnativelabs/kube-shell](https://github.com/cloudnativelabs/kube-shell)
      — последний релиз `0.0.23` (2017), последний пуш 2022-11-02; современные
      API не покрывает. Заменён `kube-prompt`. Покрыт: `kube-prompt` и
      `kubeprompt` (роль `kubernetes`), также `k9s`.
- [ ] **klum** — управление пользователями и доступом к кластеру. —
      [ibuildthecloud/klum](https://github.com/ibuildthecloud/klum) — не
      обновлялся с 2023, последний пуш 2023-09-21; только `go build`, релизов
      нет. Покрыт частично: `kubecm` (kubeconfig), `rbac-tool`, `rbac-lookup`,
      `kubectl-who-can`, `audit2rbac`; создания пользователей нет.
- [ ] **KuberEz** — графическое моделирование манифестов. —
      [uengine-oss/kubeez](https://github.com/uengine-oss/kubeez) — переименован
      из `kuber-ez`, заброшен с 2023, последний пуш 2023-11-13; в релизе
      `1.0alpha` нет ассетов. Покрыт: `monokle`, `rubick`, `klustr`, `sextant`
      (роль `kubernetes`).
- [ ] **kopylot** — AI-аудит, диагностика и чат по ресурсам кластера. —
      [avsthiago/kopylot](https://github.com/avsthiago/kopylot) — не
      обновлялся с 2024, последний пуш 2024-01-24; дублирует `kopilot` и
      требует OpenAI-токен. Покрыт: `kopilot`, `k8sgpt`, `kubectl-ai`,
      `kubernetes-mcp-server` (роль `kubernetes`).
- [ ] **kubectl-mtail** — tail логов подов по label selector. —
      проект живёт на GitLab, ссылки в трекере нет; последний релиз 2020 года,
      ассетов в нём нет. Покрыт: `stern`, `kail`, `kubetail`, `kftui`, `kl`
      (роль `kubernetes`).
- [ ] **kubestriker** — быстрый security-аудит кластера: неаутентифицированный
      API, kubelet, dashboard, мисконфиги. —
      [vchinnipilli/kubestriker](https://github.com/vchinnipilli/kubestriker) —
      последний релиз `v1.2.0` (2021-05-06), последний пуш 2024-04-06; пины
      `figlet==0.0.1`, `PyYAML==5.3.1`, `prompt-toolkit==1.0.15` не дают
      поставить пакет даже на Python 3.14. Покрыт: `kube-hunter`
      (неаутентифицированный скан), `kubescape`, `trivy`, `kube-bench`,
      `kubeaudit`, `popeye`, `kube-score`, `marvin` (роль `kubernetes`);
      RBAC — `rbac-tool`, `kubectl-who-can`, `kubehound`.
- [ ] **PowerfulSeal** — chaos-тестирование Kubernetes: сценарии в YAML,
      убийство подов, остановка/запуск нод, SSH-команды, HTTP-пробы после
      отказа. —
      [powerfulseal/powerfulseal](https://github.com/powerfulseal/powerfulseal) —
      последний релиз `3.3.0` (2021-09-17), последний пуш 2023-11-10; требует
      `PyYAML<6`, который не собирается на Python 3.14. Ничем не покрыт:
      chaos-инструменты в плейбук не берутся (решение 2026-10-25), включая
      `pumba`, который убран из роли `kubernetes`. Кандидаты — в
      [`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md).

## 3. Формально живы, но два года без активности

Кандидаты без релизного бинарника: последний пуш старше двух лет, но архива
нет и явного «заброшен» в трекере не написано. Пересматривать только вместе
с релизом — сами по себе они не вернутся.

- [ ] **xlskubectl** — управление кластером из «электронной таблицы». —
      [learnk8s/xlskubectl](https://github.com/learnk8s/xlskubectl) — последний
      пуш 2022-09-23; на PyPI не публиковался, релизов нет.
- [ ] **kuttle** — sshuttle-доступ к подам без SSH. —
      [kayrus/kuttle](https://github.com/kayrus/kuttle) — последний пуш
      2023-01-29; релизов нет, имя на PyPI занято другим проектом. Покрыт
      частично: `telepresence`, `kubevpn`, `ktunnel`, `kubectl-relay`,
      `kubefwd`, `gefyra`, `mirrord`; sshuttle-модели нет.
- [ ] **mico** — AI-помощник kubectl. —
      [tahtaciburak/mico](https://github.com/tahtaciburak/mico) — последний
      пуш 2023-03-25; только `go build`, релизов нет. Покрыт: `kubectl-ai` и
      `k8sgpt` (роль `kubernetes`).
- [ ] **KindScaler** — управление нодами KinD-кластера. —
      [lobuhi/kindscaler](https://github.com/lobuhi/kindscaler) — последний
      пуш 2024-06-15; только `go build`, релизов нет.

## 4. Из статьи Habr «Полезные консольные Linux утилиты»

Сверка со статьёй
[habr.com/ru/articles/553000](https://habr.com/ru/articles/553000/) (2021):
живые кандидаты оттуда — в
[`TODO-habr-553000-not-added.md`](TODO-habr-553000-not-added.md), здесь только
те, чей апстрим в архиве, годами не выпускает релизов или последний пуш был
в 2023 году и раньше. Даты `pushed_at` и `archived` проверены через GitHub
API 2026-10-24, HTTP Prompt — 2026-10-25.

### 4.1. Репозиторий в архиве

- [ ] **dnsmeter** — генератор DNS-запросов для нагрузочного теста сервера
      имён и инфраструктуры вокруг него. *(только исходники)* —
      [DNS-OARC/dnsmeter](https://github.com/DNS-OARC/dnsmeter) — архив;
      последний пуш 2026-02-04; linux-ассетов в релизах нет. Роль не закрыта:
      `dnsperf`/`dnsx` в плейбуке нет.
- [ ] **ssh-tools** — набор скриптов для проверки удалённых хостов (версия
      SSH, доступность портов, баннеры). *(`make install`)* —
      [vaporup/ssh-tools](https://github.com/vaporup/ssh-tools) — архив;
      последний пуш 2023-08-29. Покрыт частично: `assh` и `ssh`-утилиты роли
      `network`; набора проверок хоста нет.
- [ ] **Nginx-builder** — сборка nginx с нужными модулями из YAML, на выходе
      rpm/deb. — [TinkoffCreditSystems/Nginx-builder](https://github.com/TinkoffCreditSystems/Nginx-builder)
      — архив; последний пуш 2023-05-22. Роль не закрыта: nginx в плейбуке не
      собирается.
- [ ] **GeoLogonalyzer** — поиск аномалий в логах по ASN, гео и подсетям
      (например, вход с неожиданного IP). *(Python)* —
      [fireeye/GeoLogonalyzer](https://github.com/fireeye/GeoLogonalyzer) —
      архив; последний пуш 2024-08-12. Покрыт частично: `goaccess` и `lnav`
      (кандидаты) разбирают логи, гео-аномалий не ищут.
- [ ] **container-diff** — сравнение образов контейнеров: история, файловая
      система, пакеты apt/pip/npm. *(`linux-amd64` в старых релизах)* —
      [GoogleContainerTools/container-diff](https://github.com/GoogleContainerTools/container-diff)
      — архив; последний пуш 2024-03-27. Покрыт частично: `dive` (слои и
      размер образа); сравнения пакетов нет.
- [ ] **asciicast2gif** — конвертация asciicast в GIF. *(Docker-образ)* —
      [asciinema/asciicast2gif](https://github.com/asciinema/asciicast2gif) —
      архив; последний пуш 2022-08-14. Не нужен: `asciinema` стоит в роли
      `shell`, а GIF при необходимости соберёт `agg`.
- [ ] **skx/sysadmin-util** — набор shell-скриптов для админа, ставится
      копированием в `$PATH`. —
      [skx/sysadmin-util](https://github.com/skx/sysadmin-util) — архив;
      последний пуш 2020-03-30. Скрипты из статьи:
        - [ ] **ago** — сколько времени прошло с изменения файла. Покрыт: `stat` и
              `find -mtime` из коробки.
        - [ ] **cronic** — тихий запуск команды в cron до первой ошибки. Покрыт:
              `chronic` из `moreutils` (пакет Ubuntu) либо `systemd` timers; в Ubuntu
              есть и отдельный пакет `cronic`.
        - [ ] **cidr2ip** — разворачивает CIDR в список IP. Покрыт частично:
              `iprange` (кандидат в
              [`TODO-habr-553000-not-added.md`](TODO-habr-553000-not-added.md)); в
              системе такого инструмента нет.
        - [ ] **collapse** — убирает пустые строки и строки из пробелов. Покрыт:
              `grep -v '^[[:space:]]*$'` и `sed`.
        - [ ] **dupes** — дубликаты файлов по SHA1. Покрыт частично: `fdupes` и
              `rmlint` в плейбуке не стоят.
        - [ ] **empty-dir** — проверяет, пуст ли каталог. Покрыт: `find -empty` и
              `ls -A`.
        - [ ] **expand-ipv6** — разворачивает сжатый IPv6 до полной формы. Покрыт
              частично: `python3 -c 'import ipaddress; …'`; `sipcalc` не стоит.
        - [ ] **multi-ping** — ping без выбора между IPv4 и IPv6. Покрыт: `ping`
              умеет оба протокола.
        - [ ] **pyhttpd** — одноразовый HTTP-сервер на Python. Покрыт:
              `python3 -m http.server`.
        - [ ] **randpass** — генератор паролей. Покрыт: `openssl rand -base64`.
        - [ ] **since** — новый контент файла с прошлого чтения. Покрыт частично:
              `tail -f`, `less +F`, `journalctl -f`; запоминания позиции нет.
        - [ ] **ssl-expiry-date** — дата истечения сертификата домена. Покрыт:
              `openssl s_client`; удобнее — `ssl-cert-check` (кандидат).
        - [ ] **until-error / until-success** — повторять команду до ошибки или
              успеха. Покрыт: `until`/`while` в shell.
        - [ ] **when-down / when-up** — ждать падения или подъёма хоста. Покрыт
              частично: цикл `until ping`/`until ! ping`.
        - [ ] **mysql-slave-check** — является ли текущий хост MySQL-репликой.
              Покрыт: `SHOW REPLICA STATUS` в `mysql`.
        - [ ] **which-shell** — определяет текущую оболочку. Покрыт: `$SHELL` и
              `ps -p $$`.

### 4.2. Не архив, но проект мёртв

- [ ] **runnel** — автоподъём SSH-туннелей с переподключением. *(Ruby)* —
      [mdp/runnel](https://github.com/mdp/runnel) — последний пуш 2017-09-04,
      gem не публиковался. Покрыт частично: `mosh` и `assh`; автоподъёма
      туннелей нет.
- [ ] **ssh-config** — CLI для правки `~/.ssh/config`. *(Go, только
      `go build`)* — [dbrady/ssh-config](https://github.com/dbrady/ssh-config)
      — последний пуш 2020-12-29, релиз без ассетов. Покрыт: `assh` (роль
      `network`) генерирует `~/.ssh/config` из YAML.
- [ ] **pd.sh** — отладка пайплайнов: где именно упало. —
      [ketancmaheshwari/pd](https://github.com/ketancmaheshwari/pd) —
      последний пуш 2020-09-15, релизов нет. Покрыт частично: `set -o
      pipefail` и `bashdb` (кандидат).
- [ ] **critic.sh** — «суровое» тестирование bash-скриптов. —
      [Checksum/critic.sh](https://github.com/Checksum/critic.sh) — последний
      пуш 2020-08-11, релизов нет. Покрыт частично: `shellcheck` (роль
      `shell`).
- [ ] **SSH-Attack-Stats** — статистика неудачных SSH-входов в MOTD.
      *(Python)* —
      [Sodium-Hydrogen/SSH-Attack-Stats](https://github.com/Sodium-Hydrogen/SSH-Attack-Stats)
      — последний пуш 2021-05-06, релизов нет. Покрыт частично: `lastb` и
      `journalctl -u ssh`; готового MOTD-скрипта нет.
- [ ] **tunnelto** — публичный URL на локальный веб-сервер. *(`linux.tar.gz`
      в релизе)* — [agrinman/tunnelto](https://github.com/agrinman/tunnelto) —
      последний пуш 2022-09-24. Роль не закрыта: `frp` и `https-portal` —
      кандидаты, `cloudflared` в плейбуке нет.
- [ ] **tfquery** — SQL-запросы к состоянию Terraform. *(PyPI)* —
      [mazen160/tfquery](https://github.com/mazen160/tfquery) — последний пуш
      2022-10-27. Покрыт частично: `terraform show -json` + `jq`.
- [ ] **kubesql** — SQL-запросы к ресурсам Kubernetes. *(только
      `go build`)* — [xuxinkun/kubesql](https://github.com/xuxinkun/kubesql) —
      последний пуш 2022-11-16. Покрыт частично: `kubectl -o json` + `jq`.
- [ ] **localtls** — DNS-сервер, выдающий TLS-имена локальным адресам.
      *(только `go build`, linux-ассетов нет)* —
      [Corollarium/localtls](https://github.com/Corollarium/localtls) —
      последний пуш 2023-06-18. Покрыт частично: `mkcert` (локальный CA);
      DNS-части нет.
- [ ] **logtop** — realtime-top по IP/строкам из логов веб-сервера. —
      [JulienPalard/logtop](https://github.com/JulienPalard/logtop) — последний
      пуш 2023-06-29; в Ubuntu пакет `logtop` 0.7 ещё есть. Роль не закрыта:
      `goaccess` и `lnav` — кандидаты, в плейбуке их нет.
- [ ] **frontail** — отдаёт лог в браузер с live-обновлением. *(npm,
      `frontail-linux`)* — [mthenw/frontail](https://github.com/mthenw/frontail)
      — последний пуш 2023-11-12. Роль не закрыта.
- [ ] **HTTP Prompt** — интерактивный HTTPie с автодополнением и импортом
      OpenAPI. *(PyPI)* —
      [httpie/http-prompt](https://github.com/httpie/http-prompt) — последний
      релиз `v2.1.0` вышел в 2021, последний пуш 2024-05-21; пять лет без
      релизов. Покрыт: `httpie`/`xh` для запросов и `posting` (роль `network`)
      для коллекций, окружений и истории; интерактивного автодополнения
      OpenAPI нет.
- [ ] **linux-exploit-suggester-2** — подбор эксплойтов под локальное ядро,
      второе поколение. *(Perl-скрипт)* —
      [jondonas/linux-exploit-suggester-2](https://github.com/jondonas/linux-exploit-suggester-2)
      — последний пуш 2023-01-28. Покрыт частично:
      `linux-exploit-suggester` (кандидат, тоже скрипт).

---

## 5. Из списка binenv

Сверка с [DISTRIBUTIONS.md](https://github.com/devops-works/binenv/blob/develop/DISTRIBUTIONS.md)
(снято 2026-10-24): записи, чей апстрим в архиве или не обновлялся два года.
`archived` и `pushed_at` проверены 2026-10-24 через GitHub API, GitLab-проекты —
через GitLab API. Роль-заменитель подбиралась только там, где она очевидна;
если проект оживёт, кандидат переезжает в
[`TODO-binenv-not-added.md`](TODO-binenv-not-added.md).

- [ ] **asciinema-edit** — постобработка записей asciinema: обрезка и ускорение каста.
      — [cirocosta/asciinema-edit](https://github.com/cirocosta/asciinema-edit/) — последний пуш 2023-06-28.
- [ ] **awless** — CLI для AWS с шаблонами и генерацией команд.
      — [wallix/awless](https://github.com/wallix/awless/) — последний пуш 2022-08-02.
- [ ] **batect** — окружения сборки и тестов как код.
      — [batect/batect](https://github.com/batect/batect) — архив; последний пуш 2023-10-22.
- [ ] **bomberman** — нагрузочный тест SMTP-сервера.
      — [c1982/bomberman](https://github.com/c1982/bomberman/) — последний пуш 2020-04-28.
- [ ] **bud** — full-stack фреймворк для Go: роутинг, рендеринг, сборка.
      — [livebud/bud](https://github.com/livebud/bud/) — последний пуш 2023-11-24.
- [ ] **check-tls-cert** — проверка TLS-сертификата и цепочки.
      — [heartbeatsjp/check-tls-cert](https://github.com/heartbeatsjp/check-tls-cert/) — последний пуш 2022-05-04.
- [ ] **clog-cli** — changelog из истории коммитов.
      — [clog-tool/clog-cli](https://github.com/clog-tool/clog-cli) — последний пуш 2024-08-15.
- [ ] **cloudman** — TUI для управления EC2-инстансами.
      — [dutchcoders/cloudman](https://github.com/dutchcoders/cloudman) — последний пуш 2021-04-10.
- [ ] **config-registry** — переключение между kubeconfig-ами (защита от прода).
      — [mumoshu/config-registry](https://github.com/mumoshu/config-registry/) — последний пуш 2022-01-09.
- [ ] **confused** — поиск dependency confusion в пакетных менеджерах.
      — [visma-prodsec/confused](https://github.com/visma-prodsec/confused) — последний пуш 2024-08-19.
- [ ] **derefexo** — менеджер процессов и просмотр логов для разработки (exo).
      — [deref/exo](https://github.com/deref/exo/) — последний пуш 2022-08-17.
- [ ] **devdash** — настраиваемый терминальный дашборд для разработчика.
      — [Phantas0s/devdash](https://github.com/Phantas0s/devdash/) — архив; последний пуш 2023-07-19.
- [ ] **driftwood** — проверка использования приватных ключей.
      — [trufflesecurity/driftwood](https://github.com/trufflesecurity/driftwood) — архив; последний пуш 2025-04-04.
- [ ] **dw-query-digest** — анализ slow-логов MySQL, альтернатива pt-query-digest.
      — [devops-works/dw-query-digest](https://github.com/devops-works/dw-query-digest) — последний пуш 2023-02-25.
- [ ] **exa** — предшественник `eza` (`ls` с иконками и git-статусом).
      — [ogham/exa](https://github.com/ogham/exa/) — последний пуш 2024-09-24. Заменён `eza`, который уже стоит в роли `shell`.
- [ ] **gbt** — конструктор prompt для bash/zsh/powershell.
      — [jtyr/gbt](https://github.com/jtyr/gbt/) — последний пуш 2024-02-22.
- [ ] **github-release-notes** — release notes из истории pull request-ов GitHub.
      — [buchanae/github-release-notes](https://github.com/buchanae/github-release-notes/) — последний пуш 2019-02-06.
- [ ] **go-mod-outdated** — устаревшие зависимости Go-проекта таблицей.
      — [psampaz/go-mod-outdated](https://github.com/psampaz/go-mod-outdated) — последний пуш 2023-02-19.
- [ ] **gokart** — статический анализ безопасности Go-кода.
      — [praetorian-inc/gokart](https://github.com/praetorian-inc/gokart/) — архив; последний пуш 2024-01-23.
- [ ] **grafana_cli** — CLI для дашбордов, папок и аннотаций Grafana.
      — [kckecheng/grafana_cli](https://github.com/kckecheng/grafana_cli/) — последний пуш 2021-01-04.
- [ ] **grizzly** — Grafana как код: Jsonnet-дашборды через API.
      — [grafana/grizzly](https://github.com/grafana/grizzly/) — архив; последний пуш 2026-06-05.
- [ ] **gws** — хелпер для работы с git worktree.
      — [StreakyCobra/gws](https://github.com/StreakyCobra/gws/) — последний пуш 2020-02-28.
- [ ] **kcli** — TUI-браузер Kafka только для чтения.
      — [cswank/kcli](https://github.com/cswank/kcli/) — последний пуш 2020-01-04. Kafka на ноутбуке не используется; `kaf`/`kafkactl` — кандидаты.
- [ ] **ketall** — `kubectl get all`, но по всем типам ресурсов.
      — [corneliusweig/ketall](https://github.com/corneliusweig/ketall/) — последний пуш 2023-12-06. Частично покрыт `kubectl get` по типам ресурсов.
- [ ] **kuberlogic** — PaaS на Kubernetes: разворачивание софта как managed-сервиса.
      — [kuberlogic/kuberlogic](https://github.com/kuberlogic/kuberlogic/) — архив; последний пуш 2022-10-26.
- [ ] **kubesurvival** — подбор самых дешёвых машин под нагрузку.
      — [aporia-ai/kubesurvival](https://github.com/aporia-ai/kubesurvival) — последний пуш 2021-11-03.
- [ ] **local-php-security-checker** — проверка PHP-зависимостей на известные CVE.
      — [fabpot/local-php-security-checker](https://github.com/fabpot/local-php-security-checker/) — архив; последний пуш 2024-08-02.
- [ ] **mygopherhose** — ускоренный импорт mysqldump.
      — [devops-works/mygopherhose](https://github.com/devops-works/mygopherhose/) — последний пуш 2021-10-23.
- [ ] **mysql_random_data_load** — генератор случайных данных для MySQL.
      — [Percona-Lab/mysql_random_data_load](https://github.com/Percona-Lab/mysql_random_data_load/) — последний пуш 2022-12-24.
- [ ] **noti** — уведомление по завершении длинной команды.
      — [variadico/noti](https://github.com/variadico/noti) — архив; последний пуш 2026-05-01.
- [ ] **oto** — кодогенерация RPC для Go.
      — [pacedotdev/oto](https://github.com/pacedotdev/oto/) — последний пуш 2024-08-16.
- [ ] **pass-checker** — энтропия пароля и проверка SHA1 в HaveIBeenPwned.
      — [devops-works/pass-checker](https://github.com/devops-works/pass-checker/) — последний пуш 2021-05-11.
- [ ] **phpsecscan** — сканер уязвимостей PHP (standalone или веб-сервис).
      — [devops-works/phpsecscan](https://github.com/devops-works/phpsecscan) — последний пуш 2023-02-18.
- [ ] **ruflood** — DDoS-флуд российских государственных сайтов.
      — [zegkljan/ruflood](https://github.com/zegkljan/ruflood/) — последний пуш 2022-02-26. Помимо заброшенности не берём по назначению: DDoS-инструмент.
- [ ] **shaloc** — передача файлов в локальной сети по AES-256.
      — [eze-kiel/shaloc](https://github.com/eze-kiel/shaloc/) — последний пуш 2020-11-26.
- [ ] **slowql-digest** — дайджест slow-логов SQL (MySQL, MariaDB, Percona).
      — [devops-works/slowql](https://github.com/devops-works/slowql/) — последний пуш 2024-02-15.
- [ ] **slowql-replayer** — воспроизведение slow-логов SQL.
      — [devops-works/slowql](https://github.com/devops-works/slowql/) — последний пуш 2024-02-15.
- [ ] **snowcat** — аудит Istio service mesh.
      — [praetorian-inc/snowcat](https://github.com/praetorian-inc/snowcat) — последний пуш 2021-10-22.
- [ ] **spt** — клиент Spotify для терминала.
      — [Rigellute/spotify-tui](https://github.com/Rigellute/spotify-tui/) — последний пуш 2024-04-04.
- [ ] **ssllabs-scan** — клиент API SSL Labs для массовой проверки TLS.
      — [ssllabs/ssllabs-scan](https://github.com/ssllabs/ssllabs-scan/) — последний пуш 2024-08-05.
- [ ] **stoppropaganda** — DDoS-флуд прокремлёвских сайтов.
      — [erkexzcx/stoppropaganda](https://github.com/erkexzcx/stoppropaganda/) — архив; последний пуш 2022-05-24. Помимо заброшенности не берём по назначению: DDoS-инструмент.
- [ ] **sysz** — TUI для systemctl на базе fzf.
      — [joehillen/sysz](https://github.com/joehillen/sysz/) — последний пуш 2024-04-22.
- [ ] **telegraf-tailcount** — счётчик новых строк файла в метриках InfluxDB.
      — [devops-works/telegraf-tailcount](https://github.com/devops-works/telegraf-tailcount/) — последний пуш 2022-10-23.
- [ ] **teler** — HTTP IDS в реальном времени.
      — [kitabisa/teler](https://github.com/kitabisa/teler/) — архив; последний пуш 2024-02-13.
- [ ] **tf2pulumi** — конвертер Terraform-проектов в Pulumi.
      — [pulumi/tf2pulumi](https://github.com/pulumi/tf2pulumi/) — репозиторий
      удалён (GitHub API отдаёт 404). Pulumi в проекте не используется.
- [ ] **tlder** — проверка занятости домена по всем TLD.
      — [dwisiswant0/tlder](https://github.com/dwisiswant0/tlder/) — последний пуш 2024-10-20.
- [ ] **underpass** — self-hosted альтернатива ngrok.
      — [cjdenio/underpass](https://github.com/cjdenio/underpass/) — последний пуш 2022-05-03.
- [ ] **yh** — подсветка YAML в выводе kubectl.
      — [andreazorzetto/yh](https://github.com/andreazorzetto/yh/) — последний пуш 2020-12-14.

---

## Что сюда не попало

- **Закрытое ПО** (`Lens IDE`, `K8Studio`, `Kubexer`) — это не заброшенные, а
  платные или закрытые продукты; они остаются в [`not-install.md`](not-install.md).
- **Активные проекты с устаревшими зависимостями** (`HolmesGPT`,
  `KubeDiagrams`, `IceKube`, `vulncov`, `teller`) — апстрим жив, ломается
  совместимость с Ubuntu 26.04 / Python 3.14, поэтому они в
  [`TODO-incompatible-ubuntu-2604.md`](TODO-incompatible-ubuntu-2604.md).
  `Netchecks` из этого списка выбыл: проверен на Python 3.14 и разблокирован,
  см. [`TODO.md`](TODO.md).
- **`devbox` и `flox`** — живые, но удалены из-за отказа от Nix:
  [`TODO-trend-github-not-added.md`](TODO-trend-github-not-added.md).
- **Кандидаты без релизного бинарника, но с живым апстримом** — остаются в
  [`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md): там ждут релиз,
  а не возрождения проекта.
