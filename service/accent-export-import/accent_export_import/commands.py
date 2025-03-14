# Copyright 2023 Accent Communications

import csv
import sys

from cliff import command

from .helpers.constants import RESOURCE_FIELDS
from .helpers.import_set import ImportSet
from .helpers.importer import AccentAPI
from .helpers.ods import DumpFile


class Import(command.Command):
    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument("--username", required=True)
        parser.add_argument("--password", required=True)
        tenant_selector = parser.add_mutually_exclusive_group(required=True)
        tenant_selector.add_argument("--tenant", dest="tenant_uuid")
        tenant_selector.add_argument("--tenant-slug", dest="tenant_slug")
        parser.add_argument(
            "filename",
            help="dump filename to read from",
        )
        return parser

    def take_action(self, parsed_args):
        with DumpFile(parsed_args.filename, mode="r") as dump_file:
            import_set = ImportSet(dump_file.get_resources(), RESOURCE_FIELDS)

        import_set.check_references()

        tenant_args = {}
        if parsed_args.tenant_uuid:
            tenant_args["tenant_uuid"] = parsed_args.tenant_uuid
        elif parsed_args.tenant_slug:
            tenant_args["tenant_slug"] = parsed_args.tenant_slug
        proxy = AccentAPI(parsed_args.username, parsed_args.password, **tenant_args)
        proxy.import_all(import_set)


class ListResources(command.Command):
    def take_action(self, parsed_args):
        return " ".join(RESOURCE_FIELDS.keys())


class ListFields(command.Command):
    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        relation = parser.add_mutually_exclusive_group(required=True)
        for resource in RESOURCE_FIELDS:
            relation.add_argument(
                f"--{resource}",
                dest="resource",
                action="store_const",
                const=resource,
            )
        return parser

    def take_action(self, parsed_args):
        return " ".join(RESOURCE_FIELDS[parsed_args.resource]["fields"].keys())


class Add(command.Command):
    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        relation = parser.add_mutually_exclusive_group(required=True)
        for resource in RESOURCE_FIELDS:
            relation.add_argument(
                f"--{resource}",
                dest="resource",
                action="store_const",
                const=resource,
            )
        parser.add_argument(
            "filename",
            help="dump filename to the resources to",
        )
        return parser

    def take_action(self, parsed_args):
        reader = csv.DictReader(sys.stdin)
        first_row = True
        with DumpFile(parsed_args.filename, mode="r+w") as dump_file:
            for row in reader:
                if first_row:
                    self._validate_columns(parsed_args.resource, row)
                    first_row = False
                self._add_or_update_resource(dump_file, parsed_args.resource, row)

    def _validate_columns(self, resource, row):
        known_columns = set(RESOURCE_FIELDS[resource]["fields"].keys())
        user_supplied_columns = set(row.keys())

        unknown_columns = user_supplied_columns - known_columns
        if unknown_columns:
            raise Exception(f"unknown columns {','.join(unknown_columns)}")

    def _add_or_update_resource(self, dump_file, resource, row):
        try:
            index = self._find_matching_resource(dump_file, resource, row)
            dump_file.update_row(resource, index, row)
        except LookupError:
            dump_file.add_row(resource, row)

    def _find_matching_resource(self, dump_file, resource, row):
        selections = RESOURCE_FIELDS[resource]["unique"]
        for unique_columns in selections:
            row_has_all_columns = set(row.keys()).issuperset(set(unique_columns))
            if row_has_all_columns:
                pairs = [(key, row[key]) for key in unique_columns]
                try:
                    return dump_file.find_matching_row(resource, pairs)
                except LookupError:
                    continue
        raise LookupError("No resource matching")


class New(command.Command):
    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            "filename",
            help="dump filename to the resources to",
        )
        return parser

    def take_action(self, parsed_args):
        with DumpFile(parsed_args.filename, mode="r+w"):
            # Dump creation side effect
            pass
