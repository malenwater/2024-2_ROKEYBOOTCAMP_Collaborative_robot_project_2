# 기준 좌표 (base_pose): (x, y, z, roll, pitch, yaw)
# 예를 들어, 기준 좌표가 (100, 100, 50, 0, 0, 0)라고 가정
base_pose = (400.7184753417969, 147.26148986816406, 120, 170, -180, 169)

# Pick 영역의 셀 간 간격 (cm 단위)
pick_delta_x = 50  # 열 간 간격
pick_delta_y = -50  # 행 간 간격

# Place 영역은 기준 좌표에서 x축으로 추가 오프셋이 적용됨
place_offset_x = -151.094464779  # Place 영역의 가장 왼쪽 아래 셀은 base_pose로부터 x축으로 15cm 떨어짐
place_delta_x = 50    # 열 간 간격
place_delta_y = -50    # 행 간 간격

def get_pick_robot_pose(row, col):
    """
    Pick 영역에서 주어진 그리드 위치 (행, 열)에 대한 로봇의 6자유도 좌표를 계산합니다.
    row: 행 번호 (0부터 시작)
    col: 열 번호 (0부터 시작)
    """
    x = base_pose[0] + row * pick_delta_x
    y = base_pose[1] + col * pick_delta_y
    z = base_pose[2]
    roll, pitch, yaw = base_pose[3], base_pose[4], base_pose[5]
    return [x, y, z, roll, pitch, yaw]

def get_place_robot_pose(row, col):
    """
    Place 영역에서 주어진 그리드 위치 (행, 열)에 대한 로봇의 6자유도 좌표를 계산합니다.
    Place 영역의 기준점은 base_pose에서 x축으로 15cm 떨어진 위치에서 시작합니다.
    row: 행 번호 (0부터 시작)
    col: 열 번호 (0부터 시작)
    """
    x = base_pose[0] + row * place_delta_x
    y = base_pose[1] + place_offset_x + col * place_delta_y
    z = base_pose[2]
    roll, pitch, yaw = base_pose[3], base_pose[4], base_pose[5]
    return [x, y, z, roll, pitch, yaw]

# 예시: 각 함수의 결과 출력
print("Pick 영역 좌표 예시:")
def get_pos_block_pick():
    return_arrray = []
    for row in range(3):
        for col in range(3):
            pose = get_pick_robot_pose(row, col)
            return_arrray.append(pose)
            # print(f"Pick 셀 ({row}, {col}): {pose}")
    return return_arrray
print("\nPlace 영역 좌표 예시:")
def get_pos_block_place():
    return_arrray = []
    for row in range(3):
        for col in range(3):
            pose = get_place_robot_pose(row, col)
            return_arrray.append(pose)
            # print(f"Place 셀 ({row}, {col}): {pose}")
    return return_arrray
