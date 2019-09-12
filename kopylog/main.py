#!/usr/bin/env python
#  Authors: Sylvain Marie <sylvain.marie@se.com>
#
#  Copyright (c) Schneider Electric Industries, 2019. All right reserved.

from datetime import datetime
from logging import Logger

from kopylog.utils_bags import OrderedMunch

try:  # python 3.5+
    from typing import Dict, Any, TypeVar, Mapping, Tuple, MutableMapping, Type
    PhaseInfoType = TypeVar('PhaseInfoType', bound='PhaseInfo')
    ExecInfoType = TypeVar('ExecInfoType', bound='Kompanion')
except ImportError:
    pass


from kopylog.utils_tables import TypedTable


class InvalidStartStopCommandError(Exception):
    """
    Raised whenever a start() or stop() command is applied on a ``PhaseInfo`` without the 'force' attribute, and
    the phase happens to be already started/stopped.
    """
    def __init__(self,
                 phase_info,    # type: PhaseInfo
                 is_start=True  # type: bool
                 ):
        self.phase_info = phase_info
        self.is_start = is_start
        super(InvalidStartStopCommandError, self).__init__()

    def __str__(self):
        phase_id = self.phase_info.id
        action = "start" if self.is_start else "stop"
        return "Phase {id} was already stopped. Please use {action}(force=True) if you wish to cancel the first " \
               "{action} and {action} it again".format(id=phase_id, action=action)


class InvalidStartCommandError(InvalidStartStopCommandError):
    def __init__(self,
                 phase_info  # type: PhaseInfo
                 ):
        super(InvalidStartCommandError, self).__init__(phase_info=phase_info, is_start=True)


class InvalidStopCommandError(InvalidStartStopCommandError):
    def __init__(self,
                 phase_info  # type: PhaseInfo
                 ):
        super(InvalidStopCommandError, self).__init__(phase_info=phase_info, is_start=False)


_PHASE_ID_ATT_NAME = 'phase_id'


