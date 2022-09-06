from rest_framework.schemas.openapi import SchemaGenerator


class NoPermissionSchemaGenerator(SchemaGenerator):
    def has_view_permissions(self, path, method, view):
        return True
