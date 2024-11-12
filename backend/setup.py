from setuptools import setup, find_packages

# requirements.txt에서 의존성을 읽어오기
def parse_requirements(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()

# 프로젝트 메타데이터와 설정 정보
setup(
    name='iam-monitor-app-backend',  # 패키지 이름
    version='0.1.0',  # 초기 버전
    description='IAM Monitor - AWS IAM Access Key 모니터링 애플리케이션의 백엔드',
    author='youngsam.lee',
    author_email='niceyslee@gmail.com',
    packages=find_packages('src'),  # src 아래의 모든 패키지 포함
    package_dir={'': 'src'},  # src 디렉토리를 루트로 설정
    install_requires=parse_requirements('requirements.txt'),  # 의존성 추가
    python_requires='>=3.6',  # Python 버전 요구사항
)