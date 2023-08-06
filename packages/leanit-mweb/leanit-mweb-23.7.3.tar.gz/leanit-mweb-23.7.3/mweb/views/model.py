from __future__ import annotations

import json
import logging
from pprint import pprint
from urllib.parse import quote, urlencode

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response

from mweb import templates
from mweb.orm.model import Model
from mweb.utils import flatten, unflatten

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    pass

def _flip_order_by(order_by: str) -> str:
    """
    "tenant_id,id" -> "-tenant_id,-id"
    "-tenant_id,-id" -> "tenant_id,id"
    """
    return ",".join([f"-{field}" if not field.startswith("-") else field[1:] for field in order_by.split(",")])

class ModelView:
    model: Model
    template_directory: str
    list_limit = 10
    list_fields = []
    list_order_by = "ASC"

    def __init__(self, request: Request):
        self.request = request

        # merge query params and path params (path params take precedence)
        self.params = dict(self.request.query_params)
        self.params.update(dict(self.request.path_params))

        self.object = None
        self.object_list = None

    async def get_context(self, **kwargs):
        template_context = {
            "request": self.request,
        }

        template_context.update(kwargs)

        return template_context

    async def get_object(self) -> Model:
        pk_dict = {}
        for pk_field_name in self.model._pk:
            try:
                pk_dict[pk_field_name] = self.params[pk_field_name]
            except KeyError:
                raise HTTPException(status_code=400, detail=f"Missing required parameter: {pk_field_name}")

        self.object = await self.model.get_async(**pk_dict)
        if not self.object:
            raise HTTPException(status_code=404, detail=f"Object not found: {pk_dict}")

        return self.object

    async def get_object_list(self) -> List[Model]:
        _only = None
        if self.list_fields:
            _only = self.list_fields

        filter = {}

        order_by = ",".join(self.model._pk)
        if self.list_order_by == "DESC":
            order_by = _flip_order_by(order_by)

        page_direction = self.request.query_params.get('page-direction', "gt")

        order_flipped = False
        page_border = self.request.query_params.get('page-border', None)
        if page_border:
            page_border_tuple = unflatten(page_border)
            page_border_tuple_len = len(page_border_tuple)

            if page_direction == "gt":
                filter.update({f"{k}__gte" if i < page_border_tuple_len - 1 else f"{k}__gt": v for i, (k, v) in enumerate(page_border_tuple)})
                if self.list_order_by == "DESC":
                    order_by = _flip_order_by(order_by)
                    order_flipped = True
            elif page_direction == "gte":
                filter.update({f"{k}__gte": v for k, v in page_border_tuple})
                if self.list_order_by == "DESC":
                    order_by = _flip_order_by(order_by)
                    order_flipped = True
            elif page_direction == "lt":
                filter.update({f"{k}__lte" if i < page_border_tuple_len - 1 else f"{k}__lt": v for i, (k, v) in enumerate(page_border_tuple)})
                # order_by = ','.join([f"-{k}" for k, v in page_border_tuple])
                if self.list_order_by == "ASC":
                    order_by = _flip_order_by(order_by)
                    order_flipped = True
            elif page_direction == "lte":
                filter.update({f"{k}__lte": v for k, v in page_border_tuple})
                # order_by = ','.join([f"-{k}" for k, v in page_border_tuple])
                if self.list_order_by == "ASC":
                    order_by = _flip_order_by(order_by)
                    order_flipped = True
            else:
                raise HTTPException(status_code=400, detail=f"Invalid page-direction: {page_direction}")

        self.object_list = await self.model.filter_async(_limit=self.list_limit, _only=_only, _order_by=order_by, **filter)
        if order_flipped:
            self.object_list.reverse()

        return self.object_list

    def get_detail_template(self):
        return f"{self.template_directory}/detail.html"

    def get_edit_template(self):
        return f"{self.template_directory}/edit.html"

    def get_list_template(self):
        return f"{self.template_directory}/list.html"

    async def render_detail(self, **kwargs) -> Response:
        await self.get_object()

        template_context = await self.get_context(object=self.object, **kwargs)

        return templates.TemplateResponse(self.get_detail_template(), template_context)

    async def render_list(self, **kwargs) -> Response:
        await self.get_object_list()
        object_list = self.object_list

        page = int(self.request.query_params.get('page', 1))
        pagination = {
            "has_previous": False,
            "has_next": False,
            "page": page,
        }

        # default to "gt" - greater than
        page_direction = self.request.query_params.get('page-direction', "gt")
        page_is_full = len(object_list) == self.list_limit
        page_is_empty = len(object_list) == 0

        new_params = dict(self.request.query_params)

        if page_is_full:
            pagination["has_next"] = True

            pk_of_last_object = object_list[-1].pk_value_tuple
            flattened_pk = flatten(pk_of_last_object)

            next_url_params = new_params.copy()
            next_url_params["page"] = str(page + 1)
            next_url_params["page-direction"] = "gt" if self.list_order_by == "ASC" else "lt"
            next_url_params["page-border"] = flattened_pk

            pagination["next_url"] = self.request.url.path + "?" + urlencode(next_url_params)

        if page > 1:
            pagination["has_previous"] = True

            previous_url_params = new_params.copy()
            previous_url_params["page"] = str(page - 1)
            previous_url_params["page-direction"] = "lt" if self.list_order_by == "ASC" else "gt"

            if page_is_empty:
                previous_url_params["page-border"] = self.request.query_params["page-border"]
                previous_url_params["page-direction"] = "lte" if self.list_order_by == "ASC" else "gte"
            else:
                pk_of_first_object = object_list[0].pk_value_tuple
                flattened_pk = flatten(pk_of_first_object)

                previous_url_params["page-border"] = flattened_pk

            pagination["previous_url"] = self.request.url.path + "?" + urlencode(previous_url_params)

        template_context = await self.get_context(object_list=object_list, **kwargs)
        template_context["pagination"] = pagination

        return templates.TemplateResponse(self.get_list_template(), template_context)
