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
        movesx,
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
        DR_MVS_VEL_NONE,
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
    
    
def grip_flow(pick1,count):
    print(f"grip_flow start")
    print(f"grip_flow {pick1}")
    grip_without_wait()
    movel(pick1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    delta_2 = [0, 0, -10 * count, 0, 0, 0]
    pick1 = trans(pick1, delta_2, DR_BASE, DR_BASE) 
    movel(pick1, vel=VELOCITY, acc=ACC, ref=DR_BASE)

    task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
    set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
    while not check_force_condition(DR_AXIS_Z, max=8):
        pass
    print("current position1 : ", get_current_posx())
    pos_1 = get_current_posx()
    pos_1 = pos_1[0]
    pos_1[2] -= 7
    print("current position1 : ", pos_1)
    release()
    print("current release : ", pos_1)
    release_compliance_ctrl()
    
    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    print("current movel : ", pos_1)
    grip()
    
    delta_2 = [0, 0, 110, 0, 0, 0]
    pos_1 = trans(pos_1, delta_2, DR_BASE, DR_BASE) 
    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    
    print(f"grip_flow end")

def release_flow(place1):
    print(f"release_flow start")
    print(f"release_flow {place1}")
    delta_2 = [0, 0, 220 - place1[2], 0, 0, 0]
    pos_1 = posx(list(trans(place1, delta_2, DR_BASE, DR_BASE))) 
    xlist = [pos_1, place1]
    print(f"xlist {xlist}")
    movesx(xlist, vel=[100, 30], acc=[200, 60], vel_opt=DR_MVS_VEL_NONE)
    # movel(place1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    
    task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
    set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
    while not check_force_condition(DR_AXIS_Z, max=8):
        pass
    print("current position1 : ", get_current_posx())
    release_compliance_ctrl()
    release()
    
    # pos_1 = get_current_posx()
    # pos_1 = pos_1[0]

    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    # print(f"release_flow end")
    
def put_3cup(place,pick):
    print(f"put_3cup start")
    print(f"put_3cup {place} {pick}")
    put_1_delta = [0, -40, 0, 0, 0, 0]
    put_2_delta = [0, 40, 0, 0, 0, 0]
    put_3_delta = [0, 0, 100, 0, 0, 0]
      
    put1 = posx(list(trans(place, put_1_delta, DR_BASE, DR_BASE)))
    put2 = posx(list(trans(place, put_2_delta, DR_BASE, DR_BASE) ))
    put3 = posx(list(trans(place, put_3_delta, DR_BASE, DR_BASE) ))
    put_list = [put1, put2, put3]
    count_cup = 0
    for idx in put_list:
        grip_flow(pick,count_cup)
        release_flow(idx)
        count_cup += 1
        pass
    print(f"put_3cup end")


def put_6cup(place,pick):
    print(f"put_6cup start")
    print(f"put_6cup {place} {pick}")
    put_1_delta = [0, -80, 0, 0, 0, 0]
    put_2_delta = [0, 80, 0, 0, 0, 0]
    put_3_delta = [0, 0, 100, 0, 0, 0]
      
    put1 = posx(list(trans(place, put_1_delta, DR_BASE, DR_BASE)))
    put2 = posx(list(trans(place, put_2_delta, DR_BASE, DR_BASE) ))
    put3 = posx(list(trans(place, put_3_delta, DR_BASE, DR_BASE) ))
    put_list = [place,put1, put2]
    count_cup = 0
    
    for idx in put_list:
        grip_flow(pick,count_cup)
        release_flow(idx)
        count_cup += 1
        pass
    
    print(f"put_6cup start put_3cup")
    put_3cup(put3,pick)
    print(f"put_6cup end")
    
print("end util")
