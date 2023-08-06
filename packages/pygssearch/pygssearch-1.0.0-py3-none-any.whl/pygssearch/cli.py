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

import click
from drb.drivers.http import HTTPOAuth2
from requests.auth import HTTPBasicAuth

from pygssearch import _version, query_builder, OdataSource
from pygssearch.progress.progress import TqdmLoggingHandler
from pygssearch.utility import init_conf

logger = logging.getLogger('pygssearch')
logger.setLevel(logging.INFO)
logger.addHandler(TqdmLoggingHandler())


@click.command(help=f"""
This library PyGSSearch aims to support query and download product
from the GSS catalogue, the download can be start
with command line and also in python script. It authorize limiting
the connections to respect the services quota policies.
""")
@click.option('--service', '-s', type=str, default=None,
              envvar="GSS_SERVICE",
              help='Service to requests data')
@click.option('--filters', '-f', type=str,
              help="Filter to be applied to requests "
                   "products to be searched.")
@click.option('--username', '-u', type=str, default=None,
              envvar="GSS_USERNAME",
              help="Service connection username.")
@click.option('--password', '-p', type=str, default=None,
              envvar="GSS_PASSWORD",
              help="Service connection password.")
@click.option('--token_url', type=str, default=None,
              help="Url to retrieve the token.")
@click.option('--client_id', type=str, default=None,
              help="The client identifier.")
@click.option('--client_secret', type=str, default=None,
              help="The client secret.")
@click.option('--thread_number', '-t', type=int, default=2,
              help="Number of parallel download threads (default:2).")
@click.option('--limit', '-l', type=int,
              help="Limit the number matching products (default: 10)",
              default=10)
@click.option('--skip', type=int,
              help="Skip a number matching products (default: 0)",
              default=0)
@click.option('--output', '-o', type=str, default=".",
              help='The directory to store the downloaded files.')
@click.option('--chunk_size', '-c', type=int, default=4194304,
              help="The size of downloaded chunks "
                   "(default: 4194304 Bytes).")
@click.option('--start', '-S', type=str,
              help="start date of the query in  the format "
                   "YYYY-MM-DD or an expression like NOW-1DAY.")
@click.option('--end', '-E', type=str,
              help="End date of the query")
@click.option('--geometry', '-g', multiple=True,
              help="Path to a GeoJson file containing a search area or"
                   "a series of entries of tuple of coordinates "
                   "separated by a coma")
@click.option('--uuid', type=str, multiple=True,
              help="Select a specific product UUID. "
                   "Can be set more than once.")
@click.option('--name', '-n', type=str, multiple=True,
              help="Select specific product(s) by filename. "
                   "Can be set more than once.")
@click.option('--mission', '-m',
              type=click.Choice(["1", "2", "3", "5"]),
              help="Limit search to a Sentinel satellite (constellation).")
@click.option('--instrument', '-I',
              help="Limit search to a specific instrument "
                   "on a Sentinel satellite.")
@click.option('--product_type', '-P', type=str,
              help="Limit search to a Sentinel product type.")
@click.option('--cloud', type=int,
              help="Maximum cloud cover (in percent).")
@click.option('--download', '-d', is_flag=True,
              help="Download all the results of the query.")
@click.option('--fail_fast', is_flag=True,
              help="Skip all other other downloads if one fails.")
@click.option('--order_by', '-O', type=str,
              help="Specify the keyword to order the result."
                   "Prefix ‘-’ for descending order.")
@click.option('--verify', '-v', is_flag=True,
              help="Check the file integrity using his hash"
                   ", use with the download option.")
@click.option('--config', '-C', type=str, default=None,
              help="Give the path to a configuration file to the .ini format")
@click.option('--quiet', '-q', is_flag=True,
              help="Silent mode: only errors are reported,"
                   "use with the download option.")
@click.option('--version', is_flag=True,
              help="Show version number and exit.")
@click.option('--format', '-F', multiple=True, default=('Name', 'Id'),
              help="Define the response of the query by default show "
                   "the name and id, of each matching product of the query. "
                   "To show all information put _")
@click.option('--logs', is_flag=True,
              help="Print debug log message and no progress bar,"
                   "use with the download option.")
@click.option('--debug', is_flag=True,
              help="Print debug log message.")
def cli(service, filters, username, password, token_url,
        client_id, client_secret, thread_number, limit, skip,
        output, chunk_size, start, end, geometry, uuid, name, mission,
        instrument, product_type, cloud, download, fail_fast, order_by, verify,
        config, quiet, version, format, logs, debug):
    auth = None

    if debug:
        logger.setLevel(logging.DEBUG)
    elif logs:
        logger.setLevel(logging.DEBUG)
        quiet = True
    elif quiet:
        logger.setLevel(logging.WARNING)

    if version:
        logger.info(f"PyGSSearch python library"
                    f"{_version.get_versions()['version']}")
        return

    service, auth = init_conf(
        service, username, password, token_url,
        client_id, client_secret, config)

    if isinstance(auth, HTTPBasicAuth):
        logger.debug("Establish connection to the service "
                     "using basic authentication")
    elif isinstance(auth, HTTPOAuth2):
        logger.debug("Establish connection to the service "
                     "using OAuth2 authentication")
    elif auth is None:
        logger.debug("Establish connection to the service "
                     "without authentication")

    # Prepare filter
    query, query_order = query_builder(
        filters, (start, end), geometry, uuid, name, mission,
        instrument, product_type, cloud, order_by)

    # Connect to the service
    source = OdataSource(service=service, auth=auth)

    # To download ?
    if download:
        source.download(query=query, query_order=query_order,
                        limit=limit, skip=skip,
                        threads=thread_number,
                        chunk_size=chunk_size, verify=verify,
                        fail_fast=fail_fast,
                        output=output, quiet=quiet)

    else:
        # Query filter
        request = source.request(query, query_order, limit, skip, format)

        logger.setLevel(logging.INFO)
        logger.info(request)


if __name__ == '__main__':
    cli()
