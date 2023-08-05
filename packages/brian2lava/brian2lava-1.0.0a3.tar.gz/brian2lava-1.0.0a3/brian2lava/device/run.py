import os
import importlib
import numpy as np

from brian2.core.clocks import Clock
from brian2.core.namespace import get_local_namespace
from brian2.core.network import TextReport, _get_all_objects
from brian2.groups.neurongroup import NeuronGroup
from brian2.synapses.synapses import Synapses
from brian2.units import second

from lava.magma.core.run_configs import Loihi1SimCfg
from lava.magma.core.run_conditions import RunSteps
from lava.proc.monitor.process import Monitor

def network_run(
        self,
        net,
        duration,
        report=None,
        report_period=10 * second,
        namespace=None,
        profile=False,
        level=0,
        **kwds
    ):
    """
    Performs preparations and checks and finally calls the `build` method from the device.

    Notes
    -----
    Overwrites the `run()` method from `brian2.core.Network.run()` so for reference, see:
    https://brian2.readthedocs.io/en/stable/reference/brian2.core.network.Network.html#brian2.core.network.Network.run

    Note that in the current implementation, the following arguments are not supported and will thus be ignored or raise an error:
        - report -> ignored
        - report_period -> ignored
        - profile -> error
    """
    # Before doing anything check that the objects used by the user 
    # are supported by lava.
    check_for_brian2lava_support(net)
    
    # Store duration in device
    self.duration = duration
    
    # Log that the network run method was called
    self.logger.diagnostic("Network run is executing.")
    
    # If keyword arguments are given, notify the user that these arguments are not used in Brian2Lava
    if kwds:
        self.logger.warn(
            'Unsupported keyword argument(s) provided for run: {}'.format(', '.join(kwds.keys()))
        )
        
    # FIXME Show an error if user enabled profiling, since it is not supported
    if profile is True:
        raise NotImplementedError('Brian2Lava does not yet support detailed profiling.')
    
    # FIXME Set clocks
    net._clocks = {obj.clock for obj in net.sorted_objects}
    t_end = net.t+duration
    for clock in net._clocks:
        clock.set_interval(net.t, t_end)
    
    # Manage Spike Queues. TODO: Move this in a better place if possible
    # For now I put it here because I want this to happen as soon as possible during the
    # run call. (But still after any variable definition has been made (e.g. setting delays.))
    for obj in net.sorted_objects:
        if isinstance(obj,Synapses):
            for pathway in obj._pathways:
                # The spike queue is only added if delays are defined.
                has_spike_queue = False
                try:
                    if len(pathway._delays.get_value()):
                        has_spike_queue = True
                # The device will raise this error if the delay variable was modified 
                # and requires to be manipulated during runtime (e.g. S.delays = 'expression').
                except NotImplementedError:
                    has_spike_queue = True
                                
                if has_spike_queue:
                    spike_queue = f'{obj.name}_{pathway.objname}_spike_queue'
                    # In case no delay was specified, we use an empty array
                    delays = self.get_array_name(pathway._delays)
                    self.spike_queues[spike_queue] = {
                        'name' : 'self.'+spike_queue,
                        'delays': delays,
                        'dt': str(pathway.source.clock.dt_),
                        'sources': self.get_array_name(pathway.synapse_sources),
                        'start': pathway.source.start,
                        'stop': pathway.source.stop,
                        'owner': obj
                    }
    
    # Get the local namespace, if no namespace was given
    if namespace is None:
        namespace = get_local_namespace(level=level+2)

    # Call before_run with namespace
    net.before_run(namespace)
    
    # Update device clocks by network clocks
    self.clocks.update(net._clocks)
    if len(self.clocks) > 1:
        raise NotImplementedError("Currently multiple clocks are not supported by brian2lava.")
    
    # Set current time to end time (FIXME why? and whyt is the difference between self.t and self.t_?)
    # NOTE by carlo: self.t is with unit, self.t_ is without unit
    net.t_ = float(t_end)
    
    # FIXME Taken from CPPStandaloneDevice, but unclear what it means
    # In the CPP device it is noted that this is a hack
    # https://github.com/brian-team/brian2/blob/master/brian2/devices/cpp_standalone/device.py#L1404
    for clock in self.clocks:
        if clock.name == 'clock':
            clock._name = '_clock'
    
    # Collect code objects from network objects
    # Right now these lines don't really do anything since we're never referencing the 
    # variable code_objects again in this method
    code_objects = []
    self.lava_objects = {}
    for obj in net.sorted_objects:
        if obj.active:
            # Only the objects that generate a lava process are added to the lava_objects dict 
            # (so we avoid children of objects like StateUpdater and so on.)
            if any([isinstance(obj,supp_obj) for supp_obj in self.supported_processes]):
                self.lava_objects[obj.name] = obj
            for codeobj in obj._code_objects:
                # NOTE: For code cleanup, this is never actually used anywhere. Interesting that they save the objects as tuples of (clock,object)
                code_objects.append((obj.clock, codeobj))
    

    # FIXME This may require an update, similar to how CPPStandalone handles the report
    # https://github.com/brian-team/brian2/blob/master/brian2/devices/cpp_standalone/device.py#L1465
    #if report is not None:
    #    report_period = float(report_period)
    #    next_report_time = start_time + report_period
    #    if report == 'text' or report == 'stdout':
    #        report_callback = TextReport(sys.stdout)
    #    elif report == 'stderr':
    #        report_callback = TextReport(sys.stderr)
    #    elif isinstance(report, str):
    #        raise ValueError(f'Do not know how to handle report argument "{report}".')
    #    elif callable(report):
    #        report_callback = report
    #    else:
    #        raise TypeError(f"Do not know how to handle report argument, "
    #                        f"it has to be one of 'text', 'stdout', "
    #                        f"'stderr', or a callable function/object, "
    #                        f"but it is of type {type(report)}")
    #    report_callback(0*second, 0.0, t_start, duration)

    
    # TODO? At least in the CPPStandaloneDevice, there is some more code here,
    # that seems to generate some basic code lines ...
    
    # Call network after_run method
    net.after_run()
    
    # Call build method
    if self.build_on_run:
        if self.did_run: # Building a network with previously run objects still in it can cause unwanted behavior
            raise RuntimeError("The network has already been built and run "
                               "before. Use set_device with "
                               "build_on_run=False and an explicit "
                               "device.build call to use multiple run "
                               "statements with this device.")
        self.build(direct_call=False, **self.build_options)

