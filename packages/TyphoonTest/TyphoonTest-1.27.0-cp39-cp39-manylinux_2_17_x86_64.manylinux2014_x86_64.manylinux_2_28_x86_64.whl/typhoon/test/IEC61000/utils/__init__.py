""" This package contains support functions for IEC61000 standard."""

import typhoon.test.IEC61000.utils.impl as _impl
import pandas
import numpy


def split_samples(samples, cycles_in_window=1):
    """
    [TA Comment] This documentation is internal
    According to the IEC 61000-4-30 standard, the length of the measured window depends on the grid frequency.

    Parameters
    ----------
    samples: pandas.DataFrame
        Signal from which to compute the window. If a DataFrame is provided, the first signal is used.

    cycles_in_window: float
        Defines the number of cycles in a measured window. It must be an integer multiple of 0.5.
        For example, use 0.5 for a half cycle or 1.0 for a full grid cycle.

    Returns
    --------
    split_window_position: numpy.array
        The first and last index of each measurement window.

    Raises
    ------
    TypeError: When the input data is different from ``pandas.Series`` or ``pandas.DataFrame``
    ValueError: When ``cycles_in_window`` is not multiple of 0.5

    Examples
    --------
    >>> from typhoon.test.signals import pandas_sine
    >>> from typhoon.test.IEC61000 import split_samples
    >>> samples = pandas_sine()
    >>> split_window_position = split_samples(samples, 12)

    See also
    --------
    typhoon.test.IEC61000.utils.select_window
    typhoon.test.IEC61000.utils.fundamental_component_measurement
    typhoon.test.IEC61000.flicker
    typhoon.test.IEC61000.rms
    typhoon.test.IEC61000.harmonic_content
    typhoon.test.IEC61000.power_quantities
    typhoon.test.IEC61000.power_quantities_three_phase
    typhoon.test.IEC61000.sym_comp_voltage_unbalance
    """
    return _impl.split_samples(samples, cycles_in_window)


def select_window(data, splits, window):
    """
    [TA Comment] This documentation is internal
    Selects a window of data based on the given splits and window.

    Parameters
    ----------
    data : pandas.DataFrame or pandas.Series
        The data to select a window from.

    splits : list
        The indices that split the data into windows.

    window : int or array-like of 2 ints
        The window to select, either a single int or a list of 2 ints. If a single int is given,
        the window will be centered on that index. If a list of 2 ints is given, the window will
        be selected between those two indices.

    Returns
    -------
    selected_data : pandas.DataFrame or pandas.Series
        The window of data selected based on the given splits and window.

    Raises
    ------
    TypeError: When the input data is different from ``pandas.Series`` or ``pandas.DataFrame``

    Examples
    --------
    >>> from typhoon.test.signals import pandas_sine
    >>> from typhoon.test.IEC61000.utils import split_samples, select_window
    >>> samples = pandas_sine()
    >>> idx = split_samples(samples, 12)
    >>> df_w = select_window(samples, idx, (2, 5))

    See also
    --------
    typhoon.test.IEC61000.utils.split_samples
    """
    return _impl.select_window(data, splits, window)


def fundamental_component_measurement(
    samples: pandas.DataFrame, nominal_grid_freq: float, reference_split=None
):
    """
    [TA Comment] This documentation is internal
    Computes the fundamental component of a sinusoidal signal and the frequency of the power grid.

    Parameters
    ----------
    samples : pandas.DataFrame
        A DataFrame containing the samples of the sinusoidal signal to be analyzed.

    nominal_grid_freq : float
        The nominal frequency of the power grid in Hz.

    reference_split : list, optional
        The index of the sample to be used as a reference for phase calculation in each window.

    Returns
    --------
    rms_comp: numpy.array
        The root-mean-square value of the fundamental component of the signal.
    phase_angle: numpy.array
        The phase angle of the fundamental component in radians.
    grid_frequency_each_window_Hz: numpy.array
        Array with the power grid frequencies in Hz for each window.

    Raises
    ------
    ValueError: When the ``nominal_grid_freq`` is different from 50 Hz or 60 Hz

    Examples
    --------
    >>> from typhoon.test.signals import pandas_sine
    >>> from typhoon.test.IEC61000.utils import fundamental_component_measurement
    >>> grid_freq = 60
    >>> samples = pandas_sine(frequency=grid_freq)
    >>> rms_comp, phase_angle, grid_frequency_each_window_Hz = fundamental_component_measurement(samples, grid_freq)

    See also
    --------
    typhoon.test.IEC61000.power_quantities
    typhoon.test.IEC61000.power_quantities_three_phase
    """
    return _impl.fundamental_component_measurement(
        samples, nominal_grid_freq, reference_split
    )


def map_rms(split_samples_columns: pandas.DataFrame):
    """[TA Comment] This function will be removed from here, don't need documenation"""
    return _impl.map_rms(split_samples_columns)


def calc_rms_phasor_from_waveform(
    amplitude_VorA: numpy.array, reference_angle_rad: numpy.array
):
    """
    [TA Comment] This documentation is internal
    Calculate the complex phasor given the amplitude (Volts) and reference angle (rad).

    Parameters
    ----------
    amplitude_VorA: numpy.array
        Phasor amplitude in volts.

    reference_angle_rad : numpy.array
        Phasor angle in radians.

    Returns
    -------
    phasor: numpy.array
        Complex float number of the RMS value.

    Examples
    --------
    >>> import numpy as np
    >>> from typhoon.test.IEC61000.utils import calc_rms_phasor_from_waveform
    >>> rms_fundamental_voltage = np.array(350.692)
    >>> phase_angle_v_rad = np.array(-0.955)
    >>> phasor = calc_rms_phasor_from_waveform(rms_fundamental_voltage, phase_angle_v_rad)

    See also
    --------
    typhoon.test.IEC61000.power_quantities_three_phase
    """
    return _impl.calc_rms_phasor_from_waveform(amplitude_VorA, reference_angle_rad)


def calc_zero_pos_neg_seq_from_abc_phasor(Vabc_phasor_vector: numpy.array):
    """
    [TA Comment] This documentation is internal
    Calculate the Zero, Positive and Negative phasors given the ABC phasors.

    Parameters
    ----------
    Vabc_phasor_vector: numpy.array
        Vector of ABC phasors with amplitude in volts and angle in radians.

    Returns
    -------
    Vzpn_phasor_vector: numpy.array
        Complex vector with Zero, Positive, Negative sequence phasors.

    Examples
    --------
    >>> import numpy as np
    >>> from typhoon.test.IEC61000.utils import calc_zero_pos_neg_seq_from_abc_phasor
    >>> rms_fundamental_voltage = np.array(380) # Zero sequence only
    >>> phase_angle_v_rad = np.array(0.0)
    >>> calc_zero_pos_neg_seq_from_abc_phasor([[rms_fundamental_voltage,phase_angle_v_rad],
    >>>                                        [rms_fundamental_voltage,phase_angle_v_rad],
    >>>                                        [rms_fundamental_voltage,phase_angle_v_rad]])

    See also
    --------
    typhoon.test.IEC61000.power_quantities_three_phase
    typhoon.test.IEC61000.sym_comp_voltage_unbalance

    """
    return _impl.calc_zero_pos_neg_seq_from_abc_phasor(Vabc_phasor_vector)
