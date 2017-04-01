\* The supported bandwidth maximization problem *\
Maximize
OBJ: b_(Amsterdam,Milan)_1 + b_(Amsterdam,Milan)_2 + b_(Paris,Copenhagen)_1
 + b_(Paris,Copenhagen)_2 + b_(Praque,Paris)_1 + b_(Praque,Paris)_2
 + b_(London,Praque)_1 + b_(London,Praque)_2
Subject To
b_indicator_(Amsterdam,Milan)_1: 0.0666666666667 b_(Amsterdam,Milan)_1
 - v_(Amsterdam,Milan)_1 <= 0
b_indicator_(Amsterdam,Milan)_2: 0.0666666666667 b_(Amsterdam,Milan)_2
 - v_(Amsterdam,Milan)_2 <= 0
b_indicator_(London,Praque)_1: 0.0769230769231 b_(London,Praque)_1
 - v_(London,Praque)_1 <= 0
b_indicator_(London,Praque)_2: 0.0769230769231 b_(London,Praque)_2
 - v_(London,Praque)_2 <= 0
b_indicator_(Paris,Copenhagen)_1: 0.0833333333333 b_(Paris,Copenhagen)_1
 - v_(Paris,Copenhagen)_1 <= 0
b_indicator_(Paris,Copenhagen)_2: 0.0833333333333 b_(Paris,Copenhagen)_2
 - v_(Paris,Copenhagen)_2 <= 0
b_indicator_(Praque,Paris)_1: 0.04 b_(Praque,Paris)_1 - v_(Praque,Paris)_1
 <= 0
b_indicator_(Praque,Paris)_2: 0.04 b_(Praque,Paris)_2 - v_(Praque,Paris)_2
 <= 0
no_split_(Amsterdam,Milan): v_(Amsterdam,Milan)_1 + v_(Amsterdam,Milan)_2 <= 1
no_split_(London,Praque): v_(London,Praque)_1 + v_(London,Praque)_2 <= 1
no_split_(Paris,Copenhagen): v_(Paris,Copenhagen)_1 + v_(Paris,Copenhagen)_2
 <= 1
no_split_(Praque,Paris): v_(Praque,Paris)_1 + v_(Praque,Paris)_2 <= 1
traf_const(Amsterdam,Milan): b_(Amsterdam,Milan)_1 + b_(Amsterdam,Milan)_2
 <= 15
traf_const(London,Praque): b_(London,Praque)_1 + b_(London,Praque)_2 <= 13
traf_const(Paris,Copenhagen): b_(Paris,Copenhagen)_1 + b_(Paris,Copenhagen)_2
 <= 12
