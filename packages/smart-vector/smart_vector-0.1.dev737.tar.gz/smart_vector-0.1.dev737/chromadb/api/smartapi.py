from chromadb.api.types import (
    Embeddings,
    Include,
    QueryResult,
    Where,
    WhereDocument,
)
from overrides import override
from chromadb.api.local import LocalAPI

UUID = str

class SmartAPI(LocalAPI):

    @override
    def _query(
            self,
            collection_id: UUID,
            query_embeddings: Embeddings,
            n_results: int = 10,
            where: Where = {},
            where_document: WhereDocument = {},
            include: Include = ["documents", "metadatas", "distances"],
    ) -> QueryResult:
        query_result = self._db.get_nearest_neighbors_smart(
            collection_uuid=collection_id,
            where=where,
            where_document=where_document,
            embeddings=query_embeddings,
            n_results=n_results,
        )

        return query_result

    @override
    def _add(
            self,
            ids,
            collection_id: UUID,
            embeddings: Embeddings,
            metadatas=None,
            documents=None,
            increment_index: bool = True,
    ) -> bool:
        added_uuids = self._db.add(
            collection_id,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents,
            ids=ids,
        )
        return True
