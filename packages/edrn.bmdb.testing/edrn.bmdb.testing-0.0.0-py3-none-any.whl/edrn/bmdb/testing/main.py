# encoding: utf-8

from . import PACKAGE_NAME
from rdflib.compare import IsomorphicGraph
import logging, os, getpass, importlib.resources, argparse, sys

_logger = logging.getLogger(__name__)
_default_url = 'https://bmdb-dev.jpl.nasa.gov/rdf/'


def _check(url: str, kind: str, token: str) -> bool:
    '''Check the RDF of the given ``kind`` and give True if it matches the expected statements
    and False otherwise. Use the given ``token`` to access the full set of RDF from the server
    at ``url``. If not given, then 
    '''
    running, expected = IsomorphicGraph(), IsomorphicGraph()

    if not url.endswith('/'): url += '/'
    url = url + kind + '?' + 'all='
    _logger.debug('Retrieving server RDF from %s (token hidden)', url)
    url += token
    running.parse(url)

    _logger.debug('Reading expected RDF for %s', kind)
    with importlib.resources.open_binary(f'{PACKAGE_NAME}.data', f'{kind}.rdf') as io:
        expected.parse(io, format='xml')

    _logger.debug('Comparing RDF for %s…', kind)
    rc = running == expected
    _logger.debug('Are they equal = %r', rc)
    return rc


def main():
    parser = argparse.ArgumentParser(
        prog='bmdbtest', description='Test RDF from the Biomarker Database against known good descriptions'
    )
    parser.add_argument('-u', '--url', default=_default_url, help='URL of the BMDB to test (default: %(default)s)')
    parser.add_argument(
        '-t', '--token', help='Token for accessing the full BMDB RDF; defaults to BMDB_TOKEN env var, or prompts if unset'
    )
    logging_group = parser.add_mutually_exclusive_group()
    logging_group.add_argument(
        '-v', '--verbose', action='store_const', const=logging.DEBUG, dest='loglevel', default=logging.INFO,
        help='Enable copious debug logging'
    )
    logging_group.add_argument(
        '-q', '--quiet', action='store_const', const=logging.WARNING, dest='loglevel', help='Log only errors'
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    token = args.token if args.token else os.getenv('BMDB_TOKEN')
    if not token:
        getpass.getpass('No BMDB token specified; enter it now, please: ')

    problems = []
    for kind in ('biomarker-organs', 'biomarkers', 'publications', 'resources'):
        if not _check(args.url, kind, token):
            _logger.critical(f"RDF from {args.url} does not match expected morphology for {kind}")
            problems.append(kind)

    if len(problems) > 0:
        raise ValueError(f'Problems detected in RDF for: {", ".join(problems)}')
    else:
        _logger.info('No problems detected')
        sys.exit(0)


if __name__ == '__main__':
    main()
