from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_core import SchemaError, ValidationError

from mex.common.cli import entrypoint
from mex.common.connector import CONNECTOR_STORE
from mex.common.logging import logger
from mex.test.auxiliary.ldap import router as ldap_router
from mex.test.auxiliary.orcid import router as orcid_router
from mex.test.auxiliary.wikidata import router as wikidata_router
from mex.test.exceptions import (
    handle_detailed_error,
    handle_uncaught_exception,
    testError,
)
from mex.test.extracted.main import router as extracted_router
from mex.test.identity.main import router as identity_router
from mex.test.ingest.main import router as ingest_router
from mex.test.logging import UVICORN_LOGGING_CONFIG
from mex.test.merged.main import router as merged_router
from mex.test.preview.main import router as preview_router
from mex.test.rules.main import router as rules_router
from mex.test.security import has_read_access, has_write_access
from mex.test.settings import testSettings
from mex.test.system.main import router as system_router

startup_tasks: list[Callable[[], Any]] = [
    testSettings.get,
]
teardown_tasks: list[Callable[[], Any]] = [
    CONNECTOR_STORE.reset,
]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Async context manager to execute startup and teardown of the FastAPI app."""
    for task in startup_tasks:
        task()
        task_name = getattr(task, "__wrapped__", task).__name__
        logger.info(f"startup {task_name} complete")
    yield None
    for task in teardown_tasks:
        task()
        task_name = getattr(task, "__wrapped__", task).__name__
        logger.info(f"teardown {task_name} complete")


app = FastAPI(
    title="mex-test",
    summary="Robert Koch-Institut Metadata Exchange API",
    description=(
        "The MEx API includes endpoints for multiple use-cases, "
        "e.g. for extractor pipelines, the MEx editor or inter-departmental access."
    ),
    contact={
        "name": "RKI MEx Team",
        "email": "mex@rki.de",
        "url": "https://github.com/robert-koch-institut/mex-test",
    },
    lifespan=lifespan,
    version="v0",
)
router = APIRouter(prefix="/v0")
router.include_router(extracted_router, dependencies=[Depends(has_read_access)])
router.include_router(identity_router, dependencies=[Depends(has_write_access)])
router.include_router(ingest_router, dependencies=[Depends(has_write_access)])
router.include_router(ldap_router, dependencies=[Depends(has_read_access)])
router.include_router(merged_router, dependencies=[Depends(has_read_access)])
router.include_router(orcid_router, dependencies=[Depends(has_read_access)])
router.include_router(preview_router, dependencies=[Depends(has_read_access)])
router.include_router(rules_router, dependencies=[Depends(has_write_access)])
router.include_router(wikidata_router, dependencies=[Depends(has_read_access)])

router.include_router(system_router)

app.include_router(router)
app.add_exception_handler(testError, handle_detailed_error)
app.add_exception_handler(SchemaError, handle_detailed_error)
app.add_exception_handler(ValidationError, handle_detailed_error)
app.add_exception_handler(Exception, handle_uncaught_exception)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=["*"],
)


@entrypoint(testSettings)
def main() -> None:  # pragma: no cover
    """Start the test server process.

    Initializes and runs the FastAPI application using uvicorn server.
    Loads configuration from testSettings and starts the HTTP server
    on the configured host and port.
    """
    settings = testSettings.get()
    uvicorn.run(
        "mex.test.main:app",
        host=settings.test_host,
        port=settings.test_port,
        root_path=settings.test_root_path,
        reload=settings.debug,
        log_config=UVICORN_LOGGING_CONFIG,
        headers=[("server", "mex-test")],
    )
