import tkinter as tk
from tkinter import ttk
from . import widgets as w
from . import constants as c
import os
from tkinter import filedialog
from tkinter import simpledialog


class CreateBatchForm(tk.Frame):
    """The input form for the Batch Widgets"""
    def __init__(self, parent, callbacks, fields=None, *args, **kwargs):

        super().__init__(parent, *args, **kwargs)
        # Dictonary to keep tracK of input Widgets

        self.inputs = {}
        self.callbacks = callbacks
        ########################
        # Project Information Frame
        #######################

        frame_projectinfo = tk.LabelFrame(self, text= "Project Information")

        self.inputs['txb_ProjectLocation'] = w.LabelInput(frame_projectinfo, "Project Location:", input_class=w.ValidEntry,
                                                       input_var=tk.StringVar(),
                                                       input_arg={'state':'readonly'})



        self.inputs['txb_ProjectLocation'].grid(row=0, column=0)
        self.inputs['btn_projLocation'] = w.LabelInput(frame_projectinfo,"Browse", input_class=ttk.Button, input_var=tk.StringVar()
                                                     ,input_arg={'command': lambda:self.select_folder('txb_ProjectLocation')})
        self.inputs['btn_projLocation'].grid(row=0, column=1, sticky=tk.S)

        self.inputs['tbx_resultLocation']= w.LabelInput(frame_projectinfo, "Results Location:", input_class=w.ValidEntry,
                                                      input_var=tk.StringVar(),
                                                      input_arg={'state': 'readonly'})

        self.inputs['tbx_resultLocation'].variable.set(c.AppConfig.result_location)
        self.inputs['tbx_resultLocation'].grid(row=1, column=0 )
        frame_projectinfo.grid(row=3, sticky=(tk.W+tk.E), padx =10, pady=10)  # Display Project Info Frame
        frame_projectinfo.columnconfigure(0, weight=1)

        ########################
        # Search Scripts Frame
        #######################

        self.inputs['frm_searchscripts'] = tk.LabelFrame(self, text="Search Scripts")

        #Adding the Folder Structure
        # self.inputs['FolderStructure'] = w.FolderTreeView(self.inputs['frm_searchscripts'],self.inputs['txb_ProjectLocation'].get(),sfilter=['.git','.settings','libspecs','__pycache__','.png'])
        self.inputs['FolderStructure'] = w.FolderTreeView(self.inputs['frm_searchscripts'])

        self.inputs['FolderStructure'].grid(row=0)



        # Adding the Search Button
        self.inputs['SearchBtn'] = w.LabelInput(self.inputs['frm_searchscripts'], "Search", input_class=ttk.Button, input_var=tk.StringVar(),
                                              input_arg={'command':self.callbacks['SearchBtn']})
        self.inputs['SearchBtn'].grid(row=1, column=0)

        # Adding Tags Box
        self.inputs['cb_tags'] = w.LabelInput(self.inputs['frm_searchscripts'], "", input_class=ttk.Combobox,
                                              input_var=tk.StringVar())
        self.inputs['cb_tags'].grid(row=1,column=1)

        # Adding DataTable For Searched Scripts

        self.inputs['SearchScripts'] = w.TabularTreeView(self.inputs['frm_searchscripts'],
                                                       ('Name',
                                                        'Documentation'
                                                        , 'Tags'
                                                        , 'Suite'))
        self.inputs['SearchScripts'].set_column_width('Name', 400)

        self.inputs['SearchScripts'].grid(row=0, column=1 )


        # Adding the Search Button
        self.inputs['AddSelectedBtn'] = w.LabelInput(self.inputs['frm_searchscripts'], "Add Selected"
                                                   , input_class=ttk.Button
                                                   , input_var=tk.StringVar()
                                                   , input_arg={'command':self.callbacks['AddSelected']})

        self.inputs['AddSelectedBtn'].grid(row=0, column=2)
        self.inputs['frm_searchscripts'].grid(row=4, sticky=(tk.W+tk.E), padx =10, pady=10) # Display the Search Frame

        ########################
        # Batch Frame
        #######################
        self.inputs['frm_cb_batchscripts'] = tk.LabelFrame(self, text="Batch")

        # Adding load from Book Marks Checkbox
        self.inputs['ckb_loadfrombookMark'] = w.LabelInput(self.inputs['frm_cb_batchscripts'],label='Load from Bookmark'
                                                         , input_class=ttk.Checkbutton,input_var=tk.IntVar()
                                                         , input_arg={'command':self.cmd_load_from_bookmark})
        self.inputs['ckb_loadfrombookMark'].variable.set(0)
        self.inputs['ckb_loadfrombookMark'].grid(row=0)

        #Adding Book Maks Comobox

        self.inputs['cb_bookMark'] = w.LabelInput(self.inputs['frm_cb_batchscripts'], label='',
                                    input_class=ttk.Combobox,
                                    input_var=tk.StringVar()
                                    )
        self.inputs['cb_bookMark'].variable.set("Select Bookmark")

        self.inputs['cb_bookMark'].bind("<<ComboboxSelected>>", self.__on_combobox_selected)
        # Adding DataTable For BAtch Scripts
        self.inputs['trv_batchScripts'] = w.TabularTreeView(self.inputs['frm_cb_batchscripts'],
                                                       ('Name', 'Documentation', 'Tags', 'Suite'))
        self.inputs['trv_batchScripts'].set_column_width('Name',500)
        self.inputs['trv_batchScripts'].set_column_width('Suite', 320)
        self.inputs['trv_batchScripts'].grid(row=1, column=0)

        # Adding the Remove Button
        self.inputs['btn_removeSelected'] = w.LabelInput(self.inputs['frm_cb_batchscripts'], "Remove Selected", input_class=ttk.Button,
                                                   input_var=tk.StringVar(), input_arg={'command':self.remove_test_from_batch})
        self.inputs['btn_removeSelected'].grid(row=1, column=1, sticky=tk.E)


        # Adding the Create Batch Button
        self.inputs['btn_createBatch'] = w.LabelInput(self.inputs['frm_cb_batchscripts'], "Create Batch",
                                                      input_class=ttk.Button,
                                                      input_var=tk.StringVar(),
                                                      input_arg={'command':self.callbacks['btn_createBatch']}
                                                      )

        self.inputs['btn_createBatch'].grid(row=2, column=0, sticky=tk.W)

        # Adding the Create BookMark Button
        self.inputs['btn_createBookmark'] = w.LabelInput(self.inputs['frm_cb_batchscripts'], "Create Bookmark",
                                                      input_class=ttk.Button,
                                                      input_var=tk.StringVar(),
                                                      input_arg={'command': self.callbacks['btn_createBookmark']}
                                                      )

        self.inputs['btn_createBookmark'].grid(row=2, column=1, sticky=tk.W)

        self.inputs['frm_cb_batchscripts'].grid(row=5, sticky=(tk.W+tk.E), padx =10, pady=10)  # Display the Search Frame

    # Get the data for the all the Widgets
    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            # print(widget.widgetName)
            if  widget.widgetName in ('labelframe',):
                pass
            # elif hasattr(widget,'tree') and 'foldertreeview'in str(widget).split('!'):
            #     data[key] = widget.get_selected_item_path()
            # elif hasattr(widget, 'tree') and 'tabulartreeview' in str(widget).split('!'):
            #     data[key] = widget.get_selected_items()
            else:
                data[key] = widget.get()
        return data

    def reset(self):
        for widget in self.inputs.values():
            widget.set('')

    def populate_data(self,proj_location, bm_list, tags):
        # print("tags", tags)
        self.inputs['txb_ProjectLocation'].variable.set(proj_location)
        self.inputs['cb_bookMark'].set(bm_list)
        self.inputs['cb_tags'].set(tags)
        self.inputs['FolderStructure'].update_tree(proj_location, sfilter=['.git', '.settings', 'libspecs', '__pycache__',
                                                                   '.png'])
        self.inputs['SearchScripts'].clear_items()
        self.inputs['trv_batchScripts'].clear_items()

    def __on_combobox_selected(self,*args):
        self.callbacks['cb_bookMark'](self.inputs['cb_bookMark'].get())

    def batch_details(self):
        #############################
        # Create a top Level window
        ############################
        win_batchdetails = tk.Toplevel(self)
        self.inputs['win_batchdetails'] = win_batchdetails
        win_batchdetails.title="Create Batch"
        win_batchdetails.lift()
        win_batchdetails.grab_set()
        win_batchdetails.geometry('%dx%d+%d+%d' % (600, 850, self.winfo_rootx(), self.winfo_rooty()))
        win_batchdetails.resizable(width=False, height=False)
        win_batchdetails.columnconfigure(0,weight=1)
        ttk.Label(win_batchdetails, text="Enter the batch details", font=("TkDefaultFont", 16)).grid(row=0)


        #############################
        # Create a Batch Info Frame
        ############################
        frame_batch_info = tk.LabelFrame(win_batchdetails, text="Batch Information")
        frame_batch_info.grid(row=1, sticky=(tk.W+tk.E), padx =10, pady=10)
        frame_batch_info.columnconfigure(0, weight=1)
        self.inputs['txb_batchName'] = w.LabelInput(frame_batch_info, "Name:", input_class=w.ValidEntry,
                                                        input_var=tk.StringVar())
        self.inputs['txb_batchName'].columnconfigure(0, weight=1)
        self.inputs['txb_batchName'].grid(row=0, column=0)

        self.inputs['txb_batchNumberOfThreads'] = w.LabelInput(frame_batch_info, "Number of Threads:", input_class=w.ValidSpinbox,
                                                  input_var=tk.StringVar(), input_arg={"from_":'1',"to":'4', "increment":'1'})
        self.inputs['txb_batchNumberOfThreads'].grid(row=0,column=1)

        #############################
        # Create a Application Type Frame
        ############################
        frame_application_type = tk.LabelFrame(win_batchdetails, text="Application Type & Language")
        frame_application_type.grid(row=3, sticky=(tk.W+tk.E), padx =10, pady=10)
        # frame_application_type.columnconfigure(4, weight=1)


        self.inputs['rb_applicationTypeWeb'] = w.LabelInput(frame_application_type, "Web",
                                                             input_class=ttk.Radiobutton,
                                                             input_var=tk.StringVar()
                                                          ,input_arg={"value":"Web",'command':self.cmd_select_application_type})
        self.inputs['rb_applicationTypeWeb'].grid(row=0, column=1 ,padx=10)

        self.inputs['rb_applicationTypeMobile'] = w.LabelInput(frame_application_type, "Mobile",
                                                             input_class=ttk.Radiobutton,
                                                             input_var=self.inputs['rb_applicationTypeWeb'].variable,
                                                             input_arg={"value": "Mobile",
                                                                        'command': self.cmd_select_application_type})
        self.inputs['rb_applicationTypeMobile'].grid(row=0, column=0)

        self.inputs['rb_application_lang_FR'] = w.LabelInput(frame_application_type, "FR",
                                                            input_class=ttk.Radiobutton,
                                                            input_var=tk.StringVar()
                                                            , input_arg={"value": "FR"})
        self.inputs['rb_application_lang_FR'].grid(row=1, column=1, padx=10)

        self.inputs['rb_application_lang_EN'] = w.LabelInput(frame_application_type, "EN",
                                                               input_class=ttk.Radiobutton,
                                                               input_var=self.inputs['rb_application_lang_FR'].variable,
                                                               input_arg={"value": "EN"})
        self.inputs['rb_application_lang_EN'].grid(row=1, column=0)

        #############################
        # Create a Select Device/Browser Type Frame
        ############################
        frame_device_browser = tk.LabelFrame(win_batchdetails, text="Select Device / Browser ")
        frame_device_browser.grid(row=4, sticky=(tk.W+tk.E), padx =10, pady=10)
        frame_device_browser.columnconfigure(0, weight=1)
        self.inputs['lstbx_device'] = w.LabelInput(frame_device_browser, "Device List", input_class=tk.Listbox
                                                  , input_var=tk.StringVar(), input_arg={"selectmode": "multiple",
                                                                                         'exportselection':0})
        # self.inputs['lstbx_device'].variable.set(self._load_device_list())

        self.inputs['lstbx_device'].grid(row=0, column=0,padx=10)


        self.inputs['lstbx_browser'] = w.LabelInput(frame_device_browser,"Internet Explorer", input_class=tk.Listbox
                                                   , input_var=tk.StringVar(), input_arg={"selectmode":"multiple",
                                                                                          'exportselection':0})
        self.inputs['lstbx_browser'].variable.set(c.AppConfig.BROWSER_LIST)

        #####################################
        # Mobile Center Detials
        #####################################
        self.inputs['frame_mc_details'] = tk.LabelFrame(win_batchdetails, text="Mobile Center Details")
        self.inputs['frame_mc_details'].columnconfigure(0, weight=1)
        self.inputs['frame_mc_details'].columnconfigure(1, weight=1)
        self.inputs['frame_mc_details'].grid(row=5, sticky=(tk.W + tk.E), padx=10, pady=10)

        self.inputs['lstbx_mobile_center'] = w.LabelInput(self.inputs['frame_mc_details'], "Select Server:"
                                                          , input_class=ttk.Combobox
                                                          , input_var=tk.StringVar(),
                                                          input_arg={'values':c.AppConfig.SERVER_LIST})



        # self.inputs['lstbx_mobile_center'].columnconfigure(0, weight=1)
        self.inputs['lstbx_mobile_center'].grid(row=0, column=0, padx=10, columnspan=2)

        self.inputs['txb_mc_user_name'] = w.LabelInput(self.inputs['frame_mc_details'], "User Name:",
                                                       input_class=w.ValidEntry,
                                                       input_var=tk.StringVar())

        self.inputs['txb_mc_user_name'].grid(row=1, column=0, padx=10)

        self.inputs['txb_mc_user_pass'] = w.LabelInput(self.inputs['frame_mc_details'], "User Password:",
                                                       input_class=w.ValidEntry,
                                                       input_var=tk.StringVar(),
                                                       input_arg={'show':'*'})
        self.inputs['txb_mc_user_pass'].grid(row=1, column=1, padx=10)

        #####################################
        # URL Detials
        #####################################
        self.inputs['frame_url_details'] = tk.LabelFrame(win_batchdetails, text="URL Details")
        self.inputs['frame_url_details'].columnconfigure(0, weight=1)
        self.inputs['frame_url_details'].columnconfigure(1, weight=1)
        # self.inputs['frame_url_details'].grid(row=5, sticky=(tk.W + tk.E), padx=10, pady=10)

        self.inputs['lstbx_url_center'] = w.LabelInput(self.inputs['frame_url_details'], "Select URL:"
                                                          , input_class=ttk.Combobox
                                                          , input_var=tk.StringVar(),
                                                          input_arg={'values': c.AppConfig.URL_LIST})

        self.inputs['lstbx_url_center'].grid(row=0, column=0, padx=10, columnspan=2)

        #####################################
        # ALM  Detials
        #####################################
        self.inputs['frame_alm_details'] = tk.LabelFrame(win_batchdetails, text="ALM Details")
        self.inputs['frame_alm_details'].columnconfigure(0, weight=1)
        self.inputs['frame_alm_details'].columnconfigure(1, weight=1)
        self.inputs['frame_alm_details'].grid(row=6, sticky=(tk.W + tk.E), padx=10, pady=10)
        self.inputs['txb_alm_plan_path'] = w.LabelInput(self.inputs['frame_alm_details'], "Test Plan Path:",
                                                       input_class=w.ValidEntry,
                                                       input_var=tk.StringVar())

        self.inputs['txb_alm_plan_path'].grid(row=0, column=0, padx=10)

        self.inputs['txb_alm_lab_path'] = w.LabelInput(self.inputs['frame_alm_details'], "Test Lab Path:",
                                                        input_class=w.ValidEntry,
                                                        input_var=tk.StringVar())

        self.inputs['txb_alm_lab_path'].grid(row=0, column=1, padx=10)

        self.inputs['txb_alm_test_set_name'] = w.LabelInput(self.inputs['frame_alm_details'], "Test Set Name:",
                                                       input_class=w.ValidEntry,
                                                       input_var=tk.StringVar())

        self.inputs['txb_alm_test_set_name'].grid(row=0, column=3, padx=10)

        # Adding load from Book Marks Checkbox
        # self.inputs['ckb_createbookmark'] = w.LabelInput(win_batchdetails, label='Create Bookmark',
        #                                                  input_class=ttk.Checkbutton, input_var=tk.IntVar())
        # self.inputs['ckb_createbookmark'].variable.set(0)
        # self.inputs['ckb_createbookmark'].columnconfigure(0, weight=1)
        # self.inputs['ckb_createbookmark'].grid(row=7, padx =10)

        # Adding the Create Batch/ Book Mark Button
        self.inputs['btn_createBatch_Bookmark'] = w.LabelInput(win_batchdetails, "Create Batch", input_class=ttk.Button,
                                                                input_var=tk.StringVar(),
                                                               input_arg={'command':self.callbacks['btn_createBatch_Bookmark']})

        self.inputs['btn_createBatch_Bookmark'].grid(row=8, column=0, sticky=(tk.W), padx =10)

    def get_errors(self):
        """Get a list of field errors in the form"""
        errors ={}
        for widgetName, widget in self.inputs.items():
            if hasattr(widget, "input") and hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if hasattr(widget, "error") and widget.error.get():
                errors[widgetName] = widget.error.get()
        return errors

    def select_folder(self, entry_name):
        """command to Browser the Folder Structure"""
        folder_selected = filedialog.askdirectory()
        if folder_selected != '':
            self.inputs[entry_name].variable.set(folder_selected)
            self.inputs['FolderStructure'].update_tree(folder_selected,
                                                        sfilter=['.git', '.settings', 'libspecs', '__pycache__',
                                                                     '.png'])

            # parser = AppConfigParser(c.AppConfig.user_config_file)
            # parser.readfile()
            # if not parser.has_section(c.AppConfig.INI_APP_SETTING_SECTION):
            #     parser.add_section(c.AppConfig.INI_APP_SETTING_SECTION)
            # parser[c.AppConfig.INI_APP_SETTING_SECTION][c.AppConfig.INI_PROJECT_LOCATION] = folder_selected
            # parser.writefile()
            self.callbacks['btn_projLocation'](folder_selected)


    def populate_scripts_table(self, test_list):
        """Function to populate Scripts Table for the Searched Scripts"""
        self.inputs['SearchScripts'].clear_items()
        for test in test_list:
            self.inputs['SearchScripts'].insert_item(test, values=(test.name
                                                                   , test.doc
                                                                   , test.tags
                                                                   , test.source))

    def populate_scripts_table2(self, test_list):
        """Function to populate Scripts Table for the Searched Scripts"""
        self.inputs['SearchScripts'].clear_items()
        for test in test_list:
            self.inputs['SearchScripts'].insert_item(test, values=(test['name']
                                                                   , test['doc']
                                                                   , test['tags']
                                                                   , test['source']))

    def get_selected_folder_path(self):
        return self.inputs['FolderStructure'].get_selected_item_path()

    def get_tags(self):
        return self.inputs['cb_tags'].get()

    def get_selected_search_tests(self):
        """Function to Return Selected Tests"""
        return self.inputs['SearchScripts'].get_selected_items()

    def get_batch_tests(self):
        """Funtion will return all the items from batch Scripts Tree View"""
        return self.inputs['trv_batchScripts'].get_items()

    def insert_tests_to_batch(self,test_list):
        for test in test_list:
            self.inputs['trv_batchScripts'].insert_item(test, allow_duplicates=False, values=(test.name
                                          , test.doc
                                          , test.tags
                                          , test.source))
    def insert_tests_to_batch2(self,test_list):
        """Takes Test as List of Dict"""
        for test in test_list:
            self.inputs['trv_batchScripts'].insert_item(test, allow_duplicates=False, values=(test['name']
                                          , test['doc']
                                          , test['tags']
                                          , test['source']))

    def remove_test_from_batch(self):
        """function to Remove Test Case From Batch """
        self.inputs['trv_batchScripts'].delete_selected_item()

    def cmd_select_application_type(self):
        if self.inputs['rb_applicationTypeWeb'].variable.get() =='Mobile':
            self.inputs['lstbx_browser'].grid_remove()
            self.inputs['lstbx_device'].grid(row=0, column=0, padx=10)
            self.inputs['frame_mc_details'].grid(row=5, sticky=(tk.W + tk.E), padx=10, pady=10)
            self.inputs['frame_url_details'].grid_remove()

        else:
            self.inputs['frame_url_details'].grid(row=5, sticky=(tk.W + tk.E), padx=10, pady=10)
            self.inputs['lstbx_device'].grid_remove()
            self.inputs['lstbx_browser'].grid(row=0, column=0, padx=10)
            self.inputs['frame_mc_details'].grid_remove()

    def cmd_load_from_bookmark(self):
        if self.inputs['ckb_loadfrombookMark'].variable.get() == 1:
            self.callbacks['ckb_loadfrombookMark']()
            self.inputs['cb_bookMark'].grid(row=0, column=0, sticky=tk.E)

        else:
            self.inputs['cb_bookMark'].grid_remove()

    def load_device_list(self,device_list):
        device_list = device_list if device_list else []
        self.inputs['lstbx_device'].variable.set(device_list)

