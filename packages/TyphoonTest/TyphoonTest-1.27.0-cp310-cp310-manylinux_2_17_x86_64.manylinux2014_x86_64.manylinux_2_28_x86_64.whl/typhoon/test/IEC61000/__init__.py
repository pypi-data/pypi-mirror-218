""" This package contains measurement functions according to the IEC 61000 standard.

    Note
    ----
    This library is a **beta** version and will be updated in future releases.
"""

import typhoon.test.IEC61000.impl as _impl
import pandas
import pandas as pd
from typing import Union


def rms(
    samples: Union[pandas.DataFrame, pandas.Series],
    nominal_grid_freq: float,
    reference_split: list = None,
):
    """
    Measures the root-mean-square (RMS) value for input samples according to the IEC 61000-4-30 standard.

    Parameters
    ----------
    samples: pandas.DataFrame or pandas.Series
        Samples from the signals in which RMS values should be measured, organized in columns.

    nominal_grid_freq: float
        This method is applied only to grids with a nominal frequency of 50.0 Hz or 60.0 Hz in accordance with the
        IEC 61000-4-30 standard.

    reference_split: list
        Optional and None by default. List of the indices to split the sample in windows. If ``None``, the samples
        will be split according to the zero-crossings of the voltage signal.

    Returns
    -------
    rms_values: pandas.DataFrame
        The RMS values for each signal.

    Raises
    ------
    ValueError: When the ``nominal_grid_freq`` is different from 50 Hz or 60 Hz

    Examples
    --------
    >>> from typhoon.test.signals import pandas_sine
    >>> from typhoon.test.IEC61000 import rms
    >>> grid_freq = 60
    >>> signal = pandas_sine(frequency=grid_freq)
    >>> rms_signal = rms(signal, grid_freq)

    See also
    --------
    typhoon.test.IEC61000.flicker
    typhoon.test.IEC61000.harmonic_content
    typhoon.test.IEC61000.frequency
    """
    return _impl.rms(samples, nominal_grid_freq, reference_split)


def frequency(samples: pandas.DataFrame):
    """
    This method calculates the frequency of the grid voltage. The frequency reading is obtained every 10 seconds in
    accordance with IEC 61000-4-30. This method is applied only to grids with a nominal frequency of 50.0 Hz or 60.0 Hz
    in accordance with the IEC 61000-4-30 standard.

    Parameters
    ----------
    samples: pandas.DataFrame
        The sample voltages of the signals that want to measure the frequency.

    Returns
    -------
    freq: pandas.DataFrame
        The grid frequency in each window.

    Raises
    ------
    ValueError: When the capture time calculated is smaller than 10 seconds.

    Examples
    --------
    >>> from typhoon.test.signals import pandas_3ph_sine, pandas_sine
    >>> from typhoon.test.IEC61000 import frequency
    >>> signal = pandas_sine(duration=10.1, Ts=10/100000)  # signal needs to be 10s or bigger
    >>> freqs = frequency(sample)

    See also
    --------
    typhoon.test.IEC61000.rms
    typhoon.test.IEC61000.harmonic_content
    """
    return _impl.frequency(samples)


