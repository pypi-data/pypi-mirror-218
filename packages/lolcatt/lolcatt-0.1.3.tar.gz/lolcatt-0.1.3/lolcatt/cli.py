#!/usr/bin/env python3
import click

from lolcatt.app import LolCatt
from lolcatt.utils.utils import scan as do_scan


@click.command(
    'lolcatt',
    context_settings=dict(help_option_names=['-h', '--help']),
)
@click.argument(
    'url_or_path',
    nargs=1,
    default=None,
    required=False,
)
@click.option(
    '-d',
    '--device',
    default='default',
    help='Device name or alias (defined in catt config) to cast to. '
    'Per default, uses the device noted as default in the `catt` config file. '
    'If no default is set, the first device found will be used.',
)
@click.option(
    '--scan',
    is_flag=True,
    default=False,
    help='Scan for Chromecast devices and exit, printing found devices.',
)
def main(url_or_path, device, scan):
    """Cast media from a local file or URL to a Chromecast device."""
    if url_or_path is None and scan:
        do_scan()
        return

    lolcatt = LolCatt(device_name=device)
    if url_or_path is not None:
        lolcatt.caster.cast(url_or_path)
    lolcatt.run()


if __name__ == '__main__':
    main()
