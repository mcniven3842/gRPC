# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: showtime.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eshowtime.proto\"\x14\n\x04\x44\x61te\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\"\"\n\x0fShowtimeMovieId\x12\x0f\n\x07movieid\x18\x01 \x01(\t\")\n\tTimesData\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\x12\x0e\n\x06movies\x18\x02 \x03(\t\"\x0b\n\tEmptyDate2f\n\x08Showtime\x12.\n\x0fGetMoviesByDate\x12\x05.Date\x1a\x10.ShowtimeMovieId\"\x00\x30\x01\x12*\n\x0cGetListTimes\x12\n.EmptyDate\x1a\n.TimesData\"\x00\x30\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'showtime_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _DATE._serialized_start=18
  _DATE._serialized_end=38
  _SHOWTIMEMOVIEID._serialized_start=40
  _SHOWTIMEMOVIEID._serialized_end=74
  _TIMESDATA._serialized_start=76
  _TIMESDATA._serialized_end=117
  _EMPTYDATE._serialized_start=119
  _EMPTYDATE._serialized_end=130
  _SHOWTIME._serialized_start=132
  _SHOWTIME._serialized_end=234
# @@protoc_insertion_point(module_scope)