class PhaseInfo(OrderedMunch):
    """
    A structure to hold processing information for a given processing phase.

    It provides an object facade over an ordered dict, so you can easily add

    In addition it has
     - a phase id (implementation of DfDictEntry)
     - an optional logger
     - the ability to be started/stopped (this will log a message and insert start time / end time / elapsed time info)
     - the ability to be used as a context manager to automatically start/stop
    """

    __slots__ = _PHASE_ID_ATT_NAME, '_logger'

    def __init__(self,
                 phase_id,
                 logger=None,
                 start=True,
                 initial_dict=None,  # type: Mapping[str, Any]
                 **kwargs            # type: Any
                 ):
        """
        Constructor with a phase id. If start=True (default) the phase is started when created.

        :param phase_id:
        :param logger: an optional logger where to log the phase start and stop events
        :param start: optional boolean to start the phase
        """
        # super constructor
        super(PhaseInfo, self).__init__(initial_dict=initial_dict, **kwargs)

        # The phase id and logger are special fields
        self.set_attrs(**{_PHASE_ID_ATT_NAME: phase_id})
        self.set_attrs(_logger=logger)  # private so that it will not appear in string repr, equality tests, dict views...

        # Start the phase if requested
        if start:
            self.start()

    # ------- ContextManager implementation
    def __enter__(self):
        # type: (...) -> PhaseInfo
        """
        When entering this context, the phase is started if not already
        :return:
        """
        # start the timer
        if not self.is_started():
            self.start()

        # return the phase information as a bag
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # stop the timer
        self.stop()

    # ------- Entry > VarsViewMixIn implementation
    # @classmethod
    # def new_instance_from_vars(cls: 'Type[PhaseInfoType]', constructor_args: Mapping[str, Any], **kwargs) \
    #         -> 'PhaseInfoType':
    #     """ Override super method so that phase objects are not started automatically when restored from dict """
    #     phase_id = constructor_args.pop(PHASE_ID_ATT_NAME)
    #     return PhaseInfo(phase_id=phase_id, start=False, ordered_kwargs=constructor_args)

    # ------- Entry implementation
    # @classmethod
    # def id_fields(cls) -> Tuple[str, ...]:
    #     return PHASE_ID_ATT_NAME,

    # ------- Start/Stop goodies
    def start(self, force: bool = False):
        """
        Starts the phase by adding a 'start_time' field. By default starting an already started phase raises an error,
        but you can force it using force=True

        :param force: True to start the phase again even if it was already started. Past start information will be
            overridden
        :return:
        """
        if force or not self.is_started():
            # noinspection PyAttributeOutsideInit
            self.start_time = datetime.now()
            if self._logger is not None:
                self._logger.info("--------- Phase <{id}> started at: {time} ---------"
                                  "".format(id=self.get_id(), time=self.start_time))
        else:
            raise InvalidStartCommandError(self)

    def is_started(self):
        return hasattr(self, 'start_time')

    def stop(self, force: bool = False):
        """
        Stops the phase by adding an 'end_time' field as well as an 'elapsed_seconds' field.
        By default stopping an already stopped phase raises an error, but you can force it using force=True

        :param force: True to start the phase again even if it was already started. Past start information will be
            overridden
        :return:
        """
        if force or not self.is_stopped():
            # noinspection PyAttributeOutsideInit
            self.end_time = datetime.now()
            # noinspection PyAttributeOutsideInit
            self.elapsed_seconds = (self.end_time - self.start_time).total_seconds()
            if self._logger is not None:
                self._logger.info("--------- Phase <{id}> stopped at: {time}. Elapsed: {elapsed}s ---------"
                                 "".format(id=self.get_id(), time=self.end_time, elapsed=self.elapsed_seconds))
        else:
            raise InvalidStopCommandError(self)

    def is_stopped(self):
        return hasattr(self, 'end_time')

    # ------ MappingProxyMixIn implementation

    # def get_internal_mapping(self) -> MutableMapping[str, Any]:
    #     return self.odict

    # ------- method used by Kompanion to transform to a stacked dataframe rather than a pivoted one

    # @property
    # def contents(self) -> MaxiMunch:
    #     """
    #     Helper to return a MaxiMunch view of the phase contents.
    #
    #     :return:
    #     """
    #     return MaxiMunch(ordered_kwargs=self.odict)

    # ---------- JSONAble implementation

    # def to_jsonable_dict(self) -> Dict[Any, Any]:
    #     # # clone the internal dict
    #     # dct = copy(self.odict)
    #     # # don't forget to add the phase id  !
    #     # dct[PHASE_ID_ATT_NAME] = self.phase_id
    #     # dct.move_to_end(PHASE_ID_ATT_NAME, last=False)  # put it first
    #     # return dct
    #     return self.to_dict()
    #
    # @classmethod
    # def from_json_dict(cls: 'Type[PhaseInfoType]', dct: Dict,
    #                    json_schema_id: str, json_schema_version: VersionInfo) -> PhaseInfoType:
    #     if json_schema_version is None \
    #             or json_schema_version <= parse_version_info(cls.__json_schema_version__):
    #         # rely on our custom from_dict implementation
    #         return cls.from_dict(dct)
    #     else:
    #         raise SchemaVersionNotSupportedError(cls, dct, json_schema_version)