#
# class BatchDetailsForm(tk.Frame):
#     """The input form for the Batch Details
#     This will be displayed once user click on Create batch Button"""
#     def __init__(self, parent, fields=None, *args, **kwargs):
#
#         super().__init__(parent, *args, **kwargs)
#         # Dictonary to keep tracK of input Widgets
#
#         self.inputs = {}
#         #############################
#         # Create a top Level window
#         ############################
#         win_batchdetails = tk.Toplevel(self)
#         self.inputs['win_batchdetails'] = win_batchdetails
#         win_batchdetails.title = "Create Batch"
#         win_batchdetails.lift()
#         win_batchdetails.grab_set()
#         win_batchdetails.geometry('%dx%d+%d+%d' % (600, 500, self.winfo_rootx(), self.winfo_rooty()))
#         win_batchdetails.columnconfigure(0, weight=1)
#         ttk.Label(win_batchdetails, text="Enter the batch details", font=("TkDefaultFont", 16)).grid(row=0)
#
#         #############################
#         # Create a Batch Info Frame
#         ############################
#         frame_batch_info = tk.LabelFrame(win_batchdetails, text="Batch Information")
#         frame_batch_info.grid(row=1, sticky=(tk.W + tk.E), padx=10, pady=10)
#         frame_batch_info.columnconfigure(0, weight=1)
#         self.inputs['txb_batchName'] = w.LabelInput(frame_batch_info, "Name:", input_class=w.ValidEntry,
#                                                     input_var=tk.StringVar())
#         self.inputs['txb_batchName'].columnconfigure(0, weight=1)
#         self.inputs['txb_batchName'].grid(row=0, column=0)
#
#         self.inputs['txb_batchNumberOfThreads'] = w.LabelInput(frame_batch_info, "Number of Threads:",
#                                                                input_class=w.ValidSpinbox,
#                                                                input_var=tk.StringVar(),
#                                                                input_arg={"from_": '1', "to": '4', "increment": '1'}
#                                                                )
#         self.inputs['txb_batchNumberOfThreads'].grid(row=0, column=1)
#
#         #############################
#         # Create a Application Type Frame
#         ############################
#         frame_application_type = tk.LabelFrame(win_batchdetails, text="Application Type")
#         frame_application_type.grid(row=3, sticky=(tk.W + tk.E), padx=10, pady=10)
#         frame_application_type.columnconfigure(2, weight=1)
#
#         self.inputs['rb_applicationTypeWeb'] = w.LabelInput(frame_application_type, "Web",
#                                                             input_class=ttk.Radiobutton,
#                                                             input_var=tk.StringVar()
#                                                             , input_arg={"value": "Web",
#                                                                          'command': self.cmd_select_application_type})
#         self.inputs['rb_applicationTypeWeb'].grid(row=0, column=1, padx=20)
#
#         self.inputs['rb_applicationTypeMobile'] = w.LabelInput(frame_application_type, "Mobile",
#                                                                input_class=ttk.Radiobutton,
#                                                                input_var=self.inputs['rb_applicationTypeWeb'].variable,
#                                                                input_arg={"value": "Mobile",
#                                                                           'command': self.cmd_select_application_type})
#         self.inputs['rb_applicationTypeMobile'].grid(row=0, column=0)
#
#         #############################
#         # Create a Select Device/Browser Type Frame
#         ############################
#         frame_device_browser = tk.LabelFrame(win_batchdetails, text="Select Device / Browser ")
#         frame_device_browser.grid(row=4, sticky=(tk.W + tk.E), padx=10, pady=10)
#         frame_device_browser.columnconfigure(0, weight=1)
#         self.inputs['lstbx_device'] = w.LabelInput(frame_device_browser, "Device List", input_class=tk.Listbox
#                                                    , input_var=tk.StringVar(), input_arg={"selectmode": "multiple"},
#                                                    )
#         self.inputs['lstbx_device'].variable.set(self._load_device_list())
#         # self.inputs['lstbx_device'].variable.set(fields['DeviceList'])
#
#         self.inputs['lstbx_device'].grid(row=0, column=0, padx=10)
#
#         self.inputs['lstbx_browser'] = w.LabelInput(frame_device_browser, "Internet Explorer", input_class=tk.Listbox
#                                                     , input_var=tk.StringVar(), input_arg={"selectmode": "multiple"}
#                                                     )
#         self.inputs['lstbx_browser'].variable.set("IE Chrome FireFox Safari")
#
#         # Adding load from Book Marks Checkbox
#         self.inputs['ckb_createbookmark'] = w.LabelInput(win_batchdetails, label='Create Bookmark',
#                                                          input_class=ttk.Checkbutton, input_var=tk.IntVar())
#         self.inputs['ckb_createbookmark'].variable.set(0)
#         self.inputs['ckb_createbookmark'].columnconfigure(0, weight=1)
#         self.inputs['ckb_createbookmark'].grid(row=7, padx=10)
#
#         # Adding the Create Batch/ Book Mark Button
#         self.inputs['btn_createBatch_Bookmark'] = w.LabelInput(win_batchdetails, "Create Batch/Bookmark",
#                                                                input_class=ttk.Button,
#                                                                input_var=tk.StringVar(),
#                                                                input_arg={'command': self.cmd_insert_batch_details})
#
#         self.inputs['btn_createBatch_Bookmark'].grid(row=8, column=0, sticky=(tk.W), padx=10)

