#
# Copyright (C) 2015 - 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# Ref. python -c "import msgpack; help(msgpack.Unpacker); help(msgpack.Packer)"
#
r"""MessagePack backend:

- Format to support: MessagePack, http://msgpack.org
- Requirements: msgpack-python, https://pypi.python.org/pypi/msgpack/
- Development Status :: 4 - Beta
- Limitations: None obvious
- Special options:

  - All options of msgpack.load{s,} and msgpack.dump{s,} except object_hook
    and file_like should work.

  - See also: https://pypi.python.org/pypi/msgpack/

Changelog:

    .. versionadded:: 0.0.11
"""
import typing

import msgpack

import anyconfig.backend.base


class Parser(anyconfig.backend.base.StringStreamFnParser,
             anyconfig.backend.base.BinaryLoaderMixin,
             anyconfig.backend.base.BinaryDumperMixin):
    """
    Loader/Dumper for MessagePack files.
    """
    _type: [str] = 'msgpack'
    _extensions: typing.List[str] = []
    _load_opts: typing.List[str] = [
        'read_size', 'use_list', 'object_hook', 'list_hook',
        'encoding', 'unicode_errors', 'max_buffer_size', 'ext_hook',
        'max_str_len', 'max_bin_len', 'max_array_len', 'max_map_len',
        'max_ext_len', 'object_pairs_hook'
    ]
    _dump_opts: typing.List[str] = [
        'default', 'encoding', 'unicode_errors', 'use_single_float',
        'autoreset', 'use_bin_type'
    ]
    # Exclusive with object_hook
    _dict_opts: typing.List[str] = ['object_pairs_hook']

    _load_from_string_fn = anyconfig.backend.base.to_method(msgpack.unpackb)
    _load_from_stream_fn = anyconfig.backend.base.to_method(msgpack.unpack)
    _dump_to_string_fn = anyconfig.backend.base.to_method(msgpack.packb)
    _dump_to_stream_fn = anyconfig.backend.base.to_method(msgpack.pack)

# vim:sw=4:ts=4:et:
