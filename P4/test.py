from afinn import Afinn
afinn = Afinn()
score = afinn.score("test testing isolation execution production method risk cloud propose case methods activities software interferences environment fault event solution school providers")
print(score)
score = afinn.score("fca kd rca relational knowledge concept analysis modeling huchard catalog marianne software event datasets patterns montpellier school discovery pattern science")
print(score)
score = afinn.score("founded ba boutique based manette perfect retail 99 mary coffee concordia school suitablee fit pet holiday jordan comics seafood world ")
print(score)