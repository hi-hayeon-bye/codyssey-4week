import pickle

def manage_inventory():
    input_filename = 'Mars_Base_Inventory_List.csv'
    output_filename = 'Mars_Base_Inventory_danger.csv'
    binary_filename = 'Mars_Base_Inventory_List.bin'
    
    inventory_list = []
    header = ''

    # 1. CSV 파일 읽기 및 출력 (예외 처리)
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            header = f.readline().strip()  # 첫 줄(헤더) 저장
            print(f'--- {input_filename} 파일 내용 ---')
            print(header)
            
            for line in f:
                line = line.strip()
                if not line:
                    continue
                print(line)
                
                # 2. 리스트 객체로 변환
                parts = line.split(',')
                # 인화성 지수(마지막 열)를 계산을 위해 실수형으로 변환
                try:
                    parts[-1] = float(parts[-1])
                except ValueError:
                    parts[-1] = 0.0
                inventory_list.append(parts)
                
    except FileNotFoundError:
        print(f'에러: {input_filename} 파일이 없습니다.')
        return
    except Exception as e:
        print(f'에러 발생: {e}')
        return

    # 3. 인화성이 높은 순(내림차순)으로 정렬
    # x[4]는 Flammability 열을 의미함
    inventory_list.sort(key=lambda x: x[4], reverse=True)

    # 4. 인화성 지수 0.7 이상 필터링 및 출력
    danger_list = [item for item in inventory_list if item[4] >= 0.7]
    
    print('\n--- 인화성 지수 0.7 이상 목록 ---')
    for item in danger_list:
        print(item)

    # 5. 위험 목록을 CSV 포맷으로 저장
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(header + '\n')
            for item in danger_list:
                # 리스트를 다시 문자열로 변환 (' ' 작은따옴표 사용 규칙 준수)
                line = ','.join([str(x) for x in item])
                f.write(line + '\n')
        print(f'\n성공: {output_filename} 저장 완료')
    except IOError:
        print('에러: 파일을 저장할 수 없습니다.')

    # [보너스 과제] 이진 파일 저장 및 읽기
    try:
        # 이진 파일로 저장 (wb 모드)
        with open(binary_filename, 'wb') as f:
            pickle.dump(inventory_list, f)
        print(f'성공: {binary_filename} 이진 파일 저장 완료')

        # 이진 파일 읽기 (rb 모드)
        with open(binary_filename, 'rb') as f:
            loaded_data = pickle.load(f)
            print('\n--- 이진 파일(bin)에서 복구된 내용 ---')
            for row in loaded_data:
                print(row)
    except Exception as e:
        print(f'이진 파일 처리 중 오류: {e}')

if __name__ == '__main__':
    manage_inventory()