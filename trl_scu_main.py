
import os
import subprocess
import traceback
import wx

have_winreg = False
try:
    import winreg
    have_winreg = True
except:
    pass
    
have_win32api = False
try:
    from win32api import GetFileVersionInfo, LOWORD, HIWORD
    have_win32api = True
except Exception as e:
    pass
    
from gui.trl_scu_base import TrlScuMainFrame

LevelChoices = {
    "Main Menu" : None,

    "Croft Manor": 1,
    "Croft Manor (3)" : 3,
    "Croft Manor (5)" : 5,
    "Croft Manor (11)" : 11,
    "Bolivia, Beginning" : 2,
    "Peru, Beginning" : 4,
    "Peru Past, Excavation Site" : 15,
    "Peru Present, Excavation Site" : 16,
    "Peru, Motorbike Chase" : 17,
    "Japan, Beginning" : 6,
    "Ghana, Beginning" : 7,
    "Ghana, Beginning" : 14,
    # 8 is unknown
    "Kazakhstan, Beginning" : 9,
    "Khazakhstan, Motorbike" : 18,
    "England, Beginning" : 10,
    "Nepal, Beginning" : 12,
    "Bolivia Redux, Beginning" : 13,
}

OutfitChoices = {
    "Default" : None,

    "Legend" : "lara",
    "Legend Union Jack": "lara_alt",
    "Legend Black":"lara_alta",
    "Legend Blue": "lara_altb",
    "Legend Pink": "lara_altc",
    "Biker": "lara_biker",
    "Biker Red": "lara_biker_alt",
    "Biker - No Jacket": "lara_biker_nj",
    "Bikini (white)": "lara_bikini",
    "Bikini (Black)": "lara_bikini_alt",
    "Catsuit": "lara_catsuit",
    "Snowsuit":"lara_catsuit_snow",
    "Classic Green":"lara_classic",
    "Classic White": "lara_classic_alt",
    "Evening Dress (Buggy outside of Japan level)":"lara_evening",
    "Evening Ripped": "lara_evening_alt",
    "Evening with Dragon Tatoo":"lara_evening_alta",
    "Evening Red": "lara_evening_red",
    "Goth": "lara_goth",
    "Goth Lace Shirt": "lara_goth_alt",
    "Special Forces":"lara_special_forces",
    "Special Forces Urban": "lara_special_forces_alt",
    "Sport": "lara_sport",
    "Sport Green":"lara_sport_alt",
    "Suit":"lara_suit",
    "Suit Cream": "lara_suit_alt",
    "Winter": "lara_winter",
    "Winter - No Jacket": "lara_winter_nj",
    "Winter Orange":"lara_winter_alt",
    "Winter Orange - No Jacket": "lara_winter_alt_nj",
    "Winter Pink": "lara_winter_alta",
    "Winter Pink - No Jacket": "lara_winter_alta_nj",
    "Young Lara (from Flashback)":"lara_young",
    "Amanda": "amanda_player",
    "Amanda Winter": "amanda_player_alt"
}

AdvancedOptions = [
    ("-DRAWMONSTERATTACK", "Draw monster attack" , False),
    ("-DRAWMONSTERCOMBAT", "Draw monster combat", False),
    ("-EASYCHEAT", "Easy Cheat mode", False),
    ("-FONTNAME", "Font name", True),
    ("-CHAPTERVARS", "Chapter variables", True),
    ("-MAINMENU", "Show Main Menu", False),
    ("-NOHINTS", "Dont' show hints", False),
    ("-NOMONSTERATTACK", "No monster attack", False),
    ("-NOTRACE", "No trace", False),
    ("-NOVIBRATION", "No vibration", False),
    ("-NOHEALTH", "God Mode", False),
    ("-NOMONSTERHEALTH", "No monster health", False),
]

