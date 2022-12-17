AI Journey
==========

Notes, todos, and misc.

1. [Mar 18 2018] Cnn feature and rnn feature distribution problem.

..

  pcolor(randn() * randn()) -- looks good
  pcolor(rand() * rand())   -- vertical and horizontal strips
  pcolor(randn() * rand())
  pcolor(rand() * randn())
  
Why should this happen? This problem hampers joint embedding learning
because under the learning / optimization process of pairwise ranking loss
the cnn features and rnn features will attract each other, and each pair
of feature will be close to each other. Since there are obvious strips
that leads rnn feature to be inferior, the cnn dimension reduction linear
layer would be influenced to produce bad cnn feature too.