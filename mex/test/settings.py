from pydantic import Field, SecretStr

from mex.common.settings import BaseSettings
from mex.test.types import APIKeyDatabase, APIUserDatabase


class testSettings(BaseSettings):
    """Settings definition for the test server."""

    test_host: str = Field(
        "localhost",
        min_length=1,
        max_length=250,
        description="Host that the test server will run on.",
        validation_alias="MEX_test_HOST",
    )
    test_port: int = Field(
        8080,
        gt=0,
        lt=65536,
        description="Port that the test server should listen on.",
        validation_alias="MEX_test_PORT",
    )
    test_root_path: str = Field(
        "",
        description="Root path that the test server should run under.",
        validation_alias="MEX_test_ROOT_PATH",
    )
    graph_url: str = Field(
        "neo4j://localhost:7687",
        description="URL for connecting to the graph database.",
        validation_alias="MEX_GRAPH_URL",
    )
    graph_db: str = Field(
        "neo4j",
        description="Name of the default graph database.",
        validation_alias="MEX_GRAPH_NAME",
    )
    graph_user: SecretStr = Field(
        SecretStr("neo4j"),
        description="Username for authenticating with the graph database.",
        validation_alias="MEX_GRAPH_USER",
    )
    graph_password: SecretStr = Field(
        SecretStr("password"),
        description="Password for authenticating with the graph database.",
        validation_alias="MEX_GRAPH_PASSWORD",
    )
    graph_tx_timeout: int | float = Field(
        15.0,
        description=(
            "The graph transaction timeout in seconds. "
            "A 0 duration will make the transaction execute indefinitely. "
            "None will use the default timeout configured on the server."
        ),
        validation_alias="MEX_GRAPH_TX_TIMEOUT",
    )
    graph_session_timeout: int | float = Field(
        45.0,
        description=(
            "Maximum time transactions are allowed to retry via tx functions."
        ),
        validation_alias="MEX_GRAPH_SESSION_TIMEOUT",
    )
    test_api_key_database: APIKeyDatabase = Field(
        APIKeyDatabase(),
        description="Database of API keys.",
        validation_alias="MEX_test_API_KEY_DATABASE",
    )
    test_user_database: APIUserDatabase = Field(
        APIUserDatabase(),
        description="Database of users.",
        validation_alias="MEX_test_API_USER_DATABASE",
    )
    redis_url: SecretStr | None = Field(
        None,
        description="Fully qualified URL of a redis cache server.",
        validation_alias="MEX_test_REDIS_URL",
    )
