import struct
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk
from external.properties import _ExternalPropertyContext, _read_property_value, _write_property_value, _parse_property_value, _property_address

_FFLAG_COLOR_MUTED = '#9aa0a6'
_FFLAG_COLOR_SUCCESS = '#65d98b'
_FFLAG_COLOR_WARNING = '#f2c94c'


_EXPLORER_INSTANCE_PROPERTY_SPECS = {
    'Position': {'type': 'vec3', 'at': ('Primitive', 'Position'), 'scope': 'primitive'},
    'Size': {'type': 'vec3', 'at': ('Primitive', 'Size'), 'scope': 'primitive'},
    'AssemblyLinearVelocity': {'type': 'vec3', 'at': ('Primitive', 'AssemblyLinearVelocity'), 'scope': 'primitive'},
    'AssemblyAngularVelocity': {'type': 'vec3', 'at': ('Primitive', 'AssemblyAngularVelocity'), 'scope': 'primitive'},
    'Anchored': {'type': 'flag', 'at': ('Primitive', 'Flags'), 'mask': ('PrimitiveFlags', 'Anchored'), 'scope': 'primitive'},
    'CanCollide': {'type': 'flag', 'at': ('Primitive', 'Flags'), 'mask': ('PrimitiveFlags', 'CanCollide'), 'scope': 'primitive'},
    'CanTouch': {'type': 'flag', 'at': ('Primitive', 'Flags'), 'mask': ('PrimitiveFlags', 'CanTouch'), 'scope': 'primitive'},
    'CanQuery': {'type': 'flag', 'at': ('Primitive', 'Flags'), 'mask': ('PrimitiveFlags', 'CanQuery'), 'scope': 'primitive'},
    'Transparency': {'type': 'float', 'at': ('BasePart', 'Transparency'), 'scope': 'instance'},
    'Reflectance': {'type': 'float', 'at': ('BasePart', 'Reflectance'), 'scope': 'instance'},
    'Massless': {'type': 'bool', 'at': ('BasePart', 'Massless'), 'scope': 'instance'},
    'CastShadow': {'type': 'bool', 'at': ('BasePart', 'CastShadow'), 'scope': 'instance'},
    'Locked': {'type': 'bool', 'at': ('BasePart', 'Locked'), 'scope': 'instance'},
    'Color': {'type': 'u8x3', 'at': ('BasePart', 'Color3'), 'scope': 'instance'},
    'Material': {'type': 'int', 'at': ('BasePart', 'Material'), 'scope': 'instance'},
}