def check_for_brian2lava_support(net):
    """
    Checks that the objects defined by the user are supported by the lava device.
    If not, it throws a NotImplementedError
    Parameters
    ----------
    net : brian2.network.Network

    raises : NotImplementedError
            If any of the objects in the Network are not currently supported by brian2lava
    """
    from brian2 import get_device, Synapses
    device = get_device()
    # Raise an error if the user is trying to implement unsupported objects
    objects = []
    for obj in net.sorted_objects:
        # CMake a list of the unsupported objects present in the network (if any)
        if any([isinstance(obj,unsupp_obj) for unsupp_obj in device.unsupported_processes]):
            obj_type = type(obj).__name__
            objects.append(obj_type)
        for contained_obj in obj.contained_objects:
            if any([isinstance(contained_obj,unsupp_obj) for unsupp_obj in device.unsupported_processes]):
                obj_type = type(contained_obj).__name__
                objects.append(obj_type)
        
        # Check that no (event-driven) equations are defined in synapses, since these are not good for brian2lava.
        if isinstance(obj,Synapses):
            if obj.event_driven is not None:
                device.logger.warn(
                    """Using the (event-driven) specifier in synaptic models will most likely lead to 
                    unwanted behavior, because event-driven effects in lava are handled at the END of a timestep 
                    (so after synapses have already propagated the incoming signals).
                    This is due to the intrinsic asynchronicity present in Lava and particularly in neuromorphic hardware. 
                    For this reason, we recommend using the (clock-driven) specifier instead.
                    """
                )
        
    if len(objects):
        objects_repr = '\n\t\t'.join(objects)
        msg = f"""The following objects or functionalities are not supported by brian2lava, yet:
                {objects_repr}
        You can expect them in future releases. You can also ask for features 
        on the official brian2lava repo on GitLab:
        https://gitlab.com/brian2lava/brian2lava/-/tree/main
        """
        raise NotImplementedError(msg)
        


def compile_templates(directory, names):
    """
    Compiles the rendered templates and returns a dictionary containing the instantiated processes

    Parameters
    ----------
    directory : `string`
        The project directory, necessary to find files to compile.
    names : network object names
        Names of network objects that are used for the Lava templates
    
    Returns
    -------
    compiled_processes: `Process`
        The compiled Lava process
    """
    # Execute Lava process and Lava process model
    # Add all outcomes to global scope
    instantiated_processes = {}
    for name in names:
        with open(f'{directory}/{name}_process.py') as process_file:
            exec(process_file.read(),globals())
        with open(f'{directory}/{name}_process_model.py') as process_model_file:
            exec(process_model_file.read(),globals())
            
        # Get the process class
        process = globals()[f'{name}_P']
        # Instantiate the process and add it to the compiled processes
        instantiated_processes[name] = process(name = name)
    
    # Get instance of the processes
    return instantiated_processes 


