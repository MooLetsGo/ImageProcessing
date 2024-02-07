import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def run(image, result,settings=None):
    data=np.sin(np.arange(0,100,0.5))
    print(data)
    result.append({"name":"Plot","data":data})

if __name__ == '__main__':
    matplotlib.use('Agg')
    image=cv2.imread("..\Images\Objekte.png")
    result=[]
    run(image,result)
    for ele in result:
        if(len(ele["data"].shape)==1):
            fig=plt.figure(num=ele["name"])
            plt.plot(ele["data"])
            fig.tight_layout()
            plt.grid(True)
            plt.xlim(0.0, len(ele["data"])-1)
            fig.canvas.draw()
            data = np.array(fig.canvas.renderer._renderer)
            cv2.imshow(ele["name"],data)
        else:
            cv2.imshow(ele["name"],ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()