def flicker(
    samples: Union[pandas.DataFrame, pandas.Series],
    reference_voltage: float,
    reference_frequency: float,
    nominal_voltage: float,
    nominal_frequency: float,
    returns="all_parameters",
):
    """
    This method is used for evaluating flicker severity and calculating the d parameters in relation to steady state
    conditions. This method is applied only to grids with a nominal frequency of 50.0 Hz or 60.0 Hz in accordance with
    the IEC 61000-4-30 standard.

    Parameters
    ----------
    samples: pandas.DataFrame or pandas.Series
        Voltage samples captured from simulation.

    reference_voltage: float
        Voltage value used to determine the parameters of the weighting filter block that simulates the frequency
        response of the human ocular system to sinusoidal voltage fluctuations of a coiled filament gas-filled lamp.
        This value can be 230.0 V or 120.0 V.

    reference_frequency: float
        Frequency value used to determine the parameters of the weighting filter block that simulates the frequency
        response of the human ocular system to sinusoidal voltage fluctuations of a coiled filament gas-filled lamp.
        This value can be 60.0 Hz or 50.0 Hz.

    nominal_voltage: float
        Nominal voltage of the grid to be measured. This value can be 100.0 V, 120.0 V, 220.0 V or 230.0 V.

    nominal_frequency: float
        Nominal frequency of the grid to be measured. This value can be 60.0 Hz or 50.0 Hz.

    returns: str
        Describes which parameters the function should return, considering the metrics calculated on the
        flickmeter project (IEC 61000-4-15). This parameter accepts the following arguments:
            - ``"d_parameters"`` - Return the values ``(dc, d_max, t_max)``.
            - ``"Pinst"`` - Return the ``Pinst`` values.
            - ``"Pst"`` - Return the ``Pst`` values.
            - ``"Plt"`` - Return the ``Plt`` values.
            - ``"all_parameters"`` - Return the ``(Pst, Plt, dc, d_max, t_max)`` values.

    Returns
    -------
    Pst: numpy.array
        Is the ``Short-Term Flicker Severity``, measures the severity based on an observation period (10 min).
        This is derived from the time-at-level statistics obtained from the level classifier in block 5 of the
        flickermeter.
    Plt: numpy.array
        The long-term flicker severity (Plt), shall be dethe Short-Term Severity values (Pst).
        The Plt value is calculated over a 2-hour period measurement. This time frame is recommended for power quality
        measurements according to IEC 61000-4-30, and for measurements in accordance with IECs 61000-3-3 and 61000-3-11.
    dc: float
        The highest absolute value of all steady state voltage change observations during an
        observation period.
    d_max: float
        The highest absolute voltage change observed during an observation period.
    t_max: float
        Maximum time duration during the observation period in which the voltage deviation exceeds the dc limit.
    Pinst: numpy.array
        The output of block 4 represents the instantaneous flicker sensation (Pinst).

    Raises
    ------
    ValueError: When the parameters passed for the function are different from what is specified in the documentation.

    ValueError: When the capture time calculated from the timedelta index is smaller than 7800 seconds (2h10min) using
        ``returns="all_parameters"`` or ``returns="Plt"``.

    ValueError: When the capture time calculated from the timedelta index is smaller than 1200 seconds (20min) using
        ``returns="Pst"``.

    ValueError: When the capture time calculated from the timedelta index is smaller than 10 seconds using
        ``returns="d_parameters"``.

    Note
    ----
    The initial 2 seconds of the analyzed signal are not considered when using ``returns="d_parameters"``.

    Examples
    --------
    >>> import numpy as np
    >>> import scipy.signal as sig
    >>> from typhoon.test.IEC61000 import flicker
    >>>
    >>> # Parameters of the signal
    >>> duration = 10
    >>> sample_rate = 1000
    >>> rms_voltage = 230
    >>> frequency = 60
    >>>
    >>> # Signal and modulation signal
    >>> time = np.linspace(0, duration, sample_rate * duration)
    >>> fundamental_voltage = rms_voltage * np.sqrt(2) * np.sin(2 * np.pi * frequency * time)
    >>>
    >>> frequency_modulation, amplitude_modulation = 0.500, 0.597
    >>>
    >>> modulation = (amplitude_modulation / 2 / 100) * sig.square(2 * np.pi * frequency_modulation * time) + 1
    >>>
    >>> # pandas.Series of the ``voltages_sample = fundamental_voltage * modulation`` signals
    >>> time_index = pd.to_timedelta(time, "s")
    >>> voltage_samples = pd.Series(fundamental_voltage * modulation, index=time_index)
    >>> dc, d_max, Tmax = flicker(voltage_samples, rms_voltage, frequency, rms_voltage, frequency, 'd_parameters')

    See also
    --------
    typhoon.test.IEC61000.rms
    """
    return _impl.flicker(
        samples,
        reference_voltage,
        reference_frequency,
        nominal_voltage,
        nominal_frequency,
        returns,
    )


