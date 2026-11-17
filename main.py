
from src.mode_input import run_input_mode
from src.mode_json import run_json_mode


def main():
    while True:
        print("\n=== Mini NPU Simulator ===")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        print("0. 종료")

        try:
            choice = input("선택: ").strip()

            if choice == "1":
                run_input_mode()

            elif choice == "2":
                run_json_mode()

            elif choice == "0":
                print("프로그램을 종료합니다.")
                break

            else:
                print("잘못된 선택입니다. 다시 입력하세요.")

        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 안전하게 종료합니다.")
            break


if __name__ == "__main__":
    main()
