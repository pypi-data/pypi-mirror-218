import numpy as np

from brian2.memory.dynamicarray import DynamicArray, DynamicArray1D
from brian2.core.variables import ArrayVariable, DynamicArrayVariable

from brian2.monitors.spikemonitor import SpikeMonitor
from brian2.monitors.statemonitor import StateMonitor

def get_value(self, var, access_data=True):
    """
    Get a value from an array.
    Returning a value from the device arrays depends on the type of array,
    which can either be a static array (ArrayVariable) or a dynamic array (DynamicArrayVariable).

    Parameters
    ----------
    var : `ArrayVariable`
        The array to get
    access_data : `bool`
        A flag that indicates if it is intended to access only the data of the dynamic array (True)
        or the whole dynamic array (False)

    Returns
    -------
    `any`
        Values of the array variable as list
    """

    # Log that a value was requested from arrays
    self.logger.diagnostic(f'get_value {var.name}')

    # The variable should be stored in self.arrays, if it's None then the device hasn't been run yet.
    if self.arrays.get(var, None) is not None:
        return self.arrays[var]
    
    raise NotImplementedError(
                "Cannot retrieve the values of state "
                "variables in standalone code before the "
                "simulation has been run."
            )

def get_dtype_name(var):
    """
    Get the data type of a variable and return its name as a string - serves to avoid expressions like 'np.bool' that are deprecated since NumPy 1.24.
    In the case of a NumPy data type, returns the name with the prefix 'np.'.

    Parameters
    ----------
    var : `any`
        The variable to consider (can also be a data type object itself)

    Returns
    -------
    `string`
        Name of the dtype
    """

    # If 'var' is an array
    if np.ndim(var) > 0:
        dtype = var.dtype
    # If 'var' is a scalar variable
    else:
        dtype = np.dtype(type(var))

    # Check if Python or NumPy data type is used
    if dtype in [bool, int, float, complex, str, np.int32, np.int64, np.float32, np.float64]:
        ret = dtype.name.replace('32', '').replace('64', '')
    else:
        ret = "np." + dtype.name

    return ret


def get_lava_var_name(self, var):
    """
    Get a lava variable name based on an array variable.

    Parameters
    ----------
    var : `ArrayVariable`
        An array variable

    Returns
    -------
    `string`
        The corresponding lava variable name

    Notes
    -----
    TODO This can possibly be hamrmonized with `get_array_name`.
    """

    if isinstance(var.owner, StateMonitor):
        source_name = 'defaultclock' if var.name == 't' else var.owner.source.name
        #source_name = var.owner.name
        return f'_{source_name}_{var.name}'
    elif isinstance(var.owner, SpikeMonitor):
        lava_var_name = ''
        if var.name == 't': lava_var_name = '_defaultclock_t'
        if var.name == 'i': lava_var_name = var.owner.source.name +'_s_out'
        # Manage the case of additional variables in the SpikeMonitor
        else: lava_var_name = f'_{var.owner.source.name}_{var.name}'
        return lava_var_name
    else:
        return self.get_array_name(var,prefix=None)


def get_array_name(self, var, access_data=True, prefix='self.'):
    """
    Gets the name of an array variable.

    Parameters
    ----------
    var : `ArrayVariable`
        The array to get.
    access_data : `bool`
        A flag that indicates if it is intended to access only the data of the dynamic array (True)
        or the whole dynamic array (False)
    prefix : `string`
        A string that is added as a prefix to the array name
        Default is 'self.', in case of 'None', no prefix is added

    Returns
    -------
    `string`
        The corresponding variable name as it is used in Brian

    Notes
    -----
    TODO This can possibly be harmonized with `get_lava_var_name`.
    """
    
    # The name of the array is part of the owner attribute
    # The owner is a `Nameable`, e.g. `NeuronGroup` or `Synapses`
    # If no owner name is available, 'temporary' is assigned
    owner_name = getattr(var.owner, 'name', 'temporary')
    

    # Redefine prefix to empty string if it was set to 'None'
    if prefix is None:
        prefix = ''
    
    return f'{prefix}_{owner_name}_{var.name}'


