# TODO-server-apps: серверные приложения, агенты на нодах и Helm-чарты — не на ноутбук

Список серверных приложений, сервисов, агентов на нодах и Helm-чартов, которые
плейбук **не устанавливает**. Плейбук настраивает рабочий ноутбук: бинарники в
`/usr/local/bin`, конфиги в `~/.config`, несколько CLI-утилит и агентов.
Всё, что ниже, живёт иначе — как долгоживущий сервис с портами, доменом,
хранилищем, базой и пользователями (Docker Compose, Helm-чарт, Deployment в
кластере или отдельная ВМ) либо как шаг CI-пайплайна на сервере/раннере
(сборка и публикация релизов, например `goreleaser`). Агенты на нодах
(DaemonSet, static Pod) устроены проще, но ставятся не на ноутбук по той же
причине: без кластера и kubelet им нечего обслуживать.

Ставить такое на ноутбук «одной командой» бессмысленно: без внешних
зависимостей (БД, S3, DNS, TLS) оно не заработает, а место и обновления
требует как сервер. Если понадобится — это отдельный хост, отдельный
`docker compose`/Helm-релиз и отдельная эксплуатация.

Отдельная группа — chaos-тестирование (раздел 6). Формально это CLI, и
`chaosblade` с Chaos Toolkit запускаются на ноутбуке, но решением 2026-10-25
они не ставятся: chaos-тестирование нужно на одноразовом стенде или в
кластере, а не на рабочей машине. `pumba` тоже убран из роли `kubernetes`.
Кандидаты остаются здесь, чтобы не заводить отдельный трекер ради отказа.

Как читать:

- `- [ ]` — не ставим и не планируем в роли плейбука;
- в скобках — чем апстрим распространяется: `helm` — Helm-чарт, `образ` —
  контейнерный образ/манифесты, `сервис` — self-hosted приложение с
  установкой по документации, `бинарник` — linux-amd64 релиз есть, но
  запускается он на ноде, в кластере или в CI-раннере, а не на ноутбуке; у
  chaos-инструментов бинарник локальный, но они не берутся по решению
  2026-10-25 (раздел 6);
- пометка «DaemonSet на нодах» — компонент ставится на каждую ноду, а не
  одним Deployment;
- ссылка ведёт на репозиторий проекта.

Смежные файлы с другими причинами отказа:

