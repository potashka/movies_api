from elasticsearch import AsyncElasticsearch

es: AsyncElasticsearch | None = None   # изменено

async def get_elastic() -> AsyncElasticsearch:
    if es is None:
        raise RuntimeError("Elastic disabled in DOCS_ONLY mode")
    return es
