import random

# 1. 9개의 블록 생성 (길이: 1, 2, 3이 각각 3개씩 있다고 가정)
# 각 블록은 (블록ID, 길이) 형태의 튜플로 표현합니다.
blocks = [("block" + str(i+1), length) for i, length in enumerate([1, 1, 1, 2, 2, 2, 3, 3, 3])]

# 2. 블록들을 무작위 순서로 섞습니다.
random.shuffle(blocks)
print("초기 랜덤 블록 순서:")
for b in blocks:
    print(b)
print()

# 3. 3x3 그리드를 생성합니다. (각 칸은 나중에 블록 ID로 채워집니다.)
# grid[row][col] 형태로 사용 (행: 0~2, 열: 0~2)
grid = [[None for _ in range(3)] for _ in range(3)]

# 4. 각 열에 이미 배치된 블록의 개수를 추적할 리스트 (인덱스 0: 길이 1, 1: 길이 2, 2: 길이 3)
col_counts = [0, 0, 0]

# 5. 랜덤 순서로 블록들을 하나씩 가져와서, 길이에 따른 컬럼에 배치합니다.
for block in blocks:
    block_id, block_length = block
    # 길이에 따른 컬럼: 길이 1 → 1열(인덱스 0), 2 → 2열(인덱스 1), 3 → 3열(인덱스 2)
    col = block_length - 1
    # 해당 열에서 다음으로 배치할 행은 현재 배치된 개수를 의미합니다.
    row = col_counts[col]
    print(col_counts)   
    # 3행까지 배치할 수 있으므로, row가 3 미만일 때만 배치합니다.
    if row < 3:
        grid[row][col] = block_id
        col_counts[col] += 1
        
        # 블록이 배치된 후, 현재 그리드 상태를 로그로 출력합니다.
        print(f"{block_id} (길이 {block_length})를 {col+1}열 {row+1}행에 배치했습니다.")
        print("현재 그리드 상태:")
        for r in grid:
            print(r)
        print("-" * 40)
    else:
        print(f"열 {col+1}은 이미 꽉 찼습니다. {block_id}를 배치할 수 없습니다.")

# 6. 최종 배치된 그리드를 출력합니다.
print("최종 그리드 배치:")
for r in range(3):
    print(grid[r])