- [`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md) — у проекта нет
  linux-amd64 бинарника;
- [`TODO-incompatible-ubuntu-2604.md`](TODO-incompatible-ubuntu-2604.md) —
  бинарник не запускается на Ubuntu 26.04;
- [`not-install.md`](not-install.md) — осознанный отказ из-за бага/issue;
- [`TODO-binenv-not-added.md`](TODO-binenv-not-added.md) — активные
  CLI-кандидаты из списка binenv.

---

## 1. Наблюдаемость, метрики и SLO

- [ ] **grafana** — дашборды и визуализация метрик/логов. *(`helm`)* —
      [grafana/grafana](https://github.com/grafana/grafana)
- [ ] **prometheus** — сбор и хранение метрик. *(`helm`)* —
      [prometheus/prometheus](https://github.com/prometheus/prometheus)
- [ ] **alertmanager** — маршрутизация алертов. *(`helm`)* —
      [prometheus/alertmanager](https://github.com/prometheus/alertmanager)
- [ ] **prometheus-operator** — оператор для Prometheus/Alertmanager в
      кластере. *(`helm`)* —
      [prometheus-operator/prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)
- [ ] **node_exporter** — метрики хоста (CPU, память, диск, сеть) для
      Prometheus. *(`бинарник`)* — DaemonSet на нодах —
      [prometheus/node_exporter](https://github.com/prometheus/node_exporter)
      — есть `node_exporter-1.12.1.linux-amd64.tar.gz`, но в кластере он
      работает агентом на каждой ноде, а на ноутбуке смотреть нечего.
- [ ] **kube-state-metrics** — метрики состояния объектов кластера
      (Deployment, Pod, PVC) для Prometheus. *(`образ`)* — Deployment —
      [kubernetes/kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)
- [ ] **metrics-server** — сервер метрик для API Kubernetes (`kubectl top`,
      HPA). *(`образ`)* — Deployment —
      [kubernetes-sigs/metrics-server](https://github.com/kubernetes-sigs/metrics-server)
      — на ноутбуке его роль играет `ktop` (см. `README.md`); нужен ещё
      `kube-capacity --util`.
- [ ] **prometheus-adapter** — адаптер кастомных метрик для HPA. *(`helm`)* —
      [kubernetes-sigs/prometheus-adapter](https://github.com/kubernetes-sigs/prometheus-adapter)
- [ ] **node-problem-detector** — детекторы проблем ноды (ядро, диск, память).
      *(`бинарник`)* — DaemonSet на нодах —
      [kubernetes/node-problem-detector](https://github.com/kubernetes/node-problem-detector)
      — есть `node-problem-detector-v1.37.0-linux_amd64.tar.gz`.
- [ ] **netdata** — realtime-мониторинг хостов и приложений с веб-UI.
      *(`сервис`)* — [netdata/netdata](https://github.com/netdata/netdata)
      — на ноутбуке хватает `procs`, `fastfetch` и `jc` (уже стоят).
- [ ] **openobserve** — бэкенд для логов, метрик и трейсов. *(`сервис`)* —
      [openobserve/openobserve](https://github.com/openobserve/openobserve)
- [ ] **beszel** — лёгкий мониторинг серверов (hub + агенты). *(`сервис`)* —
      [henrygd/beszel](https://github.com/henrygd/beszel)
- [ ] **uptime-kuma** — проверки доступности и статус-страница. *(`сервис`)* —
      [louislam/uptime-kuma](https://github.com/louislam/uptime-kuma)
- [ ] **gatus** — health-dashboard и status page из YAML: проверки
      HTTP/ICMP/TCP/DNS/SSH и TLS-сертификатов, алерты, веб-UI. *(`сервис`)* —
      [TwiN/gatus](https://github.com/TwiN/gatus)
      — долгоживущий веб-сервис с портом и историей проверок; на ноутбуке
      разовые проверки закрывают `xh`/`curl`, `tcping`, `doggo` и `cloudprober`.
- [ ] **changedetection.io** — отслеживание изменений на страницах.
      *(`сервис`)* —
      [dgtlmoon/changedetection.io](https://github.com/dgtlmoon/changedetection.io)
- [ ] **cachet** — статус-страница для инцидентов. *(`сервис`)* —
      [cachethq/cachet](https://github.com/cachethq/cachet)
- [ ] **kubewatch** — события Kubernetes в уведомления (Slack и т.п.).
      *(`helm`)* — [robusta-dev/kubewatch](https://github.com/robusta-dev/kubewatch)
- [ ] **kuberhealthy** — синтетические проверки кластера. *(`helm`)* —
      [kuberhealthy/kuberhealthy](https://github.com/kuberhealthy/kuberhealthy)
- [ ] **pixie** — eBPF-наблюдаемость Kubernetes без агентов. *(`helm`)* —
      [pixie-io/pixie](https://github.com/pixie-io/pixie)
- [ ] **coroot** — observability/APM с root-cause: карта сервисов,
      инспекции, трейсы и логи. *(`сервис` / `helm`)* —
      [coroot/coroot](https://github.com/coroot/coroot)
      — одиночный бинарник `coroot` — только сервер и UI. Данные собирает
      `coroot-node-agent` (eBPF, privileged, host PID), метрики хранит
      Prometheus с remote-write receiver, логи и трейсы — ClickHouse. Без
      этого стека UI пустой, поэтому на ноутбуке держать его незачем: для
      Kubernetes — Helm-релиз в кластере и `kubectl port-forward`, для хоста —
      отдельный `docker compose`. В плейбуке не ставится.
- [ ] **odigos** — авто-инструментирование приложений для OTel.
      *(`helm`)* — [odigos-io/odigos](https://github.com/odigos-io/odigos)
- [ ] **hubble** — наблюдаемость Cilium: Hubble Relay и UI в кластере.
      *(`helm` / `образ`)* — [cilium/hubble](https://github.com/cilium/hubble)
      — CLI `hubble` только клиент к Relay; без Cilium и Hubble в кластере
      он бесполезен. Локальная наблюдаемость на ноутбуке уже есть —
      `netobserv` (eBPF, без агента).
- [ ] **Retina** — распределённая сетевая наблюдаемость для Kubernetes.
      *(`helm` / `образ`)* — DaemonSet на нодах —
      [microsoft/retina](https://github.com/microsoft/retina)
      — агент ставится чартом/оператором; в релизе есть только CLI
      `kubectl-retina-linux-amd64-v1.3.0.tar.gz`.
- [ ] **DeepFlow** — eBPF-трейсинг и профилирование для Kubernetes.
      *(`образ`)* — DaemonSet на нодах —
      [deepflowio/deepflow](https://github.com/deepflowio/deepflow)
      — релиз без ассетов.
- [ ] **Alaz** — eBPF-агент наблюдаемости сервисных взаимодействий.
      *(`образ`)* — DaemonSet на нодах —
      [getanteon/alaz](https://github.com/getanteon/alaz)
      — релиз без ассетов.
- [ ] **opencost** — стоимость ворклоадов Kubernetes и облака. *(`helm`)* —
      [opencost/opencost](https://github.com/opencost/opencost)
      — в релизах только SBOM; распространяется контейнерным образом.
      На ноутбуке уместен только CLI `kubectl-cost` к уже существующему
      серверу.
- [ ] **Kubecost** — распределение затрат по ворклоадам. *(`helm`)* —
      [kubecost/cost-model](https://github.com/kubecost/cost-model)
- [ ] **kepler** — оценка энергопотребления ворклоадов через eBPF и
      Prometheus-метрики. *(`бинарник` / `helm`)* — DaemonSet на нодах —
      [sustainable-computing-io/kepler](https://github.com/sustainable-computing-io/kepler)
      — есть `kepler-0.12.0.linux-amd64.tar.gz` и чарт.
- [ ] **Scaphandre** — агент метрик энергопотребления хоста (RAPL/powercap).
      *(`образ`)* — systemd-юнит или DaemonSet —
      [hubblo-org/scaphandre](https://github.com/hubblo-org/scaphandre)
      — в релизе `v1.0.3` ассетов нет (deb-пакеты и контейнерный образ), отдаёт
      метрики в Prometheus. На ноутбуке не нужен: хватает
      `power-profiles-daemon` и `amd-pstate`/`intel_pstate`.

- [ ] **loki** — хранилище логов (стек PLG). *(`helm`)* — сервис с
      хранилищем, ретеншеном и запросами —
      [grafana/loki](https://github.com/grafana/loki) — локальный лог-стек
      плейбук не собирает.
- [ ] **promtail** — агент сбора логов для Loki. *(`бинарник`)* — DaemonSet
      на нодах — [grafana/loki](https://github.com/grafana/loki) — без Loki и
      кластера отправлять нечего, ставится на ноды.
- [ ] **logcli** — CLI-клиент Loki. *(`бинарник`)* —
      [grafana/loki](https://github.com/grafana/loki) — без сервера Loki
      клиент бесполезен.
- [ ] **goaccess** — анализ access-логов nginx: TUI в реальном времени и
      HTML-отчёт. *(`бинарник`)* — нужен на сервере рядом с логами nginx:
      на ноутбуке разбирать нечего —
      [allinurl/goaccess](https://github.com/allinurl/goaccess)
- [ ] **parca** — continuous profiling: сервер профилей и агент. *(`helm` /
      `бинарник`)* — [parca-dev/parca](https://github.com/parca-dev/parca) —
      сервер с хранилищем профилей, агент — DaemonSet на нодах.
- [ ] **gpu-hot** — веб-дашборд реального времени по NVIDIA GPU: загрузка,
      память, температура и процессы. *(`образ`)* —
      [psalias2006/gpu-hot](https://github.com/psalias2006/gpu-hot) —
      запускается контейнером с `--gpus all` и слушает порт; на ноутбуке
      достаточно `nvidia-smi` и `btop`.

## 2. Данные, БД, хранилище и реестры артефактов

- [ ] **geesefs** — FUSE-ФС поверх S3: быстрый моунт Object Storage на
      сервере или ВМ. *(`бинарник`)* —
      [yandex-cloud/geesefs](https://github.com/yandex-cloud/geesefs) —
      linux-amd64 бинарник есть, но моунт storage нужен там, где работает
      сервис или бэкап; на ноутбуке ту же роль закрывает `rclone mount`.
- [ ] **ClickHouse** — колоночная OLAP-СУБД. *(`сервис`)* —
      [ClickHouse/ClickHouse](https://github.com/ClickHouse/ClickHouse)
- [ ] **cloudnative-pg** — оператор PostgreSQL в Kubernetes. *(`helm`)* —
      [cloudnative-pg/cloudnative-pg](https://github.com/cloudnative-pg/cloudnative-pg)
- [ ] **supabase** — self-hosted BaaS (Postgres + auth + storage + API).
      *(`сервис`)* — [supabase/supabase](https://github.com/supabase/supabase)
- [ ] **bytebase** — UI для миграций и ревью схем БД. *(`сервис`)* —
      [bytebase/bytebase](https://github.com/bytebase/bytebase)
- [ ] **ChartDB** — редактор и визуализация схем БД по SQL-дампу, веб-UI.
      *(`сервис`)* — [chartdb/chartdb](https://github.com/chartdb/chartdb) —
      self-hosted веб-приложение; локально схему смотрят через
      `pgcli`/`harlequin`, а для разовой диаграммы отдельный сервис не нужен.
- [ ] **immich** — self-hosted фото/видео с мобильными клиентами.
      *(`сервис`)* — [immich-app/immich](https://github.com/immich-app/immich)
- [ ] **sentry** — сервер сбора ошибок приложений. *(`сервис`)* —
      [getsentry/sentry](https://github.com/getsentry/sentry)
- [ ] **aptly** — репозиторий deb-пакетов. *(`сервис`)* —
      [aptly-dev/aptly](https://github.com/aptly-dev/aptly)
- [ ] **artifact-keeper** — self-hosted сервис для хранения артефактов
      сборки. *(`сервис`)* — на ноутбуке заменяется готовыми реестрами и
      `gh`/`glab`.
- [ ] **s3syncer** — S3-совместимый прокси перед несколькими хранилищами:
      запись во все бэкенды, чтение с фолбэком на бэкап, очередь ретраев,
      `resync`/`bisync`, Prometheus-метрики. *(`helm` / `образ`)* —
      [spions/s3syncer](https://github.com/spions/s3syncer)
      — бинарник в релизах есть, но это долгоживущий data-plane сервис, а не
      утилита: ему нужны реальные S3-бэкенды, TLS перед ним, конфиг с ключами
      в Secret и `mode: cluster` с общим Redis для HA. На ноутбуке нечего
      реплицировать, а `single`-режим с SQLite рядом с теми же файлами — не
      бэкап. Локально воспроизводится только `make up` с двумя MinIO, и это
      стенд для разработки самого s3syncer, а не установка.
- [ ] **TopoLVM** — CSI-плагин с учётом ёмкости локальных дисков ноды.
      *(`helm`)* — DaemonSet на нодах —
      [topolvm/topolvm](https://github.com/topolvm/topolvm)
      — в релизе только чарт `topolvm-17.3.0.tgz`; node-компонент — DaemonSet.
- [ ] **kube-fledged** — кэш контейнерных образов прямо на нодах.
      *(`образ`)* — DaemonSet + контроллер —
      [senthilrch/kube-fledged](https://github.com/senthilrch/kube-fledged)
      — релиз без ассетов.
- [ ] **Kubernetes Image Puller** — предзагрузка образов на ноды через
      DaemonSet. *(`образ`)* — DaemonSet на нодах —
      [che-incubator/kubernetes-image-puller](https://github.com/che-incubator/kubernetes-image-puller)
      — ставится манифестами/оператором в кластер.

- [ ] **athens** — прокси и хранилище Go-модулей. *(`бинарник` / `helm`)* —
      [gomods/athens](https://github.com/gomods/athens) — отдельный сервис с
      БД и S3; локально хватает кэша Go.
- [ ] **velero** — бэкап и восстановление кластера. *(`бинарник` / `helm`)* —
      [vmware-tanzu/velero](https://github.com/vmware-tanzu/velero) — CLI
      управляет сервером в кластере и объектным хранилищем; без кластера и S3
      не работает.

## 3. CI/CD, GitOps и IaC

- [ ] **Jenkins** — сервер CI. *(`сервис`)* —
      [jenkinsci/jenkins](https://github.com/jenkinsci/jenkins)
      — локально уже есть `glci`/`pre-commit`.
- [ ] **Argo CD** — GitOps-контроллер Kubernetes. *(`helm`)* —
      [argoproj/argo-cd](https://github.com/argoproj/argo-cd)
      — если понадобится работа с сервером с ноутбука, нужен только CLI
      `argocd`; в плейбуке его пока нет.
- [ ] **gitea** — self-hosted Git-сервер. *(`сервис`)* —
      [go-gitea/gitea](https://github.com/go-gitea/gitea)
- [ ] **Dokploy** — self-hosted PaaS поверх Docker. *(`сервис`)* —
      [Dokploy/dokploy](https://github.com/Dokploy/dokploy)
- [ ] **dokku** — мини-PaaS на одном сервере. *(`сервис`)* —
      [dokku/dokku](https://github.com/dokku/dokku)
- [ ] **kestra** — оркестратор пайплайнов и расписаний. *(`сервис`)* —
      [kestra-io/kestra](https://github.com/kestra-io/kestra)
- [ ] **semaphore** — веб-UI для запуска Ansible-плейбуков. *(`сервис`)* —
      [semaphoreui/semaphore](https://github.com/semaphoreui/semaphore)
- [ ] **atlantis** — PR-автоматизация Terraform. *(`сервис`)* —
      [runatlantis/atlantis](https://github.com/runatlantis/atlantis)
- [ ] **Terrakube** — self-hosted замена Terraform Enterprise. *(`helm`)* —
      [terrakube-io/terrakube](https://github.com/terrakube-io/terrakube)
- [ ] **terrapod** — ещё одна self-hosted замена Terraform Enterprise.
      *(`исходники`)* —
      [mattrobinsonsre/terrapod](https://github.com/mattrobinsonsre/terrapod)
      — в релизах только Terraform-провайдер, сервер собирается из исходников.
- [ ] **coder** — удалённые dev-окружения в кластере. *(`helm`)* —
      [coder/coder](https://github.com/coder/coder)
- [ ] **Unleash** — сервер feature-флагов. *(`сервис`)* —
      [Unleash/unleash](https://github.com/Unleash/unleash)
- [ ] **Crossplane** — control plane для управления облаками из Kubernetes.
      *(`helm`)* — [crossplane/crossplane](https://github.com/crossplane/crossplane)
- [ ] **Floci** — self-hosted сервис из подборки звёзд. *(`образ`)*
      — поднимается контейнером, а не ставится бинарником.
- [ ] **Jenkins X** — CI/CD-платформа для Kubernetes: ставится в кластер
      как платформа, а не на ноутбук. *(`образ`)* —
      [jenkins-x/jx](https://github.com/jenkins-x/jx)
- [ ] **goreleaser** — сборка и публикация релизов Go-проектов: бинарники под
      платформы, архивы, changelog, checksums, Docker-образы и пакеты.
      *(`бинарник`)* —
      [goreleaser/goreleaser](https://github.com/goreleaser/goreleaser)
      — это шаг релизного пайплайна в CI (на сервере или раннере, с тегом и
      доступом к registry), а не утилита ноутбука: локально запускать нечего,
      пока нет собственного Go-проекта и релизного пайплайна. На ноутбуке из
      этой области остаются `changie` (changelog), `act` (локальный прогон
      GitHub Actions) и `reviewdog` (замечания линтеров в PR/MR).
- [ ] **Kubefirst** — разворачивание готовой GitOps-платформы «с нуля».
      *(`сервис`)* — [konstructio/kubefirst](https://github.com/konstructio/kubefirst)
      — CLI создаёт кластер и ставит в него платформу на Argo CD; локального
      сценария нет, а Argo CD в плейбуке не применяется.
- [ ] **k3s-ansible** — готовый плейбук HA-кластера k3s (kube-vip,
      MetalLB). *(`git clone`)* —
      [timothystewart6/k3s-ansible](https://github.com/timothystewart6/k3s-ansible)
      — набор Ansible-плейбуков для серверов, релизов нет.

## 4. Сеть, VPN и API-шлюзы

- [ ] **https-portal** — автоматический HTTPS на nginx + Let's Encrypt в
      Docker. *(`образ`)* — [SteveLTN/https-portal](https://github.com/SteveLTN/https-portal)
      — распространяется контейнерным образом, работает сервисом, не на
      ноутбуке.
- [ ] **lego** — клиент ACME для Let's Encrypt и других CA: выпуск и продление
      сертификатов по HTTP-01/DNS-01, хуки на перезагрузку сервиса.
      *(`бинарник`)* — [go-acme/lego](https://github.com/go-acme/lego) —
      сертификат и приватный ключ должны жить рядом с сервисом, который их
      использует, а не на ноутбуке. Локально эту роль закрывают `mkcert`
      (свой CA для стендов) и `showcert`/`testssl.sh` (проверка), на сервере
      альтернатива — `certbot`.
- [ ] **wg-easy** — веб-UI для WireGuard. *(`сервис`)* —
      [wg-easy/wg-easy](https://github.com/wg-easy/wg-easy)
- [ ] **headscale** — self-hosted control-plane для Tailscale-клиентов.
      *(`сервис`)* — [juanfont/headscale](https://github.com/juanfont/headscale)
- [ ] **pangolin** — reverse-proxy и туннели с веб-UI. *(`сервис`)* —
      [fosrl/pangolin](https://github.com/fosrl/pangolin)
- [ ] **netmaker** — управляемая WireGuard-сеть. *(`helm`)* —
      [gravitl/netmaker](https://github.com/gravitl/netmaker)
- [ ] **APISIX** — API-шлюз. *(`helm`)* —
      [apache/apisix](https://github.com/apache/apisix)
- [ ] **Kong** — API-шлюз и service mesh. *(`helm`)* —
      [Kong/kong](https://github.com/Kong/kong)
- [ ] **cilium** — CNI и eBPF-платформа кластера. *(`helm`)* —
      [cilium/cilium](https://github.com/cilium/cilium)
- [ ] **kube-router** — CNI, service proxy вместо kube-proxy и network policy
      в одном DaemonSet. *(`бинарник`)* — DaemonSet на нодах —
      [cloudnativelabs/kube-router](https://github.com/cloudnativelabs/kube-router)
      — есть `kube-router_2.11.1_linux_amd64.tar.gz`, но бинарник запускается
      агентом на ноде, а не на ноутбуке.
- [ ] **kube-network-policies** — eBPF-реализация NetworkPolicy без CNI.
      *(`образ`)* — DaemonSet на нодах —
      [kubernetes-sigs/kube-network-policies](https://github.com/kubernetes-sigs/kube-network-policies)
      — релиз без ассетов; агент работает на каждой ноде.
- [ ] **Submariner** — связность подов и сервисов между кластерами.
      *(`образ`)* — gateway в DaemonSet —
      [submariner-io/submariner](https://github.com/submariner-io/submariner)
      — релиз без ассетов; ставится оператором/Helm.
- [ ] **goldpinger** — проверка связности между нодами кластера.
      *(`helm`)* — DaemonSet на нодах —
      [bloomberg/goldpinger](https://github.com/bloomberg/goldpinger)
      — в релизе только Helm-чарт `goldpinger-1.2.0.tgz`; распространяется
      контейнерным образом.
- [ ] **k8s-netchecker-server** — server + agent: проверка сети между нодами,
      ближайший аналог goldpinger. *(`образ`)* — DaemonSet на нодах —
      [mirantis/k8s-netchecker-server](https://github.com/mirantis/k8s-netchecker-server)
      — релиз без ассетов; server и agent ставятся манифестами в кластер.
- [ ] **k8spacket** — визуализация трафика подов на уровне ноды.
      *(`образ`)* — DaemonSet на нодах —
      [k8spacket/k8spacket](https://github.com/k8spacket/k8spacket)
      — релиз без ассетов; eBPF-агенты плюс веб-интерфейс.
- [ ] **KubeSkoop** — диагностика сети для разных CNI и облачных провайдеров.
      *(`образ`)* — DaemonSet на нодах —
      [alibaba/kubeskoop](https://github.com/alibaba/kubeskoop)
      — релиз без ассетов; `skoop-agent` работает на нодах.
- [ ] **meshery** — управление service mesh. *(`helm`)* —
      [meshery/meshery](https://github.com/meshery/meshery)
- [ ] **k8s-tun** — доступ к pod IP и service IP кластера. *(`сервис`)*
      — требует server в кластере и прав `NET_ADMIN` на клиенте; локального
      сценария нет, а доступ к pod/service IP уже даёт `k8s-insider`
- [ ] **Skupper** — мультиоблачная связность сервисов между кластерами.
      *(`сервис`)* — [skupperproject/skupper](https://github.com/skupperproject/skupper):
      CLI `skupper init` разворачивает site router в кластере, локального
      сценария без него нет

- [ ] **traefik** — обратный прокси и ingress-контроллер. *(`бинарник` /
      `helm`)* — [traefik/traefik](https://github.com/traefik/traefik) —
      сервис с портами 80/443 и TLS, на ноутбуке не нужен.
- [ ] **consul** — service discovery и KV-хранилище. *(`бинарник`)* —
      сервер/агент с кластером и портами —
      [hashicorp/consul](https://github.com/hashicorp/consul) — клиентских
      сценариев без кластера Consul у плейбука нет.
- [ ] **nomad** — оркестратор ворклоадов (альтернатива Kubernetes).
      *(`бинарник`)* — сервер/агент —
      [hashicorp/nomad](https://github.com/hashicorp/nomad) — нужны отдельные
      хосты с Nomad, которых в проекте нет.
- [ ] **pomerium** — identity-aware прокси. *(`бинарник` / `helm`)* —
      [pomerium/pomerium](https://github.com/pomerium/pomerium) — серверная
      часть; клиент — `pomerium-cli` (кандидат в
      [`TODO-binenv-not-added.md`](TODO-binenv-not-added.md)).

## 5. Безопасность

- [ ] **jumpserver** — bastion/PAM с веб-UI. *(`сервис`)* —
      [jumpserver/jumpserver](https://github.com/jumpserver/jumpserver)
- [ ] **warpgate** — bastion для SSH/MySQL/Postgres/Kubernetes. *(`сервис`)* —
      [warp-tech/warpgate](https://github.com/warp-tech/warpgate)
- [ ] **SafeLine** — WAF с веб-UI. *(`сервис`)* —
      [chaitin/SafeLine](https://github.com/chaitin/SafeLine)
- [ ] **threatmapper** — платформа поиска уязвимостей в образах и
      ворклоадах. *(`helm`)* —
      [deepfence/ThreatMapper](https://github.com/deepfence/ThreatMapper)
- [ ] **dagda** — статический анализ образов на malware и уязвимости.
      *(`сервис`)* —
      [eliasgranderubio/dagda](https://github.com/eliasgranderubio/dagda)
      — сервер (Django + MongoDB + docker-образ), а не CLI. На ноутбуке его
      функции закрывают `grype` и `copa`.
- [ ] **GSC** — «Git Security Checker»: self-learning AppSec-платформа
      (SAST/SCA/secrets/IaC, 69 детекторов), автогенерация PoC-эксплойтов и
      Proof-of-Fix. *(`образ`)* —
      [poliakarmai/gsc](https://github.com/poliakarmai/gsc)
      — движок закрытый и поставляется только Docker-образом
      `ghcr.io/poliakarmai/gsc-scanner` (BSL 1.1, в Apache 2.0 переходит
      06.08.2030); в публичном репозитории — GitHub Action, документация и
      MCP-сервер. Работает на сервере, а не на ноутбуке: это долгоживущий
      сканер с песочницей для hostile-PoC (нужны docker/podman), состоянием в
      SQLite-томе и запуском по расписанию/в CI, а не разовая утилита. Плюс
      доверия к self-reported метрикам мало: сами авторы пишут, что precision
      по CRITICAL — около 31%. Локальный аналог на ноутбуке — `opengrep`
      (SAST на правилах с taint-анализом, стоит в роли `secrets`) вместе с уже
      установленными `trivy`, `gitleaks`, `checkov` и `dependency-check`: те же
      классы находок, но без генерации PoC и проверки фиксов.
      Внимание: пакет `gsc` на PyPI — другой проект («Git for Scientists»,
      2020), ставить его «вместо GSC» нельзя.
- [ ] **scantron** — распределённый nmap/masscan с расписанием и API.
      *(`сервис`)* —
      [rackerlabs/scantron](https://github.com/rackerlabs/scantron)
      — набор Ansible-плейбуков с Django-сервером, очередью и БД. Локальный
      скан делается обычным `nmap` (уже стоит).
- [ ] **ClusterFuzzLite** — фаззинг в CI: сборка, corpus, дедупликация
      крэшей и отчёты. *(`сервис`)* —
      [google/clusterfuzzlite](https://github.com/google/clusterfuzzlite)
      — это CI-инфраструктура (GitHub Actions/GitLab CI плюс хранилище
      корпусов и крэшей), а не локальный CLI. На ноутбуке её роль закрывают
      `afl++`, libFuzzer и Jazzer из роли `fuzz`, а также встроенный
      `go test -fuzz`.
- [ ] **OSS-Fuzz** — непрерывный фаззинг open-source проектов.
      *(`сервис`)* — [google/oss-fuzz](https://github.com/google/oss-fuzz)
      — облачная платформа Google: сборочные образы, кластер воркеров,
      corpus и трекер. Локально повторяется только отдельный прогон фаззера;
      поднимать её на ноутбуке незачем.
- [ ] **Tetragon** — eBPF-наблюдаемость и runtime-enforcement.
      *(`helm`)* — DaemonSet на нодах —
      [cilium/tetragon](https://github.com/cilium/tetragon)
      — агент ставится чартом; в релизе есть только CLI
      `tetra-linux-amd64.tar.gz`.

## 6. Kubernetes-платформы и ОС

- [ ] **kubesphere** — платформа управления Kubernetes с UI. *(`helm`)* —
      [kubesphere/kubesphere](https://github.com/kubesphere/kubesphere)
- [ ] **talos** — immutable-ОС для Kubernetes-нод. *(`образ`)* —
      [siderolabs/talos](https://github.com/siderolabs/talos)
- [ ] **cozystack** — PaaS на Kubernetes. *(`helm`)* —
      [aenix-io/cozystack](https://github.com/aenix-io/cozystack)
- [ ] **kagent** — AI-агенты для операций в Kubernetes. *(`helm`)* —
      [kagent-dev/kagent](https://github.com/kagent-dev/kagent)
- [ ] **k8tz** — admission controller: таймзоны в Pods/CronJobs.
      *(`образ`)* — [k8tz/k8tz](https://github.com/k8tz/k8tz)
      — ставится в кластер; на ноутбуке CLI умеет только править YAML и
      устанавливать сам контроллер, поэтому в роль `kubernetes` не входит.
- [ ] **Radius** — cloud-native платформа приложений. *(`сервис`)* —
      [radius-project/radius](https://github.com/radius-project/radius)
      — на ноутбуке не нужна: требует развёрнутого control plane
- [ ] **kcmsu** — работа с ConfigMaps и Secrets в кластере. *(`сервис`)*
      — ставит компонент в кластер, а не локальную утилиту
- [ ] **rbac-wizard** — веб-UI для визуализации RBAC кластера: кто к чему
      имеет доступ, цепочки ServiceAccount → Role → ClusterRole. *(`helm`)* —
      [pehlicd/rbac-wizard](https://github.com/pehlicd/rbac-wizard)
      — долгоживущий веб-сервис; на ноутбуке разовый анализ закрывают
      `kubectl auth can-i --list` и `kubehound` (пути атак).
- [ ] **kured** — перезагрузка нод после обновлений ядра/ОС.
      *(`бинарник`)* — DaemonSet на нодах —
      [kubereboot/kured](https://github.com/kubereboot/kured)
      — есть `kured_1.23.0_linux_amd64`; следит за reboot-required.
- [ ] **node-feature-discovery** — разметка нод по возможностям железа
      (CPU-флаги, GPU, SR-IOV). *(`helm`)* — DaemonSet на нодах —
      [kubernetes-sigs/node-feature-discovery](https://github.com/kubernetes-sigs/node-feature-discovery)
      — в релизе только чарт `node-feature-discovery-chart-0.20.0.tgz`.
- [ ] **NVIDIA k8s-device-plugin** — доступ подов к GPU на нодах.
      *(`helm`)* — DaemonSet на нодах —
      [NVIDIA/k8s-device-plugin](https://github.com/NVIDIA/k8s-device-plugin)
      — в релизе только чарты `nvidia-device-plugin` и
      `gpu-feature-discovery`.
- [ ] **kube-fencing** — очистка ресурсов упавших нод, чтобы не блокировать
      восстановление. *(`образ`)* — DaemonSet на control-plane нодах —
      [kvaps/kube-fencing](https://github.com/kvaps/kube-fencing)
      — релиз без ассетов.
- [ ] **descheduler** — вытеснение подов с неудачно выбранных нод.
      *(`образ`)* — Job/Deployment в кластере —
      [kubernetes-sigs/descheduler](https://github.com/kubernetes-sigs/descheduler)
- [ ] **VPA (Vertical Pod Autoscaler)** — автоматическая правка
      requests/limits подов. *(`образ`)* —
      [kubernetes/autoscaler](https://github.com/kubernetes/autoscaler)
      — контроллер в кластере; локального сценария нет.
- [ ] **Goldilocks** — рекомендации requests/limits по данным VPA.
      *(`helm`)* — [FairwindsOps/goldilocks](https://github.com/FairwindsOps/goldilocks)
- [ ] **kube-green** — выключение неиспользуемых ворклоадов по расписанию.
      *(`helm`)* — [kube-green/kube-green](https://github.com/kube-green/kube-green)

Chaos-тестирование в плейбук не берём (решение 2026-10-25): для него нужен
одноразовый стенд или кластер, а инструменты дублируют друг друга. `pumba`
убран из роли `kubernetes`; кандидаты с проверенными версиями остаются
здесь, чтобы не искать их заново.

- [ ] **Chaos Mesh** — chaos-платформа для Kubernetes: CRD на все типы сбоев
      (Pod, Network, DNS, HTTP, Stress, IO, Time, Kernel, JVM, Block,
      PhysicalMachine, AWS/Azure/GCP), `Schedule`/`Workflow`/`StatusCheck` и
      dashboard. *(`helm`)* —
      [chaos-mesh/chaos-mesh](https://github.com/chaos-mesh/chaos-mesh) —
      controller + привилегированный DaemonSet на нодах + webhooks;
      локального сценария нет.
- [ ] **chaosblade** — chaos-тулкит: хост, контейнеры (Docker/CRI), k8s, JVM и
      middleware (mysql, kafka, redis, dubbo). *(`бинарник`)* —
      [chaosblade-io/chaosblade](https://github.com/chaosblade-io/chaosblade) —
      `v1.8.2` (2026-10-21), статический `chaosblade-1.8.2-linux_amd64.tar.gz`
      (53.8 МБ), на Ubuntu 26.04 `blade version` запускается. В k8s нужен
      `chaosblade-operator` в кластере. Не берём: хост-сценарии на рабочем
      ноутбуке не нужны, а кластерный chaos — не задача плейбука.
- [ ] **Chaos Toolkit** — декларативные эксперименты (JSON/YAML) с пробами и
      откатами. *(`pipx`)* —
      [chaostoolkit/chaostoolkit](https://github.com/chaostoolkit/chaostoolkit) —
      `1.21.4` (2026-10-05) + драйвер `chaostoolkit-kubernetes` `0.39.0`; на
      Python 3.14.4 `pipx install` и `pipx inject` проходят, `chaosk8s`
      импортируется. Действия: delete/terminate/exec подов,
      cordon/drain/delete нод, scale/rollout/delete деплойментов,
      scale/remove стейтфулсетов; пробы — здоровье подов, количество, фаза,
      логи. Сетевых, IO- и stress-сбоев нет. Не берём: сценарии на ноутбуке
      не нужны, а кластерный chaos — не задача плейбука. Оговорка:
      `chaos discover` вызывает исполняемый `pip`, которого в pipx-venv нет.
- [ ] **chaosd** — chaos-тулкит Chaos Mesh для машин и контейнеров вне
      Kubernetes (CPU, память, диск, сеть, процессы). *(`бинарник`)* —
      [chaos-mesh/chaosd](https://github.com/chaos-mesh/chaosd) — в релизах
      `v1.4.0`–`v1.5.0` только исходники, linux-amd64 ассетов нет (нужен
      `make build`); не берём: хост-level chaos на ноутбуке не нужен, а
      собирать из исходников ради него — лишний шаг.
- [ ] **pumba** — chaos для контейнеров Docker/containerd: kill/stop/restart/
      pause, netem (задержка, потери, дублирование, порча пакетов, лимит
      скорости), stress CPU/памяти/IO, режимы interval и random.
      *(`бинарник`)* — [alexei-led/pumba](https://github.com/alexei-led/pumba) —
      `v1.2.1` (2026-08-23), одиночный `pumba_linux_amd64`. Убран из роли
      `kubernetes` 2026-10-25: работает через Docker API, то есть требует
      доступа к сокету контейнерного рантайма и проверяет отказ живой рабочей
      машины, а не приложения.
- [ ] **chaoskube** — случайное убийство подов для проверки отказоустойчивости;
      фильтры по namespace/меткам/аннотациям/владельцу и quiet times.
      *(`helm`)* — [linki/chaoskube](https://github.com/linki/chaoskube) —
      может работать и с ноутбука по `--kubeconfig`, но по умолчанию
      выключенный dry-run легко снять и убить `kube-system` и себя.
- [ ] **kube-monkey** — Chaos Monkey для Kubernetes: удаление подов по
      расписанию, opt-in метками, MTBF, чёрные окна и dry-run по умолчанию.
      *(`helm`)* — [asobti/kube-monkey](https://github.com/asobti/kube-monkey)
- [ ] **kubeinvaders** — chaos-игра про поды кластера. *(`образ`)* —
      [lucky-sideburn/kubeinvaders](https://github.com/lucky-sideburn/kubeinvaders)

- [ ] **rancher** — платформа управления кластерами с UI. *(`helm` /
      `сервис`)* — [rancher/rancher](https://github.com/rancher/rancher) —
      сервер с веб-интерфейсом; CLI нужен только для работы с ним.

## 7. Знания, совместная работа и удалённый доступ

- [ ] **n8n** — автоматизация workflow с веб-UI. *(`сервис`)* —
      [n8n-io/n8n](https://github.com/n8n-io/n8n)
- [ ] **open-webui** — веб-UI для LLM и RAG. *(`сервис`)* —
      [open-webui/open-webui](https://github.com/open-webui/open-webui)
- [ ] **plausible** — self-hosted веб-аналитика. *(`сервис`)* —
      [plausible/analytics](https://github.com/plausible/analytics)
- [ ] **rustdesk** — self-hosted relay для удалённого доступа. *(`сервис`)* —
      [rustdesk/rustdesk](https://github.com/rustdesk/rustdesk)
- [ ] **joplin** — сервер синхронизации заметок. *(`сервис`)* —
      [laurent22/joplin](https://github.com/laurent22/joplin)
- [ ] **AFFiNE** — рабочее пространство с документами и досками.
      *(`сервис`)* — [toeverything/AFFiNE](https://github.com/toeverything/AFFiNE)
- [ ] **siyuan** — заметки с self-hosted синхронизацией. *(`сервис`)* —
      [siyuan-note/siyuan](https://github.com/siyuan-note/siyuan)
- [ ] **logseq** — заметки; десктоп-приложение, серверного пакета для
      ноутбука нет. *(`клиент`)* —
      [logseq/logseq](https://github.com/logseq/logseq)
- [ ] **excalidraw** — доски; self-hosted вариант — отдельный сервис.
      *(`сервис`)* — [excalidraw/excalidraw](https://github.com/excalidraw/excalidraw)
- [ ] **bruno** — GUI-клиент для API; ставится вручную (deb/AppImage), в
      плейбуке его нет. *(`клиент`)* —
      [usebruno/bruno](https://github.com/usebruno/bruno)

---

## Что дальше

- [ ] В плейбук ничего из этого списка не берём: он про ноутбук, а не про
      серверы и кластеры.
- [ ] Если понадобится поднять что-то из списка — отдельный хост, отдельный
      `docker compose` или Helm-релиз, а не роль `binaries`.
- [ ] Агенты на нодах (`node_exporter`, `goldpinger`, `kured`, eBPF-агенты)
      оформлять Helm-чартом или DaemonSet-манифестами, а не ролью `binaries`,
      даже когда у проекта есть linux-amd64 бинарник.
- [ ] Сверять при обновлении списка звёзд: у части проектов может появиться
      standalone-режим или удобный CLI, тогда кандидат переезжает в
      [`TODO.md`](TODO.md) как установленный. То же и для агентов: если
      появится режим без kubelet, кандидат становится ролью `binaries`.
- [ ] `VictoriaMetrics` сюда **не** относится: у него есть single-binary
      режим для локального запуска, поэтому он стоит в роли `monitoring`
      (из VictoriaMetrics — только `vmalert-tool`).
