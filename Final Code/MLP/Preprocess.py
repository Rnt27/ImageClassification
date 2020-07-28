from PIL import Image
import sys

labels = []
# download the train and test Labels for Cifar Dataset (For test set is the same)
# Link: https://www.kaggle.com/c/cifar-10/
f = open("trainLabels.csv")
for line in f:
	labels.append( '"' + line.rstrip().split(',')[1] + '"' )
f.close()

array = []
for i in range(0,32*32):
	for j in ['r','g','b']:
		array.append('"px' + j + str(i) + '"')
array.append('"class"')
print (",".join(arr))



for x in range(1, 50000+1):

	#im = Image.open('train/' + str(x) + '.png').convert('LA')
	im = Image.open('train/' + str(x) + '.png')

	#im.show()
	
	arr = []
	for i in range(0, 32):
		for j in range(0, 32):
			tp = im.getpixel((i,j))
			arr.append( str(tp[0]) )
			arr.append( str(tp[1]) )
			arr.append( str(tp[2]) )
			
	print (",".join(arr) + "," + labels[x])


# conver nominal class lavels to int
df = pd.read_csv('train.csv')
class_mapping = {label: i for i, label in enumerate(np.unique(df['class']))}
class_mapping.to_csv('train', header=None, index=False)