traf_const(Praque,Paris): b_(Praque,Paris)_1 + b_(Praque,Paris)_2 <= 25
wave_cap(Amsterdam,Berlin): c_(Amsterdam,Berlin) <= 2
wave_cap(Amsterdam,Brussels): c_(Amsterdam,Brussels) <= 2
wave_cap(Amsterdam,Copenhagen): c_(Amsterdam,Copenhagen) <= 2
wave_cap(Amsterdam,London): c_(Amsterdam,London) <= 2
wave_cap(Amsterdam,Luxembourg): c_(Amsterdam,Luxembourg) <= 2
wave_cap(Berlin,Amsterdam): c_(Berlin,Amsterdam) <= 2
wave_cap(Berlin,Copenhagen): c_(Berlin,Copenhagen) <= 2
wave_cap(Berlin,Paris): c_(Berlin,Paris) <= 2
wave_cap(Berlin,Praque): c_(Berlin,Praque) <= 2
wave_cap(Berlin,Vienna): c_(Berlin,Vienna) <= 2
wave_cap(Brussels,Amsterdam): c_(Brussels,Amsterdam) <= 2
wave_cap(Brussels,London): c_(Brussels,London) <= 2
wave_cap(Brussels,Luxembourg): c_(Brussels,Luxembourg) <= 2
wave_cap(Brussels,Milan): c_(Brussels,Milan) <= 2
wave_cap(Brussels,Paris): c_(Brussels,Paris) <= 2
wave_cap(Copenhagen,Amsterdam): c_(Copenhagen,Amsterdam) <= 2
wave_cap(Copenhagen,Berlin): c_(Copenhagen,Berlin) <= 2
wave_cap(Copenhagen,London): c_(Copenhagen,London) <= 2
wave_cap(Copenhagen,Praque): c_(Copenhagen,Praque) <= 2
wave_cap(London,Amsterdam): c_(London,Amsterdam) <= 2
wave_cap(London,Brussels): c_(London,Brussels) <= 2
wave_cap(London,Copenhagen): c_(London,Copenhagen) <= 2
wave_cap(London,Paris): c_(London,Paris) <= 2
wave_cap(Luxembourg,Amsterdam): c_(Luxembourg,Amsterdam) <= 2
wave_cap(Luxembourg,Brussels): c_(Luxembourg,Brussels) <= 2
wave_cap(Luxembourg,Paris): c_(Luxembourg,Paris) <= 2
wave_cap(Luxembourg,Praque): c_(Luxembourg,Praque) <= 2
wave_cap(Luxembourg,Zurich): c_(Luxembourg,Zurich) <= 2
wave_cap(Milan,Brussels): c_(Milan,Brussels) <= 2
wave_cap(Milan,Paris): c_(Milan,Paris) <= 2
wave_cap(Milan,Vienna): c_(Milan,Vienna) <= 2
wave_cap(Milan,Zurich): c_(Milan,Zurich) <= 2
wave_cap(Paris,Berlin): c_(Paris,Berlin) <= 2
wave_cap(Paris,Brussels): c_(Paris,Brussels) <= 2
wave_cap(Paris,London): c_(Paris,London) <= 2
wave_cap(Paris,Luxembourg): c_(Paris,Luxembourg) <= 2
wave_cap(Paris,Milan): c_(Paris,Milan) <= 2
wave_cap(Paris,Zurich): c_(Paris,Zurich) <= 2
wave_cap(Praque,Berlin): c_(Praque,Berlin) <= 2
wave_cap(Praque,Copenhagen): c_(Praque,Copenhagen) <= 2
wave_cap(Praque,Luxembourg): c_(Praque,Luxembourg) <= 2
wave_cap(Praque,Vienna): c_(Praque,Vienna) <= 2
wave_cap(Praque,Zurich): c_(Praque,Zurich) <= 2
wave_cap(Vienna,Berlin): c_(Vienna,Berlin) <= 2
wave_cap(Vienna,Milan): c_(Vienna,Milan) <= 2
wave_cap(Vienna,Praque): c_(Vienna,Praque) <= 2
wave_cap(Vienna,Zurich): c_(Vienna,Zurich) <= 2
wave_cap(Zurich,Luxembourg): c_(Zurich,Luxembourg) <= 2
wave_cap(Zurich,Milan): c_(Zurich,Milan) <= 2
wave_cap(Zurich,Paris): c_(Zurich,Paris) <= 2
wave_cap(Zurich,Praque): c_(Zurich,Praque) <= 2
wave_cap(Zurich,Vienna): c_(Zurich,Vienna) <= 2
wave_chan(Amsterdam,Berlin): 0.25 b_(Amsterdam,Milan)_2 - c_(Amsterdam,Berlin)
 <= 0
wave_chan(Amsterdam,Brussels): 0.25 b_(Amsterdam,Milan)_1
 - c_(Amsterdam,Brussels) <= 0
wave_chan(Berlin,Copenhagen): 0.25 b_(Paris,Copenhagen)_1
 - c_(Berlin,Copenhagen) <= 0
wave_chan(Berlin,Praque): 0.25 b_(London,Praque)_2 - c_(Berlin,Praque) <= 0
wave_chan(Berlin,Vienna): 0.25 b_(Amsterdam,Milan)_2 - c_(Berlin,Vienna) <= 0
wave_chan(Brussels,Milan): 0.25 b_(Amsterdam,Milan)_1 - c_(Brussels,Milan)
 <= 0
wave_chan(Copenhagen,Berlin): 0.25 b_(London,Praque)_2 - c_(Copenhagen,Berlin)
 <= 0
wave_chan(Copenhagen,Praque): 0.25 b_(London,Praque)_1 - c_(Copenhagen,Praque)
 <= 0
wave_chan(London,Copenhagen): 0.25 b_(Paris,Copenhagen)_2
 + 0.25 b_(London,Praque)_1 + 0.25 b_(London,Praque)_2 - c_(London,Copenhagen)
 <= 0
wave_chan(Luxembourg,Paris): 0.25 b_(Praque,Paris)_1 - c_(Luxembourg,Paris)
 <= 0
wave_chan(Paris,Berlin): 0.25 b_(Paris,Copenhagen)_1 - c_(Paris,Berlin) <= 0
wave_chan(Paris,London): 0.25 b_(Paris,Copenhagen)_2 - c_(Paris,London) <= 0
wave_chan(Praque,Luxembourg): 0.25 b_(Praque,Paris)_1 - c_(Praque,Luxembourg)
 <= 0
