#  Authors: Sylvain Marie <sylvain.marie@se.com>
#
#  Copyright (c) Schneider Electric Industries, 2019. All right reserved.

from kopylog import Kompanion, PhaseInfo


def test_main():
    """"""

    def main(foo):
        pi = Kompanion()

        with pi.add_new_phase('first') as phase:
            phase.useless1 = 'hello'
            print("Hello !")
            bar = foo + 1

        with pi.add_new_phase('second') as phase:
            phase.useless2 = 2
            print("World !")
            result = foo - bar

        return result, pi

    # now execute
    result, pi = main(10)

    # TODO
    # - assert that stdout worked correctly


def test_processing_information():
    """ """

    pi = Kompanion()

    first_phase = pi.add_new_phase('first', start=False)
    first_phase.hello = 'world'
    first_phase.basic_nb = 2.0

    # assert that order is preserved even in str representation
    assert str(first_phase) == "PhaseInfo<first> - {'hello': 'world', 'basic_nb': 2.0}"

    # dict
    f = first_phase.to_dict()
    from_to_dict = PhaseInfo.from_dict(f)

    # str
    assert str(first_phase) == str(from_to_dict)

    # eq and assert
    first_phase.assert_equal(from_to_dict)
    assert first_phase == from_to_dict

    # df
    f = first_phase.to_df()
    from_to_df = PhaseInfo.from_df(f)

    # str
    assert str(first_phase) == str(from_to_df)

    # eq and assert
    first_phase.assert_equal(from_to_df)
    assert first_phase == from_to_df

    # adding another phase but creating the phase object first this time
    second_phase = PhaseInfo('second', start=False)
    second_phase.yodeling = True
    second_phase.foo = 'bar'
    pi.add_existing_phase(second_phase, stop=False)

    # str repr
    assert str(pi) == "Kompanion - [" + str(first_phase) + ", " + str(second_phase) + "]"

    # dict
    f = pi.to_dict()
    pi_from_to_dict = Kompanion.from_dict(f)

    # str
    assert str(pi) == str(pi_from_to_dict)

    # equality / asserts
    pi.assert_equal(pi_from_to_dict, verbose=True)
    assert pi == pi_from_to_dict

    # df
    d = pi.to_df()
    pi_from_to_df = Kompanion.from_df(d)

    # equality / asserts
    pi.assert_equal(pi_from_to_df, verbose=True)
    assert pi == pi_from_to_df


def test_phase_context_manager():
    """ """
    with PhaseInfo('test') as test_phase:
        print('nothing, really')

    assert test_phase.is_stopped()


def test_dump_phase_info_containing_dataframe():
    """ """
    import pandas as pd
    pi = Kompanion()
    with pi.add_new_phase('phase') as phase:
        phase.df = pd.DataFrame()
        # this was the bug
        str(phase)
