from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Union

from flask_marshmallow.sqla import SQLAlchemyAutoSchema  # type: ignore[import]
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.query import Query
from sqlalchemy import select

from fullask_rest_framework.httptypes.filtering import FilteringRequest
from fullask_rest_framework.httptypes.pagination import (
    PaginationRequest,
    PaginationResponse,
)
from fullask_rest_framework.httptypes.sorting import SortingRequest
from fullask_rest_framework.repositories.base import T
from fullask_rest_framework.repositories.crud import CRUDRepositoryABC


class SQLAlchemyFullRepository(CRUDRepositoryABC, ABC, Generic[T]):
    """
    The implementation of CRUDRepositoryABC, with SQLAlchemy.
    this implementation has dependency with flask-sqlalchemy's SQLAlchemy object.
    """

    def __init__(self, db: SQLAlchemy):
        self.db: SQLAlchemy = db
        self._model: SQLAlchemy.Model = self.get_model()

    @abstractmethod
    def get_model(self):
        pass

    def save(self, entity: T) -> T:
        self.db.session.add(entity)
        self.db.session.flush()
        return entity

    def save_all(self, entities: List[T]) -> List[T]:
        saved_entities = []
        for entity in entities:
            saved_entity = self.save(entity)
            saved_entities.append(saved_entity)
        return saved_entities

    def read_by_id(self, id: int) -> Optional[T]:
        query_result = self.db.session.get(self._model, id)
        return query_result if query_result else None

    def is_exists_by_id(self, id) -> bool:
        return bool(self.db.session.get(self._model, id))

    def read_all(
        self,
        pagination_request: Optional[PaginationRequest] = None,
        sorting_request: Optional[SortingRequest] = None,
        filtering_request: Optional[FilteringRequest] = None,
    ) -> Union[List[Optional[T]] | PaginationResponse[T]]:
        query = self._get_base_query()
        if filtering_request:
            query = self._filtering(query=query, filtering_request=filtering_request)
        if sorting_request:
            query = self._sorting(query=query, sorting_request=sorting_request)
        if pagination_request:
            query = query.paginate(
                page=pagination_request.page,
                per_page=pagination_request.per_page,
                error_out=False,
            )
            return PaginationResponse(
                count=query.total,
                next_page=query.next_num,
                previous_page=query.prev_num,
                results=[item for item in query.items],
            )
        else:
            return [
                query_result
                for query_result in self.db.session.execute(select(self._model))
                .scalars()
                .all()
            ]

    def read_all_by_ids(self, ids: List[int]) -> List[Optional[T]]:
        return [self.read_by_id(_id) for _id in ids]

    def count(self) -> int:
        return self.db.session.query(self._model).count()

    def delete_by_id(self, id: int) -> None:
        model_instance = self.db.session.get(self._model, id)
        if model_instance:
            self.db.session.delete(model_instance)
        else:
            raise ValueError(f"{self._model} with id {id} not found.")

    def delete(self, entity) -> None:
        model_instance = self.db.session.get(self._model, entity.id)
        if not model_instance:
            raise ValueError(
                f"{self._model} with entity {entity} not found.\n"
                f"make sure the entity instance is stored in database."
            )
        self.db.session.delete(model_instance)
        self.db.session.flush()

    def delete_all_by_ids(self, ids: List[int]) -> None:
        self.db.session.query(self._model).filter(self._model.id.in_(ids)).delete()

    def delete_all(self) -> None:
        self._model.query.delete()

    def _get_base_query(self) -> Query:
        return self.db.session.query(self._model)

    def _filtering(self, query: Query, filtering_request: FilteringRequest) -> Query:
        """
        filter the query with filtering_object.
        this is implementation of `or` condition.
        """
        for field, word in vars(filtering_request).items():
            query = query.filter(getattr(self._model, field).ilike(f"%{word}%"))
        return query

    def _sorting(self, query: Query, sorting_request: SortingRequest) -> Query:
        for field, direction in vars(sorting_request).items():
            if direction == "asc":
                query = query.order_by(getattr(self._model, field).asc())
            elif direction == "desc":
                query = query.order_by(getattr(self._model, field).desc())
        return query
