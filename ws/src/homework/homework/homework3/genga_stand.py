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
    from ..homework3 import util_hw3
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
    set_tool("Tool Weight")
    set_tcp("GripperDA_v1")
    # 초기 위치
    JReady = [0, 0, 90, 0, 90, 0]
    pick1 = posx([419.975, 50.079, 69.93, 7.038173198699951, -179.99867248535156, 7.515153408050537])
    pick2 = posx([419.975, 50.079, 69.93, 89.495, 149.968, 89.972])
    place1 = posx([417.363, -214.612, 70.502, 89.495, 149.968, 89.972])
    place2 = posx([417.363, -214.612, 70.502, 89.459, -119.76, 90.034])
    place_final_1 = posx([316.939, -263.324, 70.989, 149.742, -179.994, 150.212])

    count_genga = 0
    while rclpy.ok():
        # 초기 위치로 이동
        movej(JReady, vel=VELOCITY, acc=ACC)
        util_hw3.grip_flow(pick1,pick2)
        util_hw3.release_flow(place1,place2)
        place_final = util_hw3.chagne_trans_50(place_final_1)
        count_genga += 1
        util_hw3.place_other_place(place_final)
        if count_genga == 4:
            break
    rclpy.shutdown()
    print("end")


if __name__ == "__main__":
    main()
