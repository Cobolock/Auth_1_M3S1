import logging

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from auth.core.config import jaeger_settings

logger = logging.getLogger(__name__)


def configure_tracer_provider() -> TracerProvider:
    resource = Resource.create(attributes={"service.name": "auth-api"})
    tracer = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer)
    if jaeger_settings.agent_host and jaeger_settings.agent_port:
        logger.warning("Jaeger is disabled.")
        tracer.add_span_processor(
            BatchSpanProcessor(
                JaegerExporter(agent_host_name=jaeger_settings.agent_host, agent_port=6831)
            )
        )
    if jaeger_settings.console_output:
        tracer.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    return tracer


tracer_provider = configure_tracer_provider()
