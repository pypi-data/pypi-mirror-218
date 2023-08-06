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
import logging

from drb.drivers.odata import ODataQueryPredicate
from drb.drivers.odata.odata_services_nodes import ODataServiceNodeCSC
from requests.auth import AuthBase

from pygssearch.source.download import Download

logger = logging.getLogger('pygssearch')


class OdataSource:
    """
    ODataSource Class is the implementation of DrbNode retrieval from an OData
    service.

    :param service: (str) the url of the product
    :param auth: (AuthBase) the authentication to access the service
    """

    def __init__(self, service: str, auth: AuthBase = None):
        self._service = service
        self.auth = auth
        self.__odata_service = ODataServiceNodeCSC(self.service,
                                                   auth=self.auth)

    @property
    def service(self):
        """
        Property to retrieve the property field as a string.

        :return: the service url as string.
        """
        return self._service

    def request(
            self, query=None, query_order=None, limit=10,
            skip=0, format=('Name', 'Id')):
        """
        Request the odata services en retrieve the matching data.

        :param query: (Expression) The filter to apply in the query
                       by default None
        :param query_order: (tuple[Expression, Expression]) to order
                             the result of the query
        :param limit: (int) Limit the number of result by default 10.
        :param skip: (int) Skip a number of matching product by default 0.
        :param format: (tuple[str]) Format the return result of the query,
                       or put _ to print all available information,
                       by default ('Name', 'Id').

        :return: A list of dict containing all the data asked
                 if no matching product return an empty list.
        """
        request = self.__odata_service[
            ODataQueryPredicate(
                filter=query,
                order=query_order
            )]

        if len(request) < limit:
            limit = len(request)

        if format == '_' or format[0] == '_':
            format = [x[0] for x in request[0].attribute_names()]

        res = []
        for prd in [request[skip + x] for x in range(limit)]:
            meta = {}
            for e in format:
                meta[e] = prd @ e
            res.append(meta)

        return res

    def download(self, query=None, query_order=None,
                 limit=10, skip=0,
                 output='.', threads=2,
                 chunk_size=4194304, verify=False,
                 fail_fast=False, quiet=False) -> None:
        """
        Download the product matching the query given in arguments.

        :param query: (Expression) The filter to apply in the query
                       by default None
        :param query_order: (tuple[Expression, Expression]) to order
                             the result of the query
        :param limit: (int) Limit the number of result by default 10.
        :param skip: (int) Skip a number of matching product by default 0.
        :param output: (str) Path to a folder to put the downloaded product,
                       by default the running directory
        :param threads: (int) Number of threads running by default 2.
        :param chunk_size: (int) the size of chunk to be downloaded
                            by default 4194304
        :param verify: (bool) check at the end of download if the hash of
                       the downloaded product match the one of the service.
                       (by default False)
        :param fail_fast: (bool) stop all the download when an error append
                          (by default False)
        :param quiet: (bool) put the quit mode.
        :return: None
        """

        request = self.__odata_service[
            ODataQueryPredicate(
                filter=query,
                order=query_order
            )]

        if len(request) < limit:
            limit = len(request)

        products = [request[skip + x] for x in range(limit)]
        # To download ?
        dm = Download(
            output_folder=output, threads=threads,
            chunk_size=chunk_size, verify=verify,
            fail_fast=fail_fast, quiet=quiet)

        for prod in products:
            dm.submit(prod)

        dm.join()