class ExternalExplorerMixin:
    _EXTERNAL_EXPLORER_NODE_CAP = 60000
    _EXTERNAL_EXPLORER_TIME_CAP = 8.0
    _EXTERNAL_EXPLORER_PAGE_SIZE = 150
    _EXTERNAL_EXPLORER_RESULT_CAP = 2000
    _EXTERNAL_EXPLORER_RETRY_LIMIT = 30

    def _external_build_explorer_panel(self, parent):
        self._external_explorer_snapshot = {}
        self._external_explorer_root = 0
        self._external_explorer_pid = 0
        self._external_explorer_scan_active = False
        self._external_explorer_retry_count = 0
        self._external_explorer_loaded = set()
        self._external_explorer_item_data = {}
        self._external_explorer_detail_vars = {}
        self._external_explorer_hidden = set()
        self._external_explorer_view_target = 0
        self._external_explorer_action_active = False
        self._external_explorer_property_generation = 0
        self._external_explorer_property_specs = dict(_EXPLORER_INSTANCE_PROPERTY_SPECS)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)
        header = ttk.Frame(parent)
        header.grid(row=0, column=0, sticky='ew', pady=(0, 7))
        ttk.Label(header, text='Explorer', font=('Segoe UI Semibold', 10)).pack(side='left')
        self.external_explorer_status = ttk.Label(header, text='Waiting for a Roblox client', foreground=_FFLAG_COLOR_MUTED)
        self.external_explorer_status.pack(side='right')
        controls = ttk.Frame(parent)
        controls.grid(row=1, column=0, sticky='ew', pady=(0, 7))
        controls.columnconfigure(0, weight=1)
        self.external_explorer_search_var = tk.StringVar(value='')
        self.external_explorer_filter_var = tk.StringVar(value='All')
        self.external_explorer_search_entry = ttk.Entry(controls, textvariable=self.external_explorer_search_var)
        self.external_explorer_search_entry.grid(row=0, column=0, sticky='ew', padx=(0, 5))
        self.external_explorer_search_entry.insert(0, '')
        self.external_explorer_search_entry.bind('<Return>', lambda _event: self._external_explorer_render())
        self.external_explorer_filter = ttk.Combobox(controls, textvariable=self.external_explorer_filter_var, state='readonly', width=11, values=('All', 'Workspace', 'Models', 'Parts', 'Scripts', 'Folders', 'Remotes'))
        self.external_explorer_filter.grid(row=0, column=1, padx=(0, 5))
        self.external_explorer_filter.bind('<<ComboboxSelected>>', lambda _event: self._external_explorer_render())
        ttk.Button(controls, text='Search', command=self._external_explorer_render).grid(row=0, column=2, padx=(0, 5))
        self.external_explorer_refresh_button = ttk.Button(controls, text='Refresh', command=self._external_explorer_refresh)
        self.external_explorer_refresh_button.grid(row=0, column=3)
        body = ttk.PanedWindow(parent, orient='horizontal')
        body.grid(row=2, column=0, sticky='nsew')
        tree_host = ttk.Frame(body, padding=(0, 0, 5, 0))
        details_host = ttk.Frame(body, padding=(5, 0, 0, 0))
        tree_host.columnconfigure(0, weight=1)
        tree_host.rowconfigure(0, weight=1)
        details_host.columnconfigure(0, weight=1)
        details_host.rowconfigure(0, weight=1)
        body.add(tree_host, weight=3)
        body.add(details_host, weight=2)
        self.external_explorer_tree = ttk.Treeview(tree_host, columns=('class', 'children'), show='tree headings', selectmode='browse')
        self.external_explorer_tree.heading('#0', text='Instance')
        self.external_explorer_tree.heading('class', text='Class')
        self.external_explorer_tree.heading('children', text='Children')
        self.external_explorer_tree.column('#0', width=175, minwidth=100, stretch=True)
        self.external_explorer_tree.column('class', width=105, minwidth=72, stretch=True)
        self.external_explorer_tree.column('children', width=55, minwidth=48, stretch=False, anchor='center')
        self.external_explorer_tree.tag_configure('search', foreground=_FFLAG_COLOR_SUCCESS)
        self.external_explorer_tree.tag_configure('hidden', foreground='#8b929a')
        scrollbar = ttk.Scrollbar(tree_host, orient='vertical', command=self.external_explorer_tree.yview)
        self.external_explorer_tree.configure(yscrollcommand=scrollbar.set)
        self.external_explorer_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.external_explorer_tree.bind('<<TreeviewOpen>>', self._external_explorer_on_open)
        self.external_explorer_tree.bind('<<TreeviewSelect>>', self._external_explorer_on_select)
        self.external_explorer_tree.bind('<Double-1>', self._external_explorer_on_double_click, add='+')
        self.external_explorer_tree.bind('<Button-3>', self._external_explorer_context_menu)
        self.external_explorer_tree.bind('<Control-t>', lambda _event: self._external_explorer_run_action('teleport'))
        self.external_explorer_tree.bind('<KeyPress-v>', lambda _event: self._external_explorer_run_action('view'))
        self.external_explorer_tree.bind('<Delete>', lambda _event: self._external_explorer_run_action('delete'))
        self.external_explorer_notebook = ttk.Notebook(details_host)
        self.external_explorer_notebook.grid(row=0, column=0, sticky='nsew')
        selection_tab = ttk.Frame(self.external_explorer_notebook, padding=8)
        properties_tab = ttk.Frame(self.external_explorer_notebook, padding=8)
        self.external_explorer_notebook.add(selection_tab, text='Selection')
        self.external_explorer_notebook.add(properties_tab, text='Properties')
        details = ttk.LabelFrame(selection_tab, text='Selected Instance', padding=9)
        details.pack(fill='both', expand=True)
        fields = (('path', 'Path'), ('name', 'Name'), ('class', 'Class'), ('parent', 'Parent'), ('address', 'Address'), ('children', 'Children'))
        for index, (key, label) in enumerate(fields):
            ttk.Label(details, text=label, foreground=_FFLAG_COLOR_MUTED).grid(row=index * 2, column=0, sticky='w', pady=(2, 0))
            value = tk.StringVar(value='—')
            self._external_explorer_detail_vars[key] = value
            ttk.Label(details, textvariable=value, wraplength=230, justify='left').grid(row=index * 2 + 1, column=0, sticky='ew', pady=(0, 5))
        details.columnconfigure(0, weight=1)
        properties_tab.columnconfigure(0, weight=1)
        properties_tab.rowconfigure(1, weight=1)
        self.external_explorer_property_status_var = tk.StringVar(value='Select a Part to inspect its properties.')
        ttk.Label(properties_tab, textvariable=self.external_explorer_property_status_var, foreground=_FFLAG_COLOR_MUTED, wraplength=260).grid(row=0, column=0, sticky='ew', pady=(0, 6))
        property_host = ttk.Frame(properties_tab)
        property_host.grid(row=1, column=0, sticky='nsew')
        property_host.columnconfigure(0, weight=1)
        property_host.rowconfigure(0, weight=1)
        self.external_explorer_property_tree = ttk.Treeview(property_host, columns=('value',), show='tree headings', selectmode='browse', height=12)
        self.external_explorer_property_tree.heading('#0', text='Property')
        self.external_explorer_property_tree.heading('value', text='Value')
        self.external_explorer_property_tree.column('#0', width=130, minwidth=90, stretch=True)
        self.external_explorer_property_tree.column('value', width=135, minwidth=100, stretch=True)
        property_scroll = ttk.Scrollbar(property_host, orient='vertical', command=self.external_explorer_property_tree.yview)
        self.external_explorer_property_tree.configure(yscrollcommand=property_scroll.set)
        self.external_explorer_property_tree.grid(row=0, column=0, sticky='nsew')
        property_scroll.grid(row=0, column=1, sticky='ns')
        self.external_explorer_property_tree.bind('<<TreeviewSelect>>', self._external_explorer_property_on_select)
        self.external_explorer_property_tree.bind('<Double-1>', lambda _event: self.external_explorer_property_entry.focus_set())
        editor = ttk.LabelFrame(properties_tab, text='Edit selected property', padding=7)
        editor.grid(row=2, column=0, sticky='ew', pady=(7, 0))
        editor.columnconfigure(0, weight=1)
        self.external_explorer_property_value_var = tk.StringVar(value='')
        self.external_explorer_property_entry = ttk.Entry(editor, textvariable=self.external_explorer_property_value_var)
        self.external_explorer_property_entry.grid(row=0, column=0, sticky='ew', pady=(0, 6))
        self.external_explorer_property_entry.bind('<Return>', lambda _event: self._external_explorer_apply_instance_property())
        property_buttons = ttk.Frame(editor)
        property_buttons.grid(row=1, column=0, sticky='ew')
        property_buttons.columnconfigure(0, weight=1)
        property_buttons.columnconfigure(1, weight=1)
        self.external_explorer_property_apply_button = ttk.Button(property_buttons, text='Apply', command=self._external_explorer_apply_instance_property)
        self.external_explorer_property_apply_button.grid(row=0, column=0, sticky='ew', padx=(0, 3))
        ttk.Button(property_buttons, text='Refresh', command=self._external_explorer_refresh_instance_properties).grid(row=0, column=1, sticky='ew', padx=(3, 0))
        actions = ttk.Frame(details_host)
        actions.grid(row=1, column=0, sticky='ew', pady=(7, 0))
        for column in range(3):
            actions.columnconfigure(column, weight=1)
        action_buttons = (
            ('Copy Path', lambda: self._external_explorer_copy('path')),
            ('Copy Name', lambda: self._external_explorer_copy('name')),
            ('Copy Class', lambda: self._external_explorer_copy('class')),
            ('Teleport', lambda: self._external_explorer_run_action('teleport')),
            ('View', lambda: self._external_explorer_run_action('view')),
            ('Delete', lambda: self._external_explorer_run_action('delete'))
        )
        for index, (label, command) in enumerate(action_buttons):
            ttk.Button(actions, text=label, command=command).grid(row=index // 3, column=index % 3, sticky='ew', padx=2, pady=2)
        self._external_explorer_status('Attach a Roblox client in Clients, then refresh.')

    @staticmethod
    def _external_explorer_format_property_value(value):
        if isinstance(value, bool):
            return 'true' if value else 'false'
        if isinstance(value, (list, tuple)):
            return ', '.join(f'{float(item):.5g}' if isinstance(item, (int, float)) else str(item) for item in value)
        if isinstance(value, float):
            return f'{value:.6g}'
        return str(value)

    def _external_explorer_clear_instance_properties(self, status='Select a Part to inspect its properties.'):
        self._external_explorer_property_generation += 1
        tree = getattr(self, 'external_explorer_property_tree', None)
        if tree is not None:
            for item in tree.get_children(''):
                tree.delete(item)
        if hasattr(self, 'external_explorer_property_status_var'):
            self.external_explorer_property_status_var.set(status)
        if hasattr(self, 'external_explorer_property_value_var'):
            self.external_explorer_property_value_var.set('')

    def _external_explorer_load_instance_properties(self, address):
        self._external_explorer_property_generation += 1
        generation = self._external_explorer_property_generation
        for item in self.external_explorer_property_tree.get_children(''):
            self.external_explorer_property_tree.delete(item)
        self.external_explorer_property_value_var.set('')
        pid = int(getattr(self, 'fflag_pid', 0) or 0)
        cls = str(self._external_explorer_snapshot.get(int(address), {}).get('cls', ''))
        if not self._external_explorer_is_basepart_class(cls):
            self.external_explorer_property_status_var.set('Properties are available for BasePart instances. Select a Part, MeshPart, UnionOperation or Seat.')
            return
        if not pid or pid != int(getattr(self, '_external_explorer_pid', 0) or 0):
            self.external_explorer_property_status_var.set('Attach a client and refresh the Explorer first.')
            return
        self.external_explorer_property_status_var.set('Reading selected Part properties…')
        def worker():
            values = []
            error_text = ''
            try:
                context = self._external_explorer_action_context(pid)
                live_class = context.class_name(int(address))
                if not self._external_explorer_is_basepart_class(live_class):
                    raise RuntimeError('The selected instance is no longer a BasePart.')
                primitive = self._external_explorer_part_primitive(context, address)
                if not primitive:
                    raise RuntimeError('The selected Part has no readable Primitive.')
                for key, spec in self._external_explorer_property_specs.items():
                    try:
                        owner = primitive if spec['scope'] == 'primitive' else int(address)
                        value = _read_property_value(spec, _property_address(spec, owner, context), context)
                        values.append((key, self._external_explorer_format_property_value(value)))
                    except Exception:
                        continue
                if not values:
                    raise RuntimeError('No supported properties were found for this Part and Roblox build.')
            except Exception as error:
                error_text = str(error)
            try:
                self.after(0, self._external_explorer_instance_properties_loaded, generation, int(address), pid, values, error_text)
            except Exception:
                pass
        threading.Thread(target=worker, daemon=True, name='RoUtilsExplorerPropertiesRead').start()

    @staticmethod
    def _external_explorer_is_basepart_class(class_name):
        name = str(class_name or '')
        return 'Part' in name or name in ('UnionOperation', 'Seat', 'VehicleSeat', 'SkateboardPlatform')

    def _external_explorer_instance_properties_loaded(self, generation, address, pid, values, error_text):
        if generation != self._external_explorer_property_generation:
            return
        selected = self._external_explorer_selected_info()
        if not selected or int(selected[0]) != int(address) or int(getattr(self, 'fflag_pid', 0) or 0) != int(pid):
            return
        tree = self.external_explorer_property_tree
        for item in tree.get_children(''):
            tree.delete(item)
        if error_text:
            self.external_explorer_property_status_var.set(error_text)
            return
        self.external_explorer_property_value_var.set('')
        for key, value in values:
            tree.insert('', 'end', iid=key, text=key, values=(value,))
        self.external_explorer_property_status_var.set(f'{len(values)} properties · select a row, edit the value and Apply.')

    def _external_explorer_property_on_select(self, event=None):
        selection = self.external_explorer_property_tree.selection()
        if not selection:
            self.external_explorer_property_value_var.set('')
            return
        key = selection[0]
        item = self.external_explorer_property_tree.item(key)
        values = item.get('values', ())
        self.external_explorer_property_value_var.set(str(values[0]) if values else '')

    def _external_explorer_refresh_instance_properties(self):
        selected = self._external_explorer_selected_info()
        if not selected:
            self._external_explorer_clear_instance_properties()
            return
        self._external_explorer_load_instance_properties(selected[0])

    def _external_explorer_apply_instance_property(self):
        selected = self._external_explorer_selected_info()
        if not selected:
            self.external_explorer_property_status_var.set('Select a Part in the Explorer first.')
            return
        selection = self.external_explorer_property_tree.selection()
        if not selection:
            self.external_explorer_property_status_var.set('Select a property row first.')
            return
        key = selection[0]
        spec = self._external_explorer_property_specs.get(key)
        if not spec:
            return
        raw_value = self.external_explorer_property_value_var.get()
        try:
            value = _parse_property_value(spec, raw_value)
            if key in ('Transparency', 'Reflectance') and not 0.0 <= float(value) <= 1.0:
                raise ValueError(f'{key} must be between 0 and 1.')
            if key == 'Size' and any(float(component) <= 0 for component in value):
                raise ValueError('Size components must be greater than zero.')
            if key == 'Color' and any(float(component) != int(component) or int(component) < 0 or int(component) > 255 for component in value):
                raise ValueError('Color components must be whole numbers between 0 and 255.')
        except Exception as error:
            self.external_explorer_property_status_var.set(str(error))
            return
        address = int(selected[0])
        pid = int(getattr(self, 'fflag_pid', 0) or 0)
        if not pid or pid != int(getattr(self, '_external_explorer_pid', 0) or 0):
            self.external_explorer_property_status_var.set('Refresh the Explorer after attaching a client.')
            return
        if getattr(self, '_external_explorer_property_apply_active', False):
            return
        self._external_explorer_property_apply_active = True
        self.external_explorer_property_apply_button.configure(state='disabled')
        self.external_explorer_property_status_var.set(f'Applying {key}…')
        def worker():
            error_text = ''
            try:
                context = self._external_explorer_action_context(pid)
                live_class = context.class_name(address)
                if not self._external_explorer_is_basepart_class(live_class):
                    raise RuntimeError('The selected instance is no longer a BasePart.')
                primitive = self._external_explorer_part_primitive(context, address)
                if not primitive:
                    raise RuntimeError('The selected Part has no Primitive.')
                owner = primitive if spec['scope'] == 'primitive' else address
                _write_property_value(spec, _property_address(spec, owner, context), value, context)
                verify = _read_property_value(spec, _property_address(spec, owner, context), context)
                if spec['type'] == 'vec3':
                    if any(abs(float(a) - float(b)) > 0.02 for a, b in zip(value, verify)):
                        raise RuntimeError(f'{key} write could not be verified.')
                elif spec['type'] in ('bool', 'flag'):
                    if bool(value) != bool(verify):
                        raise RuntimeError(f'{key} write could not be verified.')
                elif spec['type'] == 'u8x3':
                    if list(value) != list(verify):
                        raise RuntimeError(f'{key} write could not be verified.')
                elif abs(float(value) - float(verify)) > 0.001:
                    raise RuntimeError(f'{key} write could not be verified.')
            except Exception as error:
                error_text = str(error)
            try:
                self.after(0, self._external_explorer_instance_property_applied, address, pid, key, error_text)
            except Exception:
                self._external_explorer_property_apply_active = False
        threading.Thread(target=worker, daemon=True, name='RoUtilsExplorerPropertyWrite').start()

    def _external_explorer_instance_property_applied(self, address, pid, key, error_text):
        self._external_explorer_property_apply_active = False
        try:
            self.external_explorer_property_apply_button.configure(state='normal')
        except Exception:
            pass
        if error_text:
            self.external_explorer_property_status_var.set(error_text)
            return
        self.external_explorer_property_status_var.set(f'{key} applied successfully.')
        self._external_explorer_load_instance_properties(address)

    def _external_explorer_status(self, text, color=None):
        label = getattr(self, 'external_explorer_status', None)
        if label is None:
            return
        try:
            label.configure(text=str(text), foreground=color or _FFLAG_COLOR_MUTED)
        except Exception:
            pass

    def _external_explorer_refresh(self, _retry=False):
        if getattr(self, 'external_explorer_tree', None) is None:
            return
        if not _retry:
            self._external_explorer_retry_count = 0
        if getattr(self, '_external_explorer_scan_active', False):
            return
        engine = getattr(self, 'fflag_engine', None)
        pid = int(getattr(self, 'fflag_pid', 0) or 0)
        if not engine or not engine.handle or not pid or int(getattr(engine, 'pid', 0) or 0) != pid:
            self._external_explorer_status('Attach a Roblox client in Clients first.', _FFLAG_COLOR_WARNING)
            return
        self._external_explorer_scan_active = True
        try:
            self.external_explorer_refresh_button.configure(state='disabled', text='Scanning…')
        except Exception:
            pass
        self._external_explorer_status('Scanning live DataModel…')
        self._external_explorer_clear_tree()
        self._external_explorer_item_data.clear()
        self._external_explorer_loaded.clear()

        def worker():
            snapshot = {}
            root = 0
            partial = False
            error_text = ''
            try:
                if int(getattr(engine, 'pid', 0) or 0) != pid or not engine.handle:
                    raise RuntimeError('The selected Roblox client changed. Select it again.')
                offsets_data = self._external_offsets_for_client(pid)
                context = _ExternalPropertyContext(self, offsets_data)
                root = context.target('dm')
                if not root:
                    raise RuntimeError('The Roblox DataModel is not available yet.')
                try:
                    loaded_offset = context.off('DataModel', 'GameLoaded')
                    game_loaded = context.read_bytes(root + loaded_offset, 1)[0] != 0
                except Exception:
                    game_loaded = True
                if not game_loaded:
                    raise RuntimeError('The Roblox game session is loading.')
                stack = [(root, 0)]
                started = time.monotonic()
                visited = 0
                while stack and len(snapshot) < self._EXTERNAL_EXPLORER_NODE_CAP:
                    if (visited & 255) == 0 and time.monotonic() - started >= self._EXTERNAL_EXPLORER_TIME_CAP:
                        partial = True
                        break
                    address, parent = stack.pop()
                    visited += 1
                    if address in snapshot or not context.sane(address):
                        continue
                    try:
                        name = context.instance_name(address) or ('Game' if address == root else 'Unnamed')
                    except Exception:
                        name = 'Game' if address == root else 'Unnamed'
                    try:
                        class_name = context.class_name(address) or 'Instance'
                    except Exception:
                        class_name = 'Instance'
                    try:
                        children = context.children(address)
                    except Exception:
                        children = []
                    snapshot[address] = {'name': str(name)[:120], 'cls': str(class_name)[:64], 'parent': parent, 'kids': children}
                    for child in reversed(children):
                        if child and child not in snapshot:
                            stack.append((child, address))
                    if (len(snapshot) & 1023) == 0:
                        try:
                            self.after(0, self._external_explorer_status, f'Scanning… {len(snapshot):,} instances')
                        except Exception:
                            pass
                if stack:
                    partial = True
                if not snapshot:
                    raise RuntimeError('The DataModel could not be read from this client.')
            except Exception as error:
                error_text = str(error)
            try:
                self.after(0, self._external_explorer_refresh_finished, pid, root, snapshot, partial, error_text)
            except Exception:
                self._external_explorer_scan_active = False

        threading.Thread(target=worker, daemon=True, name='RoUtilsExternalExplorer').start()

    def _external_explorer_refresh_finished(self, pid, root, snapshot, partial, error_text=''):
        self._external_explorer_scan_active = False
        try:
            self.external_explorer_refresh_button.configure(state='normal', text='Refresh')
        except Exception:
            pass
        engine = getattr(self, 'fflag_engine', None)
        if int(getattr(self, 'fflag_pid', 0) or 0) != int(pid) or not engine or not engine.handle or int(getattr(engine, 'pid', 0) or 0) != int(pid):
            self._external_explorer_status('Client changed during scan.', _FFLAG_COLOR_WARNING)
            current_pid = int(getattr(self, 'fflag_pid', 0) or 0)
            if current_pid and engine and engine.handle and int(getattr(engine, 'pid', 0) or 0) == current_pid:
                self.after(450, self._external_explorer_refresh)
            return
        if error_text:
            self._external_explorer_snapshot = {}
            self._external_explorer_root = 0
            waiting_for_game = 'DataModel is not available yet' in error_text or 'game session is loading' in error_text
            if waiting_for_game and self._external_explorer_retry_count < self._EXTERNAL_EXPLORER_RETRY_LIMIT:
                self._external_explorer_retry_count += 1
                attempt = self._external_explorer_retry_count
                self._external_explorer_status(f'Waiting for game session… retry {attempt}/{self._EXTERNAL_EXPLORER_RETRY_LIMIT}', _FFLAG_COLOR_WARNING)
                self.after(1800, lambda: self._external_explorer_refresh(_retry=True))
            else:
                self._external_explorer_status(error_text, _FFLAG_COLOR_WARNING)
            return
        self._external_explorer_retry_count = 0
        self._external_explorer_snapshot = snapshot
        self._external_explorer_root = root
        self._external_explorer_pid = int(pid)
        self._external_explorer_loaded.clear()
        total = len(snapshot)
        if partial:
            self._external_explorer_status(f'Partial snapshot · {total:,} instances', _FFLAG_COLOR_WARNING)
        else:
            self._external_explorer_status(f'Live · {total:,} instances', _FFLAG_COLOR_SUCCESS)
        self._external_explorer_render()

    def _external_explorer_client_disconnected(self):
        self._external_explorer_snapshot = {}
        self._external_explorer_root = 0
        self._external_explorer_pid = 0
        self._external_explorer_loaded.clear()
        self._external_explorer_item_data.clear()
        tree = getattr(self, 'external_explorer_tree', None)
        if tree is not None:
            self._external_explorer_clear_tree()
        self._external_explorer_clear_details()
        self._external_explorer_status('Waiting for a Roblox client')

    def _external_explorer_clear_tree(self):
        tree = getattr(self, 'external_explorer_tree', None)
        if tree is None:
            return
        items = tree.get_children('')
        if items:
            tree.delete(*items)

    def _external_explorer_iid(self, address):
        return f'node_{int(address):x}'

    def _external_explorer_insert_node(self, parent_iid, address, tag=()):
        snapshot = getattr(self, '_external_explorer_snapshot', {})
        item = snapshot.get(address)
        if not item:
            return
        iid = self._external_explorer_iid(address)
        if self.external_explorer_tree.exists(iid):
            return
        label = self._external_explorer_label(item['name'], item['cls'], address in self._external_explorer_hidden)
        node_tags = tuple(tag) + (('hidden',) if address in self._external_explorer_hidden else ())
        self.external_explorer_tree.insert(parent_iid, 'end', iid=iid, text=label, values=(item['cls'], len(item['kids'])), tags=node_tags)
        self._external_explorer_item_data[iid] = {'kind': 'node', 'address': address}
        if item['kids']:
            dummy = f'dummy_{int(address):x}'
            self.external_explorer_tree.insert(iid, 'end', iid=dummy, text='…', values=('', ''))
            self._external_explorer_item_data[dummy] = {'kind': 'dummy', 'address': address}

    def _external_explorer_insert_children(self, parent_iid, parent_address, start):
        snapshot = getattr(self, '_external_explorer_snapshot', {})
        parent = snapshot.get(parent_address)
        if not parent:
            return
        children = parent['kids']
        end = min(len(children), start + self._EXTERNAL_EXPLORER_PAGE_SIZE)
        for child in children[start:end]:
            self._external_explorer_insert_node(parent_iid, child)
        if end < len(children):
            more_iid = f'more_{int(parent_address):x}_{end}'
            if not self.external_explorer_tree.exists(more_iid):
                self.external_explorer_tree.insert(parent_iid, 'end', iid=more_iid, text=f'Load more… ({len(children) - end})', values=('', ''))
                self._external_explorer_item_data[more_iid] = {'kind': 'more', 'parent_iid': parent_iid, 'address': parent_address, 'offset': end}

    def _external_explorer_on_open(self, event=None):
        tree = self.external_explorer_tree
        iid = tree.focus()
        info = self._external_explorer_item_data.get(iid, {})
        if info.get('kind') != 'node' or iid in self._external_explorer_loaded:
            return
        for child_iid in tree.get_children(iid):
            child_info = self._external_explorer_item_data.get(child_iid, {})
            if child_info.get('kind') == 'dummy':
                tree.delete(child_iid)
                self._external_explorer_item_data.pop(child_iid, None)
        self._external_explorer_loaded.add(iid)
        self._external_explorer_insert_children(iid, info['address'], 0)

    def _external_explorer_on_double_click(self, event):
        tree = self.external_explorer_tree
        iid = tree.identify_row(event.y)
        info = self._external_explorer_item_data.get(iid, {})
        if info.get('kind') != 'more':
            return None
        tree.delete(iid)
        self._external_explorer_item_data.pop(iid, None)
        self._external_explorer_insert_children(info['parent_iid'], info['address'], info['offset'])
        return 'break'

    def _external_explorer_path(self, address):
        snapshot = getattr(self, '_external_explorer_snapshot', {})
        parts = []
        current = address
        for _ in range(64):
            item = snapshot.get(current)
            if not item:
                break
            parts.append(item['name'])
            current = item['parent']
            if not current:
                break
        return '.'.join(reversed(parts))

    def _external_explorer_matches_filter(self, class_name, selected_filter):
        cls = str(class_name or '')
        if selected_filter == 'Scripts':
            return 'Script' in cls
        if selected_filter == 'Models':
            return cls == 'Model'
        if selected_filter == 'Parts':
            return 'Part' in cls or cls in ('UnionOperation', 'Terrain', 'Seat', 'VehicleSeat', 'SpawnLocation')
        if selected_filter == 'Folders':
            return cls == 'Folder'
        if selected_filter == 'Remotes':
            return cls in ('RemoteEvent', 'RemoteFunction', 'BindableEvent', 'BindableFunction')
        return True

    def _external_explorer_render(self):
        tree = getattr(self, 'external_explorer_tree', None)
        if tree is None:
            return
        self._external_explorer_clear_tree()
        self._external_explorer_item_data.clear()
        snapshot = getattr(self, '_external_explorer_snapshot', {})
        root = getattr(self, '_external_explorer_root', 0)
        if not snapshot or root not in snapshot:
            self._external_explorer_clear_details()
            return
        query = self.external_explorer_search_var.get().strip().casefold()
        selected_filter = self.external_explorer_filter_var.get()
        if query or selected_filter != 'All':
            root_iid = 'search_results'
            matches = []
            for address, item in snapshot.items():
                if address == root or not self._external_explorer_matches_filter(item['cls'], selected_filter):
                    continue
                if selected_filter == 'Workspace' and 'Workspace' not in self._external_explorer_path(address).split('.'):
                    continue
                if query and query not in item['name'].casefold() and query not in item['cls'].casefold():
                    continue
                matches.append(address)
                if len(matches) >= self._EXTERNAL_EXPLORER_RESULT_CAP:
                    break
            tree.insert('', 'end', iid=root_iid, text=f'Search Results ({len(matches):,})', values=('Results', len(matches)), open=True)
            self._external_explorer_item_data[root_iid] = {'kind': 'group'}
            for address in matches[:400]:
                self._external_explorer_insert_node(root_iid, address, ('search',))
            if len(matches) > 400:
                more_iid = 'search_more'
                tree.insert(root_iid, 'end', iid=more_iid, text=f'{len(matches) - 400:,} more matches · refine search', values=('', ''))
                self._external_explorer_item_data[more_iid] = {'kind': 'empty'}
            if not matches:
                empty_iid = 'no_results'
                tree.insert(root_iid, 'end', iid=empty_iid, text='No matches', values=('', ''))
                self._external_explorer_item_data[empty_iid] = {'kind': 'empty'}
            self._external_explorer_clear_details()
            return
        root_iid = self._external_explorer_iid(root)
        self._external_explorer_loaded.add(root_iid)
        item = snapshot[root]
        tree.insert('', 'end', iid=root_iid, text=item['name'] or 'Game', values=(item['cls'], len(item['kids'])), open=True)
        self._external_explorer_item_data[root_iid] = {'kind': 'node', 'address': root}
        self._external_explorer_insert_children(root_iid, root, 0)
        self._external_explorer_clear_details()

    def _external_explorer_clear_details(self):
        for value in getattr(self, '_external_explorer_detail_vars', {}).values():
            value.set('—')
        if hasattr(self, 'external_explorer_property_tree'):
            self._external_explorer_clear_instance_properties()

    def _external_explorer_on_select(self, event=None):
        tree = self.external_explorer_tree
        selection = tree.selection()
        if not selection:
            self._external_explorer_clear_details()
            return
        info = self._external_explorer_item_data.get(selection[0], {})
        if info.get('kind') != 'node':
            self._external_explorer_clear_details()
            return
        address = info['address']
        item = self._external_explorer_snapshot.get(address)
        if not item:
            self._external_explorer_clear_details()
            return
        parent = self._external_explorer_snapshot.get(item['parent'], {})
        values = {
            'path': self._external_explorer_path(address),
            'name': item['name'],
            'class': item['cls'],
            'parent': parent.get('name', 'None') if item['parent'] else 'None',
            'address': f'0x{address:X}',
            'children': str(len(item['kids']))
        }
        for key, value in values.items():
            self._external_explorer_detail_vars[key].set(value)
        self._external_explorer_load_instance_properties(address)

    def _external_explorer_copy(self, key):
        value = self._external_explorer_detail_vars.get(key)
        if value is None:
            return
        text = value.get()
        if not text or text == '—':
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
        except Exception:
            pass

    @staticmethod
    def _external_explorer_label(name, class_name, hidden=False):
        cls = str(class_name or '')
        if hidden:
            icon = '◌'
            suffix = '  [Hidden]'
        elif cls == 'Workspace':
            icon = '◉'
            suffix = ''
        elif cls == 'Model':
            icon = '◇'
            suffix = ''
        elif cls == 'Folder':
            icon = '▰'
            suffix = ''
        elif 'Part' in cls or cls in ('UnionOperation', 'Seat', 'VehicleSeat', 'SpawnLocation'):
            icon = '▣'
            suffix = ''
        elif 'Script' in cls:
            icon = '▤'
            suffix = ''
        else:
            icon = '•'
            suffix = ''
        return f'{icon}  {name}{suffix}'

    def _external_explorer_selected_info(self, event=None):
        tree = getattr(self, 'external_explorer_tree', None)
        if tree is None:
            return None
        if event is not None:
            iid = tree.identify_row(event.y)
            if iid:
                tree.selection_set(iid)
                tree.focus(iid)
                self._external_explorer_on_select()
        selection = tree.selection()
        if not selection:
            return None
        info = self._external_explorer_item_data.get(selection[0], {})
        if info.get('kind') != 'node':
            return None
        address = int(info.get('address', 0) or 0)
        item = self._external_explorer_snapshot.get(address)
        if not address or not item:
            return None
        return address, item

    def _external_explorer_context_menu(self, event):
        selected = self._external_explorer_selected_info(event)
        if not selected:
            return 'break'
        address, item = selected
        cls = str(item.get('cls', ''))
        menu = tk.Menu(self.external_explorer_tree, tearoff=False)
        menu.add_command(label='Teleport To\tCtrl+T', command=lambda: self._external_explorer_run_action('teleport'))
        menu.add_command(label='View\tV', command=lambda: self._external_explorer_run_action('view'))
        menu.add_command(label='Stop Viewing', command=lambda: self._external_explorer_run_action('stop_view'))
        menu.add_separator()
        can_edit = 'Part' in cls or cls in ('UnionOperation', 'Seat', 'VehicleSeat', 'SpawnLocation', 'Model')
        menu.add_command(label='Delete Locally\tDel', command=lambda: self._external_explorer_run_action('delete'), state='normal' if can_edit else 'disabled')
        menu.add_separator()
        menu.add_command(label='Properties', command=lambda: self.external_explorer_notebook.select(1))
        menu.add_separator()
        menu.add_command(label='Copy Path', command=lambda: self._external_explorer_copy('path'))
        menu.add_command(label='Copy Name', command=lambda: self._external_explorer_copy('name'))
        menu.add_command(label='Copy Class', command=lambda: self._external_explorer_copy('class'))
        menu.add_command(label='Copy Address', command=lambda: self._external_explorer_copy('address'))
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
        return 'break'

    def _external_explorer_action_context(self, pid):
        engine = getattr(self, 'fflag_engine', None)
        if not engine or not engine.handle or int(getattr(engine, 'pid', 0) or 0) != int(pid):
            raise RuntimeError('The selected Roblox client is no longer attached.')
        if int(getattr(self, 'fflag_pid', 0) or 0) != int(pid):
            raise RuntimeError('The selected Roblox client changed. Select it again.')
        offsets_data = self._external_offsets_for_client(pid)
        return _ExternalPropertyContext(self, offsets_data)

    @staticmethod
    def _external_explorer_part_primitive(context, address):
        class_name = str(context.class_name(int(address)) or '')
        if not ExternalExplorerMixin._external_explorer_is_basepart_class(class_name):
            return 0
        primitive_offset = context.off('BasePart', 'Primitive')
        primitive = context.read_pointer(int(address) + primitive_offset)
        if not context.sane(primitive):
            return 0
        return primitive

    def _external_explorer_find_parts(self, context, address, max_nodes=2500):
        found = []
        stack = [int(address)]
        visited = set()
        while stack and len(visited) < max_nodes:
            current = stack.pop()
            if current in visited or not context.sane(current):
                continue
            visited.add(current)
            try:
                primitive = self._external_explorer_part_primitive(context, current)
                if primitive:
                    found.append((current, primitive))
                    continue
            except Exception:
                pass
            try:
                children = context.children(current)
            except Exception:
                children = []
            stack.extend(reversed(children))
        return found

    def _external_explorer_write_vector(self, context, primitive, field, values):
        offset = context.off('Primitive', field)
        context.write_bytes(primitive + offset, struct.pack('<3f', *[float(value) for value in values]))

    def _external_explorer_apply_action(self, action, address, pid):
        context = self._external_explorer_action_context(pid)
        if action in ('teleport', 'view'):
            parts = self._external_explorer_find_parts(context, address, max_nodes=3500)
            if not parts:
                raise RuntimeError('No BasePart was found in the selected instance.')
            target_part, target_primitive = parts[0]
        if action == 'teleport':
            position_offset = context.off('Primitive', 'Position')
            target_position = struct.unpack('<3f', context.read_bytes(target_primitive + position_offset, 12))
            local_part = context.target('part')
            local_primitive = self._external_explorer_part_primitive(context, local_part)
            if not local_primitive:
                raise RuntimeError('The LocalPlayer HumanoidRootPart is unavailable.')
            destination = (target_position[0], target_position[1] + 4.5, target_position[2])
            self._external_explorer_write_vector(context, local_primitive, 'Position', destination)
            try:
                self._external_explorer_write_vector(context, local_primitive, 'AssemblyLinearVelocity', (0.0, 0.0, 0.0))
            except Exception:
                pass
            return f'Teleported LocalPlayer near {self._external_explorer_snapshot.get(address, {}).get("name", "selected object")}.'
        if action == 'view':
            camera = context.target('camera')
            subject_offset = context.off('Camera', 'CameraSubject')
            type_offset = context.off('Camera', 'CameraType')
            context.write_bytes(camera + subject_offset, struct.pack('<Q', target_part))
            context.write_bytes(camera + type_offset, struct.pack('<i', 4))
            self._external_explorer_view_target = int(address)
            return f'Camera is now following {self._external_explorer_snapshot.get(address, {}).get("name", "selected object")}.'
        if action == 'stop_view':
            camera = context.target('camera')
            humanoid = context.target('humanoid')
            context.write_bytes(camera + context.off('Camera', 'CameraSubject'), struct.pack('<Q', humanoid))
            context.write_bytes(camera + context.off('Camera', 'CameraType'), struct.pack('<i', 0))
            self._external_explorer_view_target = 0
            return 'Camera follow stopped.'
        if action == 'delete':
            parts = self._external_explorer_find_parts(context, address, max_nodes=5000)
            if not parts:
                raise RuntimeError('No BasePart objects were found. Delete Locally supports Parts and Models.')
            transparency_offset = context.off('BasePart', 'Transparency')
            changed = 0
            for part, primitive in parts:
                try:
                    context.write_bytes(part + transparency_offset, struct.pack('<f', 1.0))
                    try:
                        local_transparency = context.off('BasePart', 'LocalTransparencyModifier')
                        context.write_bytes(part + local_transparency, struct.pack('<f', 1.0))
                    except Exception:
                        pass
                    try:
                        flags_offset = context.off('Primitive', 'Flags')
                        flags_address = primitive + flags_offset
                        flags = context.read_bytes(flags_address, 1)[0]
                        for flag_name in ('CanCollide', 'CanTouch', 'CanQuery'):
                            try:
                                mask = context.off('PrimitiveFlags', flag_name)
                                flags &= (~mask) & 255
                            except Exception:
                                pass
                        context.write_bytes(flags_address, bytes((flags,)))
                    except Exception:
                        pass
                    changed += 1
                except Exception:
                    continue
            if not changed:
                raise RuntimeError('The selected instance could not be hidden locally.')
            self._external_explorer_hidden.add(int(address))
            self._external_explorer_hidden.update(part for part, _primitive in parts)
            return f'Deleted locally: hidden {changed} part(s). The server may restore them.'
        raise RuntimeError('Unknown Explorer action.')

    def _external_explorer_action_finished(self, action, result, error_text):
        self._external_explorer_action_active = False
        if error_text:
            self._external_explorer_status(error_text, _FFLAG_COLOR_WARNING)
            try:
                messagebox.showwarning('External Explorer', error_text, parent=self)
            except Exception:
                pass
            return
        self._external_explorer_status(result, _FFLAG_COLOR_SUCCESS)
        if action == 'delete':
            for address in self._external_explorer_hidden:
                iid = self._external_explorer_iid(address)
                if self.external_explorer_tree.exists(iid):
                    item = self._external_explorer_snapshot.get(address, {})
                    self.external_explorer_tree.item(iid, text=self._external_explorer_label(item.get('name', 'Instance'), item.get('cls', ''), True), tags=('hidden',))

    def _external_explorer_run_action(self, action):
        selected = self._external_explorer_selected_info()
        if action not in ('stop_view',) and not selected:
            self._external_explorer_status('Select an instance in the tree first.', _FFLAG_COLOR_WARNING)
            return
        if getattr(self, '_external_explorer_action_active', False):
            return
        if action == 'delete':
            name = selected[1].get('name', 'selected instance')
            confirmed = messagebox.askyesno('Delete Locally', f'Hide {name} on this client? This does not delete server data and the game may restore the object.', parent=self)
            if not confirmed:
                return
        address = selected[0] if selected else 0
        pid = int(getattr(self, 'fflag_pid', 0) or 0)
        if not pid or pid != int(getattr(self, '_external_explorer_pid', 0) or 0):
            self._external_explorer_status('Refresh the Explorer after attaching a Roblox client.', _FFLAG_COLOR_WARNING)
            return
        self._external_explorer_action_active = True
        self._external_explorer_status('Applying action…')

        def worker():
            try:
                result = self._external_explorer_apply_action(action, address, pid)
                error_text = ''
            except Exception as error:
                result = ''
                error_text = str(error)
            try:
                self.after(0, self._external_explorer_action_finished, action, result, error_text)
            except Exception:
                self._external_explorer_action_active = False

        threading.Thread(target=worker, daemon=True, name='RoUtilsExplorerAction').start()

