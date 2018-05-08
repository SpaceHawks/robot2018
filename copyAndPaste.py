class RMCHokuyoLidar(Localizer):
    def __init__(self, ui=None):
        super(RMCHokuyoLidar, self).__init__(ui)
        self.ANGLE_GAP.setValue(3)
        self.AVE_ANGLE_GAP.setValue(1.4)
        self.AVE_GAP_DX_DY.setValue(0.4)
        self.AVE_DIST_GAP.setValue(13)
        self.MARKER_LENGTH_MIN.setValue(750)
        self.MARKER_LENGTH_MAX.setValue(1000)
        self.MARKER_QUALITY_MAX .setValue(200)
        # self.ISO_QUALITY_LENGTH.setValue()