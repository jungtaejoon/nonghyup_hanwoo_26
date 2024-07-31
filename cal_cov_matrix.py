import pandas as pd
import numpy as np


def calculate_covariance_matrices(file_path, traits_columns):
    # 엑셀 파일에서 데이터 불러오기
    df = pd.read_excel(file_path)

    # 4개의 형질 데이터 추출
    traits_data = df.iloc[:, traits_columns]

    # 공분산 행렬 계산
    cov_matrix = np.cov(traits_data, rowvar=False)

    # 잔차 분산 행렬 계산 (형질 데이터의 잔차 구하기)
    residuals = traits_data - traits_data.mean()
    residual_cov_matrix = np.cov(residuals, rowvar=False)

    return cov_matrix, residual_cov_matrix


if __name__ == "__main__":
    # 사용자 입력 받기
    file_path = input("엑셀 파일 경로를 입력하세요: ")
    columns_input = input("형질이 위치한 열 번호를 쉼표로 구분하여 입력하세요 (예: 0,1,2,3): ")

    # 열 번호를 리스트로 변환
    traits_columns = [int(x) for x in columns_input.split(',')]

    # 공분산 행렬 및 잔차 분산 행렬 계산
    cov_matrix, residual_cov_matrix = calculate_covariance_matrices(file_path, traits_columns)

    # 결과 출력
    print("공분산 행렬:")
    print(cov_matrix)

    print("\n잔차 분산 행렬:")
    print(residual_cov_matrix)