class Kompanion(object):
    """
    A structure to hold processing information as a collection of PhaseInfo.
    Phases are ordered by insertion order.
    """

    def __init__(self, ):
        self.phases = TypedTable(PhaseInfo, _PHASE_ID_ATT_NAME)

    def add_new_phase(self,
                      phase_id: str,
                      start: bool = True,
                      logger: Logger = None):
        """
        Utility method to create a new phase with the given id and return it

        :param phase_id:
        :param start: a boolean flag indicating if the new phase should be started. Default = True (to align with
            PhaseInfo constructor)
        :param logger:
        :return:
        """
        new_phase = PhaseInfo(phase_id, start=start, logger=logger)
        self.phases.append(new_phase)
        return new_phase

    def add_existing_phase(self,
                           phase: PhaseInfo,
                           stop: bool = True
                           ):
        """
        Utility method to add an existing phase. By default the phase is stopped when added, except if you set
        stop=False. Note that if the phase was not started or was already stopped, this does not try to stop it

        :param phase:
        :param stop:
        :return:
        """
        self.phases.append(phase)
        if stop and phase.is_started() and not phase.is_stopped():
            phase.stop()

    def add_existing_phases(self,
                            *phases,
                            stop: bool = True
                            ):
        """
        Utility method to add a bunch of existing phases. By default the phases are stopped when added, except if you
        set stop=False. Note that if a phase was not started or was already stopped, this does not try to stop it.

        :param phases:
        :param stop:
        :return:
        """
        for phase in phases:
            self.add_existing_phase(phase, stop=stop)

    # ---------- BuildableFromDf / ConvertibleToDf implementation

    # def to_df(self):
    #     """
    #     Returns the processing information as a dataframe
    #
    #     :return:
    #     """
    #     result_df = None
    #     for phase_id, phase in self.items():
    #         df = phase.contents.to_df(single_col=True).reset_index()
    #         df[PHASE_ID_ATT_NAME] = phase_id
    #         if result_df is None:
    #             result_df = df
    #         else:
    #             result_df = concat_with_size_check([result_df, df], axis=0)
    #
    #     if result_df is not None:
    #         # put the id first
    #         new_order = list(result_df.columns)[-1:] + list(result_df.columns)[:-1]
    #         return result_df[new_order]
    #     else:
    #         return pd.DataFrame.from_dict(data={PHASE_ID_ATT_NAME: [], PROPERTY: [], VALUE: []})
    #
    # @classmethod
    # def from_df(cls: 'Type[ExecInfoType]', df: pd.DataFrame, **kwargs) -> ExecInfoType:
    #     """
    #     Restores the processing information from a dataframe
    #
    #     :param df:
    #     :param kwargs:
    #     :return:
    #     """
    #     new_pi = Kompanion()
    #     for phase_id in df[PHASE_ID_ATT_NAME].unique():
    #         phase = new_pi.add_new_phase(phase_id, start=False)
    #         for row in df.loc[df[PHASE_ID_ATT_NAME] == phase_id].itertuples():
    #             phase[getattr(row, PROPERTY)] = getattr(row, VALUE)
    #
    #     return new_pi

    # ------------ AssertEqualsAble + equality implementation: we compare the to_df() views. Not needed anymore

    # def __eq__(self, other):
    #     """ relies on eq_pandas_ok on the df views """
    #     if isinstance(other, Kompanion):
    #         return eq_pandas_ok(self.to_df(), other.to_df())
    #     else:
    #         return super(Kompanion, self).__eq__(other)
    #
    # def assert_equal(self, other, verbose: bool = False):
    #     """ asserts that the two dataframe views are equal """
    #     if isinstance(other, Kompanion):
    #         assert_equals_pandas_ok(self.to_df(), other.to_df())
    #     else:
    #         return super(Kompanion, self).__eq__(other)

    # ---------- JSONAble implementation

    # def to_jsonable_dict(self) -> Dict[Any, Any]:
    #     # -- rely on autodict
    #     # return self
    #     # -- rely on DictViewMixIn
    #     # return self.to_dict()
    #     # -- rely on TypedTable
    #     return copy(self.odict)
    #
    # @classmethod
    # def from_json_dict(cls: 'Type[ExecInfoType]', dct: Dict,
    #                    json_schema_id: str, json_schema_version: VersionInfo) -> ExecInfoType:
    #     if json_schema_version is None \
    #             or json_schema_version <= parse_version_info(cls.__json_schema_version__):
    #         # -- rely on autodict
    #         # return cls.from_dict(dct)
    #         # -- rely on DictViewMixIn
    #         # return cls.from_dict(dct)
    #         # -- rely on TypedTable
    #         return cls.from_dict(dct)
    #     else:
    #         raise SchemaVersionNotSupportedError(cls, dct, json_schema_version)