wave_chan(Praque,Zurich): 0.25 b_(Praque,Paris)_2 - c_(Praque,Zurich) <= 0
wave_chan(Vienna,Milan): 0.25 b_(Amsterdam,Milan)_2 - c_(Vienna,Milan) <= 0
wave_chan(Zurich,Paris): 0.25 b_(Praque,Paris)_2 - c_(Zurich,Paris) <= 0
Bounds
0 <= b_(Praque,Paris)_2
0 <= b_(Amsterdam,Milan)_1
0 <= c_(Zurich,Vienna)
0 <= b_(Paris,Copenhagen)_2
0 <= c_(Zurich,Paris)
0 <= c_(Praque,Copenhagen)
0 <= b_(Paris,Copenhagen)_1
0 <= c_(Zurich,Milan)
0 <= b_(London,Praque)_1
0 <= c_(Praque,Berlin)
0 <= c_(Berlin,Copenhagen)
0 <= c_(Paris,Milan)
0 <= c_(Milan,Zurich)
0 <= b_(Amsterdam,Milan)_2
0 <= c_(Luxembourg,Brussels)
0 <= c_(Praque,Luxembourg)
0 <= c_(Zurich,Luxembourg)
0 <= c_(Paris,London)
0 <= c_(Luxembourg,Paris)
0 <= c_(Luxembourg,Zurich)
0 <= c_(Berlin,Amsterdam)
0 <= c_(London,Amsterdam)
0 <= c_(Zurich,Praque)
0 <= c_(Amsterdam,Luxembourg)
0 <= c_(Berlin,Praque)
0 <= c_(Praque,Zurich)
0 <= c_(Paris,Brussels)
0 <= c_(London,Paris)
0 <= c_(Amsterdam,Copenhagen)
0 <= c_(Paris,Luxembourg)
0 <= c_(Copenhagen,Amsterdam)
0 <= c_(Milan,Brussels)
0 <= c_(Amsterdam,Brussels)
0 <= c_(Berlin,Vienna)
0 <= c_(London,Copenhagen)
0 <= b_(Praque,Paris)_1
0 <= c_(Luxembourg,Praque)
0 <= c_(Amsterdam,London)
0 <= c_(Paris,Zurich)
0 <= c_(Paris,Berlin)
0 <= c_(Luxembourg,Amsterdam)
0 <= c_(Copenhagen,Praque)
0 <= c_(Amsterdam,Berlin)
0 <= c_(Milan,Vienna)
0 <= c_(Berlin,Paris)
0 <= c_(Praque,Vienna)
0 <= b_(London,Praque)_2
0 <= c_(London,Brussels)
0 <= c_(Milan,Paris)
0 <= c_(Brussels,Paris)
0 <= c_(Brussels,London)
0 <= c_(Brussels,Milan)
0 <= c_(Brussels,Amsterdam)
0 <= c_(Copenhagen,London)
0 <= c_(Vienna,Milan)
0 <= c_(Vienna,Berlin)
0 <= c_(Vienna,Zurich)
0 <= c_(Vienna,Praque)
0 <= c_(Brussels,Luxembourg)
0 <= c_(Copenhagen,Berlin)
Generals
b_(Praque,Paris)_2
b_(Amsterdam,Milan)_1
c_(Zurich,Vienna)
b_(Paris,Copenhagen)_2
c_(Zurich,Paris)
c_(Praque,Copenhagen)
b_(Paris,Copenhagen)_1
c_(Zurich,Milan)
b_(London,Praque)_1
c_(Praque,Berlin)
c_(Berlin,Copenhagen)
c_(Paris,Milan)
c_(Milan,Zurich)
b_(Amsterdam,Milan)_2
c_(Luxembourg,Brussels)
c_(Praque,Luxembourg)
c_(Zurich,Luxembourg)
c_(Paris,London)
c_(Luxembourg,Paris)
c_(Luxembourg,Zurich)
c_(Berlin,Amsterdam)
c_(London,Amsterdam)
c_(Zurich,Praque)
c_(Amsterdam,Luxembourg)
c_(Berlin,Praque)
c_(Praque,Zurich)
c_(Paris,Brussels)
c_(London,Paris)
c_(Amsterdam,Copenhagen)
c_(Paris,Luxembourg)
c_(Copenhagen,Amsterdam)
c_(Milan,Brussels)
c_(Amsterdam,Brussels)
c_(Berlin,Vienna)
c_(London,Copenhagen)
b_(Praque,Paris)_1
c_(Luxembourg,Praque)
c_(Amsterdam,London)
c_(Paris,Zurich)
c_(Paris,Berlin)
c_(Luxembourg,Amsterdam)
c_(Copenhagen,Praque)
c_(Amsterdam,Berlin)
c_(Milan,Vienna)
c_(Berlin,Paris)
c_(Praque,Vienna)
b_(London,Praque)_2
c_(London,Brussels)
c_(Milan,Paris)
c_(Brussels,Paris)
c_(Brussels,London)
c_(Brussels,Milan)
c_(Brussels,Amsterdam)
c_(Copenhagen,London)
c_(Vienna,Milan)
c_(Vienna,Berlin)
c_(Vienna,Zurich)
c_(Vienna,Praque)
c_(Brussels,Luxembourg)
c_(Copenhagen,Berlin)
Binaries
v_(Paris,Copenhagen)_2
v_(Paris,Copenhagen)_1
v_(Praque,Paris)_1
v_(London,Praque)_2
v_(Amsterdam,Milan)_2
v_(Praque,Paris)_2
v_(Amsterdam,Milan)_1
v_(London,Praque)_1
End
