import rclpy
import DR_init

print("start util")
# for single robot
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 60, 60

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

OFF, ON = 0, 1
print("start util")
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
    
    
def wait_digital_input(sig_num):
    while not get_digital_input(sig_num):
        wait(0.5)
        print("Wait for digital input")
        pass

def release():
    set_digital_output(2, ON)
    set_digital_output(1, OFF)
    wait_digital_input(2)

def grip():
    release()
    set_digital_output(1, ON)
    set_digital_output(2, OFF)
    wait_digital_input(1)
    
def grip_without_wait():
    release()
    set_digital_output(1, ON)
    set_digital_output(2, OFF)
    


def grip_flow(move_pos):
    print("grip_flow")
    print(f"grip_flow { move_pos}")
    print(f"grip_flow { move_pos}")
    print(f"grip_flow { move_pos}")
    delta_1 = [0, 0, -55, 0, 0, 0]
    movel(move_pos, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    move_pos = trans(move_pos, delta_1, DR_BASE, DR_BASE) 
    movel(move_pos, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    
    task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
    set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
    while not check_force_condition(DR_AXIS_Z, max=8):
        pass
    print("current position1 : ", get_current_posx())
    pos_1 = get_current_posx()
    pos_1 = pos_1[0]
    block_z = pos_1[2]
    pos_1[2] -= 20
    print("current position1 : ", pos_1)
    release()
    print("current release : ", pos_1)
    release_compliance_ctrl()
    
    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    delta_2 = [0, 0, 120 - pos_1[2], 0, 0, 0]
    pos_1 = trans(pos_1, delta_2, DR_BASE, DR_BASE) 
    print("current movel : ", pos_1)
    grip()
    print("current grip : ", pos_1)
    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    return block_z

def release_flow(move_pos):
    # delta_3 = [0, -150, 0, 0, 0, 0]
    delta_1 = [0, 0, -55, 0, 0, 0]
    print("release_flow")
    print(type(move_pos))
    print(move_pos)
    # print(delta_3)
    # move_pos = trans(move_pos, delta_3, DR_BASE, DR_BASE) 
    movel(move_pos, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    move_pos = trans(move_pos, delta_1, DR_BASE, DR_BASE) 
    movel(move_pos, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    
    task_compliance_ctrl(stx=[3000, 3000, 3000, 200, 200, 200])
    set_desired_force(fd=[0, 0, -15, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
    while not check_force_condition(DR_AXIS_Z, max=13):
        pass
    print("current position1 : ", get_current_posx())
    pos_1 = get_current_posx()
    pos_1 = pos_1[0]
    delta_4 = [0, 0, 120 - pos_1[2], 0, 0, 0]
    pos_1 = trans(pos_1, delta_4, DR_BASE, DR_BASE) 
    release()
    release_compliance_ctrl()
    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    grip_without_wait()
    
print("end util")
