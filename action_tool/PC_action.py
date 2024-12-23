from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER

class Audio_control:

    def volume_control(self, plus=False, minus=False, step=0.2):

        # Получаем все аудиовыходы
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Получаем текущую громкость
        current_volume = volume.GetMasterVolumeLevelScalar()

        if minus:
            # Уменьшаем громкость на заданное количество единиц
            new_volume = max(0.0, current_volume - step)
        elif plus:
            new_volume = max(0.0, current_volume + step)

        # Устанавливаем новую громкость
        volume.SetMasterVolumeLevelScalar(new_volume, None)

    def step_volume_stable(self, step):
        if step is False:
            step = 0.2
        elif step > 10:
            step = step / 100
        elif step <= 10:
            step = step / 10
        elif 0 >= step > 100:
            step = 1
        else:
            step = 0
        return step
    def volume_down_step(self, step):
        self.volume_control(minus=True, step=self.step_volume_stable(step))

    def volume_high_step(self, step):
        self.volume_control(minus=True, step=self.step_volume_stable(step))