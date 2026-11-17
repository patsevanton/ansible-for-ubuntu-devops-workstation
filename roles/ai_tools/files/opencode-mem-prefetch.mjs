// Предзагрузка модели эмбеддингов для opencode-mem.
//
// Плагин качает модель при первом поиске, поэтому первый запрос в холодном
// процессе ждёт скачивание (bge-m3 q8 — около 560 МБ) и прогрев ONNX. Скрипт
// делает то же самое заранее: берёт transformers из npm-кэша самого плагина
// (отдельную копию не ставим), кладёт веса в кэш плагина и прогоняет один
// эмбеддинг.
//
// Пути и модель передаются через окружение (OM_TRANSFORMERS, OM_CACHE_DIR,
// OM_MODEL, OM_DTYPE), чтобы не дублировать их в двух местах.
const { env, pipeline } = await import(process.env.OM_TRANSFORMERS);

env.cacheDir = process.env.OM_CACHE_DIR;
env.allowLocalModels = true;
env.allowRemoteModels = true;

const model = process.env.OM_MODEL;
const dtype = process.env.OM_DTYPE || "q8";

const extractor = await pipeline("feature-extraction", model, { dtype });
const out = await extractor(["проверка модели эмбеддингов"], { pooling: "cls", normalize: true });
console.log(`opencode-mem: ${model} (${dtype}) готова, выход ${out.dims.join("x")}`);