def get_monitor_type_name(owner):
    """
    Get monitor type name, i.e. spike monitor or state monitor

    Parameters
    ----------
    owner : `StateMonitor` or `SpikeMonitor`
        The owner of a group

    Returns
    -------
    `string`
        The corresponding monitor type as string
    """

    # Init monitor type variables
    monitor_type_name = ''

    # Check instance of owner and define types
    if isinstance(owner, StateMonitor):
        monitor_type_name = 'state'
    elif isinstance(owner, SpikeMonitor):
        monitor_type_name = 'spike'
    else:
        raise Exception('Unknown owner instance. Owner instance has to be StateMonitor or SpikeMonitor.')

    return monitor_type_name


def add_array(self, var):
    """
    Add a variable array to the `arrays` list of the device.
    It can either be added directly or as a `DynamicArrayVariable` object.
    The `DynamicArrayVariable` can dynamically be extended (in contrast to a static array).

    We separate between monitors and all other owner types of the variable to add.
    Monitors are added to the `lava_monitors` list. All other variable types are added to `lava_variable_names`.

    Parameters
    ----------
    var : `ArrayVariable`
        The array variable to add
    """

    # NOTE only for Loihi hardware, on CPU this is not necessary
    # Only add array if owner is of class SpikeMonitor or StateMonitor
    #if not isinstance(var.owner, (SpikeMonitor, StateMonitor)):
    #    return

    # Log that a value was added to arrays
    self.logger.diagnostic(f'add_array {var.name}')

    # Create a static numpy array
    arr = np.empty(var.size, dtype=var.dtype)

    # Add array to device arrays
    self.arrays[var] = arr

    if isinstance(var.owner, (SpikeMonitor, StateMonitor)):
        # NOTE Currently only dynamic array variables of a monitor (like v, t, etc.) are added
        #      Constant values like N or __indices are currently ignored
        if isinstance(var, DynamicArrayVariable):
            if isinstance(var.owner.record,bool):
                # we only add a monitor if the record flag is not set to False, which means that the
                # monitor is not used for recording.
                if var.owner.record == False:
                    if isinstance(var.owner,SpikeMonitor):
                        self.logger.warn("Currently, setting 'record=False' in the SpikeMonitor is being ignored. It will be implemented in future releases")
                    else:
                        return   
            else:
                msg = """[EFFICIENCY]: Setting recording indices is currently not supported by Lava. 
                        The monitor will record all indices, which will then be filtered by brian2lava at a 
                        later stage (so that the output will be compatible with what expected from Brian). 
                        For this reason, the current implementation will be significantly slower than the 
                        Brian implementation for larger simulations."""
                # Check if the user is trying to record specific indices
                try:
                    if len(var.owner.record) != len(var.owner.source) and var.name != 't':
                        self.logger.warn(msg)
                # This error is raised in case len(source) is not defined yet (we need to run the simulation first), 
                # in this case the warning still applies, though.
                except NotImplementedError:
                    self.logger.warn(msg)

            # Get monitor type name from owner ('state' or 'spike')
            monitor_type_name = get_monitor_type_name(var.owner)

            # We don't need a monitor for spike timings since this measurement is 
            # handled differently.
            if var.name == 't' and monitor_type_name == 'spike':
                return

            # Define monitor name and lava variable name
            monitor_name = f'_{monitor_type_name}_{var.owner.name}'
            # Spike monitors don't need variable names, this is to allow monitoring additional variables.
            monitor_name += f'_{var.name}' if isinstance(var.owner, StateMonitor) else ''
            lava_var_name = self.get_lava_var_name(var)

            # Set up the additional monitors if they were not yet defined.
            if not monitor_name in self.additional_monitors:
                self.additional_monitors[monitor_name] = []

            # Collect lava variable names that shall be monitored by lava
            # NOTE Only add variable name if it's not already in the list
            #      Variable names can occure in multiple monitors, e.g. time
            if lava_var_name not in self.lava_variables_to_monitor:
                self.lava_variables_to_monitor.append(lava_var_name)

            # Special case: If the monitor already exists then we are dealing with an additional variable for SpikeMonitor
            if monitor_type_name == 'spike' and var.name != 'i':
                monitor_dict = {
                        'name' : monitor_name + f"_add_{var.name}", # The name of this monitor, mainly for debugging
                        'source': var.owner.source.name,
                        'var': var,  # Brian variable
                        'indices': var.owner.record,  # The indices of the variable to record
                        'lava_var_name': lava_var_name,  # The variable name used in Lava
                        'lava_monitor': None,  # The Lava monitor, instance is added later during 'run'
                        'process_name': None # The name of the process that is monitored, will be set in 'run'
                    }
                # Add this monitor to the additional monitors
                self.additional_monitors[monitor_name].append(monitor_dict)
                try:
                    # Add the additional monitors to the existing monitor
                    self.lava_monitors[monitor_name]['additional_var_monitors'] = self.additional_monitors[monitor_name]
                except KeyError:
                    # This happens if the monitor was not added yet, so the additional monitors will be added 
                    # when the monitor is defined through the 'i' variable.
                    self.logger.debug(f"Monitor {monitor_name} not added yet, will add the additional var monitor for {lava_var_name} later.")
                return

            # This is the general purpose case. We are dealing with a new monitor.
            self.lava_monitors[monitor_name] = {
                'name' : monitor_name, # The name of this monitor, mainly for debugging
                'source': var.owner.source.name,
                'var': var,  # Brian variable
                'indices': var.owner.record,  # The indices of the variable to record
                'lava_var_name': lava_var_name,  # The variable name used in Lava
                'type': self.monitor_types[monitor_type_name],  # The monitor type ('state' or 'spike')
                'additional_var_monitors': self.additional_monitors[monitor_name],  # Additional variables to monitor, e.g. 'v' for SpikeMonitor
                'lava_monitor': None,  # The Lava monitor, instance is added later during 'run'
                'process_name': None # The name of the process that is monitored, will be set in 'run'
            }
    else:
        
        dtype_name = get_dtype_name(arr)
        type_name = dtype_name

        # Add the definition of a numpy array as string for lava
        # By default we initialize to zero, as it's generally a safe value.
        var_definition = f'np.zeros({var.size}, dtype={type_name})'

        # TODO is the key unique?
        # See also: https://github.com/brian-team/brian2/pull/304
        name = self.get_array_name(var,prefix=None)
        self.lava_variables[name] = {
            'name': var.name,
            'owner': var.owner.name,
            'definition': var_definition,
            'size': var.size,
            'shape': np.shape(arr),
            'type': type_name,
            'dtype': dtype_name
        }

        # NOTE information from this dict can also be obtained from self.lava_variables
        #      directly, but it's a bit complicated, for now we can leave it as a kind of cache
        self.lava_variable_names[var.name] = name


