import cv2
import torch
import time
import matplotlib.pyplot as plt

p_timeframe = 0
new_timeframe = 0

midas = torch.hub.load(repo_or_dir="intel-isl/MiDaS", model="MiDaS_small", trust_repo=True)
midas.to('cuda')
midas.eval()

transforms = torch.hub.load(repo_or_dir="intel-isl/MiDaS", model="transforms", trust_repo=True)
transform = transforms.small_transform

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()

    img = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2RGB)
    imgbatch = transform(img).to("cuda")

    with torch.no_grad():
        prediction = midas(imgbatch)
        prediction = torch.nn.functional.interpolate(input=prediction.unsqueeze(1), size=img.shape[:2], mode="bicubic", align_corners=False).squeeze()
        output = prediction.cpu().numpy()
    
    plt.imshow(X=output)
    plt.pause(interval=0.001)
    
    cv2.imshow(winname="CV2Frame", mat=frame)
    if cv2.waitKey(delay=10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()

plt.show()