def run_processes(self):
    """
    Executes the Lava simulation.

    We first compile the templates, initialize Lava and add configured monitors.
    Finally, the compiled Lava code is executed and monitor data is extracted.
    """
    
    # Compile templates
    processes = compile_templates(self.project_dir, [obj for obj in self.lava_objects])

    
    # NOTE adding one step is necessary such that spikes are evaluated
    #      correctly by Lava and match Brian results
    num_steps = int(self.duration/self.defaultclock.dt) + 1

    # First initialize the monitors
    for process in processes.values():
        self.init_lava_monitors(process, num_steps)

    # Connect the ports of connected processes
    self.connect_lava_ports(processes)
    root_processes = self.select_root_processes(processes)

    # Log that the run method was called
    self.logger.debug(f'Running Lava simulation for {self.duration} ({num_steps} steps)')
    print(f'Running Lava simulation for {self.duration} ({num_steps} steps)')
    
    # Run the simulation
    for process in root_processes:
        self.logger.debug(f"Running process: {process.name}")
        # Prepare simulation
        run_cfg = Loihi1SimCfg()
        process.run(condition=RunSteps(num_steps=num_steps), run_cfg=run_cfg)

    self.logger.debug("Successfully run simulation")

    # After running the simulation, copy the monitored values from all the processes to brian
    for process in processes.values():
        # Set monitor values
        self.set_brian_monitor_values(process)

    self.logger.debug("Successfully retrieved monitor values")

    # Update the class attributes of BrianObjects, so that the user can get their values normally.
    self.update_brian_class_attributes(processes)

    # Stop processes to terminate execution
    for process in root_processes:
        process.stop()

    # Indicate that the network simulation did run
    self.did_run = True


def connect_lava_ports(self, processes):
    """
    Connect the ports of the connected processes.

    Parameters
    ----------
    processes : dict(`Process[]`)
        Dictionary of instantiated Lava processes.
    """

    for var in self.lava_ports.values():
        portname = var['portname']
        pathway = var['pathway']

        # First connect the spiking sources to the synapses
        source = processes[var['sender']]
        synapses = processes[pathway.synapses.name]

        # To avoid the DuplicateConnection error from Lava
        syn_spikes_in = synapses.in_ports._members['s_in_'+pathway.prepost]
        # Only reshape the spike port once
        if syn_spikes_in.size == 0:
            # Here we shape the InPort of synapses to accomodate the spikes
            neur_spike_port = processes[source.name].out_ports._members[source.name+'_s_out']
            syn_spikes_in.shape = neur_spike_port.shape
            # Connect the spike ports
            neur_spike_port.connect(syn_spikes_in)
            self.logger.debug(f"Connected {source.name} spiking port to {synapses.name} input")

        # Then connect the synapses to the neurons, here we only require the name
        target = var['receiver']

        # Again, first reshape the ports as needed
        # TODO: not sure this is the intended use of the _members attribute of the Collection class:
        # https://github.com/lava-nc/lava/blob/4283428c3dda02ea6c326d5660a952cafcdd2c03/src/lava/magma/core/process/process.py
        syn_out_port = processes[synapses.name].out_ports._members[portname+'_out']
        neur_in_port = processes[target].in_ports._members[portname+'_in']

        # Reshape the input port of the neuron 
        neur_in_port.shape = syn_out_port.shape
        # Connect the port
        syn_out_port.connect(neur_in_port)

        self.logger.debug(f"Connected {synapses.name} variable {portname} to target neuron: {target}")


def select_root_processes(self, processes):
    """
    This is a helper function to determine which processes to run, in order to avoid running 
    processes connnected to each other twice. Lava automatically runs connected processes together,
    so if we have A-->B-->C we only need to run A.
    This function selects one node from each isolated subnetwork in the lava_ports dictionary through
    a breadth-first search algorithm.

    Parameters
    ----------
    processes : `Process[]`
        A list of the initialized processes in the simulation.

    Returns
    -------
    `list`
        A list of root processes, one from each isolated subnetwork.
    """

    # Build the graph of connected processes
    graph = {}
    for node in self.lava_ports.values():
        sender = node['sender']
        receiver = node['receiver']
        synapses = node['pathway'].synapses.name
        if sender not in graph:
            graph[sender] = set()
        if receiver not in graph:
            graph[receiver] = set()
        graph[sender].add(receiver)
        # Also add the synapses to the sender graph
        graph[sender].add(synapses)
        graph[receiver].add(sender)
    
    # Check for processes which don't require lava ports (isolated components)
    for process in processes:
        if not process in list(graph.keys()):
            graph[process] = set()

    # Log the whole graph to know that everything is working out correctly
    self.logger.diagnostic(graph)

    # Traverse the graph to find connected components
    visited = set()
    components = []
    # BFS algorithm: https://en.wikipedia.org/wiki/Breadth-first_search
    for node in graph:
        if node not in visited:
            component = set()
            queue = [node]
            while queue:
                curr_node = queue.pop(0)
                if curr_node not in visited:
                    visited.add(curr_node)
                    component.add(curr_node)
                    # Add the neighboring nodes to the queue
                    queue.extend(graph[curr_node])
            components.append(component)

    # Select one node from each component
    root_nodes = []
    for component in components:
        root_nodes.append(processes[list(component)[0]])

    return root_nodes


