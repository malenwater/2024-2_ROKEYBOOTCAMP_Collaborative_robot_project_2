# pick and place in 1 method. from pos1 to pos2 @20241104

import rclpy
import DR_init
# for single robot
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 60, 60

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

OFF, ON = 0, 1


def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("force_control", namespace=ROBOT_ID)

    DR_init.__dsr__node = node
    from ..homework4 import util_hw4
    # import util_hw4
    try:
        from DSR_ROBOT2 import (
            trans,
            get_current_posx,
            release_compliance_ctrl,
            check_force_condition,
            task_compliance_ctrl,
            set_desired_force,
            set_tool,
            set_tcp,
            movej,
            movel,
            DR_FC_MOD_REL,
            DR_AXIS_Z,
            DR_BASE,
            DR_TOOL,
            set_digital_output,
            get_digital_input,
            wait,
        )

        from DR_common2 import posx

    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return

    # 초기 위치
    JReady = posx([367.23846435546875, 3.2307586669921875, 220.86367797851562, 82.57035064697266, 179.97665405273438, 83.04486083984375])
    pick1 = posx([273.209, -178.614, 214.596, 141.998, 179.98, 140.073])
    place1 = posx([505.650146484375, -1.451927900314331, 100.67518615722656,  141.998, 179.98, 140.073])
    count_cup = 0
    while rclpy.ok():
        # 초기 위치로 이동
        movel(JReady, vel=VELOCITY, acc=ACC, ref=DR_BASE)
        # util_hw4.grip_flow(pick1,count_cup )
        # util_hw4.release_flow(place1)
        util_hw4.put_3cup(place1,pick1,count_cup)
        # util_hw4.put_6cup(place1,pick1,count_cup)
        break
    rclpy.shutdown()
    print("end")


if __name__ == "__main__":
    main()
