#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#

import random

from opentelemetry import trace
from opentelemetry.trace import Tracer
from opentelemetry.trace.span import Span, SpanContext, NonRecordingSpan

# from mesh.environ import System
from mesh.telemetry.telemetry import MeshTelemetry

mot = MeshTelemetry()


def init():
    """ init function """
    pass


def provider_tracer(tracer_name: str = '', print_std: bool = False) -> "Tracer":
    """
    :param tracer_name: app name may be better
    :param print_std: True: print metrics data on stdout; False: ignore
    :return: Tracer, used as below,
    for example:
    with tracer.start_as_current_span("asm.init"):
        pass
    """

    __tracer__ = mot.get_tracer(enable_std=print_std)
    if __tracer__:
        if tracer_name != '':
            return __tracer__.get_tracer(tracer_name)
        else:
            return __tracer__.get_tracer('gaia-tracer')
    else:
        print('open telemetry not active!')
        # raise Exception('open telemetry not active!')


def get_current_span() -> Span:
    return trace.get_current_span()


tracer = provider_tracer(print_std=True)


def if_rebuild_span(attachments: dict) -> bool:
    # tracer may be not active
    if not tracer:
        return False
    return True


def build_via_remote(attachments: dict, name: str):
    """
    enable only for if_rebuild_span return True
    :param name:
    :param attachments: mesh context
    :return: telemetry Span
    """
    trace_id = random.getrandbits(128)
    span_id = random.getrandbits(64)
    if 'mesh-telemetry-trace-id' in attachments:
        trace_id = int(attachments['mesh-telemetry-trace-id'], 16)
    span_context = SpanContext(trace_id=trace_id, span_id=span_id, is_remote=True)
    ctx = trace.set_span_in_context(NonRecordingSpan(span_context))
    return tracer.start_as_current_span(name=name, context=ctx)
