import td
import tdu


class PlaybackExt:

    def __init__(self, owner_comp, tdotio_stack):
        self.owner_comp = owner_comp
        self._comp_playback = self.owner_comp.op("comp_playback")
        self._constant_bg = self.owner_comp.op("constant_bg")
        self._track_master = td.op.Core.op("base_track_master")
        self.video_tracks = []
        self.a_clip = tdu.Dependency(str())
        self.b_clip = tdu.Dependency(str())

        self.__rebuild(tdotio_stack)

    def __rebuild(self, tdotio_stack):
        # garbage cleanup
        for track_clone in tdotio_stack.tracks:
            if isinstance(track_clone, td.baseCOMP):
                track_clone.destroy()

    def __add_video_tracks(self, tdotio_stack):
        node_y = self._constant_bg.nodeY + self._constant_bg.nodeHeight
        for tdotio_track in tdotio_stack.tracks:
            index = tdotio_stack.tracks.index(tdotio_track)
            container_track = self.owner_comp.create(td.baseCOMP, "video_track_{0:02d}_{1}".format(
                index, tdotio_track.name))

            # make clone
            container_track.par.clone = self._track_master.path
            container_track.outputConnectors[0].connect(self._comp_playback.inputConnectors[index])

            container_track.nodeY = node_y
            node_y -= container_track.nodeHeight

    def AddVideoTrack(self, tdotio_track):
        self.__add_video_tracks(tdotio_track)
