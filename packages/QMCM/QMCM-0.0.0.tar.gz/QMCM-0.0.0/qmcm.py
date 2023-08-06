#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
import numpy as np

# label_encoder = LabelEncoder()
# label = label_encoder.fit_transform(label)
y_train = np.array([-1,1])
x_train = np.array([[1,1],[0,1]])
# scaler = MinMaxScaler()
# x_train = scaler.fit_transform(x_train)
# svm_model = SVM() 

x1 = np.random.randn(5, 2) + np.array([2, 2])
x2 = np.random.randn(5, 2) + np.array([-2, -2])
x_train = np.concatenate((x1, x2))
y_train = y = np.array([1] * 5 + [-1] * 5)
print("x value",x_train)
print()

model2 = svm.SVC(kernel='linear')

model2.fit(x_train,y_train)
# y2 = model2.predict(x_train)
# print(y2)
print("Weight vector using sklearn:",model2.coef_)
print("Bias using sklearn:",model2.intercept_)


# In[2]:


class SVM:
    
    def __init__(self, learning_rate=0.001, lambda_param=0.01, epochs=1000):
        self.lr = learning_rate # 𝛼 in formula
        self.lambda_param = lambda_param
        self.epochs = epochs 
        self.w = None
        self.b = None

    def fit(self, X, y):
        n_samples, n_features = X.shape

        self.w = np.zeros(n_features)
        self.b = 0

        for _ in range(self.epochs):
            for idx, x_i in enumerate(X):
                self.update(x_i, y[idx])
        return self.w, self.b
    
    def update(self,x,y):
        distance = 1 - (y * (np.dot(x, self.w) + self.b))
        hinge_loss = max(0,distance)
        if(hinge_loss == 0):
            self.w = self.w - self.lr * (2 * self.lambda_param * self.w)
            print("Weight here")
        else: 
            self.w = self.w - self.lr * (2 * self.lambda_param * self.w - np.dot(x,y))
            self.b = self.b + self.lr * y
            print("Bias here")
        
        
    def predict(self, X):
        eq = np.dot(X, self.w) + self.b
        return np.sign(eq)


# In[3]:


svm_model = SVM() 
print("x value",x_train)
print()
svm_model.__init__()
weight,bias = svm_model.fit(x_train,y_train)
print(weight)
print(bias)


# Stochastic Subgradient descent QMCM

# In[4]:


print((x_train).shape)
print(y_train.shape)
print(type(y_train))


# In[5]:


import numpy as np

def compute_f(x,y,w,z,R):
    C = 1.75
    D = 2.50
    M = x.shape[0]
    first = 0
    second = 0
    third = 0
    four = 0
    five = 0
    six = 0
    
    e_T = np.ones(shape=(len(z),))
    first = (np.dot(e_T, z))*R
    print("first:",first)
    
    for i in range(M):
#         print((w.transpose() * x[i]))
#         print(x[i])
        second = second + (np.maximum(0,1-y[i]*np.dot(x[i],w.transpose())))**2
        print("Value of y[i]:",y[i])
        print("Value of x[i]:",x[i])
        print("Value of w.transpose():",w.transpose())
        print("Intermediate value:",1-y[i]*np.dot(x[i],w.transpose()))
    second = C*second
    second = second/(2*M)
    print("second:",second)
    for i in range(M):
        third = third + max((0,np.linalg.norm(x[i],ord=2)- R))**2
    
    third = (D/2)*(third/M)
    print("third:",third)    
    fourth = (np.sum(w-z)**2)/2
    fourth = np.maximum(0,fourth)
    print(fourth)
    print("fourth:",fourth)
    fifth = (np.sum(-w-z)**2)/2
    print(fifth)
    fifth = np.maximum(0,fifth)
    print("fifth:",fifth)
    sixth = (np.sum(-z)**2)/2
    print(sixth)
    sixth = np.maximum(0,sixth)
    print("sixth",sixth)
    F = first+second+third+fourth+fifth+sixth
    
    return F     

compute_f(x_train,y_train,np.array([-25,-7]),np.array([-2,-12]),7)


# In[6]:


a  = [[1,2],[3,2],[4,5]]
R = 10
b = np.linalg.norm(a[0], ord=2)
print(b)


# In[7]:


def get_x(x_idx,y_idx,w):
    if np.dot(y_idx,np.dot(w.transpose(),x_idx)) <= 1:
        return x_idx
    else:
        return np.zeros(shape=(len(x_idx),))

def compute_gradient_wrt_w(x,y,w,z,R):
    C = 1.75
    M = x.shape[0]
    n = x.shape[1]
    print("The shape of z is:",z.shape)             
    total = 0
    x_cap = np.zeros_like(x)
    
    for i in range(M):
        x_cap[i] = get_x(x[i],y[i],w)
        total = (1 - np.dot(y[i],(np.dot(w.transpose(),x_cap[i]))))
        total = np.dot(y[i],total)
        total += total*x_cap[i] #This should be a vector of size of w.
        
    total = (-C/M)*total
    total_iterations = z.shape[0]
    for k in range(total_iterations):
        if w[k] >= z[k] and w[k] >= 0:

            first = total + (w[k] - z[k])

            return first

        elif w[k] <= -z[k] and w[k] <= 0:

            second = total + (w[k] + z[k])

            return second


        elif -z[k] <= w[k] and w[k] <= z[k]:

            return total
print(get_x(x_train[1],y_train[1],np.array([-3,1])))    
print(compute_gradient_wrt_w(x_train,y_train,np.array([4,6]),np.array([5,6]),2))


# In[8]:


# def compute_gradient_wrt_z(k, w, z, R):
#     if w[k] >= z[k] and w[k] >= 0 and z[k] > 0:
        
#         return (R - (w[k] - z[k]))
    
#     elif w[k] >= z[k] and w[k] >= 0 and z[k] < 0:
        
#         return (R - (w[k] - z[k]) + z[k])
    
#     elif w[k] <= -z[k] and w[k] <= 0 and z[k] > 0:
        
#         return (R + (w[k] + z[k]))
    
#     elif w[k] <= -z[k] and w[k] <= 0 and z[k] < 0:
        
#         return (R + (w[k] + z[k]) + z[k])    
    
#     elif -z[k] <= w[k] and w[k] <= z[k] and z[k] > 0:
        
#         return R
    
#     elif -z[k] <= w[k] and w[k] <= z[k] and z[k] < 0:
        
#         return (R + z[k])
#     return 0 # without this the last function gives an error
# compute_gradient_wrt_z(2,np.array([0,0,1]),np.array([-2,-4,-5]),3)


# In[9]:


def compute_gradient_wrt_z(w, z, R):
    total_iterations = z.shape[0]
    for k in range(total_iterations):       
        
        if w[k] >= z[k] and w[k] >= 0 and z[k] != 0:
            if z[k] > 0:
                return (R - (w[k] - z[k]))
            else:
                return (R - (w[k] - z[k]) + z[k])

        elif w[k] <= -z[k] and w[k] <= 0 and z[k] != 0:
            if z[k] > 0:
                return (R + (w[k] + z[k]))
            else:
                return (R + (w[k] + z[k]) + z[k])

        elif -z[k] <= w[k] and w[k] <= z[k] and z[k] != 0:
            if z[k] > 0:
                return R
            else:
                return (R + z[k])
        return 0
        
compute_gradient_wrt_z(np.array([0,0,1]),np.array([-2,-4,-5]),3)


# In[10]:


def get_x_of_R(x_cap,R):
    norm2 = np.linalg.norm(x_cap,ord=2)
    if R <= norm2:
        return x_cap
    else:
        return np.zeros(shape=(len(x_cap),))
    
def compute_gradient_wrt_R(updated_x_cap,z, R) :
    D = 2.5
    M2 = 10
    e_T = np.ones(shape=(len(z),))
    first = np.dot(e_T,z)
    
    total_norm = 0
    length = len(updated_x_cap)
    if length < M2:
        M2 = length
    
    for i in range(M2):
        total_norm += np.linalg.norm(get_x_of_R(updated_x_cap[i],R),ord=2)
    
    second = (-D/M2)*(total_norm - R)
    
    return first + second

compute_gradient_wrt_R(x_train,np.array([42,31,24]),32)


# In[11]:


def update_variables(w, z, R, grad_w, grad_z, grad_R, eta):
    w = w - eta*grad_w
    
    z = z - eta*grad_z
    print("The new value of z is ",z)
    R = R - eta*grad_R
    
    return w,z,R

