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
        amove_periodic,
        trans,
        get_current_posx,
        release_force,
        release_compliance_ctrl,
        check_force_condition,
        task_compliance_ctrl,
        set_desired_force,
        set_tool,
        set_tcp,
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
    
    
def grip_flow(pick):
    print(f"grip_flow start")
    print(f"grip_flow {pick}")
    release()
    movel(pick, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    print(f"grip_flow {pick}")
    delta_1 = [0,0,-100 , 0,0,0]
    move_pos = trans(pick, delta_1, DR_BASE, DR_BASE) 
    movel(move_pos, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    grip()
    movel(pick, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    print(f"grip_flow end")
    pass
def release_flow(place,force_place):
    print(f"release_flow start")
    print(f"grip_flow {place}")
    print(f"grip_flow {force_place}")
    movel(place, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    movel(force_place, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    
    task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
    set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)

    while not check_force_condition(DR_AXIS_Z, max=8):
        pass
    
    while True:
        release_force()
        release_compliance_ctrl()
        move_periodic(amp=[0, 0, 0, 0, 0, 8], period=2.0, atime=0.02, repeat=1, ref=DR_TOOL)
        print(f"move_periodic")
        task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
        set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
        
        pos = get_current_posx()[0]
        if not check_force_condition(DR_AXIS_Z, max=8):
            print(f"check_force_condition")
            while True:
                pos = get_current_posx()[0]
                if pos[2] < 45:
                    break
                elif check_force_condition(DR_AXIS_Z, max=8):
                    break
            if pos[2] < 45: 
                break
        else:
            print(f"False")
            continue

    # 높이 체크
    # 높이가 40 이하 break
    # 높이 40이상 움직이게
    print("current position2 : ", get_current_posx())
    print("current position2 : ", get_current_posx())
    print("current position2 : ", get_current_posx())
    release_force()
    release_compliance_ctrl()
    print("current position1 : ", get_current_posx())
    
    release()
    
    movel(place, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    print(f"release_flow end")
    pass
    
    
print("end util")
