# pick and place in 1 method. from pos1 to pos2 @20241104

import rclpy
import DR_init
import get_pos
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
    col_counts = [0, 0, 0]
    set_tool("Tool Weight_2FG")
    set_tcp("2FG_TCP")
    picks = get_pos.get_pos_block_pick()
    places = get_pos.get_pos_block_place()
    print(f"pick {picks}")
    print(f"pick {len(picks)}")
    print(f"place {places}")
    print(f"place {len(places)}")
    while rclpy.ok():
        # 초기 위치로 이동
        for pick in picks:
            print(f"pick {pick}")
            print(f"pick {pick}")
            print(f"pick {pick}")
            pos = posx(pick)
            util.grip_without_wait()
            movej(JReady, vel=VELOCITY, acc=ACC)
            block_z = util.grip_flow(pos)
            
            if block_z < 45:
                size = 0
                col_counts[0] += 1
            elif block_z > 55 :
                size = 2
                col_counts[2] += 1
            else: 
                size = 1
                col_counts[1] += 1
            print(f"block_z {block_z}")
            print(f"size {size}")
            place = places[3 * size + col_counts[size] - 1]
            print(f"place {place}")
            place = posx(place)
            util.release_flow(place)
        break
    rclpy.shutdown()
    print("end")


if __name__ == "__main__":
    main()