update_variables(np.array([4,3,2,1]),np.array([5,4,6,2]),3,2,0,14,75)


# In[12]:


def QMCM_SGD(x,y,theta,eta=0.75,tolerance=0.01,iter_max=10):
    if theta > 0:
        x = np.hstack((x, np.ones((x.shape[0],1))))
        
        num_features,num_samples = x.shape[1],x.shape[0]
        
        t = 0
        
        w = np.zeros(num_features)
        z = np.random.rand(num_features)
        
        R = np.max(np.linalg.norm(x,axis=1))
        f = compute_f(x,y,w,z,R)
        print("f:",f)
        
        f_prev = 10000
        batch_size = 2
        
        while t <= iter_max and np.abs(f-f_prev) >= tolerance:
            np.random.shuffle(x)
            x_t = x[:batch_size]
            y_t = y[:batch_size]
            
            grad_w = compute_gradient_wrt_w(x_t, y_t, w, z, R)
            
            grad_z = compute_gradient_wrt_z(w, z, R)
            
            grad_R = compute_gradient_wrt_R(x_t, z, R) 
            
            w, z, R = update_variables(w, z, R, grad_w, grad_z, grad_R, eta)
            print("z here:",z)
            f_new = compute_f(x,y,w,z,R)
            print("f_new",f_new)
            
            if np.abs(f-f_prev) < tolerance:
                return f_new,w,z,R
            else:
                f_prev = f
            
            f = compute_f(x, y, w, z, R)
            
            t += 1
            
            eta /= t
        
    return f,w,z,R
        
f,w,z,R = QMCM_SGD(x_train,y_train,0.5,0.75,0.02,15)        
print("Value of f:",f)
print("Value of w:",w)
print("Value of z:",z)
print("Value of R:",R)


# In[13]:


f,w,z,R = QMCM_SGD(x_train,y_train,0.5,0.75,0.01,30)        
print("Value of f:",f)
print("Value of w:",w)
print("Value of z:",z)
print("Value of R:",R)


# In[14]:


# from scipy.optimize import minimize

# def objective_function(wz, x_train, y_train, w, z, R):
#     F = compute_f(x_train, y_train, w, z, R)
#     return F
# print(x_train.shape)

# ones = np.ones((x_train.shape[0], 1))
# x_train_new = np.append(x_train, ones, axis=1)

# print(x_train_new.shape)

# # Define the initial guess for w and z
# initial_wz = np.array([-25, -2, -12, -21]) 
# arr1 = np.array([-25, -2])
# print(arr1.shape)
# # Call the minimize function
# result = minimize(objective_function, args=(x_train_new, y_train, np.random.rand(3,), np.random.rand(3,), 360800), x0=np.random.rand(6,))


# print('Optimized objective function value:', result.fun)

# # Optimized w and z values
# optimal_wz = result.x
# optimal_w = optimal_wz[:3]
# optimal_z = optimal_wz[3:]
# print('Optimized w:', optimal_w)
# print('Optimized z:', optimal_z)


# In[15]:


import numpy as np
from scipy.optimize import minimize

# # Given x_train array with shape (10, 2)
# x_train = np.random.rand(10, 2)
# print(x_train.shape)

# Append ones column to x_train
ones = np.ones((x_train.shape[0], 1))
x_train_new = np.append(x_train, ones, axis=1)

print(x_train_new.shape)

# Rest of your code
def objective_function(wz, x_train, y_train, w, z, R):
    F = compute_f(x_train, y_train, w, z, R)
    return F

initial_wz = np.array([-25, -2, -12, -21]) 
arr1 = np.array([-25, -2])
print(arr1.shape)

result = minimize(objective_function, args=(x_train_new, y_train, np.random.rand(3,), np.random.rand(3,), 7), x0=np.random.rand(6,), options={'disp': True})
print('Optimized objective function value:', result.fun)

optimal_wz = result.x
optimal_w = optimal_wz[:3]
optimal_z = optimal_wz[3:]
print('Optimized w:', optimal_w)
print('Optimized z:', optimal_z)


# In[16]:


#w1 0.35 0.34
#bias 0.117


# In[17]:


optimal_w.shape


# In[18]:


print(w)


# In[19]:


compute_gradient_wrt_w(x_train,y_train,np.array([4,6]),np.array([5,6]),2)

