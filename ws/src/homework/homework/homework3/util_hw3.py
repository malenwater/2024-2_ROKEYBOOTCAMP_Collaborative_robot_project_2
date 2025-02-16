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
        mwait,
        amove_periodic,
        trans,
        wait,
        get_current_posx,
        release_force,
        release_compliance_ctrl,
        check_force_condition,
        task_compliance_ctrl,
        set_desired_force,
        set_tool,
        check_position_condition,
        set_tcp,
        parallel_axis,
        movej,
        move_periodic,
        movel,
        DR_FC_MOD_REL,
        DR_AXIS_Z,
        DR_TOOL,
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
    
    
def grip_flow(pick1,pick2):
    print(f"grip_flow start")
    print(f"grip_flow {pick1} {pick2}")
    grip_without_wait()
    movel(pick1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    movel(pick2, vel=VELOCITY, acc=ACC, ref=DR_BASE)

    task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
    set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
    while not check_force_condition(DR_AXIS_Z, max=8):
        pass
    print("current position1 : ", get_current_posx())
    pos_1 = get_current_posx()
    pos_1 = pos_1[0]
    pos_1[2] -= 10
    print("current position1 : ", pos_1)
    release()
    print("current release : ", pos_1)
    release_compliance_ctrl()
    
    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    delta_2 = [0, 0, 100 - pos_1[2], 0, 0, 0]
    pos_1 = trans(pos_1, delta_2, DR_BASE, DR_BASE) 
    print("current movel : ", pos_1)
    grip()
    print("current grip : ", pos_1)
    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    
    print(f"grip_flow end")

def release_flow(place1,place2):
    print(f"release_flow start")
    print(f"release_flow {place1}")
    movel(place1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    movel(place2, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    
    task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
    set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
    while not check_force_condition(DR_AXIS_Z, max=8):
        pass
    print("current position1 : ", get_current_posx())
    release_compliance_ctrl()
    release()
    parallel_axis([0,0,-1],DR_AXIS_Z,DR_AXIS_Z)
    grip()
    pos_1 = get_current_posx()
    pos_1 = pos_1[0]
    delta_2 = [0, 0, 100 - pos_1[2], 0, 0, 0]
    pos_1 = trans(pos_1, delta_2, DR_BASE, DR_BASE) 
    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    print(f"release_flow end")
    
def chagne_trans_50(place):
    print(f"chagne_trans_50 start")
    final = place
    final[1] = final[1] + 50
    print(f"chagne_trans_50 {place}")
    print(f"chagne_trans_50 {final}")
    print(f"chagne_trans_50 end")
    return final

def place_other_place(place_final):
    print(f"place_other_place strat")
    movel(place_final, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    
    task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
    set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
    while not check_force_condition(DR_AXIS_Z, max=8):
        pass

    release_compliance_ctrl()
    release()
    
    delta_2 = [0, 0, 100 - place_final[2], 0, 0, 0]
    pos_1 = trans(place_final, delta_2, DR_BASE, DR_BASE) 
    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    
    print(f"place_other_place end")
print("end util")
