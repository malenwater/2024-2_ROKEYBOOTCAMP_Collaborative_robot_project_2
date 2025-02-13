import rclpy
import DR_init
import math

print("start util")
# for single robot
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 350, 350

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL
CUP_HEIGHT = -11.3
ROOT_3 = math.sqrt(3)

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

    task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
    set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
    while not check_force_condition(DR_AXIS_Z, max=8):
        pass
    print("current position1 : ", get_current_posx())
    pos_1 = get_current_posx()
    pos_1 = pos_1[0]
    pos_1[2] -= 8
    print("current position1 : ", pos_1)
    release()
    wait(0.25)
    print("current release : ", pos_1)
    release_compliance_ctrl()
    
    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    print("current movel : ", pos_1)
    grip()
    
    delta_2 = [0, 0, 105, 0, 0, 0]
    pos_1 = trans(pos_1, delta_2, DR_BASE, DR_BASE) 
    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    
    print(f"grip_flow end")

def release_flow(place1,size,pick,count):
    print(f"release_flow start")
    print(f"release_flow {place1} {size}")
    delta_2 = [-30, 0, size - place1[2], 0, 0, 0]
    pos_1 = posx(list(trans(place1, delta_2, DR_BASE, DR_BASE))) 
    xlist = [pos_1, place1]
    
    print(f"xlist {xlist}")
    movesx(xlist, vel=[VELOCITY, VELOCITY],time=0.8, acc=[ACC, ACC], vel_opt=DR_MVS_VEL_NONE)
    
    task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
    set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
    while not check_force_condition(DR_AXIS_Z, max=8):
        pass
    print("current position1 : ", get_current_posx())
    release_compliance_ctrl()
    release()
    
    delta_3 = [0, 0, CUP_HEIGHT * count, 0, 0, 0]
    pick_2 = posx(list(trans(pick, delta_3, DR_BASE, DR_BASE))) 
    
    xlist = [pos_1,pick,pick_2]
    movesx(xlist, vel=[VELOCITY, VELOCITY],time=0.8, acc=[ACC, ACC], vel_opt=DR_MVS_VEL_NONE)
    print(f"release_flow end")
    
def put_6bottom(place, pick, count_cup):
    print(f"put_6bottom start")
    print(f"put_6bottom {place} {pick} {count_cup}")
    x_1 = ROOT_3 * (-40)
    x_2 = ROOT_3 * (-80)
    put_1_delta = [0, 80, 0, 0, 0, 0]
    put_2_delta = [0, -80, 0, 0, 0, 0]
    put_3_delta = [x_1, 40, 0, 0, 0, 0]
    put_4_delta = [x_1, -40, 0, 0, 0, 0]
    put_5_delta = [x_2, 0, 0, 0, 0, 0]
      
    put1 = posx(list(trans(place, put_1_delta, DR_BASE, DR_BASE)))
    put2 = posx(list(trans(place, put_2_delta, DR_BASE, DR_BASE) ))
    put3 = posx(list(trans(place, put_3_delta, DR_BASE, DR_BASE) ))
    put4 = posx(list(trans(place, put_4_delta, DR_BASE, DR_BASE)))
    put5 = posx(list(trans(place, put_5_delta, DR_BASE, DR_BASE) ))
    
    put_list = [put1, place, put2, put3, put4, put5]
    count_cup_1 = count_cup
    for idx in put_list:
        print(f"put_6bottom {idx}")
        grip_flow(pick,count_cup_1)
        count_cup_1 += 1
        release_flow(idx,200,pick,count_cup_1)
        pass
    print(f"put_6bottom end")
    return count_cup_1

