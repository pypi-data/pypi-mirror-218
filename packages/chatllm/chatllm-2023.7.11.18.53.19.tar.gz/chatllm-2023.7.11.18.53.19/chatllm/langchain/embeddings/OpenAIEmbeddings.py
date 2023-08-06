#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : OpenAIEmbeddings
# @Time         : 2023/7/11 18:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from langchain.embeddings import OpenAIEmbeddings as _OpenAIEmbeddings
import langchain

OPENAI_API_KEY_SET = (
    os.getenv("OPENAI_API_KEY_SET", "").replace(' ', '').strip(',').strip().split(',') | xfilter() | xset  # 获取keys
)

OPENAI_API_KEY_PATH = os.getenv("OPENAI_API_KEY_PATH")

if OPENAI_API_KEY_PATH and Path(OPENAI_API_KEY_PATH).is_file():
    OPENAI_API_KEY_SET = set(Path(OPENAI_API_KEY_PATH).read_text().strip().split())

MAX_WORKERS = max(len(OPENAI_API_KEY_SET), 1)


class OpenAIEmbeddings(_OpenAIEmbeddings):
    """多key多线程"""

    def embed_documents(
        self, texts: List[str], chunk_size: Optional[int] = 0
    ) -> List[List[float]]:
        if MAX_WORKERS > 1:
            embeddings_map = {}
            for i, openai_api_key in enumerate(OPENAI_API_KEY_SET):
                kwargs = self.dict()
                kwargs['openai_api_key'] = openai_api_key
                embeddings_map[i] = _OpenAIEmbeddings(**kwargs)

            if langchain.debug:
                logger.info([e.openai_api_key for e in embeddings_map.values()])
                logger.info(f"Maximum concurrency: {MAX_WORKERS * self.chunk_size}")

            def __embed_documents(arg):
                idx, texts = arg
                embeddings = embeddings_map.get(idx % MAX_WORKERS, 0)
                return embeddings.embed_documents(texts)

            return (
                texts | xgroup(self.chunk_size)
                | xenumerate
                | xThreadPoolExecutor(__embed_documents, MAX_WORKERS)
                | xchain_
            )

        return super().embed_documents(texts)