def harmonic_content(
    samples: pandas.DataFrame,
    nominal_grid_freq: float,
    max_harmonic_order: int,
    interharm: bool = False,
    reference_split=None,
):
    """
    This method measures harmonics, interharmonics, and total harmonic distortion according to IEC
    61000-4-7. The measurements are valid up to the 180th (50 Hz) or 150th (60 Hz) harmonic order.

    Parameters
    ----------
    samples: pandas.DataFrame
        Samples captured from simulation. The grid voltage is used for synchronization and detecting zero-crossings.
        According to the IEC 61000-4-30 standard the calculation window length is determined by the grid frequency.
        The voltage is also used to calculate harmonics, interharmonics, and total harmonic distortion.

    nominal_grid_freq : float
        According to the IEC 61000-4-7 standard, this method is applied only in grids with a nominal frequency of
        50.0 Hz or 60.0 Hz.

    max_harmonic_order: int
        The order of the highest harmonic that is taken into account.

    interharm: bool
        If True, returns the rms values of the harmonics and interharmonics.
        If False, returns the rms values of the harmonics only.

    reference_split: list, optional
        List of indices to split the sample in windows. If None, the samples will be split according to the zero-crossings
        of the voltage signal.

    Returns
    -------
    THD: numpy.array
        Ratio of the r.m.s. value of the sum of all the harmonic components up to a specific
    order to the r.m.s. voltage of the fundamental component, measured per window.
    rms_values: numpy.array
        RMS of a spectral components (harmonics and interharmonics).
    freq: numpy.array
        Frequency measured at each measurement window.

    Raises
    ------
    ValueError: When the ``nominal_grid_freq`` is different from 50 Hz or 60 Hz


    Examples
    --------
    >>> from typhoon.test.signals import pandas_sine
    >>> from typhoon.test.IEC61000 import harmonic_content
    >>>
    >>> frequency = 60
    >>> max_harmonic_order = 33
    >>> enable_interharmonics = False
    >>> samples = pandas_sine(frequency=frequency)
    >>>
    >>> THD, rms_components, measure_frequency = harmonic_content(samples, frequency, max_harmonic_order, enable_interharmonics)
    """
    return _impl.harmonic_content(
        samples, nominal_grid_freq, max_harmonic_order, interharm, reference_split
    )


def power_quantities(
    voltage_samples: pandas.DataFrame,
    current_samples: pandas.DataFrame,
    nominal_grid_freq: float,
    reference_split=None,
):
    """
    This method measures power quantities under non-sinusoidal conditions (general case) according to IEC
    61000-1-7. This method is applied only in grids with a nominal frequency of 50.0 Hz or 60.0 Hz.

    Parameters
    ----------
    voltage_samples: pandas.DataFrame
        Samples of voltage data captured from simulation.

    current_samples: pandas.DataFrame
        Samples of current data captured from simulation.

    nominal_grid_freq: float
        Nominal frequency of the grid (in Hz).

    reference_split: list, optional
        List of indices to split the sample in windows. If None, the samples will be split according to the zero-crossings
        of the voltage signal.

    Returns
    -------
    active_power: pandas.DataFrame
        Active power calculated over the entire signal.
    apparent_power: pandas.DataFrame
        Apparent power calculated over the entire signal.
    non_active_power: pandas.DataFrame
        Non-active power (reactive power + distortion power) calculated over the entire signal.
    power_factor: pandas.DataFrame
        Power factor calculated over the entire signal.
    fundamental_active_power: pandas.DataFrame
        Active power calculated over the fundamental frequency component.
    fundamental_apparent_power: pandas.DataFrame
        Apparent power calculated over the fundamental frequency component.
    reactive_power: pandas.DataFrame
        Reactive power calculated over the fundamental frequency component.
    fundamental_power_factor: pandas.DataFrame
        Power factor calculated over the fundamental frequency component.
    distortion_active_power: pandas.DataFrame
        Active power due to harmonic distortion.
    non_fundamental_power_factor: pandas.DataFrame
        Power factor calculated over the non-fundamental frequency components.
    non_fundamental_apparent_power: pandas.DataFrame
        Apparent power calculated over the non-fundamental frequency components.
    distortion_reactive_power: pandas.DataFrame
        Reactive power due to harmonic distortion.

    Raises
    ------
    ValueError: When the ``nominal_grid_freq`` is different from 50 Hz or 60 Hz

    Examples
    --------
    >>> from typhoon.test.signals import pandas_sine
    >>> from typhoon.test.IEC61000 import power_quantities
    >>> frequency = 50
    >>> voltage_samples = pandas_sine(phase=0, frequency=frequency)
    >>> current_samples = pandas_sine(phase=90, frequency=frequency)
    >>>
    >>> (active_power, apparent_power, non_active_power, power_factor, fundamental_active_power,
    >>>  fundamental_apparent_power, reactive_power, fundamental_power_factor, distortion_active_power,
    >>>  non_fundamental_power_factor, non_fundamental_apparent_power,
    >>>  distortion_reactive_power) = power_quantities(voltage_samples, current_samples, frequency)

    See also
    --------
    typhoon.test.IEC61000.power_quantities_three_phase
    """
    return _impl.power_quantities(
        voltage_samples, current_samples, nominal_grid_freq, reference_split
    )


