import logging

import orjson
import structlog.types
from structlog import processors

from logs.config import Config, LogsRenderer


class AsyncBindableLogger(
    structlog.stdlib.AsyncBoundLogger,
    structlog.types.BindableLogger,
): ...


def startup(config: Config) -> None:
    pre_chain = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt=config.time_format, utc=config.utc),
    ]

    handler = logging.StreamHandler()
    handler.set_name("default")
    handler.setLevel(config.level)

    if config.call_site:
        pre_chain.append(processors.CallsiteParameterAdder())

    if config.renderer == LogsRenderer.text:
        renderer = structlog.dev.ConsoleRenderer(colors=True)
    elif config.renderer == LogsRenderer.json:
        renderer = processors.JSONRenderer(
            serializer=lambda data, **kwargs: orjson.dumps(data).decode(),
        )
    else:
        raise ValueError("Logging: Unknown renderer set")

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
        foreign_pre_chain=pre_chain,
    )
    handler.setFormatter(formatter)

    logging.basicConfig(handlers=(handler,), level=config.level)
    structlog.configure(
        processors=[
            *pre_chain,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=AsyncBindableLogger,
        cache_logger_on_first_use=True,
    )
