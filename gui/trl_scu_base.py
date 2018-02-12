# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jan 23 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class TrlScuMainFrame
###########################################################################

class TrlScuMainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Tomb Raider Legend SCU", pos = wx.DefaultPosition, size = wx.Size( 640,535 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.Size( 640,480 ), wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		main_frame_sizer = wx.FlexGridSizer( 3, 1, 0, 0 )
		main_frame_sizer.AddGrowableCol( 0 )
		main_frame_sizer.AddGrowableRow( 0 )
		main_frame_sizer.SetFlexibleDirection( wx.BOTH )
		main_frame_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_content_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_main_tab = wx.Panel( self.m_content_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_main_content_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		self.m_main_content_sizer.AddGrowableCol( 0 )
		self.m_main_content_sizer.AddGrowableRow( 1 )
		self.m_main_content_sizer.SetFlexibleDirection( wx.BOTH )
		self.m_main_content_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		level_choice_sizer = wx.StaticBoxSizer( wx.StaticBox( self.m_main_tab, wx.ID_ANY, u"On startup, load..." ), wx.VERTICAL )
		
		m_level_choiceChoices = []
		self.m_level_choice = wx.Choice( level_choice_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_level_choiceChoices, 0 )
		self.m_level_choice.SetSelection( 0 )
		level_choice_sizer.Add( self.m_level_choice, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_main_content_sizer.Add( level_choice_sizer, 1, wx.EXPAND, 5 )
		
		self.m_outer_radio_sizer = wx.StaticBoxSizer( wx.StaticBox( self.m_main_tab, wx.ID_ANY, u"Choose Outfit" ), wx.VERTICAL )
		
		self.m_outfit_sizer = wx.GridSizer( 0, 2, 0, 0 )
		
		
		self.m_outer_radio_sizer.Add( self.m_outfit_sizer, 1, wx.EXPAND, 5 )
		
		
		self.m_main_content_sizer.Add( self.m_outer_radio_sizer, 1, wx.EXPAND, 5 )
		
		
		self.m_main_tab.SetSizer( self.m_main_content_sizer )
		self.m_main_tab.Layout()
		self.m_main_content_sizer.Fit( self.m_main_tab )
		self.m_content_notebook.AddPage( self.m_main_tab, u"General Settings", True )
		self.m_adv_tab = wx.Panel( self.m_content_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_outer_dev_opts_sizer = wx.StaticBoxSizer( wx.StaticBox( self.m_adv_tab, wx.ID_ANY, u"Developer options" ), wx.VERTICAL )
		
		self.m_inner_dev_opts_content_sizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		self.m_inner_dev_opts_content_sizer.AddGrowableCol( 1 )
		self.m_inner_dev_opts_content_sizer.SetFlexibleDirection( wx.BOTH )
		self.m_inner_dev_opts_content_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		
		self.m_outer_dev_opts_sizer.Add( self.m_inner_dev_opts_content_sizer, 1, wx.EXPAND, 5 )
		
		self.m_info_text = wx.StaticText( self.m_outer_dev_opts_sizer.GetStaticBox(), wx.ID_ANY, u"Please note, that most of the options specified here don't have any effect. \nThey are mentioned in the executable but may be disabled in the code.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_info_text.Wrap( -1 )
		self.m_outer_dev_opts_sizer.Add( self.m_info_text, 0, wx.ALL, 5 )
		
		
		self.m_adv_tab.SetSizer( self.m_outer_dev_opts_sizer )
		self.m_adv_tab.Layout()
		self.m_outer_dev_opts_sizer.Fit( self.m_adv_tab )
		self.m_content_notebook.AddPage( self.m_adv_tab, u"Advanced Settings (Developer Hacks)", False )
		
		main_frame_sizer.Add( self.m_content_notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		bottom_info_sizer = wx.FlexGridSizer( 2, 2, 0, 0 )
		bottom_info_sizer.AddGrowableCol( 1 )
		bottom_info_sizer.SetFlexibleDirection( wx.BOTH )
		bottom_info_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_exe_label = wx.StaticText( self, wx.ID_ANY, u"TR Legend Executable", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_exe_label.Wrap( -1 )
		bottom_info_sizer.Add( self.m_exe_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_exe_picker = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"TR Legend Executable (trl.exe)|trl.exe|All executables (*.exe)|*.exe", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST|wx.FLP_OPEN|wx.FLP_SMALL )
		bottom_info_sizer.Add( self.m_exe_picker, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_version_label = wx.StaticText( self, wx.ID_ANY, u"TR Legend Version", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_version_label.Wrap( -1 )
		bottom_info_sizer.Add( self.m_version_label, 0, wx.ALL, 5 )
		
		self.m_version_display_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		self.m_version_display_text.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bottom_info_sizer.Add( self.m_version_display_text, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		main_frame_sizer.Add( bottom_info_sizer, 1, wx.EXPAND, 5 )
		
		lower_button_sizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_save_btn = wx.Button( self, wx.ID_ANY, u"Save Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
		lower_button_sizer.Add( self.m_save_btn, 0, wx.ALL, 5 )
		
		self.m_load_btn = wx.Button( self, wx.ID_ANY, u"Load Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
		lower_button_sizer.Add( self.m_load_btn, 0, wx.ALL, 5 )
		
		self.m_reset_btn = wx.Button( self, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0 )
		lower_button_sizer.Add( self.m_reset_btn, 0, wx.ALL, 5 )
		
		
		lower_button_sizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_run_btn = wx.Button( self, wx.ID_ANY, u"Run", wx.DefaultPosition, wx.DefaultSize, 0 )
		lower_button_sizer.Add( self.m_run_btn, 0, wx.ALL, 5 )
		
		
		main_frame_sizer.Add( lower_button_sizer, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( main_frame_sizer )
		self.Layout()
		self.m_menubar = wx.MenuBar( 0 )
		self.m_menu_help = wx.Menu()
		self.m_mi_help_about = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_help.Append( self.m_mi_help_about )
		
		self.m_menubar.Append( self.m_menu_help, u"Help" ) 
		
		self.SetMenuBar( self.m_menubar )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_level_choice.Bind( wx.EVT_CHOICE, self.OnSelectLevel )
		self.m_exe_picker.Bind( wx.EVT_FILEPICKER_CHANGED, self.OnExeSelected )
		self.m_save_btn.Bind( wx.EVT_BUTTON, self.OnSaveSettings )
		self.m_load_btn.Bind( wx.EVT_BUTTON, self.OnLoadSettings )
		self.m_reset_btn.Bind( wx.EVT_BUTTON, self.OnReset )
		self.m_run_btn.Bind( wx.EVT_BUTTON, self.OnRun )
		self.Bind( wx.EVT_MENU, self.OnAbout, id = self.m_mi_help_about.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnSelectLevel( self, event ):
		event.Skip()
	
	def OnExeSelected( self, event ):
		event.Skip()
	
	def OnSaveSettings( self, event ):
		event.Skip()
	
	def OnLoadSettings( self, event ):
		event.Skip()
	
	def OnReset( self, event ):
		event.Skip()
	
	def OnRun( self, event ):
		event.Skip()
	
	def OnAbout( self, event ):
		event.Skip()
	

