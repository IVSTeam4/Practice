# 카메라를 이용해 QR code 인식 (ex.7-2)
from base_camera import BaseCamera
import cv2

class QRCodeCamera(BaseCamera):
    @staticmethod
    def frames():
        det = cv2.QRCodeDetector()

        # 카메라 객체 생성
        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        
        while True:
            # 카메라 프레임 읽기
            _, frame = camera.read()
            info, box_coordinates, _ = det.detectAndDecode(frame)

            # QR code 정보 출력
            if box_coordinates is None:
                print("No Code")
            else:
                print(info)
            
            # QR code 주변에 사각형을 그리기
            if box_coordinates is not None:
                box_coordinates = [box_coordinates[0].astype(int)]
                n = len(box_coordinates[0])
                for i in range(n):
                    cv2.line(
                        frame,
                        tuple(box_coordinates[0][i]),
                        tuple(box_coordinates[0][(i+1)%n]),
                        (0, 255, 0),
                        3,
                    )
            yield cv2.imencode('.jpg', frame)[1].tobytes()