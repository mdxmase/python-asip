from python_asip_client.boards.serial_board import SerialBoard
from python_asip_client.services.bump_service import BumpService
from python_asip_client.services.ir_service import IRService
from python_asip_client.services.motor_service import MotorService
from python_asip_client.services.lcd_service import LCDService
from python_asip_client.services.distance_service import DistanceService
import sys


class SerialMirtoRobot(SerialBoard):

    def __init__(self, tcp_handler=None, enable_serial_listening=False):
        SerialBoard.__init__(self, tcp_handler, enable_serial_listening)

        # Creating instances of services
        self._motors = [MotorService(0, self.asip), MotorService(1, self.asip)]  # init 2 motors (wheels)
        self._irs = [IRService(0, self.asip), IRService(1, self.asip), IRService(2, self.asip)]  # init 3 IR sensors
        self._bumps = [BumpService(0, self.asip), BumpService(1, self.asip)]  # init 2 bump sensors
        self._lcd = [LCDService(0, self.asip)]  # Init lcd service
        self._distance = [DistanceService(0, self.asip)]  # Init distance service
        sys.stdout.write("DEBUG: instances of services created\n")

        # Setting reporting interval of sensors
        reporting_interval = 25
        self._motors[0].enable_encoder()
        self._motors[1].enable_encoder()
        self._irs[0].set_reporting_interval(reporting_interval)
        self._irs[1].set_reporting_interval(reporting_interval)
        self._irs[2].set_reporting_interval(reporting_interval)
        self._bumps[0].set_reporting_interval(reporting_interval)
        self._bumps[1].set_reporting_interval(reporting_interval)
        self._distance[0].set_reporting_interval(reporting_interval)
        sys.stdout.write("DEBUG: reporting interval set to {}\n".format(reporting_interval))

        #  Adding services
        self.get_asip_client().add_service(self._motors[0].get_service_id(), self._motors)
        # self.get_asip_client().add_service(self._encoders[0].get_service_id(), self._encoders)
        self.get_asip_client().add_service(self._irs[0].get_service_id(), self._irs)
        self.get_asip_client().add_service(self._bumps[0].get_service_id(), self._bumps)
        self.all_services = {"motors": self._motors, "irs": self._irs, "bumps": self._bumps, "lcd": self._lcd,
                             "distance": self._distance}
        sys.stdout.write("DEBUG: services added\nServices: {}".format(self.all_services.keys()))

    def get_services(self):
        return self.all_services
