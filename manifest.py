"""create-manifest.py

Create `Manifest` file to be used by pxmcli to create a render.

Usage: manifest.py [OPTIONS] [SOURCES]

  Create a PXM manifest file

Options:
  -t, --tileset STR  Mapbox tileset id ({username}.{map})  [required]
  --license TEXT     License and usage restrictions  [required]
  --account STR      Valid mapbox account name  [required]
  --product TEXT     Product name  [required]
  --date STR         Images date  [required]
  --notes TEXT       Additional notes
  --bidx STR         Band index array
  --crs STR          Coordinate Reference System, EPSG:NNNN
  --color TEXT       rio color formulas
  --ndv STR          nodata value array
  --output STR       Output file name
  --help             Show this message and exit.

"""

from collections import Counter
import datetime
import json
import re

import click

version = "0.5.0"


# Custom click input types
class CustomType(object):

    class BdxParamType(click.ParamType):
        """Band Index Type"""

        name = 'str'

        def convert(self, value, param, ctx):
            try:
                bands = [int(x) for x in value.split(',')]
                if len(bands) in (3, 4):
                    if all(b > 0 for b in bands):
                        return bands
                    else:
                        raise click.ClickException('bands must be a '
                                                   'positive number')
                else:
                    raise click.ClickException('band array length '
                                               'can be 3 or 4')
            except (AttributeError):
                raise click.ClickException('bidx must be a string with 3 or 4 '
                                           'ints comma-separated, '
                                           'representing the band indexes '
                                           'for R,G,B(,A)')

    class TilesetParamType(click.ParamType):
        """Tileset Type

        The tileset must be in a form of "{account}.{id}" with a maximum
        of 32 chars for each.

        """
        name = 'str'

        def convert(self, value, param, ctx):
            if re.match(r"^[a-z0-9-_]{1,32}\.[a-z0-9-_]{1,32}$", value):
                return value
            else:
                raise click.ClickException('layers must follow the {account}.'
                                           '{id} naming (each with 32 chars '
                                           'max)')

    class DateParamType(click.ParamType):
        """Date Type
        The date must be in a form of "YYYY" or "YYYY-MM-DD".
        """
        name = 'str'

        def convert(self, value, param, ctx):
            err_msg = 'date must be in either {YYYY} or {YYYY-MM-DD} format'
            try:
                if not re.fullmatch('^[0-9]{4}|[0-9]{4}-[0-9]{2}-[0-9]{2}$',
                                    value):
                    raise click.ClickException(err_msg)

                if re.fullmatch('^[0-9]{4}$', value):
                    if not datetime.datetime.strptime(value, '%Y'):
                        raise click.ClickException(err_msg)

                if re.fullmatch('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', value):
                    if not datetime.datetime.strptime(value, '%Y-%m-%d'):
                        raise click.ClickException(err_msg)

                return value
            except (ValueError):
                raise click.ClickException(err_msg)

    class NdvParamType(click.ParamType):
        """No Data Value
        The ndv input must be in a form of "[0,0,0]".
        """
        name = 'str'

        def convert(self, value, param, ctx):
            try:
                ndv = [int(x) for x in value.split(',')]
                if not len(ndv) == 3:
                    raise click.ClickException('ndv must be 3 values')

                if not all(v > 0 for v in ndv):
                    raise click.ClickException('ndv must be greater than zero')
                return ndv
            except (AttributeError, TypeError):
                raise click.ClickException('ndv must be a string with ints '
                                           'comma-separated')

    class CRSParamType(click.ParamType):
        """Coordinate System
        The CRS input must start with "EPSG"
        """
        name = 'str'

        def convert(self, value, param, ctx):
            if not value.startswith('EPSG:'):
                raise click.ClickException('crs string must start with EPSG')
            return value

    class MbxAccountParamType(click.ParamType):
        """Mapbox Account
        A Mapbox account cannot have spaces
        """
        name = 'str'

        def convert(self, value, param, ctx):
            if not re.match(r"^[a-z0-9-_]{1,32}$", value):
                raise click.ClickException('Mapbox account name must have 32'
                                           '() chars max and no blank space')
            return value

    bdx = BdxParamType()
    tileset = TilesetParamType()
    date = DateParamType()
    ndv = NdvParamType()
    crs = CRSParamType()
    account = MbxAccountParamType()


def sources_callback(ctx, param, value):
    """Validate scheme and uniqueness of sources
    Notes
    -----
    The callback takes a fileobj, but then converts it to a sequence
    of strings.
    Returns
    -------
    list
    """
    sources = list([name.strip() for name in value])

    # Validate scheme.
    non_s3 = [name for name in sources if not name.startswith('s3://')]
    if len(non_s3) > 0:
        raise click.BadParameter("Sources {!r} do not have the required 's3' scheme.".format(non_s3))

    # Identify duplicate sources.
    dupes = [name for (name, count) in Counter(sources).items() if count > 1]
    if len(dupes) > 0:
        raise click.BadParameter("Duplicated sources {!r} cannot be processed.".format(dupes))

    return sources


@click.command()
@click.argument('sources', default='-', type=click.File('r'), callback=sources_callback)
@click.option('--tileset', '-t', type=CustomType.tileset, required=True,
              multiple=True, help='Mapbox tileset id ({username}.{map})')
@click.option('--license', type=str, required=True, help='License and usage restrictions')
@click.option('--account', type=CustomType.account, required=True, help='Valid mapbox account name')
@click.option('--product', type=str, required=True, help='Product name')
@click.option('--date', type=CustomType.date, required=True, help='Images date')
@click.option('--notes', type=str, default='', help='Additional notes')
@click.option('--bidx', type=CustomType.bdx, help="Band index array")
@click.option('--crs', type=CustomType.crs, help="Coordinate Reference System, EPSG:NNNN")
@click.option('--color', type=str, help="rio color formula")
@click.option('--ndv', type=CustomType.ndv, help="nodata value array")
@click.option('--output', '-o', type=click.Path(exists=False), help='Output file name')
@click.version_option(version=version)
def create_manifest(sources, tileset, license, account, product, date, notes,
                    bidx, crs, color, ndv, output):
    """Create a PXM manifest file
    """

    info = {
        'tilesets': tileset,  # list
        'license': license,
        'account': account,
        'product': product,
        'notes': notes,
        'date': date}

    if bidx:
        info['bidx'] = bidx

    if crs:
        info['crs'] = crs

    if color:
        info['color'] = {
            # color formula assumed to apply to all sources
            '.': color
        }

    if ndv:
        info['ndv'] = ndv

    manifest = json.dumps({
        'sources': sources,
        'info': info,
        'version': version
    }, sort_keys=True, indent=4, separators=(',', ': '))

    if output:
        with open(output, mode='w') as f:
            f.write(manifest)
    else:
        click.echo(manifest)


if __name__ == "__main__":
    create_manifest()

