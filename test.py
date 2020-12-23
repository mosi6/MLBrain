import idx2numpy
from machineLearn3 import *
import matplotlib.pyplot as plt
import json
a=5
# Reading
Test_images = idx2numpy.convert_from_file('Test_images.idx3-ubyte')
Test_labels = idx2numpy.convert_from_file('Test_labels.idx1-ubyte')
#print(Test_images[a])
for i in range(50):
    plt.imshow(Test_images[i], cmap = plt.cm.gray_r, interpolation = 'nearest')
    print(Test_labels[i])
    plt.show()
Test_labels = fix_targets(Test_labels, 10)
testt = np.array([Test_images[a].flatten()])
Test_images = np.array([i.flatten() for i in Test_images])
parameters=ReadDict(name="NNt")
#model_test(parameters, Test_images, Test_labels)
apply_on_example(testt,parameters)


plt.show()
