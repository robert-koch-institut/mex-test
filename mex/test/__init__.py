from mex.common.identity.registry import register_provider
from mex.common.types import IdentityProvider
from mex.test.identity.provider import GraphIdentityProvider

register_provider(IdentityProvider.GRAPH, GraphIdentityProvider)
