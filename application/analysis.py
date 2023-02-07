from matplotlib import pyplot as plt
import numpy as np
import os
current_dir=os.path.abspath(os.path.dirname(__file__))

class analyze:

    def histogram(self,marks):
        a = np.array(marks)
        fig, ax = plt.subplots(figsize =(100, 100))
        ax.hist(a,rwidth=0.5)
        ax.set_xticks([60,70,80,90,100])
        plt.savefig(os.path.join(current_dir,"../static/images/image.png"))

    def preprocess(self,x,y):
        temp=[]
        for i in range(len(x)):
            temp+=[[x[i],y[i]]]
        temp.sort()
        nx=[]
        ny=[]
        for i in temp:
            nx+=[i[0]]
            ny+=[i[1]]
        return nx,ny


    def return_percentile(self,l):
        a=min(l)
        b=max(l)
        a,b=int(a),int(b)
        #print(l)
        print(a,b)
        inter=(b-a)//10
        l=[]
        
        l+=[a-10]
        c=a-10
        for i in range(10):
            l+=[l[-1]+inter]
        l+=[b+10]
        return l

    def plot_an(self,x,y,m):
        plt.clf()
        x,y=analyze().preprocess(x,y)
        plt.plot(x, y)
        print(x,y)
        plt.xlabel(m)
        plt.ylabel('Sale Quantity')
        if max(y)!=min(y):
            plt.xticks(analyze().return_percentile(x))
        plt.title('Product sale analysis '+m+' based')
        plt.savefig(os.path.join(current_dir,"../static/images/image_"+m+".png"))


    