# GAEL SYSTEMS CONFIDENTIAL
# __________________
#
# 2023 GAEL SYSTEMS
# All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of GAEL SYSTEMS,
# if any.  The intellectual and technical concepts contained
# herein are proprietary to GAEL SYSTEMS
# and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from GAEL SYSTEMS.
import json
import logging
import os
import uuid
from typing import Union

from drb.drivers.odata import (
    ExpressionFunc,
    ExpressionType, LogicalOperator,
    ComparisonOperator, GroupingOperator)

from pygssearch.utility import parse_date, footprint_extract

logger = logging.getLogger('pygssearch')


def __concat_query(query_a, query_b):
    if query_a is None:
        return query_b
    else:
        return LogicalOperator.lo_and(query_a, query_b)


def query_builder(
        filters: str = None,
        date: tuple = (None, None),
        geometry: Union[tuple, str] = (),
        id: Union[tuple, str, uuid.UUID] = (),
        name: Union[tuple, str] = (), mission: int = None,
        instrument: str = None, product_type: str = None,
        cloud: str = None, order: str = None) -> tuple:
    """
    Help to build the odata query corresponding to a series of
    filter given in argument,
    the user can give a filter already wrote and this builder
    will append it with a logical
    and to the query built.

    :param filters: (str) an already wrote Odata query to apply.
                    by default None.
    :param date: (tuple[str, str]) A tuple of date the first one corresponding
                 to the ContentDate/Start and the second one for the End
                 (by default (None, None)
    :param geometry: Can be a path to the geojson file containing a footprint
                     or a series of coordinate containing in a tuple separated
                     by a coma. default ()
    :param id: A series of uuid matching a series of product by default ()
    :param name: A series of complete name or part on the name of a product
                 this will call the contains method on the field name.
                 by default ()
    :param mission: Filter on the sentinel mission can be 1, 2, 3 or 5.
                    by default None
    :param instrument: Filter on the instrument.
                       by default None by default None
    :param product_type: Filter on the product type you want ot retrieve.
                         by default None
    :param cloud: Maximum cloud cover in percent by default None
    :param order: Specify the keyword to order the result.
                  Prefix ‘-’ for descending order. by default None

    :return: A tuple the first entry corresponding to the filter
             and the second to the order.
    """
    query = None
    query_order = None
    if filters:
        query = ExpressionType.property(filters)

    if mission is not None:
        query_mission = ExpressionFunc.startswith(
            ExpressionType.property('Name'),
            f'S{int(mission)}')
        query = __concat_query(query, query_mission)

    if instrument is not None:
        query_lambda = ExpressionFunc.any('d', LogicalOperator.lo_and(
            ComparisonOperator.eq(
                ExpressionType.property('d/Name'),
                ExpressionType.string('instrumentShortName')),
            ComparisonOperator.eq(
                ExpressionType.property('d/Value'),
                ExpressionType.string(instrument))))
        query_instrument = ExpressionType.property(
            f"StringAttributes/{query_lambda.evaluate()}")
        query = __concat_query(query, query_instrument)

    if product_type is not None:
        query_lambda = ExpressionFunc.any('d', LogicalOperator.lo_and(
            ComparisonOperator.eq(
                ExpressionType.property('d/Name'),
                ExpressionType.string('productType')),
            ComparisonOperator.eq(
                ExpressionType.property('d/Value'),
                ExpressionType.string(product_type))))
        query_type = ExpressionType.property(
            f"StringAttributes/{query_lambda.evaluate()}")
        query = __concat_query(query, query_type)

    if cloud is not None:
        query_lambda = ExpressionFunc.any(
            'd', LogicalOperator.lo_and(
                ComparisonOperator.eq(
                    ExpressionType.property(
                        'd/Name'), ExpressionType.string('cloudCover')),
                ComparisonOperator.lt(
                    ExpressionType.property(
                        'd/OData.CSC.DoubleAttribute/Value'),
                    ExpressionType.number(cloud))))
        query_could = ExpressionType.property(
            f"Attributes/OData.CSC.DoubleAttribute/{query_lambda.evaluate()}")
        query = __concat_query(query, query_could)

    if date[0] is not None or date[1] is not None:
        if date[0] is not None:
            parsed_date = parse_date(date[0])

            query_start = ComparisonOperator.ge(
                ExpressionType.property('ContentDate/Start'),
                ExpressionType.property(parsed_date))
            query = __concat_query(query, query_start)

        if len(date) > 1 and date[1] is not None:
            parsed_date = parse_date(date[1])

            query_end = ComparisonOperator.lt(
                ExpressionType.property('ContentDate/End'),
                ExpressionType.property(parsed_date))
            query = __concat_query(query, query_end)

    if len(geometry) > 0:
        if len(geometry) == 1 or isinstance(geometry, str):
            if os.path.exists(geometry[0]):
                with open(geometry[0]) as f:
                    geo = json.load(f)
            elif os.path.exists(geometry):
                with open(geometry) as f:
                    geo = json.load(f)
            geo = footprint_extract(geo)
        else:
            geo = []
            if isinstance(geometry[0], str):
                for e in geometry:
                    geo.append((
                        float(e.split(',')[0]),
                        float(e.split(',')[1])))
            else:
                for e in geometry:
                    geo.append((float(e[0]), float(e[1])))
        geometry = ExpressionType.footprint(geo)
        query_geo = ExpressionFunc.csc_intersect(ExpressionType.property(
            'location=Footprint'),
            ExpressionType.property(
                f'area={geometry.evaluate()}'))
        query = __concat_query(query, query_geo)

    if len(name) > 0:
        if isinstance(name, str):
            query_name = ExpressionFunc.contains(
                ExpressionType.property('Name'),
                name)
        elif len(name) == 1:
            query_name = ExpressionFunc.contains(
                ExpressionType.property('Name'),
                name[0])
        else:
            tmp = ''
            for n in name:
                tmp += ExpressionFunc.contains(
                    ExpressionType.property('Name'), n).evaluate() + ' or '
            query_name = GroupingOperator.group(
                ExpressionType.property(tmp[:len(tmp) - 4]))
        query = __concat_query(query, query_name)

    if isinstance(id, uuid.UUID) or isinstance(id, str):
        query_uuid = ComparisonOperator.eq(
            ExpressionType.property('Id'),
            ExpressionType.property(id))
        query = __concat_query(query, query_uuid)
    elif len(id) > 0:
        if len(id) == 1:
            query_uuid = ComparisonOperator.eq(
                ExpressionType.property('Id'),
                ExpressionType.property(id[0]))
        else:
            tmp = ''
            for product_id in id:
                tmp += ComparisonOperator.eq(
                    ExpressionType.property('Id'),
                    ExpressionType.property(product_id)).evaluate() + ' or '
            query_uuid = GroupingOperator.group(
                ExpressionType.property(tmp[:len(tmp) - 4]))
        query = __concat_query(query, query_uuid)

    if order is not None:
        if order.startswith('-'):
            query_order = (ExpressionType.property(order[1:]),
                           ExpressionType.property('desc'))
        else:
            query_order = (ExpressionType.property(order),
                           ExpressionType.property('asc'))

    if query is not None:
        logger.debug(f"The query build is {query.evaluate()}")

    return query, query_order
