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

    pos = posx([400.53314208984375, 91.08312225341797, 120.66590881347656, 170.563720703125, -180.0, 169.79397583007812])
    # 초기 위치
    JReady = [0, 0, 90, 0, 90, 0]
    set_tool("Tool Weight_2FG")
    set_tcp("2FG_TCP")
        
    while rclpy.ok():
        # 초기 위치로 이동
        # grip()
        movej(JReady, vel=VELOCITY, acc=ACC)
        move_pos_1 = util.grip_flow(pos)
        move_pos_1 = posx(move_pos_1.tolist())
        print(type(move_pos_1))
        print(move_pos_1)
        util.release_flow(move_pos_1)
        
    rclpy.shutdown()
    print("end")


if __name__ == "__main__":
    main()