def put_3middle(place, pick, count_cup):
    print(f"put_3middle start")    
    print(f"put_3middle {place} {pick} {count_cup}")
    x_1 = ROOT_3 * (-40) / 3
    x_2 = ROOT_3 * (-40) + x_1
    put_1_delta = [x_1, 40, 94, 0, 0, 0]
    put_2_delta = [x_1, -40, 94, 0, 0, 0]
    put_3_delta = [x_2, 0, 94, 0, 0, 0]
      
    put1 = posx(list(trans(place, put_1_delta, DR_BASE, DR_BASE)))
    put2 = posx(list(trans(place, put_2_delta, DR_BASE, DR_BASE) ))
    put3 = posx(list(trans(place, put_3_delta, DR_BASE, DR_BASE) ))
    
    put_list = [put1, put2, put3]
    count_cup_1 = count_cup
    for idx in put_list:
        grip_flow(pick,count_cup_1)
        count_cup_1 += 1
        release_flow(idx,240.,pick,count_cup_1)
        pass
    print(f"put_3middle end")
    return count_cup_1

def put_top(place, pick, count_cup):
    print(f"put_top start")
    x_1 = (-80) * ROOT_3 / 3
    put_1_delta = [x_1, 0, 189, 0, 0, 0]
    put1 = posx(list(trans(place, put_1_delta, DR_BASE, DR_BASE)))
    count_cup_1 = count_cup
    grip_flow(pick,count_cup_1)
    release_flow(put1,330.,pick,count_cup_1)
    count_cup_1 += 1
    print(f"put_top end")
    return count_cup_1
    
def grip_flow_reverse(pick1,count):
    print(f"grip_flow start")
    print(f"grip_flow {pick1}")
    
    grip_without_wait()
    print(f"grip_flow change")
    # delta_2 = [0, 0, CUP_HEIGHT * count, 0, 0, 0]
    # pick1 = trans(pick1, delta_2, DR_BASE, DR_BASE) 
    # movel(pick1, vel=VELOCITY, acc=ACC, ref=DR_BASE)

    task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
    set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
    while not check_force_condition(DR_AXIS_Z, max=8):
        pass
    print("current position1 : ", get_current_posx())
    pos_1 = get_current_posx()
    pos_1 = pos_1[0]
    pos_1[2] -= 20
    pos_1[1] += 20
    print("current position1 : ", pos_1)
    release()
    print("current release : ", pos_1)
    release_compliance_ctrl()
    
    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    print("current movel : ", pos_1)
    
    parallel_axis([0,1,0],DR_AXIS_Z,ref=DR_BASE)
    grip()
    
    delta_2 = [0, 0, 110, 0, 0, 0]
    print("current movel : ", delta_2)
    pos_1 = trans(pos_1, delta_2, DR_BASE, DR_BASE) 
    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    
    print(f"grip_flow end")

def release_flow_reverse(place1):
    print(f"release_flow_reverse start")
    print(f"release_flow_reverse {place1}")
    
    delta_2 = [-30, 0, 40 , 0, 0, 0]
    pos_1 = posx(list(trans(place1, delta_2, DR_BASE, DR_BASE))) 
    xlist = [pos_1, place1]
    print(f"xlist {xlist}")
    movesx(xlist, vel=[VELOCITY, VELOCITY],time=0.8, acc=[ACC, ACC], vel_opt=DR_MVS_VEL_NONE)
    
    parallel_axis([0,-1,0],DR_AXIS_Z,ref=DR_BASE)
    
    pos_2 = posx(list(get_current_posx()[0]))
    delta_2 = [-1, -16, -20, 0, 0, 0]
    pos_1 = posx(list(trans(pos_2, delta_2, DR_BASE, DR_BASE))) 
    movel(pos_1, vel=VELOCITY, acc=ACC, ref=DR_BASE)
    
    task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
    set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
    while not check_force_condition(DR_AXIS_Z, max=8):
        pass
    release_compliance_ctrl()
    release()

    print(f"release_flow_reverse end")
    
def put_reverse(place,pick,count_cup):
    count_cup_1 = count_cup
    x_1 = (-80) * ROOT_3 / 3
    put_1_delta = [x_1, 0, 250, 0, 0, 0]
    put1 = posx(list(trans(place, put_1_delta, DR_BASE, DR_BASE)))
    
    grip_flow_reverse(pick,count_cup_1)
    release_flow_reverse(put1)
    pass

print("end util")