class BatchMonitor(tk.Frame):
    """The input form for the Batch Widgets"""

    def __init__(self, parent, callbacks,  fields=None,  *args, **kwargs):

        super().__init__(parent, *args, **kwargs)
        # Dictonary to keep tracK of input Widgets

        self.inputs = {}
        self.callbacks = callbacks
        ########################
        # Batch Frame
        #######################

        frame_projectinfo = tk.LabelFrame(self, text="Batches")
        frame_projectinfo.grid(row=3, sticky=(tk.W + tk.E), padx=10, pady=10)  # Display Project Info Frame
        frame_projectinfo.columnconfigure(0, weight=1)

        # Adding Table For Searched Batches

        self.inputs['trv_batches'] = w.BatchTabularTreeView(frame_projectinfo,
                                                       ('Batch ID',
                                                        'Name',
                                                        'Creation Date',
                                                        '#Threads',
                                                        '#Scripts',
                                                        'Application Type',
                                                        'Device/Browsers'),selection_mode='browse', height=35,**kwargs)



        self.inputs['trv_batches'].set_column_width('Batch ID', 60)
        self.inputs['trv_batches'].set_column_width('Name', 300)
        self.inputs['trv_batches'].set_column_width('#Threads', 60)
        self.inputs['trv_batches'].set_column_width('#Scripts', 55)
        self.inputs['trv_batches'].set_column_width('Application Type', 100)
        self.inputs['trv_batches'].set_column_width('Creation Date', 120)
        self.inputs['trv_batches'].grid(row=0, column=0)
        # Adding the Open Selected Batch
        self.inputs['btn_open_selected'] = w.LabelInput(frame_projectinfo, "Open Selected"
                                                   , input_class=ttk.Button
                                                   , input_var=tk.StringVar()
                                                   , input_arg={'command': self.callbacks['btn_open_selected']})

        self.inputs['btn_open_selected'].grid(row=1, column=0)

        self.inputs['trv_batches'].add_cmd(label="Open",
                                                              command=self.callbacks['Open'])

        self.inputs['trv_batches'].add_cmd(label="Start",
                                                              command=self.callbacks['Start'])

        self.inputs['trv_batches'].add_cmd(label="Stop",
                                                              command=self.callbacks['Stop'])

        self.inputs['trv_batches'].add_cmd(label="Rerun",
                                                              command=self.callbacks['Rerun'])
        self.inputs['trv_batches'].add_cmd(label="Update Details",
                                                              command=self.callbacks['Update Details'])



    def populate_batch_information(self, batches):
        """Remove Existing Batches"""
        self.inputs['trv_batches'].clear_items()
        for batch in batches:
            self.inputs['trv_batches'].insert_item(batch, allow_duplicates=False,
                                                                      values=(batch.Batch_ID,
                                                                              batch.Batch_Name,
                                                                              batch.CreationDate,
                                                                              batch.ThreadCount,
                                                                              batch.ScriptCount,
                                                                              batch.TestType,
                                                                              batch.Browsers_OR_Devices))