class MainFrame(TrlScuMainFrame):
    def __init__(self):
        TrlScuMainFrame.__init__(self, None)
        self.__m_current_outfit = None
        self.__m_current_level = None
        self.__m_current_adv_opts = {}
        self._m_outfit_boxes = []
        self._m_devopts_controls = {}
        self._InitMainOptions()
        self._InitAdvancedOptions()
        self._FindLegend()
        self.Fit()

    def _InitMainOptions(self):
        for name, id in LevelChoices.items():
            self.m_level_choice.Append(name, id)
        self.m_level_choice.Select(0)
        
        
        is_first = True
        for name, id in OutfitChoices.items():
            if is_first:
                flags = wx.RB_GROUP
            else:
                flags = 0
            is_first = False
            outfit_button = wx.RadioButton( self.m_outer_radio_sizer.GetStaticBox(), wx.ID_ANY, name, wx.DefaultPosition, wx.DefaultSize, flags )
            outfit_button.Bind( wx.EVT_RADIOBUTTON, self.OnOutfitChoice)
            self._m_outfit_boxes.append(outfit_button)
            self.m_outfit_sizer.Add( outfit_button, 0, wx.ALL, 5 )
        self.m_outer_radio_sizer.Layout()
        
    def _InitAdvancedOptions(self):
        self._m_devopts_controls = {}
        for (key, caption, has_parameter) in AdvancedOptions:
            text_box = None
            check_box = wx.CheckBox(self.m_outer_dev_opts_sizer.GetStaticBox(), wx.ID_ANY, caption, wx.DefaultPosition, wx.DefaultSize, 0, name=key)
            check_box.SetToolTip(key)
            check_box.Bind(wx.EVT_CHECKBOX, self.OnToggleAdvanced)
            self.m_inner_dev_opts_content_sizer.Add( check_box, 0, wx.ALL, 5 )
            if has_parameter:
                text_box = wx.TextCtrl( self.m_outer_dev_opts_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
                text_box.Enabled = False
                self.m_inner_dev_opts_content_sizer.Add( text_box, 0, wx.ALL|wx.EXPAND, 5 )
            else:
                self.m_inner_dev_opts_content_sizer.Add( (0, 0), 0, wx.ALL, 5 )
            self._m_devopts_controls[key] =  (check_box, text_box)
        self.m_outer_dev_opts_sizer.Layout()
        
    def _FindLegend(self):  
        if not have_winreg:
            return
        try:
            aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            aKey = winreg.OpenKey(aReg, r"SOFTWARE\"Crystal Dynamics\Tomb Raider: Legend")
            val = winreg.QueryValueEx(aKey, "InstallPath")
            self.SetLegendExecutable(os.path.join(val, "tr7.exe"))
        except Exception as e:
            wx.MessageBox(
                "Could not auto-detect TR Legend:\n\n%s" % (str(e), ),
                "Auto detection failed",
                wx.ICON_WARNING)
        
    def SetLegendExecutable(self, exe_path):
        exe_path = os.path.abspath(exe_path)
        self.m_exe_picker.SetPath(exe_path)
        exe_version = self.GetExecutableVersion(exe_path)
        exe_version_string = ".".join((str(x) for x in exe_version))
        if exe_version < (1, 2, 0, 0):
            wx.MessageBox("Legend Executable with version < 1.2 detected (%s).\n"
                          "This SCU will not work with the provided executable." % (
                            exe_version_string,),
                            "Wrong game version", wx.ICON_WARNING)
        self.m_version_display_text.SetValue(exe_version_string)
        
    def GetExecutableVersion(self, filename):
        if not have_win32api:
            wx.MessageBox("No api")
            return 0, 0, 0, 0
        try:
            info = GetFileVersionInfo(filename, "\\")
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            return HIWORD (ms), LOWORD (ms), HIWORD (ls), LOWORD (ls)
        except:
            return 0,0,0,0
    
    def OnExeSelected(self, event):
        self.SetLegendExecutable(event.GetPath())
    
    def OnOutfitChoice(self, evt):
        self.__m_current_outfit = OutfitChoices[evt.GetEventObject().GetLabelText()]
        
    def OnSelectLevel(self, event):
        self.__m_current_level = self.m_level_choice.GetClientData(event.GetSelection())

    def OnToggleAdvanced(self, event):
        key = event.GetEventObject().GetName()
        (check_box, text_box) = self._m_devopts_controls[key]
        if text_box:
            text_box.Enabled = check_box.IsChecked()
            
    def _GetAdvancedOptions(self):
        opts = []
        for key, (check_box, text_box) in self._m_devopts_controls.items():
            if check_box.IsChecked():
                opts.append(key)
                if text_box:
                    opts.append('"%s"' % (text_box.GetValue(), ))
        return opts
        
    def _GetCommandLineOptions(self):
        options = []
        if self.__m_current_level:
            options.extend(["-NOMAINMENU", "-CHAPTER", "%d" % (self.__m_current_level, )])
        if self.__m_current_outfit:
            options.extend(["-PLAYER", self.__m_current_outfit])
        options.extend(self._GetAdvancedOptions())
        return options

    def _WriteConfig(self, legend_install_dir):
        config_dir = os.path.join(legend_install_dir, "TR7", "GAME", "PC")
        if not os.path.isdir(config_dir):
            try:
                os.makedirs(config_dir)
            except Exception as e:
                raise Exception("Could not create config directory '%s': %s",
                    (config_dir, str(e)))
        command_line_args = self._GetCommandLineOptions()
        config_file_path = os.path.join(config_dir, "TR7.arg")
        with open(config_file_path, "w+") as config_file:
            config_file.write(" ".join(command_line_args))
        
    def _LaunchGame(self, exe_path):
        p = subprocess.Popen(
            executable=exe_path, 
            args=[],
            cwd=os.path.dirname(exe_path))
        # p.wait()
        
    def OnRun(self, event):
        try:
            exe_path = self.m_exe_picker.GetPath()
            if not exe_path:
                raise Exception("Please set the Tomb Raider Legend executable path!");
            if not os.path.isfile(exe_path):
                raise Exception("Tomb Raider Legend executable was not found at '%s'!" % (exe_path, ))
            legend_install_dir = os.path.dirname(exe_path)
            self._WriteConfig(legend_install_dir)
            self._LaunchGame(exe_path)
        except Exception as e:
            wx.MessageBox("%s" % (e, ), "Error launching TR Legend", wx.ICON_ERROR)
            traceback.print_exc()
        

class Application(wx.App):

    def OnInit(self):
        self._m_main_frame = MainFrame()
        self.SetTopWindow(self._m_main_frame)
        self._m_main_frame.Show()
        return True
        
    def Start(self):
        self.MainLoop()

THE_APP = None
def main():
    THE_APP = Application()
    THE_APP.Start()


if __name__ == "__main__":
    main()