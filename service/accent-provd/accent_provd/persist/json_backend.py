# Copyright 2023 Accent Communications

from __future__ import annotations

import json
import logging
import os
from collections.abc import Generator
from copy import deepcopy
from typing import Any, Literal

from accent_provd.persist.common import (
    AbstractBackend,
    AbstractDatabase,
    AbstractDatabaseFactory,
)
from accent_provd.persist.id import GeneratorFactory, get_id_generator_factory
from accent_provd.persist.util import (
    SimpleBackendDocumentCollection,
    new_backend_based_collection,
)

logger = logging.getLogger(__name__)


class JsonSimpleBackend(AbstractBackend):
    closed = False

    def __init__(self, directory: str) -> None:
        self._directory = directory
        self._dict: dict[str, Any] = {}
        self._load()
        self._closed = False

    def _load(self) -> None:
        if not os.path.isdir(self._directory):
            os.mkdir(self._directory)

        for rel_filename in os.listdir(self._directory):
            abs_filename = os.path.join(self._directory, rel_filename)
            try:
                fobj = open(abs_filename)
            except OSError as e:
                logger.warning('Could not open file %s: %s', abs_filename, e)
            else:
                try:
                    document = json.load(fobj)
                except ValueError as e:
                    logger.warning(
                        'Could not decode JSON document %s: %s', abs_filename, e
                    )
                else:
                    self._dict[rel_filename] = document
                finally:
                    fobj.close()

    def close(self) -> None:
        self._dict = {}
        self._closed = True

    def __getitem__(self, document_id: str) -> dict[str, Any]:
        return deepcopy(self._dict[document_id])

    def __setitem__(self, document_id: str, document: dict[str, Any]) -> None:
        self._dict[document_id] = deepcopy(document)
        abs_filename = os.path.join(self._directory, document_id)
        with open(abs_filename, 'w') as f:
            json.dump(document, fp=f, separators=(',', ':'))

    def __delitem__(self, document_id: str) -> None:
        del self._dict[document_id]
        abs_filename = os.path.join(self._directory, document_id)
        try:
            os.remove(abs_filename)
        except OSError as e:
            logger.info('Error while removing JSON document %s: %s', e)

    def __contains__(self, document_id: str) -> bool:
        return document_id in self._dict

    def values(self) -> Generator[dict[str, Any], None, None]:
        for document in self._dict.values():
            yield deepcopy(document)

    def items(self) -> Generator[tuple[str, dict[str, Any]], None, None]:
        for document_id, document in self._dict.items():
            yield document_id, deepcopy(document)


def new_json_collection(
    directory: str, generator: Generator[str, None, None]
) -> SimpleBackendDocumentCollection:
    return new_backend_based_collection(JsonSimpleBackend(directory), generator)


class JsonDatabase(AbstractDatabase):
    def __init__(
        self, base_directory: str, generator_factory: GeneratorFactory
    ) -> None:
        self._base_directory = base_directory
        self._generator_factory = generator_factory
        self._collections: dict[str, SimpleBackendDocumentCollection] = {}
        self._create_base_directory()

    def _create_base_directory(self) -> None:
        if not os.path.isdir(self._base_directory):
            os.makedirs(self._base_directory)

    def close(self) -> None:
        for collection in self._collections.values():
            collection.close()
        self._collections = {}

    def _new_collection(self, collection_id: str) -> SimpleBackendDocumentCollection:
        generator = self._generator_factory()
        directory = os.path.join(self._base_directory, collection_id)
        try:
            return new_json_collection(directory, generator)
        except Exception as e:
            # could not create collection
            raise ValueError(e)

    def collection(self, collection_id: str) -> SimpleBackendDocumentCollection:
        if (
            collection_id not in self._collections
            or self._collections[collection_id].closed
        ):
            self._collections[collection_id] = self._new_collection(collection_id)
        return self._collections[collection_id]


class JsonDatabaseFactory(AbstractDatabaseFactory):
    @staticmethod
    def new_database(
        db_type: str, generator: Literal['default', 'numeric', 'uuid'], **kwargs: Any
    ) -> JsonDatabase:
        if db_type != 'json':
            raise ValueError(f'unrecognised type "{db_type}"')
        try:
            base_directory = kwargs['json_db_dir']
        except KeyError:
            raise ValueError(f'missing "json_db_dir" arguments in "{kwargs}"')

        generator_factory = get_id_generator_factory(generator)
        return JsonDatabase(base_directory, generator_factory)
