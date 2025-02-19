import torch 
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from torchvision import datasets
from torch.utils.data import DataLoader
import model as mod 
import train 
import evaluation 
import visualisation as v



# Définissez les transformations
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)) # normalisation de la base de données 
])

# Téléchargement du dataset MNIST
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)


# creation des data loader 
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)






                    ###############################################################
                                            #entrainement


model = mod.Net().to("cpu")
optimizer = torch.optim.Adam(model.parameters())

for epoch in range(1):  # Nombre d'époques
    train.ftrain(model,"cpu", train_loader, optimizer, epoch)

                    ###############################################################
                                            # evaluation


device = "cpu"
model.to(device)
evaluation.evaluate_model(model, test_loader, device)




                    ################################################################
                                        # test 

def test(image,model):
    model.eval()
    with torch.no_grad():
        output=model(image)
        _,predicted=torch.max(output,1)
        print("prediction ============> ",predicted[0].item())



# on effectue le teste sur une image du data set de test 

images,label=next(iter(test_loader))
image=images[2].unsqueeze(0)
v.afficher_image(image)
test(image,model)
print("resultat attendus : ",label[2].item())




