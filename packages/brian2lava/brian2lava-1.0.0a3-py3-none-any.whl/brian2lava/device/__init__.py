import jinja2
import os
import numpy as np
from collections import defaultdict

#from types import SimpleNamespace
from weakref import WeakKeyDictionary

# Import Brian2 modules
from brian2.devices.device import all_devices, Device
from brian2.utils.logger import get_logger

__all__ = ['LavaDevice']


class LavaDevice(Device):
    """
    The Lava device combines most of the functionality. It activates the device,
    transforms all variables (to and from Lava), builds and executes the generated Lava code.

    The generation of the Lava Python code, based on the abstract code from Brian,
    is performed mostly from the `LavaCodeGenerator` and partly from `LavaCodeObject`.
    Also the `code_object` method within this `LavaDevice` takes part in generating Lava code.

    The LavaDevice is split into several files. The import statements below the init method
    include the code of the other files into the LavaDevice.
    """


    def __init__(self):
        super(LavaDevice, self).__init__()
        # Make logger available to all methods in this class
        self.logger = get_logger('brian2.devices.lava')

        # Store root directory of this package
        self.package_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # The project dir is fixed in the Lava device
        # This is important, since a reinit otherweise don't know which directory to clean
        self.project_dir = 'lava_workspace'
        os.makedirs('lava_workspace', exist_ok=True)
        # Clear the contents of the workspace if it already existed.
        for filename in os.listdir(self.project_dir):
            file_path = os.path.join(self.project_dir, filename)

            if os.path.isfile(file_path):
                os.remove(file_path)

        # FIXME Defines the network schedule, if None, the user can choose the schedule
        self.network_schedule = None
        # NOTE Brian2Loihi used: ['start', 'synapses', 'groups', 'thresholds',  'resets', 'end']

        # Random number buffer
        self.randn_buffer_index = np.zeros(1, dtype=np.int32)
        self.rand_buffer_index = np.zeros(1, dtype=np.int32)

        # Predefines a default clock, it is set in the `activate` method
        self.defaultclock = None

        # Define an empty set to store clocks
        self.clocks = set([])

        # Stores weak references from a `Variable` objects to the containing value(s)
        # Methods to handle the arrays are provided in `arrays.py`
        self.arrays = {}  # FIXME is was originally a WeakKeyDictionary()
        self.array_cache = {}
        self.proc_init_queue = defaultdict(list) # In CPP device 'main_queue' a list, but we need a queue for each process
        self.proc_model_add_code = defaultdict(set) # Additional code for process models. Defaults to set to avoid duplicates, ordering shouldn't matter.

        # Define empty dicts to store code objects and abstract code
        self.code_objects = {}

        # Brian network objects
        self.net_objects = set()

        # Store Lava variables
        # Key: variable name, Value: variable definition (e.g. 'np.empty(...)')
        self.lava_variables = {}
        self.lava_variable_names = {}
        
        # Store the ports required to connect processes
        self.spike_queues = {}
        self.lava_ports = {}

        # Brian template functions that belong to the process,
        # instead of the process model, e.g. 'group_variable_set'
        self.init_template_functions = [
            'group_variable_set',
            'group_variable_set_conditional',
            'synapses_create_generator',
            'synapses_create_array'
        ]
        
        # Variables that represent our current feature support
        from brian2 import SpikeGeneratorGroup, NeuronGroup, Synapses, PoissonGroup
        self.supported_processes = [
            NeuronGroup,
            Synapses,
            SpikeGeneratorGroup,
            PoissonGroup
        ]
        from brian2 import PoissonInput,PopulationRateMonitor,SpatialNeuron
        from brian2.synapses.synapses import SummedVariableUpdater
        self.unsupported_processes = [
            PoissonInput,
            PopulationRateMonitor,
            SpatialNeuron,
            SummedVariableUpdater
        ]

        self.available_hardware = ["CPU"]

        # Stores names of indices that are used to initialize variables
        # e.g. _group_idx_1_v, _group_idx_2_ge, etc.
        self.set_variable_index_names = []

        # Store Lava monitors
        # NOTE Some variables shall be probed only once by Lava, but are required
        #      for different Brian monitors, e.g. time
        self.lava_variables_to_monitor = []
        self.lava_monitors = {}
        # Add monitors for additional variables (only for SpikeMonitors)
        self.additional_monitors = {}
        #self.brian_monitors = {}

        self.monitor_types = {'state': 0, 'spike': 1}  # SimpleNamespace(**{ 'state': 0, 'spike': 1 })

        # Stores if the network did run
        self.did_run = False  # FIXME necessary?: Yes? since otherwise the user
        # can use multiple run calls but if he does it the objects and network
        # might have changed but the compiled code for lava is still the old
        # one. He needs to do a device.reini(), device.activat() to reinit the
        # whole build process again. WIth this flag here we chan check this.

        # Define constants
        #C = SimpleNamespace(**{
        #    CPU: 'CPU',
        #    LOIHI1: 'Loihi1',
        #    LOIHI2: 'Loihi2'
        #})

        # Add super to self to make it available in sub-files
        self.super = super(LavaDevice, self)

    
    # Device activation
    from .activate import (
        activate, seed, reinit
    )

    # Build the network
    from .build import (
        build, render_templates, get_compiled_code, get_jinja_environment,
        get_lava_proc_variables, get_lava_proc_model_variables,
        get_lava_function_calls, get_lava_ports_definitions, generate_init_queue,
        generate_additional_code, get_proc_model_init_code, get_lrn_guard_code
    )

    # Writer for writing rendered templates
    from .writer import (
        prepare_directory, write_templates
    )

    # Define code objects
    from .codeobject import (
        code_object
    )

    # Run the network
    from .run import (
        network_run, 
        run_processes,
        set_brian_monitor_values,
        init_lava_monitors, 
        connect_lava_ports,
        select_root_processes,
        update_brian_class_attributes
    )

    # Handle storage
    from .arrays import (
        add_array, get_value, get_array_name, init_with_zeros,
        init_with_arange, fill_with_array,
        get_lava_var_name, resize
    )

    # Handle setter and getter for variables
    from .variables import (
        variableview_set_with_index_array,
        variableview_set_with_expression,
        variableview_set_with_expression_conditional
    )

    # Handle synapses
    from .synapses import (
        synapses_connect,
        spike_queue,
        determine_lava_ports,
        _add_spiking_synapses_vars
    )


# Add lava device to all_devices and make it with this available to Brian2
lava_device = LavaDevice()
all_devices['lava'] = lava_device