def power_quantities_three_phase(
    voltages_samples: pandas.DataFrame,
    currents_samples: pandas.DataFrame,
    nominal_grid_freq: float,
    line_voltage: bool = True,
    reference_split=None,
):
    """
    This method measures power quantities in Three-phase systems under non-sinusoidal conditions (general case)
    according to IEEE Std 1459-2010. This method is applied only in grids with a nominal frequency of 50.0 Hz or
    60.0 Hz.

    Parameters
    ----------
    voltages_samples : pandas.DataFrame
        Voltage points vector.
    currents_samples : pandas.DataFrame
        Current points vector.
    nominal_grid_freq : float
        Nominal frequency of the voltage signal; 50 Hz or 60 Hz.
    line_voltage : bool
        Type of voltage; line-to-line or line-to-neutral voltage.
    reference_split: list, optional
        List of indices to split the sample in windows. If None, the samples will be split according to the zero-crossings
        of the voltage signal.

    Returns
    -------
    active_power: pandas.DataFrame
        The measured active power of the input data in W.
    fundamental_active_power: pandas.DataFrame
        The measured active power in W only considering the fundamental component of the input data.
    nonfundamental_active_power: pandas.DataFrame
        The measured active power in W subtracting the fundamental component of the input data.
    effective_voltage: pandas.DataFrame
        The measured effective voltage of the input data in V.
    fundamental_effective_voltage: pandas.DataFrame
        The measured effective voltage in V considering the fundamental component of the input data.
    nonfundamental_effective_voltage: pandas.DataFrame
        The measured effective voltage in V subtracting the fundamental component of the input data.
    effective_current: pandas.DataFrame
        The measured effective current of the input data in A.
    fundamental_effective_current: pandas.DataFrame
        The measured effective current in A considering the fundamental component of the input data.
    nonfundamental_effective_current: pandas.DataFrame
        The measured effective current in A subtracting the fundamental component of the input data.
    effective_apparent_power : pandas.DataFrame
        The measured apparent power of the input data in VA.
    fundamental_effective_apparent_power : pandas.DataFrame
        The measured apparent power in VA only considering the fundamental component of the input data.
    nonfundamental_effective_apparent_power : pandas.DataFrame
        The measured apparent power in VA subtracting the fundamental component of the input data.
    harmonic_apparent_power : pandas.DataFrame
        Evaluates the amount of VA caused by harmonic distortion.
    non_active_power : pandas.DataFrame
        The measured non active power of the input data in VAr.
    current_distortion_power: pandas.DataFrame
        The apparent power caused by current distortion in relation to the fundamental voltage component.
    voltage_distortion_power:pandas.DataFrame
        The apparent power caused by voltage distortion in relation to the fundamental current component.
    power_factor : pandas.DataFrame
        The measured power factor of the input data.
    harmonic_pollution_factor : pandas.DataFrame
        This power factor quantifies the overall amount of harmonic pollution delivered or absorbed by a load.
    fundamental_positive_active_power : pandas.DataFrame
        The measured active power in W considering only the fundamental component of the positive-sequence of the
        input data.
    fundamental_positive_reactive_power : pandas.DataFrame
        The measured reactive power in VAr only considering the fundamental component of the positive-sequence of the
        input data.
    fundamental_positive_apparent_power : pandas.DataFrame
        The measured apparent power in VA only considering the fundamental component of the positive-sequence of the
        input data.
    fundamental_unbalance_power : pandas.DataFrame
        Evaluates the amount of VA caused by an unbalanced system.
    fudamental_positive_power_factor : pandas.DataFrame
        The measured power factor only considering the fundamental component of the positive-sequence of the input data.
    load_unbalance : pandas.DataFrame
        The estimated load unbalance between the phases, considering the fundamental active and reactive power and the
        THD measured on the system.
    harmonic_distortion_power: pandas.DataFrame
         The measured non active power in VAr considering the harmonic components of the input data.

    Examples
    --------
    >>> from typhoon.test.signals import pandas_3ph_sine
    >>> from typhoon.test.IEC61000 import power_quantities_three_phase
    >>>
    >>> frequency = 60.0
    >>> line_to_line_voltage = True
    >>> voltage_samples = pandas_3ph_sine(phase=0, frequency=frequency)
    >>> current_samples = pandas_3ph_sine(phase=90, frequency=frequency)
    >>>
    >>> (active_power_df, fundamental_active_power_df, nonfundamental_active_power_df,
    >>> effective_voltage_df, fundamental_effective_voltage_df, nonfundamental_effective_voltage_df,
    >>> effective_current_df, fundamental_effective_current_df, nonfundamental_effective_current_df,
    >>> effective_apparent_power_df, fundamental_effective_apparent_power_df,
    >>> nonfundamental_effective_apparent_power_df,  harmonic_apparent_power_df, non_active_power_df,
    >>> current_distortion_power_df, voltage_distortion_power_df, power_factor_df,
    >>> harmonic_pollution_factor_df, fundamental_positive_active_power_df,
    >>> fundamental_positive_reactive_power_df, fundamental_positive_apparent_power_df,
    >>> fundamental_unbalanced_power_df, fundamental_positive_power_factor_df, load_unbalance_df,
    >>> harmonic_distortion_power_df) = power_quantities_three_phase(
    >>>     voltage_samples, current_samples, frequency, line_to_line_voltage)

    Raises
    ------
    ValueError: When the ``nominal_grid_freq`` is different from 50 Hz or 60 Hz

    See also
    --------
    typhoon.test.IEC61000.power_quantities
    """
    return _impl.power_quantities_three_phase(
        voltages_samples,
        currents_samples,
        nominal_grid_freq,
        line_voltage,
        reference_split,
    )