def init_lava_monitors(self, process, num_steps):
    """
    Initializes Lava monitors as required by the monitors defined by the user in Brian.
    In case a monitor has additional variables to be monitored, the function this method wraps 
    is called recursively.

    Parameters
    ----------
    process : `Process`
        Lava process. If the process possesses a variable which is to be monitored, the monitor is initialized.
    num_steps : `int`
        Number of steps for which the monitor shall be active. In the current implementation this is set to
          the number of steps in the simulation.

    Notes
    -----
    Lava variables can only be accessed by one Monitor at a time. This means that if a variable is probed
    by multiple Brian monitors, it will be probed only once by Lava. The reference to the variable values is then 
    handled by referencing the same monitor object in the different Brian monitors.
    """

    def init_lava_monitor(m,num_steps):
        """
        We define this extra method because it can be called recursively for additional variables
        """
        # If you find a process which should be monitored, look at which variable should be monitored
        lava_var_name = m['lava_var_name']

        # If the given process does not have the required variable, raise an error
        # This should never happen, but just for debugging I'll leave it for now
        if not hasattr(process,lava_var_name):
            raise ValueError(f"Something went wrong: the process {process.name} does not have the variable {lava_var_name} required from the monitor")
        
        
        # NOTE Lava allows only one monitor per variable, so we only create one if one was not already created
        try:
            # Init Lava monitor and define probe for variable
            monitor = Monitor()
            monitor.probe(getattr(process, lava_var_name), num_steps)
            # Allow probing of additional variables for spike monitors
            for additional_monitor in m['additional_var_monitors']:
                init_lava_monitor(additional_monitor, num_steps)

        # If the monitor already exists, lava throws an AssertionError
        except AssertionError:
            # If that's the case, we look for the monitor in the previously defined monitors
            for k in self.lava_monitors.values():
                if not k['lava_monitor'] is None and k['source'] == m['source'] and m['lava_var_name'] == k['lava_var_name']:
                    monitor = k['lava_monitor']
                    break
            if monitor == None: raise AssertionError(f"Something went wrong: the monitor for {m['source']} and {m['lava_var_name']} was not found")

        m['lava_monitor'] = monitor
        # Note that for the spike monitor additional variables this is not set,
        # which means that it will be skipped in the set_brian_monitor_values function
        m['process_name'] = getattr(process, 'name')

    # TODO: This might not be the best way to do this, but it ensures that no extra monitors are created
    # and that they are associated with the correct 'sources' only. Probably we could find a more efficient way to do this.
    for m in self.lava_monitors.values():
        # Only look at the right monitors
        if not process.name == m['source']:
            continue
        init_lava_monitor(m, num_steps)