class BatchExecutionMonitor(tk.Toplevel):
    """Class for Batch Execution Monitor"""
    def __init__(self, parent, callbacks, batch_id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # Dictonary to keep tracK of input Widgets
        self.inputs = {}
        self.callbacks =callbacks
        self.title("Batch Exexution Monitor:{}".format(batch_id))
        self.lift()
        self.columnconfigure(0,weight=1)
        self.Batch_ID=batch_id

        frame_batch_execution_details = ttk.LabelFrame(self, text="Batch Execution Details")
        frame_batch_execution_details.grid(row=1,sticky=(tk.W+tk.E), padx =10, pady=10)
        frame_batch_execution_details.columnconfigure(0, weight=1)

        ###################################################
        # Batch Information Section
        #################################################
        frame_batch_info = ttk.LabelFrame(self, text="Batch Infromation")
        frame_batch_info.columnconfigure(5, weight=1)
        frame_batch_info.grid(row=0, sticky=(tk.W + tk.E), padx=10, pady=10)
        ttk.Label(frame_batch_info, text="Batch Name:", font=("TkDefaultFont", 9, 'bold')).grid(row=0, column=0,
                                                                                                padx=50,
                                                                                                sticky=tk.W)
        self.inputs["lbl_batchName"] = w.LabelInput(frame_batch_info, "", input_class=ttk.Label,
                                                    input_var=tk.StringVar())
        self.inputs["lbl_batchName"].grid(row=0, column=1)

        ttk.Label(frame_batch_info, text="Creation Date:", font=("TkDefaultFont", 9, 'bold')).grid(row=0, column=2,
                                                                                                   padx=50,
                                                                                                   sticky=tk.W)
        self.inputs["lbl_creationDate"] = w.LabelInput(frame_batch_info, "", input_class=ttk.Label,
                                                       input_var=tk.StringVar())
        self.inputs["lbl_creationDate"].grid(row=0, column=3)

        ttk.Label(frame_batch_info, text="Total Scripts:", font=("TkDefaultFont", 9, 'bold')).grid(row=0, column=4,
                                                                                                   padx=50,
                                                                                                   sticky=tk.W)
        self.inputs["lbl_totalScripts"] = w.LabelInput(frame_batch_info, "", input_class=ttk.Label,
                                                       input_var=tk.IntVar())
        self.inputs["lbl_totalScripts"].grid(row=0, column=5)

        ttk.Label(frame_batch_info, text="Passed:", font=("TkDefaultFont", 9, 'bold')).grid(row=1, column=0,
                                                                                            padx=50,
                                                                                            sticky=tk.W)
        self.inputs["lbl_totalpassed"] = w.LabelInput(frame_batch_info, "", input_class=ttk.Label,
                                                      input_var=tk.IntVar())
        self.inputs["lbl_totalpassed"].grid(row=1, column=1)

        ttk.Label(frame_batch_info, text="Failed:", font=("TkDefaultFont", 9, 'bold')).grid(row=1, column=2,
                                                                                            padx=50,
                                                                                            sticky=tk.W)
        self.inputs["lbl_totalFailed"] = w.LabelInput(frame_batch_info, "", input_class=ttk.Label,
                                                      input_var=tk.IntVar())
        self.inputs["lbl_totalFailed"].grid(row=1, column=3)

        ttk.Label(frame_batch_info, text="Pass Percentage:", font=("TkDefaultFont", 9, 'bold')).grid(row=1, column=4,
                                                                                                     padx=50,
                                                                                                     sticky=tk.W)

        self.inputs["lbl_passpercent"] = w.LabelInput(frame_batch_info, "", input_class=ttk.Label,
                                                      input_var=tk.IntVar())
        self.inputs["lbl_passpercent"].grid(row=1, column=5)




        #*****************************
        # Scripts Gui
        #*****************************
        self.inputs['trv_batchScripts'] = w.ScriptTabularTreeView(frame_batch_execution_details,
                                                          ('S.No',
                                                           'Name',
                                                           'Documentation',
                                                           'Module',
                                                           'Status',
                                                           'Start Date',
                                                           'End Date',
                                                           'Device/Browser',
                                                           'Run Count'), selection_mode='browse',height=30)

        self.inputs['trv_batchScripts'].set_column_width('S.No', 60)
        self.inputs['trv_batchScripts'].set_column_width('Name', 300)
        self.inputs['trv_batchScripts'].set_column_width('Documentation', 300)
        self.inputs['trv_batchScripts'].set_column_width('Module', 100)
        self.inputs['trv_batchScripts'].set_column_width('Status', 80)
        self.inputs['trv_batchScripts'].set_column_width('Start Date', 100)
        self.inputs['trv_batchScripts'].set_column_width('End Date', 100)
        self.inputs['trv_batchScripts'].set_column_width('Device/Browser', 100)
        self.inputs['trv_batchScripts'].set_column_width('Run Count', 60)

        self.inputs['trv_batchScripts'].grid(row=0, column=0)


        self.inputs['trv_batchScripts'].add_cmd(label="Open",
                                                                        command=self.callbacks['Open'])
        self.inputs['trv_batchScripts'].add_cmd(label="Re-Run",
                                                                        command=self.callbacks['Re-Run'])
        self.inputs['trv_batchScripts'].add_cmd(label="Update",
                                                                        command=self.callbacks['Update'])
        self.inputs['trv_batchScripts'].add_cmd(label="Stop",
                                                                        command=self.callbacks['Stop'])



    def load_batch_information(self, batch_name, creation_date, script_count, scripts_passed, scripts_failed):

        self.inputs["lbl_batchName"].variable.set(batch_name)
        self.inputs["lbl_creationDate"].variable.set(creation_date)
        self.inputs["lbl_totalScripts"].variable.set(script_count)
        self.inputs["lbl_totalpassed"].variable.set(scripts_passed)
        self.inputs["lbl_totalFailed"].variable.set(scripts_failed)
        pass_percentage = (scripts_passed / script_count) * 100
        self.inputs["lbl_passpercent"].variable.set(pass_percentage)

    def load_scripts_information(self, scripts):

        count=1
        for row in scripts:
            self.inputs['trv_batchScripts'].insert_item(row, allow_duplicates=False,
                                                        values=(count,row.ScriptName,
                                                                    row.Documentation,
                                                                    os.path.split(row.Source)[1],
                                                                    row.Status,
                                                                    row.StartTime,
                                                                    row.End_Time,
                                                                    row.Device_Browser,
                                                                    row.Run_Count))
            count+=1

    def refresh_scripts(self, scripts):
        """Function to refresh the Batch"""
        #Delete the Scripts
        self.inputs['trv_batchScripts'].clear_items()
        # Reinsert the scripts
        count = 1
        for row in scripts:
            self.inputs['trv_batchScripts'].insert_item(row, allow_duplicates=False,
                                                        values=(count, row.ScriptName,
                                                                row.Documentation,
                                                                os.path.split(row.Source)[1],
                                                                row.Status,
                                                                row.StartTime,
                                                                row.End_Time,
                                                                row.Device_Browser,
                                                                row.Run_Count))
            count += 1
    #
    # def refresh_batch_labels(self, batch_name, script_count, scripts_passed, scripts_failed):
    #     """KW to Update Batch Labels"""
    #     self.inputs["lbl_batchName"].variable.set(batch_name)
    #     self.inputs["lbl_totalScripts"].variable.set(script_count)
    #     self.inputs["lbl_totalpassed"].variable.set(scripts_passed)
    #     self.inputs["lbl_totalFailed"].variable.set(scripts_failed)
    #     pass_percentage = (scripts_passed / script_count) * 100
    #     self.inputs["lbl_passpercent"].variable.set(pass_percentage)

class BatchUpdate(tk.Toplevel):
    """Class for Batch Update Window"""
    def __init__(self, parent, callbacks, batch_id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # Dictonary to keep tracK of input Widgets
        self.inputs = {}
        self.frames = {}
        self.callbacks =callbacks
        self.title("Batch Update:{}".format(batch_id))
        self.lift()
        self.grab_set()
        self.columnconfigure(0,weight=1)
        self.Batch_ID=batch_id

        ttk.Label(self, text="Update the batch details", font=("TkDefaultFont", 16)).grid(row=0)

        #############################
        # Create a Batch Info Frame
        ############################
        frame_batch_info = tk.LabelFrame(self, text="Batch Information")
        frame_batch_info.grid(row=1, sticky=(tk.W + tk.E), padx=10, pady=10)
        frame_batch_info.columnconfigure(0, weight=1)
        self.inputs['txb_batchName'] = w.LabelInput(frame_batch_info, "Name:", input_class=w.ValidEntry,
                                                    input_var=tk.StringVar(),
                                                    input_arg={'state': 'readonly'})
        self.inputs['txb_batchName'].columnconfigure(0, weight=1)
        self.inputs['txb_batchName'].grid(row=0, column=0)

        self.inputs['txb_batchNumberOfThreads'] = w.LabelInput(frame_batch_info, "Number of Threads:",
                                                               input_class=w.ValidSpinbox,
                                                               input_var=tk.StringVar(),
                                                               input_arg={"from_": '1', "to": '4', "increment": '1'})
        self.inputs['txb_batchNumberOfThreads'].grid(row=0, column=1)

        #############################
        # Create a Application Type Frame
        ############################
        frame_application_type = tk.LabelFrame(self, text="Application Type & Language")
        frame_application_type.grid(row=3, sticky=(tk.W + tk.E), padx=10, pady=10)
        # frame_application_type.columnconfigure(4, weight=1)

        self.inputs['rb_applicationTypeWeb'] = w.LabelInput(frame_application_type, "Web",
                                                            input_class=ttk.Radiobutton,
                                                            input_var=tk.StringVar()
                                                            , input_arg={"value": "Web",
                                                                         'command': self.cmd_select_application_type
                                                                         })
        self.inputs['rb_applicationTypeWeb'].grid(row=0, column=1, padx=10)

        self.inputs['rb_applicationTypeMobile'] = w.LabelInput(frame_application_type, "Mobile",
                                                               input_class=ttk.Radiobutton,
                                                               input_var=self.inputs['rb_applicationTypeWeb'].variable,
                                                               input_arg={"value": "Mobile",
                                                                          'command': self.cmd_select_application_type
                                                                          })
        self.inputs['rb_applicationTypeMobile'].grid(row=0, column=0)

        self.inputs['rb_application_lang_FR'] = w.LabelInput(frame_application_type, "FR",
                                                             input_class=ttk.Radiobutton,
                                                             input_var=tk.StringVar()
                                                             , input_arg={"value": "FR"})
        self.inputs['rb_application_lang_FR'].grid(row=1, column=1, padx=10)

        self.inputs['rb_application_lang_EN'] = w.LabelInput(frame_application_type, "EN",
                                                             input_class=ttk.Radiobutton,
                                                             input_var=self.inputs['rb_application_lang_FR'].variable,
                                                             input_arg={"value": "EN"})
        self.inputs['rb_application_lang_EN'].grid(row=1, column=0)

        #############################
        # Create a Select Device/Browser Type Frame
        ############################
        frame_device_browser = tk.LabelFrame(self, text="Select Device / Browser ")
        frame_device_browser.grid(row=4, sticky=(tk.W + tk.E), padx=10, pady=10)
        frame_device_browser.columnconfigure(0, weight=1)
        self.inputs['lstbx_device'] = w.LabelInput(frame_device_browser, "Device List", input_class=tk.Listbox
                                                   , input_var=tk.StringVar(), input_arg={"selectmode": "multiple",
                                                                                          'exportselection': 0})

        self.inputs['lstbx_device'].grid(row=0, column=0, padx=10)

        self.inputs['lstbx_browser'] = w.LabelInput(frame_device_browser, "Internet Explorer", input_class=tk.Listbox
                                                    , input_var=tk.StringVar(), input_arg={"selectmode": "multiple",
                                                                                           'exportselection': 0})
        self.inputs['lstbx_browser'].variable.set(c.AppConfig.BROWSER_LIST)

        #####################################
        # Mobile Center Detials
        #####################################

        self.frames['frame_mc_details'] = tk.LabelFrame(self, text="Mobile Center Details")
        self.frames['frame_mc_details'].columnconfigure(0, weight=1)
        self.frames['frame_mc_details'].columnconfigure(1, weight=1)
        self.frames['frame_mc_details'].grid(row=5, sticky=(tk.W + tk.E), padx=10, pady=10)
        self.inputs['lstbx_mobile_center'] = w.LabelInput(self.frames['frame_mc_details'], "Select Server:"
                                                          , input_class=ttk.Combobox
                                                          , input_var=tk.StringVar(),
                                                          input_arg={'values': c.AppConfig.SERVER_LIST})

        self.inputs['lstbx_mobile_center'].grid(row=0, column=0, padx=10, columnspan=2)

        self.inputs['txb_mc_user_name'] = w.LabelInput(self.frames['frame_mc_details'], "User Name:",
                                                       input_class=w.ValidEntry,
                                                       input_var=tk.StringVar())

        self.inputs['txb_mc_user_name'].grid(row=1, column=0, padx=10)

        self.inputs['txb_mc_user_pass'] = w.LabelInput(self.frames['frame_mc_details'], "User Password:",
                                                       input_class=w.ValidEntry,
                                                       input_var=tk.StringVar(),
                                                       input_arg={'show':'*'})
        self.inputs['txb_mc_user_pass'].grid(row=1, column=1, padx=10)

        #####################################
        # URL Detials
        #####################################
        self.frames['frame_url_details'] = tk.LabelFrame(self, text="URL Details")
        self.frames['frame_url_details'].columnconfigure(0, weight=1)
        self.frames['frame_url_details'].columnconfigure(1, weight=1)
        # self.inputs['frame_url_details'].grid(row=5, sticky=(tk.W + tk.E), padx=10, pady=10)

        self.inputs['lstbx_url_center'] = w.LabelInput(self.frames['frame_url_details'], "Select URL:"
                                                       , input_class=ttk.Combobox
                                                       , input_var=tk.StringVar(),
                                                       input_arg={'values': c.AppConfig.URL_LIST})

        self.inputs['lstbx_url_center'].grid(row=0, column=0, padx=10, columnspan=2)

        #####################################
        # ALM  Detials
        #####################################
        frame_alm_details = tk.LabelFrame(self, text="ALM Details")
        frame_alm_details.columnconfigure(0, weight=1)
        frame_alm_details.columnconfigure(1, weight=1)
        frame_alm_details.grid(row=6, sticky=(tk.W + tk.E), padx=10, pady=10)
        self.inputs['txb_alm_plan_path'] = w.LabelInput(frame_alm_details, "Test Plan Path:",
                                                        input_class=w.ValidEntry,
                                                        input_var=tk.StringVar())

        self.inputs['txb_alm_plan_path'].grid(row=0, column=0, padx=10)

        self.inputs['txb_alm_lab_path'] = w.LabelInput(frame_alm_details, "Test Lab Path:",
                                                       input_class=w.ValidEntry,
                                                       input_var=tk.StringVar())

        self.inputs['txb_alm_lab_path'].grid(row=0, column=1, padx=10)

        self.inputs['txb_alm_test_set_name'] = w.LabelInput(frame_alm_details, "Test Set Name:",
                                                            input_class=w.ValidEntry,
                                                            input_var=tk.StringVar())

        self.inputs['txb_alm_test_set_name'].grid(row=0, column=3, padx=10)


        # Adding the Create Batch/ Book Mark Button
        self.inputs['btn_update'] = w.LabelInput(self, "Update",
                                                               input_class=ttk.Button,
                                                               input_var=tk.StringVar(),
                                                               input_arg={'command': self.callbacks[
                                                                   'btn_update']})

        self.inputs['btn_update'].grid(row=8, column=0, sticky=(tk.W), padx=10)
        # self.bind('<Destroy>', self.on_destroy)

    def on_destroy(self, *args):
        self.callbacks['refresh']()

    def load_device_list(self,device_list):
        device_list = device_list if device_list else []
        self.inputs['lstbx_device'].variable.set(device_list)

    def cmd_select_application_type(self):
        if self.inputs['rb_applicationTypeWeb'].variable.get() =='Mobile':
            self.inputs['lstbx_browser'].grid_remove()
            self.inputs['lstbx_device'].grid(row=0, column=0, padx=10)
            self.frames['frame_mc_details'].grid(row=5, sticky=(tk.W + tk.E), padx=10, pady=10)
            self.frames['frame_url_details'].grid_remove()
        else:
            self.inputs['lstbx_device'].grid_remove()
            self.frames['frame_url_details'].grid(row=5, sticky=(tk.W + tk.E), padx=10, pady=10)
            self.inputs['lstbx_browser'].grid(row=0, column=0, padx=10)
            self.frames['frame_mc_details'].grid_remove()

    def populate(self, batch_details, device_list):
        self.inputs['txb_batchName'].variable.set(batch_details.Batch_Name)
        self.inputs['txb_batchNumberOfThreads'].variable.set(batch_details.ThreadCount)
        self.inputs['rb_applicationTypeWeb'].variable.set(batch_details.TestType)
        self.inputs['rb_application_lang_FR'].variable.set(batch_details.ENV_LANGUAGE)
        self.inputs['lstbx_device'].variable.set(device_list)
        if batch_details.TestType != 'Web':
            self.inputs['lstbx_mobile_center'].variable.set(batch_details.ENV_MC_SERVER)
            self.inputs['txb_mc_user_name'].variable.set(batch_details.ENV_MC_USER_NAME)
            self.inputs['txb_mc_user_pass'].variable.set(batch_details.ENV_MC_USER_PASS)
            self.inputs['lstbx_browser'].grid_remove()
            self.inputs['lstbx_device'].grid(row=0, column=0, padx=10)
            self.frames['frame_mc_details'].grid(row=5, sticky=(tk.W + tk.E), padx=10, pady=10)
            self.frames['frame_url_details'].grid_remove()
        else:
            self.frames['frame_url_details'].grid(row=5, sticky=(tk.W + tk.E), padx=10, pady=10)
            self.frames['frame_mc_details'].grid_remove()
            self.inputs['lstbx_device'].grid_remove()
            self.inputs['lstbx_browser'].grid(row=0, column=0, padx=10)
            self.inputs['lstbx_url_center'].variable.set(batch_details.ENV_URL)
        self.inputs['txb_alm_plan_path'].variable.set(batch_details.ALMTestPlanPath)
        self.inputs['txb_alm_lab_path'].variable.set(batch_details.ALMTestLabPath)
        self.inputs['txb_alm_test_set_name'].variable.set(batch_details.ALMTestSetName)

    # Get the data for the all the Widgets
    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            # print(key)
            data[key] = widget.get()
        return data

    def get_errors(self):
        """Get a list of field errors in the form"""
        errors ={}
        for widgetName, widget in self.inputs.items():
            if hasattr(widget, "input") and hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if hasattr(widget, "error") and widget.error.get():
                errors[widgetName] = widget.error.get()
        return errors


class ScriptUpdate(tk.Toplevel):
    """Class for Script Update Window"""
    def __init__(self, parent, callbacks, script_id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # Dictonary to keep tracK of input Widgets
        self.inputs = {}
        self.frames = {}
        self.callbacks =callbacks
        self.script_id = script_id
        self.title("Script Update:{}".format(self.script_id))
        self.lift()
        self.grab_set()
        self.columnconfigure(0,weight=1)


        ttk.Label(self, text="Update the Scripts details", font=("TkDefaultFont", 16)).grid(row=0)

        #############################
        # Create a Script Info Frame
        ############################
        frame_batch_info = tk.LabelFrame(self, text="Script Information")
        frame_batch_info.grid(row=1, sticky=(tk.W + tk.E), padx=10, pady=10)
        frame_batch_info.columnconfigure(0, weight=1)
        self.inputs['txb_ScriptName'] = w.LabelInput(frame_batch_info, "Name:", input_class=w.ValidEntry,
                                                    input_var=tk.StringVar(),
                                                    input_arg={'state': 'readonly'})
        self.inputs['txb_ScriptName'].columnconfigure(0, weight=1)
        self.inputs['txb_ScriptName'].grid(row=0, column=0)


        #############################
        # Create a Application Type Frame
        ############################
        frame_application_type = tk.LabelFrame(self, text="Application Type & Language")
        frame_application_type.grid(row=3, sticky=(tk.W + tk.E), padx=10, pady=10)

        self.inputs['rb_applicationTypeWeb'] = w.LabelInput(frame_application_type, "Web",
                                                            input_class=ttk.Radiobutton,
                                                            input_var=tk.StringVar()
                                                            , input_arg={"value": "Web",
                                                                         'state': 'disabled'
                                                                         })
        self.inputs['rb_applicationTypeWeb'].grid(row=0, column=1, padx=10)

        self.inputs['rb_applicationTypeMobile'] = w.LabelInput(frame_application_type, "Mobile",
                                                               input_class=ttk.Radiobutton,
                                                               input_var=self.inputs['rb_applicationTypeWeb'].variable,
                                                               input_arg={"value": "Mobile",
                                                                          'state': 'disabled'
                                                                          })
        self.inputs['rb_applicationTypeMobile'].grid(row=0, column=0)

        self.inputs['rb_application_lang_FR'] = w.LabelInput(frame_application_type, "FR",
                                                             input_class=ttk.Radiobutton,
                                                             input_var=tk.StringVar()
                                                             , input_arg={"value": "FR",
                                                                          'state': 'disabled'
                                                                          })
        self.inputs['rb_application_lang_FR'].grid(row=1, column=1, padx=10)

        self.inputs['rb_application_lang_EN'] = w.LabelInput(frame_application_type, "EN",
                                                             input_class=ttk.Radiobutton,
                                                             input_var=self.inputs['rb_application_lang_FR'].variable,
                                                             input_arg={"value": "EN",
                                                                        'state': 'disabled'
                                                                        })
        self.inputs['rb_application_lang_EN'].grid(row=1, column=0)

        #############################
        # Create a Select Device/Browser Type Frame
        ############################
        frame_device_browser = tk.LabelFrame(self, text="Select Device / Browser ")
        frame_device_browser.grid(row=4, sticky=(tk.W + tk.E), padx=10, pady=10)
        frame_device_browser.columnconfigure(0, weight=1)
        self.inputs['lstbx_device'] = w.LabelInput(frame_device_browser, "Device List", input_class=tk.Listbox
                                                   , input_var=tk.StringVar(), input_arg={"selectmode": "single",
                                                                                          'exportselection': 0})

        self.inputs['lstbx_device'].grid(row=0, column=0, padx=10)

        self.inputs['lstbx_browser'] = w.LabelInput(frame_device_browser, "Internet Explorer", input_class=tk.Listbox
                                                    , input_var=tk.StringVar(), input_arg={"selectmode": "single",
                                                                                           'exportselection': 0})
        self.inputs['lstbx_browser'].variable.set("IE Chrome FireFox Safari")

        #####################################
        # Mobile Center Detials
        #####################################

        self.frames['frame_mc_details'] = tk.LabelFrame(self, text="Mobile Center Details")
        self.frames['frame_mc_details'].columnconfigure(0, weight=1)
        self.frames['frame_mc_details'].columnconfigure(1, weight=1)
        self.frames['frame_mc_details'].grid(row=5, sticky=(tk.W + tk.E), padx=10, pady=10)

        self.inputs['lstbx_mobile_center'] = w.LabelInput(self.frames['frame_mc_details'], "Select Server:"
                                                          , input_class=ttk.Combobox
                                                          , input_var=tk.StringVar(),
                                                          input_arg={'values': c.AppConfig.SERVER_LIST,
                                                                     'state':'disabled'})

        self.inputs['lstbx_mobile_center'].grid(row=0, column=0, padx=10, columnspan=2)

        self.inputs['txb_mc_user_name'] = w.LabelInput(self.frames['frame_mc_details'], "User Name:",
                                                       input_class=w.ValidEntry,
                                                       input_var=tk.StringVar(),
                                                       input_arg={'state':'readonly'})

        self.inputs['txb_mc_user_name'].grid(row=1, column=0, padx=10)

        self.inputs['txb_mc_user_pass'] = w.LabelInput(self.frames['frame_mc_details'], "User Password:",
                                                       input_class=w.ValidEntry,
                                                       input_var=tk.StringVar(),
                                                       input_arg={'state':'readonly',
                                                                  'show':'*'})
        self.inputs['txb_mc_user_pass'].grid(row=1, column=1, padx=10)

        #####################################
        # URL Detials
        #####################################
        self.frames['frame_url_details'] = tk.LabelFrame(self, text="URL Details")
        self.frames['frame_url_details'].columnconfigure(0, weight=1)
        self.frames['frame_url_details'].columnconfigure(1, weight=1)
        # self.inputs['frame_url_details'].grid(row=5, sticky=(tk.W + tk.E), padx=10, pady=10)

        self.inputs['lstbx_url_center'] = w.LabelInput(self.frames['frame_url_details'], "Select URL:"
                                                       , input_class=ttk.Combobox
                                                       , input_var=tk.StringVar(),
                                                       input_arg={'values': c.AppConfig.URL_LIST,
                                                                  'state':'disabled'})

        self.inputs['lstbx_url_center'].grid(row=0, column=0, padx=10, columnspan=2)

        #####################################
        # ALM  Detials
        #####################################
        frame_alm_details = tk.LabelFrame(self, text="ALM Details")
        frame_alm_details.columnconfigure(0, weight=1)
        frame_alm_details.columnconfigure(1, weight=1)
        frame_alm_details.grid(row=6, sticky=(tk.W + tk.E), padx=10, pady=10)
        self.inputs['txb_alm_plan_path'] = w.LabelInput(frame_alm_details, "Test Plan Path:",
                                                        input_class=w.ValidEntry,
                                                        input_var=tk.StringVar(),
                                                        input_arg={'state':'readonly'})

        self.inputs['txb_alm_plan_path'].grid(row=0, column=0, padx=10)

        self.inputs['txb_alm_lab_path'] = w.LabelInput(frame_alm_details, "Test Lab Path:",
                                                       input_class=w.ValidEntry,
                                                       input_var=tk.StringVar(),
                                                       input_arg={'state':'readonly'})

        self.inputs['txb_alm_lab_path'].grid(row=0, column=1, padx=10)

        self.inputs['txb_alm_test_set_name'] = w.LabelInput(frame_alm_details, "Test Set Name:",
                                                            input_class=w.ValidEntry,
                                                            input_var=tk.StringVar(),
                                                            input_arg={'state':'readonly'})

        self.inputs['txb_alm_test_set_name'].grid(row=0, column=3, padx=10)


        # Adding the Create Batch/ Book Mark Button
        self.inputs['btn_update'] = w.LabelInput(self, "Update",
                                                               input_class=ttk.Button,
                                                               input_var=tk.StringVar(),
                                                               input_arg={'command': self.callbacks[
                                                                   'btn_update']})

        self.inputs['btn_update'].grid(row=8, column=0, sticky=(tk.W), padx=10)
        # self.bind('<Destroy>', self.on_destroy)

    def on_destroy(self,*args):
        self.callbacks['refresh']()

    def load_device_list(self,device_list):
        device_list = device_list if device_list else []
        self.inputs['lstbx_device'].variable.set(device_list)

    def populate(self, batch_details, device_list):
        self.inputs['txb_ScriptName'].variable.set(batch_details.ScriptName)
        self.inputs['rb_applicationTypeWeb'].variable.set(batch_details.TestType)
        self.inputs['rb_application_lang_FR'].variable.set(batch_details.ENV_LANGUAGE)
        self.inputs['lstbx_device'].variable.set(device_list)
        if batch_details.TestType != 'Web':
            self.inputs['lstbx_mobile_center'].variable.set(batch_details.ENV_MC_SERVER)
            self.inputs['txb_mc_user_name'].variable.set(batch_details.ENV_MC_USER_NAME)
            self.inputs['txb_mc_user_pass'].variable.set(batch_details.ENV_MC_USER_PASS)
            self.inputs['lstbx_browser'].grid_remove()
            self.inputs['lstbx_device'].grid(row=0, column=0, padx=10)
            self.frames['frame_mc_details'].grid(row=5, sticky=(tk.W + tk.E), padx=10, pady=10)
            self.frames['frame_url_details'].grid_remove()
        else:
            self.frames['frame_mc_details'].grid_remove()
            self.frames['frame_url_details'].grid(row=5, sticky=(tk.W + tk.E), padx=10, pady=10)
            self.inputs['lstbx_device'].grid_remove()
            self.inputs['lstbx_browser'].grid(row=0, column=0, padx=10)
            self.inputs['lstbx_url_center'].variable.set(batch_details.ENV_URL)
        self.inputs['txb_alm_plan_path'].variable.set(batch_details.ALMTestPlanPath)
        self.inputs['txb_alm_lab_path'].variable.set(batch_details.ALMTestLabPath)
        self.inputs['txb_alm_test_set_name'].variable.set(batch_details.ALMTestSetName)

    # Get the data for the all the Widgets
    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            # print(key)
            data[key] = widget.get()
        return data

    def get_errors(self):
        """Get a list of field errors in the form"""
        errors ={}
        for widgetName, widget in self.inputs.items():
            if hasattr(widget, "input") and hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if hasattr(widget, "error") and widget.error.get():
                errors[widgetName] = widget.error.get()
        return errors


class CreateBookMark(tk.Toplevel):
    """Class for Book mark Update Window"""
    def __init__(self, parent, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # Dictonary to keep tracK of input Widgets
        self.inputs = {}
        self.frames = {}
        self.callbacks = callbacks
        self.title("Create BookMark")
        self.lift()
        self.grab_set()
        self.columnconfigure(0,weight=1)

        ttk.Label(self, text="Enter Bookmark Details", font=("TkDefaultFont", 16)).grid(row=0)

        #############################
        # Create a Book Mark Frame
        ############################
        self.frames['frame_batch_info'] = tk.LabelFrame(self, text="Bookmark Information")
        self.frames['frame_batch_info'].grid(row=1, sticky=(tk.W + tk.E), padx=10, pady=10)
        self.frames['frame_batch_info'].columnconfigure(0, weight=1)
        self.inputs['txb_bookmarkName'] = w.LabelInput(self.frames['frame_batch_info'], "Name:", input_class=w.ValidEntry,
                                                    input_var=tk.StringVar())
        self.inputs['txb_bookmarkName'].columnconfigure(0, weight=1)
        self.inputs['txb_bookmarkName'].grid(row=0, column=0)

        # Adding the Create  Book Mark Button
        self.inputs['btn_createBookMark'] = w.LabelInput(self, "Create Bookmark",
                                                               input_class=ttk.Button,
                                                               input_var=tk.StringVar(),
                                                               input_arg={'command': self.callbacks[
                                                                   'btn_createBookMark']})

        self.inputs['btn_createBookMark'].grid(row=2, column=0, sticky=(tk.W), padx=10)

    def load_admin_ui(self):
        return simpledialog.askstring('Admin Access Required', 'Admin Password:', parent=self, show='*')

    # Get the data for the all the Widgets
    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    def get_errors(self):
        """Get a list of field errors in the form"""
        errors ={}
        for widgetName, widget in self.inputs.items():
            if hasattr(widget, "input") and hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if hasattr(widget, "error") and widget.error.get():
                errors[widgetName] = widget.error.get()
        return errors


class AlmLoginForm(tk.Toplevel):
    """The input form for the Batch Widgets"""
    def __init__(self, parent, callbacks, *args, **kwargs):

        super().__init__(parent, *args, **kwargs)
        self.inputs = {}
        self.frames = {}
        self.data_dict={}
        self.callbacks = callbacks
        self.resizable(width=False, height=False)
        parent.update_idletasks()
        x = int(parent.winfo_x()) + 100
        y = int(parent.winfo_y()) + 100
        self.geometry("+%d+%d" % (x, y))
        self.grab_set()
        self.lift()
        self.columnconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", parent.destroy)

        ttk.Label(self, text="Application Lifecycle Management Login", font=("TkDefaultFont", 16)).grid(row=0)


        self.frames['frm_user_details'] = tk.LabelFrame(self, text="User Details")
        self.frames['frm_user_details'].grid(row=1, sticky=(tk.W + tk.E), padx=10, pady=10)
        self.frames['frm_user_details'].columnconfigure(0, weight=1)
        self.inputs['txb_user_name'] = w.LabelInput(self.frames['frm_user_details'], "Name:", input_class=w.ValidEntry,
                                                       input_var=tk.StringVar()
                                                       )
        self.inputs['txb_user_name'].grid(row=0, column=0)
        self.inputs['txb_user_name'].bind('<Key>', self.__on_key_pressed)

        self.inputs['txb_user_pass'] = w.LabelInput(self.frames['frm_user_details'], "Password:", input_class=ttk.Entry,
                                                    input_var=tk.StringVar(),
                                                    input_arg={'show':'*'}
                                                    )
        self.inputs['txb_user_pass'].grid(row=1, column=0)

        self.inputs['btn_authenticate'] = w.LabelInput(self.frames['frm_user_details'], label='Authenticate',
                                                input_class=ttk.Button,
                                                input_var=tk.StringVar(),
                                                input_arg={'command':self.callbacks['btn_authenticate']}
                                                )
        self.inputs['btn_authenticate'].grid(row=2, column=0)

        self.frames['frm_project_details'] = tk.LabelFrame(self, text="Project Details")
        self.frames['frm_project_details'].grid(row=2, sticky=(tk.W + tk.E), padx=10, pady=10)
        self.frames['frm_project_details'].columnconfigure(0, weight=1)

        self.inputs['cb_domain'] = w.LabelInput(self.frames['frm_project_details'], label='Domain:',
                                              input_class=ttk.Combobox,
                                              input_var=tk.StringVar(),
                                              input_arg={'state':'disabled'})
        self.inputs['cb_domain'].grid(row=0, column=0)

        self.inputs['cb_domain'].bind("<<ComboboxSelected>>", self.__on_combobox_selected)

        self.inputs['cb_project'] = w.LabelInput(self.frames['frm_project_details'], label='Project:',
                                                input_class=ttk.Combobox,
                                                input_var=tk.StringVar(),
                                                input_arg={'state':'disabled'})
        self.inputs['cb_project'].grid(row=1, column=0)

        self.inputs['btn_login']= w.LabelInput(self.frames['frm_project_details'], label='Login',
                                                input_class=ttk.Button,
                                                input_var=tk.StringVar(),
                                                input_arg={'state':'disabled', 'command':self.callbacks['btn_login']})
        self.inputs['btn_login'].grid(row=2, column=0)

    def populate(self, data_dict):
        self.data_dict = data_dict
        self.inputs['cb_domain'].input.configure(state='readonly')
        self.inputs['cb_project'].input.configure(state='readonly')
        self.inputs['btn_login'].input.configure(state=tk.NORMAL)
        self.inputs['cb_domain'].variable.set('')
        self.inputs['cb_project'].variable.set('')
        self.inputs['cb_domain'].set(list(self.data_dict.keys()))
        self.inputs['cb_project'].set(self.data_dict.get(self.inputs['cb_domain'].get()),[])


    # Get the data for the all the Widgets
    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            if  widget.widgetName in ('labelframe',):
                pass
            else:
                data[key] = widget.get()
        return data

    def reset(self):
        for widget in self.inputs.values():
            widget.set('')

    def get_errors(self):
        """Get a list of field errors in the form"""
        errors ={}
        for widgetName, widget in self.inputs.items():
            if hasattr(widget, "input") and hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if hasattr(widget, "error") and widget.error.get():
                errors[widgetName] = widget.error.get()
        return errors

    def __on_combobox_selected(self,*args):
        self.inputs['cb_project'].set(self.data_dict.get(self.inputs['cb_domain'].get()), [])

    def __on_key_pressed(self,*args):
        self.inputs['cb_domain'].input.configure(state=tk.DISABLED)
        self.inputs['cb_project'].input.configure(state=tk.DISABLED)
        self.inputs['btn_login'].input.configure(state=tk.DISABLED)
