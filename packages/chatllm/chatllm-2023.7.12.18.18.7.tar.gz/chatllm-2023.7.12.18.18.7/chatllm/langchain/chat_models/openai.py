#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : callbacks
# @Time         : 2023/7/12 17:37
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from threading import Thread

from langchain.chat_models import ChatOpenAI as _ChatOpenAI
from langchain.callbacks import AsyncIteratorCallbackHandler
from chatllm.langchain.callbacks import StreamingGeneratorCallbackHandler

from meutils.pipe import *


class ChatOpenAI(_ChatOpenAI):

    def stream(self, text: str, *, stop: Optional[Sequence[str]] = None, **kwargs: Any) -> Generator:
        """Stream the answer to a query.

        NOTE: this is a beta feature. Will try to build or use
        better abstractions about response handling.

        """
        _predict = partial(self.predict, stop=stop)

        handler = StreamingGeneratorCallbackHandler()
        self.callbacks = [handler]
        self.streaming = True

        #  background_tasks.add_task(_predict, text, **kwargs)
        thread = Thread(target=_predict, args=[text], kwargs=kwargs)
        thread.start()

        return handler.get_response_gen()

    async def astream(self, text: str, *, stop: Optional[Sequence[str]] = None, **kwargs: Any) -> AsyncGenerator:

        handler = AsyncIteratorCallbackHandler()
        self.callbacks = [handler]
        self.streaming = True

        if not getattr(self, "streaming", False):
            raise ValueError("LLM must support streaming and set streaming=True.")

        task = asyncio.create_task(self.apredict(text, stop=stop, **kwargs))

        async for token in handler.aiter():
            yield token


if __name__ == '__main__':
    llm = ChatOpenAI(streaming=True, temperature=0)
    for i in llm.stream('你好'):
        print(i, end='')

    async for token in llm.astream('你好'):
        print(token, end='')
