
import os
import wx

have_winreg = False
try:
    import _winreg
    have_winreg = True
except:
    pass
    
have_win32api = False
try:
    from win32api import GetFileVersionInfo, LOWORD, HIWORD
    have_win32api = True
except:
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
    "Evening Dress (Lara might not react)":"lara_evening",
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

class MainFrame(TrlScuMainFrame):
    def __init__(self):
        TrlScuMainFrame.__init__(self, None)
        self.__m_current_outfit = None
        self.__m_current_level = None
        self._InitLayout()
        self._FindLegend()

    def _InitLayout(self):
        for name, id in LevelChoices.items():
            self.m_level_choice.Append(name, id)
        self.m_level_choice.Select(0)
        
        self._m_outfit_boxes = []
        is_first = True
        for name, id in OutfitChoices.items():
            if is_first:
                flags = wx.RB_GROUP
            else:
                flags = 0
            is_first = False
            outfit_button = wx.RadioButton( self.m_outer_radio_sizer.GetStaticBox(), wx.ID_ANY, name, wx.DefaultPosition, wx.DefaultSize, flags )
            outfit_button.Bind( wx.EVT_RADIOBUTTON, lambda evt: self.OnOutfitChoice(evt, id))
            self._m_outfit_boxes.append(outfit_button)
            self.m_outfit_sizer.Add( outfit_button, 0, wx.ALL, 5 )

        self.m_outer_radio_sizer.Layout()
        self.Fit()
        
    def _FindLegend(self):  
        if not have_winreg:
            return
        try:
            aReg = _winreg.ConnectRegistry(None,HKEY_LOCAL_MACHINE)
            aKey = _winreg.OpenKey(aReg, r"SOFTWARE\"Crystal Dynamics\Tomb Raider: Legend")
            val = _winreg.QueryValueEx(aKey, "InstallPath")
            self.SetLegendExecutable(os.path.join(val, "trl.exe"))
        except _winreg.EnvironmentError:
            pass
        
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
    
    def OnOutfitChoice(self, evt, outfit):
        self.__m_current_outfit = outfit
        
    def OnSelectLevel(self, event):
        self.__m_current_level = self.m_level_choice.GetClientData(event.GetSelection())


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