def set_brian_monitor_values(self, process):
    """
    Transform Lava monitors to Brian monitor format.

    Parameters
    ----------
    process : `Process`
        Lava process that is provided with a monitor
    """

    # Iterate over Lava monitors
    for k, m in self.lava_monitors.items():

        # Only do this if the monitor refers to this process
        if not getattr(process,"name") == m['process_name']:
            continue

        # Get monitor variable
        var = m['var']

        # Define empty data variable
        # NOTE Lava monitors do not probe the inital values while Brian does
        #      We need to manually prepend the initial values to the monitored data
        init_data = None  # Contains initial values
        data = None  # Contains all other values

        # In case of a spike monitor, we need a more specific handling to get the time/spike indices
        if m['type'] == self.monitor_types['spike']:
            if var.name == 'i':
                # Get initial values from process
                init_raw = getattr(process, f'_{getattr(process,"name")}__spikespace').init
                i_init_data = np.nonzero(init_raw)[0]
                t_init_data = np.nonzero(init_raw)[0]*self.defaultclock.dt

                # Get the data from the monitor, for both i and t the data is the same
                raw = get_monitor_values(m)
                t_data = (np.nonzero(raw)[0] * self.defaultclock.dt)

                # Format it correctly
                t_data = np.concatenate((t_init_data, t_data))
                i_data = np.concatenate((i_init_data,np.nonzero(raw)[1]))
                count = np.bincount(i_data,minlength = m['var'].owner.source.N)
                
                # Store the monitor data into the device arrays
                self.arrays[var] = i_data
                self.arrays[var.owner.variables["t"]] = t_data
                self.arrays[var.owner.variables['count']] = count

                # Also set the N variable of the SpikeMonitor in order to be able to use indices properly
                self.arrays[var.owner.variables['N']] = np.array([len(t_data)])

                # Deal with the additional variables
                for additional_monitor in m['additional_var_monitors']:
                    # New variable to update in the arrays
                    add_var = additional_monitor['var']
                    data = get_monitor_values(additional_monitor)[:-2,:]

                    # Get initial values from process and prepare to concatenate
                    init_data = getattr(process, additional_monitor['lava_var_name']).init
                    init_data = np.expand_dims(init_data,0)
                    # Select only the correct time points for the spiking neurons
                    data = np.concatenate((init_data, data), axis=0)[np.nonzero(raw)[1],i_data]
                    self.arrays[add_var] = data

        # In case of a state monitor, just take the raw data from Lava
        if m['type'] == self.monitor_types['state']:

            # NOTE remove additional simulation steps from monitor to match Brian simulation
            data = get_monitor_values(m)[:-2,:]
            
            # Get initial values from process
            init_data = getattr(process, m['lava_var_name']).init

            if len(init_data) > 0:
                # Account for the extra dimension for the concatenation
                init_data = np.expand_dims(init_data,0)
                data = np.concatenate((init_data, data), axis=0)
        
            # Just formatting to make sure that we always have two dimensions
            # as used in brian for state monitor values (only for variables other than time)
            if var.name == 't':
                self.arrays[var] = np.squeeze(data)
                continue

            # Manage other variables
            if np.ndim(data) == 1:
                data = np.array([data])

            # If record is set to some specific indices, we only store the data at those indices
            # Note that this is very inefficient, but in Lava it's impossible to select indices
            # to record from a monitor. This is only to keep the results consistent with Brian.
            if isinstance(m['indices'],np.ndarray):
                # This case happens for variables that were not defined before calling the run() method
                if m['indices'].shape == (0,):
                    m['indices'] = np.arange(data.shape[1])
                data = data[:,m['indices']]

            self.arrays[var] = data

def get_monitor_values(monitor):
    """
    Get data from a Lava monitor.

    Parameters
    ----------
    monitor
        A monitor as defined in the device
    """

    # Define variables
    lava_monitor = monitor['lava_monitor']
    lava_var_name = monitor['lava_var_name']
    process_name = monitor['process_name']
    

    # Return lava monitor values
    data = np.array(lava_monitor.get_data()[process_name][lava_var_name])

    return data


def update_brian_class_attributes(self,processes):
    """
    Update class attributes of Brian objects.
    This allows the user to access attributes of Brian objects as they would in normal Brian.
    We do this by going through the processes and finding their corresponding Brian objects.
    Then we update the 'array' variable of the device with the new values so that when get_value gets called
    the correct values are displayed.
    Args:
        processes: List of Lava processes
    """
    self.logger.debug("Updating Brian class attributes..")
    # Iterate over processes
    for p in processes.values():
        obj = self.lava_objects[p.name]
        # We have to check for variables also in the objects contained in each of our objects (e.g. SynapticPathway inside Synapses)
        obj_to_check = [o for o in obj.contained_objects if hasattr(o,"variables")]
        obj_to_check.append(obj)
        for _obj in obj_to_check:
            for varname,var in _obj.variables.items():
                # SpikeQueue is a variable, but has no owner (and should not be accessed anyways)
                if not hasattr(var,'owner'):
                    continue
                p_varname = self.get_array_name(var,prefix = None)

                if hasattr(p,p_varname):
                    # Empty array variables cannot be handled by lava get() so we just set it to an empty array manually.
                    if getattr(p,p_varname).shape == (0,):
                        dtype = var.dtype
                        self.arrays[var] = np.array([],dtype=dtype)
                    else:
                        dtype = var.dtype
                        self.arrays[var] = np.array(getattr(p,p_varname).get(), dtype=dtype)

            if isinstance(_obj, Synapses):
                # Update the variables counting the number of synapses
                # TODO: Verify that this is not needed during the simulation
                # as right now we only update these variables AFTER running a simulation..
                _obj._update_synapse_numbers(len(_obj))
