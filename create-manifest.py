"""create-manifest.py

Create `Manifest` file to be used by pxmcli to create a render.

Usage: create-manifest.py [OPTIONS] [SOURCES]

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

import re
import json
import click
import datetime


# Custom click input types
class CustomType():
    class BdxParamType(click.ParamType):
        """Band Index Type
        """
        name = 'str'

        def convert(self, value, param, ctx):
            try:
                bands = [int(x) for x in value.split(',')]
                assert len(bands) in (3, 4)
                assert all(b > 0 for b in bands)
                return value
            except (AttributeError, AssertionError):
                raise click.ClickException('bidx must be a string with 3 or 4 ints comma-separated, '
                                           'representing the band indexes for R,G,B(,A)')

    class TilesetParamType(click.ParamType):
        """Tileset Type
        The tileset must be in a form of "{account}.{id}" with a maximum of 32 chars for each.
        """
        name = 'str'

        def convert(self, value, param, ctx):
            try:
                assert re.match(r"^[a-z0-9-_]{1,32}\.[a-z0-9-_]{1,32}$", value)
                return value
            except (AssertionError):
                raise click.ClickException('layers must follow the {account}.{id} naming (each with 32 chars max)')

    class DateParamType(click.ParamType):
        """Date Type
        The date must be in a form of "YYYY" or "YYYY-MM-DD".
        """
        name = 'str'

        def convert(self, value, param, ctx):
            try:
                assert re.fullmatch('^[0-9]{4}|[0-9]{4}-[0-9]{2}-[0-9]{2}$', value)

                if re.fullmatch('^[0-9]{4}$', value):
                    assert datetime.datetime.strptime(value, '%Y')

                if re.fullmatch('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', value):
                    assert datetime.datetime.strptime(value, '%Y-%m-%d')

                return value
            except (AssertionError, ValueError):
                raise click.ClickException('date must be in either {YYYY} or {YYYY-MM-DD} format')

    class NdvParamType(click.ParamType):
        """No Data Value
        The ndv input must be in a form of "[0,0,0]".
        """
        name = 'str'

        def convert(self, value, param, ctx):
            try:
                ndv = json.loads(value)
                assert len(ndv) == 3
                assert all(isinstance(v, int) for v in ndv)
                return value
            except (AttributeError, TypeError):
                raise click.ClickException('layers must follow the {account}.{id} naming (each with 32 chars max)')

    class CRSParamType(click.ParamType):
        """Coordinate System
        The CRS input must start with "EPSG"
        """
        name = 'str'

        def convert(self, value, param, ctx):
            try:
                assert value.startswith('EPSG:')
                return value
            except (AssertionError):
                raise click.ClickException('crs string must start with EPSG')

    class MbxAccountParamType(click.ParamType):
        """Mapbox Account
        A Mapbox account cannot have spaces
        """
        name = 'str'

        def convert(self, value, param, ctx):
            try:
                assert re.match(r"^[a-z0-9-_]{1,32}$", value)
                return value
            except (AssertionError):
                raise click.ClickException('Mapbox account name must have 32 () chars max and no blank space')

    bdx = BdxParamType()
    tileset = TilesetParamType()
    date = DateParamType()
    ndv = BdxParamType()
    crs = CRSParamType()
    account = MbxAccountParamType()


@click.command()
@click.argument('sources', default='-', type=click.File('r'))
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
def create_manifest(sources, tileset, license, account, product, date, notes,
                    bidx, crs, color, ndv, output):
    """Create a PXM manifest file
    """

    sources = list([x.strip() for x in sources])
    for source in sources:
        assert source.startswith('s3')
        assert '-' not in source.split('/')[-1]

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
        'info': info
    })

    if output:
        with open(output, mode='w') as f:
            f.write(manifest)
    else:
        click.echo(manifest)


if __name__ == "__main__":
    create_manifest()
