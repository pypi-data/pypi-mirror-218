"""
CLI command for "traces" command
"""
import logging

import click

from samcli.cli.cli_config_file import TomlProvider, configuration_option
from samcli.cli.main import aws_creds_options, pass_context, print_cmdline_args
from samcli.cli.main import common_options as cli_framework_options
from samcli.commands._utils.command_exception_handler import command_exception_handler
from samcli.commands._utils.options import common_observability_options
from samcli.lib.observability.util import OutputOption
from samcli.lib.telemetry.metric import track_command
from samcli.lib.utils.version_checker import check_newer_version

LOG = logging.getLogger(__name__)

HELP_TEXT = """
Use this command to fetch AWS X-Ray traces generated by your stack.\n
\b
Run the following command to fetch X-Ray traces by ID.
$ sam traces --trace-id tracing-id-1 --trace-id tracing-id-2
\b
Run the following command to tail X-Ray traces as they become available.
$ sam traces --tail
"""


@click.command("traces", help=HELP_TEXT, short_help="Fetch AWS X-Ray traces")
@configuration_option(provider=TomlProvider(section="parameters"))
@click.option(
    "--trace-id",
    "-ti",
    multiple=True,
    help="Fetch specific trace by providing its id",
)
@common_observability_options
@cli_framework_options
@aws_creds_options
@pass_context
@track_command
@check_newer_version
@print_cmdline_args
@command_exception_handler
def cli(
    ctx,
    trace_id,
    start_time,
    end_time,
    tail,
    output,
    config_file,
    config_env,
):
    """
    `sam traces` command entry point
    """
    do_cli(trace_id, start_time, end_time, tail, output, ctx.region)


def do_cli(trace_ids, start_time, end_time, tailing, output, region):
    """
    Implementation of the ``cli`` method
    """
    from datetime import datetime

    import boto3

    from samcli.commands.logs.logs_context import parse_time
    from samcli.commands.traces.traces_puller_factory import generate_trace_puller
    from samcli.lib.utils.boto_utils import get_boto_config_with_user_agent

    sanitized_start_time = parse_time(start_time, "start-time")
    sanitized_end_time = parse_time(end_time, "end-time") or datetime.utcnow()

    boto_config = get_boto_config_with_user_agent(region_name=region)
    xray_client = boto3.client("xray", config=boto_config)

    # generate puller depending on the parameters
    puller = generate_trace_puller(xray_client, OutputOption(output) if output else OutputOption.text)

    if trace_ids:
        puller.load_events(trace_ids)
    elif tailing:
        puller.tail(sanitized_start_time)
    else:
        puller.load_time_period(sanitized_start_time, sanitized_end_time)
