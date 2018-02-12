
import os
import subprocess
import traceback
import wx
import wx.adv

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

import __version__
from gui.trl_scu_base import TrlScuMainFrame


LevelChoices = (
    (None, "Main Menu"),

    (1, "Croft Manor"),
    (2, "Bolivia - Tiwanaku"),
    (3, "Croft Manor"),
    (4, "Peru - Return to Paraiso"),
    (15, "Peru - Excavation Site (Flashback)"),
    (16, "Peru - Excavation Site (Present)"),
    (17, "Peru - Motorbike Chase"),
    (5, "Croft Manor"),
    (6, "Japan"),
    (7, "Ghana"),
    (14, "Ghana"),
    # 8 is unknown
    (9, "Kazakhstan - Project Carbonek"),
    (18, "Khazakhstan, Motorbike Chase"),
    (10, "England - King Arthur's Tomb"),
    (11, "Croft Manor"),
    (12, "Nepal - The Ghalali Key"),
    (13, "Bolivia Redux"),
)

OutfitChoices = (
    (None, "Default"),

    ("lara",                    "Legend" ),
    ("lara_alt",                "Legend Union Jack"),
    ("lara_alta",               "Legend Black"),
    ("lara_altb",               "Legend Blue"),
    ("lara_altc",               "Legend Pink"),
    ("lara_biker",              "Biker"),
    ("lara_biker_alt",          "Biker Red"),
    ("lara_biker_nj",           "Biker - No Jacket"),
    ("lara_bikini",             "Bikini (white)"),
    ("lara_bikini_alt",         "Bikini (Black)"),
    ("lara_catsuit",            "Catsuit"),
    ("lara_catsuit_snow",       "Snowsuit"),
    ("lara_classic",            "Classic Green"),
    ("lara_classic_alt",        "Classic White"),
    ("lara_evening",            "Evening Dress (Buggy outside of Japan level)"),
    ("lara_evening_alt",        "Evening Ripped"),
    ("lara_evening_alta",       "Evening with Dragon Tattoo"),
    ("lara_evening_red",        "Evening Red"),
    ("lara_goth",               "Goth"),
    ("lara_goth_alt",           "Goth Lace Shirt"),
    ("lara_special_forces",     "Special Forces"),
    ("lara_special_forces_alt", "Special Forces Urban"),
    ("lara_sport",              "Sport"),
    ("lara_sport_alt",          "Sport Green"),
    ("lara_suit",               "Suit"),
    ("lara_suit_alt",           "Suit Cream"),
    ("lara_winter",             "Winter"),
    ("lara_winter_nj",          "Winter - No Jacket"),
    ("lara_winter_alt",         "Winter Orange"),
    ("lara_winter_alt_nj",      "Winter Orange - No Jacket"),
    ("lara_winter_alta",        "Winter Pink"),
    ("lara_winter_alta_nj",     "Winter Pink - No Jacket"),
    ("lara_young",              "Young Lara (from Flashback)"),
    ("amanda_player",           "Amanda"),
    ("amanda_player_alt",       "Amanda Winter"),
)

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
        self.__m_outfit_to_id_map = {}
        self.__m_current_level = None
        self.__m_current_adv_opts = {}
        self.__m_outfit_boxes = []
        self.__m_devopts_controls = {}
        self._InitMainOptions()
        self._InitAdvancedOptions()
        self._FindLegend()
        self.Fit()

    def _InitMainOptions(self):
        for id, name in LevelChoices:
            item_name = ("%s (%d)" % (name, id)) if id is not None else name
            self.m_level_choice.Append(item_name, id)
        self.m_level_choice.Select(0)


        is_first = True
        for id, name in OutfitChoices:
            if is_first:
                flags = wx.RB_GROUP
            else:
                flags = 0
            is_first = False
            outfit_button = wx.RadioButton( self.m_outer_radio_sizer.GetStaticBox(), wx.ID_ANY, name, wx.DefaultPosition, wx.DefaultSize, flags )
            outfit_button.Bind( wx.EVT_RADIOBUTTON, self.OnOutfitChoice)
            self.__m_outfit_boxes.append(outfit_button)
            self.__m_outfit_to_id_map[outfit_button.GetId()] = id
            self.m_outfit_sizer.Add( outfit_button, 0, wx.ALL, 5 )
        self.m_outer_radio_sizer.Layout()

    def _InitAdvancedOptions(self):
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
            self.__m_devopts_controls[key] =  (check_box, text_box)
        self.m_outer_dev_opts_sizer.Layout()

    def _FindLegend(self):
        if not have_winreg:
            return
        try:
            aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            aKey = winreg.OpenKey(aReg, r"SOFTWARE\Crystal Dynamics\Tomb Raider: Legend")
            val = winreg.QueryValueEx(aKey, "InstallPath")[0]
            self.SetLegendExecutable(os.path.join(val, "trl.exe"))
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
        self.__m_current_outfit = self.__m_outfit_to_id_map[evt.GetEventObject().GetId()]

    def OnSelectLevel(self, event):
        self.__m_current_level = self.m_level_choice.GetClientData(event.GetSelection())

    def OnToggleAdvanced(self, event):
        key = event.GetEventObject().GetName()
        (check_box, text_box) = self.__m_devopts_controls[key]
        if text_box:
            text_box.Enabled = check_box.IsChecked()

    def OnSaveSettings(self, event):
        self._WriteConfig()

    def OnLoadSettings(self, event):
        wx.MessageBox("Sorry, not implemented yet.")

    def OnReset(self, event):
        config_path = self._GetConfigFilePath()
        if not os.path.exists(config_path):
            return
        res = wx.MessageBox("This will remove the file '%s' from your computer.\n\nDo you wish to continue?" % (config_path, ),
            "Confirmation", wx.ICON_INFORMATION | wx.YES_NO)
        if res != wx.YES:
            return
        try:
            os.unlink(config_path)
        except Exception as e:
            wx.MessageBox("Error while removing '%s': %s" % (config_path, str(e)), "Warning", wx.ICON_ERROR)
            
    def OnAbout(self, event):
        info = wx.adv.AboutDialogInfo()
        info.Name = __version__.ProgramName
        info.Version = __version__.Version
        info.Copyright = __version__.Copyright
        info.Description = __version__.Description
        info.WebSite = __version__.ProjectSite
        info.Developers = __version__.Contributers
        info.License = __version__.License
        # Show the wx.AboutBox
        wx.adv.AboutBox(info)


    def _GetAdvancedOptions(self):
        opts = []
        for key, (check_box, text_box) in self.__m_devopts_controls.items():
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

    def _GetConfigFilePath(self):
        exe_path = self._GetTombRaiderExecutable()
        if not exe_path:
            raise Exception("Please set the Tomb Raider Legend executable path!");
        legend_install_dir = os.path.dirname(exe_path)
        return os.path.join(os.path.splitdrive(legend_install_dir)[0] + os.sep, "TR7", "GAME", "PC", "TR7.arg")

    def _GetTombRaiderExecutable(self):
        return self.m_exe_picker.GetPath()

    def _WriteConfig(self):
        command_line_args = self._GetCommandLineOptions()

        config_file_path = self._GetConfigFilePath()
        config_dir = os.path.dirname(config_file_path)
        if not os.path.isdir(config_dir):
            try:
                os.makedirs(config_dir)
            except Exception as e:
                raise Exception("Could not create config directory '%s': %s",
                    (config_dir, str(e)))
        with open(config_file_path, "w+") as config_file:
            config_file.write(" ".join(command_line_args))

    def _LaunchGame(self):
        exe_path = self._GetTombRaiderExecutable()
        if not os.path.isfile(exe_path):
            raise Exception("Tomb Raider Legend executable was not found at '%s'!" % (exe_path, ))

        p = subprocess.Popen(
            executable=exe_path,
            args=[],
            cwd=os.path.dirname(exe_path))

    def OnRun(self, event):
        try:
            self._WriteConfig()
            self._LaunchGame()
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