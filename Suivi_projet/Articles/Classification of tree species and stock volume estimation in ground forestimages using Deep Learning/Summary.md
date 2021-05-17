# Ressources
## Contact
xuefeng@ifrit.ac.cn (X. Wang)

## Data & code
The forest images were collected and aren't public but can be made available on request (cf. [Supplementary data 1.](https://ars.els-cdn.com/content/image/1-s2.0-S0168169919308713-mmc1.xml)).

# Subject
## Aim
This paper proposes methods to both apply semantic segmentation on trees in complex environnements such as forests, and estimate the volume of wood in a given area, using deep learning models and base models respectively.

## Challenges
Complex dynamic background environnement makes it difficult to correctly segment trees under all conditions and current solutions either rely on external equipment such as LIDARs or are computionnaly heavy.

# How
## Acquisition
3000 high resolution images were captured in the region of Daxing'anling (120°48′01′′ ~ 121°50′1.52′′E, 51°20′59.18′′ ~ 51°57′41.75′′N), China at various spots, each producing 8 views from a rotating camera taking sots along the polar axis and intermediates (North, Northeast, East etc...)

## Semantic segmentation (SS)
A convolutionnal deep neural network U-Net, pre-trained from VGG16's weights on ImageNet, is used to conduct the semantic segmentation and is compared to other variants of itself (pre-trained from VGG19, VGG11, no pre-training).

The metrics sued were the accuracy, precision, recall and IoU.

## Growth Stock Volume (GSV)
Several base models used to represent trees volume were compared and one, characterizing trees by approximated ellipsoids, was selected. To better match reality, estimations were disturbed with fixed and random effect applied to the model coefficients, different for each tree species, to model the differences of width between species.

The metrics used were the R² and RMSE but the Akaike Information Criterion (AIC, denoted as m(AIC)) and the Bayesian Information Criterion (BIC, denoted as m(BIC)) were also used for the evaluation and comparison of the fitting accuracy of the nonlinear hybrid model


## Results
### SS
| Method        | Accuracy | Precision | Recall |
| ------------- | -------- | --------- | ------ |
| U-Net + VGG16 | 0.9603   | 0.9725    | 0.9568 |

### GSV
| Model | R²   |
| ----- | ----- |
| M3    | 0.680 |

## Critic
The paper is complete and contains enough explaination to precisely reproduce the models thanks to the detailled listing of the parameters and data structure. The benchmarks and parallel studies were thoroughly conducted and sufficiently convincing to justify the selection of technical solutions.

However, this paper doesn't individual tree volume estimation so even though the ideas raised in the GSV part were interesting, they won't be of much use to our project.