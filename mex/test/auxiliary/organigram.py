from typing import cast

from mex.common.models import ExtractedOrganizationalUnit
from mex.common.organigram.extract import extract_organigram_units
from mex.common.organigram.transform import (
    transform_organigram_units_to_organizational_units,
)
from mex.test.auxiliary.primary_source import (
    extracted_primary_source_organigram,
)
from mex.test.extracted.helpers import search_extracted_items_in_graph
from mex.test.graph.connector import GraphConnector


def extracted_organizational_units() -> list[ExtractedOrganizationalUnit]:
    """Auxiliary function to get ldap as primary resource and ingest org units."""
    organigram_units = extract_organigram_units()
    organigram_primary_source = extracted_primary_source_organigram()

    unit_container = search_extracted_items_in_graph(
        entity_type=["ExtractedOrganizationalUnit"],
        referenced_identifiers=[organigram_primary_source.stableTargetId],
        reference_field="hadPrimarySource",
        limit=len(organigram_units),
    )
    if unit_container.total >= len(organigram_units):
        return cast("list[ExtractedOrganizationalUnit]", unit_container.items)

    extracted_units = transform_organigram_units_to_organizational_units(
        organigram_units, organigram_primary_source
    )
    connector = GraphConnector.get()
    connector.ingest(extracted_units)
    return extracted_units
