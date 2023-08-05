"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright 2020 Alibaba Group Holding Limited. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import graphscope.proto.attr_value_pb2
import graphscope.proto.error_codes_pb2
import graphscope.proto.graph_def_pb2
import graphscope.proto.types_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class OpDef(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class AttrEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.int
        @property
        def value(self) -> graphscope.proto.attr_value_pb2.AttrValue: ...
        def __init__(
            self,
            *,
            key: builtins.int = ...,
            value: graphscope.proto.attr_value_pb2.AttrValue | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    KEY_FIELD_NUMBER: builtins.int
    OP_FIELD_NUMBER: builtins.int
    PARENTS_FIELD_NUMBER: builtins.int
    OUTPUT_TYPE_FIELD_NUMBER: builtins.int
    ATTR_FIELD_NUMBER: builtins.int
    LARGE_ATTR_FIELD_NUMBER: builtins.int
    QUERY_ARGS_FIELD_NUMBER: builtins.int
    key: builtins.str
    """Unique key for every OpDef. Usually generated by analytical engine."""
    op: graphscope.proto.types_pb2.OperationType.ValueType
    """The operation name. There may be custom parameters in attrs."""
    @property
    def parents(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Used for store an op's parents, i.e. use which op to produce this op."""
    output_type: graphscope.proto.types_pb2.OutputType.ValueType
    """Different types of op may create different output."""
    @property
    def attr(self) -> google.protobuf.internal.containers.MessageMap[builtins.int, graphscope.proto.attr_value_pb2.AttrValue]:
        """Operation-specific configuration."""
    @property
    def large_attr(self) -> graphscope.proto.attr_value_pb2.LargeAttrValue:
        """Operation-specific configuration for large chunk.
        e.g. dataframe or numpy data
        """
    @property
    def query_args(self) -> graphscope.proto.types_pb2.QueryArgs:
        """arguments that served as application querying parameters.
        Such as source vertex id for SSSP.
        """
    def __init__(
        self,
        *,
        key: builtins.str = ...,
        op: graphscope.proto.types_pb2.OperationType.ValueType = ...,
        parents: collections.abc.Iterable[builtins.str] | None = ...,
        output_type: graphscope.proto.types_pb2.OutputType.ValueType = ...,
        attr: collections.abc.Mapping[builtins.int, graphscope.proto.attr_value_pb2.AttrValue] | None = ...,
        large_attr: graphscope.proto.attr_value_pb2.LargeAttrValue | None = ...,
        query_args: graphscope.proto.types_pb2.QueryArgs | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["large_attr", b"large_attr", "query_args", b"query_args"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["attr", b"attr", "key", b"key", "large_attr", b"large_attr", "op", b"op", "output_type", b"output_type", "parents", b"parents", "query_args", b"query_args"]) -> None: ...

global___OpDef = OpDef

@typing_extensions.final
class OpResult(google.protobuf.message.Message):
    """Result of Op"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class Meta(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        METRICS_FIELD_NUMBER: builtins.int
        HAS_LARGE_RESULT_FIELD_NUMBER: builtins.int
        metrics: builtins.str
        """if success, store the metrics. (e.g. how many seconds used, memory bytes...)"""
        has_large_result: builtins.bool
        """result represents raw bytes if:
         1) NDArray or DataFrame
         2) Gremlin result
         3) Graph report information of Networkx
        """
        def __init__(
            self,
            *,
            metrics: builtins.str = ...,
            has_large_result: builtins.bool = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["has_large_result", b"has_large_result", "metrics", b"metrics"]) -> None: ...

    CODE_FIELD_NUMBER: builtins.int
    KEY_FIELD_NUMBER: builtins.int
    META_FIELD_NUMBER: builtins.int
    RESULT_FIELD_NUMBER: builtins.int
    ERROR_MSG_FIELD_NUMBER: builtins.int
    GRAPH_DEF_FIELD_NUMBER: builtins.int
    code: graphscope.proto.error_codes_pb2.Code.ValueType
    """Status code"""
    key: builtins.str
    """unique key for every op"""
    @property
    def meta(self) -> global___OpResult.Meta:
        """Meta"""
    result: builtins.bytes
    """result represents app_name or context_key or raw bytes If the op returns a NDArray or DataFrame"""
    error_msg: builtins.str
    @property
    def graph_def(self) -> graphscope.proto.graph_def_pb2.GraphDefPb: ...
    def __init__(
        self,
        *,
        code: graphscope.proto.error_codes_pb2.Code.ValueType = ...,
        key: builtins.str = ...,
        meta: global___OpResult.Meta | None = ...,
        result: builtins.bytes = ...,
        error_msg: builtins.str = ...,
        graph_def: graphscope.proto.graph_def_pb2.GraphDefPb | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["graph_def", b"graph_def", "meta", b"meta"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["code", b"code", "error_msg", b"error_msg", "graph_def", b"graph_def", "key", b"key", "meta", b"meta", "result", b"result"]) -> None: ...

global___OpResult = OpResult

@typing_extensions.final
class DagDef(google.protobuf.message.Message):
    """Consist by list of ops."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OP_FIELD_NUMBER: builtins.int
    @property
    def op(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___OpDef]: ...
    def __init__(
        self,
        *,
        op: collections.abc.Iterable[global___OpDef] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["op", b"op"]) -> None: ...

global___DagDef = DagDef