def sym_comp_voltage_unbalance(
    samples: pandas.DataFrame, nominal_grid_freq: float, reference_split: list = None
):
    """
    Measures the Symmetrical components and Voltage Unbalance according to IEEE Std 1159-2019.

    Parameters
    ----------
    samples: pandas.DataFrame
        The samples of the signals in which to measure the symmetrical component, organized in columns.

    nominal_grid_freq: float
        According to the IEC 61000-4-30 standard, this method is applied only in grids with nominal frequency of 50.0 Hz
        or 60.0 Hz.

    reference_split: list, optional
        List of indices to split the sample in windows. If None, the samples will be split according to the
        zero-crossings of the voltage signal.

    Returns
    -------
    ZeroPosNeg_seq_per_window_df: pandas.DataFrame
        The magnitude of the zero sequence component, magnitude of the positive sequence component, and magnitude of the
        negative sequence component per window.

    voltage_unbalance_df: pandas.DataFrame
        The ratio of the magnitude of the negative sequence component to the magnitude of the positive sequence
        component, expressed as a percentage.

    Raises
    ------
    ValueError: When the ``nominal_grid_freq`` is different from 50 Hz or 60 Hz

    Examples
    --------
    >>> from typhoon.test.signals import pandas_3ph_sine
    >>> from typhoon.test.IEC61000 import sym_comp_voltage_unbalance
    >>>
    >>> frequency = 60
    >>> voltage_samples = pandas_3ph_sine(frequency=frequency)
    >>>
    >>> ZeroPosNeg_seq_per_window_df, voltage_unbalance_df = sym_comp_voltage_unbalance(voltage_samples, frequency)
    """
    return _impl.sym_comp_voltage_unbalance(samples, nominal_grid_freq, reference_split)