def init_with_zeros(self, var, dtype):
    """
    Initialize an array with zeros and adds it to the `arrays` list.

    Parameters
    ----------
    var : `ArrayVariable`
        The array variable to initialize with zeros
    dtype : `dtype`
        The data type to use for the array
    """

    # Redefine variable definition for Lava variables
    name = self.get_array_name(var,prefix=None)
    if name in self.lava_variables.keys():
        lv = self.lava_variables[name]
        lv['definition'] = f"np.zeros({lv['size']}, dtype={lv['dtype']})"
    
    # Log that an empty array was initialized
    self.logger.diagnostic(f'init_with_zeros {var.name}')
    
    self.arrays[var][:] = 0


def init_with_arange(self, var, start, dtype):
    """
    Initializes an array using the numpy arange function and adds it to the `arrays` list.
    The `start` value defines the start of the range, the length is given by the length of the `var` array.
    
    Parameters
    ----------
    var : `ArrayVariable`
        The array to initialize is based on the length of this `var` array
    start : `int`
        Start value of the range
    dtype : `dtype`
        The data type to use for the array
    """

    # Redefine variable definition for Lava variables
    name = self.get_array_name(var,prefix=None)
    if name in self.lava_variables.keys():
        lv = self.lava_variables[name]
        lv['definition'] = f"np.arange({start}, {lv['size']+start}, dtype={lv['dtype']})"
    
    # Log that an array was created based on numpy arange
    self.logger.diagnostic(f'init_with_arange, arange from {start} to {var.get_len()+start}')
    
    self.arrays[var][:] = np.arange(start, stop=var.get_len()+start, dtype=dtype)


