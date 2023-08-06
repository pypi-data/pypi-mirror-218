import os
import cv2
import numpy as np
import pickle
import time
import requests
import shutil
import torch
os.system("pip install scenedetect")
os.system("pip install mega.py")
os.system("pip install timm")
from scenedetect import detect, ContentDetector, split_video_ffmpeg
from mega import Mega

class DataOptimizer():

    def __init__(self, directory):
        self.directory = directory

    def DownloadData(self, urls):
        for i, url in enumerate(urls):
            r = requests.get(url, allow_redirects=True)
            open('Video' + str(i + 1) + '.mp4', 'wb').write(r.content)

    def PrepareData(self):
        if os.path.exists(self.directory + "/Scenes"):
            shutil.rmtree(self.directory + "/Scenes")
        os.mkdir(self.directory + "/Scenes")

        video_files = [f for f in os.listdir(self.directory) if
                       f.endswith(".mp4") or f.endswith(".mkv") or f.endswith(".avi") or f.endswith(
                           ".mov") or f.endswith(".webm")]

        for video_file in video_files:
            video_path = os.path.join(self.directory, video_file)
            scene_list = detect(video_path, ContentDetector())
            os.chdir(self.directory + "/Scenes")
            split_video_ffmpeg(video_path, scene_list, show_progress=True)
            # os.remove(video_path)
        self.directory = self.directory + "/Scenes"

        video_files = [f for f in os.listdir(self.directory) if
                       f.endswith(".mp4") or f.endswith(".mkv") or f.endswith(".avi") or f.endswith(".mov")]
        Train_X = list()
        FirstFrames = list()
        i = 1
        for video_file in video_files:
            FirstFrames.append(i)
            video_path = os.path.join(self.directory, video_file)
            video = cv2.VideoCapture(video_path)

            while video.isOpened():
                ret, frame = video.read()
                if not ret or i == 10000:
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                Train_X.append(frame.reshape(36864, ))

                i += 1

            video.release()
        Train_X = np.array(Train_X).T  # 144x256

        return Train_X, FirstFrames


class Convection3D():
    def __init__(self):
        pass

    def Generate(self, directory=os.getcwd() + "/Scenes"):
        model_type = "DPT_Large"
        midas = torch.hub.load("intel-isl/MiDas", model_type, force_reload=False)
        device = torch.device("cuba") if torch.cuda.is_available() else torch.device("cpu")
        midas.to(device)
        midas.eval()
        midas_transforms = torch.hub.load("intel-isl/MiDas", "transforms")

        if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
            transform = midas_transforms.dpt_transform
        else:
            transform = midas_transforms.small_transform

        video_files = [f for f in os.listdir(directory) if
                       f.endswith(".mp4") or f.endswith(".mkv") or f.endswith(".avi") or f.endswith(".mov")]
        Conv3D = list()
        i = 1
        for video_file in video_files:
            video_path = os.path.join(directory, video_file)
            video = cv2.VideoCapture(video_path)
            while video.isOpened():
                ret, frame = video.read()
                if ret == False or i == 10000:
                    break

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                input_batch = transform(img).to(device)

                with torch.no_grad():
                    prediction = midas(input_batch)
                    prediction = torch.nn.functional.interpolate(
                        prediction.unsqueeze(1),
                        size=img.shape[:2],
                        mode="bicubic",
                        align_corners=False,
                    ).squeeze()

                    depth_map = prediction.cpu().numpy()
                    depth_map = cv2.normalize(depth_map, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_64F)
                    depth_map = (depth_map * 255).astype(np.uint8)
                    Conv3D.append(depth_map.reshape(36864, ))
                    print(i)

                    i += 1

        return np.array(Conv3D).T


class NextFrameGenerator():
    def __init__(self):
        pass

    def Train(self, X, Y, num_iterations=1000, learning_rate=0.01):
        W1 = np.random.randn(40000, 16) * 0.01
        b1 = np.zeros((40000, 1))
        W2 = np.random.randn(1000, 40000) * 0.01
        b2 = np.zeros((1000, 1))
        W3 = np.random.randn(2400, 1000) * 0.01
        b3 = np.zeros((2400, 1))
        W4 = np.random.randn(240, 2400) * 0.01
        b4 = np.zeros((16, 1))
        print("weights init...")

        for i in range(num_iterations):
            # forward prop
            Z1 = np.dot(W1, X) + b1
            A1 = np.maximum(0, Z1)

            Z2 = np.dot(W2, A1) + b2
            A2 = np.maximum(0, Z2)

            Z3 = np.dot(W3, A2) + b3
            A3 = np.maximum(0, Z3)

            Z4 = np.dot(W4, A3) + b4
            A4 = 1 / (1 + np.exp(-Z4))

            # backward prop

            m = X.shape[1]

            dZ4 = A4 - Y

            dW4 = (1 / m) * np.dot(dZ4, A3.T)
            db4 = (1 / m) * np.sum(dZ4, axis=1, keepdims=True)

            dA3 = np.dot(W4.T, dZ4)
            dZ3 = np.multiply(dA3, np.int64(A3 > 0))

            dW3 = (1 / m) * np.dot(dZ3, A2.T)
            db3 = (1 / m) * np.sum(dZ3, axis=1, keepdims=True)

            dA2 = np.dot(W3.T, dZ3)
            dZ2 = np.multiply(dA2, np.int64(A2 > 0))

            dW2 = (1 / m) * np.dot(dZ2, A1.T)
            db2 = (1 / m) * np.sum(dZ2, axis=1, keepdims=True)

            dA1 = np.dot(W2.T, dZ2)
            dZ1 = np.multiply(dA1, np.int64(A1 > 0))

            dW1 = (1 / m) * np.dot(dZ1, X.T)
            db1 = (1 / m) * np.sum(dZ1, axis=1, keepdims=True)

            parameters = (dW1, db1, dW2, db2, dW3, db3, dW4, db4)
            print(i, " iteration finished at - ", time.strftime("%H:%M:%S"))

        file = open("Discriminator.bin", 'wb')
        pickle.dump(parameters, file)

        return parameters

def Sync(urls, device_id):

    global DataOptimizer
    global Convection3D
    global NextFrameGenerator

    Data_Optimizer=DataOptimizer(os.getcwd())
    Data_Optimizer.DownloadData(urls)
    Train_X,FirstFrames=Data_Optimizer.PrepareData()
    Conv3D=Convection3D().Generate()

    file=open(".\\"+device_id+"Train_X.bin",'wb')
    pickle.dump(Train_X,file)
    file.close()
    file=open(".\\"+device_id+"FirstFrames.bin",'wb')
    pickle.dump(FirstFrames,file)
    file.close()
    file=open(".\\"+device_id+"Conv3D.bin",'wb')
    pickle.dump(Conv3D,file)
    file.close()
    print("done")
    mega=Mega()
    log=mega.login("neuronode.bin@gmail.com","getAccessAtNeuroNodeDataStorage")
    log.upload("Train_X.bin")
    log.upload("FirstFrames.bin")
    log.upload("Conv3D.bin")

    # Generator = NextFrameGenerator()
    # Train_D = np.random.randint(0, 255, (241, 10000))
    # Train_D_Y = np.random.randint(0, 1, (240, 10000))
    # print("data loaded...")
    # NextFrameGenerator.Train(Train_D, Train_D_Y)
