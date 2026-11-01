import struct
import threading
import time
import tkinter as tk
from tkinter import ttk
from external.properties import _ExternalPropertyContext, _read_property_value, _property_address

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
        self._external_explorer_detail_vars = {key: tk.StringVar(value='—') for key in ('path', 'name', 'class', 'parent', 'address', 'children')}
        self._external_explorer_workspace = 0
        self._external_explorer_auto_refresh_job = None
        self._external_explorer_auto_refresh_active = False
        self._external_explorer_last_property_poll = 0.0
        self._external_explorer_property_generation = 0
        self._external_explorer_property_specs = dict(_EXPLORER_INSTANCE_PROPERTY_SPECS)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)
        header = ttk.Frame(parent)
        header.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(header, text='Workspace Explorer', font=('Segoe UI Semibold', 11)).pack(side='left')
        self.external_explorer_status = ttk.Label(header, text='Waiting for a Roblox client', foreground=_FFLAG_COLOR_MUTED)
        self.external_explorer_status.pack(side='right')
        controls = ttk.Frame(parent)
        controls.grid(row=1, column=0, sticky='ew', pady=(0, 8))
        controls.columnconfigure(0, weight=1)
        self.external_explorer_search_var = tk.StringVar(value='')
        self.external_explorer_filter_var = tk.StringVar(value='All')
        self.external_explorer_search_entry = ttk.Entry(controls, textvariable=self.external_explorer_search_var)
        self.external_explorer_search_entry.grid(row=0, column=0, sticky='ew', padx=(0, 6))
        self.external_explorer_search_entry.bind('<Return>', lambda _event: self._external_explorer_render())
        self.external_explorer_filter = ttk.Combobox(controls, textvariable=self.external_explorer_filter_var, state='readonly', width=12, values=('All', 'Workspace', 'Models', 'Parts', 'Scripts', 'Folders', 'Remotes'))
        self.external_explorer_filter.grid(row=0, column=1, padx=(0, 6))
        self.external_explorer_filter.bind('<<ComboboxSelected>>', lambda _event: self._external_explorer_render())
        ttk.Button(controls, text='Search', command=self._external_explorer_render).grid(row=0, column=2, padx=(0, 6))
        self.external_explorer_refresh_button = ttk.Button(controls, text='Refresh', command=self._external_explorer_refresh)
        self.external_explorer_refresh_button.grid(row=0, column=3)
        body = ttk.PanedWindow(parent, orient='horizontal')
        body.grid(row=2, column=0, sticky='nsew')
        tree_host = ttk.Frame(body, padding=(0, 0, 6, 0))
        details_host = ttk.Frame(body, padding=(6, 0, 0, 0))
        tree_host.columnconfigure(0, weight=1)
        tree_host.rowconfigure(0, weight=1)
        details_host.columnconfigure(0, weight=1)
        details_host.rowconfigure(0, weight=1)
        body.add(tree_host, weight=3)
        body.add(details_host, weight=2)
        explorer_style = ttk.Style(parent)
        palette = globals().get('_CURRENT_PALETTE', {}) or {}
        explorer_bg = palette.get('bg_medium', palette.get('bg_dark', '#252526'))
        explorer_fg = palette.get('fg', '#dcdcdc')
        explorer_selected = palette.get('accent', '#365b88')
        explorer_muted = palette.get('fg_muted', '#9aa0a6')
        try:
            explorer_style.configure('RoUtils.Explorer.Treeview', rowheight=25, borderwidth=0, relief='flat', font=('Segoe UI', 9), background=explorer_bg, fieldbackground=explorer_bg, foreground=explorer_fg)
            explorer_style.map('RoUtils.Explorer.Treeview', background=[('selected', explorer_selected)], foreground=[('selected', '#ffffff')])
            explorer_style.configure('RoUtils.Explorer.Heading', font=('Segoe UI Semibold', 9), padding=(7, 5))
            explorer_style.configure('RoUtils.Properties.Treeview', rowheight=24, borderwidth=0, relief='flat', font=('Segoe UI', 9), background=explorer_bg, fieldbackground=explorer_bg, foreground=explorer_fg)
            explorer_style.map('RoUtils.Properties.Treeview', background=[('selected', explorer_selected)], foreground=[('selected', '#ffffff')])
        except Exception:
            pass
        self.external_explorer_tree = ttk.Treeview(tree_host, columns=('class', 'children'), show='tree', selectmode='browse', style='RoUtils.Explorer.Treeview')
        self.external_explorer_tree.column('#0', width=250, minwidth=145, stretch=True)
        self.external_explorer_tree.column('class', width=110, minwidth=70, stretch=False)
        self.external_explorer_tree.column('children', width=48, minwidth=40, stretch=False, anchor='center')
        self.external_explorer_tree.tag_configure('search', foreground='#8be0a7')
        self.external_explorer_tree.tag_configure('workspace', foreground='#d9e4ff')
        self.external_explorer_tree.tag_configure('model', foreground='#b8c8ff')
        self.external_explorer_tree.tag_configure('folder', foreground='#d8c69b')
        self.external_explorer_tree.tag_configure('part', foreground='#a9d6c1')
        self.external_explorer_tree.tag_configure('script', foreground='#e5c28b')
        self.external_explorer_tree.tag_configure('remote', foreground='#d2a8f5')
        scrollbar = ttk.Scrollbar(tree_host, orient='vertical', command=self.external_explorer_tree.yview)
        self.external_explorer_tree.configure(yscrollcommand=scrollbar.set)
        self.external_explorer_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.external_explorer_tree.bind('<<TreeviewOpen>>', self._external_explorer_on_open)
        self.external_explorer_tree.bind('<<TreeviewSelect>>', self._external_explorer_on_select)
        self.external_explorer_tree.bind('<Double-1>', self._external_explorer_on_double_click, add='+')
        self.external_explorer_tree.bind('<Button-3>', self._external_explorer_context_menu)
        self.external_explorer_tree.bind('<Button-2>', self._external_explorer_context_menu)
        self.external_explorer_notebook = ttk.Notebook(details_host)
        self.external_explorer_notebook.grid(row=0, column=0, sticky='nsew')
        properties_tab = ttk.Frame(self.external_explorer_notebook, padding=9)
        self.external_explorer_notebook.add(properties_tab, text='Properties')
        properties_tab.columnconfigure(0, weight=1)
        properties_tab.rowconfigure(2, weight=1)
        property_selection = ttk.LabelFrame(properties_tab, text='Selection', padding=(9, 7))
        property_selection.grid(row=0, column=0, sticky='ew', pady=(0, 7))
        for column in (1, 3):
            property_selection.columnconfigure(column, weight=1)
        self.external_explorer_property_name_var = tk.StringVar(value='—')
        self.external_explorer_property_class_var = tk.StringVar(value='—')
        self.external_explorer_property_path_var = tk.StringVar(value='—')
        ttk.Label(property_selection, text='Name', foreground=_FFLAG_COLOR_MUTED).grid(row=0, column=0, sticky='w', padx=(2, 7), pady=3)
        ttk.Label(property_selection, textvariable=self.external_explorer_property_name_var).grid(row=0, column=1, sticky='ew', padx=(0, 12), pady=3)
        ttk.Label(property_selection, text='Class', foreground=_FFLAG_COLOR_MUTED).grid(row=0, column=2, sticky='w', padx=(2, 7), pady=3)
        ttk.Label(property_selection, textvariable=self.external_explorer_property_class_var).grid(row=0, column=3, sticky='ew', pady=3)
        ttk.Label(property_selection, text='Path', foreground=_FFLAG_COLOR_MUTED).grid(row=1, column=0, sticky='w', padx=(2, 7), pady=3)
        ttk.Label(property_selection, textvariable=self.external_explorer_property_path_var, wraplength=360, justify='left').grid(row=1, column=1, columnspan=3, sticky='ew', pady=3)
        ttk.Label(property_selection, text='Parent', foreground=_FFLAG_COLOR_MUTED).grid(row=2, column=0, sticky='w', padx=(2, 7), pady=3)
        ttk.Label(property_selection, textvariable=self._external_explorer_detail_vars['parent']).grid(row=2, column=1, sticky='ew', padx=(0, 12), pady=3)
        ttk.Label(property_selection, text='Children', foreground=_FFLAG_COLOR_MUTED).grid(row=2, column=2, sticky='w', padx=(2, 7), pady=3)
        ttk.Label(property_selection, textvariable=self._external_explorer_detail_vars['children']).grid(row=2, column=3, sticky='ew', pady=3)
        ttk.Label(property_selection, text='Address', foreground=_FFLAG_COLOR_MUTED).grid(row=3, column=0, sticky='w', padx=(2, 7), pady=3)
        ttk.Label(property_selection, textvariable=self._external_explorer_detail_vars['address']).grid(row=3, column=1, columnspan=3, sticky='ew', pady=3)
        self.external_explorer_property_status_var = tk.StringVar(value='Select an instance to inspect its properties.')
        property_toolbar = ttk.Frame(properties_tab)
        property_toolbar.grid(row=1, column=0, sticky='ew', pady=(0, 6))
        property_toolbar.columnconfigure(0, weight=1)
        ttk.Label(property_toolbar, textvariable=self.external_explorer_property_status_var, foreground=_FFLAG_COLOR_MUTED, wraplength=420).grid(row=0, column=0, sticky='ew')
        property_host = ttk.Frame(properties_tab)
        property_host.grid(row=2, column=0, sticky='nsew')
        property_host.columnconfigure(0, weight=1)
        property_host.rowconfigure(0, weight=1)
        self.external_explorer_property_tree = ttk.Treeview(property_host, columns=('value',), show='tree headings', selectmode='browse', height=10, style='RoUtils.Properties.Treeview')
        self.external_explorer_property_tree.heading('#0', text='Property')
        self.external_explorer_property_tree.heading('value', text='Value')
        self.external_explorer_property_tree.column('#0', width=140, minwidth=95, stretch=True)
        self.external_explorer_property_tree.column('value', width=150, minwidth=95, stretch=True)
        self.external_explorer_property_tree.tag_configure('property_group', foreground=explorer_muted)
        property_scroll = ttk.Scrollbar(property_host, orient='vertical', command=self.external_explorer_property_tree.yview)
        self.external_explorer_property_tree.configure(yscrollcommand=property_scroll.set)
        self.external_explorer_property_tree.grid(row=0, column=0, sticky='nsew')
        property_scroll.grid(row=0, column=1, sticky='ns')
        self.external_explorer_property_tree.bind('<<TreeviewSelect>>', self._external_explorer_property_on_select)
        self._external_explorer_status('Attach a Roblox client in Clients. Explorer refreshes when the game changes.')
        self._external_explorer_schedule_auto_refresh()

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

    def _external_explorer_load_instance_properties(self, address):
        self._external_explorer_property_generation += 1
        generation = self._external_explorer_property_generation
        for item in self.external_explorer_property_tree.get_children(''):
            self.external_explorer_property_tree.delete(item)
        pid = int(getattr(self, 'fflag_pid', 0) or 0)
        cls = str(self._external_explorer_snapshot.get(int(address), {}).get('cls', ''))
        if not self._external_explorer_is_basepart_class(cls):
            self.external_explorer_property_status_var.set('Select a BasePart instance to view its properties.')
            return
        if not pid or pid != int(getattr(self, '_external_explorer_pid', 0) or 0):
            self.external_explorer_property_status_var.set('Attach a client and refresh the Explorer first.')
            return
        self.external_explorer_property_status_var.set('Reading selected Part properties…')
        def worker():
            values = []
            error_text = ''
            try:
                context = self._external_explorer_read_context(pid)
                live_class = context.class_name(int(address))
                if not self._external_explorer_is_basepart_class(live_class):
                    raise RuntimeError('The selected instance is not a BasePart.')
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
        return name in {'Part', 'MeshPart', 'UnionOperation', 'WedgePart', 'CornerWedgePart', 'TrussPart', 'Seat', 'VehicleSeat', 'SpawnLocation', 'SkateboardPlatform'}

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
        groups = {'Transform': ('Position', 'Size'), 'Physics': ('AssemblyLinearVelocity', 'AssemblyAngularVelocity', 'Anchored', 'CanCollide', 'CanTouch', 'CanQuery', 'Massless', 'Locked'), 'Appearance': ('Transparency', 'Reflectance', 'Color', 'Material', 'CastShadow')}
        group_ids = {}
        for group_name in groups:
            group_ids[group_name] = f'group_{group_name.casefold()}'
            tree.insert('', 'end', iid=group_ids[group_name], text=group_name, values=('',), open=True, tags=('property_group',))
        group_for = {key: group_name for group_name, keys in groups.items() for key in keys}
        for key, value in values:
            tree.insert(group_ids.get(group_for.get(key, 'Physics')), 'end', iid=key, text=key, values=(value,))
        self.external_explorer_property_status_var.set(f'{len(values)} read-only properties loaded.')

    def _external_explorer_property_on_select(self, event=None):
        selection = self.external_explorer_property_tree.selection()
        if not selection:
            return
        key = selection[0]
        values = self.external_explorer_property_tree.item(key, 'values')
        value = str(values[0]) if values else ''
        if key.startswith('group_'):
            return
        self.external_explorer_property_status_var.set(f'{key}: {value} · Read only')

    def _external_explorer_status(self, text, color=None):
        label = getattr(self, 'external_explorer_status', None)
        if label is None:
            return
        try:
            label.configure(text=str(text), foreground=color or _FFLAG_COLOR_MUTED)
        except Exception:
            pass

    def _external_explorer_schedule_auto_refresh(self):
        try:
            if self._external_explorer_auto_refresh_job:
                self.after_cancel(self._external_explorer_auto_refresh_job)
        except Exception:
            pass
        try:
            self._external_explorer_auto_refresh_job = self.after(3000, self._external_explorer_auto_refresh_tick)
        except Exception:
            self._external_explorer_auto_refresh_job = None

    def _external_explorer_auto_refresh_tick(self):
        self._external_explorer_auto_refresh_job = None
        engine = getattr(self, 'fflag_engine', None)
        pid = int(getattr(self, 'fflag_pid', 0) or 0)
        if not engine or not engine.handle or not pid or int(getattr(engine, 'pid', 0) or 0) != pid:
            self._external_explorer_schedule_auto_refresh()
            return
        if pid != int(getattr(self, '_external_explorer_pid', 0) or 0):
            self._external_explorer_refresh()
            self._external_explorer_schedule_auto_refresh()
            return
        if not getattr(self, '_external_explorer_scan_active', False) and not self._external_explorer_auto_refresh_active:
            self._external_explorer_auto_refresh_active = True
            def worker():
                root = 0
                workspace = 0
                error_text = ''
                try:
                    context = self._external_explorer_read_context(pid)
                    root = context.target('dm')
                    workspace = context.target('workspace')
                except Exception as error:
                    error_text = str(error)
                try:
                    self.after(0, self._external_explorer_auto_refresh_checked, pid, root, workspace, error_text)
                except Exception:
                    self._external_explorer_auto_refresh_active = False
            threading.Thread(target=worker, daemon=True, name='RoUtilsExplorerGameWatch').start()
        self._external_explorer_schedule_auto_refresh()

    def _external_explorer_auto_refresh_checked(self, pid, root, workspace, error_text=''):
        self._external_explorer_auto_refresh_active = False
        current_pid = int(getattr(self, 'fflag_pid', 0) or 0)
        if current_pid != int(pid):
            if current_pid:
                self._external_explorer_refresh()
            else:
                self._external_explorer_client_disconnected()
            return
        old_root = int(getattr(self, '_external_explorer_root', 0) or 0)
        old_workspace = int(getattr(self, '_external_explorer_workspace', 0) or 0)
        if root and workspace and (root != old_root or workspace != old_workspace):
            self._external_explorer_status('Game changed · refreshing Explorer', _FFLAG_COLOR_SUCCESS)
            self._external_explorer_refresh()
            if hasattr(self, '_external_property_refresh_all'):
                self._external_property_refresh_all(silent=True)
            return
        selected = self._external_explorer_selected_info()
        now = time.monotonic()
        if selected and now - float(getattr(self, '_external_explorer_last_property_poll', 0.0)) >= 6.0:
            self._external_explorer_last_property_poll = now
            self._external_explorer_load_instance_properties(selected[0])

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
            workspace = 0
            partial = False
            error_text = ''
            try:
                if int(getattr(engine, 'pid', 0) or 0) != pid or not engine.handle:
                    raise RuntimeError('The selected Roblox client changed. Select it again.')
                offsets_data = self._external_offsets_for_client(pid)
                context = _ExternalPropertyContext(self, offsets_data)
                root = context.target('dm')
                workspace = context.target('workspace')
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
                self.after(0, self._external_explorer_refresh_finished, pid, root, workspace, snapshot, partial, error_text)
            except Exception:
                self._external_explorer_scan_active = False

        threading.Thread(target=worker, daemon=True, name='RoUtilsExternalExplorer').start()

    def _external_explorer_refresh_finished(self, pid, root, workspace, snapshot, partial, error_text=''):
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
            self._external_explorer_workspace = 0
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
        self._external_explorer_workspace = int(workspace or 0)
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
        self._external_explorer_workspace = 0
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
        label = self._external_explorer_label(item['name'], item['cls'])
        node_tags = tuple(tag)
        class_name = str(item.get('cls', ''))
        class_tag = 'workspace' if class_name == 'Workspace' else 'model' if class_name == 'Model' else 'folder' if class_name == 'Folder' else 'script' if 'Script' in class_name else 'part' if self._external_explorer_is_basepart_class(class_name) else 'remote' if class_name.startswith(('Remote', 'Bindable')) else ''
        if class_tag:
            node_tags = tuple(node_tags) + (class_tag,)
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
        tree.insert('', 'end', iid=root_iid, text=self._external_explorer_label(item['name'] or 'Game', item['cls']), values=(item['cls'], len(item['kids'])), tags=('workspace',), open=True)
        self._external_explorer_item_data[root_iid] = {'kind': 'node', 'address': root}
        self._external_explorer_insert_children(root_iid, root, 0)
        self._external_explorer_clear_details()

    def _external_explorer_clear_details(self):
        for value in getattr(self, '_external_explorer_detail_vars', {}).values():
            value.set('—')
        for name in ('external_explorer_property_name_var', 'external_explorer_property_class_var', 'external_explorer_property_path_var'):
            variable = getattr(self, name, None)
            if variable is not None:
                variable.set('—')
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
        if hasattr(self, 'external_explorer_property_name_var'):
            self.external_explorer_property_name_var.set(item['name'])
            self.external_explorer_property_class_var.set(item['cls'])
            self.external_explorer_property_path_var.set(values['path'])
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
        return str(name or 'Unnamed')

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
        iid = self.external_explorer_tree.selection()[0]
        is_open = bool(self.external_explorer_tree.item(iid, 'open'))
        menu = tk.Menu(self.external_explorer_tree, tearoff=False)
        menu.add_command(label='Collapse' if is_open else 'Expand', command=lambda: self.external_explorer_tree.item(iid, open=not is_open))
        menu.add_command(label='Refresh Explorer', command=self._external_explorer_refresh)
        menu.add_command(label='Properties', command=lambda: self.external_explorer_notebook.select(0))
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

    def _external_explorer_read_context(self, pid):
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

