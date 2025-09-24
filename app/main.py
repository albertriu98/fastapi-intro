from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, authentication, votes

from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

Instrumentator().instrument(app).expose(app)


# OpenTelemetry Tracing setup
resource = Resource.create(attributes={"service.name": "fastapi-app"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(
    endpoint="tempo-gateway.tempo.svc.cluster.local:4317",  # Tempo gRPC port
    insecure=True
)

span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(authentication.router)
app.include_router(votes.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

