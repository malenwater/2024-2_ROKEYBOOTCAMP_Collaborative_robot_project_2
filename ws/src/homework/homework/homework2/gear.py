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
    import util

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
            set_digital_output,
            get_digital_input,
            wait,
        )

        from DR_common2 import posx

    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return

    # 초기 위치
    JReady = [0, 0, 90, 0, 90, 0]
    pick = posx([423.215, -154.955, 138.865, 160.242, 179.93, 167.995])
    place = posx([429.157, 144.867, 138.865, 173.2, 179.898, -179.038])
    force_place = posx([429.182, 144.899, 60.823, 167.352, 179.915, 175.111])

    while rclpy.ok():
        # 초기 위치로 이동
        util.grip_without_wait()
        movej(JReady, vel=VELOCITY, acc=ACC)
        util.grip_flow(pick)
        util.release_flow(place,force_place)
        break
    rclpy.shutdown()
    print("end")


if __name__ == "__main__":
    main()
