"""Structured JSON logging via structlog.

In development we use a pretty console renderer.
In production the output is machine-parseable JSON suitable for
CloudWatch, Datadog, or any log aggregation system.
"""
import logging
import sys

import structlog


def configure_logging() -> None:
    """Configure structlog and stdlib logging once at startup."""
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if sys.stderr.isatty():
        # Developer console: coloured, pretty output
        renderer: structlog.types.Processor = structlog.dev.ConsoleRenderer()
    else:
        # Production: JSON for log aggregators
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