def fill_with_array(self, var, arr):
    """
    Fill array variable `var` with the values given in an array `arr` and add it to the `arrays` list.
    Instead of modifying the definition of the variable itself, we add a line of code to the init queue
    which will be executed at initialization of the process. This allows the user to modify variables
    seamlessly any number of times without incurring into bugs.
    The methodology we use is compatible with the one used in the CPPStandaloneDevice:
    https://github.com/brian-team/brian2/blob/master/brian2/devices/cpp_standalone/device.py#L415
    
    Parameters
    ----------
    var : `ArrayVariable`
        The array variable to fill
    arr : `ndarray`
        The array values that should be copied to `var`
    """

    arr = np.asarray(arr)
    # Redefine variable definition for Lava variables
    name = self.get_array_name(var,prefix=None)
    if name in self.lava_variables.keys():
        lv = self.lava_variables[name]

        # Check if 'arr' is given as scalar
        is_scalar = not bool(len(np.shape(arr)))
        
        # If 'arr' is scalar and size is 1, we set the whole var to that value
        # This accounts for variables initially initialized to [0.] but which will be resized later on.
        # FIXME: the 'size' key could cause other bugs in the future, so it needs to be addressed!
        if is_scalar and lv['size'] == 1:
            self.proc_init_queue[var.owner.name].append(('set_by_single_value', (name,':',arr.item())))
        # If 'arr' is scalar and size > 1, add an array that repeats the value accordingly
        elif is_scalar and lv['size'] > 1:
            self.proc_init_queue[var.owner.name].append(
                (
                'set_by_constant', (name,arr.item())
                )
            )
        # If 'arr' is actually an array, it's just transformed to a string definition
        else:
            if not lv['size'] == arr.shape[0]:
                raise ValueError(f"The array used to set variable {name} is not of the same size as the variable. {lv['size']}!={arr.shape[0]}")
            arr_str = np.array2string(np.array(arr), separator=', ')
            self.proc_init_queue[var.owner.name].append(
                ('set_by_array', (name,arr_str))
            )

    # Log that an array was filled with given values
    self.logger.diagnostic(f'fill_with_array, add {arr} to {var.name}')
    
    # Set array value
    if isinstance(var, DynamicArrayVariable):
        # Following CPPStandalone example, we can't correctly know the 
        # value of a dynamic array, so for now we don't save it at all
        self.arrays[var] = None
    else:
        self.arrays[var][:] = arr

def resize(self, var, new_size):
    """
    Method called most times a DynamicArray variable is created. Updates the size of a DynamicArray.
    We add this operation to the initialization queue for the lava processes in order to keep the ordering consistent.
    """
    # This is an operation we can still manage with the array cache (useful for synaptic numbers such as N_incoming and N_outgoing)
    if self.arrays.get(var,None) is not None:
        self.arrays[var] = np.resize(self.arrays[var], new_size)
    # Change the size of the variable in our init_queue
    name = self.get_array_name(var,prefix=None)
    if name in self.lava_variables.keys():
        self.proc_init_queue[var.owner.name].append(('resize_array', (name,new_size)))


    

